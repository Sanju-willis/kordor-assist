# src\app\services\session_service.py
from app.core import thread_manager, get_app
from langchain_core.runnables import RunnableConfig
from app.schemas import ThreadRequest
from app.types.graph_state import CustomState
from typing import cast
from app.lib import build_context, build_initial_state


class SessionService:
    @staticmethod
    async def create_thread(body: ThreadRequest, user_id: str, company_id: str):
        
        thread_id = thread_manager.create_thread(
            user_id,
            company_id,
            body.module.value,
            body.thread_type.value,
            body.parent_thread_id,
            body.entity_id,
        )

        # compiled graph for the module
        graph = get_app(body.module)

        context = build_context(
            body.thread_type.value,
            body.entity_id,
        )

        state: CustomState = cast(
            CustomState,
            build_initial_state(
                user_id,
                company_id,
                body.module.value,  # str
                body.thread_type.value,  # str
                context,
            ),
        )


        config: RunnableConfig = cast(
            RunnableConfig, {"configurable": {"thread_id": thread_id}}
        )

        # Write initial state via LangGraph API (this persists via the checkpointer)
        graph.update_state(config, state)

        return {"thread_id": thread_id, "parent_thread_id": body.parent_thread_id}
