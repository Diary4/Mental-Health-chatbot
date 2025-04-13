from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from ..utils.response_validator import is_professional
import torch

class ChatService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained("model/tokenizer")
        self.model = self._load_model()
    
    def _load_model(self):
        base_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
        return PeftModel.from_pretrained(base_model, "model").to(self.device)
    
    def generate_response(self, message: str) -> str:
        prompt = self._build_prompt(message)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            repetition_penalty=2.0,
            eos_token_id=self.tokenizer.eos_token_id
        )
        
        return self._process_output(outputs)
    
    def _build_prompt(self, message: str) -> str:
        return f"""Mental Health Professional Response Guidelines:
1. Validate emotion briefly
2. Suggest ONE evidence-based technique
3. Offer follow-up support

User: {message}
Assistant:"""
    
    def _process_output(self, outputs) -> str:
        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        assistant_part = full_response.split("Assistant:")[-1].strip()
        
        if not is_professional(assistant_part):
            return self._get_fallback_response()
        return assistant_part
    
    def _get_fallback_response(self) -> str:
        return "I hear this is challenging. Try the 5-4-3-2-1 grounding technique..."