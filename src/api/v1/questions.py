from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID, uuid4
from datetime import datetime
from typing import List
from sqlmodel import Session, select
from src.schemas.questions import QuestionResponse, QuestionsResp,QuestionCreate
from src.models.questions import Questions, QuestionTypesEnum
from src.db import get_session

questions_router = APIRouter()


@questions_router.post("/", response_model=QuestionResponse)
async def create_question(
    question: QuestionCreate,
    session: Session = Depends(get_session)
):
    question = Questions(
        id=uuid4(),
        org_id=question.org_id,
        question_text=question.question_text,
        question_type=question.question_type,
        options=question.options,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    session.add(question)
    await session.commit()
    await session.refresh(question)
    return question


@questions_router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: UUID, session: Session = Depends(get_session)):
    question = await session.get(Questions, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@questions_router.get("/", response_model=QuestionsResp)
async def list_questions(session: Session = Depends(get_session)):
    results = await session.exec(select(Questions))
    return QuestionsResp(questions=results.all())


@questions_router.delete("/{question_id}")
async def delete_question(question_id: UUID, session: Session = Depends(get_session)):
    question = await session.get(Questions, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    await session.delete(question)
    await session.commit()
    return {"message": "Question deleted successfully"}
