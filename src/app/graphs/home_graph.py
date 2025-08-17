# src\app\graphs\home_graph.py
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage
from app.graphs.state import CustomState
import logging

logger = logging.getLogger(__name__)

def onboarding_node(state: CustomState):
    msgs = state["messages"] + [{"role":"assistant","content":"Home module ready. Say 'company' or 'product'."}]
    return {**state, "messages": msgs, "stage": "onboarding"}

def company_node(state: CustomState):
    msgs = state["messages"] + [{"role":"assistant","content":"Company agent activated. Ready to help!"}]
    return {**state, "messages": msgs, "stage": "company_active"}

def product_node(state: CustomState):
    msgs = state["messages"] + [{"role":"assistant","content":"Product agent activated. Ready to help!"}]
    return {**state, "messages": msgs, "stage": "product_active"}

def route_by_stage(state: CustomState) -> str:
    """Route based on thread stage"""
    stage = state.get("stage", "")
    logger.info(f"Routing by stage: {stage}")
    if "company" in stage:
        return "company_agent"
    elif "product" in stage:
        return "product_agent"
    return "onboarding"

def route_by_message(state: CustomState) -> str:
    """Route based on user message - FIXED"""
    try:
        if not state.get("messages"):
            logger.info("No messages, routing to onboarding")
            return "onboarding"
        
        last_msg = state["messages"][-1]
        logger.info(f"Last message type: {type(last_msg)}")
        
        # Handle both LangChain message objects and dicts
        if isinstance(last_msg, BaseMessage):
            content = last_msg.content
        elif hasattr(last_msg, 'content'):
            content = last_msg.content  
        elif isinstance(last_msg, dict):
            content = last_msg.get("content", "")
        else:
            content = str(last_msg)
        
        content = content.lower().strip()
        logger.info(f"Message content: '{content}'")
        
        if "company" in content:
            logger.info("Routing to company_agent")
            return "company_agent"
        elif "product" in content:
            logger.info("Routing to product_agent") 
            return "product_agent"
        
        logger.info("Routing to onboarding (default)")
        return "onboarding"
        
    except Exception as e:
        logger.error(f"Error in route_by_message: {e}")
        return "onboarding"

def build_home_workflow() -> StateGraph:
    wf = StateGraph(CustomState)
    
    wf.add_node("onboarding", onboarding_node)
    wf.add_node("company_agent", company_node)
    wf.add_node("product_agent", product_node)
    
    # Entry routing
    wf.set_conditional_entry_point(route_by_stage)
    
    # From onboarding, route by message
    wf.add_conditional_edges("onboarding", route_by_message, {
        "company_agent": "company_agent",
        "product_agent": "product_agent", 
        "onboarding": END
    })
    
    wf.add_edge("company_agent", END)
    wf.add_edge("product_agent", END)
    
    return wf
