from fastapi import FastAPI

from app.api.api import api_router
from app.core.db import GatewayModel, database


app = FastAPI(
    title="FastAPI Elastic Sms Gateway Project",
    description={
        "name": "Jafar Esmaili",
        "url": "http://devcoach.ir",
        "email": "jaffar9898@gmail.com",
    },
    version="0.0.1"
)

app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"FastAPI Sms Gateway Service"}


@app.post("/seed-data")
async def seed_data():
    gateways = await GatewayModel.objects.all()
    if gateways:
        return {"data has been seeded"}
    await GatewayModel.objects.bulk_create([
        GatewayModel(title="ghasedak", token="YOUR_TOKEN", line_number="LINE_NUMBER", active=True, priority=1),
        GatewayModel(title="kavenegar", token="YOUR_TOKEN", line_number="LINE_NUMBER", active=True, priority=2)
    ])
    return {"data has been seeded"}


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()



@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
