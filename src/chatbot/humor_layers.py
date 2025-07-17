import re
import random
from typing import Dict, List, Tuple


class HumorEnhancer:
    def __init__(self):
        self.timing_words = ["...", "uh", "um", "well", "so"]
        self.intensifiers = ["literally", "totally", "absolutely", "completely"]
        self.callbacks = self._load_callbacks()
    
    def _load_callbacks(self) -> Dict[str, List[str]]:
        return {
            "witty": ["*adjusts monocle*", "*tips fedora*", "*winks*"],
            "sarcastic": ["*rolls eyes*", "*slow clap*", "*chef's kiss*"],
            "observational": ["You ever notice...", "What's the deal with...", "I mean..."],
            "self-deprecating": ["Story of my life", "Classic me", "I'm a disaster"],
            "absurd": ["*quantum tunnels*", "*exists in 4D*", "*becomes sentient*"]
        }
    
    def enhance(self, response: str, humor_style: str) -> str:
        enhanced = response
        
        enhanced = self._add_comedic_timing(enhanced)
        
        enhanced = self._add_callbacks(enhanced, humor_style)
        
        enhanced = self._enhance_wordplay(enhanced)
        
        return enhanced
    
    def _add_comedic_timing(self, text: str) -> str:
        sentences = text.split('. ')
        if len(sentences) > 1 and random.random() < 0.3:
            insert_pos = random.randint(0, len(sentences) - 1)
            timing = random.choice(self.timing_words)
            sentences[insert_pos] = f"{sentences[insert_pos]} {timing}"
        return '. '.join(sentences)
    
    def _add_callbacks(self, text: str, humor_style: str) -> str:
        if humor_style in self.callbacks and random.random() < 0.4:
            callback = random.choice(self.callbacks[humor_style])
            text = f"{text} {callback}"
        return text
    
    def _enhance_wordplay(self, text: str) -> str:
        pun_triggers = {
            "wait": "weight",
            "right": "write",
            "break": "brake",
            "piece": "peace"
        }
        
        for word, pun in pun_triggers.items():
            if word in text.lower() and random.random() < 0.2:
                text += f" (or should I say {pun}? 😏)"
                break
        
        return text
    
    def analyze_humor_score(self, text: str) -> float:
        score = 0.5
        
        if any(word in text.lower() for word in ["funny", "hilarious", "joke"]):
            score += 0.1
        
        if "!" in text:
            score += 0.05
        
        if any(emoji in text for emoji in ["😂", "🤣", "😄", "😆"]):
            score += 0.15
        
        return min(score, 1.0)