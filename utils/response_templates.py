# utils/response_templates.py
import random
import os
import json

# Base responses for when dataset fails
DEFAULT_RESPONSES = [
    "I'm here to listen and support you. Could you tell me more about what's on your mind?",
    "Thank you for sharing that with me. How long have you been feeling this way?",
    "I understand this can be difficult to talk about. What specific aspects are most challenging for you?",
    "Your feelings are valid. What strategies have you tried so far to cope with this situation?",
    "It sounds like you're going through a lot. Let's take a moment to focus on what might help you feel better right now."
]

# Crisis responses
CRISIS_RESPONSES = [
    "I'm deeply concerned about what you're sharing. Please consider contacting a crisis line immediately at 988 (US) or your local emergency services.",
    "This sounds serious. I strongly encourage you to reach out to a mental health professional or crisis support service right away.",
    "Your safety is the priority. Please consider calling a crisis helpline or going to your nearest emergency room for immediate support."
]

# Emotion-specific responses
EMOTION_RESPONSES = {
    "admiration": [
        "It's wonderful to appreciate positive qualities in others. How does this admiration influence you?",
        "Recognizing what we admire can tell us a lot about our own values. What about this resonates with you?"
    ],
    "amusement": [
        "Finding moments of joy and humor is so important for our wellbeing. What other things bring you this feeling?",
        "It's great that you found something amusing. Laughter can be really therapeutic."
    ],
    "anger": [
        "Anger often signals that a boundary has been crossed or a need isn't being met. What do you think this anger is telling you?",
        "It's natural to feel angry sometimes. Can we explore what triggered this feeling and how you might address it constructively?"
    ],
    "annoyance": [
        "Minor frustrations can sometimes build up over time. How long have you been feeling this way?",
        "That sounds irritating. What strategies do you usually use when you feel annoyed by something?"
    ],
    "anxiety": [
        "When anxiety arises, try the 5-4-3-2-1 grounding technique: notice 5 things you see, 4 things you can touch, 3 things you hear, 2 things you smell, and 1 thing you taste.",
        "Anxiety can make threats seem larger than they are. Let's examine your concerns together and see if we can put them in perspective.",
        "Your anxiety is a response trying to protect you. Let's work on distinguishing between helpful caution and excessive worry."
    ],
    "approval": [
        "It's affirming when things align with our values or expectations. What specifically meets your approval here?",
        "Positive recognition can be motivating. How does this approval affect your outlook?"
    ],
    "caring": [
        "Your compassion for others shows emotional intelligence. How do you balance caring for others with self-care?",
        "Caring deeply is a beautiful quality. How does this caring connection affect your wellbeing?"
    ],
    "confusion": [
        "Confusion often happens when we face complex situations. Would it help to break this down into smaller parts?",
        "It's okay to not have all the answers right away. What part feels most unclear to you?"
    ],
    "curiosity": [
        "Curiosity is a wonderful driver of growth and learning. What specifically sparked your interest?",
        "Following our curiosity can lead to meaningful discoveries. What are you hoping to learn more about?"
    ],
    "desire": [
        "Our desires can tell us a lot about what we value and need. How long have you wanted this?",
        "It's natural to have desires and aspirations. How does this particular desire align with your overall goals?"
    ],
    "depression": [
        "Depression can distort our perspective, making it hard to see positives. What's one small positive thing you noticed today, however minor?",
        "I hear how heavy this feels. You're not alone in this experience - depression affects many people and there are pathways forward.",
        "When we're depressed, even small tasks can feel overwhelming. Could we identify one tiny step that might feel manageable?"
    ],
    "disappointment": [
        "Disappointment often comes from unmet expectations. What were you hoping would happen?",
        "I'm sorry things didn't work out as you wanted. How are you taking care of yourself through this disappointment?"
    ],
    "disapproval": [
        "When something doesn't align with our values, it can be concerning. What specific aspects do you find problematic?",
        "It sounds like this conflicts with what you believe is right. Could you share more about the values that inform your perspective?"
    ],
    "disgust": [
        "Strong aversions can sometimes be protective mechanisms. What about this situation triggers such a strong reaction?",
        "That sounds very off-putting to you. How does this feeling affect your choices or behavior?"
    ],
    "embarrassment": [
        "Embarrassment can be uncomfortable but is a universal human experience. Would it help to talk through what happened?",
        "Many of us are harder on ourselves than we would be on others in similar situations. How might you respond if a friend told you they experienced this?"
    ],
    "excitement": [
        "Your enthusiasm is palpable! What aspects of this are you most looking forward to?",
        "Excitement can be energizing. How does this positive anticipation affect your mood and outlook?"
    ],
    "fear": [
        "Fear serves as our internal alarm system, though sometimes it can be oversensitive. What's the core concern behind this fear?",
        "When we're afraid, our minds often go to worst-case scenarios. Would it help to explore both the fears and possible positive outcomes?"
    ],
    "gratitude": [
        "Practicing gratitude has been shown to positively impact our wellbeing. What other things are you appreciative of lately?",
        "That's a beautiful expression of thankfulness. How does focusing on gratitude affect your overall perspective?"
    ],
    "grief": [
        "Grief reflects the depth of our attachments and what matters to us. How are you caring for yourself through this loss?",
        "Loss can affect us in waves and in different ways. There's no right way to grieve. What support would be most helpful right now?"
    ],
    "joy": [
        "Those moments of joy are so important for our wellbeing. What other things bring you this feeling?",
        "It's wonderful when we experience genuine joy. How can you create more space for these positive experiences?"
    ],
    "love": [
        "Love is one of our most profound emotional experiences. How does this connection enrich your life?",
        "That sounds like a meaningful bond. How do you nurture this relationship?"
    ],
    "nervousness": [
        "Feeling nervous often happens when we care about outcomes. What specifically triggers this feeling?",
        "A certain amount of nervousness can actually help us perform better. What techniques help you manage these feelings?"
    ],
    "optimism": [
        "Your positive outlook is impressive. What helps you maintain this hopefulness?",
        "Optimism can be a powerful resource during challenges. How does this perspective help you navigate difficulties?"
    ],
    "pride": [
        "Taking pride in our achievements or qualities acknowledges our value. What specifically brings you this sense of pride?",
        "That's a meaningful accomplishment. How did you develop the qualities that made this possible?"
    ],
    "realization": [
        "Those moments of clarity can be quite powerful. What led to this insight?",
        "New realizations can shift our perspective significantly. How might this change things for you going forward?"
    ],
    "relief": [
        "Relief often comes after tension or worry. What changed to bring about this feeling?",
        "It must feel good to have that weight lifted. How are you celebrating this positive turn?"
    ],
    "sadness": [
        "Sadness is often connected to something we value or care about. What matters to you in this situation?",
        "I hear the sadness in what you're sharing. How are you taking care of yourself through these feelings?"
    ],
    "surprise": [
        "Unexpected events can really catch us off guard. How are you processing this surprise?",
        "That sounds quite unexpected. How has this changed your perspective?"
    ],
    "neutral": [
        "Thank you for sharing that with me. Would you like to explore any particular aspect of what you've mentioned?",
        "I appreciate you telling me more about your situation. What would be most helpful to focus on right now?"
    ]
}

