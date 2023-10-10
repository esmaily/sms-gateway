from uuid import uuid4
from app.core.db import GatewayModel
import ghasedakpack


class GhasedakGateway:
    def __init__(self, instance: GatewayModel):
        self.model = instance
        self.tracking_number = str(uuid4())
        self.api = ghasedakpack.Ghasedak(self.model.token)

    async def send(self, payload: dict):
        params = {
            'message': payload["text"],
            'receptor': payload["mobile"],
            'linenumber': 'xxxx',
            'checkid': self.tracking_number
        }
        response = self.api.send(params)
        return response

    async def send_verify(self, payload: dict):
        params = {
            {'receptor': payload["mobile"], 'type': '1', 'template': 'Your', 'param1': '', 'param2': '', 'param3': ''}
        }
        response = self.api.verification(params)
        return response
