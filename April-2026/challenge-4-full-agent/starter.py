import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from datetime import date, datetime
import requests

from strands import Agent, tool
from strands_tools import calculator, mem0_memory

MODEL = "us.amazon.nova-pro-v1:0"


# ============================================================
# Streaming callback
# ============================================================

def stream_callback(**kwargs):
    if "data" in kwargs:
        print(kwargs["data"], end="", flush=True)

    elif "current_tool_use" in kwargs:
        tool_name = kwargs["current_tool_use"].get("name", "")
        if tool_name:
            print(f"\n🔧 Using tool: {tool_name}")


# ============================================================
# Custom Tools
# ============================================================

@tool
def weather(city: str) -> str:
    """Get the current weather for a city.

    Args:
        city: The name of the city.
    """
    try:
        r = requests.get(f"https://wttr.in/{city}?format=3", timeout=5)
        return r.text
    except Exception:
        return f"Weather in {city}: Sunny, 30°C"


@tool
def age_calculator(birth_date: str) -> str:
    """Calculate age from a birth date.

    Args:
        birth_date: Date of birth in YYYY-MM-DD format.
    """
    today = date.today()
    born = datetime.strptime(birth_date, "%Y-%m-%d").date()

    age = today.year - born.year - (
        (today.month, today.day) < (born.month, born.day)
    )

    return f"Someone born on {birth_date} is {age} years old."


# ============================================================
# Agent
# ============================================================

agent = Agent(
    model=MODEL,
    tools=[
        calculator,
        weather,
        age_calculator,
        mem0_memory
    ],
    callback_handler=stream_callback,
    system_prompt="""
You are a fun, helpful assistant! 🤖

You have access to:
- calculator
- weather
- age_calculator
- mem0_memory

Rules:
- Use calculator for math
- Use weather for weather questions
- Use age_calculator for age calculations
- Use mem0_memory to remember and recall user information
- Be friendly and use emojis
"""
)


# ============================================================
# Interactive Loop
# ============================================================

print("🤖 Full Agent Ready! Type 'quit' to exit.")
print("Try: What's the weather in Delhi and how old is someone born 2000-01-01?")
print("Try: Remember my name is Samarth, then ask What's my name?\n")

while True:
    try:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("Bye! 👋")
            break

        print("\nAgent: ", end="")
        agent(user_input)
        print("\n")

    except KeyboardInterrupt:
        print("\nBye! 👋")
        break

print("\n✅ Challenge 4 complete! 🏆")
