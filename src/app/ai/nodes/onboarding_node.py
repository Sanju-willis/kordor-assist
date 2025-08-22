# src\app\ai\nodes\onboarding_node.py
from typing import Dict, Any
from langchain_core.messages import AIMessage, BaseMessage
from app.types import CustomState
from app.ai.agents.onboarding_agent import get_onboarding_agent

ONBOARDING_AGENT = get_onboarding_agent()

def onboarding_node(state: CustomState) -> Dict[str, Any]:
    history: list[BaseMessage] = state.get("messages", [])

    try:
        # Invoke the agent directly from the node
        result = ONBOARDING_AGENT.invoke({"messages": history})
        return {
            "messages": result.get("messages", []),
            "stage": "onboarding"
        }
    except Exception:
        # Fallback if the agent call fails
        fallback = AIMessage(content="Let's start: what's your name?")
        return {"messages": [*history, fallback], "stage": "onboarding"}
