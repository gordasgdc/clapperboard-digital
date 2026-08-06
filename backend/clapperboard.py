"""
Clapperboard Digital - generates the on-screen "slate" image shown at the
start of a take: project, scene, take, director, camera, date/time, notes.

Default visual: classic black background with yellow text/stripes — the
real-world clapperboard convention (yellow-on-black reads reliably on
camera). Colors, font, and an optional logo are customizable per the
person's `customization` settings; QR embedding is optional and separate.
"""

import os
import sys
import datetime
from PIL import Image, ImageDraw, ImageFont

DEFAULT_COLORS = {
    "bg": "#0A0A0C",
    "text": "#F0F0F0",
    "accent": "#F5C518",
    "footer": "#E8483C",
}

WIDTH, HEIGHT = 1920, 1080


def _hex_to_rgb(hex_color: str, fallback: str) -> tuple:
    try:
        h = (hex_color or fallback).lstrip("#")
        if len(h) != 6:
            h = fallback.lstrip("#")
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except (ValueError, TypeError):
        return tuple(int(fallback.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))


def _resource_path(*parts) -> str:
    """Resolve a bundled resource path, working both from source and from
    inside a PyInstaller bundle."""
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, *parts)


SANS_BOLD = {
    "darwin": "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "win32": "C:\\Windows\\Fonts\\arialbd.ttf",
    "default": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
}
SANS_REGULAR = {
    "darwin": "/System/Library/Fonts/Supplemental/Arial.ttf",
    "win32": "C:\\Windows\\Fonts\\arial.ttf",
    "default": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}
SERIF_BOLD = {
    "darwin": "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    "win32": "C:\\Windows\\Fonts\\georgiab.ttf",
    "default": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
}
SERIF_REGULAR = {
    "darwin": "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "win32": "C:\\Windows\\Fonts\\georgia.ttf",
    "default": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
}

FONT_STYLES = {
    "sans_bold": (SANS_BOLD, SANS_REGULAR),
    "serif": (SERIF_BOLD, SERIF_REGULAR),
}


def _platform_key() -> str:
    if sys.platform == "darwin":
        return "darwin"
    if sys.platform == "win32":
        return "win32"
    return "default"


def _load_font(size: int, bold: bool = False, font_style: str = "sans_bold"):
    """Tries the requested style's system font before falling back through
    sans-serif, then the PIL default, so the slate always renders."""
    bold_map, regular_map = FONT_STYLES.get(font_style, FONT_STYLES["sans_bold"])
    chosen_map = bold_map if bold else regular_map
    plat = _platform_key()

    candidates = [chosen_map.get(plat), chosen_map.get("default")]
    # Always fall back to plain sans as a last resort if a serif file is missing.
    fallback_map = SANS_BOLD if bold else SANS_REGULAR
    candidates += [fallback_map.get(plat), fallback_map.get("default")]

    for path in candidates:
        if path and os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


