import asyncio

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm  # For multi-model support
from google.adk.runners import Runner
from google.genai import types  # For creating message Content/Parts


# Mock tool implementation
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}


def say_hello(name: str) -> str:
    """Provides a simple greeting message"""
    return f"Hello, {name}!"


def say_goodbye(name: str) -> str:
    """Provides a simple farewell message."""
    return f"Goodbye {name}! Have a great day."


greeting_agent = Agent(
    # Using a potentially different/cheaper model for a simple task
    model="gemini-flash-latest",
    name="greeting_agent",
    instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
    "Use the 'say_hello' tool to generate the greeting. "
    "Make sure to pass the name the user provides to the tool. "
    "Do not engage in any other conversation or tasks.",
    description="Handles simple greetings and hellos using the 'say_hello' tool.",  # Crucial for delegation
    tools=[say_hello],
)

farewell_agent = Agent(
    # Can use the same or a different model
    model="gemini-flash-latest",
    name="farewell_agent",
    instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
    "Use the 'say_goodbye' tool to generate the farewell. "
    "Make sure to pass the name the user provides to the tool. "
    "Do not engage in any other conversation or tasks.",
    description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",  # Crucial for delegation
    tools=[say_goodbye],
)

root_agent = Agent(
    model="gemini-flash-latest",
    name="current_time_agent",
    description="Tells the current time in a specified city and delegates greetings/farewells to specialists.",
    instruction="""You are the main Current Time Agent coordinating a team.
    Your primary responsibility is to provide the current time.
    Use the 'get_current_time' tool ONLY for specific current time requests (e.g., 'current time in London').
    You have specialized sub-agents:
    1. 'greeting_agent': Handles simple greetings. Delegate to it for these.
    2. 'farewell_agent': Handles simple farewells. Delegate to it for these.
    Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'
    If it's a farewell, delegate to 'farewell_agent'
    If it's a current time request, handle it yourself using 'get_current_time'
    For anything else, respond appropriately or state you cannot handle it""",
    tools=[get_current_time],
    # Key change: Link the sub-agents here!
    sub_agents=[greeting_agent, farewell_agent],
)
