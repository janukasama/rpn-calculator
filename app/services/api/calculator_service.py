from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import State

from app.models.operation import Operation
from app.schemas.request import OperationCreate
from app.services.application.db_service import DBService
from app.utils.rpn import evaluate_rpn


class CalculatorService:
    """
    Service responsible for handling RPN calculations and related database operations.
    """

    def __init__(self, app_state: State, db_session: AsyncSession):
        """
        Initialize the CalculatorService with application state and database session.

        params:
            app_state: Shared application state, containing service instances like logger.
            db_session: SQLAlchemy async session used for DB operations.
        """
        self.__logger = app_state.services["logger"]
        self.__database_service = DBService(self.__logger, db_session)

    async def calculate(self, op: OperationCreate) -> Operation:
        """
        Evaluate an RPN expression and persist the result as a new Operation in the database.

        params:
            op: OperationCreate schema containing the expression and user_id.

        return:
            Operation: The created operation record with result and metadata.
        """
        result: float = evaluate_rpn(op.expression)
        self.__logger.info(f"Expression={op.expression} by user_id={op.user_id} evaluated to={result}")
        return await self.__database_service.create_operation(op.user_id, op.expression, result)

    async def generate_csv_file(self):
        """
        Generate a CSV row generator function that streams operation records.

        return:
            Callable: An async generator function that yields CSV rows line-by-line.
        """
        async def row_generator():
            yield "id|expression|result|user_id|created_time\n"
            async for batch in self.__database_service.fetch_operations_in_batches():
                for op in batch:
                    yield f"{op.id}|{op.expression}|{op.result}|{op.user_id}|{op.created_time.isoformat()}\n"

        return row_generator
