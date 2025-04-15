# app.py - Updated version
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from utils.safety_checker import SafetyChecker
from services.chat_service import ChatService
from utils.index_builder import build_mental_health_index
from services.chat_service import ChatService

chat = ChatService()
print(chat.generate_response("I've been feeling depressed"))

def main():
    # First, build the index if needed
    data_dir = "data/mental_health_resources"
    if not os.path.exists("vector_store"):
        print("Building knowledge index...")
        build_mental_health_index(data_dir)
    
    # Initialize chat service
    print("Initializing chat service...")
    chat_service = ChatService()
    
    # Chat loop
    print("Mental Health Assistant (Type 'quit' to exit)")
    conversation_history = []
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']:
            break
            
        # Generate response
        response = chat_service.generate_response(user_input)
        print(f"Assistant: {response}")
        
        # Store conversation for context
        conversation_history.append({"user": user_input, "assistant": response})
        # Keep only the last 5 turns to avoid context getting too long
        if len(conversation_history) > 5:
            conversation_history = conversation_history[-5:]

if __name__ == "__main__":
    main()