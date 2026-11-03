from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

root_agent = Agent(
    model=LiteLlm(
        model="openai/gpt-4o",
        num_retries=2,
        # Backup chain executed in order
        fallbacks=["anthropic/claude-3-5-sonnet-20241022", "ollama/llama3.3"],
    ),
    name="time_agent",
    instruction="You are a helpful assistant.",
    tools=[],
)
