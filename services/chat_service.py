import torch
from typing import Optional, Tuple, Dict, Any
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from peft import PeftModel
from utils.safety_checker import SafetyChecker
from services.retrieval_service import MentalHealthRetrievalService

class ChatService:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.safety_checker = SafetyChecker()
        self.retrieval_service = MentalHealthRetrievalService()
        
        # Initialize with strict validation
        self.model = None
        self.tokenizer = None
        self._initialize_model_with_validation()

    def _initialize_model_with_validation(self) -> None:
        """Initialize with thorough validation checks"""
        try:
            print("Initializing tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                "model/tokenizer",
                padding_side="left",
                pad_token="<|endoftext|>",
                truncation_side="left"
            )
            
            print("Loading base model...")
            base_model = AutoModelForCausalLM.from_pretrained(
                "microsoft/DialoGPT-small",
                torch_dtype=torch.float16 if 'cuda' in self.device else torch.float32
            )
            
            print("Loading PEFT adapter...")
            self.model = PeftModel.from_pretrained(
                base_model,
                "model",
                device_map="auto"
            ).eval()
            
            # Immediate validation test
            print("Running validation test...")
            test_response = self._validate_model()
            if not test_response or len(test_response) < 10:
                raise RuntimeError("Model validation failed - generating empty/short responses")
            print(f"Validation test passed. Sample output: {test_response[:100]}...")
            
        except Exception as e:
            raise RuntimeError(f"Model initialization failed: {str(e)}")

    def _validate_model(self) -> str:
        """Generate a test response to validate model"""
        test_prompt = """You are a mental health assistant. 
Question: What is anxiety?
Answer:"""
        
        inputs = self.tokenizer(test_prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=100,
                temperature=0.7,
                do_sample=True
            )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def _build_prompt(self, user_input: str, context: Optional[str] = None) -> str:
        """Construct strict therapeutic prompt"""
        base_prompt = """You are a professional mental health assistant. 
Rules:
1. Provide accurate, supportive information
2. Be concise but empathetic
3. Only discuss mental health topics
4. If unsure, recommend professional help

"""
        if context:
            return f"""{base_prompt}Context:
{context}

Question: {user_input}
Answer:"""
        return f"""{base_prompt}Question: {user_input}
Answer:"""

    def _generate_response(self, prompt: str) -> str:
        """Strict generation with quality controls"""
        generation_config = GenerationConfig(
            max_new_tokens=150,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    generation_config=generation_config
                )
            full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Strict extraction of answer
            if "Answer:" in full_text:
                return full_text.split("Answer:")[-1].strip()
            return full_text
            
        except Exception as e:
            print(f"Generation error: {str(e)}")
            return ""

    def _validate_response(self, response: str) -> bool:
        """Ensure response meets quality standards"""
        if not response:
            return False
        if len(response) < 10:
            return False
        if any(bad in response.lower() for bad in ["i'm not", "i don't know", "sorry"]):
            return False
        return True

    def generate_response(self, user_input: str) -> str:
        """Generate and validate mental health responses"""
        try:
            # Strict safety check
            if self.safety_checker.is_unsafe(user_input):
                return "I specialize in mental health support. Please ask related questions."
            
            # Retrieve context
            docs = self.retrieval_service.retrieve(
                query=user_input,
                k=2,
                filter={"type": {"$in": ["qa_pair", "book_page"]}}
            )
            
            # Format context
            context = "\n".join(
                f"Source: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
                for doc in docs
            ) if docs else None
            
            # Build strict prompt
            prompt = self._build_prompt(user_input, context)
            
            # Generate and validate
            raw_response = self._generate_response(prompt)
            
            # Post-processing
            response = raw_response.split("User:")[0].strip()
            response = response.replace("\n", " ").strip()
            
            # Final validation
            if not self._validate_response(response):
                return "I'm still learning. Could you ask in a different way?"
                
            return response
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return "I'm currently improving my responses. Please try again later."


# Emergency testing function
def emergency_test():
    print("\n=== Running Emergency Tests ===")
    service = ChatService()
    
    test_questions = [
        "What is anxiety?",
        "How can I manage stress?",
        "What are symptoms of depression?"
    ]
    
    for question in test_questions:
        print(f"\nQ: {question}")
        response = service.generate_response(question)
        print(f"A: {response}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    emergency_test()