# app.py
import os
import warnings
from services.chat_service import ChatService

# Suppress warnings
warnings.filterwarnings("ignore")

def main():
    """Main function to run the mental health assistant"""
    print("Initializing mental health assistant...")
    
    # Initialize the chat service
    try:
        assistant = ChatService()
        print("System ready. Type 'quit' to exit.\n")
        
        # Welcome message
        welcome_message = "I'm here to listen and support you. Feel free to share what's on your mind or how you're feeling today."
        print(f"Assistant: {welcome_message}")
        
        # Main conversation loop
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("Assistant: Take care. Remember I'm here whenever you need to talk.")
                    break
                    
                if not user_input:
                    continue
                    
                # Generate and display response
                response = assistant.generate_response(user_input)
                print(f"Assistant: {response}")
                
            except KeyboardInterrupt:
                print("\nSession ended. Take care.")
                break
            except Exception as e:
                print(f"Error occurred: {e}")
                print("Assistant: I apologize for the technical issue. Let's continue our conversation.")
    
    except Exception as e:
        print(f"Failed to initialize the assistant: {e}")
        print("Please check your installation and try again.")

if __name__ == "__main__":
    main()