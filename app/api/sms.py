import json

from typing import Any, List
from app.core.db import SmsModel

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/list", response_model=List[SmsModel])
async def sms_list():
      
     return await SmsModel.objects.all()


# @router.get("/get/{title}", response_model=Article)
# async def article_by_title(title: str):
#     return await Article.objects.filter(title=title).get()


@router.post("/send")
async def send_normal(sms: SmsModel):
    # payload = json.dumps({
    #     "title": article.title,
    #     "content": article.content,
    #     "author": article.author,
    #     "created_at": article.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    #     "updated_at": article.created_at.strftime("%Y-%m-%d %H:%M:%S")
    # })
    """ 
    store articles in rabbit mq queues
    """
 

    return {"success":True,"message":"sms has bee"}

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
 

    return {"success":True,"message":"article has been store in article queue"}


 
