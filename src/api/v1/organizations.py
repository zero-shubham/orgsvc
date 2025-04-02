from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID, uuid4
from datetime import datetime, UTC
from typing import List
from sqlmodel import Session, select
from src.schemas.organizations import OrganizationBase
from src.models.organizations import Organizations
from src.db import get_session
from src.logger import get_request_logger
from structlog.typing import FilteringBoundLogger

org_router = APIRouter()


@org_router.post("/", response_model=OrganizationBase)
async def create_organization(
        name: str,
        session: Session = Depends(get_session),
        logger: FilteringBoundLogger = Depends(get_request_logger)
):
    logger.info("creating organization")
    org = Organizations(
        id=uuid4(),
        name=name,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    session.add(org)
    await session.commit()
    await session.refresh(org)
    logger.info("created organization")
    return org


@org_router.get("/{org_id}", response_model=OrganizationBase)
async def get_organization(org_id: UUID, session: Session = Depends(get_session)):
    org = await session.get(Organizations, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@org_router.get("/", response_model=List[OrganizationBase])
async def list_organizations(session: Session = Depends(get_session)):
    results = await session.exec(select(Organizations))
    return results


@org_router.delete("/{org_id}")
async def delete_organization(org_id: UUID, session: Session = Depends(get_session)):
    org = await session.get(Organizations, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    await session.delete(org)
    await session.commit()
    return {"message": "Organization deleted successfully"}
