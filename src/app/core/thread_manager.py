# src/app/core/thread_manager.py
import json
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Optional
from app.utils import logger


@dataclass
class ThreadMeta:
    thread_id: str
    module: str
    thread_type: str  # "module" | "company" | "product"
    parent_thread_id: Optional[str] = None
    entity_id: Optional[str] = None


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
            logger.error(f"failed to load threads: {e}", exc_info=True)
            return {}

    def _save_threads(self) -> None:
        try:
            self.db_file.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.db_file.with_suffix(".json.tmp")
            payload = {k: asdict(v) for k, v in self._threads.items()}
            with tmp.open("w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
            tmp.replace(self.db_file)  # atomic-ish write on most OSes
            logger.debug(f"saved threads: {len(self._threads)}")
        except Exception as e:
            logger.error(f"failed to save threads: {e}", exc_info=True)

    def create_module_thread(self, module: str) -> str:
        module_norm = (module or "").strip().lower()
        if not module_norm:
            raise ValueError("module is required")
        thread_id = f"{module_norm}_{uuid.uuid4().hex[:6]}"
        self._threads[thread_id] = ThreadMeta(
            thread_id=thread_id, module=module_norm, thread_type="module"
        )
        self._save_threads()
        logger.info(f"created module thread: {thread_id}")
        return thread_id

    def create_sub_thread(
        self, parent_thread_id: str, sub_type: str, entity_id: Optional[str] = None
    ) -> str:
        parent = self._threads.get(parent_thread_id)
        if not parent:
            raise ValueError(f"parent thread not found: {parent_thread_id}")

        sub_norm = (sub_type or "").strip().lower()
        if sub_norm in {"company", "product"} and not entity_id:
            raise ValueError("entity_id is required for sub_type 'company' or 'product'")

        thread_id = f"{parent.module}_{sub_norm}_{uuid.uuid4().hex[:6]}"
        self._threads[thread_id] = ThreadMeta(
            thread_id=thread_id,
            module=parent.module,
            thread_type=sub_norm,
            parent_thread_id=parent_thread_id,
            entity_id=entity_id,
        )
        self._save_threads()
        logger.info(f"created sub-thread: {thread_id} (parent={parent_thread_id})")
        return thread_id

    def get_thread(self, thread_id: str) -> Optional[ThreadMeta]:
        t = self._threads.get(thread_id)
        if t:
            logger.debug(f"get_thread hit: {thread_id} -> {t.thread_type}")
        else:
            logger.warning(f"thread not found: {thread_id}")
        return t

    def list_all_threads(self) -> Dict[str, ThreadMeta]:
        return dict(self._threads)


# Global instance
thread_manager = ThreadManager()
