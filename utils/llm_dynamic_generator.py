import os
from dotenv import load_dotenv
from google import generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Correct model usage
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_dynamic_llm(prompt: str) -> str:
    try:
        # Add context about being a mental health assistant
        system_prompt = """You are a compassionate mental health assistant. Your role is to:
        1. Listen actively and empathetically
        2. Provide supportive responses
        3. Encourage healthy coping strategies
        4. Maintain a non-judgmental tone
        5. Focus on emotional well-being
        
        Please respond to the following message with this context in mind:"""
        
        full_prompt = f"{system_prompt}\n\nUser: {prompt}"
        
        response = model.generate_content(full_prompt)
        
        # Check if response has expected text
        if hasattr(response, "text"):
            return response.text.strip()
        elif hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].content.parts[0].text
        else:
            return "I'm here to listen and support you. Could you tell me more about how you're feeling?"

    except Exception as e:
        print(f"[Gemini Error] {e}")
        return "I'm here to support you. Could you share more about what's on your mind?"
