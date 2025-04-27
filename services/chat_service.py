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
from services.conversation_learning import ConversationLearning
from typing import List

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
        self.responses = load_json_folder("data/responses")
        self.advice = load_json_folder("data/advice")
        self.validator = MentalHealthResponseValidator()
        self.retriever = DocumentRetrievalService(
            "data/mental_health_resources/mental_health_dataset_improved.jsonl"
        )
        self.learning = ConversationLearning()

        model_name = "microsoft/DialoGPT-small"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.eval()
        if torch.cuda.is_available():
            self.model.to('cuda')

        self.conversation_history = []

    def generate_response(self, user_input: str) -> str:
        try:
            user_input_clean = user_input.strip()
            self.conversation_history.append({"role": "user", "content": user_input_clean})

            # Analyze conversation for learning
            self.learning.analyze_conversation(self.conversation_history)

            if not is_mental_health_topic(user_input_clean):
                redirection_response = (
                    "I'm here to support you with mental health and emotional well-being. "
                    "I don't provide general knowledge or answer non-mental health related questions. "
                    "Would you like to talk about how you're feeling or any emotional challenges you're facing?"
                )
                self.conversation_history.append({"role": "assistant", "content": redirection_response})
                self._save_conversation()
                return redirection_response

            lower = user_input_clean.lower()
            for topic, replies in self.responses.items():
                if topic in lower:
                    response = random.choice(replies)
                    self.conversation_history.append({"role": "assistant", "content": response})
                    self._save_conversation()
                    return response

            for topic, advice_section in self.advice.items():
                if topic in lower:
                    response = random.choice(list(advice_section.values()))
                    self.conversation_history.append({"role": "assistant", "content": response})
                    self._save_conversation()
                    return response

            last_user_input = ""
            for item in reversed(self.conversation_history):
                if item["role"] == "user" and item["content"] != user_input_clean:
                    last_user_input = item["content"]
                    break
            combined_input = f"{last_user_input} {user_input_clean}".strip()

            # Try static document retrieval
            fallback = self.retriever.search(combined_input)
            if fallback:
                self.conversation_history.append({"role": "assistant", "content": fallback})
                self._save_conversation()
                return fallback

            # Generate dynamically using Gemini
            dyn_resp = self._generate_dynamic(combined_input)
            validated = self.validator.validate_response(user_input_clean, dyn_resp)
            final = validated if validated else dyn_resp
            self.conversation_history.append({"role": "assistant", "content": final})
            self._save_conversation()
            return final

        except Exception as e:
            print(f"Error in generate_response: {e}")
            return "I'm here to support you. Could you tell me more about how you're feeling?"

    def _save_conversation(self):
        """Save the current conversation for learning"""
        if len(self.conversation_history) >= 2:  # Only save if we have at least one exchange
            self.learning.save_conversation(self.conversation_history)

    def get_learning_insights(self):
        """Get insights from conversation analysis"""
        return self.learning.generate_insights()

    def update_responses(self, topic: str, new_responses: List[str]):
        """Update responses for a specific topic"""
        response_file = f"data/responses/{topic}.json"
        self.learning.update_responses(response_file, new_responses)
        # Reload responses to include new ones
        self.responses = load_json_folder("data/responses")

    def _generate_dynamic(self, user_input: str) -> str:
        return generate_dynamic_llm(user_input)

    def validate_response(self, user_input: str, bot_response: str) -> str:
        # Final pass through custom validator
        result = self.validator.validate_response(user_input, bot_response)
        return result if result else bot_response