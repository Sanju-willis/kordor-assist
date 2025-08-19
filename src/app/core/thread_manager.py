# src\app\core\thread_manager.py

import json
import hashlib
from dataclasses import asdict
from pathlib import Path
from typing import Dict, Optional
from app.lib import logger
from app.models import ThreadMeta
from app.middleware import ValidationError, NotFoundError
from app.utils.hash_utils import generate_thread_id


class ThreadManager:
    def __init__(self) -> None:
        self.db_file = Path(".data/threads.json")
        self._threads: Dict[str, ThreadMeta] = self._load_threads()
        logger.info(f"ThreadManager ready (threads={len(self._threads)})")

    def _load_threads(self) -> Dict[str, ThreadMeta]:
        if not self.db_file.exists():
            return {}
        try:
            with self.db_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return {k: ThreadMeta(**v) for k, v in data.items()}
        except Exception as e:
            logger.error(f"Failed to load threads: {e}", exc_info=True)
            return {}

    def _save_threads(self) -> None:
        try:
            self.db_file.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.db_file.with_suffix(".json.tmp")
            payload = {k: asdict(v) for k, v in self._threads.items()}
            with tmp.open("w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
            tmp.replace(self.db_file)
            logger.debug(f"Saved threads: {len(self._threads)}")
        except Exception as e:
            logger.error(f"Failed to save threads: {e}", exc_info=True)

    def create_thread(
        self,
        thread_type: str,
        module: str,
        parent_thread_id: Optional[str] = None,
        entity_id: Optional[str] = None,
    ) -> str:
        if parent_thread_id:
            parent = self._threads.get(parent_thread_id)
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

        self._threads[thread_id] = thread_meta
        return thread_id

    def get_thread(self, thread_id: str) -> ThreadMeta:
        thread = self._threads.get(thread_id)
        if not thread:
            raise NotFoundError("Thread")
        logger.debug(f"get_thread hit: {thread_id} -> {thread.thread_type}")
        return thread

    def list_all_threads(self) -> Dict[str, ThreadMeta]:
        return dict(self._threads)

    def _short_hash(self, input_str: str) -> str:
        return hashlib.md5(input_str.encode()).hexdigest()[:6]


# Global instance
thread_manager = ThreadManager()
