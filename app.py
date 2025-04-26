# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import warnings
from services.chat_service import ChatService

# Suppress warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
# Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "*"}})
chat_service = ChatService()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Check if request has JSON content
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400

        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
            
        if 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Message field is required'
            }), 400
            
        user_input = data['message']
        
        # Validate message content
        if not isinstance(user_input, str) or not user_input.strip():
            return jsonify({
                'success': False,
                'error': 'Message must be a non-empty string'
            }), 400
            
        # Generate response
        response = chat_service.generate_response(user_input)
        
        return jsonify({
            'success': True,
            'data': {
                'response': response
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for the API"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'message': 'API is running'
    })

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
    # Run the Flask app in debug mode
    app.run(debug=True, port=8000, host='0.0.0.0')