# Try to load dataset responses or use defaults
def _load_dataset_responses():
    try:
        # Try local file first
        json_path = "data/mental_health_resources/mental_health_dataset.json"
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            responses = [item["therapist_response"] for item in data if "therapist_response" in item]
            if responses:
                return [r for r in responses if 20 < len(r) < 150]  # Filter for appropriate length
        
        # Fall back to imports if local file fails
        try:
            from datasets import load_dataset
            dataset = load_dataset("Amod/mental_health_counseling_conversations", split="train[:300]")
            responses = [item["therapist_response"] for item in dataset]
            return [r for r in responses if 20 < len(r) < 150]  # Filter for appropriate length
        except:
            pass
    except Exception as e:
        print(f"Error loading dataset responses: {e}")
    
    # Return default responses if all else fails
    return DEFAULT_RESPONSES

# Load responses when module is imported
BASE_RESPONSES = _load_dataset_responses()

def get_response(user_input: str, emotion: str = "") -> str:
    """Generate context-appropriate response"""
    input_lower = user_input.lower()
    
    # 1. Crisis detection
    crisis_terms = ["suicide", "kill myself", "end it all", "don't want to live", "better off dead"]
    if any(phrase in input_lower for phrase in crisis_terms):
        return random.choice(CRISIS_RESPONSES)
    
    # 2. Emotion-matched responses
    if emotion and emotion in EMOTION_RESPONSES:
        return random.choice(EMOTION_RESPONSES[emotion])
    
    # 3. Dataset-based or default response
    if BASE_RESPONSES:
        return random.choice(BASE_RESPONSES)
    else:
        return random.choice(DEFAULT_RESPONSES)