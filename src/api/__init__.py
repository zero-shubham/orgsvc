from fastapi import APIRouter
from .v1 import apiv1_router

api_router = APIRouter()

api_router.include_router(apiv1_router, prefix="/v1")
