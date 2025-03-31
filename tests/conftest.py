import pytest
from src.application import app
from httpx import ASGITransport, AsyncClient
from src.db import run_migrations, clean_test_db, DATABASE_URL, get_session
import asyncio
import pytest_asyncio


@pytest_asyncio.fixture(scope='session', autouse=True)
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def migrate():
    await run_migrations("./migrations", DATABASE_URL)
    yield
    async for session in get_session():
        await clean_test_db(session)
