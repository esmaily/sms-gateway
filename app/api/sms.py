import json

from typing import Any, List
from app.core.db import SmsModel, GatewayModel
from app.core.gateway_api import gateway_api
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/list", response_model=List[SmsModel])
async def sms_list():
    return await SmsModel.objects.all()


@router.post("/send")
async def send_normal(sms: SmsModel):
    res, ct = await  gateway_api.send(sms)
    """ 
    store articles in rabbit mq queues
    """
    # response, status_code
    print(sms.mobile)
    return {"success": True, "message": "sms has been send"}


@router.post("/send-verify")
async def send_verify(article: SmsModel):
    payload = json.dumps({
        "title": article.title,
        "content": article.content,
        "author": article.author,
        "created_at": article.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": article.created_at.strftime("%Y-%m-%d %H:%M:%S")
    })
    """ 
    store articles in rabbit mq queues
    """
    res, ct = await  gateway_api.send_verify(sms)

    return {"success": True, "message": "sms has been send"}
