import urllib.parse

import boto3
import requests
from warrant.aws_srp import AWSSRP

from .const import API_KEY, BASE_URL, CLIENT_ID, POOL_ID, REGION, USER_AGENT


class Phyn:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        client = boto3.client("cognito-idp", region_name=REGION)
        aws = AWSSRP(
            username=self.username,
            password=self.password,
            pool_id=POOL_ID,
            client_id=CLIENT_ID,
            client=client,
        )
        tokens = aws.authenticate_user()
        return tokens["AuthenticationResult"]["AccessToken"]

    def _http_headers(self):
        return {
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
            "Connection": "keep-alive",
            "x-api-key": API_KEY,
            "Accept": "application/json",
            "Authorization": self.access_token,
            "Accept-Encoding": "gzip, deflate, br",
        }

    def session_startup(self):
        resp = requests.post(
            f"{BASE_URL}/users/accounts%40chrisbarrett.com/session_startup/App",
            headers=self._http_headers(),
        )
        return resp.json()

    def homes(self):
        resp = requests.get(
            f"{BASE_URL}/homes?user_id={urllib.parse.quote(self.username)}",
            headers=self._http_headers(),
        )
        return resp.json()

    def state(self, device_id):
        homes = self.homes()
        device_ids = homes[0].get("device_ids")
        resp = requests.get(
            f"{BASE_URL}/devices/{device_id}/state",
            headers=self._http_headers(),
        )
        return resp.json()
