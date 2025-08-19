# src\app\ai\nodes\onboarding_node.py
from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_openai import ChatOpenAI
from app.types.graph_state import CustomState
from app.agents.onboarding_agent import build_onboarding_agent

# Build once; bind OpenAI model here if you want
ONBOARDING_AGENT = build_onboarding_agent(
    model=ChatOpenAI(model="gpt-4o"),
    checkpointer=None,  # let the graph-level Sqlite saver handle state
)

def onboarding_node(state: CustomState) -> Dict[str, Any]:
    msgs: List[BaseMessage] = state.get("messages", [])
    payload = {"messages": [msgs[-1]]} if msgs else {"messages": [HumanMessage(content="Start onboarding")]}
    config = {"configurable": {"thread_id": state.get("thread_id", "onboarding")}}

    result = ONBOARDING_AGENT.invoke(payload, config=config)
    new_msgs = result["messages"]
    delta = new_msgs[len(msgs):] if len(new_msgs) >= len(msgs) else new_msgs

    return {"messages": msgs + delta, "stage": "onboarding"}
