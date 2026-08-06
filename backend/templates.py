"""
Clapperboard Digital - quick-fill templates.

A template pre-fills the form with common values for a type of shoot. The
`project` field may contain a `{param}` placeholder (e.g. "Nunta {client}")
— when applied, the app asks for that one value and substitutes it.
"""

import re
import uuid

DEFAULT_TEMPLATES = [
    {
        "name": "Nuntă",
        "name_en": "Wedding",
        "name_es": "Boda",
        "project": "Nunta {client}",
        "scene": "Ceremonia",
        "director": "",
        "camera": "",
        "notes": "Filmare nuntă",
        "is_default": True,
    },
    {
        "name": "Reclamă",
        "name_en": "Commercial",
        "name_es": "Anuncio",
        "project": "Reclamă {brand}",
        "scene": "Studio",
        "director": "",
        "camera": "",
        "notes": "Filmare reclamă",
        "is_default": True,
    },
    {
        "name": "Interviu",
        "name_en": "Interview",
        "name_es": "Entrevista",
        "project": "Interviu {subject}",
        "scene": "Interior",
        "director": "",
        "camera": "",
        "notes": "",
        "is_default": True,
    },
    {
        "name": "Documentar",
        "name_en": "Documentary",
        "name_es": "Documental",
        "project": "Documentar {title}",
        "scene": "",
        "director": "",
        "camera": "",
        "notes": "",
        "is_default": True,
    },
]

PLACEHOLDER_RE = re.compile(r"\{(\w+)\}")


def ensure_default_templates(settings: dict) -> None:
    """Seeds the built-in templates once, on first run. Safe to call every
    startup — it's a no-op once any default template already exists."""
    templates = settings.get("templates") or []
    if any(t.get("is_default") for t in templates):
        return
    for tpl in DEFAULT_TEMPLATES:
        entry = dict(tpl)
        entry["id"] = uuid.uuid4().hex[:8]
        templates.append(entry)
    settings["templates"] = templates


def template_label(template: dict, lang: str) -> str:
    if lang == "en":
        return template.get("name_en") or template.get("name", "")
    if lang == "es":
        return template.get("name_es") or template.get("name", "")
    return template.get("name", "")


def extract_placeholder(project_pattern: str):
    """Returns the first {placeholder} name in the pattern, or None."""
    match = PLACEHOLDER_RE.search(project_pattern or "")
    return match.group(1) if match else None


def apply_template(template: dict, placeholder_value: str = "") -> dict:
    """Returns a dict of field values ready to drop into the form."""
    project = template.get("project", "")
    placeholder = extract_placeholder(project)
    if placeholder:
        project = PLACEHOLDER_RE.sub(placeholder_value or "", project, count=1).strip()

    return {
        "project": project,
        "scene": template.get("scene", ""),
        "director": template.get("director", ""),
        "camera": template.get("camera", ""),
        "notes": template.get("notes", ""),
    }


def new_template(name: str, project: str, scene: str, director: str, camera: str, notes: str) -> dict:
    return {
        "id": uuid.uuid4().hex[:8],
        "name": name,
        "name_en": name,
        "name_es": name,
        "project": project,
        "scene": scene,
        "director": director,
        "camera": camera,
        "notes": notes,
        "is_default": False,
    }
