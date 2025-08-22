# src\app\ai\graphs\home_graph.py
from langgraph.graph import StateGraph, END
from app.types.graph_state import CustomState
from app.ai.nodes import onboarding_node, company_node, product_node


def _last_is_ai(state: CustomState) -> bool:
    msgs = state.get("messages") or []
    if not msgs:
        return False
    m = msgs[-1]
    t = getattr(m, "type", None)
    if t:  # LangChain message
        return t == "ai"
    return isinstance(m, dict) and m.get("role") == "assistant"  # dict-style


def route_by_stage(state: CustomState) -> str:
    if _last_is_ai(state):
        return "END"

    stage = str(state.get("stage"))
    stage_map = {
        "company_ready": "company_agent",
        "onboarding_company": "company_agent",
        "product_ready": "product_agent",
        "onboarding_products": "product_agent",
        "done": "END",
        "onboarding_completed": "END",
    }
    return stage_map.get(stage, "onboarding")


def build_home_workflow() -> StateGraph:
    wf = StateGraph(CustomState)

    def router(state: CustomState) -> CustomState:
        return state

    wf.add_node("router", router)
    wf.add_node("onboarding", onboarding_node)
    wf.add_node("company_agent", company_node)
    wf.add_node("product_agent", product_node)

    wf.set_entry_point("router")

    # Use the top-level route_by_stage with the END guard
    wf.add_conditional_edges(
        "router",
        route_by_stage,
        {
            "onboarding": "onboarding",
            "company_agent": "company_agent",
            "product_agent": "product_agent",
            "END": END,
        },
    )

    for node in ["onboarding", "company_agent", "product_agent"]:
        wf.add_edge(node, "router")

    return wf
