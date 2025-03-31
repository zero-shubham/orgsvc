from fastapi import APIRouter
from .campaigns import campaigns_router
from .organizations import org_router
from .questions import questions_router

apiv1_router = APIRouter()

apiv1_router.include_router(
    campaigns_router, prefix="/campaigns", tags=["campaigns"])
apiv1_router.include_router(
    org_router, prefix="/organizations", tags=["organizations"])
apiv1_router.include_router(
    questions_router, prefix="/questions", tags=["questions"])
