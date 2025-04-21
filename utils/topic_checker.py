# utils/topic_checker.py

from transformers import pipeline

# Load classifier once (can move to a global init if needed)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def is_mental_health_topic(text):
    candidate_labels = ["mental health", "general knowledge", "car mechanics", "geography", "sports"]
    
    result = classifier(text, candidate_labels)
    top_label = result['labels'][0]
    
    return top_label == "mental health"
