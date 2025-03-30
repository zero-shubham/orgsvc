from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from uuid import UUID, uuid4
from datetime import datetime
from typing import List

from app.models.campaigns import Campaigns
from app.db import get_session
from app.schemas.campaigns import CampaignCreate, CampaignResponse

campaign_router = APIRouter()


@campaign_router.post("/", response_model=CampaignResponse)
def create_campaign(
    campaign: CampaignCreate,
    session: Session = Depends(get_session)
):
    db_campaign = Campaigns(
        id=uuid4(),
        name=campaign.name,
        org_id=campaign.org_id,
        start_date=campaign.start_date,
        end_date=campaign.end_date,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    session.add(db_campaign)
    session.commit()
    session.refresh(db_campaign)
    return db_campaign


@campaign_router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(
    campaign_id: UUID,
    session: Session = Depends(get_session)
):
    campaign = session.get(Campaigns, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@campaign_router.get("/", response_model=List[CampaignResponse])
def list_campaigns(
    session: Session = Depends(get_session)
):
    campaigns = session.exec(select(Campaigns)).all()
    return campaigns


@campaign_router.delete("/{campaign_id}")
def delete_campaign(
    campaign_id: UUID,
    session: Session = Depends(get_session)
):
    campaign = session.get(Campaigns, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    session.delete(campaign)
    session.commit()
    return {"message": "Campaign deleted successfully"}
