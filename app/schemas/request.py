"""
Pydantic schema definitions for input validation.
"""

from pydantic import BaseModel


class OperationCreate(BaseModel):
    user_id: int
    expression: str
