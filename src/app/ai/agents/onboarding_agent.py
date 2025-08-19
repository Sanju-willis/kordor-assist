# src\app\ai\agents\onboarding_agent.py
from typing import Optional
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.base import BaseCheckpointSaver

# Tools
@tool
def get_module_info(module: str) -> str:
    """Return info about an available module: company or product."""
    m = (module or "").strip().lower()
    if m not in {"company", "product"}:
        return "Modules: company, product. Choose one."
    return (
        "Company: org profile, roles, datasources, KPIs."
        if m == "company" else
        "Product: SKUs/services, ICPs, offers, funnels."
    )

@tool
def validate_choice(choice: str) -> str:
    """Validate user choice and say what's next."""
    c = (choice or "").strip().lower()
    if c not in {"company", "product"}:
        return "Invalid. Choose 'company' or 'product'."
    nxt = "company.profile" if c == "company" else "product.catalog"
    return f"Valid: {c}. Next step: {nxt}"

DEFAULT_SYSTEM = """You are an onboarding specialist.
1) Explain modules (company, product)
2) Ask for a single choice
3) Validate choice and tell the next step
Be concise and directive. One question at a time.
"""

def build_onboarding_agent(
    *,
    system_prompt: str = DEFAULT_SYSTEM,
    model: Optional[ChatOpenAI] = None,
    checkpointer: Optional[BaseCheckpointSaver] = None,
):
    # Pick a model that supports tool-calling. 4o is a safe default.
    llm = model or ChatOpenAI(model="gpt-4o")  # or "gpt-4.1", "gpt-4o-mini" for cheaper
    tools = [get_module_info, validate_choice]
    agent = create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=SystemMessage(content=system_prompt),
        checkpointer=checkpointer,
    )
    return agent
