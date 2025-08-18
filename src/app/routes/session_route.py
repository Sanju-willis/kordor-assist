# src\app\routes\session_route.py
from fastapi import APIRouter, HTTPException, Request
from app.lib import get_user_from_jwt
from app.core import thread_manager
from app.schemas import ThreadRequest
from app.lib.logger import logger

router = APIRouter(prefix="/session", tags=["session"])


@router.post("/create-thread")
async def create_thread(body: ThreadRequest, request: Request):
    # Auth present even if you’re not using it yet; keeps parity with chat route
    _auth = get_user_from_jwt(request)

    try:
        thread_id = thread_manager.create_thread(
            body.thread_type,
            body.module,
            body.parent_thread_id,
            body.entity_id,
        )
        return {"thread_id": thread_id, "parent_thread_id": body.parent_thread_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating thread: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
