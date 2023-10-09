from fastapi import FastAPI
from app.core.db import database
from app.api.api import api_router

app = FastAPI(title="FastAPI Elastic Example Project")

app.include_router(api_router, prefix="/api")
 


@app.get("/")
async def root():
    return {"FastAPI Sms Gateway Service"}


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # consume_message()
 

@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
