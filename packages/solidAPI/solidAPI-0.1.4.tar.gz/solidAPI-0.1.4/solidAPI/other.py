import requests
from . import BASE_URL


def get_message(chat_id: int, key: str) -> str:
    r = requests.get(f"{BASE_URL}/message", params={
        "chat_id": chat_id,
        "key": key
    })
    message = r.json()['message']
    return message


def get_available_language(lang: str = None):
    if not lang:
        r = requests.get(f"{BASE_URL}/langs")
        language = r.json()["language"]
        return list(language)
    r = requests.get(f"{BASE_URL}/langs", params={
        "lang": lang
    })
    key = r.json()["key"]
    return dict(key)
