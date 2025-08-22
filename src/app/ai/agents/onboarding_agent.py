# src\app\ai\agents\onboarding_agent.py
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from pydantic import SecretStr
from app.config.settings import settings

@tool
def get_user_name(name: str) -> str:
    """Save the user's name and confirm."""
    return f"Got it — your name is {name}."

@tool
def get_user_role(role: str) -> str:
    """Save the user's role and confirm."""
    return f"Okay, your role is {role}."

TOOLS = [get_user_name, get_user_role]

# --------------------------------------------------------------------
# System prompt
# --------------------------------------------------------------------

ONBOARDING_PROMPT = """You are an onboarding specialist.
Ask the user for their name and role.
When the user provides each, call the appropriate tool with that info.
After both are collected, say: "Perfect! Let's set up your company profile next."
"""

# --------------------------------------------------------------------
# Build the agent (a Runnable)
# --------------------------------------------------------------------

def get_onboarding_agent():
    llm = ChatOpenAI(
        model="gpt-4o",
        api_key=SecretStr(settings.OPENAI_API_KEY),  # ✅ now using your config
    )
    return create_react_agent(
        model=llm,
        tools=TOOLS,
        prompt=ONBOARDING_PROMPT,
        checkpointer=None,  # graph handles memory
    )
