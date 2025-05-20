from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List


class OrganizationBase(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OrganizationsResp(BaseModel):
    organizations: List[OrganizationBase]
