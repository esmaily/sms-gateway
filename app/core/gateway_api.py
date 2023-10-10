from uuid import uuid4
import random

from app.core.db import GatewayModel
from app.core.gateways.kavenegar import KavenegarGateway
from app.core.gateways.ghasedak import GhasedakGateway


class GatewayApi:
    def __init__(self):
        self.gateway = None
        self.tracking_number = str(uuid4())

    async def init_gateway(self, service_name: str):
        gateway = await GatewayModel.objects.filter(active=True).order_by("priority").first()
        if not gateway:
            return False
        if gateway.title == "kavenegar":
            self.gateway = KavenegarGateway(gateway)
        if gateway.title == "ghasedak":
            self.gateway = GhasedakGateway(gateway)

        return service_name in dir(self.gateway)

    async def send(self, payload: dict):
        answer = {"success": False, "message": "خطای رخ داده هست", "data": None}
        init = await self.init_gateway('send')
        if not init:
            answer["message"] = "سرویس دهنده پشتیبانی نمی کند"
            return answer, 400

        resp = await self.gateway.send(payload)

        json_response = {
            "data": None,
            "success": True if resp else False,
            "message": "ok",
        }
        state_code = 200 if resp else 400

        return json_response, state_code

    async def send_verify(self, payload: dict = {}):
        answer = {"success": False, "message": "خطای رخ داده هست", "data": None}
        init = await self.init_gateway('send_verify')
        if not init:
            answer["message"] = "سرویس دهنده پشتیبانی نمی کند"
            return answer, 400

        resp = await self.gateway.send(payload)

        json_response = {
            "data": None,
            "success": True if resp else False,
            "message": "ok",
        }
        state_code = 200 if resp else 400

        return json_response, state_code


gateway_api = GatewayApi()
