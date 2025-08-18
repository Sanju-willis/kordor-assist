# src\app\routes\chat_route.py
from fastapi import APIRouter, HTTPException
from app.services import ChatService
from app.core import thread_manager
from app.schemas import (
    CreateSubThreadRequest,
    SendMessageRequest,
)
from app.schemas import ThreadRequest

router = APIRouter()

@router.post("/create-thread")
async def create_thread(body: ThreadRequest):
    thread_id = thread_manager.create_module_thread(body.module)

    return {"thread_id": thread_id, "module": body.module}

@router.post("/create-sub-thread")
async def create_sub_thread(body: CreateSubThreadRequest):
    if body.sub_type in ("company", "product") and body.entity_id is None:
        raise HTTPException(status_code=422, detail="entity_id is required for this sub_type")

    assert not (body.sub_type in ("company","product") and body.entity_id is None)

    thread_id = thread_manager.create_sub_thread(
        body.parent_thread_id,
        body.sub_type,
        body.entity_id,  # now safe
    )
    return {"thread_id": thread_id, "parent_thread_id": body.parent_thread_id}


@router.post("/send")
async def send_message(body: SendMessageRequest):
    
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
