from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import os
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.chatbot.cohost_engine import HumorCohost, GenerationConfig
from src.chatbot.humor_layers import HumorEnhancer
from src.utils.feedback import FeedbackManager

app = FastAPI(
    title="AI Comedy Cohost API",
    description="Backend API for the AI Comedy Cohost chatbot",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
humor_engine = None
humor_enhancer = None
feedback_manager = None


# Pydantic models
class GenerateRequest(BaseModel):
    user_input: str
    humor_style: str = "witty"
    conversation_history: Optional[List[Dict[str, str]]] = None
    session_id: Optional[str] = None


class GenerateResponse(BaseModel):
    response: str
    enhanced_response: str
    metadata: Dict
    humor_style: str
    enhanced: bool


class FeedbackRequest(BaseModel):
    user_input: str
    ai_response: str
    humor_style: str
    rating: int
    session_id: str
    additional_data: Optional[Dict] = None


class HealthResponse(BaseModel):
    status: str
    model: str
    ollama_host: str
    timestamp: str
    ollama_connection: str
    feedback_system: str


@app.on_event("startup")
async def startup_event():
    """Initialize the humor engine and related components."""
    global humor_engine, humor_enhancer, feedback_manager
    
    try:
        config = GenerationConfig(
            temperature=float(os.getenv("TEMPERATURE", "0.9")),
            top_p=float(os.getenv("TOP_P", "0.9")),
            max_tokens=int(os.getenv("MAX_TOKENS", "150")),
            timeout=float(os.getenv("TIMEOUT", "30.0"))
        )
        
        humor_engine = HumorCohost(config=config)
        humor_enhancer = HumorEnhancer()
        feedback_manager = FeedbackManager()
        
        print("✅ AI Comedy Cohost API initialized successfully")
        
    except Exception as e:
        print(f"❌ Failed to initialize API: {e}")
        raise


@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "message": "AI Comedy Cohost API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    if not humor_engine:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    health_data = humor_engine.health_check()
    return HealthResponse(**health_data)


@app.post("/generate", response_model=GenerateResponse)
async def generate_response(request: GenerateRequest):
    """Generate a humorous response."""
    if not humor_engine or not humor_enhancer:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        # Generate response using the engine
        response, metadata = humor_engine.generate_response(
            user_input=request.user_input,
            humor_style=request.humor_style,
            conversation_history=request.conversation_history or [],
            session_id=request.session_id
        )
        
        # Enhance the response
        enhanced_response = humor_enhancer.enhance(response, request.humor_style)
        
        return GenerateResponse(
            response=response,
            enhanced_response=enhanced_response,
            metadata=metadata,
            humor_style=request.humor_style,
            enhanced=enhanced_response != response
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.post("/feedback")
async def save_feedback(request: FeedbackRequest):
    """Save user feedback."""
    if not feedback_manager:
        raise HTTPException(status_code=503, detail="Feedback service not initialized")
    
    try:
        feedback_manager.save_feedback(
            user_input=request.user_input,
            ai_response=request.ai_response,
            humor_style=request.humor_style,
            rating=request.rating,
            session_id=request.session_id,
            additional_data=request.additional_data
        )
        
        return {"message": "Feedback saved successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save feedback: {str(e)}")


@app.get("/feedback/stats")
async def get_feedback_stats():
    """Get feedback statistics."""
    if not feedback_manager:
        raise HTTPException(status_code=503, detail="Feedback service not initialized")
    
    try:
        stats = feedback_manager.get_feedback_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@app.get("/model/info")
async def get_model_info():
    """Get model information."""
    if not humor_engine:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        info = humor_engine.get_model_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )