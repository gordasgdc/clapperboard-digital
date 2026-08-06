"""
Clapperboard Digital - configuration & settings persistence.

Settings (last-used project/scene/take/etc, language) are stored in a small
JSON file in the user's per-machine app data directory, so they survive
between sessions without needing any database.
"""

import os
import sys
import json
import platform

APP_NAME = "ClapperboardDigital"
APP_VERSION = "1.0.0"
BUNDLE_ID = "com.gordasgdc.clapperboarddigital"

DEFAULT_SETTINGS = {
    "language": "ro",
    "project": "",
    "scene": "",
    "take": "1",
    "director": "",
    "camera": "",
    "notes": "",
    "last_export_dir": "",
    "qr_enabled": False,
    "templates": [],   # populated on first run — see templates.py
    "history": [],     # recent project/scene sessions — see history.py
    "customization": {
        "bg": "#0A0A0C",
        "text": "#F0F0F0",
        "accent": "#F5C518",
        "footer": "#E8483C",
        "font_style": "sans_bold",
        "logo_path": "",
    },
}


def is_frozen() -> bool:
    return getattr(sys, "frozen", False)


def get_data_dir() -> str:
    system = platform.system()
    if system == "Darwin":
        base = os.path.expanduser("~/Library/Application Support")
    elif system == "Windows":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        base = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))

    data_dir = os.path.join(base, APP_NAME)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


DATA_DIR = get_data_dir()
SETTINGS_PATH = os.path.join(DATA_DIR, "settings.json")


def load_config() -> dict:
    settings = dict(DEFAULT_SETTINGS)
    settings["customization"] = dict(DEFAULT_SETTINGS["customization"])

    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                saved = json.load(f)
            if isinstance(saved, dict):
                custom = saved.pop("customization", None)
                settings.update(saved)
                if isinstance(custom, dict):
                    settings["customization"].update(custom)
        except (json.JSONDecodeError, OSError):
            pass
    return settings


def save_config(settings: dict) -> None:
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
    except OSError:
        pass
