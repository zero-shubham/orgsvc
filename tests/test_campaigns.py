import pytest
from uuid import UUID
from datetime import date, timedelta
from src.models.campaigns import Campaigns

@pytest.mark.anyio
async def test_create_campaign(client):
    # First create an organization
    org_response = await client.post("/v1/organizations/", params={"name": "Test Org"})
    print(org_response)
    org_id = org_response.json()["id"]

    # Create campaign data
    start_date = date.today() + timedelta(days=1)
    end_date = start_date + timedelta(days=30)

    response =await  client.post(
        "/v1/campaigns/",
        json={
            "name": "Test Campaign",
            "org_id": str(org_id),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Campaign"
    assert data["org_id"] == str(org_id)
    assert data["start_date"] == start_date.isoformat()
    assert data["end_date"] == end_date.isoformat()
    assert UUID(data["id"])


def test_create_campaign_with_past_start_date(client):
    # First create an organization
    org_response = client.post("/v1/organizations/", params={"name": "Test Org"})
    org_id = org_response.json()["id"]

    # Create campaign data with past start date
    start_date = date.today() - timedelta(days=1)
    end_date = start_date + timedelta(days=30)

    response = client.post(
        "/v1/campaigns/",
        json={
            "name": "Test Campaign",
            "org_id": str(org_id),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
    )
    assert response.status_code == 422  # Validation error


def test_get_campaign(client):
    # Create an organization and campaign
    org_response = client.post("/v1/organizations/", params={"name": "Test Org"})
    org_id = org_response.json()["id"]

    start_date = date.today() + timedelta(days=1)
    end_date = start_date + timedelta(days=30)

    create_response = client.post(
        "/campaigns/",
        json={
            "name": "Test Campaign",
            "org_id": str(org_id),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
    )
    campaign_id = create_response.json()["id"]

    # Get the campaign
    response = client.get(f"/v1/campaigns/{campaign_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Campaign"
    assert data["id"] == campaign_id


def test_get_nonexistent_campaign(client):
    response = client.get("/v1/campaigns/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_list_campaigns(client):
    # Create an organization
    org_response = client.post("/v1/organizations/", params={"name": "Test Org"})
    org_id = org_response.json()["id"]

    # Create multiple campaigns
    start_date = date.today() + timedelta(days=1)
    end_date = start_date + timedelta(days=30)

    client.post(
        "/v1/campaigns/",
        json={
            "name": "Campaign 1",
            "org_id": str(org_id),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
    )
    client.post(
        "/v1/campaigns/",
        json={
            "name": "Campaign 2",
            "org_id": str(org_id),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
    )

    response = client.get("/v1/campaigns/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {c["name"] for c in data} == {"Campaign 1", "Campaign 2"}


def test_delete_campaign(client):
    # Create an organization and campaign
    org_response = client.post("/v1/organizations/", params={"name": "Test Org"})
    org_id = org_response.json()["id"]

    start_date = date.today() + timedelta(days=1)
    end_date = start_date + timedelta(days=30)

    create_response = client.post(
        "/v1/campaigns/",
        json={
            "name": "Test Campaign",
            "org_id": str(org_id),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
    )
    campaign_id = create_response.json()["id"]

    # Delete the campaign
    response = client.delete(f"/v1/campaigns/{campaign_id}")
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/v1/campaigns/{campaign_id}")
    assert get_response.status_code == 404


def test_create_campaign_with_duplicate_name(client):
    # Create an organization
    org_response = client.post("/v1/organizations/", params={"name": "Test Org"})
    org_id = org_response.json()["id"]

    start_date = date.today() + timedelta(days=1)
    end_date = start_date + timedelta(days=30)

    # Create first campaign
    client.post(
        "/v1/campaigns/",
        json={
            "name": "Test Campaign",
            "org_id": str(org_id),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
    )

    # Try to create second campaign with same name
    response = client.post(
        "/v1/campaigns/",
        json={
            "name": "Test Campaign",
            "org_id": str(org_id),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
    )
    assert response.status_code == 400  # Bad request due to duplicate name 