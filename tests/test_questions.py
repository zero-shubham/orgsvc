import pytest
from uuid import UUID
from src.models.questions import Questions, QuestionTypesEnum
from src.application import app
from httpx import ASGITransport, AsyncClient

@pytest.mark.asyncio
async def test_create_question():
    async with AsyncClient(
        transport=ASGITransport(app=app, ), base_url="http://test"
    ) as client:
        # First create an organization
        org_response = await client.post("/v1/organizations/", params={"name": "Test Org"})
        org_id = org_response.json()["id"]

        # Then create a question
        response = await client.post(
            "/v1/questions/",
            json={
                "org_id": org_id,
                "question_text": "What is your name?",
                "question_type": QuestionTypesEnum.descriptive,
                "options": []
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["question_text"] == "What is your name?"
        assert data["question_type"] == QuestionTypesEnum.descriptive
        assert data["options"] == []
        assert UUID(data["id"])


@pytest.mark.asyncio
async def test_get_question():
    async with AsyncClient(
        transport=ASGITransport(app=app, ), base_url="http://test"
    ) as client:
        # Create an organization and question
        org_response = await client.post("/v1/organizations/", params={"name": "Test Org"})
        org_id = org_response.json()["id"]

        create_response = await client.post(
            "/v1/questions/",
            json={
                "org_id": org_id,
                "question_text": "What is your name?",
                "question_type": QuestionTypesEnum.descriptive,
                "options": []
            }
        )
        question_id = create_response.json()["id"]

        # Get the question
        response = await client.get(f"/v1/questions/{question_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["question_text"] == "What is your name?"
        assert data["id"] == question_id


# @pytest.mark.anyio
# async def test_get_nonexistent_question(client):
#     response = await client.get("/v1/questions/00000000-0000-0000-0000-000000000000")
#     assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_questions():
    async with AsyncClient(
        transport=ASGITransport(app=app, ), base_url="http://test"
    ) as client:
        # Create an organization
        org_response = await client.post(
            "/v1/organizations/", params={"name": "Test Org"})
        org_id = org_response.json()["id"]

        # Create multiple questions
        await client.post(
            "/v1/questions/",
            json={
                "org_id": org_id,
                "question_text": "Question 1",
                "question_type": QuestionTypesEnum.descriptive,
                "options": []
            }
        )
        await client.post(
            "/v1/questions/",
            json={
                "org_id": org_id,
                "question_text": "Question 2",
                "question_type": QuestionTypesEnum.multiple_choice,
                "options": ["A", "B", "C"]
            }
        )

        response = await client.get("/v1/questions/")
        assert response.status_code == 200
        data = response.json()
        assert len(data["questions"]) == 2
        assert {q["question_text"] for q in data["questions"]} == {"Question 1", "Question 2"}


@pytest.mark.asyncio
async def test_delete_question():
    async with AsyncClient(
        transport=ASGITransport(app=app, ), base_url="http://test"
    ) as client:
        # Create an organization and question
        org_response = await client.post(
            "/v1/organizations/", params={"name": "Test Org"})
        org_id = org_response.json()["id"]

        create_response = await client.post(
            "/v1/questions/",
            json={
                "org_id": org_id,
                "question_text": "What is your name?",
                "question_type": QuestionTypesEnum.descriptive,
                "options": []
            }
        )
        question_id = create_response.json()["id"]

        # Delete the question
        response = await client.delete(f"/v1/questions/{question_id}")
        assert response.status_code == 200

        # Verify it's deleted
        get_response = await client.get(f"/v1/questions/{question_id}")
        assert get_response.status_code == 404
