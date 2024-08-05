import requests
from typing import Dict
import base64
from rakuten.models import Result
import xmltojson
from io import StringIO
import json
import csv

class RestAdapter:
    def __init__(self, host: str, client_id: str, client_secret: str, account_id: int):
        self.host = host
        self.client_id = client_id
        self.client_secret = client_secret
        self.account_id = account_id
        self.token_key = base64.b64encode(
            f'{client_id}:{client_secret}'.encode('utf-8')
        ).decode('utf-8')
        self.access_token = None

    def _do(
            self,
            return_type: str,
            http_method: str,
            endpoint: str,
            params: Dict = None,
            data: Dict = None,
            is_auth: bool = False,
            is_json: bool = False,
    ) -> Result:
        url = f"{self.host}{endpoint}"
        if is_auth:
            # Get our access token
            headers = {
                'Authorization': f'Bearer {self.token_key}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'scope': self.account_id
            }
        else:
            if self.access_token is None:
                raise Exception("access_token is None. Authenticate first.")
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
        if is_json:
            response = requests.request(
                method=http_method,
                url=url, headers=headers,
                params=params,
                json=data
            )
        else:
            response = requests.request(
                method=http_method,
                url=url, headers=headers,
                params=params,
                data=data
            )
        # Some APIs return XML whereas others return JSON
        # Quick check to see what we're dealing with here
        # TODO: Make this more robust or tag individual APIs with their datatype
        text = response.text
        match return_type:
            case "json":
                try:
                    response_data = response.json()
                except json.JSONDecodeError:
                    raise Exception(text)
            case "xml":
                try:
                    mem_file = StringIO(response.text)
                    response_data = json.loads(xmltojson.parse(mem_file.read()))
                except Exception as e:
                    raise Exception(e, text)
            case "csv":
                response_data = response.text
        # if text.startswith("<") and not text.startswith("{"):
        #     mem_file = StringIO(text)
        #     response_data = json.loads(xmltojson.parse(mem_file.read()))
        # else:
        #     try:
        #         response_data = response.json()
        #     except json.JSONDecodeError:
        #         raise Exception(text)
        if response.status_code >= 200 and response.status_code <= 299:
            return Result(response.status_code, message=response.reason, data=response_data)
        raise Exception(response_data)
  
    def post(
        self,
        endpoint: str,
        params: Dict = None,
        data: Dict = None,
        is_auth: bool = False,
        is_json: bool = False
    ):
        return self._do(
            http_method="POST",
            endpoint=endpoint,
            params=params,
            data=data,
            is_auth=is_auth,
            is_json=is_json
        )

    def get(self, endpoint: str, params: Dict = None, return_type="json"):
        return self._do(
            http_method="GET",
            endpoint=endpoint,
            params=params,
            return_type=return_type
        )
   
    def delete(
        self,
        endpoint: str,
        params: Dict = None,
        data: Dict = None,
        return_type="json"
    ):
        return self._do(http_method="GET", endpoint=endpoint, data=data, return_type=return_type)

    def get_token(self):
        response = self.post(endpoint="/token", is_auth=True, return_type="json")
        self.access_token = response.data["access_token"]
        return response
    