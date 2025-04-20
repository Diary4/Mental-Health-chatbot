import json
import os
import difflib

class DocumentRetrievalService:
    def __init__(self, jsonl_path: str):
        self.data = self._load_jsonl(jsonl_path)

    def _load_jsonl(self, path: str):
        items = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    items.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
        return items

    def search(self, user_input: str, threshold: float = 0.6):
        best_match = None
        best_score = 0

        for item in self.data:
            question = item.get("question", "")
            answer = item.get("answer", "")
            if not question or not answer:
                continue

            score = difflib.SequenceMatcher(None, user_input.lower(), question.lower()).ratio()

            if score > best_score:
                best_score = score
                best_match = item

        if best_score >= threshold:
            return best_match["answer"]
        else:
            return None
