from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from app.models.operation import Operation
from app.services.application.logger_service import LoggerService


class DBService:
    """
    Handles database operations related to the Operation model.
    Includes functionality for inserting new records and fetching data in batches.
    """

    def __init__(self, logger: LoggerService, db_session: AsyncSession):
        """
        Initialize the DBService with a logger and an asynchronous DB session.

        params:
            logger: LoggerService instance for logging events and errors.
            db_session: SQLAlchemy async session used for all DB interactions.
        """
        self.__logger = logger
        self.__db_session = db_session

    async def create_operation(self, user_id: int, expression: str, result: float) -> Operation:
        """
        Insert a new operation into the database, or retrieve it if it already exists.

        params:
            user_id: ID of the user who submitted the operation.
            expression: RPN expression as a string.
            result: Computed float result of the expression.

        return:
            Operation: The newly created or existing operation record.

        raises:
            SQLAlchemyError: If a DB error occurs during insertion or selection.
        """
        try:
            # Attempt to insert the new operation (do nothing if already exists)
            stmt = insert(Operation).values(
                user_id=user_id,
                expression=expression,
                result=result
            ).on_conflict_do_nothing(
                index_elements=["user_id", "expression"]
            ).returning(Operation)

            result_proxy = await self.__db_session.execute(stmt)
            await self.__db_session.commit()

            operation = result_proxy.scalars().one_or_none()
            if operation is not None:
                self.__logger.info(f"Inserted operation for user_id={user_id} with expression='{expression}'")
                return operation

            # If insert was skipped due to conflict, retrieve the existing operation
            self.__logger.warning(f"Operation already exists for user_id={user_id} and expression='{expression}'")
            select_stmt = select(Operation).where(
                Operation.user_id == user_id,
                Operation.expression == expression
            )
            result_proxy = await self.__db_session.execute(select_stmt)
            return result_proxy.scalar_one()
        except SQLAlchemyError as e:
            self.__logger.error(f"Database error while creating operation: {e}")
            raise

    async def fetch_operations_in_batches(self, chunk_size=1000):
        """
        Asynchronously stream all Operation records from the database in batches.

        params:
            chunk_size: The number of records to include in each batch (default=1000).

        return:
            AsyncGenerator[List[Operation]]: Generator yielding lists of Operation records.
        """
        stmt = select(Operation)
        stream = await self.__db_session.stream(stmt)

        batch = []
        async for result in stream:
            batch.append(result.Operation)
            if len(batch) == chunk_size:
                yield batch
                batch = []
        if batch:
            yield batch
