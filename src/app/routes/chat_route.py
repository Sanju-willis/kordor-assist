# src\app\routes\chat_route.py
from fastapi import APIRouter, HTTPException, Request
from app.services import ChatService
from app.lib import get_user_from_jwt

from app.core import thread_manager
from app.schemas import (
    #CreateSubThreadRequest,
    SendMessageRequest,
)
from app.schemas import ThreadRequest

router = APIRouter()

@router.post("/create-thread")
async def create_thread(body: ThreadRequest, request: Request):
   auth = get_user_from_jwt(request)
   print(auth)
   
   # Create thread (module or sub-thread based on parent_thread_id presence)
   if body.parent_thread_id:
       # Creating sub-thread
       thread_id = thread_manager.create_thread(
           body.sub_type,
           body.parent_thread_id,
           body.entity_id,
       )
       return {"thread_id": thread_id, "parent_thread_id": body.parent_thread_id}
   else:
       # Creating module thread
       thread_id = thread_manager.create_thread(body.module or body.sub_type)
       return {"thread_id": thread_id, "module": body.module or body.sub_type}



@router.post("/send")
async def send_message(body: SendMessageRequest, request: Request):
    auth = get_user_from_jwt(request)
    print(auth)

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

