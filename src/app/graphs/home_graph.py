# src\app\graphs\home_graph.py
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage
from app.graphs.state import CustomState
from app.lib.logger import logger
from app.graphs.nodes.home_nodes import onboarding_node, company_node, product_node

def route_by_stage(state: CustomState) -> str:
    stage = state.get("stage", "")
    logger.info(f"Routing by stage: {stage}")
    if "company" in stage:
        return "company_agent"
    elif "product" in stage:
        return "product_agent"
    return "onboarding"

def route_by_message(state: CustomState) -> str:
    try:
        if not state.get("messages"):
            logger.info("No messages, routing to onboarding")
            return "onboarding"

        last_msg = state["messages"][-1]

        if isinstance(last_msg, BaseMessage):
            content = last_msg.content
        elif hasattr(last_msg, "content"):
            content = last_msg.content
        elif isinstance(last_msg, dict):
            content = last_msg.get("content", "")
        else:
            content = str(last_msg)

        content = content.lower().strip()
        logger.info(f"Message content: '{content}'")

        if "company" in content:
            return "company_agent"
        elif "product" in content:
            return "product_agent"

        return "onboarding"

    except Exception as e:
        logger.error(f"Error in route_by_message: {e}", exc_info=True)
        return "onboarding"

def build_home_workflow() -> StateGraph:
    wf = StateGraph(CustomState)

    wf.add_node("onboarding", onboarding_node)
    wf.add_node("company_agent", company_node)
    wf.add_node("product_agent", product_node)

    wf.set_conditional_entry_point(route_by_stage)

    wf.add_conditional_edges("onboarding", route_by_message, {
        "company_agent": "company_agent",
        "product_agent": "product_agent",
        "onboarding": "onboarding",  # stay in onboarding until switch
    })

    wf.add_edge("company_agent", END)
    wf.add_edge("product_agent", END)

    return wf
