# src\app\routes\session_route.py
from fastapi import APIRouter
from app.lib import get_user_from_jwt
from app.schemas import ThreadRequest, AuthContext
from app.services import SessionService
from fastapi import Depends


router = APIRouter(prefix="/session", tags=["session"])


@router.post("/create-thread")
async def create_thread(
    body: ThreadRequest,
    auth: AuthContext = Depends(get_user_from_jwt),
):
    return await SessionService.create_thread(
        body=body,
        user_id=auth.user_id,
        company_id=auth.company_id,
    )
