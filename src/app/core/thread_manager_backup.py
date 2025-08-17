# src/app/core/thread_manager.py
import logging
import json
import os
from typing import Dict, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import uuid

logger = logging.getLogger(__name__)

@dataclass
class ThreadMeta:
    thread_id: str
    module: str
    thread_type: str  # "module", "company", "product"
    parent_thread_id: Optional[str] = None
    entity_id: Optional[str] = None

class ThreadManager:
    def __init__(self):
        self.db_file = Path(".data/threads.json")
        self._threads: Dict[str, ThreadMeta] = self._load_threads()
        logger.info(f"ThreadManager initialized with {len(self._threads)} existing threads")
        
    def _load_threads(self) -> Dict[str, ThreadMeta]:
        """Load threads from persistent storage"""
        if self.db_file.exists():
            try:
                with open(self.db_file, 'r') as f:
                    data = json.load(f)
                    threads = {k: ThreadMeta(**v) for k, v in data.items()}
                    logger.info(f"Loaded {len(threads)} threads from storage")
                    return threads
            except Exception as e:
                logger.error(f"Failed to load threads: {e}")
        return {}
    
    def _save_threads(self):
        """Save threads to persistent storage"""
        try:
            self.db_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.db_file, 'w') as f:
                data = {k: asdict(v) for k, v in self._threads.items()}
                json.dump(data, f, indent=2)
                logger.info(f"Saved {len(self._threads)} threads to storage")
        except Exception as e:
            logger.error(f"Failed to save threads: {e}")
        
    def create_module_thread(self, module: str) -> str:
        """Create module level thread: home_abc123"""
        thread_id = f"{module}_{uuid.uuid4().hex[:6]}"
        thread_meta = ThreadMeta(
            thread_id=thread_id,
            module=module,
            thread_type="module"
        )
        self._threads[thread_id] = thread_meta
        self._save_threads()
        logger.info(f"Created module thread: {thread_id} for module: {module}")
        return thread_id
    
    def create_sub_thread(self, parent_thread_id: str, sub_type: str, entity_id: str = None) -> str:
        """Create sub thread: home_company_def456"""
        logger.info(f"Creating sub-thread: parent={parent_thread_id}, type={sub_type}, entity={entity_id}")
        
        parent = self._threads.get(parent_thread_id)
        if not parent:
            logger.error(f"Parent thread not found: {parent_thread_id}")
            logger.info(f"Available threads: {list(self._threads.keys())}")
            raise ValueError(f"Parent thread {parent_thread_id} not found")
            
        thread_id = f"{parent.module}_{sub_type}_{uuid.uuid4().hex[:6]}"
        thread_meta = ThreadMeta(
            thread_id=thread_id,
            module=parent.module,
            thread_type=sub_type,
            parent_thread_id=parent_thread_id,
            entity_id=entity_id
        )
        self._threads[thread_id] = thread_meta
        self._save_threads()
        logger.info(f"Created sub-thread: {thread_id}")
        return thread_id
    
    def get_thread(self, thread_id: str) -> Optional[ThreadMeta]:
        thread = self._threads.get(thread_id)
        if thread:
            logger.info(f"Found thread: {thread_id} -> {thread.thread_type}")
        else:
            logger.warning(f"Thread not found: {thread_id}")
            logger.info(f"Available threads: {list(self._threads.keys())}")
        return thread
    
    def list_all_threads(self) -> Dict[str, ThreadMeta]:
        """Get all threads for debugging"""
        return self._threads.copy()

# Global instance
thread_manager = ThreadManager()
