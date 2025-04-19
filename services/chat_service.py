import torch
import random
from transformers import BlenderbotForConditionalGeneration, BlenderbotTokenizer
from utils.safety_checker import SafetyChecker
from services.retrieval_service import MentalHealthRetrievalService
from utils.response_enhancer import enhance_response
from utils.response_templates import get_template

class ChatService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.safety_checker = SafetyChecker()
        self.retrieval_service = MentalHealthRetrievalService()
        self.last_responses = []  # Track last 3 responses to avoid repetition

        # Initialize Blenderbot
        self.model_name = "facebook/blenderbot-400M-distill"
        self.tokenizer = BlenderbotTokenizer.from_pretrained(self.model_name)
        self.model = BlenderbotForConditionalGeneration.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if 'cuda' in self.device else torch.float32
        ).to(self.device).eval()

    def _format_prompt(self, user_input: str, context: str = "") -> str:
        """Structured prompt for mental health responses"""
        prompt = (
            f"Conversation with a mental health counselor. Be empathetic, concise (1-2 sentences), "
            f"and focused on the user's immediate needs.\n\n"
            f"Context: {context}\n"
            f"User: {user_input}\n"
            f"Counselor:"
        )
        return prompt

    def _is_repetitive(self, response: str) -> bool:
        """Check if response resembles recent ones"""
        return any(
            resp.lower() in response.lower() 
            for resp in self.last_responses[-2:]
        ) if self.last_responses else False

    def generate_response(self, user_input: str) -> str:
        try:
            # Safety check
            if self.safety_checker.is_unsafe(user_input):
                return get_template("crisis")

            # Retrieve context
            context = self.retrieval_service.get_emotional_context(user_input)
            prompt = self._format_prompt(user_input, context)

            # Generate
            inputs = self.tokenizer([prompt], return_tensors="pt").to(self.device)
            outputs = self.model.generate(**inputs, max_new_tokens=100)
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Post-process
            response = response.split("Counselor:")[-1].split("User:")[0].strip()
            
            # Fallback if response is poor
            if len(response) < 10 or self._is_repetitive(response):
                response = get_template(user_input)

            # Final enhancement
            response = enhance_response(response)
            self.last_responses = [response] + self.last_responses[:2]  # Update history
            
            return response

        except Exception as e:
            print(f"Error: {str(e)}")
            return random.choice([
                "I'm having trouble understanding. Could you rephrase?",
                "Let's focus on how you're feeling right now."
            ])