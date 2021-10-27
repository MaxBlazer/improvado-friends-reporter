import requests
import json


class VK:
    """VK API wrapper."""

    def __init__(self, version: str, access_token: str):
        self.version = version
        self.token = access_token

    def get_friends(self, user_id=0):
        return self._api_call('friends.get', user_id=user_id)

    def get_users(self, user_ids: list[int]):
        return self._api_call('users.get', user_ids=','.join(str(id) for id in user_ids))

    def _api_call(self, method: str, **params) -> dict:
        params = '&'.join(f'{k}={v}' for k, v in params.items())
        url = f'https://api.vk.com/method/{method}?access_token={self.token}&v={self.version}&{params}'
        response = requests.get(url)
        return json.loads(response.text)

