from google.adk.agents import Agent
from google.adk.tools import google_search


# Define the single search-enabled agent
root_agent = Agent(
    name="search_assistant",
    model="gemini-flash-latest",
    description="A helpful assistant that can search the live web using Google Search.",
    instruction=(
        "You are a knowledgeable assistant with access to Google Search. "
        "When asked about current events, facts, or data requiring up-to-date information, "
        "use the Google Search tool to find accurate and grounded answers."
    ),
    tools=[google_search],
)
