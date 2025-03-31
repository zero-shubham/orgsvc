from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID, uuid4
from datetime import datetime
from typing import List
from sqlmodel import Session, select
from src.schemas.questions import QuestionBase
from src.models.questions import Questions, QuestionTypesEnum
from src.db import get_session

questions_router = APIRouter()


@questions_router.post("/", response_model=QuestionBase)
async def create_question(
    org_id: UUID,
    question_text: str,
    question_type: QuestionTypesEnum,
    options: List[str],
    session: Session = Depends(get_session)
):
    question = Questions(
        id=uuid4(),
        org_id=org_id,
        question_text=question_text,
        question_type=question_type,
        options=options,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    session.add(question)
    await session.commit()
    await session.refresh(question)
    return question


@questions_router.get("/{question_id}", response_model=QuestionBase)
async def get_question(question_id: UUID, session: Session = Depends(get_session)):
    question = await session.get(Questions, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@questions_router.get("/", response_model=List[QuestionBase])
async def list_questions(session: Session = Depends(get_session)):
    results = await session.exec(select(Questions))
    return results.all()


@questions_router.delete("/{question_id}")
async def delete_question(question_id: UUID, session: Session = Depends(get_session)):
    question = await session.get(Questions, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    await session.delete(question)
    await session.commit()
    return {"message": "Question deleted successfully"}
