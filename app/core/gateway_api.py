from uuid import uuid4
import random

from app.core.db import GatewayModel, SmsModel
from app.core.gateways.kavenegar import KavenegarGateway
from app.core.gateways.ghasedak import GhasedakGateway


class GatewayApi:
    """
        Represents an API for managing and interacting with SMS gateways.

        This class is responsible for initializing a gateway, sending SMS messages, and sending verification codes.
        It supports multiple gateway providers such as Kavenegar and Ghasedak.

        Attributes:
            gateway: An instance of the selected gateway (KavenegarGateway or GhasedakGateway).
            tracking_number (str): A unique tracking number generated for each SMS operation.

        Methods:
            __init__():
                Initializes a new instance of the GatewayApi class.

            init_gateway(service_name: str) -> bool:
                Initializes the selected gateway based on the service name.

                Args:
                    service_name (str): The name of the service to use ('send' or 'send_verify').

                Returns:
                    bool: True if the gateway was successfully initialized, False if no active gateway is available for the service.

            send(payload: dict) -> Tuple[Dict[str, Any], int]:
                Sends an SMS message using the initialized gateway.

                Args:
                    payload (dict): A dictionary containing the following parameters:
                        - 'mobile' (str): The recipient's mobile number.
                        - 'text' (str): The text of the SMS message.

                Returns:
                    Tuple[Dict[str, bool], int]: A tuple containing a response dictionary and an HTTP status code.

            send_verify(**kwargs) -> Tuple[Dict[str, Any], int]:
                Sends a verification SMS using the initialized gateway.

                Keyword Args:
                    **kwargs: A set of keyword arguments containing the following parameters:
                        - 'mobile' (str): The recipient's mobile number.
                        - 'param1' (str): The first parameter for the verification template.

                Returns:
                    Tuple[Dict[str, bol], int]: A tuple containing a response dictionary and an HTTP status code.
    """

    def __init__(self):
        """
            Initializes a new instance of the GatewayApi class.
        """
        self.gateway = None
        self.tracking_number = str(uuid4())

    async def init_gateway(self, service_name: str):
        """
               Initializes the selected gateway based on the service name.

               Args:
                   service_name (str): The name of the service to use ('send' or 'send_verify').

               Returns:
                   bool: True if the gateway was successfully initialized, False if no active gateway is available for the service.

        """

        gateway = await GatewayModel.objects.filter(active=True).order_by("priority").all()

        if not gateway:
            return False
        gateway = gateway[0]
        match gateway.title:
            case "kavenegar":
                self.gateway = KavenegarGateway(gateway)
            case "ghasedak":
                self.gateway = GhasedakGateway(gateway)
            case _:
                self.gateway = GhasedakGateway(gateway)

        return service_name in dir(self.gateway)

    async def send(self, payload: dict):
        """
           Sends an SMS message using the initialized gateway.

           Args:
               payload (dict): A dictionary containing the following parameters:
                   - 'mobile' (str): The recipient's mobile number.
                   - 'text' (str): The text of the SMS message.

           Returns:
               Tuple[Dict[str, bool], int]: A tuple containing a response dictionary and an HTTP status code.

        """
        answer = {"success": False, "message": "خطای رخ داده هست"}
        init = await self.init_gateway('send')
        if not init:
            answer["message"] = "سرویس دهنده پشتیبانی نمی کند"
            return answer, 400

        resp = await self.gateway.send(payload["mobile"], payload["text"])

        json_response = {
            "data": None,
            "success": True if resp else False,
            "message": "ok",
        }
        state_code = 200 if resp else 400

        """ 
            store articles in rabbit mq queues
        """
        sms_object = SmsModel(mobile=payload['mobile'], text=payload['text'], gateway=self.gateway.model.id)
        await sms_object.save()
        return json_response, state_code

    async def send_verify(self, **kwargs):
        """
            Sends a verification SMS using the initialized gateway.

            Keyword Args:
                **kwargs: A set of keyword arguments containing the following parameters:
                    - 'mobile' (str): The recipient's mobile number.
                    - 'param1' (str): The first parameter for the verification template.

            Returns:
                Tuple[Dict[str, bool], int]: A tuple containing a response dictionary and an HTTP status code.

        """

        answer = {"success": False, "message": "خطای رخ داده هست", "data": None}
        init = await self.init_gateway('send_verify')
        if not init:
            answer["message"] = "سرویس دهنده پشتیبانی نمی کند"
            return answer, 400
        resp = await self.gateway.send_verify(kwargs)

        json_response = {
            "data": None,
            "success": True if resp else False,
            "message": "ok",
        }
        state_code = 200 if resp else 400
        sms_object = SmsModel(mobile=kwargs['mobile'], text=kwargs['param1'], gateway=self.gateway.model.id)
        await sms_object.save()
        return json_response, state_code


gateway_api = GatewayApi()
