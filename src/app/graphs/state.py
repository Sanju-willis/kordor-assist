# src\app\graphs\state.py
from typing import Literal
from typing_extensions import NotRequired
from langgraph.graph import MessagesState

class CustomState(MessagesState):
    module: Literal["home", "social", "analytics"]
    stage: NotRequired[str]
    user_id: NotRequired[str]
    company_id: NotRequired[str]
    product_id: NotRequired[str]
