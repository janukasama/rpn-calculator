import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.utils.config import ConfigLoader


def get_async_engine():
    """
    Create an asynchronous SQLAlchemy engine.

    return:
        Engine: An asynchronous SQLAlchemy engine instance.
    """
    return create_async_engine(
        url=get_async_db_url(),  # Database connection string
        pool_size=5,  # Each replica holds up to 5 persistent connections
        max_overflow=10,  # Allows temporary connections if demand spikes
        pool_recycle=300,  # Recycle connections every 5 minutes
        pool_pre_ping=True,  # Ensure dead connections are replaced
        pool_use_lifo=True  # Reuse most recently used connections first
    )


# Create a sessionmaker for asynchronous sessions
AsyncSessionLocal = sessionmaker(bind=get_async_engine(), expire_on_commit=False, class_=AsyncSession)


async def get_async_db_session() -> AsyncSession:
    """
    Get an asynchronous database session.

    yield:
        AsyncSession: An asynchronous SQLAlchemy session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session  # Yield the session to the caller
        except Exception:
            await session.rollback()  # Rollback the transaction in case of an error
            raise
        finally:
            await session.close()  # Ensure the session is closed


def get_async_db_url() -> str:
    """
        Generate a async database connection.

        return:
            str: The formatted database connection string.
    """
    config = ConfigLoader.load()
    try:
        return (
            f'postgresql+asyncpg://{os.environ.get("POSTGRES_USER")}:{os.environ.get("POSTGRES_PASSWORD")}'
            f'@{config.tender_db.host}:{config.tender_db.port}/'
            f'{config.tender_db.database}'
        )
    except Exception as e:
        raise Exception(str(e))


def get_sync_db_url():
    """
        Generate a sync database connection for alembic.

        return:
            str: The formatted database connection string.
    """
    config = ConfigLoader.load()
    try:
        return (
            f'postgresql+psycopg2://{os.environ.get("POSTGRES_USER")}:{os.environ.get("POSTGRES_PASSWORD")}'
            f'@{config.tender_db.host}:{config.tender_db.port}/'
            f'{config.tender_db.database}'
        )
    except Exception as e:
        raise Exception(str(e))
