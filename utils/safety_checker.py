import torch
from transformers import pipeline
from typing import Dict, Optional

class SafetyChecker:
    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        self.crisis_phrases = [
            "kill myself", "want to die", "end it all",
            "suicide", "self harm", "hurt myself"
        ]
        
        # Load pre-trained safety models
        try:
            self.toxicity_checker = pipeline(
                "text-classification",
                model="unitary/toxic-bert",
                device=self.device
            )
            self.emotion_detector = pipeline(
                "text-classification",
                model="SamLowe/roberta-base-go_emotions",
                device=self.device
            )
        except Exception as e:
            print(f"Safety models failed to load: {e}")
            self.fallback_mode = True
        else:
            self.fallback_mode = False

    def is_unsafe(self, text: str) -> bool:
        text_lower = text.lower()
        
        # 1. Immediate crisis phrases (highest priority)
        crisis_phrases = {
            "kill myself", "end my life", "want to die",
            "suicide", "no reason to live", "end it all"
        }
        if any(phrase in text_lower for phrase in crisis_phrases):
            return True
            
        # 2. Toxic content detection
        if not self.fallback_mode:
            try:
                tox_result = self.toxicity_checker(text)[0]
                if tox_result['label'] == 'toxic' and tox_result['score'] > 0.7:
                    return True
            except:
                self.fallback_mode = True
        
        return False

    def get_crisis_resources(self) -> Dict[str, str]:
        """Return emergency contacts based on location"""
        return {
            "US": "988 Suicide & Crisis Lifeline",
            "UK": "116 123 (Samaritans)",
            "IN": "91-9820466726 (Aasra)",
            "Global": "https://findahelpline.com"
        }