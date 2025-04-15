import re
from typing import Optional

class MentalHealthResponseValidator:
    def __init__(self):
        self.mental_health_keywords = {
            'anxiety', 'depression', 'stress', 'mental health', 
            'therapy', 'counseling', 'psychologist', 'psychiatrist',
            'panic', 'ocd', 'ptsd', 'bipolar', 'schizophrenia',
            'self-care', 'coping', 'wellbeing', 'mindfulness'
        }
        self.inappropriate_phrases = {
            "I'm not your friend", "I am your father", "Why not both",
            "I'm not a bot", "u Zaiyaq"
        }

    def validate_response(self, user_input: str, bot_response: str) -> Optional[str]:
        """Validate and potentially modify the bot response"""
        # Check for inappropriate phrases
        if any(phrase.lower() in bot_response.lower() for phrase in self.inappropriate_phrases):
            return "I'm sorry, I don't have an appropriate response for that. Could we focus on mental health topics?"
        
        # Check if response is relevant to mental health
        if not self._is_mental_health_related(user_input, bot_response):
            return self._get_redirect_response(user_input)
        
        return None  # Response is valid

    def _is_mental_health_related(self, user_input: str, response: str) -> bool:
        """Check if the conversation is about mental health"""
        input_text = user_input + " " + response
        return any(
            re.search(rf'\b{keyword}\b', input_text, re.IGNORECASE) 
            for keyword in self.mental_health_keywords
        )

    def _get_redirect_response(self, user_input: str) -> str:
        """Get a response to redirect to mental health topics"""
        if any(word in user_input.lower() for word in ['what', 'why', 'how']):
            return "That's an interesting question. In mental health contexts, we often find that..."
        return "I specialize in mental health topics. Could you tell me more about what's on your mind?"