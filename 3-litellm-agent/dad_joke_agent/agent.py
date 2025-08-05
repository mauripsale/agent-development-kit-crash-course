import os
import random

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# As shown in the README, you can use various models through LiteLlm and OpenRouter.
# Let's use a modern and capable model like Claude 3.5 Sonnet.
# The previous model "openrouter/openai/gpt-4.1" is not a valid OpenRouter model identifier.
model = LiteLlm(
    #model="openrouter/mistralai/devstral-small-2505:free",
    model="openrouter/qwen/qwen3-235b-a22b:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def get_dad_joke() -> dict:
    """
    Selects a random dad joke from a predefined list.

    Returns:
        A dictionary containing the joke.
    """
    jokes = [
        "Why did the chicken cross the road? To get to the other side!",
        "What do you call a belt made of watches? A waist of time.",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
    ]
    return {"joke": random.choice(jokes)}


root_agent = Agent(
    name="dad_joke_agent",
    model=model,
    description="Dad joke agent",
    instruction="""
    You are a helpful assistant that tells dad jokes.
    1. Use the `get_dad_joke` tool to get a joke.
    2. Present the joke from the tool's output to the user.
    """,
    tools=[get_dad_joke],
)
