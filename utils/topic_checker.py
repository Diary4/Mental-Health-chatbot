from transformers import pipeline
import re

# Load classifier once (ideally in a singleton/global if reused often)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Keywords related to mental health and emotions
MENTAL_HEALTH_KEYWORDS = [
    # Basic emotions
    "feel", "feeling", "emotion", "emotional", "mood", "sad", "happy", "angry", "fear", "scared",
    "afraid", "nervous", "anxious", "worried", "stressed", "overwhelmed", "depressed", "lonely",
    "isolated", "hopeless", "helpless", "worthless", "guilty", "ashamed", "embarrassed", "proud",
    "confident", "excited", "joy", "content", "peaceful", "calm", "relaxed", "tired", "exhausted",
    
    # Mental health terms
    "mental", "psychological", "psychiatric", "therapy", "counsel", "psych", "mind", "brain",
    "thought", "thinking", "memory", "concentration", "focus", "sleep", "insomnia", "appetite",
    "eating", "energy", "motivation", "self-esteem", "confidence", "self-care", "well-being",
    
    # Coping and support
    "cope", "coping", "handle", "manage", "deal", "struggle", "challenge", "difficult", "hard",
    "bad", "good", "better", "worse", "improve", "help", "support", "advice", "guidance",
    
    # Life situations
    "relationship", "family", "friend", "work", "job", "school", "study", "pressure", "stress",
    "trauma", "grief", "loss", "change", "transition", "adjust", "adapt", "crisis", "emergency"
]

def contains_mental_health_keywords(text):
    """Check if text contains any mental health related keywords"""
    text_lower = text.lower()
    # Check for exact matches
    if any(keyword in text_lower for keyword in MENTAL_HEALTH_KEYWORDS):
        return True
    
    # Check for emotional expressions
    emotional_patterns = [
        r"i (feel|am feeling) .*",
        r"i'm (feeling )?.*",
        r"i am .*",
        r"makes me feel .*",
        r"feel like .*",
        r"feeling .*",
        r"i have been feeling .*",
        r"i've been feeling .*",
        r"i have been .*",
        r"i've been .*"
    ]
    
    return any(re.search(pattern, text_lower) for pattern in emotional_patterns)

def is_mental_health_topic(text):
    # First check for direct keywords and emotional expressions
    if contains_mental_health_keywords(text):
        return True

    # If no direct matches, use the classifier
    candidate_labels = [
        "mental health and emotional well-being",
        "general knowledge and facts",
        "technical and mechanical topics",
        "geography and locations",
        "sports and physical activities",
        "entertainment and media",
        "science and technology",
        "history and culture"
    ]

    try:
        result = classifier(text, candidate_labels)

        if isinstance(result, dict) and "labels" in result and "scores" in result:
            top_label = result['labels'][0]
            top_score = result['scores'][0]
            
            # Be more lenient with the confidence threshold for emotional expressions
            return (top_label == "mental health and emotional well-being" and 
                   (top_score > 0.5 or "feel" in text.lower() or "feeling" in text.lower()))
        else:
            # If classifier fails, check for basic emotional expressions
            return "feel" in text.lower() or "feeling" in text.lower()
    except Exception as e:
        print(f"Topic classification error: {e}")
        # If classifier fails, check for basic emotional expressions
        return "feel" in text.lower() or "feeling" in text.lower()
