"""
Clapperboard Digital - take history.

Tracks the highest take number reached per (project, scene) pair, so the
person can see "Nunta Ana & Mihai - Ceremonia - Take 1-15" and reload that
context instantly instead of retyping it.
"""

import datetime

MAX_HISTORY_ENTRIES = 20


def upsert_history_entry(settings: dict, data: dict) -> None:
    """Updates (or creates) the history entry matching this project+scene
    with the latest field values and the highest take number seen."""
    project = (data.get("project") or "").strip()
    if not project:
        return  # nothing meaningful to record yet

    scene = (data.get("scene") or "").strip()
    try:
        take_num = int(data.get("take") or "1")
    except ValueError:
        take_num = 1

    history = settings.get("history") or []
    today = datetime.date.today().isoformat()

    for entry in history:
        if entry.get("project") == project and entry.get("scene") == scene:
            entry["takes"] = max(entry.get("takes", 1), take_num)
            entry["director"] = data.get("director", "")
            entry["camera"] = data.get("camera", "")
            entry["notes"] = data.get("notes", "")
            entry["date"] = today
            _move_to_front(history, entry)
            settings["history"] = history[:MAX_HISTORY_ENTRIES]
            return

    new_entry = {
        "project": project,
        "scene": scene,
        "director": data.get("director", ""),
        "camera": data.get("camera", ""),
        "notes": data.get("notes", ""),
        "takes": take_num,
        "date": today,
    }
    history.insert(0, new_entry)
    settings["history"] = history[:MAX_HISTORY_ENTRIES]


def _move_to_front(history: list, entry: dict) -> None:
    if entry in history:
        history.remove(entry)
    history.insert(0, entry)


def clear_history(settings: dict) -> None:
    settings["history"] = []


def entry_label(entry: dict) -> str:
    date = entry.get("date", "")
    project = entry.get("project", "")
    scene = entry.get("scene", "")
    takes = entry.get("takes", 1)
    scene_part = f" · {scene}" if scene else ""
    return f"{date} — {project}{scene_part} — Take 1-{takes}"
