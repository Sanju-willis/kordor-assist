# src\app\graphs\home_graph.py
from typing import Any
import re
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage
from app.graphs.state import CustomState
from app.lib.logger import logger
from app.graphs.nodes.home_nodes import onboarding_node, company_node, product_node

# Word-boundary patterns
RE_COMPANY = re.compile(r"\bcompany\b", re.IGNORECASE)
RE_PRODUCT = re.compile(r"\bproduct\b", re.IGNORECASE)

def _last_message_text(state: CustomState) -> str:
    msgs = state.get("messages") or []
    if not msgs:
        return ""
    last = msgs[-1]
    # LangChain BaseMessage or duck-typed object
    if isinstance(last, BaseMessage) or hasattr(last, "content"):
        try:
            return str(getattr(last, "content"))
        except Exception:
            return ""
    # Dict shape
    if isinstance(last, dict):
        return str(last.get("content", ""))
    # Fallback
    return str(last)

def route_by_stage(state: CustomState) -> str:
    stage = str(state.get("stage", "")).lower().strip()
    logger.debug("route_by_stage stage=%s", stage)
    if stage == "company_ready":
        return "company_agent"
    if stage == "product_ready":
        return "product_agent"
    return "onboarding"

def route_by_message(state: CustomState) -> str:
    text = _last_message_text(state).strip()
    if not text:
        logger.debug("route_by_message no messages; onboarding")
        return "onboarding"

    logger.debug("route_by_message text=%r", text[:160])
    if RE_COMPANY.search(text):
        return "company_agent"
    if RE_PRODUCT.search(text):
        return "product_agent"
    return "onboarding"

def build_home_workflow() -> StateGraph:
    wf = StateGraph(CustomState)

    # Nodes
    wf.add_node("onboarding", onboarding_node)
    wf.add_node("company_agent", company_node)
    wf.add_node("product_agent", product_node)

    # Entry and transitions
    wf.set_conditional_entry_point(route_by_stage)

    wf.add_conditional_edges(
        "onboarding",
        route_by_message,
        {
            "company_agent": "company_agent",
            "product_agent": "product_agent",
            "onboarding": "onboarding",
        },
    )

    # End edges
    wf.add_edge("company_agent", END)
    wf.add_edge("product_agent", END)

    return wf
