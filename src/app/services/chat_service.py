# src\app\services\chat_service.py
import sqlite3
from typing import cast
from pathlib import Path
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.sqlite import SqliteSaver
from app.core.thread_manager import ThreadMeta
from app.graphs import (
    build_social_workflow,
    build_analytics_workflow,
    build_home_workflow,
)
from app.utils.logger import logger  # use shared logger


def get_checkpointer() -> SqliteSaver:
    db_path = Path(".data/langraph.sqlite")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    return SqliteSaver(conn)


def get_workflow(module: str):
    workflows = {
        "home": build_home_workflow,
        "social": build_social_workflow,
        "analytics": build_analytics_workflow,
    }
    builder = workflows.get(module.lower())
    if not builder:
        raise ValueError(f"Unknown module: {module}")
    return builder()


class ChatService:
    @staticmethod
    async def process_message(thread_id: str, meta: ThreadMeta, user_text: str) -> str:
        try:
            logger.info(f"process_message thread={thread_id} type={meta.thread_type}")
            logger.debug(f"user_text='{user_text}'")

            # Build workflow once per call (consider caching later)
            wf = get_workflow(meta.module)
            app = wf.compile(checkpointer=get_checkpointer())

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
                # LangChain objects
                if isinstance(msg, AIMessage):
                    return msg.content
                if hasattr(msg, "type") and getattr(msg, "type", None) == "ai":
                    return getattr(msg, "content", "")

                # Dict style
                if isinstance(msg, dict) and msg.get("role") == "assistant":
                    return msg.get("content", "")

            logger.warning("no assistant message found; returning default")
            return "Ready to help!"

        except Exception as e:
            logger.error(f"process_message failed: {e}", exc_info=True)
            raise  # rethrow for middleware to handle
