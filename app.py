# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import warnings
from services.chat_service import ChatService

warnings.filterwarnings("ignore")

app = Flask(__name__)
# Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "*"}})
chat_service = ChatService()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
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

if __name__ == "__main__":
    # Run the Flask app in debug mode
    app.run(debug=True, port=8000, host='0.0.0.0')