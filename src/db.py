from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import command
from alembic.config import Config
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from src.config import DATABASE_URL

alembic_cfg = Config()

connect_args = {"check_same_thread": True}

engine = create_async_engine(DATABASE_URL, echo=True, future=True)


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


async def run_migrations(script_location: str, dsn: str) -> None:
    alembic_cfg.set_main_option("script_location", script_location)
    alembic_cfg.set_main_option("sqlalchemy.url", dsn)

    async with engine.begin() as conn:
        await conn.run_sync(__execute_upgrade)


def __execute_upgrade(connection):
    alembic_cfg.attributes["connection"] = connection
    command.upgrade(alembic_cfg, "head")


async def clean_test_db(session) -> None:
    await session.execute(text("DELETE from questions"))
    await session.execute(text("DELETE from campaigns"))
    await session.execute(text("DELETE from organizations"))
    await session.commit()
