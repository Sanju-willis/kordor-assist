# src/app/graphs/nodes/home_nodes.py
from app.types.graph_state import CustomState
from langchain_core.messages import AIMessage

def onboarding_node(state: CustomState):
    msgs = state["messages"] + [AIMessage(content="Home module ready. Say 'company' or 'product'.")]
    return {**state, "messages": msgs, "stage": "onboarding"}

def company_node(state: CustomState):
    msgs = state["messages"] + [AIMessage(content="Company agent activated. Ready to help!")]
    return {**state, "messages": msgs, "stage": "company_active"}

def product_node(state: CustomState):
    msgs = state["messages"] + [AIMessage(content="Product agent activated. Ready to help!")]
    return {**state, "messages": msgs, "stage": "product_active"}
