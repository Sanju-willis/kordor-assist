# src\app\routes\__init__.py
from fastapi import FastAPI
from .chat_route import router as chat_router
from .session_route import router as session_router
from .health import router as health_router


def include_routes(app: FastAPI) -> None:
    app.include_router(session_router)
    app.include_router(chat_router)
    app.include_router(health_router)
