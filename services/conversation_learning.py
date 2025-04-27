import json
import os
from datetime import datetime
from collections import defaultdict
import re
from typing import List, Dict, Any

class ConversationLearning:
    def __init__(self, conversation_storage_path: str = "data/conversations"):
        self.conversation_storage_path = conversation_storage_path
        self.ensure_storage_directory()
        self.patterns = defaultdict(int)
        self.topics = defaultdict(int)
        
    def ensure_storage_directory(self):
        """Ensure the conversation storage directory exists"""
        os.makedirs(self.conversation_storage_path, exist_ok=True)
        
    def save_conversation(self, conversation: List[Dict[str, str]], user_id: str = "anonymous"):
        """Save a conversation to storage"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{user_id}_{timestamp}.json"
        filepath = os.path.join(self.conversation_storage_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": timestamp,
                "user_id": user_id,
                "conversation": conversation
            }, f, indent=2)
            
    def analyze_conversation(self, conversation: List[Dict[str, str]]):
        """Analyze conversation patterns and update learning"""
        for message in conversation:
            if message["role"] == "user":
                text = message["content"].lower()
                words = re.findall(r'\w+', text)
                
                for word in words:
                    if len(word) > 3: 
                        self.topics[word] += 1
                        
                for i in range(len(words) - 1):
                    pattern = f"{words[i]} {words[i+1]}"
                    self.patterns[pattern] += 1
                    
    def update_responses(self, response_file: str, new_responses: List[str]):
        """Update response file with new responses"""
        try:
            with open(response_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
           
            existing_responses = set(data.get("responses", []))
            for response in new_responses:
                if response not in existing_responses:
                    data["responses"].append(response)
                    
            with open(response_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Error updating responses: {e}")
            
    def get_common_topics(self, n: int = 10) -> List[str]:
        """Get the n most common topics from conversations"""
        return sorted(self.topics.items(), key=lambda x: x[1], reverse=True)[:n]
        
    def get_common_patterns(self, n: int = 10) -> List[str]:
        """Get the n most common patterns from conversations"""
        return sorted(self.patterns.items(), key=lambda x: x[1], reverse=True)[:n]
        
    def generate_insights(self) -> Dict[str, Any]:
        """Generate insights from conversation analysis"""
        return {
            "common_topics": self.get_common_topics(),
            "common_patterns": self.get_common_patterns(),
            "total_conversations": len(os.listdir(self.conversation_storage_path)),
            "total_messages": sum(len(json.load(open(os.path.join(self.conversation_storage_path, f)))["conversation"]) 
                                for f in os.listdir(self.conversation_storage_path) if f.endswith('.json'))
        } 