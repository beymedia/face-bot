import json
import os
import threading
from typing import Optional

DATA_FILE = os.environ.get("DATA_FILE", "users.json")
_lock = threading.Lock()


def _load() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict) -> None:
    tmp = DATA_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f)
    os.replace(tmp, DATA_FILE)


def save_embedding(user_id: int, embedding: list[float]) -> None:
    with _lock:
        data = _load()
        data[str(user_id)] = embedding
        _save(data)


def get_embedding(user_id: int) -> Optional[list[float]]:
    with _lock:
        return _load().get(str(user_id))


def delete_embedding(user_id: int) -> bool:
    with _lock:
        data = _load()
        if str(user_id) in data:
            del data[str(user_id)]
            _save(data)
            return True
        return False
