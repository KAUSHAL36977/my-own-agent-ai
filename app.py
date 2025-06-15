from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from agent import Agent
from tools import TimeTool, WeatherTool, CalculatorTool
import os
from dotenv import load_dotenv
from datetime import datetime
import json
from collections import defaultdict

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize agent
agent = Agent()
agent.add_tool(TimeTool())
agent.add_tool(WeatherTool())
agent.add_tool(CalculatorTool())

# Analytics storage
analytics = {
    'total_messages': 0,
    'tool_usage': defaultdict(int),
    'conversation_history': [],
    'active_users': set(),
    'response_times': []
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/analytics')
def get_analytics():
    return jsonify({
        'total_messages': analytics['total_messages'],
        'tool_usage': dict(analytics['tool_usage']),
        'active_users': len(analytics['active_users']),
        'average_response_time': sum(analytics['response_times']) / len(analytics['response_times']) if analytics['response_times'] else 0,
        'recent_conversations': analytics['conversation_history'][-10:]  # Last 10 conversations
    })

@socketio.on('send_message')
def handle_message(data):
    user_message = data.get('message', '')
    user_id = request.sid
    
    if not user_message:
        return
    
    # Update analytics
    analytics['total_messages'] += 1
    analytics['active_users'].add(user_id)
    start_time = datetime.now()
    
    # Process the message using our agent
    response = agent.process_input(user_message)
    
    # Calculate response time
    response_time = (datetime.now() - start_time).total_seconds()
    analytics['response_times'].append(response_time)
    
    # Track tool usage
    tool = agent._should_use_tool(user_message)
    if tool:
        analytics['tool_usage'][tool.name()] += 1
    
    # Store conversation
    conversation = {
        'timestamp': datetime.now().isoformat(),
        'user_message': user_message,
        'assistant_response': response,
        'tool_used': tool.name() if tool else None,
        'response_time': response_time
    }
    analytics['conversation_history'].append(conversation)
    
    # Emit the response back to the client
    emit('receive_message', {
        'message': response,
        'type': 'assistant',
        'tool_used': tool.name() if tool else None,
        'response_time': response_time
    })
    
    # Broadcast analytics update to dashboard
    emit('analytics_update', {
        'total_messages': analytics['total_messages'],
        'tool_usage': dict(analytics['tool_usage']),
        'active_users': len(analytics['active_users']),
        'average_response_time': sum(analytics['response_times']) / len(analytics['response_times']) if analytics['response_times'] else 0
    }, broadcast=True)

@socketio.on('connect')
def handle_connect():
    user_id = request.sid
    analytics['active_users'].add(user_id)
    
    # Send welcome message
    emit('receive_message', {
        'message': "Hello! I'm your AI assistant. How can I help you today?",
        'type': 'assistant'
    })
    
    # Broadcast user count update
    emit('analytics_update', {
        'active_users': len(analytics['active_users'])
    }, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    user_id = request.sid
    analytics['active_users'].discard(user_id)
    
    # Broadcast user count update
    emit('analytics_update', {
        'active_users': len(analytics['active_users'])
    }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True) 