from fastapi import FastAPI
from src.api import api_router
from contextlib import asynccontextmanager
from src.db import init_db, run_migrations, DATABASE_URL
from time import sleep
from src.logger import get_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    sleep(5)
    await init_db()
    get_logger().info("running migrations..")
    try:
        await run_migrations("./migrations", DATABASE_URL)
    except Exception as e:
        get_logger().info("failed to migrate..", exception=e)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
