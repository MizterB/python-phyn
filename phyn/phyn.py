import secrets
from datetime import date
from urllib.parse import quote_plus

import boto3
import requests
from pycognito.aws_srp import AWSSRP

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

    def homes(self):
        resp = requests.get(
            f"{BASE_URL}/homes?user_id={requests.utils.quote(self.username)}",
            headers=self._http_headers(),
        )
        return resp.json()

    def users_session_startup(self):
        resp = requests.post(
            f"{BASE_URL}/users/{requests.utils.quote(self.username)}/session_startup/App",
            headers=self._http_headers(),
        )
        return resp.json()

    def users_iot_policy(self):
        resp = requests.post(
            f"{BASE_URL}/users/{requests.utils.quote(self.username)}/iot_policy",
            headers=self._http_headers(),
        )
        return resp.json()

    def users_devices(self):
        resp = requests.get(
            f"{BASE_URL}/users/{requests.utils.quote(self.username)}/devices/v2?product_group=phyn",
            headers=self._http_headers(),
        )
        return resp.json()

    def config_app_phyn_app(self):
        resp = requests.get(
            f"{BASE_URL}/config/APP/PHYN_APP",
            headers=self._http_headers(),
        )
        return resp.json()

    def users_config_app_phyn_app(self):
        resp = requests.get(
            f"{BASE_URL}/config/ML/PRESSURE_RANGE",
            headers=self._http_headers(),
        )
        return resp.json()

    def devices_auto_shutoff(self, device_id):
        resp = requests.get(
            f"{BASE_URL}/devices/{device_id}/auto_shutoff",
            headers=self._http_headers(),
        )
        return resp.json()

    def devices_consumption_details(
        self,
        device_id,
        duration=date.today().strftime("%Y/%m/%d"),
        details="Y",
        event_count=None,
        comparison=None,
        precision=6,
    ):
        """
        duration=5/2022 (url-encoded, required)
        details=Y (optional)
        event_count=Y (optional)
        comparison=Y (optional)
        precision=6 (required)
        """
        resp = requests.get(
            f"{BASE_URL}/devices/{device_id}/consumption/details?duration={quote_plus(duration)}&details={details}&event_count={event_count}&comparison={comparison}&precision={precision}",
            headers=self._http_headers(),
        )
        return resp.json()

    def devices_health_tests(self, device_id, health_test_id):
        resp = requests.get(
            f"{BASE_URL}/devices/{device_id}/health_tests/{health_test_id}",
            headers=self._http_headers(),
        )
        return resp.json()

    def devices_health_tests_active(self, device_id):
        resp = requests.get(
            f"{BASE_URL}/devices/{device_id}/health_tests/active",
            headers=self._http_headers(),
        )
        return resp.json()

    def devices_health_tests_success(self, device_id):
        resp = requests.get(
            f"{BASE_URL}/devices/{device_id}/health_tests?is_success=true",
            headers=self._http_headers(),
        )
        return resp.json()

    def devices_state(self, device_id):
        resp = requests.get(
            f"{BASE_URL}/devices/{device_id}/state",
            headers=self._http_headers(),
        )
        return resp.json()

    def devices_sov_close(self, device_id):
        resp = requests.post(
            f"{BASE_URL}/devices/{device_id}/sov/Close",
            headers=self._http_headers(),
        )
        return resp.json()

    def devices_auto_shutoff(self, device_id):
        resp = requests.get(
            f"{BASE_URL}/devices/{device_id}/auto_shutoff",
            headers=self._http_headers(),
        )
        return resp.json()

    def devices_auto_shutoff_status_disable(self, device_id, seconds=None):
        if seconds:
            url_seconds = f"/{seconds}"
        resp = requests.post(
            f"{BASE_URL}/devices/{device_id}/auto_shutoff/status/Disable{seconds}",
            headers=self._http_headers(),
        )
        return resp.json()

    def devices_auto_shutoff_status_enable(self, device_id):
        resp = requests.post(
            f"{BASE_URL}/devices/{device_id}/auto_shutoff/status/Enable",
            headers=self._http_headers(),
        )
        return resp.json()

    def devices_sov_open(self, device_id):
        resp = requests.post(
            f"{BASE_URL}/devices/{device_id}/sov/Open",
            headers=self._http_headers(),
        )
        return resp.json()

    def home_inventory_device(self, device_id):
        resp = requests.get(
            f"{BASE_URL}/home-inventory/device/{device_id}",
            headers=self._http_headers(),
        )
        return resp.json()

    def home_inventory_types(self):
        resp = requests.get(
            f"{BASE_URL}/home-inventory/types",
            headers=self._http_headers(),
        )
        return resp.json()

    def water_usage_events(self, device_id, from_ts, to_ts):
        """
        from_ts=1653364800557
        to_ts=1653451199999
        """
        resp = requests.get(
            f"{BASE_URL}/water-usage-events?device_id={device_id}&from_ts={from_ts}&to_ts={to_ts}",
            headers=self._http_headers(),
        )
        return resp.json()

    def preferences_device(self, device_id):
        resp = requests.get(
            f"{BASE_URL}/preferences/device/{device_id}",
            headers=self._http_headers(),
        )
        return resp.json()

    def preferences_device_away_mode_disable(self, device_id):
        data = [
            {
                "name": "leak_sensitivity_away_mode",
                "value": "false",
                "device_id": device_id,
            }
        ]
        resp = requests.post(
            f"{BASE_URL}/preferences/device/{device_id}",
            data=data,
            headers=self._http_headers(),
        )
        return resp.json()

    def preferences_device_away_mode_enable(self, device_id):
        data = [
            {
                "name": "leak_sensitivity_away_mode",
                "value": "true",
                "device_id": device_id,
            }
        ]
        resp = requests.post(
            f"{BASE_URL}/preferences/device/{device_id}",
            data=data,
            headers=self._http_headers(),
        )
        return resp.json()

    def preferences_device_plumbing_check(
        self, device_id, automatic_tests, from_hour=0, to_hour=6
    ):
        data = [
            {"name": "scheduler_enable", "value": "true", "device_id": device_id},
            {
                "name": "scheduler_start_time",
                "value": from_hour,
                "device_id": device_id,
            },
            {"name": "scheduler_end_time", "value": to_hour, "device_id": device_id},
        ]
        resp = requests.post(
            f"{BASE_URL}/preferences/device/{device_id}",
            data=data,
            headers=self._http_headers(),
        )
        return resp.json()

    def preferences_device_notification(self, device_id):
        resp = requests.get(
            f"{BASE_URL}/preferences/device/{device_id}/notification",
            headers=self._http_headers(),
        )
        return resp.json()

    def preferences_user(self):
        resp = requests.get(
            f"{BASE_URL}/preferences/user/{requests.utils.quote(self.username)}/notification",
            headers=self._http_headers(),
        )
        return resp.json()

    def alerts_latest(self, home_id, limit=50):
        type = [
            "pinhole_leak",
            "freeze_warn",
            "leak",
            "high_pressure",
            "offline_leak",
            "periodic_leak",
            "temperature",
            "humidity",
            "water_detected",
            "battery",
        ]
        resp = requests.get(
            f"{BASE_URL}/alerts/latest?user_id={requests.utils.quote(self.username)}&home_id={home_id}&limit={limit}&type={','.join(type)}",
            headers=self._http_headers(),
        )
        return resp.json()

    def alerts_status_read(self, alert_id):
        resp = requests.post(
            f"{BASE_URL}/alerts/{alert_id}/status/read",
            headers=self._http_headers(),
        )
        return resp.json()

    def alerts_summary_active(self, filter_type="unresolved_unread"):
        resp = requests.get(
            f"{BASE_URL}/alerts/summary/active?user_id={requests.utils.quote(self.username)}&filter_type={filter_type}",
            headers=self._http_headers(),
        )
        return resp.json()

    def notifications_register(
        self, app_id=None, device_type="IOS", instance_id="default"
    ):
        raise NotImplementedError
        if not app_id:
            app_id = secrets.token_hex(32)
        data = {
            "user_id": requests.utils.quote(self.username),
            "app_id": app_id,
            "device_type": device_type,
            "instance_id": instance_id,
        }
        resp = requests.post(
            f"{BASE_URL}/notifications/register",
            data=data,
            headers=self._http_headers(),
        )
        return resp.json()
