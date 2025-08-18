# src\app\core\thread_manager.py
import json
import hashlib
from dataclasses import asdict
from pathlib import Path
from typing import Dict, Optional
from app.lib import logger
from app.models import ThreadMeta


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
        sub_type = (thread_type or "").strip().lower()
        if not sub_type:
            raise ValueError("thread_type is required")

        if parent_thread_id:
            parent = self._threads.get(parent_thread_id)
            if not parent:
                raise ValueError(f"Parent thread not found: {parent_thread_id}")

            if sub_type in {"company", "product"} and not entity_id:
                raise ValueError("entity_id is required for sub_type 'company' or 'product'")

            hash_input = f"{parent.module}_{sub_type}_{parent_thread_id}_{entity_id or ''}"
            thread_id = f"{parent.module}_{sub_type}_{self._short_hash(hash_input)}"
            thread_meta = ThreadMeta(
                thread_id=thread_id,
                module=parent.module,
                thread_type=sub_type,
                parent_thread_id=parent_thread_id,
                entity_id=entity_id,
            )
            logger.info(f"Created sub-thread: {thread_id} (parent={parent_thread_id})")
        else:
            hash_input = f"{module}_{sub_type}"
            thread_id = f"{module}_{sub_type}_{self._short_hash(hash_input)}"
            thread_meta = ThreadMeta(
                thread_id=thread_id,
                module=module,
                thread_type=sub_type,
                parent_thread_id=None,
                entity_id=None,
            )
            logger.info(f"Created module thread: {thread_id}")

        self._threads[thread_id] = thread_meta
        self._save_threads()
        return thread_id

    def get_thread(self, thread_id: str) -> ThreadMeta:
        t = self._threads.get(thread_id)
        if not t:
            logger.error(f"Thread not found: {thread_id}")
            raise ValueError(f"Thread not found: {thread_id}")
        logger.debug(f"get_thread hit: {thread_id} -> {t.thread_type}")
        return t

    def list_all_threads(self) -> Dict[str, ThreadMeta]:
        return dict(self._threads)

    def _short_hash(self, input_str: str) -> str:
        return hashlib.md5(input_str.encode()).hexdigest()[:6]


# Global instance
thread_manager = ThreadManager()
