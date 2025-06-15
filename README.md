# Claude-Like AI Agent Simulator (No API)

This project is an educational guide demonstrating how to build a Claude-like AI agent from scratch **without using the Claude API**. The agent simulates core features such as conversational ability, tool integration, and user experience, using open-source LLMs or mock logic.

## Features

- **Conversational AI:** Mimics Claude's chat-based interface and reasoning.
- **Tool Integration:** Supports adding custom tools (e.g., time lookup, weather, file operations).
- **Memory:** Maintains context and conversation history.
- **Prompt Engineering:** Structured prompts for tool use and direct responses.
- **No Claude API:** Uses local LLMs, open-source models, or mock logic for simulation.

## Prerequisites

- **Python 3.7+**
- **Basic knowledge of Python programming**
- **Optional:** Access to an open-source LLM (e.g., Llama 2, GPT-2, or a local LLM service)
- **Optional:** API keys for external services (e.g., OpenWeatherMap for weather tool)

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/claude-agent-simulator.git
cd claude-agent-simulator
```

2. **Install dependencies:**
   *(Note: A `requirements.txt` file will be provided in a future update. For now, manually install any necessary libraries like `requests` if you implement tools requiring them.)*
*(Optional: If using a local LLM, install its dependencies as well.)*

## Usage

1. **Define Tools**

Create custom tools by implementing the `Tool` abstract base class. Example:
```python
from abc import ABC, abstractmethod

class Tool(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def use(self, *args, **kwargs):
        pass
```

2. **Implement Tools**

Example: Time and Weather tools.
```python
import datetime
import requests

class TimeTool(Tool):
    def name(self):
        return "Time Tool"

    def description(self):
        return "Provides the current time."

    def use(self, *args, **kwargs):
        return f"The current time is {datetime.datetime.now()}."
```

3. **Build the Agent**

Create an `Agent` class that manages conversation, tool use, and memory:
```python
class Agent:
    def __init__(self):
        self.tools = []
        self.memory = []

    def add_tool(self, tool):
        self.tools.append(tool)

    def process_input(self, user_input):
        # Logic to decide tool use or direct response
        # Example: Use mock LLM logic or open-source LLM call
        pass
```

4. **Run the Agent**
```python
agent = Agent()
agent.add_tool(TimeTool())
# To run the agent, you would typically implement a loop
# that takes user input and calls agent.process_input(input).
# For example:
# while True:
#     user_query = input("You: ")
#     if user_query.lower() == "exit":
#         break
#     response = agent.process_input(user_query)
#     print(f"Agent: {response}")
```

## Example Workflow

- **User Input:** "What time is it?"
- **Agent:** Uses the TimeTool and returns the current time.
- **User Input:** "How are you?"
- **Agent:** Responds directly without tool use.

## Customization

- **Add New Tools:** Implement new `Tool` classes and add them to the agent.
- **Prompt Engineering:** Customize prompts for better tool selection and reasoning.
- **Memory Management:** Expand memory handling for longer conversations.

## Limitations

- **No Claude API:** This agent does not use the real Claude API but simulates its behavior.
- **LLM Dependency:** For advanced reasoning, you may need to use a local or open-source LLM.

## Contributing

Feel free to contribute by adding new tools, improving memory, or integrating with open-source LLMs!

---

> **Note:** This project is for educational purposes to understand the mechanics of an AI agent like Claude, focusing on its architecture rather than direct API usage.
