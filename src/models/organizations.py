from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from datetime import datetime


class Organizations(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    name: str = Field(index=True, unique=True)
    created_at: datetime = Field()
    updated_at: datetime = Field()

    # questions: list["Questions"] = Relationship(back_populates="questions")

    # organizations: list["Organizations"] = Relationship(
    #     back_populates="organizations")
