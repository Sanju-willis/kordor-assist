# src\app\routes\chat_route.py
from fastapi import APIRouter, Request
from app.services import ChatService
from app.lib import get_user_from_jwt
from app.core import thread_manager
from app.schemas import SendMessageRequest
from app.middleware import NotFoundError

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/send")
async def send_message(body: SendMessageRequest, request: Request):
    _auth = get_user_from_jwt(request)

    meta = thread_manager.get_thread(body.thread_id)
    if not meta:
        raise NotFoundError("Thread")

    response = await ChatService.process_message(body.thread_id, meta, body.message)

    return {
        "response": response,
        "thread_id": body.thread_id,
        "module": meta.module,
        "thread_type": meta.thread_type,
    }
