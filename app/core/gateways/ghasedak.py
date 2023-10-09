

class GhasedakGateway:
    def __init__(self,instance: GatewayModel ):
        self.model = instance
        self.headers = {
            'Accept-Language': "fa",
            'cache-control': "no-cache",
        }

    def send_request(self, path_url, payload):
        url = FARABOOM['url'] + path_url
        api_call = APICall(provider_type.FARABOOM_BILL_INQUIRY)
        try:
            response = api_call.rest_request(
                url=url, method='post', json=payload, headers=self.headers, timeout=FARABOOM_TIMEOUT, verify=False)
            if response.status_code == 200:
                response = api_call.json_serializer(answer=response)
                success = True
                state = GeneralStatusCode.SUCCESS
            else:
                json_resp = api_call.json_serializer(answer=response)
                response = json_resp['errors'][0]
                state = faraboom_error_codes.get(response.get('code', {}), FaraboomStatusCodes.FARABOOM_UNKNOWN_ERROR)
                success = False
            return response, success, state
        except Exception as e:
            from gpay import tasks
            tasks.send_provider_alarm.delay(
                is_transaction=False,
                service_name=provider_type.FARABOOM_BILL_INQUIRY,
                message=str(e),
                response=str(e),
                title=BillStatusCodes.BILL_INQUIRY_SERVICE_EXCEPTION.message
            )
            return {'exception': str(e)}, False, GeneralStatusCode.PROVIDER_IS_NOT_AVAILABLE

    def send(self, **kwargs):
        payload = {
            "bill_id": kwargs['bill_id']
        }
        response = self.send_request(path_url="vas/tavanir/bills", payload=payload)
        self.recording_request(type='electricity', data=payload, response=response)
        return response

    def send_verify(self, **kwargs):
        payload = {
            "bill_id": kwargs['bill_id']
        }
        response = self.send_request(path_url="vas/abfa/bills", payload=payload)
        self.recording_request(type='abfa', data=payload, response=response)
        return response

  