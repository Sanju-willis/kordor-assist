# src\app\schemas\chat.py
from pydantic import BaseModel, Field
from typing import Optional, Literal

Module = Literal["home", "social", "analytics"]
SubType = Literal["company", "product"]

class CreateThreadRequest(BaseModel):
    module: Module

class CreateThreadResponse(BaseModel):
    thread_id: str
    module: Module

class CreateSubThreadRequest(BaseModel):
    parent_thread_id: str = Field(min_length=1)
    sub_type: SubType
    entity_id: Optional[str] = None

class CreateSubThreadResponse(BaseModel):
    thread_id: str
    parent_thread_id: str

class SendMessageRequest(BaseModel):
    thread_id: str = Field(min_length=1)
    message: str = Field(min_length=1)

class SendMessageResponse(BaseModel):
    response: str
    thread_id: str
    module: Module
    thread_type: str
