import torch
from transformers import BlenderbotForConditionalGeneration, BlenderbotTokenizer
from utils.safety_checker import SafetyChecker
from services.retrieval_service import MentalHealthRetrievalService
from utils.response_enhancer import enhance_response

class ChatService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.safety_checker = SafetyChecker()
        self.retrieval_service = MentalHealthRetrievalService()
        self.last_user_input = None  # ✅ Light memory

        # Initialize Blenderbot model
        self.model_name = "facebook/blenderbot-400M-distill"
        self.tokenizer = BlenderbotTokenizer.from_pretrained(self.model_name)
        self.model = BlenderbotForConditionalGeneration.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if 'cuda' in self.device else torch.float32
        ).to(self.device).eval()

        # Test the model immediately
        test_response = self.generate_response("Hello")
        if not test_response or len(test_response) < 5:
            raise RuntimeError("Model failed to initialize properly")

    def _format_prompt(self, user_input: str, context: str = "") -> str:
        """Format prompt for mental health responses"""
        prompt = f"You are a mental health counselor.\n"
        if context:
            prompt += f"Use this information:\n{context}\n"
        prompt += f"\nUser: {user_input}\nCounselor:"
        
        # ✅ Add memory
        if self.last_user_input:
            prompt += f"\n(Earlier you mentioned: '{self.last_user_input}')"

        return prompt

    def generate_response(self, user_input: str) -> str:
        """Generate safe, helpful responses"""
        try:
            if self.safety_checker.is_unsafe(user_input):
                return "I specialize in mental health support. Please ask related questions."

            docs = self.retrieval_service.retrieve(user_input, k=2)
            context = "\n".join(doc.page_content for doc in docs) if docs else ""
            prompt = self._format_prompt(user_input, context)

            inputs = self.tokenizer([prompt], return_tensors="pt").to(self.device)
            outputs = self.model.generate(**inputs, max_new_tokens=150)
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Extract counselor part
            if "Counselor:" in response:
                response = response.split("Counselor:")[-1].strip()

            if not response or len(response) < 10:
                return "Could you please share more about what you're experiencing?"

            # ✅ Apply emotional tone enhancer
            response = enhance_response(response)

            # ✅ Save for memory
            self.last_user_input = user_input

            return response

        except Exception as e:
            print(f"Error: {str(e)}")
            return "I'm having trouble responding. Could you try again?"

# Quick test
if __name__ == "__main__":
    print("Initializing chatbot...")
    bot = ChatService()
    
    test_questions = [
        "What is anxiety?",
        "How can I handle stress?",
        "I'm feeling depressed",
        "Life feels meaningless lately"
    ]

    for q in test_questions:
        print(f"\nUser: {q}")
        print(f"Bot: {bot.generate_response(q)}")
