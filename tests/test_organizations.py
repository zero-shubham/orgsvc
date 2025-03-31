import pytest
from uuid import UUID
from src.models.organizations import Organizations


def test_create_organization(client):
    response = client.post("/v1/organizations/", params={"name": "Test Org"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Org"
    assert UUID(data["id"])  # Verify it's a valid UUID


def test_get_organization(client):
    # First create an organization
    create_response = client.post("/v1/organizations/", params={"name": "Test Org"})
    org_id = create_response.json()["id"]

    # Then get it
    response = client.get(f"/organizations/{org_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Org"
    assert data["id"] == org_id


def test_get_nonexistent_organization(client):
    response = client.get("/v1/organizations/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_list_organizations(client):
    # Create multiple organizations
    client.post("/v1/organizations/", params={"name": "Org 1"})
    client.post("/v1/organizations/", params={"name": "Org 2"})

    response = client.get("/v1/organizations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {org["name"] for org in data} == {"Org 1", "Org 2"}


def test_delete_organization(client):
    # First create an organization
    create_response = client.post("/v1/organizations/", params={"name": "Test Org"})
    org_id = create_response.json()["id"]

    # Then delete it
    response = client.delete(f"/v1/organizations/{org_id}")
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/v1/organizations/{org_id}")
    assert get_response.status_code == 404 