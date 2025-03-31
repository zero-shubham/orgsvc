from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db import init_db
from src.api import api_router

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app.include_router(api_router)
