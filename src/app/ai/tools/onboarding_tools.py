# src\app\graphs\tools\onboarding_tools.py
from langchain_core.tools import tool

@tool
def get_module_info(module_name: str) -> str:
    """Get information about available modules.
    
    Args:
        module_name: Name of module (company/product)
    """
    modules = {
        "company": "Analyze business data, metrics, and competitive landscape",
        "product": "Manage features, user feedback, and product roadmap"
    }
    return modules.get(module_name, "Available modules: company, product")

@tool  
def validate_choice(choice: str) -> str:
    """Validate user's module selection.
    
    Args:
        choice: User's selected module
    """
    valid_choices = ["company", "product"]
    if choice.lower() in valid_choices:
        return f"✅ Valid choice: {choice}. Proceeding to {choice} module."
    return f"❌ Invalid choice: {choice}. Please choose: company or product"



