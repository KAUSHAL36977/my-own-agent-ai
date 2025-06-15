# Claude-Like AI Agent (No API)

This project demonstrates how to build a Claude-like AI agent from scratch **without using the Claude API**. The agent simulates core features such as conversational ability, tool integration, and user experience, using open-source LLMs or mock logic.

## Features

- **Conversational AI:** Mimics Claude's chat-based interface and reasoning
- **Tool Integration:** Supports adding custom tools (e.g., time lookup, weather, calculations)
- **Memory:** Maintains context and conversation history
- **Prompt Engineering:** Structured prompts for tool use and direct responses
- **No Claude API:** Uses local LLMs (GPT-2 by default) or mock logic for simulation

## Prerequisites

- Python 3.7+
- Basic knowledge of Python programming
- Optional: Access to an open-source LLM (e.g., GPT-2, Llama 2)
- Optional: API keys for external services (e.g., OpenWeatherMap for weather tool)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/claude-agent-simulator.git
cd claude-agent-simulator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Create a `.env` file for API keys:
```
OPENWEATHERMAP_API_KEY=your_api_key_here
```

## Usage

Run the agent:
```bash
python main.py
```

The agent supports the following tools:
- Time Tool: Get the current time
- Weather Tool: Get weather information for a location
- Calculator Tool: Perform basic calculations

Example interactions:
```
You: What time is it?
Assistant: The current time is 2024-02-20 15:30:45

You: What's the weather in London?
Assistant: Weather in London: cloudy, Temperature: 12°C

You: Calculate 2 + 2
Assistant: Result of 2 + 2 = 4
```

## Customization

### Adding New Tools

Create a new tool by implementing the `Tool` abstract base class:

```python
from tools import Tool

class MyCustomTool(Tool):
    def name(self) -> str:
        return "My Custom Tool"
    
    def description(self) -> str:
        return "Description of what my tool does"
    
    def use(self, *args, **kwargs) -> str:
        # Implement tool functionality
        return "Tool result"
```

### Using Different LLMs

The agent uses GPT-2 by default, but you can use other models from Hugging Face:

```python
agent = Agent(model_name="gpt2-medium")  # or any other model
```

## Limitations

- The agent uses a simple rule-based system when no LLM is available
- Weather tool requires an OpenWeatherMap API key
- Basic tool selection based on keyword matching
- Limited conversation context (last 5 messages)

## Contributing

Feel free to contribute by:
1. Adding new tools
2. Improving the LLM integration
3. Enhancing the conversation memory
4. Adding more sophisticated tool selection logic

## License

MIT License 