# src\app\core\__init__.py
from app.core.thread_manager import thread_manager
from app.core.runtime import get_app

__all__ = ["thread_manager", "get_app"]
