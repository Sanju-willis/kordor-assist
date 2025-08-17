# src\app\services\chat_service.py
import logging
import sqlite3
from typing import cast
from pathlib import Path
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.sqlite import SqliteSaver
from app.core.thread_manager import ThreadMeta
from app.graphs.home_graph import build_home_workflow
from app.graphs.social_graph import build_social_workflow
from app.graphs.analytics_graph import build_analytics_workflow

logger = logging.getLogger(__name__)

def get_checkpointer():
    # Create persistent SQLite database
    db_path = Path(".data/langraph.sqlite")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    return SqliteSaver(conn)

def get_workflow(module: str):
    workflows = {
        "home": build_home_workflow,
        "social": build_social_workflow,
        "analytics": build_analytics_workflow
    }
    builder = workflows.get(module.lower())
    if not builder:
        raise ValueError(f"Unknown module: {module}")
    return builder()

class ChatService:
    @staticmethod
    async def process_message(thread_id: str, meta: ThreadMeta, user_text: str) -> str:
        try:
            logger.info(f"Processing message for thread {thread_id}: '{user_text}'")
            
            # Get workflow by module
            logger.info(f"Getting workflow for module: {meta.module}")
            wf = get_workflow(meta.module)
            app = wf.compile(checkpointer=get_checkpointer())

            # Set stage based on thread type
            stage = "onboarding"
            if meta.thread_type == "company":
                stage = "company_ready"
            elif meta.thread_type == "product":
                stage = "product_ready"

            logger.info(f"Setting stage: {stage} for thread type: {meta.thread_type}")

            state = {
                "module": meta.module,
                "stage": stage,
                "messages": [HumanMessage(content=user_text)],
            }
            
            # Add entity context
            if meta.entity_id:
                if meta.thread_type == "company":
                    state["company_id"] = meta.entity_id
                    logger.info(f"Added company_id: {meta.entity_id}")
                elif meta.thread_type == "product":
                    state["product_id"] = meta.entity_id
                    logger.info(f"Added product_id: {meta.entity_id}")

            config: RunnableConfig = cast(RunnableConfig, {
                "configurable": {"thread_id": thread_id}
            })
            
            logger.info(f"Invoking workflow with state keys: {list(state.keys())}")
            result = app.invoke(state, config=config)
            logger.info(f"Workflow result keys: {result.keys() if isinstance(result, dict) else 'not dict'}")

            # Extract response
            msgs = result.get("messages", [])
            logger.info(f"Extracted {len(msgs)} messages from result")
            
            for i, msg in enumerate(reversed(msgs)):
                logger.info(f"Message {i}: type={type(msg).__name__}")
                
                # Handle LangChain message objects
                if isinstance(msg, AIMessage):
                    logger.info(f"Found AIMessage: {msg.content}")
                    return msg.content
                elif hasattr(msg, 'content') and hasattr(msg, 'type'):
                    if msg.type == "ai":
                        logger.info(f"Found AI message: {msg.content}")
                        return msg.content
                # Handle dict messages  
                elif isinstance(msg, dict):
                    if msg.get("role") == "assistant":
                        content = msg.get("content", "")
                        logger.info(f"Found assistant dict message: {content}")
                        return content
            
            logger.warning("No assistant message found, returning default")
            return "Ready to help!"
            
        except Exception as e:
            logger.error(f"Error in process_message: {str(e)}", exc_info=True)
            raise