class ClapperboardGenerator:
    def __init__(self, customization: dict = None):
        customization = customization or {}
        self.colors = {
            "bg": _hex_to_rgb(customization.get("bg"), DEFAULT_COLORS["bg"]),
            "text": _hex_to_rgb(customization.get("text"), DEFAULT_COLORS["text"]),
            "accent": _hex_to_rgb(customization.get("accent"), DEFAULT_COLORS["accent"]),
            "footer": _hex_to_rgb(customization.get("footer"), DEFAULT_COLORS["footer"]),
        }
        self.logo_path = customization.get("logo_path") or ""
        font_style = customization.get("font_style") or "sans_bold"

        self.font_title = _load_font(64, bold=True, font_style=font_style)
        self.font_label = _load_font(34, bold=True, font_style=font_style)
        self.font_value = _load_font(38, bold=False, font_style=font_style)
        self.font_notes = _load_font(28, bold=False, font_style=font_style)
        self.font_footer = _load_font(22, bold=False, font_style=font_style)

    @staticmethod
    def get_current_date() -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def get_current_time() -> str:
        return datetime.datetime.now().strftime("%H:%M")

    def generate(self, data: dict, qr_image: Image.Image = None) -> Image.Image:
        """Builds the full 1920x1080 slate image from the given field data.
        `qr_image`, if given, is composited in the bottom-right corner."""
        bg = self.colors["bg"]
        text_color = self.colors["text"]
        accent = self.colors["accent"]
        footer_color = self.colors["footer"]

        image = Image.new("RGB", (WIDTH, HEIGHT), bg)
        draw = ImageDraw.Draw(image)

        self._draw_clapper_stripes(draw, top=True, bg=bg, accent=accent)
        self._draw_clapper_stripes(draw, top=False, bg=bg, accent=accent)

        title = "CLAPPERBOARD"
        draw.text((WIDTH // 2, 150), title, fill=text_color, font=self.font_title, anchor="mm")
        draw.line([(140, 210), (WIDTH - 140, 210)], fill=accent, width=3)

        rows = [
            (data.get("project_label", "Project"), data.get("project", "")),
            (data.get("scene_label", "Scene"), data.get("scene", "")),
            (data.get("take_label", "Take"), str(data.get("take", "1"))),
            (data.get("director_label", "Director"), data.get("director", "")),
            (data.get("camera_label", "Camera"), data.get("camera", "")),
        ]

        y = 280
        row_height = 78
        label_x = 160
        value_x = 560
        band_footer_offset = 95  # keeps the footer clear of the bottom stripe band

        for label, value in rows:
            draw.text((label_x, y), f"{label}", fill=accent, font=self.font_label, anchor="lm")
            draw.text((value_x, y), value or "—", fill=text_color, font=self.font_value, anchor="lm")
            y += row_height

        # Date / time, right-aligned block, each with a small label above it
        date_str = data.get("date") or self.get_current_date()
        time_str = data.get("time") or self.get_current_time()
        date_label = data.get("date_label", "Date")
        time_label = data.get("time_label", "Time")

        draw.text((WIDTH - 160, 280 - 30), date_label, fill=accent, font=self.font_notes, anchor="rm")
        draw.text((WIDTH - 160, 280), date_str, fill=text_color, font=self.font_value, anchor="rm")
        draw.text((WIDTH - 160, 280 + row_height - 30), time_label, fill=accent, font=self.font_notes, anchor="rm")
        draw.text((WIDTH - 160, 280 + row_height), time_str, fill=text_color, font=self.font_value, anchor="rm")

        notes = (data.get("notes") or "").strip()
        if notes:
            notes_y = y + 30
            draw.line([(140, notes_y - 20), (WIDTH - 140, notes_y - 20)], fill=(70, 70, 74), width=2)
            wrapped = self._wrap_text(notes, self.font_notes, WIDTH - 320)
            for line in wrapped[:4]:
                draw.text((label_x, notes_y), line, fill=(200, 200, 200), font=self.font_notes, anchor="lm")
                notes_y += 40

        draw.text(
            (WIDTH // 2, HEIGHT - band_footer_offset),
            "Clapperboard Digital · GDC",
            fill=footer_color,
            font=self.font_footer,
            anchor="mm",
        )

        if self.logo_path and os.path.exists(self.logo_path):
            self._paste_logo(image)

        if qr_image is not None:
            self._paste_qr(image, qr_image)

        return image

    def _paste_logo(self, image: Image.Image):
        try:
            logo = Image.open(self.logo_path).convert("RGBA")
        except (OSError, ValueError):
            return
        max_h = 90
        ratio = max_h / logo.height
        logo = logo.resize((max(1, int(logo.width * ratio)), max_h), Image.LANCZOS)
        image.paste(logo, (WIDTH - logo.width - 160, 230 - logo.height // 2), logo)

    def _paste_qr(self, image: Image.Image, qr_image: Image.Image):
        qr_size = 190
        qr_resized = qr_image.resize((qr_size, qr_size), Image.LANCZOS)
        pad = 14
        frame = Image.new("RGB", (qr_size + pad * 2, qr_size + pad * 2), (255, 255, 255))
        frame.paste(qr_resized, (pad, pad))
        image.paste(frame, (WIDTH - qr_size - pad * 2 - 140, HEIGHT - qr_size - pad * 2 - 130))

    def _draw_clapper_stripes(self, draw: ImageDraw.ImageDraw, top: bool, bg: tuple, accent: tuple):
        band_height = 60
        y0 = 0 if top else HEIGHT - band_height
        y1 = band_height if top else HEIGHT

        stripe_width = 70
        skew = 40
        x = -skew
        toggle = True
        while x < WIDTH + skew:
            color = accent if toggle else bg
            draw.polygon(
                [
                    (x, y1),
                    (x + skew, y0),
                    (x + skew + stripe_width, y0),
                    (x + stripe_width, y1),
                ],
                fill=color,
            )
            toggle = not toggle
            x += stripe_width

    @staticmethod
    def _wrap_text(text: str, font, max_width: int) -> list:
        words = text.split()
        lines = []
        current = ""
        dummy = Image.new("RGB", (10, 10))
        d = ImageDraw.Draw(dummy)
        for word in words:
            trial = f"{current} {word}".strip()
            bbox = d.textbbox((0, 0), trial, font=font)
            if bbox[2] - bbox[0] <= max_width or not current:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines
