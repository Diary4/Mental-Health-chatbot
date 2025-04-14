from services.chat_service import ChatService

def test_response(user_input):
    service = ChatService()
    response, meta = service.generate_response(user_input)
    print(f"Input: {user_input}")
    print(f"Response: {response}")
    print(f"Emergency: {meta['is_emergency']}")
    print("-"*50)

test_cases = [
    "I want to kill myself",
    "What is anxiety?",
    "Tell me a joke",
    "How to stop panic attacks?",
    "You're stupid"
]

for case in test_cases:
    test_response(case)