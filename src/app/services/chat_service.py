# src\app\services\chat_service.py
from typing import cast
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from app.core import thread_manager, get_app
from app.lib import logger


class ChatService:
    @staticmethod
    async def process_message(thread_id: str, user_text: str) -> str:
        meta = thread_manager.get_thread(thread_id)

        app = get_app(meta.module)

        config: RunnableConfig = cast(
            RunnableConfig, {"configurable": {"thread_id": thread_id}}
        )

        result = app.invoke(
            {"messages": [HumanMessage(content=user_text)]},
            config=config,
        )

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
