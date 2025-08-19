# src\app\services\chat_service.py
from typing import cast
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from app.models import ThreadMeta
from app.core import get_app
from app.lib import logger

class ChatService:
    @staticmethod
    async def process_message(thread_id: str, meta: ThreadMeta, user_text: str) -> str:
        app = get_app(meta.module)

        # Stage by thread type
        stage = (
            "company_ready"
            if meta.thread_type == "company"
            else "product_ready"
            if meta.thread_type == "product"
            else "onboarding"
        )
        logger.debug(f"stage={stage}")

        state = {
            "module": meta.module,
            "stage": stage,
            "messages": [HumanMessage(content=user_text)],
        }

        # Entity context
        if meta.entity_id:
            if meta.thread_type == "company":
                state["company_id"] = meta.entity_id
            elif meta.thread_type == "product":
                state["product_id"] = meta.entity_id
            logger.debug(f"context set for {meta.thread_type}: {meta.entity_id}")

        config: RunnableConfig = cast(
            RunnableConfig, {"configurable": {"thread_id": thread_id}}
        )

        logger.debug(f"invoking workflow with keys={list(state.keys())}")
        result = app.invoke(state, config=config)

        msgs = result.get("messages", []) if isinstance(result, dict) else []
        logger.debug(f"messages returned={len(msgs)}")

        # Walk from last to first to find assistant reply
        for msg in reversed(msgs):
            if isinstance(msg, AIMessage):
                return msg.content
            if hasattr(msg, "type") and getattr(msg, "type", None) == "ai":
                return getattr(msg, "content", "")
            if isinstance(msg, dict) and msg.get("role") == "assistant":
                return msg.get("content", "")

        logger.warning("no assistant message found; returning default")
        return "Ready to help!"