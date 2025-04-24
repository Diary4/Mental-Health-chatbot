import os
import json
import random
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from services.document_retrieval import DocumentRetrievalService
from utils.response_validator import MentalHealthResponseValidator
from utils.topic_checker import is_mental_health_topic
from dotenv import load_dotenv
from utils.llm_dynamic_generator import generate_dynamic_llm

load_dotenv()


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

        # Conversation history (session-level only)
        self.conversation_history = []

    def generate_response(self, user_input: str) -> str:
        try:
            # 0. Clean input and record in history
            user_input_clean = user_input.strip()
            self.conversation_history.append({"role": "user", "content": user_input_clean})

            # 1. Check if it's a mental health topic first
            if not is_mental_health_topic(user_input_clean):
                # For non-mental health topics, provide a clear redirection
                redirection_response = (
                    "I'm here to support you with mental health and emotional well-being. "
                    "I don't provide general knowledge or answer non-mental health related questions. "
                    "Would you like to talk about how you're feeling or any emotional challenges you're facing?"
                )
                self.conversation_history.append({"role": "assistant", "content": redirection_response})
                return redirection_response

            # 2. Static direct replies
            lower = user_input_clean.lower()
            for topic, replies in self.responses.items():
                if topic in lower:
                    response = random.choice(replies)
                    self.conversation_history.append({"role": "assistant", "content": response})
                    return response

            # 3. Static advice handling
            for topic, advice_section in self.advice.items():
                if topic in lower:
                    response = random.choice(list(advice_section.values()))
                    self.conversation_history.append({"role": "assistant", "content": response})
                    return response

            # 4. Build contextual input from last user input
            last_user_input = ""
            for item in reversed(self.conversation_history):
                if item["role"] == "user" and item["content"] != user_input_clean:
                    last_user_input = item["content"]
                    break
            combined_input = f"{last_user_input} {user_input_clean}".strip()

            # 5. First try static document retrieval
            fallback = self.retriever.search(combined_input)
            if fallback:
                self.conversation_history.append({"role": "assistant", "content": fallback})
                return fallback

            # 6. Generate dynamically using Gemini
            dyn_resp = self._generate_dynamic(combined_input)
            validated = self.validator.validate_response(user_input_clean, dyn_resp)
            final = validated if validated else dyn_resp
            self.conversation_history.append({"role": "assistant", "content": final})
            return final

        except Exception as e:
            print(f"Error in generate_response: {e}")
            return "I'm here to support you. Could you tell me more about how you're feeling?"

    def _generate_dynamic(self, user_input: str) -> str:
        return generate_dynamic_llm(user_input)

    def validate_response(self, user_input: str, bot_response: str) -> str:
        # Final pass through custom validator
        result = self.validator.validate_response(user_input, bot_response)
        return result if result else bot_response