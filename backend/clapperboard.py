"""
Clapperboard Digital - generates the on-screen "slate" image shown at the
start of a take: project, scene, take, director, camera, date/time, notes.

Visual choice: classic black background with yellow text/stripes. This is
the real-world clapperboard convention (yellow-on-black reads reliably on
camera, in bright or dim sets alike) — deliberately different from the
app's own dark-teal UI chrome, because the exported screen has to work as
an on-camera reference, not as branding.
"""

import os
import sys
import datetime
from PIL import Image, ImageDraw, ImageFont


BG_COLOR = (10, 10, 12)
STRIPE_BLACK = (10, 10, 12)
STRIPE_YELLOW = (245, 197, 24)
TEXT_WHITE = (240, 240, 240)
LABEL_YELLOW = (245, 197, 24)
ACCENT_RED = (232, 72, 60)

WIDTH, HEIGHT = 1920, 1080


def _resource_path(*parts) -> str:
    """Resolve a bundled resource path, working both from source and from
    inside a PyInstaller bundle."""
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, *parts)


def _load_font(size: int, bold: bool = False):
    """Tries a handful of common system fonts before falling back to the
    PIL default, so the slate still looks reasonable on any machine."""
    candidates = []
    if sys.platform == "darwin":
        candidates = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/HelveticaNeue.ttc",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        ]
    elif sys.platform == "win32":
        candidates = [
            "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
            "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]

    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


class ClapperboardGenerator:
    def __init__(self):
        self.font_title = _load_font(64, bold=True)
        self.font_label = _load_font(34, bold=True)
        self.font_value = _load_font(38, bold=False)
        self.font_notes = _load_font(28, bold=False)
        self.font_footer = _load_font(22, bold=False)

    @staticmethod
    def get_current_date() -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def get_current_time() -> str:
        return datetime.datetime.now().strftime("%H:%M")

    def generate(self, data: dict) -> Image.Image:
        """Builds the full 1920x1080 slate image from the given field data."""
        image = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(image)

        self._draw_clapper_stripes(draw, top=True)
        self._draw_clapper_stripes(draw, top=False)

        title = "CLAPPERBOARD"
        draw.text((WIDTH // 2, 150), title, fill=TEXT_WHITE, font=self.font_title, anchor="mm")
        draw.line([(140, 210), (WIDTH - 140, 210)], fill=STRIPE_YELLOW, width=3)

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
            draw.text((label_x, y), f"{label}", fill=LABEL_YELLOW, font=self.font_label, anchor="lm")
            draw.text((value_x, y), value or "—", fill=TEXT_WHITE, font=self.font_value, anchor="lm")
            y += row_height

        # Date / time, right-aligned block, each with a small label above it
        date_str = data.get("date") or self.get_current_date()
        time_str = data.get("time") or self.get_current_time()
        date_label = data.get("date_label", "Date")
        time_label = data.get("time_label", "Time")

        draw.text((WIDTH - 160, 280 - 30), date_label, fill=LABEL_YELLOW, font=self.font_notes, anchor="rm")
        draw.text((WIDTH - 160, 280), date_str, fill=TEXT_WHITE, font=self.font_value, anchor="rm")
        draw.text((WIDTH - 160, 280 + row_height - 30), time_label, fill=LABEL_YELLOW, font=self.font_notes, anchor="rm")
        draw.text((WIDTH - 160, 280 + row_height), time_str, fill=TEXT_WHITE, font=self.font_value, anchor="rm")

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
            fill=ACCENT_RED,
            font=self.font_footer,
            anchor="mm",
        )

        return image

    def _draw_clapper_stripes(self, draw: ImageDraw.ImageDraw, top: bool):
        band_height = 60
        y0 = 0 if top else HEIGHT - band_height
        y1 = band_height if top else HEIGHT

        stripe_width = 70
        skew = 40
        x = -skew
        toggle = True
        while x < WIDTH + skew:
            color = STRIPE_YELLOW if toggle else STRIPE_BLACK
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
    def _wrap_text(text: str, font: ImageFont.ImageFont, max_width: int) -> list:
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
