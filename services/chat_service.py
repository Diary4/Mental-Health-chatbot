import os
import json
import random
from services.document_retrieval import DocumentRetrievalService
from utils.response_validator import MentalHealthResponseValidator      
from utils.topic_checker import is_mental_health_topic


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
        # Load responses and advice
        self.responses = load_json_folder("data/responses")
        self.advice = load_json_folder("data/advice")

        # Validator and retriever for mental health resources
        self.validator = MentalHealthResponseValidator()
        self.retriever = DocumentRetrievalService(
            "data/mental_health_resources/mental_health_dataset_improved.jsonl"
        )

        # Conversation history and memory
        self.conversation_history = []
        self.memory_file = "data/conversations.json"
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                try:
                    self.memory = json.load(f)
                except json.JSONDecodeError:
                    self.memory = []
        else:
            self.memory = []

    def _save_to_memory(self, user_input: str, response: str):
        entry = {"user": user_input, "bot": response}
        self.memory.append(entry)
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=2)

    def _check_memory(self, user_input: str) -> str:
        for entry in self.memory:
            if entry["user"].strip().lower() == user_input.strip().lower():
                return entry["bot"]
        return None

    def generate_response(self, user_input: str) -> str:
        self.conversation_history.append({"role": "user", "content": user_input})

        # 1. Memory lookup
        memory_response = self._check_memory(user_input)
        if memory_response:
            self.conversation_history.append({"role": "assistant", "content": memory_response})
            return memory_response

        # 2. Exact-match responses and advice
        user_input_lower = user_input.lower()
        for topic, replies in self.responses.items():
            if topic in user_input_lower:
                response = random.choice(replies)
                self._save_to_memory(user_input, response)
                self.conversation_history.append({"role": "assistant", "content": response})
                return response

        for topic, advice_section in self.advice.items():
            if topic in user_input_lower:
                response = random.choice(list(advice_section.values()))
                self._save_to_memory(user_input, response)
                self.conversation_history.append({"role": "assistant", "content": response})
                return response

        # 3. Check if it's a mental health related topic
        if is_mental_health_topic(user_input):
            # Try retrieval
            fallback = self.retriever.search(user_input)
            if fallback:
                self._save_to_memory(user_input, fallback)
                self.conversation_history.append({"role": "assistant", "content": fallback})
                return fallback

            # Default mental health response
            default_resp = random.choice(self.responses.get("default", [
                "I'm here to support you. Could you tell me more about what's going on?",
                "I'm listening. What would you like to talk about today?"
            ]))
            self._save_to_memory(user_input, default_resp)
            self.conversation_history.append({"role": "assistant", "content": default_resp})
            return default_resp

        # 4. Off-topic fallback
        off_topic_msg = (
            "I'm here to help with mental health-related topics. "
            "Could we talk about how you're feeling today?"
        )
        self.conversation_history.append({"role": "assistant", "content": off_topic_msg})
        return off_topic_msg

    def validate_response(self, user_input: str, bot_response: str) -> str:
        validation_result = self.validator.validate_response(user_input, bot_response)
        return validation_result if validation_result else bot_response
