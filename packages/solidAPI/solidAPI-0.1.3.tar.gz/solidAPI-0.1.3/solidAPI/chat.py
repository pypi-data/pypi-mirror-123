import requests

from solidAPI import BASE_URL
from solidAPI.other import get_available_language


def add_chat(chat_id: int, lang="en"):
    """
    :param chat_id:
    :param lang: str
    :return: 201 or 404 or 500
    """
    r = requests.post(f"{BASE_URL}/chats/", json={
        "chat_id": chat_id,
        "lang": lang
    })
    return r.status_code


def get_chat(chat_id: int):
    r = requests.get(f"{BASE_URL}/chats/{chat_id}")
    return r.json()


def set_lang(chat_id: int, lang: str):
    """

    :param chat_id:
    :param lang:
    :return: str or 200
    """
    if lang not in get_available_language():
        return f"language {lang} not in our database."
    r = requests.put(f"{BASE_URL}/chats/{chat_id}?lang={lang}")
    return r.status_code


def del_chat(chat_id: int):
    r = requests.delete(f"{BASE_URL}/chats/", json={
        "chat_id": chat_id
    })
    return r.status_code
