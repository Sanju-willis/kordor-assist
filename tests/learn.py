from abc import ABC
from typing import Any, Dict, Optional
from pydantic import BaseModel

class BaseMessage(BaseModel, ABC):
    """Abstract base class for all messages."""

    content: str
    additional_kwargs: Dict[str, Any] = {}
    response_metadata: Dict[str, Any] = {}
    id: Optional[str] = None

    @property
    def type(self) -> str:
        """Each subclass overrides this with its role name."""
        raise NotImplementedError
