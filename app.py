from services.chat_service import ChatService

def main():
    print("Initializing Mental Health Assistant...")
    chat_service = ChatService()
    
    print("System Ready. Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['quit', 'exit']:
            break
            
        response = chat_service.generate_response(user_input)
        print(f"Assistant: {response}")

if __name__ == "__main__":
    main()