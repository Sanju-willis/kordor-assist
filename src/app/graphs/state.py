# src\app\graphs\state.py
from typing import Literal, Dict, Any
from typing_extensions import NotRequired
from langgraph.graph import MessagesState


class CustomState(MessagesState):
    module: Literal["home", "social", "analytics"]
    stage: str
    user_id: NotRequired[str]
    company_id: NotRequired[str]
    product_id: NotRequired[str]
    context: NotRequired[Dict[str, Any]]
