from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import StreamingResponse

from app.models.db_connection import get_async_db_session
from app.schemas.request import OperationCreate
from app.schemas.response import OperationRead
from app.services.api.calculator_service import CalculatorService

router = APIRouter()


@router.post("/calculate", response_model=OperationRead)
async def calculate(request: Request, op: OperationCreate, db_session: AsyncSession = Depends(get_async_db_session)):
    try:
        response = await CalculatorService(
            app_state=request.app.state,
            db_session=db_session
        ).calculate(op)
        return response
    except Exception as e:
        request.app.state.services["logger"].error(
            f"Failed while calculating results for expression={op.expression} of user={op.user_id}, error={e}"
        )
        raise HTTPException(status_code=500, detail="Internal server error while calculating results.")


@router.get("/export")
async def export_csv(request: Request, db_session: AsyncSession = Depends(get_async_db_session)):
    try:
        row_gen = await CalculatorService(
            app_state=request.app.state,
            db_session=db_session
        ).generate_csv_file()

        return StreamingResponse(
            row_gen(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=operations.csv"}
        )
    except Exception as e:
        request.app.state.services["logger"].error(f"Failed while creating the CSV, error={e}")
        raise HTTPException(status_code=500, detail="Internal server error while calculating results.")
