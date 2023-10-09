from uuid import uuid4
import random

from app.core.db import GatewayModel
from app.core.gateways.kavenegar import KavenegarGateway
from app.core.gateways.ghasedak import GhasedakGateway
 


class GatewayApi:
    def __init__(self, **kwargs):
        self.gateway = None
        self.tracking_number = str(uuid4())

    def init_gateway(self):
        gateway = GatewayModel.objects.filter(status=True, types__key=bill_type.rstrip("_bill")).order_by(
            "-priority").last()
        if not gateway:
            return False
        if gateway.title == "kavenegar":
            self.gateway = KavenegarGateway(gateway)
        if gateway.title == "ghasedak":
            self.gateway = GhasedakGateway(gateway)
      
        return True

    def send(self, payload: dict):
        answer = {"success": False, "msg": "خطای رخ داده هست"}
        
        if not self.init_gateway():
            answer["msg"] = "سرویس دهنده پشتیبانی نمی کند"
            return answer, 400
        
        resp = self.gateway.send()
        json_response = {
            "data": resp["data"] if resp["success"] else None,
            "success": resp["success"],
            "message": resp["msg"],
        }
        state_code = 200 if resp["success"] else 400

        return json_response, state_code

    def send_verify(self,   payload: dict = {}):
        answer = {"success": False, "msg": "خطای رخ داده هست"}
        if not self.has_support_bill_type(bill_type):
            answer["msg"] = "سرویس دهنده پشتیبانی نمی کند"
            return answer, 400

        bill_type = f"pay_{bill_type}_bill"
        resp = getattr(self.provider, bill_type)(payload)
        json_response = {
            "data": resp["data"],
            "success": resp["success"],
            "message": resp["msg"],
        }
        state_code = 200 if resp["success"] else 400

        return json_response, state_code
 