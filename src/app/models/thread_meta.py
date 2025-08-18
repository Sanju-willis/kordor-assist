# src\app\models\thread_meta.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class ThreadMeta:
    thread_id: str
    module: str
    thread_type: str  # "module" | "company" | "product"
    parent_thread_id: Optional[str] = None
    entity_id: Optional[str] = None
