from transformers import pipeline
import re

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

MENTAL_HEALTH_KEYWORDS = [
    
    "feel", "feeling", "emotion", "emotional", "mood", "sad", "happy", "angry", "fear", "scared",
    "afraid", "nervous", "anxious", "worried", "stressed", "overwhelmed", "depressed", "lonely",
    "isolated", "hopeless", "helpless", "worthless", "guilty", "ashamed", "embarrassed", "proud",
    "confident", "excited", "joy", "content", "peaceful", "calm", "relaxed", "tired", "exhausted",
    
    "mental", "psychological", "psychiatric", "therapy", "counsel", "psych", "mind", "brain",
    "thought", "thinking", "memory", "concentration", "focus", "sleep", "insomnia", "appetite",
    "eating", "energy", "motivation", "self-esteem", "confidence", "self-care", "well-being",
    
    "cope", "coping", "handle", "manage", "deal", "struggle", "challenge", "difficult", "hard",
    "bad", "good", "better", "worse", "improve", "help", "support", "advice", "guidance",
    
    "relationship", "family", "friend", "work", "job", "school", "study", "pressure", "stress",
    "trauma", "grief", "loss", "change", "transition", "adjust", "adapt", "crisis", "emergency",
    
    "love", "loved", "loving", "need", "needed", "want", "wanted", "desire", "desired", "miss",
    "missing", "care", "cared", "caring", "someone", "somebody", "person", "people", "partner",
    "friend", "friendship", "family", "parent", "child", "sibling", "brother", "sister", "mother",
    "father", "spouse", "wife", "husband", "boyfriend", "girlfriend", "crush", "dating", "breakup",
    "broken", "heart", "heartbroken", "rejection", "rejected", "abandon", "abandoned", "alone",
    "lonely", "isolation", "isolated", "connection", "connect", "connected", "belong", "belonging",
    "accept", "accepted", "reject", "rejected", "understand", "understood", "listen", "heard"
]

def contains_mental_health_keywords(text):
    """Check if text contains any mental health related keywords"""
    text_lower = text.lower()
    if any(keyword in text_lower for keyword in MENTAL_HEALTH_KEYWORDS):
        return True
    
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
        r"i've been .*",
        r"i (need|want|love|miss|care about) .*",
        r"i'm (in love|heartbroken|lonely|alone) .*",
        r"no one (understands|listens|cares) .*",
        r"someone (doesn't|does not) (love|care|understand) .*",
        r"i feel (alone|lonely|rejected|abandoned) .*",
        r"i (can't|cannot) (find|get) (someone|anyone) .*",
        r"i (wish|want) (someone|somebody) .*",
        r"i (don't|do not) have (anyone|someone) .*"
    ]
    
    return any(re.search(pattern, text_lower) for pattern in emotional_patterns)

def is_mental_health_topic(text):
    if contains_mental_health_keywords(text):
        return True

    candidate_labels = [
        "mental health and emotional well-being",
        "relationships and emotional connections",
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
            
            return ((top_label in ["mental health and emotional well-being", "relationships and emotional connections"] and 
                    top_score > 0.5) or
                   any(word in text.lower() for word in ["feel", "feeling", "love", "need", "want", "miss", "care"]))
        else:
            return any(word in text.lower() for word in ["feel", "feeling", "love", "need", "want", "miss", "care"])
    except Exception as e:
        print(f"Topic classification error: {e}")
        return any(word in text.lower() for word in ["feel", "feeling", "love", "need", "want", "miss", "care"])
