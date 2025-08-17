# src\app\api\chat.py
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.chat_service import ChatService
from app.core.thread_manager import thread_manager

logger = logging.getLogger(__name__)
router = APIRouter()

class CreateThreadRequest(BaseModel):
    module: str  # "home", "social", "analytics"

class CreateSubThreadRequest(BaseModel):
    parent_thread_id: str
    sub_type: str  # "company", "product"
    entity_id: Optional[str] = None

class SendMessageRequest(BaseModel):
    thread_id: str
    message: str

@router.post("/create-thread")
async def create_thread(request: CreateThreadRequest):
    """POST /create-thread {"module": "home"}"""
    try:
        logger.info(f"Creating thread for module: {request.module}")
        thread_id = thread_manager.create_module_thread(request.module)
        logger.info(f"Created thread: {thread_id}")
        return {"thread_id": thread_id, "module": request.module}
    except Exception as e:
        logger.error(f"Failed to create thread: {str(e)}")
        raise HTTPException(400, f"Failed to create thread: {str(e)}")

@router.post("/create-sub-thread") 
async def create_sub_thread(request: CreateSubThreadRequest):
    """POST /create-sub-thread {"parent_thread_id": "home_abc123", "sub_type": "company", "entity_id": "comp_123"}"""
    try:
        logger.info(f"Creating sub-thread: {request.sub_type} under {request.parent_thread_id}")
        thread_id = thread_manager.create_sub_thread(
            request.parent_thread_id, 
            request.sub_type, 
            request.entity_id
        )
        logger.info(f"Created sub-thread: {thread_id}")
        return {"thread_id": thread_id, "parent_thread_id": request.parent_thread_id}
    except ValueError as e:
        logger.error(f"Thread creation failed: {str(e)}")
        raise HTTPException(404, str(e))
    except Exception as e:
        logger.error(f"Unexpected error creating sub-thread: {str(e)}")
        raise HTTPException(400, f"Failed to create sub-thread: {str(e)}")

@router.post("/send")
async def send_message(request: SendMessageRequest):
    """POST /send {"thread_id": "home_company_def456", "message": "help"}"""
    try:
        logger.info(f"Processing message for thread: {request.thread_id}")
        thread_meta = thread_manager.get_thread(request.thread_id)
        if not thread_meta:
            logger.warning(f"Thread not found: {request.thread_id}")
            raise HTTPException(404, "Thread not found")
        
        logger.info(f"Thread meta: module={thread_meta.module}, type={thread_meta.thread_type}")
        
        response = await ChatService.process_message(
            request.thread_id, 
            thread_meta, 
            request.message
        )
        
        logger.info(f"Message processed successfully for thread: {request.thread_id}")
        return {
            "response": response,
            "thread_id": request.thread_id,
            "module": thread_meta.module,
            "thread_type": thread_meta.thread_type
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        raise HTTPException(500, f"Failed to process message: {str(e)}")
