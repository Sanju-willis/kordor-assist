# src\app\routes\health.py
from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/")
async def root():
    return {"status": "Kordor Assist is running"}
