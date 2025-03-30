import pytest
from uuid import UUID
from app.models.questions import Questions, QuestionTypesEnum


def test_create_question(client):
    # First create an organization
    org_response = client.post("/v1/organizations/", params={"name": "Test Org"})
    org_id = org_response.json()["id"]

    # Then create a question
    response = client.post(
        "/v1/questions/",
        params={
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


def test_get_question(client):
    # Create an organization and question
    org_response = client.post("/v1/organizations/", params={"name": "Test Org"})
    org_id = org_response.json()["id"]

    create_response = client.post(
        "/v1/questions/",
        params={
            "org_id": org_id,
            "question_text": "What is your name?",
            "question_type": QuestionTypesEnum.descriptive,
            "options": []
        }
    )
    question_id = create_response.json()["id"]

    # Get the question
    response = client.get(f"/v1/questions/{question_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["question_text"] == "What is your name?"
    assert data["id"] == question_id


def test_get_nonexistent_question(client):
    response = client.get("/v1/questions/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_list_questions(client):
    # Create an organization
    org_response = client.post("/v1/organizations/", params={"name": "Test Org"})
    org_id = org_response.json()["id"]

    # Create multiple questions
    client.post(
        "/v1/questions/",
        params={
            "org_id": org_id,
            "question_text": "Question 1",
            "question_type": QuestionTypesEnum.descriptive,
            "options": []
        }
    )
    client.post(
        "/v1/questions/",
        params={
            "org_id": org_id,
            "question_text": "Question 2",
            "question_type": QuestionTypesEnum.multiple_choice,
            "options": ["A", "B", "C"]
        }
    )

    response = client.get("/v1/questions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {q["question_text"] for q in data} == {"Question 1", "Question 2"}


def test_delete_question(client):
    # Create an organization and question
    org_response = client.post("/v1/organizations/", params={"name": "Test Org"})
    org_id = org_response.json()["id"]

    create_response = client.post(
        "/v1/questions/",
        params={
            "org_id": org_id,
            "question_text": "What is your name?",
            "question_type": QuestionTypesEnum.descriptive,
            "options": []
        }
    )
    question_id = create_response.json()["id"]

    # Delete the question
    response = client.delete(f"/v1/questions/{question_id}")
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/v1/questions/{question_id}")
    assert get_response.status_code == 404 