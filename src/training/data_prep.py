import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple
import re
from tqdm import tqdm


class DataPreprocessor:
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def preprocess_reddit_data(self, file_path: Path) -> List[Dict]:
        conversations = []
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        for post in tqdm(data, desc="Processing Reddit data"):
            if self._is_comedy_content(post.get('title', '') + post.get('body', '')):
                conversation = {
                    'setup': post.get('title', ''),
                    'punchline': post.get('top_comment', ''),
                    'style': self._classify_humor_style(post.get('top_comment', '')),
                    'rating': post.get('score', 0) / 1000,  # Normalize score
                    'context': []
                }
                conversations.append(conversation)
        
        return conversations
    
    def preprocess_script_data(self, file_path: Path) -> List[Dict]:
        conversations = []
        
        with open(file_path, 'r') as f:
            script_lines = f.readlines()
        
        dialogue_pairs = self._extract_dialogue_pairs(script_lines)
        
        for setup, punchline in dialogue_pairs:
            conversation = {
                'setup': setup,
                'punchline': punchline,
                'style': 'witty',  # Default style for scripts
                'rating': 3.0,  # Neutral rating
                'context': []
            }
            conversations.append(conversation)
        
        return conversations
    
    def _is_comedy_content(self, text: str) -> bool:
        comedy_keywords = ['funny', 'joke', 'humor', 'comedy', 'laugh', 'hilarious']
        return any(keyword in text.lower() for keyword in comedy_keywords)
    
    def _classify_humor_style(self, text: str) -> str:
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['sarcasm', 'ironic', 'yeah right']):
            return 'sarcastic'
        elif any(word in text_lower for word in ['notice', 'ever wonder', 'whats with']):
            return 'observational'
        elif any(word in text_lower for word in ['im so', 'i cant even', 'story of my']):
            return 'self-deprecating'
        elif any(word in text_lower for word in ['quantum', 'dimension', 'surreal']):
            return 'absurd'
        else:
            return 'witty'
    
    def _extract_dialogue_pairs(self, lines: List[str]) -> List[Tuple[str, str]]:
        pairs = []
        
        for i in range(len(lines) - 1):
            if self._is_dialogue_line(lines[i]) and self._is_dialogue_line(lines[i + 1]):
                setup = self._clean_dialogue(lines[i])
                punchline = self._clean_dialogue(lines[i + 1])
                
                if len(setup) > 10 and len(punchline) > 10:
                    pairs.append((setup, punchline))
        
        return pairs
    
    def _is_dialogue_line(self, line: str) -> bool:
        return bool(re.match(r'^[A-Z][A-Z\s]+:', line))
    
    def _clean_dialogue(self, line: str) -> str:
        cleaned = re.sub(r'^[A-Z][A-Z\s]+:\s*', '', line)
        cleaned = re.sub(r'\([^)]*\)', '', cleaned)
        return cleaned.strip()
    
    def create_training_dataset(self, conversations: List[Dict]) -> pd.DataFrame:
        df = pd.DataFrame(conversations)
        
        df = df[df['rating'] >= 2.0]
        
        df = df.drop_duplicates(subset=['setup', 'punchline'])
        
        df['text_length'] = df['punchline'].str.len()
        df = df[(df['text_length'] > 10) & (df['text_length'] < 200)]
        
        return df.drop('text_length', axis=1)
    
    def save_dataset(self, df: pd.DataFrame, name: str) -> None:
        output_path = self.output_dir / f"{name}.jsonl"
        df.to_json(output_path, orient='records', lines=True)
        
        csv_path = self.output_dir / f"{name}.csv"
        df.to_csv(csv_path, index=False)
        
        print(f"Saved dataset to {output_path} and {csv_path}")
        print(f"Total samples: {len(df)}")
        print(f"Humor style distribution:\n{df['style'].value_counts()}")