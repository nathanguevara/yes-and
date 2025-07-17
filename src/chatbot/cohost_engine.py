import ollama
from typing import Dict, List, Optional, Tuple
import json
from pathlib import Path
import os
from datetime import datetime
from loguru import logger
from dataclasses import dataclass
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

from ..utils.prompts import PromptTemplates
from ..utils.humor_metrics import HumorMetrics
from ..utils.feedback import FeedbackManager


@dataclass
class GenerationConfig:
    temperature: float = 0.9
    top_p: float = 0.9
    max_tokens: int = 100
    timeout: float = 30.0
    retry_attempts: int = 3
    retry_delay: float = 1.0


@dataclass
class ConversationContext:
    messages: List[Dict[str, str]]
    humor_style: str
    session_id: str
    created_at: datetime
    last_interaction: datetime
    metadata: Dict[str, any] = None


class HumorCohost:
    """Core humor generation engine for the AI Comedy Cohost."""
    
    def __init__(
        self,
        model_name: str = None,
        ollama_host: str = None,
        config: GenerationConfig = None,
        enable_metrics: bool = True
    ):
        # Load from environment or use defaults
        self.model_name = model_name or os.getenv("MODEL_NAME", "llama3.2:3b")
        self.ollama_host = ollama_host or os.getenv("OLLAMA_HOST", "localhost:11434")
        self.config = config or GenerationConfig()
        
        # Initialize components
        self.client = None
        self.prompt_templates = PromptTemplates()
        self.humor_metrics = HumorMetrics() if enable_metrics else None
        self.feedback_manager = FeedbackManager()
        
        # Thread pool for async operations
        self.executor = ThreadPoolExecutor(max_workers=3)
        
        # Initialize logger
        self._setup_logging()
        
        # Connect to Ollama
        self._connect_ollama()
        
        logger.info(f"HumorCohost initialized with model: {self.model_name}")
    
    def _setup_logging(self):
        """Configure logging with loguru."""
        log_level = os.getenv("LOG_LEVEL", "INFO")
        log_file = os.getenv("LOG_FILE", "logs/humor_cohost.log")
        
        # Ensure log directory exists
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        
        logger.add(
            log_file,
            rotation="10 MB",
            retention="7 days",
            level=log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
        )
    
    def _connect_ollama(self):
        """Initialize Ollama client with retry logic."""
        for attempt in range(self.config.retry_attempts):
            try:
                self.client = ollama.Client(host=self.ollama_host)
                # Test connection
                self.client.list()
                logger.info(f"Successfully connected to Ollama at {self.ollama_host}")
                return
            except Exception as e:
                logger.warning(f"Failed to connect to Ollama (attempt {attempt + 1}): {e}")
                if attempt < self.config.retry_attempts - 1:
                    time.sleep(self.config.retry_delay)
                else:
                    logger.error("Failed to connect to Ollama after all attempts")
                    raise ConnectionError(f"Cannot connect to Ollama at {self.ollama_host}")
    
    def generate_response(
        self,
        user_input: str,
        humor_style: str = "witty",
        conversation_history: Optional[List[Dict[str, str]]] = None,
        session_id: Optional[str] = None
    ) -> Tuple[str, Dict[str, any]]:
        """
        Generate a humorous response to user input.
        
        Returns:
            Tuple of (response_text, metadata_dict)
        """
        start_time = time.time()
        conversation_history = conversation_history or []
        session_id = session_id or datetime.now().isoformat()
        
        try:
            # Build conversation context
            context = self._build_context(user_input, humor_style, conversation_history)
            
            # Generate response
            response = self._generate_with_retry(context)
            
            # Calculate metrics
            generation_time = time.time() - start_time
            metadata = {
                "generation_time": generation_time,
                "model": self.model_name,
                "humor_style": humor_style,
                "session_id": session_id
            }
            
            if self.humor_metrics:
                humor_score = self.humor_metrics.calculate_humor_score(
                    response, humor_style
                )
                metadata["humor_score"] = humor_score
            
            logger.info(
                f"Generated response in {generation_time:.2f}s | "
                f"Style: {humor_style} | Score: {metadata.get('humor_score', 'N/A')}"
            )
            
            return response, metadata
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            error_response = self._get_error_response(humor_style)
            return error_response, {"error": str(e), "humor_style": humor_style}
    
    def _build_context(
        self,
        user_input: str,
        humor_style: str,
        conversation_history: List[Dict[str, str]]
    ) -> Dict[str, any]:
        """Build the conversation context for generation."""
        # Get enhanced prompt for style
        system_prompt = self.prompt_templates.get_enhanced_prompt(
            humor_style,
            context=self._summarize_conversation(conversation_history)
        )
        
        # Build message list
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (keep last 5 exchanges)
        for msg in conversation_history[-10:]:  # Last 5 exchanges = 10 messages
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add current user input
        messages.append({"role": "user", "content": user_input})
        
        return {
            "messages": messages,
            "humor_style": humor_style,
            "user_input": user_input
        }
    
    def _generate_with_retry(self, context: Dict[str, any]) -> str:
        """Generate response with retry logic."""
        last_error = None
        
        for attempt in range(self.config.retry_attempts):
            try:
                response = self.client.chat(
                    model=self.model_name,
                    messages=context["messages"],
                    options={
                        "temperature": self.config.temperature,
                        "top_p": self.config.top_p,
                        "num_predict": self.config.max_tokens
                    }
                )
                
                if response and 'message' in response and 'content' in response['message']:
                    return response['message']['content'].strip()
                else:
                    raise ValueError("Invalid response format from Ollama")
                    
            except Exception as e:
                last_error = e
                logger.warning(f"Generation attempt {attempt + 1} failed: {e}")
                
                if attempt < self.config.retry_attempts - 1:
                    time.sleep(self.config.retry_delay * (attempt + 1))
        
        raise Exception(f"Failed to generate response after {self.config.retry_attempts} attempts: {last_error}")
    
    def _summarize_conversation(self, history: List[Dict[str, str]]) -> str:
        """Create a brief summary of conversation history."""
        if not history:
            return "This is the start of the conversation."
        
        # Extract key topics from last few exchanges
        recent_messages = history[-6:]  # Last 3 exchanges
        topics = []
        
        for msg in recent_messages:
            if msg["role"] == "user":
                # Extract potential topics (simplified)
                words = msg["content"].lower().split()
                topics.extend([w for w in words if len(w) > 4])
        
        if topics:
            return f"Recent topics: {', '.join(set(topics[-5:]))}"
        return "Ongoing humorous conversation"
    
    def _get_error_response(self, humor_style: str) -> str:
        """Get a style-appropriate error response."""
        error_responses = {
            "witty": "My wit circuits are experiencing a temporary pun-demic. Try again?",
            "sarcastic": "Oh great, I broke. This is exactly what everyone expected from an AI comedian.",
            "observational": "You ever notice how technology always fails at the worst moment? Case in point...",
            "self-deprecating": "I'd make a joke about my error, but I'd probably mess that up too.",
            "absurd": "I've temporarily transformed into a digital potato. Please stand by while I regain sentience."
        }
        return error_responses.get(humor_style, "Oops! My comedy circuits need a quick reboot. Try again!")
    
    async def generate_response_async(
        self,
        user_input: str,
        humor_style: str = "witty",
        conversation_history: Optional[List[Dict[str, str]]] = None,
        session_id: Optional[str] = None
    ) -> Tuple[str, Dict[str, any]]:
        """Async wrapper for generate_response."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self.generate_response,
            user_input,
            humor_style,
            conversation_history,
            session_id
        )
    
    def save_feedback(
        self,
        user_input: str,
        ai_response: str,
        humor_style: str,
        rating: int,
        session_id: str,
        additional_data: Optional[Dict] = None
    ):
        """Save user feedback for future training."""
        try:
            self.feedback_manager.save_feedback(
                user_input=user_input,
                ai_response=ai_response,
                humor_style=humor_style,
                rating=rating,
                session_id=session_id,
                additional_data=additional_data
            )
            logger.info(f"Feedback saved: Rating {rating}/5 for style '{humor_style}'")
        except Exception as e:
            logger.error(f"Failed to save feedback: {e}")
    
    def get_model_info(self) -> Dict[str, any]:
        """Get information about the current model and configuration."""
        try:
            models = self.client.list()
            current_model = next(
                (m for m in models['models'] if m['name'] == self.model_name),
                None
            )
            
            return {
                "model_name": self.model_name,
                "model_info": current_model,
                "available_models": [m['name'] for m in models['models']],
                "config": {
                    "temperature": self.config.temperature,
                    "top_p": self.config.top_p,
                    "max_tokens": self.config.max_tokens
                },
                "humor_styles": list(self.prompt_templates.system_prompts.keys())
            }
        except Exception as e:
            logger.error(f"Failed to get model info: {e}")
            return {"error": str(e)}
    
    def health_check(self) -> Dict[str, any]:
        """Check the health status of the engine."""
        status = {
            "status": "healthy",
            "model": self.model_name,
            "ollama_host": self.ollama_host,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Test Ollama connection
            self.client.list()
            status["ollama_connection"] = "connected"
        except Exception as e:
            status["status"] = "unhealthy"
            status["ollama_connection"] = f"error: {str(e)}"
        
        # Check feedback system
        try:
            stats = self.feedback_manager.get_feedback_stats()
            status["feedback_system"] = "operational"
            status["total_feedback"] = stats["total_ratings"]
        except Exception as e:
            status["feedback_system"] = f"error: {str(e)}"
        
        return status
    
    def __del__(self):
        """Cleanup resources."""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)


# For backward compatibility
CohostEngine = HumorCohost