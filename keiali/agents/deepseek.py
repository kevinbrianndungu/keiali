import torch
from transformers import AutoModelForCausalLM

class DeepSeekV3:
    def __init__(self, model_path: str = "/models/deepseek-v3"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = AutoModelForCausalLM.from_pretrained(model_path).to(self.device)
        
    def generate(self, prompt: str, max_tokens: int = 200) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(**inputs, max_new_tokens=max_tokens)
        return self.tokenizer.decode(outputs[0])
