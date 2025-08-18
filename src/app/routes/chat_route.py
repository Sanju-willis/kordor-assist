# src\app\routes\chat_route.py
from fastapi import APIRouter, HTTPException, Request
from app.services import ChatService
from app.lib import get_user_from_jwt
from app.core import thread_manager
from app.schemas import SendMessageRequest
from app.lib.logger import logger

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/send")
async def send_message(body: SendMessageRequest, request: Request):
    try:
        _auth = get_user_from_jwt(request)
        #print(f"shisge:{body}")

        meta = thread_manager.get_thread(body.thread_id)
        if not meta:
            raise HTTPException(status_code=404, detail="Thread not found")

        response = await ChatService.process_message(body.thread_id, meta, body.message)

        return {
            "response": response,
            "thread_id": body.thread_id,
            "module": meta.module,
            "thread_type": meta.thread_type,
        }

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
