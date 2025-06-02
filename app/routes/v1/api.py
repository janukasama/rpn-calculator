"""
Mount versioned routes.
"""

from fastapi import APIRouter
from app.routes.v1.endpoints import calculator

api_router = APIRouter()
api_router.include_router(calculator.router, prefix="/api/v1/rpn", tags=["calculator"])
