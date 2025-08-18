# src\app\schemas\chat.py
from pydantic import BaseModel, Field, model_validator
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


class ThreadRequest(BaseModel):
    module: Module
    sub_type: Optional[SubType] = None
    parent_thread_id: Optional[str] = Field(default=None, min_length=1)
    entity_id: Optional[str] = None

    @model_validator(mode="after")
    def validate_subthread_rules(self):
        if self.sub_type is None:
            if self.parent_thread_id or self.entity_id:
                raise ValueError(
                    "For module thread, do not send parent_thread_id or entity_id."
                )
        else:
            if not self.parent_thread_id:
                raise ValueError("parent_thread_id is required when sub_type is set.")
            if self.sub_type in {"company", "product"} and not self.entity_id:
                raise ValueError(
                    "entity_id is required for sub_type 'company' or 'product'."
                )
        return self


class ThreadResponse(BaseModel):
    thread_id: str
    module: Module
    thread_type: Literal["module", "company", "product"]
    parent_thread_id: Optional[str] = None
