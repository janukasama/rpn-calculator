from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import State

from app.models.operation import Operation
from app.schemas.request import OperationCreate
from app.services.application.db_service import DBService


class CalculatorService:

    def __init__(self, app_state: State, db_session: AsyncSession):
        self.__logger = app_state.services["logger"]
        self.__database_service = DBService(self.__logger, db_session)

    async def calculate(self, op: OperationCreate) -> Operation:
        result: float = self.__evaluate_rpn(op.expression)
        self.__logger.info(f"Expression={op.expression} by user_id={op.user_id} evaluated to={result}")
        return await self.__database_service.create_operation(op.user_id, op.expression, result)

    @staticmethod
    def __evaluate_rpn(expression: str) -> float:
        stack = []
        tokens = expression.strip().split()

        for token in tokens:
            if token in "+-*/":
                b = stack.pop()
                a = stack.pop()
                result = eval(f"{a}{token}{b}")
                stack.append(result)
            else:
                stack.append(float(token))
        if len(stack) != 1:
            raise ValueError("Invalid RPN expression")
        return stack[0]

    async def generate_csv_file(self):
        async def row_generator():
            yield "id|expression|result|user_id|created_time\n"
            async for batch in self.__database_service.fetch_operations_in_batches():
                for op in batch:
                    yield f"{op.id}|{op.expression}|{op.result}|{op.user_id}|{op.created_time.isoformat()}\n"
        return row_generator

