"""
Clapperboard Digital - QR code embedding.

Encodes the shoot's metadata (project, scene, take, director, camera, date,
time) as JSON in a QR code, so it can be scanned by a phone or a script
during ingest instead of retyped.
"""

import json


def qr_available() -> bool:
    try:
        import qrcode  # noqa: F401
        return True
    except ImportError:
        return False


def generate_qr_image(data: dict, box_size: int = 8):
    """Returns a PIL Image of the QR code, or None if the qrcode package
    isn't available (export/preview should degrade gracefully, not crash)."""
    try:
        import qrcode
    except ImportError:
        return None

    payload = json.dumps({
        "project": data.get("project", ""),
        "scene": data.get("scene", ""),
        "take": data.get("take", ""),
        "director": data.get("director", ""),
        "camera": data.get("camera", ""),
        "date": data.get("date", ""),
        "time": data.get("time", ""),
    }, ensure_ascii=False)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=2,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").convert("RGB")
