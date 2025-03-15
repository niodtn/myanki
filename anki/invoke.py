import requests
from requests.exceptions import ConnectionError

from . import AnkiConnectError

ANKI_CONNECT_URL = "http://localhost:8765"


def invoke(action, params={}):
    """AnkiConnect API 호출"""
    try:
        response = requests.post(
            ANKI_CONNECT_URL, json={"action": action, "params": params, "version": 6}
        ).json()
        if response.get("error"):
            raise AnkiConnectError(response["error"])
        return response
    except ConnectionError:
        raise AnkiConnectError("Anki가 실행되지 않았습니다. Anki를 먼저 실행해주세요.")
