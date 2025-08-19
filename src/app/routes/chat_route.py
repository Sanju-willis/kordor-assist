# src\app\routes\chat_route.py
from fastapi import APIRouter, Request
from app.services import ChatService
from app.lib import get_user_from_jwt
from app.schemas import SendMessageRequest

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/send")
async def send_message(body: SendMessageRequest, request: Request):
    _auth = get_user_from_jwt(request)

    response = await ChatService.process_message(body.thread_id, body.message)

    return {
        "response": response,
        "thread_id": body.thread_id,
    }
