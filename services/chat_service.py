import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from utils.safety_checker import SafetyChecker

class ChatService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.safety_checker = SafetyChecker()
        
        # Load ONLY your custom model
        self.tokenizer = AutoTokenizer.from_pretrained("model/tokenizer")
        base_model = AutoModelForCausalLM.from_pretrained("model/base_model")
        self.model = PeftModel.from_pretrained(base_model, "model").to(self.device)
        
    def generate_response(self, user_input: str) -> str:
        if self.safety_checker.is_unsafe(user_input):
            return "I specialize in mental health support. Please ask related questions."
            
        prompt = f"""Your Custom Assistant:
User: {user_input}
Assistant:"""
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7
        )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).split("Assistant:")[-1].strip()