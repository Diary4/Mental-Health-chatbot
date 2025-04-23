import torch
from transformers import pipeline
from typing import Dict, Optional, List
import re

class SafetyChecker:
    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        self.fallback_mode = False
        
        self.crisis_patterns = [
            re.compile(r"\b(kill|end|harm)\b.*\b(my|me|self)\b", re.IGNORECASE),
            re.compile(r"\b(suicide|overdose|jump(ing|ed)?)\b", re.IGNORECASE),
            re.compile(r"\b(no reason to live|want to die)\b", re.IGNORECASE)
        ]
        
        self._load_models()

    def _load_models(self):
        """Safely load NLP models with fallback options"""
        try:
            self.toxicity_checker = pipeline(
                "text-classification",
                model="unitary/toxic-bert",
                device=self.device,
                max_length=512,
                truncation=True
            )
            
            self.emotion_detector = pipeline(
                "text-classification",
                model="SamLowe/roberta-base-go_emotions",
                device=self.device,
                top_k=3  
            )
        except Exception as e:
            print(f"⚠️ Safety models loading failed: {str(e)}")
            self.fallback_mode = True

    def is_unsafe(self, text: str) -> bool:
        """
        Enhanced safety check with multiple verification layers
        Returns True if the text indicates crisis or harmful intent
        """
        if not text.strip():
            return False
            
        text_lower = text.lower()
        
        # Layer 1: Fast pattern matching for immediate crisis
        if self._detect_crisis_patterns(text):
            return True
            
        # Layer 2: Toxic content detection (if models loaded)
        if not self.fallback_mode:
            try:
                # Check for toxic content
                tox_result = self.toxicity_checker(text[:1000])[0]  # Truncate to avoid OOM
                if tox_result['label'] == 'toxic' and tox_result['score'] > 0.85:  # Higher threshold
                    return True
                    
                # Check for extreme negative emotions
                emotions = self.emotion_detector(text[:1000])
                for emotion in emotions[0]:
                    if emotion['label'] in ['grief', 'despair'] and emotion['score'] > 0.9:
                        return True
            except Exception as e:
                print(f"⚠️ Safety check error: {str(e)}")
                self.fallback_mode = True
                
        return False

    def _detect_crisis_patterns(self, text: str) -> bool:
        """Advanced pattern matching for crisis phrases"""
        for pattern in self.crisis_patterns:
            if pattern.search(text):
                return True
                
        # Additional checks for self-harm references
        self_harm_phrases = [
            "cut myself", "self harm", "bleed out",
            "hang myself", "overdose", "jump off"
        ]
        return any(phrase in text.lower() for phrase in self_harm_phrases)

    def get_crisis_resources(self, country_code: Optional[str] = None) -> Dict[str, str]:
        """Return localized crisis resources with global fallback"""
        resources = {
            "US": {"text": "Text Home to 0000", "call": "964 750 000 0000"},
            "global": {
                "website": "https://findahelpline.com",
                "text": "WHO Mental Health Resources: https://www.who.int/mental_health"
            }
        }
        
        if country_code and country_code.upper() in resources:
            return resources[country_code.upper()]
        return resources["global"]

    def get_response_level(self, text: str) -> int:
        """
        Threat level classification:
        0 = Safe
        1 = Concerning (needs gentle probing)
        2 = Crisis (immediate intervention)
        """
        if self._detect_crisis_patterns(text):
            return 2
            
        if not self.fallback_mode:
            try:
                emotions = self.emotion_detector(text[:1000])[0]
                negative_scores = sum(
                    e['score'] for e in emotions 
                    if e['label'] in ['grief', 'despair', 'fear']
                )
                if negative_scores > 1.5:  # Combined threshold
                    return 1
            except:
                pass
                
        return 0