from uuid import uuid4
from app.core.db import GatewayModel
import ghasedakpack
import asyncio
import concurrent.futures


class GhasedakGateway:
    def __init__(self, instance: GatewayModel):
        self.model = instance
        self.tracking_number = str(uuid4())
        self.api = ghasedakpack.Ghasedak(self.model.token)


    async def send(self, mobile: str, message: str):
        params = {
            'receptor': mobile,
            'message': message,
            'linenumber': self.model.line_number,
            'checkid': self.tracking_number
        }

        async def async_send():
            result = await run_in_executor(None, self.api.send, params)
            return result
        async def run_in_executor(executor, fn, *args, **kwargs):
            return await asyncio.to_thread(fn, *args, **kwargs)

        return await async_send()

    async def send_verify(self, payload: dict):
        params = {
            'receptor': payload['mobile'],
            'type': '1',
            'template': payload["mobile"],
            'param1': payload['param1'] if 'param1' in payload else None,
            'param2': payload['param2'] if 'param2' in payload else None,
            'param3': payload['param3'] if 'param3' in payload else None
        }

        async def async_send():
            result = await run_in_executor(None, self.api.verification, params)
            return result

        async def run_in_executor(executor, fn, *args, **kwargs):
            return await asyncio.to_thread(fn, *args, **kwargs)

        return await async_send()

