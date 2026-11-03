import asyncio

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.genai import types  # For creating message Content/Parts


# Mock tool implementation
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}


root_agent = Agent(
    model="gemini-flash-latest",
    name="current_time_agent",
    description="Tells the current time in a specified city.",
    instruction="""You are a helpful assistant that tells the current time in cities.
    Use the 'get_current_time' tool for this purpose.""",
    tools=[get_current_time],
)


session_service = InMemorySessionService()

# Define constants for identifying the interaction context
APP_NAME = "current_time_app"
USER_ID = "user_001"
SESSION_ID = "session_001"


async def init_session(app_name: str, user_id: str, session_id: str) -> Session:
    session = await session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )
    return session


session = asyncio.run(init_session(APP_NAME, USER_ID, SESSION_ID))

runner = Runner(
    agent=root_agent,  # The agent we want to run
    app_name=APP_NAME,  # Associates runs with our app
    session_service=session_service,  # Uses our session manager
)
print(f"Runner created for agent '{runner.agent.name}'.")


async def call_agent_async(query: str, runner, user_id, session_id):
    """Sends a query to the agent and prints the final response."""

    # Prepare the user's message in ADK format
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = "Agent did not produce a final response."  # Default

    # Key Concept: run_async executes the agent logic and yields Events.
    # We iterate through events to find the final answer.
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        # is_final_response() marks the concluding message for the turn.
        if event.is_final_response():
            if event.content and event.content.parts:
                # Assuming text response in the first part
                final_response_text = event.content.parts[0].text
            elif (
                event.actions and event.actions.escalate
            ):  # Handle potential errors/escalations
                final_response_text = (
                    f"Agent escalated: {event.error_message or 'No specific message.'}"
                )

    # Return the value instead of just printing it
    return final_response_text


# We need an async function to await our interaction helper
async def run_conversation():
    response = await call_agent_async(
        "What is the time in London?",
        runner=runner,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    print(f"Agent Response: {response}")


if __name__ == "__main__":
    try:
        asyncio.run(run_conversation())
    except asyncio.CancelledError:
        print("The agent task was cancelled externally (timeout or abort).")
    except Exception as e:
        print(f"An error occurred: {e}")
