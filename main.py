from contextlib import asynccontextmanager
from src.db import init_db, run_migrations
from fastapi import FastAPI
from src.application import app


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
