# src/app/main.py
from fastapi import FastAPI
from app.api.chat import router
from app.middleware.error_handler import error_handling_middleware  # central logging+errors

app = FastAPI(title="Kordor Assist")

# One global middleware for access logs + error handling
app.middleware("http")(error_handling_middleware)

# Routes
app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "Kordor Assist is running"}
