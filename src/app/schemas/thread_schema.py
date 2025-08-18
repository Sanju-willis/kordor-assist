# src\app\schemas\thread_schema.py
from pydantic import BaseModel, Field
from typing import Optional, Literal

Module = Literal["home", "social", "analytics"]
SubType = Literal["module", "company", "product"]

class ThreadRequest(BaseModel):
    module: Module
    sub_type: SubType
    entity_id: Optional[str] = None
    parent_thread_id: Optional[str] = None 

class ThreadResponse(BaseModel):
    thread_id: str
    module: Module
    thread_type: Literal["module", "company", "product"]
    parent_thread_id: Optional[str] = None
    
class CreateThreadResponse(BaseModel):
    thread_id: str
    module: Module




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





