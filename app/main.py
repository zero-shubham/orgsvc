from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import init_db
from app.api import api_router

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app.include_router(api_router)
