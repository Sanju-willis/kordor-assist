# src\app\ai\tools\onboarding_tools.py
from langchain.tools import tool


@tool
def get_module_info(module: str) -> str:
    """Get information about available modules."""
    m = (module or "").strip().lower()
    if m not in {"company", "product"}:
        return "Modules: company, product. Choose one."
    return (
        "Company: org profile, roles, datasources, KPIs."
        if m == "company"
        else "Product: SKUs/services, ICPs, offers, funnels."
    )


@tool
def validate_choice(choice: str) -> str:
    """Validate user's module choice."""
    c = (choice or "").strip().lower()
    if c not in {"company", "product"}:
        return "Invalid. Choose 'company' or 'product'."
    nxt = "company.profile" if c == "company" else "product.catalog"
    return f"Valid: {c}. Next step: {nxt}"