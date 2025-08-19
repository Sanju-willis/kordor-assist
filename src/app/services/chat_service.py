# src\app\services\chat_service.py
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from typing import cast
from app.core import thread_manager, get_app
from app.lib import logger


class ChatService:
    @staticmethod
    async def process_message(thread_id: str, user_text: str) -> str:
        meta = thread_manager.get_thread(thread_id)
        app = get_app(meta.module)

        config: RunnableConfig = cast(
            RunnableConfig,
            {"configurable": {"thread_id": thread_id}, "recursion_limit": 100},
        )

        result = app.invoke({"messages": [HumanMessage(content=user_text)]}, config=config)
        msgs: list[BaseMessage] = result.get("messages", []) if isinstance(result, dict) else []

        for msg in reversed(msgs):
            if isinstance(msg, AIMessage):
                return str(msg.content)
            if isinstance(msg, dict) and msg.get("role") == "assistant":
                return str(msg.get("content", ""))

        logger.warning("No assistant message found; returning default")
        return "Ready to help!"
