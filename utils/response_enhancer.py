import random

def enhance_response(response):
    # Strip and clean
    response = response.strip()

    # Handle too short or empty responses
    if len(response.split()) < 5:
        return "I'm here with you — it's okay to take your time. Could you share a bit more?"

    # Replace robotic or repetitive language
    replacements = {
        "I understand": [
            "That makes sense.",
            "I hear you.",
            "Thank you for sharing that with me."
        ],
        "You are not alone": [
            "You're not alone in this — many people go through similar feelings.",
            "What you're feeling is valid and important."
        ],
        "mental health": [
            "your well-being",
            "your mental wellness",
            "how you've been feeling lately"
        ]
    }

    for phrase, variations in replacements.items():
        if phrase.lower() in response.lower():
            response = response.replace(phrase, random.choice(variations))

    # Add an empathetic prefix (but randomly)
    empathy_starters = [
        "Thank you for being open with me. ",
        "It's completely okay to feel this way. ",
        "I'm really glad you reached out. ",
        ""
    ]
    response = random.choice(empathy_starters) + response

    return response
