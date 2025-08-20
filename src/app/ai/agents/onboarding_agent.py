# src\app\ai\agents\onboarding_agent.py
from typing import Optional, List
from langchain_core.messages import SystemMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.base import BaseCheckpointSaver

DEFAULT_SYSTEM = """You are an onboarding specialist.
1) Explain modules (company, product)
2) Ask for a single choice
3) Validate choice and tell the next step
Be concise and directive. One question at a time.
"""

@tool
def get_module_info(module: str) -> str:
    """Return info about 'company' or 'product'."""
    m = (module or "").strip().lower()
    if m not in {"company", "product"}:
        return "Modules: company, product. Choose one."
    return "Company: org profile, roles, datasources, KPIs." if m == "company" else "Product: SKUs/services, ICPs, offers, funnels."

@tool
def validate_choice(choice: str) -> str:
    """Validate user's choice ('company' or 'product') and indicate the next step."""
    c = (choice or "").strip().lower()
    if c not in {"company", "product"}:
        return "Invalid. Choose 'company' or 'product'."
    nxt = "company.profile" if c == "company" else "product.catalog"
    return f"Valid: {c}. Next step: {nxt}"

def _messages_modifier(state) -> List[BaseMessage]:
    # Pull override from config if present; else use default.
    cfg = (state or {}).get("config", {})
    override = (cfg.get("configurable") or {}).get("system_prompt")
    prompt = override or DEFAULT_SYSTEM
    return [SystemMessage(content=prompt)]

def build_onboarding_agent(
    *,
    model: ChatOpenAI,                           # required
    checkpointer: Optional[BaseCheckpointSaver] = None,
):
    tools = [get_module_info, validate_choice]
    return create_react_agent(
        model=model,
        tools=tools,
        checkpointer=checkpointer,
    )