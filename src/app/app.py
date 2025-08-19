# src\app\app.py
from fastapi import FastAPI
from app.middleware import logging_middleware, error_handling_middleware
from app.routes import include_routes
from app.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    # Middleware (order: logging → error handler)
    app.middleware("http")(logging_middleware)
    app.middleware("http")(error_handling_middleware)

    # Routes
    include_routes(app)

    return app
