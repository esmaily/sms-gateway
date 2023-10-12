import json
import random
from typing import Annotated, Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Response

from app.core.db import GatewayModel, SmsModel
from app.core.gateway_api import gateway_api


router = APIRouter()


@router.get("/list", response_model=List[SmsModel])
async def sms_list(skip: int = 0, limit: int = 100):
    items = await SmsModel.objects.offset(skip).limit(limit).all()

    return items


@router.post("/send", status_code=200)
async def send_normal(
        mobile: Annotated[str, Body(embed=True, max_length=11)],
        text: Annotated[str, Body(embed=True, max_length=80)],
        response: Response):
    answer, status_code = await  gateway_api.send({
        "text": text,
        "mobile": mobile
    })
    response.status_code = status_code
    return {"success": answer["success"], "message": answer["message"]}


@router.post("/send-verify", status_code=200)
async def send_verify(
        mobile: Annotated[str, Body(embed=True, max_length=11)],
        response: Response):
    otp = random.randint(10000, 99999)
    answer, status_code = await  gateway_api.send_verify(template='register', mobile=mobile, param1=otp)
    response.status_code = status_code

    return {"success": answer["success"], "message": answer["message"]}
