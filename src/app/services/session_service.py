# src\app\services\session_service.py
from app.core import thread_manager, get_app
from app.schemas import ThreadRequest
from app.graphs import CustomState


class SessionService:
    @staticmethod
    async def create_thread(body: ThreadRequest, user_id: str, company_id: str):
        thread_id = thread_manager.create_thread(
            body.thread_type.value, body.module.value, body.parent_thread_id, body.entity_id
        )

        # compiled graph for the module
        graph = get_app(body.module)

        context = {
            "entity_id": body.entity_id,
            "thread_type": body.thread_type,
        }

        stage = (
            "company_ready"
            if body.thread_type == "company"
            else "product_ready"
            if body.thread_type == "product"
            else "onboarding"
        )

        # initial values must match your graph state schema
        state: CustomState = {
            "user_id": user_id,
            "company_id": company_id,
            "module": body.module,
            "stage": stage,
            "messages": [],
            "context": context,
        }
        config = {"configurable": {"thread_id": thread_id}}

        # Write initial state via LangGraph API (this persists via the checkpointer)
        graph.update_state(config, state)

        return {"thread_id": thread_id, "parent_thread_id": body.parent_thread_id}
