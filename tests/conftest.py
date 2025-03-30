import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from app.main import app
from app.db import get_session, DATABASE_URL
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
def client_fixture():
    # def get_session_override():
    #     yield session

    # app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear() 