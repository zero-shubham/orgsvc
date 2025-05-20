from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime
from typing import List


class CampaignBase(BaseModel):
    name: str
    org_id: UUID
    start_date: date
    end_date: date


class CampaignCreate(CampaignBase):
    pass


class CampaignResponse(CampaignBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CampaignsResp(BaseModel):
    campaigns: List[CampaignResponse]
