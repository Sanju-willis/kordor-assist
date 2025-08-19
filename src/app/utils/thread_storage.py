# src\app\utils\thread_storage.py
import json
from dataclasses import asdict
from pathlib import Path
from typing import Dict
from app.lib import logger
from app.models import ThreadMeta
from app.middleware import NotFoundError


class ThreadStorage:
    def __init__(self, db_file: Path):
        self.db_file = db_file
        self._threads: Dict[str, ThreadMeta] = self._load_threads()

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

    def save_threads(self) -> None:
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

    def get_thread(self, thread_id: str) -> ThreadMeta:
        thread = self._threads.get(thread_id)
        if not thread:
            raise NotFoundError("Thread")
        logger.debug(f"get_thread hit: {thread_id} -> {thread.thread_type}")
        return thread

    def add_thread(self, thread_meta: ThreadMeta) -> None:
        self._threads[thread_meta.thread_id] = thread_meta
        self.save_threads()

    def get_all_threads(self) -> Dict[str, ThreadMeta]:
        return dict(self._threads)

    def thread_count(self) -> int:
        return len(self._threads)