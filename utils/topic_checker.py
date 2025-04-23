from transformers import pipeline

# Load classifier once (ideally in a singleton/global if reused often)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def is_mental_health_topic(text):
    candidate_labels = ["mental health", "general knowledge", "car mechanics", "geography", "sports"]

    try:
        result = classifier(text, candidate_labels)

        if isinstance(result, dict) and "labels" in result:
            top_label = result['labels'][0]
            return top_label == "mental health"
        else:
            # Unexpected format
            return False
    except Exception as e:
        print(f"Topic classification error: {e}")
        return False
