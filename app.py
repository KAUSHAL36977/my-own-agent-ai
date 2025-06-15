from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from agent import AIAgent
import os
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize analytics data
analytics = {
    'total_messages': 0,
    'active_users': 0,
    'average_response_time': 0,
    'tool_usage': {},
    'recent_conversations': []
}

# Initialize AI Agent
agent = AIAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/analytics')
def get_analytics():
    return jsonify(analytics)

@socketio.on('connect')
def handle_connect():
    analytics['active_users'] += 1
    socketio.emit('analytics_update', analytics)

@socketio.on('disconnect')
def handle_disconnect():
    analytics['active_users'] = max(0, analytics['active_users'] - 1)
    socketio.emit('analytics_update', analytics)

@socketio.on('message')
def handle_message(data):
    start_time = datetime.now()
    
    # Get user message
    user_message = data.get('message', '')
    
    # Process message with AI agent
    response = agent.process_message(user_message)
    
    # Calculate response time
    end_time = datetime.now()
    response_time = (end_time - start_time).total_seconds()
    
    # Update analytics
    analytics['total_messages'] += 1
    analytics['average_response_time'] = (
        (analytics['average_response_time'] * (analytics['total_messages'] - 1) + response_time)
        / analytics['total_messages']
    )
    
    # Update tool usage
    tool_used = response.get('tool_used', 'None')
    analytics['tool_usage'][tool_used] = analytics['tool_usage'].get(tool_used, 0) + 1
    
    # Add to recent conversations
    conversation = {
        'timestamp': datetime.now().isoformat(),
        'user_message': user_message,
        'assistant_response': response.get('response', ''),
        'tool_used': tool_used,
        'response_time': response_time
    }
    analytics['recent_conversations'].insert(0, conversation)
    analytics['recent_conversations'] = analytics['recent_conversations'][:10]  # Keep only last 10
    
    # Emit response and analytics update
    socketio.emit('response', response)
    socketio.emit('analytics_update', analytics)

if __name__ == '__main__':
    # For local development
    socketio.run(app, debug=True)
else:
    # For Vercel deployment
    app = app 