# src\app\types\graph_state.py
from typing import Dict, Any, Literal
from typing_extensions import NotRequired
from langgraph.graph import MessagesState

ModuleStr = Literal["home", "social", "analytics"]

class CustomState(MessagesState):
    user_id: str
    company_id: str
    module: ModuleStr      
    thread_type: str
    stage: str
    product_id: NotRequired[str]
    context: NotRequired[Dict[str, Any]]
