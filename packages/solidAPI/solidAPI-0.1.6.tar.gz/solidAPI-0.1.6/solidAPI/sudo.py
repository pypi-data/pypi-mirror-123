import requests
from typing import Union
from ._base_url import BASE_URL

SUDO_URL = f"{BASE_URL}/sudos/"


def get_sudos(chat_id: int) -> Union[list[int], int]:
    try:
        r = requests.get(f"{SUDO_URL}{chat_id}")
        return r.json()["sudos"]
    except KeyError:
        return 404


def add_sudo(chat_id: int, user_id: int):
    r = requests.post(f"{SUDO_URL}", json={
        "chat_id": chat_id,
        "user_id": user_id
    })
    return r.status_code


def del_sudo(chat_id: int, user_id: int):
    r = requests.delete(f"{SUDO_URL}", json={
        "chat_id": chat_id,
        "user_id": user_id
    })
    return r.status_code


def put_sudo(chat_id: int, user_id: int) -> dict:
    r = requests.put(f"{SUDO_URL}{chat_id}", json={
        "chat_id": chat_id,
        "user_id": user_id
    })
    return r.json()
