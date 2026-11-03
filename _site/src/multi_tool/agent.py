from google.adk.agents.llm_agent import Agent


# Mock tool implementation
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}


# Mock tool implementation
def get_current_weather(city: str) -> dict:
    """Returns the current weather in a specified city."""
    return {"status": "success", "city": city, "weather": "Sunny with a temperature of 77 degrees Fahrenheit"}


root_agent = Agent(
    model='gemini-flash-latest',
    name='root_agent',
    description="Tells the current time or weather in a specified city.",
    instruction="""You are a helpful assistant that tells the current time or weather in cities.
    Use the 'get_current_time' or 'get_current_weather' tools for these purposes.""",
    tools=[get_current_time, get_current_weather],
)

