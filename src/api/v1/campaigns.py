from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID, uuid4
from datetime import date, datetime, UTC
from typing import List
from sqlmodel import Session, select
from src.schemas.campaigns import CampaignBase, CampaignCreate, CampaignResponse
from src.models.campaigns import Campaigns
from src.db import get_session

campaigns_router = APIRouter()


@campaigns_router.post("/", response_model=CampaignResponse)
async def create_campaign(
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
    await session.commit()
    await session.refresh(db_campaign)
    return db_campaign


@campaigns_router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: UUID, session: Session = Depends(get_session)):
    campaign = await session.get(Campaigns, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@campaigns_router.get("/", response_model=List[CampaignResponse])
async def list_campaigns(
    session: Session = Depends(get_session)
):
    campaigns = await session.exec(select(Campaigns)).all()
    return campaigns


@campaigns_router.delete("/{campaign_id}")
async def delete_campaign(campaign_id: UUID, session: Session = Depends(get_session)):
    campaign = await session.get(Campaigns, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    session.delete(campaign)
    await session.commit()
    return {"message": "Campaign deleted successfully"}
