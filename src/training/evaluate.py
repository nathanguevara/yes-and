import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import Dataset
import numpy as np
from typing import Dict, List, Tuple
from pathlib import Path
import json
from tqdm import tqdm
from collections import defaultdict


class HumorEvaluator:
    def __init__(self, model_path: str, tokenizer_path: str):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.model.eval()
    
    def evaluate_dataset(self, test_data_path: Path) -> Dict[str, float]:
        with open(test_data_path, 'r') as f:
            test_data = [json.loads(line) for line in f]
        
        metrics = defaultdict(list)
        
        for sample in tqdm(test_data, desc="Evaluating"):
            response = self._generate_response(sample['setup'], sample['style'])
            
            perplexity = self._calculate_perplexity(sample['setup'], response)
            metrics['perplexity'].append(perplexity)
            
            coherence = self._evaluate_coherence(sample['setup'], response)
            metrics['coherence'].append(coherence)
            
            humor_score = self._evaluate_humor_quality(response, sample['style'])
            metrics['humor_score'].append(humor_score)
            
            diversity = self._calculate_diversity([response])
            metrics['diversity'].append(diversity)
        
        avg_metrics = {
            metric: np.mean(values) for metric, values in metrics.items()
        }
        
        avg_metrics['response_time'] = self._measure_inference_speed(test_data[:10])
        
        return avg_metrics
    
    def _generate_response(self, setup: str, style: str) -> str:
        prompt = f"Style: {style}\nUser: {setup}\nAssistant:"
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=100,
                temperature=0.9,
                top_p=0.9,
                do_sample=True
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.split("Assistant:")[-1].strip()
    
    def _calculate_perplexity(self, setup: str, response: str) -> float:
        text = f"{setup} {response}"
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs, labels=inputs['input_ids'])
            loss = outputs.loss
            perplexity = torch.exp(loss).item()
        
        return min(perplexity, 1000.0)  # Cap at 1000 for outliers
    
    def _evaluate_coherence(self, setup: str, response: str) -> float:
        coherence_score = 1.0
        
        if len(response.split()) < 3:
            coherence_score *= 0.5
        
        setup_words = set(setup.lower().split())
        response_words = set(response.lower().split())
        overlap = len(setup_words & response_words) / max(len(setup_words), 1)
        coherence_score *= (0.5 + 0.5 * min(overlap, 1.0))
        
        if response.count('.') > 5:
            coherence_score *= 0.8
        
        return coherence_score
    
    def _evaluate_humor_quality(self, response: str, style: str) -> float:
        humor_score = 0.5
        
        humor_indicators = {
            'witty': ['clever', 'pun', 'wordplay', 'twist'],
            'sarcastic': ['oh', 'sure', 'totally', 'right'],
            'observational': ['notice', 'ever', 'always', 'why'],
            'self-deprecating': ['i', 'me', 'my', 'myself'],
            'absurd': ['suddenly', 'random', 'somehow', 'apparently']
        }
        
        style_words = humor_indicators.get(style, [])
        response_lower = response.lower()
        
        for word in style_words:
            if word in response_lower:
                humor_score += 0.1
        
        if '!' in response:
            humor_score += 0.05
        if '?' in response:
            humor_score += 0.05
        
        if any(emoji in response for emoji in ['😂', '🤣', '😄', '😆', '🙃']):
            humor_score += 0.1
        
        return min(humor_score, 1.0)
    
    def _calculate_diversity(self, responses: List[str]) -> float:
        all_tokens = []
        for response in responses:
            tokens = response.lower().split()
            all_tokens.extend(tokens)
        
        if not all_tokens:
            return 0.0
        
        unique_tokens = set(all_tokens)
        diversity = len(unique_tokens) / len(all_tokens)
        
        return diversity
    
    def _measure_inference_speed(self, samples: List[Dict]) -> float:
        import time
        
        times = []
        
        for sample in samples:
            start = time.time()
            _ = self._generate_response(sample['setup'], sample['style'])
            end = time.time()
            times.append(end - start)
        
        return np.mean(times)
    
    def generate_evaluation_report(self, metrics: Dict[str, float], output_path: Path):
        report = {
            "model_performance": {
                "perplexity": round(metrics['perplexity'], 2),
                "coherence": round(metrics['coherence'], 3),
                "humor_score": round(metrics['humor_score'], 3),
                "diversity": round(metrics['diversity'], 3),
                "avg_response_time_seconds": round(metrics['response_time'], 3)
            },
            "recommendations": []
        }
        
        if metrics['perplexity'] > 50:
            report['recommendations'].append("High perplexity - consider more training")
        
        if metrics['coherence'] < 0.7:
            report['recommendations'].append("Low coherence - review training data quality")
        
        if metrics['humor_score'] < 0.6:
            report['recommendations'].append("Low humor score - add more comedy-specific data")
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report