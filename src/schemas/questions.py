from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List
from src.models.questions import QuestionTypesEnum


class QuestionBase(BaseModel):
    org_id: UUID
    question_text: str
    question_type: QuestionTypesEnum
    options: List[str]


class QuestionCreate(QuestionBase):
    pass


class QuestionResponse(QuestionBase):
    created_at: datetime
    updated_at: datetime
    id: UUID

    class Config:
        from_attributes = True


class QuestionsResp(BaseModel):
    questions: List[QuestionResponse]
