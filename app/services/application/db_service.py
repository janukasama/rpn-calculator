from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from app.models.operation import Operation
from app.services.application.logger_service import LoggerService


class DBService:

    def __init__(self, logger: LoggerService, db_session: AsyncSession):
        self.__logger = logger
        self.__db_session = db_session

    async def create_operation(self, user_id: int, expression: str, result: float) -> Operation:
        try:
            stmt = insert(Operation).values(
                user_id=user_id,
                expression=expression,
                result=result
            ).on_conflict_do_nothing(
                index_elements=["user_id", "expression"]
            ).returning(Operation)

            result_proxy = await self.__db_session.execute(stmt)
            await self.__db_session.commit()

            row = result_proxy.fetchone()
            if row is not None:
                self.__logger.info(f"Inserted operation for user_id={user_id} with expression='{expression}'")
                return row

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
