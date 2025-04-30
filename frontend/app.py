import os
import sys

# Add the parent directory to sys.path to be able to import modules from the root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from requirement_analyzer_agent import RequirementAnalyzerAgent

app = Flask(__name__)
app.static_folder = 'static'

# Initialize the Requirement Analyzer Agent
agent = RequirementAnalyzerAgent()

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chat functionality"""
    user_input = request.json.get('message', '')
    
    if not user_input.strip():
        return jsonify({'response': 'Please enter a message.'})
    
    # Get response from the agent
    try:
        response = agent.run_conversation(user_input)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Run the Flask application
    print("🚀 Starting Taiga AI Agent Chatbot...")
    print("📊 Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True)