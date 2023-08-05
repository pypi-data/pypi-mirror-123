import requests
from solidAPI import BASE_URL
from typing import Optional


def get_message(chat_id: int, key: str):
    r = requests.get(f"{BASE_URL}/message", params={
        "chat_id": chat_id,
        "key": key
    })
    message = r.json()['message']
    return message


def get_available_language(lang: Optional[str] = None):
    if not lang:
        r = requests.get(f"{BASE_URL}/langs")
        language = r.json()["language"]
        return language
    r = requests.get(f"{BASE_URL}/langs", params={
        "lang": lang
    })
    key = r.json()["key"]
    return key
