from typing import List, Dict, Any, Optional
from tools import Tool
import json
from transformers import pipeline
import torch

class Agent:
    """Main agent class that manages conversation and tool usage."""
    
    def __init__(self, model_name: str = "gpt2"):
        """Initialize the agent with tools and conversation memory."""
        self.tools: List[Tool] = []
        self.conversation_history: List[Dict[str, str]] = []
        self.model_name = model_name
        
        # Initialize the language model
        try:
            self.model = pipeline("text-generation", model=model_name)
        except Exception as e:
            print(f"Warning: Could not load {model_name}. Using mock responses.")
            self.model = None
    
    def add_tool(self, tool: Tool) -> None:
        """Add a new tool to the agent's toolkit."""
        self.tools.append(tool)
    
    def _generate_response(self, user_input: str) -> str:
        """Generate a response using the language model or fallback to mock responses."""
        if self.model:
            try:
                # Create a prompt that includes conversation history and available tools
                prompt = self._create_prompt(user_input)
                response = self.model(prompt, max_length=100, num_return_sequences=1)[0]["generated_text"]
                return response.split(prompt)[-1].strip()
            except Exception as e:
                print(f"Error generating response: {str(e)}")
                return self._mock_response(user_input)
        else:
            return self._mock_response(user_input)
    
    def _create_prompt(self, user_input: str) -> str:
        """Create a prompt that includes conversation history and available tools."""
        prompt = "Conversation History:\n"
        for msg in self.conversation_history[-5:]:  # Include last 5 messages
            prompt += f"{msg['role']}: {msg['content']}\n"
        
        prompt += "\nAvailable Tools:\n"
        for tool in self.tools:
            prompt += f"- {tool.name()}: {tool.description()}\n"
        
        prompt += f"\nUser: {user_input}\nAssistant:"
        return prompt
    
    def _mock_response(self, user_input: str) -> str:
        """Generate a mock response when the language model is not available."""
        # Simple rule-based responses
        user_input = user_input.lower()
        if "hello" in user_input or "hi" in user_input:
            return "Hello! How can I help you today?"
        elif "how are you" in user_input:
            return "I'm doing well, thank you for asking! How can I assist you?"
        elif "bye" in user_input or "goodbye" in user_input:
            return "Goodbye! Have a great day!"
        else:
            return "I understand. How else can I help you?"
    
    def _should_use_tool(self, user_input: str) -> Optional[Tool]:
        """Determine if a tool should be used based on the user input."""
        user_input = user_input.lower()
        
        # Simple keyword matching for tool selection
        if "time" in user_input:
            return next((tool for tool in self.tools if tool.name() == "Time Tool"), None)
        elif "weather" in user_input:
            return next((tool for tool in self.tools if tool.name() == "Weather Tool"), None)
        elif any(op in user_input for op in ["+", "-", "*", "/", "calculate"]):
            return next((tool for tool in self.tools if tool.name() == "Calculator Tool"), None)
        
        return None
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate a response."""
        # Add user input to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Check if we should use a tool
        tool = self._should_use_tool(user_input)
        if tool:
            response = tool.use(user_input)
        else:
            response = self._generate_response(user_input)
        
        # Add response to conversation history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def run(self) -> None:
        """Run the agent in an interactive loop."""
        print("Agent started. Type 'quit' to exit.")
        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() == "quit":
                print("Goodbye!")
                break
            
            response = self.process_input(user_input)
            print(f"\nAssistant: {response}") 