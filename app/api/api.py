from fastapi import APIRouter
from app.api import sms

api_router = APIRouter()
api_router.include_router(sms.router, prefix="/sms")
