from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List
from src.models.questions import QuestionTypesEnum


class QuestionBase(BaseModel):
    id: UUID
    org_id: UUID
    question_text: str
    question_type: QuestionTypesEnum
    options: List[str]
    created_at: datetime
    updated_at: datetime


class QuestionsResp(BaseModel):
    questions: List[QuestionBase]
