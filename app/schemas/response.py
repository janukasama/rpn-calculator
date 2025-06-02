"""
Pydantic schema definitions for input validation.
"""
from datetime import datetime
from pydantic import BaseModel


class OperationRead(BaseModel):
    id: int
    expression: str
    result: float
    user_id: int
    created_time: datetime

    class Config:
        from_attributes = True
