from fastapi import FastAPI
from fastapi.testclient import TestClient
# from starlette.testclient import TestClient.
from typing import Any, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.db import SmsModel
from app.main import app,database
from app.core.db import BaseMeta


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_app_db.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


BaseMeta.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[database] = override_get_db

client = TestClient(app)

def test_sms_list():

    # response = client.get("/api/sms/list")
    with client as cl:
        response = cl.get("/api/sms/list")
        assert response.status_code == 200
        # items = [SmsModel(**item) for item in response.json()]
        # assert items[0].mobile == "09385137677"


def test_sms_send():
    with client as cl:
        response = client.post("/api/sms/send", json={"mobile": "09385137677", "text": "hi jafar"})
        assert response.status_code == 200
        assert response.json() == {"success": False, "message": "ok"}

def test_sms_send_verify():
    with client as cl:
        response = client.post("/api/sms/send-verify", json={"mobile": "09385137677"})
        assert response.status_code == 200
        assert response.json() == {"success": True, "message": "ok"}
