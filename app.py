# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import warnings
from services.chat_service import ChatService

warnings.filterwarnings("ignore")

app = Flask(__name__)
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
        
        if not isinstance(user_input, str) or not user_input.strip():
            return jsonify({
                'success': False,
                'error': 'Message must be a non-empty string'
            }), 400
            
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

@app.route('/api/insights', methods=['GET'])
def get_insights():
    """Get insights from conversation analysis"""
    try:
        insights = chat_service.get_learning_insights()
        return jsonify({
            'success': True,
            'data': insights
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/update_responses', methods=['POST'])
def update_responses():
    """Update responses for a specific topic"""
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400

        data = request.get_json()
        
        if not data or 'topic' not in data or 'responses' not in data:
            return jsonify({
                'success': False,
                'error': 'Topic and responses fields are required'
            }), 400
            
        topic = data['topic']
        responses = data['responses']
        
        if not isinstance(responses, list) or not all(isinstance(r, str) for r in responses):
            return jsonify({
                'success': False,
                'error': 'Responses must be a list of strings'
            }), 400
            
        chat_service.update_responses(topic, responses)
        
        return jsonify({
            'success': True,
            'message': f'Responses updated for topic: {topic}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000, host='0.0.0.0')