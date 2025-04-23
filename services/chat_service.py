import os
import json
import random
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from services.document_retrieval import DocumentRetrievalService
from utils.response_validator import MentalHealthResponseValidator
from utils.topic_checker import is_mental_health_topic


def load_json_folder(folder_path: str) -> dict:
    """
    Load all JSON files in a folder into a dict keyed by filename (without extension).
    """
    data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                key = filename.replace('.json', '')
                data[key] = json.load(f)
    return data


class ChatService:
    def __init__(self):
        # Load static responses and advice
        self.responses = load_json_folder("data/responses")
        self.advice = load_json_folder("data/advice")

        # Validator to enforce safe outputs
        self.validator = MentalHealthResponseValidator()

        # Retriever for domain-specific resources
        self.retriever = DocumentRetrievalService(
            "data/mental_health_resources/mental_health_dataset_improved.jsonl"
        )

        # Dynamic generation model
        model_name = "microsoft/DialoGPT-small"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.eval()
        if torch.cuda.is_available():
            self.model.to('cuda')

        # Conversation history (session-level)
        self.conversation_history = []

        # Persistent memory file for learning
        self.memory_file = "data/conversations.json"
        self.memory = []
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                try:
                    self.memory = json.load(f)
                except json.JSONDecodeError:
                    self.memory = []
        else:
            # Initialize empty memory
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
            self.memory = []

    def _save_to_memory(self, user_input: str, response: str):
        entry = {"user": user_input.strip(), "bot": response}
        self.memory.append(entry)
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=2)

    def _check_memory(self, user_input: str) -> str:
        lookup = user_input.strip().lower()
        for entry in self.memory:
            if entry["user"].lower() == lookup:
                return entry["bot"]
        return None

    def _generate_dynamic(self, user_input: str) -> str:
        # Encode input with EOS token and optional conversation history
        input_ids = self.tokenizer.encode(user_input + self.tokenizer.eos_token, return_tensors="pt")
        if torch.cuda.is_available():
            input_ids = input_ids.to('cuda')

        # Generate a response
        output_ids = self.model.generate(
            input_ids,
            max_length=input_ids.shape[-1] + 50,
            pad_token_id=self.tokenizer.eos_token_id,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7
        )
        response = self.tokenizer.decode(
            output_ids[:, input_ids.shape[-1]:][0],
            skip_special_tokens=True
        )
        return response.strip()

    def generate_response(self, user_input: str) -> str:
        # Record user input in session history
        self.conversation_history.append({"role": "user", "content": user_input})
        user_input_clean = user_input.strip()

        # 1. Persistent memory lookup
        memory_resp = self._check_memory(user_input_clean)
        if memory_resp:
            self.conversation_history.append({"role": "assistant", "content": memory_resp})
            return memory_resp

        # 2. Static responses
        lower = user_input_clean.lower()
        for topic, replies in self.responses.items():
            if topic in lower:
                response = random.choice(replies)
                self._save_to_memory(user_input_clean, response)
                self.conversation_history.append({"role": "assistant", "content": response})
                return response

        # 3. Static advice
        for topic, advice_section in self.advice.items():
            if topic in lower:
                response = random.choice(list(advice_section.values()))
                self._save_to_memory(user_input_clean, response)
                self.conversation_history.append({"role": "assistant", "content": response})
                return response

        # 4. Dynamic generation for mental health topics
        if is_mental_health_topic(user_input_clean):
            # Try retrieval
            fallback = self.retriever.search(user_input_clean)
            if fallback:
                self._save_to_memory(user_input_clean, fallback)
                self.conversation_history.append({"role": "assistant", "content": fallback})
                return fallback

            # Generate dynamically
            dyn_resp = self._generate_dynamic(user_input_clean)
            # Validate and sanitize
            validated = self.validator.validate_response(user_input_clean, dyn_resp)
            final = validated if validated else dyn_resp
            self._save_to_memory(user_input_clean, final)
            self.conversation_history.append({"role": "assistant", "content": final})
            return final

        # 5. Off-topic fallback
        off_msg = (
            "I'm here to help with mental health-related topics. "
            "Could we talk about how you're feeling today?"
        )
        self.conversation_history.append({"role": "assistant", "content": off_msg})
        return off_msg

    def validate_response(self, user_input: str, bot_response: str) -> str:
        # Final pass through custom validator
        result = self.validator.validate_response(user_input, bot_response)
        return result if result else bot_response
