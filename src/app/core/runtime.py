# src\app\core\runtime.py

import sqlite3
from pathlib import Path
from langgraph.checkpoint.sqlite import SqliteSaver

from app.graphs import (
    build_home_workflow,
    build_social_workflow,
    build_analytics_workflow,
)


# 1. Create SQLite connection ONCE
_db_path = Path(".data/langraph.sqlite")
_db_path.parent.mkdir(parents=True, exist_ok=True)
_conn = sqlite3.connect(str(_db_path), check_same_thread=False)
CHECKPOINTER = SqliteSaver(_conn)

# 2. Build + compile each graph ONCE
APP_REGISTRY = {
    "home": build_home_workflow().compile(checkpointer=CHECKPOINTER),
    "social": build_social_workflow().compile(checkpointer=CHECKPOINTER),
    "analytics": build_analytics_workflow().compile(checkpointer=CHECKPOINTER),
}


# 3. Safe fetch
def get_app(module: str):
    module = module.lower()
    if module not in APP_REGISTRY:
        raise ValueError(f"Unknown module: {module}")
    return APP_REGISTRY[module]
print("[✔] LangGraph apps compiled and ready")
