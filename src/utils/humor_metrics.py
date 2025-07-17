import numpy as np
from typing import Dict, List, Tuple, Optional
from collections import Counter
import re


class HumorMetrics:
    def __init__(self):
        self.humor_keywords = {
            'witty': ['clever', 'pun', 'wordplay', 'smart', 'quick'],
            'sarcastic': ['oh', 'sure', 'totally', 'right', 'yeah'],
            'observational': ['notice', 'ever', 'always', 'why', 'weird'],
            'self-deprecating': ['i', 'me', 'my', 'myself', 'fail'],
            'absurd': ['suddenly', 'random', 'somehow', 'apparently', 'inexplicably']
        }
    
    def calculate_humor_score(
        self,
        text: str,
        style: str = 'witty',
        user_rating: Optional[float] = None
    ) -> float:
        base_score = 0.5
        
        style_score = self._calculate_style_match(text, style)
        base_score += style_score * 0.2
        
        structure_score = self._analyze_joke_structure(text)
        base_score += structure_score * 0.2
        
        timing_score = self._analyze_timing(text)
        base_score += timing_score * 0.1
        
        if user_rating is not None:
            base_score = 0.7 * base_score + 0.3 * (user_rating / 5.0)
        
        return min(max(base_score, 0.0), 1.0)
    
    def _calculate_style_match(self, text: str, style: str) -> float:
        if style not in self.humor_keywords:
            return 0.5
        
        keywords = self.humor_keywords[style]
        text_lower = text.lower()
        
        matches = sum(1 for keyword in keywords if keyword in text_lower)
        return min(matches / len(keywords), 1.0)
    
    def _analyze_joke_structure(self, text: str) -> float:
        score = 0.0
        
        if re.search(r'\.{3}|\?!|!+', text):
            score += 0.3
        
        sentences = text.split('.')
        if 2 <= len(sentences) <= 4:
            score += 0.3
        
        if re.search(r'\([^)]*\)', text):
            score += 0.2
        
        if re.search(r'"[^"]*"', text):
            score += 0.2
        
        return score
    
    def _analyze_timing(self, text: str) -> float:
        timing_markers = ['...', '—', 'wait', 'actually', 'oh']
        
        score = 0.0
        for marker in timing_markers:
            if marker in text.lower():
                score += 0.2
        
        return min(score, 1.0)
    
    def analyze_conversation_flow(self, messages: List[Dict[str, str]]) -> Dict[str, float]:
        if not messages:
            return {'engagement': 0.0, 'variety': 0.0, 'progression': 0.0}
        
        engagement = self._calculate_engagement(messages)
        variety = self._calculate_variety(messages)
        progression = self._calculate_progression(messages)
        
        return {
            'engagement': engagement,
            'variety': variety,
            'progression': progression,
            'overall': (engagement + variety + progression) / 3
        }
    
    def _calculate_engagement(self, messages: List[Dict[str, str]]) -> float:
        if len(messages) < 2:
            return 0.0
        
        user_messages = [m for m in messages if m['role'] == 'user']
        
        avg_length = np.mean([len(m['content'].split()) for m in user_messages])
        
        length_score = min(avg_length / 20, 1.0)
        
        frequency_score = min(len(messages) / 20, 1.0)
        
        return (length_score + frequency_score) / 2
    
    def _calculate_variety(self, messages: List[Dict[str, str]]) -> float:
        ai_messages = [m['content'] for m in messages if m['role'] == 'assistant']
        
        if not ai_messages:
            return 0.0
        
        all_words = []
        for msg in ai_messages:
            words = msg.lower().split()
            all_words.extend(words)
        
        unique_words = set(all_words)
        vocabulary_richness = len(unique_words) / max(len(all_words), 1)
        
        return vocabulary_richness
    
    def _calculate_progression(self, messages: List[Dict[str, str]]) -> float:
        if len(messages) < 4:
            return 0.5
        
        callbacks = 0
        for i in range(2, len(messages)):
            current = messages[i]['content'].lower()
            previous = messages[i-2]['content'].lower()
            
            current_words = set(current.split())
            previous_words = set(previous.split())
            
            if current_words & previous_words:
                callbacks += 1
        
        callback_rate = callbacks / max(len(messages) - 2, 1)
        
        return min(callback_rate * 2, 1.0)
    
    def generate_humor_report(self, conversations: List[List[Dict[str, str]]]) -> Dict:
        all_scores = []
        style_distribution = Counter()
        
        for conv in conversations:
            flow_metrics = self.analyze_conversation_flow(conv)
            all_scores.append(flow_metrics['overall'])
            
            for msg in conv:
                if msg['role'] == 'assistant':
                    detected_style = self._detect_humor_style(msg['content'])
                    style_distribution[detected_style] += 1
        
        return {
            'average_score': np.mean(all_scores) if all_scores else 0.0,
            'score_std': np.std(all_scores) if all_scores else 0.0,
            'total_conversations': len(conversations),
            'style_distribution': dict(style_distribution),
            'recommendations': self._generate_recommendations(all_scores, style_distribution)
        }
    
    def _detect_humor_style(self, text: str) -> str:
        best_style = 'witty'
        best_score = 0.0
        
        for style, keywords in self.humor_keywords.items():
            score = self._calculate_style_match(text, style)
            if score > best_score:
                best_score = score
                best_style = style
        
        return best_style
    
    def _generate_recommendations(
        self,
        scores: List[float],
        style_distribution: Counter
    ) -> List[str]:
        recommendations = []
        
        if scores and np.mean(scores) < 0.6:
            recommendations.append("Consider adding more varied humor patterns")
        
        if len(style_distribution) < 3:
            recommendations.append("Expand humor style variety for better coverage")
        
        dominant_style = style_distribution.most_common(1)
        if dominant_style and dominant_style[0][1] > sum(style_distribution.values()) * 0.5:
            recommendations.append(f"Over-reliance on {dominant_style[0][0]} style detected")
        
        return recommendations