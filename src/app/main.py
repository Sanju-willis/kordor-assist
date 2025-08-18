# src\app\main.py

from fastapi import FastAPI
from app.middleware.error_handler import error_handling_middleware
from app.core.runtime import get_app  # noqa: F401
from app.routes import include_routes


app = FastAPI(title="Kordor Assist")

app.middleware("http")(error_handling_middleware)

# Routes
include_routes(app)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"status": "Kordor Assist is running"}
