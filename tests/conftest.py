import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from src.application import app
from src.db import get_session, DATABASE_URL
from httpx import ASGITransport, AsyncClient
# Use in-memory SQLite for testing
# TEST_DATABASE_URL = DATABASE_URL
# engine = create_engine(TEST_DATABASE_URL, echo=False)


# @pytest.fixture(name="session")
# def session_fixture():
#     SQLModel.metadata.create_all(engine)
#     with Session(engine) as session:
#         yield session
#     SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
@pytest.mark.anyio
async def client_fixture():
    # def get_session_override():
    #     yield session

    # app.dependency_overrides[get_session] = get_session_override
    async with AsyncClient(
        transport=ASGITransport(app=app)
    ) as client:
        yield client
    app.dependency_overrides.clear() 