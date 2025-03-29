from sqlmodel import Field, SQLModel
from uuid import UUID
from datetime import datetime
import enum
from typing import List
from sqlalchemy import Column, Enum, ARRAY, String


class QuestionTypesEnum(str, enum.Enum):
    descriptive = "descriptive"
    multiple_choice = "multiple_choice"
    multiple_option = "multiple_option"


class Questions(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    org_id: UUID = Field(foreign_key="organizations.id")
    question_text: str = Field()
    question_type: QuestionTypesEnum = Field(
        sa_column=Column(Enum(QuestionTypesEnum)))
    options: List[str] = Field(sa_column=Column(ARRAY(String)))
    created_at: datetime = Field()
    updated_at: datetime = Field()
