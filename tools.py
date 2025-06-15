from abc import ABC, abstractmethod
import datetime
import requests
import os
from typing import Any, Dict, List, Optional

class Tool(ABC):
    """Base class for all tools that can be used by the agent."""
    
    @abstractmethod
    def name(self) -> str:
        """Return the name of the tool."""
        pass
    
    @abstractmethod
    def description(self) -> str:
        """Return a description of what the tool does."""
        pass
    
    @abstractmethod
    def use(self, *args: Any, **kwargs: Any) -> str:
        """Execute the tool's functionality."""
        pass

class TimeTool(Tool):
    """Tool for getting the current time."""
    
    def name(self) -> str:
        return "Time Tool"
    
    def description(self) -> str:
        return "Provides the current time in various formats."
    
    def use(self, *args: Any, **kwargs: Any) -> str:
        current_time = datetime.datetime.now()
        return f"The current time is {current_time.strftime('%Y-%m-%d %H:%M:%S')}"

class WeatherTool(Tool):
    """Tool for getting weather information."""
    
    def name(self) -> str:
        return "Weather Tool"
    
    def description(self) -> str:
        return "Provides weather information for a given location."
    
    def use(self, location: str, *args: Any, **kwargs: Any) -> str:
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not api_key:
            return "Error: OpenWeatherMap API key not found. Please set OPENWEATHERMAP_API_KEY environment variable."
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                temp = data["main"]["temp"]
                description = data["weather"][0]["description"]
                return f"Weather in {location}: {description}, Temperature: {temp}°C"
            else:
                return f"Error getting weather for {location}: {data.get('message', 'Unknown error')}"
        except Exception as e:
            return f"Error getting weather information: {str(e)}"

class CalculatorTool(Tool):
    """Tool for performing basic calculations."""
    
    def name(self) -> str:
        return "Calculator Tool"
    
    def description(self) -> str:
        return "Performs basic arithmetic calculations."
    
    def use(self, expression: str, *args: Any, **kwargs: Any) -> str:
        try:
            # Safely evaluate the expression
            result = eval(expression, {"__builtins__": {}}, {"abs": abs, "round": round})
            return f"Result of {expression} = {result}"
        except Exception as e:
            return f"Error calculating expression: {str(e)}" 