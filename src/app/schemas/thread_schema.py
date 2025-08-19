# src\app\schemas\thread_schema.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from enum import Enum


class ModuleEnum(str, Enum):
    home = "home"
    social = "social"
    analytics = "analytics"

class ThreadTypeEnum(str, Enum):
    module = "module"
    company = "company"
    product = "product"

class ThreadRequest(BaseModel):
    module: ModuleEnum
    thread_type: ThreadTypeEnum
    entity_id: Optional[str] = None
    parent_thread_id: Optional[str] = None
    

class ThreadResponse(BaseModel):
    thread_id: str
    module: ModuleEnum
    thread_type: Literal["module", "company", "product"]
    parent_thread_id: Optional[str] = None


class SendMessageRequest(BaseModel):
    thread_id: str = Field(min_length=1)
    message: str = Field(min_length=1)


class SendMessageResponse(BaseModel):
    response: str
    thread_id: str
    module: ModuleEnum
    thread_type: str



class AuthContext(BaseModel):
    user_id: str
    company_id: str

    @field_validator("user_id", "company_id")
    @classmethod
    def not_empty(cls, v, info):
        if not v:
            raise ValueError(f"Invalid token: missing {info.field_name}")
        return v
