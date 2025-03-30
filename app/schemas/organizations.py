from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class OrganizationBase(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
