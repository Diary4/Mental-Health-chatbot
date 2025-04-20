import os
import json
import random
from services.document_retrieval import DocumentRetrievalService
from utils.response_validator import MentalHealthResponseValidator      


def load_json_folder(folder_path: str) -> dict:
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
        self.retriever = DocumentRetrievalService("data/mental_health_resources/mental_health_dataset_improved.jsonl") 
        self.conversation_history = []

    def generate_response(self, user_input: str) -> str:
        self.conversation_history.append({"role": "user", "content": user_input})

        user_input_lower = user_input.lower()

        for topic in self.responses:
            if topic in user_input_lower:
                response = random.choice(self.responses[topic])
                self.conversation_history.append({"role": "assistant", "content": response})
                return response

        for topic in self.advice:
            if topic in user_input_lower:
                advice_section = self.advice[topic]
                selected_key = random.choice(list(advice_section.keys()))
                advice = advice_section[selected_key]
                self.conversation_history.append({"role": "assistant", "content": advice})
                return advice

        fallback_response = self.retriever.search(user_input)
        if fallback_response:
            self.conversation_history.append({"role": "assistant", "content": fallback_response})
            return fallback_response

        default_response = random.choice(self.responses.get("default", [
            "I'm here to support you. Could you tell me more about what's going on?",
            "I'm listening. What would you like to talk about today?"
        ]))
        self.conversation_history.append({"role": "assistant", "content": default_response})
        return default_response

    def validate_response(self, user_input: str, bot_response: str) -> str:
        validation_result = self.validator.validate_response(user_input, bot_response)
        return validation_result if validation_result else bot_response
