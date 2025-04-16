import re

def enhance_response(response):
    # Basic clean-up
    response = response.strip()
    
    # Avoid repeated generic lines
    if "I am a psychologist" in response:
        response = response.replace("I am a psychologist", "I'm here to support you with your mental well-being.")
    
    if "How do you feel about mental health" in response:
        response = "Mental health is important. You're doing the right thing by opening up."

    # Add empathy if the message is too short
    if len(response.split()) < 5:
        response = "I hear you. It might help to talk more about what you're feeling."

    return response
