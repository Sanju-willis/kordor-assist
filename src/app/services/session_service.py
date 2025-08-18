# src\app\services\session_service.py
from typing import Dict, Any

def get_initial_state(user_id: str, company_id: str, module: str = "home") -> Dict[str, Any]:
    """Factory for initial workflow state"""
    return {
        "user_id": user_id,
        "company_id": company_id,
        "module": module,
        "stage": "onboarding",
        "messages": []
    }

def create_session(thread_manager, user_id: str, company_id: str, module: str = "home"):
    """Create a new session/thread with initial state"""
    state = get_initial_state(user_id, company_id, module)
    return thread_manager.create_thread(user_id, company_id, module, state)
