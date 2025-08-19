# src\app\routes\session_route.py
from fastapi import APIRouter, Request
from app.lib import get_user_from_jwt
from app.schemas import ThreadRequest
from app.services.session_service import SessionService

router = APIRouter(prefix="/session", tags=["session"])


@router.post("/create-thread")
async def create_thread(body: ThreadRequest, request: Request):
    auth = get_user_from_jwt(request)
    user_id = auth["user_id"]
    company_id = auth["company_id"]
    return await SessionService.create_thread(
        body,
        user_id=user_id,
        company_id=company_id,
    )
