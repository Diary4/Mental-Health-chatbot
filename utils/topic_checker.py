from transformers import pipeline
import re

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

MENTAL_HEALTH_KEYWORDS = [
    # Original keywords (keep all existing ones)
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
    "accept", "accepted", "reject", "rejected", "understand", "understood", "listen", "heard",

    # NEWLY ADDED KEYWORDS (100+ more)
    "hate", "hated", "hating", "dislike", "unwanted", "unloved", "useless", "failure", "loser",
    "ugly", "stupid", "dumb", "hopeless", "helpless", "pathetic", "worthless", "inadequate",
    "insecure", "self-doubt", "self-loathing", "self-harm", "cutting", "suicidal", "suicide",
    "end my life", "kill myself", "don't want to live", "overdose", "hang myself", "jump off",
    "self-destructive", "self-sabotage", "panic", "panic attack", "breakdown", "meltdown",
    "burnout", "exhausted", "drained", "empty", "numb", "dissociate", "disconnected", "triggered",
    "flashback", "nightmare", "ptsd", "traumatized", "abuse", "bullied", "harassed", "humiliated",
    "betrayed", "abandonment", "neglected", "unworthy", "unlovable", "unimportant", "ignored",
    "invisible", "outcast", "alone", "no friends", "can't connect", "social anxiety", "phobia",
    "paranoia", "delusional", "hearing voices", "psychosis", "mania", "manic", "bipolar",
    "borderline", "bpd", "ocd", "eating disorder", "anorexia", "bulimia", "body dysmorphia",
    "self-image", "self-worth", "self-confidence", "self-esteem", "self-hate", "self-pity",
    "self-blame", "guilt", "shame", "regret", "remorse", "despair", "misery", "suffering",
    "emotional pain", "hurt", "heartache", "grieving", "mourning", "loss", "death", "died",
    "passed away", "funeral", "bereavement", "divorce", "breakup", "cheated", "lied to",
    "gaslighting", "manipulated", "toxic", "narcissist", "sociopath", "psychopath", "violence",
    "assault", "rape", "molestation", "trafficking", "addiction", "alcoholic", "drugs", "overdose",
    "relapse", "sobriety", "recovery", "therapy", "counseling", "psychiatrist", "psychologist",
    "medication", "antidepressants", "ssri", "prozac", "zoloft", "xanax", "valium", "klonopin",
    "hospitalization", "mental ward", "psych ward", "sectioned", "5150", "suicide watch",
    "crisis line", "hotline", "help me", "save me", "i can't take it", "i give up", "i quit",
    "i'm done", "no way out", "trapped", "no hope", "no future", "nothing matters", "why bother",
    "what's the point", "meaningless", "purposeless", "why am I here", "existential", "nihilism",
    "dark thoughts", "intrusive thoughts", "voices", "hallucinations", "delusions", "paranoid",
    "persecuted", "stalked", "watched", "spied on", "conspiracy", "government", "fbi", "cia",
    "they're after me", "people talk about me", "whispers", "laughing at me", "judging me",
    "mocking me", "bullying me", "gossip", "rumors", "lied about", "framed", "set up", "betrayed",
    "backstabbed", "used", "manipulated", "controlled", "dominated", "abused", "victimized",
    "scapegoat", "black sheep", "rebel", "outcast", "misfit", "weirdo", "freak", "alien",
    "different", "don't fit in", "no one understands", "alone in this world", "no one cares",
    "no one listens", "no one helps", "ignored", "dismissed", "invalidated", "gaslit", "crazy",
    "insane", "psycho", "mental case", "unstable", "broken", "damaged", "unfixable", "too much",
    "too sensitive", "too emotional", "too needy", "too clingy", "too dependent", "too weak",
    "pathetic", "failure", "disappointment", "embarrassment", "shameful", "regretful", "sorry",
    "apologize", "forgive me", "i messed up", "i ruined everything", "it's all my fault",
    "i deserve this", "i deserve pain", "i deserve to die", "i'm a burden", "i'm worthless",
    "i'm useless", "i'm nothing", "i'm nobody", "i don't matter", "i hate myself", "i hate my life",
    "i wish i was dead", "i wish i was never born", "i want to disappear", "i want to sleep forever",
    "i can't go on", "i can't do this anymore", "make it stop", "end the pain", "end the suffering",
    "no more", "enough", "i give up", "i surrender", "i quit", "i'm done", "goodbye", "farewell",
    "last words", "final message", "no one will miss me", "they'll be better off", "no one cares",
    "the world is cruel", "life is pain", "existence is suffering", "why was i born", "what's the point",
    "nothing gets better", "it never ends", "i'm stuck", "i'm trapped", "no escape", "no way out",
    "helpless", "powerless", "weak", "fragile", "broken beyond repair", "too damaged to fix",
    "lost cause", "hopeless case", "beyond help", "too far gone", "irredeemable", "monster",
    "demon", "evil", "cursed", "doomed", "damned", "hell", "punishment", "karma", "fate",
    "destiny", "why me", "what did i do", "i didn't ask for this", "i don't deserve this",
    "life isn't fair", "the universe hates me", "god hates me", "no higher power", "abandoned by god",
    "prayed but nothing", "faith lost", "no belief", "no hope", "no light", "only darkness",
    "void", "emptiness", "numb", "dead inside", "soulless", "heartless", "cold", "unfeeling",
    "robot", "zombie", "going through motions", "fake smile", "mask", "pretending", "acting",
    "no real emotions", "hollow", "shell", "ghost", "walking dead", "barely alive", "just existing",
    "not living", "surviving", "enduring", "suffering", "waiting to die", "waiting for death",
    "longing for death", "death wish", "suicidal ideation", "planning suicide", "suicide method",
    "suicide note", "final letter", "last goodbye", "no turning back", "no second thoughts",
    "ready to die", "prepared to die", "accepting death", "welcoming death", "death is peace",
    "death is freedom", "death is escape", "no more pain", "no more suffering", "eternal sleep",
    "rest in peace", "finally free", "release", "liberation", "end of pain", "end of suffering",
    "no more tears", "no more sadness", "no more anger", "no more fear", "no more anxiety",
    "no more stress", "no more pressure", "no more expectations", "no more disappointment",
    "no more failure", "no more shame", "no more guilt", "no more regret", "no more loneliness",
    "no more heartbreak", "no more betrayal", "no more abuse", "no more trauma", "no more memories",
    "no more past", "no more future", "no more present", "no more time", "no more existence",
    "nothingness", "void", "oblivion", "nonexistence", "peace at last", "silence", "darkness",
    "eternal rest", "final sleep", "never wake up", "never again", "the end", "goodbye forever"
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
