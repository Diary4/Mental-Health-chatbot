import os
from dotenv import load_dotenv
from google import generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Correct model usage
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_dynamic_llm(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        
        # Check if response has expected text
        if hasattr(response, "text"):
            return response.text.strip()
        elif hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].content.parts[0].text
        else:
            return "I'm here for you. Could you tell me more about how you're feeling?"

    except Exception as e:
        print(f"[Gemini Error] {e}")
        return "I'm here to support you. Could you share more about what's on your mind?"
