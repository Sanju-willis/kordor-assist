# src\app\graphs\social_graph.py
from langgraph.graph import StateGraph, END
from app.graphs.state import CustomState

def social_root(state: CustomState):
    msgs = state["messages"] + [{"role":"assistant","content":"Social module."}]
    return {**state, "messages": msgs, "stage": "social_ready"}

def build_social_workflow() -> StateGraph:
    wf = StateGraph(CustomState)
    wf.add_node("root", social_root)
    wf.set_entry_point("root")
    wf.add_edge("root", END)
    return wf
