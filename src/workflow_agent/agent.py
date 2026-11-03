# For building AI agents
from google.adk import Agent
# For chaining agents into a pipeline
from google.adk import Workflow
# For managing messages
from google.adk import Event
# Pydantic's base class, used to define structured data schemas and validate data types in Python
from pydantic import BaseModel

# This agent generates a city name
city_generator_agent = Agent(
    name="city_generator_agent",
    model="gemini-flash-latest",
    instruction="""Return the name of a random city.
      Return only the name, nothing else.""",
)


# Defines a structured data model using Pydantic
# Any data conforming to this schema must contain two string fields: time_info and city
class CityTime(BaseModel):
    time_info: str  # time information
    city: str       # city name


# Time Lookup Helper Function
def lookup_time_function(node_input: str):
    """Simulate returning the current time in the specified city."""
    return CityTime(time_info="10:10 AM", city=node_input)


# AI agent responsible for generating the final report string
city_report_agent = Agent(
    name="city_report_agent",
    model="gemini-flash-latest",
    input_schema=CityTime,
    instruction="""Output following line:
    It is {CityTime.time_info} in {CityTime.city} right now.""",
)


# Helper function that receives the text output from the city_report_agent
# Wraps the text inside an Event object and appends "\n WORKFLOW COMPLETED."
# to signify that the pipeline has successfully finished execution
def completed_message_function(node_input: str):
    return Event(
        message=f"{node_input}\n WORKFLOW COMPLETED.",
    )


# edges: Defines the execution pipeline sequence
# 1. "START": Triggers the workflow
# 2. city_generator_agent: Generates a random city name
# 3. lookup_time_function: Takes that city name and creates a CityTime object with a simulated time
# 4. city_report_agent: Takes the structured object and formats it into a report sentence
# 5. completed_message_function: Wraps the final report in an Event object with a completion banner.
root_agent = Workflow(
    name="root_agent",
    edges=[
        ("START", city_generator_agent, lookup_time_function,
         city_report_agent, completed_message_function)
    ],
)
