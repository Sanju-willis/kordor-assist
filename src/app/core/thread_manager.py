# src\app\core\thread_manager.py
from pathlib import Path
from typing import Optional, Dict
from app.lib import logger
from app.models import ThreadMeta
from app.middleware import ValidationError, NotFoundError
from app.utils.hash_utils import generate_thread_id
from app.utils.thread_storage import ThreadStorage


class ThreadManager:
    def __init__(self) -> None:
        self.storage = ThreadStorage(Path(".data/threads.json"))
        logger.info(f"ThreadManager ready (threads={self.storage.thread_count()})")

    def create_thread(
        self,
        thread_type: str,
        module: str,
        parent_thread_id: Optional[str] = None,
        entity_id: Optional[str] = None,
    ) -> str:
        if parent_thread_id:
            parent = self.storage.get_thread(parent_thread_id)
            if not parent:
                raise NotFoundError("Parent thread")

            if thread_type in {"company", "product"} and not entity_id:
                raise ValidationError(
                    "entity_id is required for sub_type 'company' or 'product'"
                )

        # Generate thread ID (works for both cases)
        thread_id = generate_thread_id(module, thread_type, parent_thread_id, entity_id)

        # Create thread metadata
        thread_meta = ThreadMeta(
            thread_id=thread_id,
            module=module,
            thread_type=thread_type,
            parent_thread_id=parent_thread_id,
            entity_id=entity_id,
        )

        # Log appropriate message
        if parent_thread_id:
            logger.info(f"Created sub-thread: {thread_id} (parent={parent_thread_id})")
        else:
            logger.info(f"Created module thread: {thread_id}")

        self.storage.add_thread(thread_meta)
        return thread_id

    def get_thread(self, thread_id: str) -> ThreadMeta:
        return self.storage.get_thread(thread_id)

    def list_all_threads(self) -> Dict[str, ThreadMeta]:
        return self.storage.get_all_threads()


# Global instance
thread_manager = ThreadManager()