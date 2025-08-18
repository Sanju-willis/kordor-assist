# src\app\schemas\thread_schema.py
from pydantic import BaseModel, Field
from typing import Optional, Literal

Module = Literal["home", "social", "analytics"]
ThreadType = Literal["module", "company", "product"]


class ThreadRequest(BaseModel):
    module: Module
    thread_type: ThreadType
    entity_id: Optional[str] = None
    parent_thread_id: Optional[str] = None 
    

class ThreadResponse(BaseModel):
    thread_id: str
    module: Module
    thread_type: Literal["module", "company", "product"]
    parent_thread_id: Optional[str] = None




class SendMessageRequest(BaseModel):
    thread_id: str = Field(min_length=1)
    message: str = Field(min_length=1)


class SendMessageResponse(BaseModel):
    response: str
    thread_id: str
    module: Module
    thread_type: str


class StartSessionRequest(BaseModel):
    module: Module
    thread_type: ThreadType
    entity_id: Optional[str] = None
    parent_thread_id: Optional[str] = None 


