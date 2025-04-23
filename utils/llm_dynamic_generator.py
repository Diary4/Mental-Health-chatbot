import os
import requests

API_KEY = os.getenv("GEMINI_API_KEY") 
MODEL_URL = "https://generativelanguage.googleapis.com/v1beta/models/text-bison-001:generateText"

def generate_dynamic_llm(prompt: str) -> str:
    print(f"[LLM Called with prompt]: {prompt}")  # Add this line for debugging
    try:
        response = requests.post(
            MODEL_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "prompt": {"text": prompt},
                "temperature": 0.7,
                "candidateCount": 1,
            }
        )
        response.raise_for_status()
        return response.json()["candidates"][0]["output"]
    except Exception as e:
        print(f"[LLM Error]: {e}")
        return "I'm here for you. Can you share more about what you're feeling?"
