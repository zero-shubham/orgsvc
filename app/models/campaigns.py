from sqlmodel import Field, SQLModel
from uuid import UUID
from datetime import date, datetime


class Campaigns(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    name: str = Field(index=True, unique=True)
    org_id: UUID = Field(foreign_key="organizations.id")
    start_date: date = Field(gt=date.today())
    end_date: date = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()
