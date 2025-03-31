from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text


from .v1 import apiv1_router

api_router = APIRouter()

api_router.include_router(apiv1_router, prefix="/v1")
