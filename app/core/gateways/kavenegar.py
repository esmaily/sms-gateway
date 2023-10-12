from uuid import uuid4
import asyncio
from app.core.db import GatewayModel
from kavenegar import APIException, HTTPException, KavenegarAPI


class KavenegarGateway:
    """
       Represents a gateway for sending SMS messages using the Kavenegar service.

       This class provides methods for sending SMS messages and verifying phone numbers using the Kavenegar API.

       Attributes:
           model (GatewayModel): An instance of the GatewayModel representing the configuration of the gateway.
           tracking_number (str): A unique tracking number generated for each SMS operation.
           api (KavenegarAPI): An instance of the KavenegarAPI for interacting with the Kavenegar service.

       Methods:
           send(mobile: str, message: str) -> bool:
               Sends an SMS message to the specified mobile number.

               Args:
                   mobile (str): The recipient's mobile number.
                   message (str): The text of the SMS message.

               Returns:
                   bool: True if the message was successfully sent, False if there was an error.

           send_verify(payload: dict) -> bool:
               Sends a verification SMS using a predefined template.

               Args:
                   payload (dict): A dictionary containing the following parameters:
                       - 'mobile' (str): The recipient's mobile number.
                       - 'template' (str): The name of the template to use.
                       - 'param1' (str, optional): The first parameter for the template.
                       - 'param2' (str, optional): The second parameter for the template.
                       - 'param3' (str, optional): The third parameter for the template.

               Returns:
                   bool: True if the verification SMS was successfully sent, False if there was an error.

       """
    def __init__(self, instance: GatewayModel):
        """
               Initializes a new instance of the KavenegarGateway class.

               Args:
                   instance (GatewayModel): An instance of GatewayModel representing the configuration of the gateway.

        """
        self.model = instance
        self.tracking_number = str(uuid4())
        self.api = KavenegarAPI(instance.token)

    async def send(self, mobile: str, message: str):
        """
               Sends an SMS message to the specified mobile number.

               Args:
                   mobile (str): The recipient's mobile number.
                   message (str): The text of the SMS message.

               Returns:
                   bool: True if the message was successfully sent, False if there was an error.

        """
        params = {
            'sender': self.model.line_number,
            'receptor': mobile,
            'message': message
        }

        async def async_send():
            result = await run_in_executor(None, self.api.sms_send, params)
            return result

        async def run_in_executor(executor, fn, *args, **kwargs):
            return await asyncio.to_thread(fn, *args, **kwargs)

        return await async_send()

    async def send_verify(self, payload: dict):
        """
                Sends a verification SMS using a predefined template.

                Args:
                    payload (dict): A dictionary containing the following parameters:
                        - 'mobile' (str): The recipient's mobile number.
                        - 'template' (str): The name of the template to use.
                        - 'param1' (str, optional): The first parameter for the template.
                        - 'param2' (str, optional): The second parameter for the template.
                        - 'param3' (str, optional): The third parameter for the template.

                Returns:
                    bool: True if the verification SMS was successfully sent, False if there was an error.

        """

        params = {
            'receptor': payload['mobile'],
            'template': payload['template'],
            'token': payload['param1'] if 'param1' in payload else None,
            'token2': payload['param2'] if 'param2' in payload else None,
            'token3': payload['param3'] if 'param3' in payload else None,
            'token10': None,
            'token20': None,
        }

        async def async_send():
            result = await run_in_executor(None, self.api.verify_lookup, params)
            return result

        async def run_in_executor(executor, fn, *args, **kwargs):
            return await asyncio.to_thread(fn, *args, **kwargs)

        return await async_send()

