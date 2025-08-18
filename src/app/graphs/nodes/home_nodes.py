# src\app\graphs\nodes\home_nodes.py
from app.graphs.state import CustomState

def onboarding_node(state: CustomState):
    msgs = state["messages"] + [{
        "role": "assistant",
        "content": "Home module ready. Say 'company' or 'product'."
    }]
    return {**state, "messages": msgs, "stage": "onboarding"}

def company_node(state: CustomState):
    msgs = state["messages"] + [{
        "role": "assistant",
        "content": "Company agent activated. Ready to help!"
    }]
    return {**state, "messages": msgs, "stage": "company_active"}

def product_node(state: CustomState):
    msgs = state["messages"] + [{
        "role": "assistant",
        "content": "Product agent activated. Ready to help!"
    }]
    return {**state, "messages": msgs, "stage": "product_active"}
