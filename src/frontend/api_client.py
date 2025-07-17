import requests
from typing import Dict, List, Optional, Tuple
import os
from datetime import datetime
import json


class ComedyAPIClient:
    """Client for interacting with the AI Comedy Cohost API backend."""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("API_BASE_URL", "http://localhost:8000")
        self.session = requests.Session()
        self.timeout = 30.0
    
    def generate_response(
        self,
        user_input: str,
        humor_style: str = "witty",
        conversation_history: Optional[List[Dict[str, str]]] = None,
        session_id: Optional[str] = None
    ) -> Tuple[str, Dict]:
        """Generate a humorous response via the API."""
        url = f"{self.base_url}/generate"
        
        payload = {
            "user_input": user_input,
            "humor_style": humor_style,
            "conversation_history": conversation_history or [],
            "session_id": session_id
        }
        
        try:
            response = self.session.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            return data["enhanced_response"], {
                "generation_time": data["metadata"].get("generation_time", 0),
                "humor_score": data["metadata"].get("humor_score", 0),
                "enhanced": data["enhanced"],
                "original_response": data["response"]
            }
            
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to generate response: {e}")
        except KeyError as e:
            raise ValueError(f"Invalid response format: {e}")
    
    def save_feedback(
        self,
        user_input: str,
        ai_response: str,
        humor_style: str,
        rating: int,
        session_id: str,
        additional_data: Optional[Dict] = None
    ) -> bool:
        """Save user feedback via the API."""
        url = f"{self.base_url}/feedback"
        
        payload = {
            "user_input": user_input,
            "ai_response": ai_response,
            "humor_style": humor_style,
            "rating": rating,
            "session_id": session_id,
            "additional_data": additional_data or {}
        }
        
        try:
            response = self.session.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to save feedback: {e}")
            return False
    
    def get_feedback_stats(self) -> Dict:
        """Get feedback statistics via the API."""
        url = f"{self.base_url}/feedback/stats"
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to get feedback stats: {e}")
            return {"total_ratings": 0, "average_rating": 0, "style_ratings": {}}
    
    def get_model_info(self) -> Dict:
        """Get model information via the API."""
        url = f"{self.base_url}/model/info"
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to get model info: {e}")
            return {"error": str(e)}
    
    def health_check(self) -> Dict:
        """Check API health."""
        url = f"{self.base_url}/health"
        
        try:
            response = self.session.get(url, timeout=10.0)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {"status": "unhealthy", "error": str(e)}
    
    def is_healthy(self) -> bool:
        """Quick health check that returns boolean."""
        health = self.health_check()
        return health.get("status") == "healthy"