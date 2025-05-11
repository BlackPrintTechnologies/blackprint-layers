from pydantic import BaseModel
from typing import Any, Optional

class Response(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None

    @classmethod
    def success(cls, data: Any = None, message: str = "Success"):
        return cls(success=True, data=data, message=message)

    @classmethod
    def error(cls, message: str, data: Any = None):
        return cls(success=False, data=data, message=message)

    @classmethod
    async def async_success(cls, data: Any = None, message: str = "Success"):
        return cls(success=True, data=data, message=message)

    @classmethod
    async def async_error(cls, message: str, data: Any = None):
        return cls(success=False, data=data, message=message) 