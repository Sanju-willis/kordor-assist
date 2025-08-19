# src\app\ai\nodes\product_node.py
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from app.types.graph_state import CustomState
from app.ai.tools.product_tools import (
    analyze_product_features,
    get_user_feedback,
    track_product_metrics,
    generate_roadmap,
)


def create_product_agent():
    """Create specialized product management agent."""

    checkpointer = InMemorySaver()

    agent = create_react_agent(
        model="anthropic:claude-3-5-sonnet-latest",
        tools=[
            analyze_product_features,
            get_user_feedback,
            track_product_metrics,
            generate_roadmap,
        ],
        prompt="""You are a product management specialist.
        
        Your expertise includes:
        - Feature analysis and prioritization
        - User feedback interpretation  
        - Product metrics tracking
        - Roadmap planning
        
        Focus on user value and business impact in your recommendations.""",
        checkpointer=checkpointer,
    )

    return agent


def product_node(state: CustomState) -> Dict[str, Any]:
    """Execute product agent with PM tools."""

    agent = create_product_agent()

    config = {"configurable": {"thread_id": "product_session"}}

    if state["messages"]:
        messages = state["messages"]
    else:
        messages = [HumanMessage(content="Product agent activated")]

    response = agent.invoke({"messages": messages}, config=config)

    return {"messages": response["messages"], "stage": "product_active"}
