from app.core.db import GatewayModel
from kavenegar import *


class KavenegarGateway:
    def __init__(self, instance: GatewayModel):
        self.model = instance
        self.tracking_number = str(uuid4())
        self.api = KavenegarAPI(instance.token, timeout=20)

    async def send(self, payload: dict):
        params = {
            'message': payload["text"],
            'receptor': payload["mobile"],
            'sender': 'xxxx',
        }
        response = self.api.sms_send(params)
        return response

    async def send_verify(self, payload: dict):
        params = {
            'receptor': payload["mobile"],
            'template': '',
            'token': '',
            'type': 'sms',  # sms vs call
        }
        response = self.sms_call.verify_lookup(params)
        return response
