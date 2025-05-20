# import pytest
# from uuid import UUID
# from src.models.organizations import Organizations


# @pytest.mark.anyio
# async def test_create_organization(client):
#     response = await client.post("/v1/organizations/", params={"name": "Test Org"})
#     assert response.status_code == 200
#     data = response.json()
#     assert data["name"] == "Test Org"
#     assert UUID(data["id"])  # Verify it's a valid UUID


# @pytest.mark.anyio
# async def test_get_organization(client):
#     # First create an organization
#     create_response = await client.post(
#         "/v1/organizations/", params={"name": "Test Org"})
#     org_id = create_response.json()["id"]

#     # Then get it
#     response = await client.get(f"/organizations/{org_id}")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["name"] == "Test Org"
#     assert data["id"] == org_id


# @pytest.mark.anyio
# async def test_get_nonexistent_organization(client):
#     response = await client.get(
#         "/v1/organizations/00000000-0000-0000-0000-000000000000")
#     assert response.status_code == 404


import pytest
from uuid import UUID
from src.models.organizations import Organizations
from src.application import app
from httpx import ASGITransport, AsyncClient

@pytest.mark.asyncio
async def test_list_organizations():
    async with AsyncClient(
        transport=ASGITransport(app=app, ), base_url="http://test"
    ) as client:
        # Create multiple organizations
        await client.post("/v1/organizations/", params={"name": "Org 1"})
        await client.post("/v1/organizations/", params={"name": "Org 2"})

        response = await client.get("/v1/organizations/")
        assert response.status_code == 200
        data = response.json()
        assert len(data["organizations"]) == 2
        assert {org["name"] for org in data["organizations"]} == {"Org 1", "Org 2"}


# @pytest.mark.anyio
# async def test_delete_organization(client):
#     # First create an organization
#     create_response = await client.post(
#         "/v1/organizations/", params={"name": "Test Org"})
#     org_id = create_response.json()["id"]

#     # Then delete it
#     response = await client.delete(f"/v1/organizations/{org_id}")
#     assert response.status_code == 200

#     # Verify it's deleted
#     get_response = await client.get(f"/v1/organizations/{org_id}")
#     assert get_response.status_code == 404
