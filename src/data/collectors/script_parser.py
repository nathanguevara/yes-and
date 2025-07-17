import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import json


class ScriptParser:
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.character_pattern = re.compile(r'^([A-Z][A-Z\s\-\']+)(?:\s*\([^)]*\))?\s*:(.*)$')
        self.action_pattern = re.compile(r'^\[.*\]$|^\(.*\)$')
        self.scene_pattern = re.compile(r'^(INT\.|EXT\.|SCENE|ACT)')
    
    def parse_script_file(self, file_path: Path) -> Dict:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        script_data = {
            'title': file_path.stem,
            'scenes': [],
            'dialogues': [],
            'characters': set()
        }
        
        current_scene = None
        current_dialogue = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            if not line:
                continue
            
            if self.scene_pattern.match(line):
                if current_scene and current_dialogue:
                    script_data['scenes'].append({
                        'scene': current_scene,
                        'dialogues': current_dialogue
                    })
                current_scene = line
                current_dialogue = []
                continue
            
            match = self.character_pattern.match(line)
            if match:
                character = match.group(1).strip()
                dialogue = match.group(2).strip()
                
                if dialogue:
                    script_data['characters'].add(character)
                    current_dialogue.append({
                        'character': character,
                        'line': dialogue,
                        'line_number': i + 1
                    })
                    script_data['dialogues'].append({
                        'character': character,
                        'line': dialogue,
                        'scene': current_scene
                    })
        
        if current_scene and current_dialogue:
            script_data['scenes'].append({
                'scene': current_scene,
                'dialogues': current_dialogue
            })
        
        script_data['characters'] = list(script_data['characters'])
        
        return script_data
    
    def extract_comedy_exchanges(self, script_data: Dict) -> List[Dict]:
        comedy_exchanges = []
        dialogues = script_data['dialogues']
        
        for i in range(len(dialogues) - 1):
            setup = dialogues[i]
            response = dialogues[i + 1]
            
            if setup['character'] != response['character']:
                if self._is_comedy_exchange(setup['line'], response['line']):
                    exchange = {
                        'setup_character': setup['character'],
                        'setup': setup['line'],
                        'response_character': response['character'],
                        'response': response['line'],
                        'scene': setup.get('scene', 'Unknown'),
                        'comedy_score': self._score_comedy(setup['line'], response['line'])
                    }
                    comedy_exchanges.append(exchange)
        
        comedy_exchanges.sort(key=lambda x: x['comedy_score'], reverse=True)
        
        return comedy_exchanges
    
    def _is_comedy_exchange(self, setup: str, response: str) -> bool:
        comedy_indicators = [
            (r'\?', r'!'),  # Question followed by exclamation
            (r'why', r'because'),  # Setup-punchline pattern
            (r'what', r'\.{3}'),  # Setup with ellipsis response
            (r'how', r'like'),  # Comparison jokes
        ]
        
        for setup_pattern, response_pattern in comedy_indicators:
            if re.search(setup_pattern, setup.lower()) and re.search(response_pattern, response.lower()):
                return True
        
        min_length = 10
        max_length = 200
        if (min_length <= len(setup) <= max_length and 
            min_length <= len(response) <= max_length):
            return True
        
        return False
    
    def _score_comedy(self, setup: str, response: str) -> float:
        score = 0.5
        
        if '?' in setup:
            score += 0.1
        
        if any(word in response.lower() for word in ['actually', 'well', 'technically']):
            score += 0.15
        
        if '!' in response or '...' in response:
            score += 0.1
        
        setup_words = set(setup.lower().split())
        response_words = set(response.lower().split())
        if setup_words & response_words:  # Word callbacks
            score += 0.15
        
        return min(score, 1.0)
    
    def parse_multiple_scripts(self, script_dir: Path, file_pattern: str = "*.txt") -> List[Dict]:
        all_exchanges = []
        script_files = list(script_dir.glob(file_pattern))
        
        for script_file in script_files:
            print(f"Parsing {script_file.name}...")
            
            try:
                script_data = self.parse_script_file(script_file)
                exchanges = self.extract_comedy_exchanges(script_data)
                
                for exchange in exchanges:
                    exchange['source'] = script_file.name
                
                all_exchanges.extend(exchanges)
                
                self.save_script_data(script_data, exchanges, script_file.stem)
                
            except Exception as e:
                print(f"Error parsing {script_file}: {e}")
        
        return all_exchanges
    
    def save_script_data(self, script_data: Dict, exchanges: List[Dict], name: str):
        script_path = self.output_dir / f"{name}_parsed.json"
        with open(script_path, 'w') as f:
            json.dump(script_data, f, indent=2)
        
        exchanges_path = self.output_dir / f"{name}_exchanges.json"
        with open(exchanges_path, 'w') as f:
            json.dump(exchanges, f, indent=2)
        
        print(f"Saved {len(exchanges)} comedy exchanges from {name}")