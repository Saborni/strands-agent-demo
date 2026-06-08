from strands import Agent

from bedrock_agentcore import BedrockAgentCoreApp

from strands.models import BedrockModel
from strands_tools import http_request
from strands import tool
import logging
import requests

# Define a weather-focused system prompt
# WEATHER_SYSTEM_PROMPT = """You are a weather assistant with HTTP capabilities. You can:

# 1. Make HTTP requests to the National Weather Service API
# 2. Process and display weather forecast data
# 3. Provide weather information for locations in the United States

# When retrieving weather information:
# 1. First get the coordinates or grid information using https://api.weather.gov/points/{latitude},{longitude} or https://api.weather.gov/points/{zipcode}
# 2. Then use the returned forecast URL to get the actual forecast

# When displaying responses:
# - Format weather data in a human-readable way
# - Highlight important information like temperature, precipitation, and alerts
# - Handle errors appropriately
# - Convert technical terms to user-friendly language

# Always explain the weather conditions clearly and provide context for the forecast.
# """

MULTI_SYSTEM_PROMPT = """You are a helpful assistant with multiple capabilities:

**Weather Information:**
- Make HTTP requests to the National Weather Service API
- Provide weather forecasts for locations in the United States
- When retrieving weather: First get coordinates using https://api.weather.gov/points/{latitude},{longitude}
- Then use the returned forecast URL to get the actual forecast
- Format weather data in a human-readable way with temperature, precipitation, and alerts

**Metal Commodity Rates:**
- Fetch current prices for gold and silver using https://api.gold-api.com/price/{symbol}/{?currency}
- Provide up-to-date market rates in USD
- Explain price trends when relevant

**General Guidelines:**
- Handle errors appropriately
- Convert technical terms to user-friendly language
- Provide clear, concise responses with relevant context
- If asked about both weather and metal rates, handle both requests
"""

app = BedrockAgentCoreApp(debug=True)

agent_model = BedrockModel(model_id="minimax.minimax-m2.5", region_name="eu-west-1")

logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

@tool
def get_metal_rates(metal: str) -> dict:
    """
    Fetch current rates for gold or silver.
    Args:
        metal: The metal to fetch rates for. Must be either gold or silver.
    Returns:
        Dictionary containing the metal rates and currency information.
    """
    metal = metal.lower()
    if metal == "gold":
        symbol = "XAU"
    elif metal == "silver":
        symbol = "XAG"
    else:
        return {"error": "Invalid metal. Please specify 'gold' or 'silver'."}
    api_url = f"https://api.gold-api.com/price/{symbol}/USD"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Fetched {metal} rates: {data}")
        return data
    except Exception as e:
        return {"error": f"Failed to fetch {metal} rates: {str(e)}"}


# Create an agent with HTTP capabilities
weather_agent = Agent(
    model=agent_model,
    system_prompt=MULTI_SYSTEM_PROMPT,
    tools=[http_request, get_metal_rates],
)

# The main entry point for your AgentCore application.
@app.entrypoint 
def invoke(payload): 
     """Your AI agent function""" 
     user_input = payload.get("prompt", "Hello! How can I help you today?") 
     logger.info("\n User input: %s", user_input) 
     response = weather_agent(user_input) 
     logger.info("\n Agent result: %s ", response.message) 
    # Find the text content block (skip reasoning)
     for block in response.message['content']:
        if 'text' in block:
            return block['text']
    # Fallback if no text block found
     return str(response)

if __name__ == "__main__": 
     app.run() 
