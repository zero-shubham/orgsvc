from typing import AsyncGenerator

from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.orm import sessionmaker
from src.config import DATABASE_URL


connect_args = {"check_same_thread": True}

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# test_engine = create_engine(app_config.DATABASE_URL, pool_pre_ping=True)
# TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
