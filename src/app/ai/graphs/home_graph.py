# src\app\ai\graphs\home_graph.py
from langgraph.graph import StateGraph, END
from app.lib import logger
from app.types.graph_state import CustomState
from app.ai.nodes import  onboarding_node, company_node, product_node


def build_home_workflow() -> StateGraph:
    wf = StateGraph(CustomState)

    # Nodes
    wf.add_node("onboarding", onboarding_node)
    wf.add_node("company_agent", company_node)
    wf.add_node("product_agent", product_node)

    # Inline routing function
    def _route(state: CustomState) -> str:
        stage = str(state["stage"])
        logger.debug("route_by_stage stage=%s", stage)

        if stage == "company_ready":
            return "company_agent"
        if stage == "product_ready":
            return "product_agent"
        return "onboarding"

    # Entry point based on stage
    wf.set_conditional_entry_point(_route)

    # Transitions from onboarding based on stage changes
    wf.add_conditional_edges(
        "onboarding",
        _route,
        {
            "company_agent": "company_agent",
            "product_agent": "product_agent",
            "onboarding": END, 
        },
    )

    # End edges
    wf.add_edge("company_agent", END)
    wf.add_edge("product_agent", END)

    return wf
