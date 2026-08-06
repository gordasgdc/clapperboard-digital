"""
Clapperboard Digital - import projects from a GDC Production Manager export.

GDC Production Manager's "Export data (JSON)" produces a file shaped like:
    {"export_version": 1, "clients": [...], "projects": [...], "templates": [...]}

We only need enough from each project to prefill the slate form. GDC PM's
project schema has no "director" or "camera" field (Cristi is implicitly
the colorist/editor on every project there), so those are intentionally
left blank for the person to fill in here.
"""

import json


class ImportError_(Exception):
    """Raised with a user-facing reason when the file can't be parsed."""


def load_gdc_projects(json_path: str) -> list:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise ImportError_(str(e))

    if not isinstance(payload, dict) or "projects" not in payload:
        raise ImportError_("not_a_gdc_export")

    clients_by_id = {c.get("id"): c.get("name", "") for c in payload.get("clients", [])}

    projects = []
    for p in payload.get("projects", []):
        client_name = p.get("client_name") or clients_by_id.get(p.get("client_id"), "")
        projects.append({
            "title": p.get("title", ""),
            "client_name": client_name,
            "shoot_location": p.get("shoot_location", ""),
            "project_type": p.get("project_type", ""),
        })
    return projects


def project_to_form_data(project: dict) -> dict:
    """Maps a GDC PM project entry onto clapperboard form fields."""
    notes_parts = []
    if project.get("client_name"):
        notes_parts.append(f"Client: {project['client_name']}")
    if project.get("shoot_location"):
        notes_parts.append(project["shoot_location"])

    return {
        "project": project.get("title", ""),
        "scene": "",
        "director": "",
        "camera": "",
        "notes": " · ".join(notes_parts),
    }
