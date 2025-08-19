# src\app\ai\nodes\company_node.py
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from app.types.graph_state import CustomState
from app.ai.tools.company_tools import (
    search_company_data,
    get_company_metrics,
    analyze_competitors,
)


def create_company_agent():
    """Create specialized company analysis agent."""

    checkpointer = InMemorySaver()

    agent = create_react_agent(
        model="anthropic:claude-3-5-sonnet-latest",
        tools=[search_company_data, get_company_metrics, analyze_competitors],
        prompt="""You are a company analysis expert.
        
        Your capabilities:
        - Research company information
        - Analyze business metrics  
        - Compare with competitors
        - Provide strategic insights
        
        Always provide data-driven responses with clear analysis.""",
        checkpointer=checkpointer,
    )

    return agent


def company_node(state: CustomState) -> Dict[str, Any]:
    """Execute company agent with business analysis tools."""

    agent = create_company_agent()

    config = {"configurable": {"thread_id": "company_session"}}

    # Process user query
    if state["messages"]:
        messages = state["messages"]
    else:
        messages = [HumanMessage(content="Company agent activated")]

    response = agent.invoke({"messages": messages}, config=config)

    return {"messages": response["messages"], "stage": "company_active"}
