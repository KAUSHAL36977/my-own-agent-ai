from agent import Agent
from tools import TimeTool, WeatherTool, CalculatorTool
import os
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Create agent instance
    agent = Agent()
    
    # Add tools
    agent.add_tool(TimeTool())
    agent.add_tool(WeatherTool())
    agent.add_tool(CalculatorTool())
    
    # Print welcome message
    print("Welcome to the Claude-like AI Agent!")
    print("Available tools:")
    for tool in agent.tools:
        print(f"- {tool.name()}: {tool.description()}")
    print("\nYou can ask about the time, weather, or perform calculations.")
    print("Type 'quit' to exit.")
    
    # Run the agent
    agent.run()

if __name__ == "__main__":
    main() 