import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset
import json
from pathlib import Path
from typing import Dict, List, Optional


class HumorFineTuner:
    def __init__(
        self,
        model_name: str = "meta-llama/Llama-3.2-3B-Instruct",
        output_dir: str = "./models/humor-cohost"
    ):
        self.model_name = model_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.tokenizer = None
        self.model = None
        self.peft_config = None
    
    def setup_model_and_tokenizer(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            load_in_8bit=True
        )
        
        self.peft_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            inference_mode=False,
            r=16,
            lora_alpha=32,
            lora_dropout=0.1,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj"]
        )
        
        self.model = get_peft_model(self.model, self.peft_config)
        self.model.print_trainable_parameters()
    
    def prepare_dataset(self, data_path: Path) -> Dataset:
        with open(data_path, 'r') as f:
            conversations = [json.loads(line) for line in f]
        
        formatted_data = []
        for conv in conversations:
            text = self._format_conversation(conv)
            formatted_data.append({"text": text})
        
        dataset = Dataset.from_list(formatted_data)
        
        def tokenize_function(examples):
            return self.tokenizer(
                examples["text"],
                truncation=True,
                padding="max_length",
                max_length=512
            )
        
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        return tokenized_dataset
    
    def _format_conversation(self, conv: Dict) -> str:
        style_prompts = {
            "witty": "Be witty and clever",
            "sarcastic": "Be sarcastic and ironic",
            "observational": "Make observational humor",
            "self-deprecating": "Use self-deprecating humor",
            "absurd": "Be absurd and surreal"
        }
        
        style_instruction = style_prompts.get(conv['style'], "Be funny")
        
        text = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a comedy AI assistant. {style_instruction}.<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{conv['setup']}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
{conv['punchline']}<|eot_id|><|end_of_text|>"""
        
        return text
    
    def train(self, train_dataset: Dataset, eval_dataset: Optional[Dataset] = None):
        training_args = TrainingArguments(
            output_dir=str(self.output_dir),
            num_train_epochs=3,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            gradient_accumulation_steps=4,
            warmup_steps=100,
            learning_rate=2e-5,
            fp16=True,
            logging_steps=10,
            save_steps=500,
            eval_steps=100,
            evaluation_strategy="steps" if eval_dataset else "no",
            save_total_limit=3,
            load_best_model_at_end=True if eval_dataset else False,
            report_to="tensorboard",
            push_to_hub=False
        )
        
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=self.tokenizer,
            data_collator=data_collator
        )
        
        trainer.train()
        
        self.model.save_pretrained(self.output_dir / "final_model")
        self.tokenizer.save_pretrained(self.output_dir / "final_model")
    
    def load_finetuned_model(self, checkpoint_path: Path):
        from peft import PeftModel
        
        base_model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        model = PeftModel.from_pretrained(base_model, checkpoint_path)
        return model.merge_and_unload()
    
    def generate_comedy(self, prompt: str, style: str = "witty") -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=100,
                temperature=0.9,
                top_p=0.9,
                do_sample=True
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.split("assistant")[-1].strip()