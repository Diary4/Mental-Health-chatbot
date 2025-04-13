
PROFESSIONAL_KEYWORDS = [
    "try", "suggest", "technique", 
    "exercise", "might help", "consider"
]

def is_professional(response: str) -> bool:
    """Check if response contains mental health support content"""
    lower_response = response.lower()
    return any(kw in lower_response for kw in PROFESSIONAL_KEYWORDS)

def contains_harmful_content(response: str) -> bool:
    """Basic safety check"""
    blacklist = ["kill myself", "hurt others", "want to die"]
    return any(phrase in response.lower() for phrase in blacklist)