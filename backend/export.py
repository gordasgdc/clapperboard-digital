"""
Clapperboard Digital - export the generated slate as video, PDF, or PNG.

Video export shells out to FFmpeg (not bundled — see ffmpeg_available()).
PDF export uses reportlab. Both fail gracefully with a clear reason instead
of crashing the app.
"""

import os
import shutil
import subprocess
import tempfile

from clapperboard import ClapperboardGenerator


class ExportError(Exception):
    """Raised with a user-facing message when an export step fails."""


def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


class Exporter:
    def __init__(self, customization: dict = None):
        self.generator = ClapperboardGenerator(customization=customization)

    def update_customization(self, customization: dict):
        self.generator = ClapperboardGenerator(customization=customization)

    # ------------------------------------------------------------- image --

    def export_png(self, data: dict, output_path: str, qr_image=None) -> None:
        image = self.generator.generate(data, qr_image=qr_image)
        try:
            image.save(output_path, "PNG")
        except OSError as e:
            raise ExportError(str(e))

    # ------------------------------------------------------------- video --

    def export_video(self, data: dict, output_path: str, duration_seconds: int = 5, qr_image=None) -> None:
        """Renders a static slate clip of `duration_seconds`. Codec is
        chosen from the output extension: ProRes for .mov, H.264 for .mp4."""
        if not ffmpeg_available():
            raise ExportError("ffmpeg_missing")

        image = self.generator.generate(data, qr_image=qr_image)

        tmp_dir = tempfile.mkdtemp(prefix="clapperboard_")
        tmp_image = os.path.join(tmp_dir, "slate.png")
        try:
            image.save(tmp_image, "PNG")

            ext = os.path.splitext(output_path)[1].lower()
            if ext == ".mov":
                codec_args = ["-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le"]
            else:
                codec_args = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18"]

            cmd = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", tmp_image,
                "-t", str(max(1, int(duration_seconds))),
                "-r", "25",
                *codec_args,
                output_path,
            ]

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120
            )
            if result.returncode != 0:
                raise ExportError(result.stderr.strip()[-500:] or "ffmpeg_failed")
        except subprocess.TimeoutExpired:
            raise ExportError("ffmpeg_timeout")
        finally:
            try:
                os.remove(tmp_image)
                os.rmdir(tmp_dir)
            except OSError:
                pass

    # --------------------------------------------------------------- pdf --

    def export_pdf(self, data: dict, output_path: str, qr_image=None) -> None:
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib.utils import ImageReader
        except ImportError:
            raise ExportError("reportlab_missing")

        try:
            c = canvas.Canvas(output_path, pagesize=landscape(A4))
            width, height = landscape(A4)

            c.setFillColorRGB(0.04, 0.04, 0.047)
            c.rect(0, 0, width, height, fill=1, stroke=0)

            c.setFillColorRGB(0.96, 0.77, 0.09)
            c.rect(0, height - 14, width, 14, fill=1, stroke=0)
            c.rect(0, 0, width, 14, fill=1, stroke=0)

            c.setFillColorRGB(1, 1, 1)
            c.setFont("Helvetica-Bold", 26)
            c.drawCentredString(width / 2, height - 60, "CLAPPERBOARD")

            c.setStrokeColorRGB(0.96, 0.77, 0.09)
            c.setLineWidth(1.4)
            c.line(60, height - 80, width - 60, height - 80)

            rows = [
                (data.get("project_label", "Project"), data.get("project", "")),
                (data.get("scene_label", "Scene"), data.get("scene", "")),
                (data.get("take_label", "Take"), str(data.get("take", "1"))),
                (data.get("director_label", "Director"), data.get("director", "")),
                (data.get("camera_label", "Camera"), data.get("camera", "")),
                (data.get("date_label", "Date"), data.get("date", "")),
                (data.get("time_label", "Time"), data.get("time", "")),
            ]

            y = height - 130
            for label, value in rows:
                c.setFillColorRGB(0.96, 0.77, 0.09)
                c.setFont("Helvetica-Bold", 13)
                c.drawString(70, y, f"{label}")
                c.setFillColorRGB(0.94, 0.94, 0.94)
                c.setFont("Helvetica", 13)
                c.drawString(220, y, value or "—")
                y -= 26

            notes = (data.get("notes") or "").strip()
            if notes:
                y -= 10
                c.setStrokeColorRGB(0.3, 0.3, 0.32)
                c.line(70, y, width - 70, y)
                y -= 22
                c.setFillColorRGB(0.8, 0.8, 0.8)
                c.setFont("Helvetica-Oblique", 11)
                for line in self._wrap_pdf_text(notes, 100):
                    c.drawString(70, y, line)
                    y -= 18

            c.setFillColorRGB(0.91, 0.28, 0.24)
            c.setFont("Helvetica-Oblique", 9)
            c.drawCentredString(width / 2, 26, "Clapperboard Digital · GDC")

            if qr_image is not None:
                qr_size = 90
                c.drawImage(
                    ImageReader(qr_image),
                    width - 70 - qr_size, 40,
                    width=qr_size, height=qr_size,
                )

            c.save()
        except OSError as e:
            raise ExportError(str(e))

    @staticmethod
    def _wrap_pdf_text(text: str, max_chars: int) -> list:
        words = text.split()
        lines, current = [], ""
        for word in words:
            trial = f"{current} {word}".strip()
            if len(trial) <= max_chars:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines[:6]
