import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
from collections import defaultdict


class FeedbackManager:
    def __init__(self, feedback_file: str = "data/feedback.json"):
        self.feedback_file = Path(feedback_file)
        self.feedback_file.parent.mkdir(parents=True, exist_ok=True)
        self.feedback_data = self._load_feedback()
    
    def _load_feedback(self) -> List[Dict]:
        if self.feedback_file.exists():
            with open(self.feedback_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_feedback(
        self,
        user_input: str,
        ai_response: str,
        humor_style: str,
        rating: int,
        session_id: Optional[str] = None,
        additional_data: Optional[Dict] = None
    ):
        feedback_entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'user_input': user_input,
            'ai_response': ai_response,
            'humor_style': humor_style,
            'rating': rating,
            'additional_data': additional_data or {}
        }
        
        self.feedback_data.append(feedback_entry)
        
        with open(self.feedback_file, 'w') as f:
            json.dump(self.feedback_data, f, indent=2)
    
    def get_feedback_stats(self) -> Dict:
        if not self.feedback_data:
            return {
                'total_ratings': 0,
                'average_rating': 0.0,
                'style_ratings': {},
                'rating_distribution': {}
            }
        
        df = pd.DataFrame(self.feedback_data)
        
        stats = {
            'total_ratings': len(df),
            'average_rating': df['rating'].mean(),
            'style_ratings': df.groupby('humor_style')['rating'].agg(['mean', 'count']).to_dict('index'),
            'rating_distribution': df['rating'].value_counts().to_dict()
        }
        
        return stats
    
    def get_low_rated_examples(self, threshold: int = 2) -> List[Dict]:
        return [
            entry for entry in self.feedback_data
            if entry['rating'] <= threshold
        ]
    
    def get_high_rated_examples(self, threshold: int = 4) -> List[Dict]:
        return [
            entry for entry in self.feedback_data
            if entry['rating'] >= threshold
        ]
    
    def analyze_feedback_patterns(self) -> Dict:
        if not self.feedback_data:
            return {'patterns': [], 'recommendations': []}
        
        patterns = defaultdict(list)
        
        for entry in self.feedback_data:
            patterns['by_style'][entry['humor_style']].append(entry['rating'])
            
            hour = datetime.fromisoformat(entry['timestamp']).hour
            patterns['by_hour'][hour].append(entry['rating'])
            
            response_length = len(entry['ai_response'].split())
            if response_length < 20:
                patterns['by_length']['short'].append(entry['rating'])
            elif response_length < 50:
                patterns['by_length']['medium'].append(entry['rating'])
            else:
                patterns['by_length']['long'].append(entry['rating'])
        
        analysis = {
            'patterns': {},
            'recommendations': []
        }
        
        for style, ratings in patterns['by_style'].items():
            avg_rating = sum(ratings) / len(ratings)
            analysis['patterns'][f'style_{style}'] = {
                'average_rating': avg_rating,
                'count': len(ratings)
            }
            
            if avg_rating < 3.0:
                analysis['recommendations'].append(
                    f"Improve {style} humor - current avg rating: {avg_rating:.2f}"
                )
        
        length_ratings = {
            length: sum(ratings) / len(ratings)
            for length, ratings in patterns['by_length'].items()
            if ratings
        }
        
        if length_ratings:
            best_length = max(length_ratings, key=length_ratings.get)
            analysis['recommendations'].append(
                f"Optimal response length appears to be {best_length}"
            )
        
        return analysis
    
    def export_training_data(self, min_rating: int = 4) -> List[Dict]:
        training_data = []
        
        for entry in self.feedback_data:
            if entry['rating'] >= min_rating:
                training_data.append({
                    'setup': entry['user_input'],
                    'punchline': entry['ai_response'],
                    'style': entry['humor_style'],
                    'rating': entry['rating']
                })
        
        return training_data
    
    def get_conversation_history(self, session_id: str) -> List[Dict]:
        return [
            entry for entry in self.feedback_data
            if entry.get('session_id') == session_id
        ]
    
    def clear_old_feedback(self, days: int = 30):
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        self.feedback_data = [
            entry for entry in self.feedback_data
            if datetime.fromisoformat(entry['timestamp']).timestamp() > cutoff_date
        ]
        
        with open(self.feedback_file, 'w') as f:
            json.dump(self.feedback_data, f, indent=2)