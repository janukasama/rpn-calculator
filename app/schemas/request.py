"""
Pydantic schema definitions for input/output validation.
"""

from pydantic import BaseModel
from datetime import datetime


class OperationCreate(BaseModel):
    user_id: int
    expression: str


class OperationRead(BaseModel):
    id: int
    expression: str
    result: float
    user_id: int
    created_time: datetime

    class Config:
        orm_mode = True
