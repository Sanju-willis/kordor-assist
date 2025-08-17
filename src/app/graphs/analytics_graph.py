# src\app\graphs\analytics_graph.py
from langgraph.graph import StateGraph, END
from app.graphs.state import CustomState

def analytics_root(state: CustomState):
    msgs = state["messages"] + [{"role":"assistant","content":"Analytics module."}]
    return {**state, "messages": msgs, "stage": "analytics_ready"}

def build_analytics_workflow() -> StateGraph:
    wf = StateGraph(CustomState)
    wf.add_node("root", analytics_root)
    wf.set_entry_point("root")
    wf.add_edge("root", END)
    return wf
