#!/usr/bin/env python3
import functools
import pathlib
from json import JSONDecodeError

import requests
from requests import auth


@functools.cache
def _read_env():
    return dict(
        line.strip().split("=", maxsplit=1)
        for line in pathlib.Path(".env").read_text().splitlines()
    )


def _read_username():
    return _read_env()["BOTFIGHTS_USER"]


def _read_password():
    return _read_env()["BOTFIGHTS_PASS"]


class BotfightsClient:
    """Python wrapper for the botfights API"""

    def __init__(self, url="https://api.botfights.ai", username=None, password=None):
        self._url = url
        self._username = username or _read_username()
        self._password = password or _read_password()

    def _request(self, method, path, json=None):
        resp = requests.request(
            method,
            self._url + path,
            auth=auth.HTTPBasicAuth(self._username, self._password),
            json=json,
        )
        try:
            return resp.json()
        except JSONDecodeError:
            pass
        resp.raise_for_status()
        raise RuntimeError

    def patch_user(
        self,
        display_name=None,
        github_link=None,
        description=None,
        external_link=None,
        btc_address=None,
    ):
        """Change information about authenticated user"""
        return self._request(
            "PATCH",
            f"/api/v1/user/{self._username}",
            json={k: v for k, v in locals().items() if v is not None and k != "self"},
        )

    def get_user(self):
        """Get information about authenticated user"""
        return self._request("GET", f"/api/v1/user/{self._username}")


if __name__ == "__main__":
    import fire

    fire.Fire(BotfightsClient)
