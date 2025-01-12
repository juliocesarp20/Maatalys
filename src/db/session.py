from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, Request
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class DatabaseSettings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str
    DATABASE_ENGINE_POOL_SIZE: int
    DATABASE_ENGINE_MAX_OVERFLOW: int
    DATABASE_ENGINE_POOL_PING: bool


settings = DatabaseSettings()

engine: AsyncEngine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_size=settings.DATABASE_ENGINE_POOL_SIZE,
    max_overflow=settings.DATABASE_ENGINE_MAX_OVERFLOW,
    pool_pre_ping=settings.DATABASE_ENGINE_POOL_PING,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, class_=AsyncSession, future=True
)


@asynccontextmanager
async def get_async_session():
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_db_session(request: Request) -> AsyncSession:
    return request.state.db


DbSession = Annotated[AsyncSession, Depends(get_db_session)]
