import random

response_templates = {
    "stress": [
        "When stressed, try box breathing: Inhale 4s → Hold 4s → Exhale 6s. Repeat 3 times.",
        "Stress often comes from feeling overwhelmed. What's one small thing you can control right now?"
    ],
    "worthless": [
        "You're describing deep pain. These feelings are valid, but they don't define your worth.",
        "I hear how hard this is. Would you share what triggered this feeling?"
    ],
    "depression": [
        "Depression can make everything feel heavy. Have you been able to get outside today?",
        "This sounds really difficult. Remember: healing isn't linear."
    ],
    "crisis": "Please reach out to a crisis hotline immediately. You're not alone in this.",
    "default": [
        "I'm listening. Tell me more.",
        "Help me understand what this is like for you."
    ]
}

def get_template(user_input: str) -> str:
    """Smart template selection with keyword matching"""
    input_lower = user_input.lower()
    
    if any(word in input_lower for word in ["stress", "overwhelmed"]):
        return random.choice(response_templates["stress"])
    elif any(word in input_lower for word in ["worthless", "useless"]):
        return random.choice(response_templates["worthless"])
    elif any(word in input_lower for word in ["depress", "hopeless"]):
        return random.choice(response_templates["depression"])
    elif any(word in input_lower for word in ["kill myself", "end it all"]):
        return response_templates["crisis"]
    else:
        return random.choice(response_templates["default"])