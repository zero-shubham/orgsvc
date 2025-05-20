from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID, uuid4
from datetime import date, datetime, UTC
from typing import List
from sqlmodel import Session, select
from src.schemas.campaigns import CampaignCreate, CampaignResponse, CampaignsResp
from src.models.campaigns import Campaigns
from src.db import get_session
from src.logger import get_request_logger
from structlog.typing import FilteringBoundLogger

campaigns_router = APIRouter()


@campaigns_router.post("/", response_model=CampaignResponse)
async def create_campaign(
    campaign: CampaignCreate,
    session: Session = Depends(get_session),
    logger: FilteringBoundLogger = Depends(get_request_logger)
):
    logger.info("creating campaign")
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
    logger.info("created campaign")
    return db_campaign


@campaigns_router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: UUID, session: Session = Depends(get_session)):
    campaign = await session.get(Campaigns, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@campaigns_router.get("/", response_model=CampaignsResp)
async def list_campaigns(
    session: Session = Depends(get_session)
):
    campaigns = await session.exec(select(Campaigns))
    return CampaignsResp(campaigns=campaigns.all())


@campaigns_router.delete("/{campaign_id}")
async def delete_campaign(campaign_id: UUID, session: Session = Depends(get_session)):
    campaign = await session.get(Campaigns, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    session.delete(campaign)
    await session.commit()
    return {"message": "Campaign deleted successfully"}
