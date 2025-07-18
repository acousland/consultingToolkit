import json
import os
from pathlib import Path

CONFIG_PATH = Path("openai_keys.json")

DEFAULT_DATA = {"active": None, "keys": {}}


def _load_data() -> dict:
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_DATA.copy()


def _save_data(data: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(data, indent=2))


def get_active_key() -> str | None:
    data = _load_data()
    active_name = data.get("active")
    if active_name:
        key = data["keys"].get(active_name)
        if key:
            return key
    # Fallback to env or streamlit secrets if available
    return os.getenv("OPENAI_API_KEY")


def list_keys() -> list[str]:
    data = _load_data()
    return list(data["keys"].keys())


def add_key(name: str, key: str) -> None:
    data = _load_data()
    data["keys"][name] = key
    if data.get("active") is None:
        data["active"] = name
    _save_data(data)


def remove_key(name: str) -> None:
    data = _load_data()
    if name in data["keys"]:
        data["keys"].pop(name)
        if data.get("active") == name:
            data["active"] = next(iter(data["keys"]), None)
        _save_data(data)


def set_active_key(name: str) -> None:
    data = _load_data()
    if name in data["keys"]:
        data["active"] = name
        _save_data(data)
