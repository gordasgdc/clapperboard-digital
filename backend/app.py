"""
Clapperboard Digital - main application window.

A focused, single-window Tkinter app: fill in the shoot info on the left,
watch the slate update live on the right, export when ready.
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from PIL import Image, ImageTk

from clapperboard import ClapperboardGenerator
from export import Exporter, ExportError, ffmpeg_available
from config import load_config, save_config, APP_VERSION
from translations import t

# ------------------------------------------------------------- dark theme --

COLORS = {
    "bg": "#101218",
    "bg_elevated": "#171A22",
    "panel": "#1B1F29",
    "border": "#2A2F3B",
    "text": "#ECEEF1",
    "text_muted": "#9199A8",
    "accent": "#35D6BE",
    "accent_dark": "#143A35",
    "tally": "#E8483C",
    "amber": "#E8A33D",
}

FIELD_KEYS = ["project", "scene", "take", "director", "camera", "notes"]


class ClapperboardApp:
    def __init__(self):
        self.settings = load_config()
        self.lang = self.settings.get("language", "ro")

        self.generator = ClapperboardGenerator()
        self.exporter = Exporter()

        self.root = tk.Tk()
        self.root.title(t(self.lang, "app_title"))
        self.root.geometry("1100x680")
        self.root.minsize(880, 560)
        self.root.configure(bg=COLORS["bg"])

        self.vars = {key: tk.StringVar(value=self.settings.get(key, "")) for key in FIELD_KEYS}
        if not self.vars["take"].get():
            self.vars["take"].set("1")

        self.duration_var = tk.IntVar(value=5)
        self.status_var = tk.StringVar(value=t(self.lang, "status_ready"))

        self._preview_photo = None  # keep a reference so Tk doesn't GC it
        self._debounce_job = None
        self._label_widgets = {}  # key -> widget, for live language switching

        self._build_menu()
        self._build_ui()
        self._apply_theme()

        for key in FIELD_KEYS:
            self.vars[key].trace_add("write", self._on_field_change)

        self._regenerate_preview()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ---------------------------------------------------------------- UI --

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label=t(self.lang, "menu_export_video"), command=self._export_video)
        file_menu.add_command(label=t(self.lang, "menu_export_pdf"), command=self._export_pdf)
        file_menu.add_command(label=t(self.lang, "menu_export_png"), command=self._export_png)
        file_menu.add_separator()
        file_menu.add_command(label=t(self.lang, "menu_quit"), command=self._on_close)
        menubar.add_cascade(label=t(self.lang, "menu_file"), menu=file_menu)
        self._menu_file = file_menu

        lang_menu = tk.Menu(menubar, tearoff=0)
        self.lang_choice = tk.StringVar(value=self.lang)
        for code, label in (("ro", "Română"), ("en", "English"), ("es", "Español")):
            lang_menu.add_radiobutton(
                label=label, value=code, variable=self.lang_choice,
                command=lambda c=code: self._set_language(c),
            )
        menubar.add_cascade(label=t(self.lang, "menu_language"), menu=lang_menu)
        self._menu_lang = lang_menu

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label=t(self.lang, "menu_about"), command=self._show_about)
        menubar.add_cascade(label=t(self.lang, "menu_help"), menu=help_menu)
        self._menu_help = help_menu

        self._menubar = menubar
        self.root.config(menu=menubar)

    def _build_ui(self):
        header = tk.Frame(self.root, bg=COLORS["bg"])
        header.pack(fill="x", padx=24, pady=(18, 8))

        self._title_label = tk.Label(
            header, text=f"🎬 {t(self.lang, 'app_title')}",
            font=("Helvetica", 20, "bold"), fg=COLORS["text"], bg=COLORS["bg"],
        )
        self._title_label.pack(side="left")

        body = tk.Frame(self.root, bg=COLORS["bg"])
        body.pack(fill="both", expand=True, padx=24, pady=8)
        body.columnconfigure(0, weight=1, uniform="cols")
        body.columnconfigure(1, weight=1, uniform="cols")
        body.rowconfigure(0, weight=1)

        # ---- left: form ----
        left = tk.LabelFrame(
            body, text=t(self.lang, "section_info"),
            bg=COLORS["panel"], fg=COLORS["accent"], bd=1, relief="solid",
            font=("Helvetica", 11, "bold"), labelanchor="nw",
        )
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self._left_frame = left

        self._field_rows = {}
        for key in FIELD_KEYS:
            row = tk.Frame(left, bg=COLORS["panel"])
            row.pack(fill="x", padx=16, pady=(12, 0))

            label = tk.Label(
                row, text=t(self.lang, f"field_{key}"), width=12, anchor="w",
                fg=COLORS["text_muted"], bg=COLORS["panel"], font=("Helvetica", 10),
            )
            label.pack(side="left")
            self._field_rows[key] = label

            if key == "take":
                take_frame = tk.Frame(row, bg=COLORS["panel"])
                take_frame.pack(side="left", fill="x", expand=True)
                entry = tk.Entry(
                    take_frame, textvariable=self.vars["take"], width=6,
                    bg=COLORS["bg_elevated"], fg=COLORS["text"],
                    insertbackground=COLORS["text"], relief="flat",
                    highlightthickness=1, highlightbackground=COLORS["border"],
                    highlightcolor=COLORS["accent"], justify="center",
                )
                entry.pack(side="left", ipady=4)
                minus_btn = tk.Button(
                    take_frame, text="−", width=3, command=self._decrement_take,
                    bg=COLORS["bg_elevated"], fg=COLORS["text"], relief="flat",
                    activebackground=COLORS["border"], activeforeground=COLORS["text"],
                )
                minus_btn.pack(side="left", padx=(8, 2))
                plus_btn = tk.Button(
                    take_frame, text="+", width=3, command=self._increment_take,
                    bg=COLORS["bg_elevated"], fg=COLORS["text"], relief="flat",
                    activebackground=COLORS["border"], activeforeground=COLORS["text"],
                )
                plus_btn.pack(side="left", padx=2)
            else:
                entry = tk.Entry(
                    row, textvariable=self.vars[key],
                    bg=COLORS["bg_elevated"], fg=COLORS["text"],
                    insertbackground=COLORS["text"], relief="flat",
                    highlightthickness=1, highlightbackground=COLORS["border"],
                    highlightcolor=COLORS["accent"],
                )
                entry.pack(side="left", fill="x", expand=True, ipady=4)

        # Video duration control
        dur_row = tk.Frame(left, bg=COLORS["panel"])
        dur_row.pack(fill="x", padx=16, pady=(16, 0))
        self._duration_label = tk.Label(
            dur_row, text=t(self.lang, "video_duration_label"),
            fg=COLORS["text_muted"], bg=COLORS["panel"], font=("Helvetica", 10),
        )
        self._duration_label.pack(side="left")
        duration_spin = tk.Spinbox(
            dur_row, from_=1, to=60, textvariable=self.duration_var, width=5,
            bg=COLORS["bg_elevated"], fg=COLORS["text"], relief="flat",
            highlightthickness=1, highlightbackground=COLORS["border"],
            buttonbackground=COLORS["bg_elevated"],
        )
        duration_spin.pack(side="left", padx=8)

        # Buttons
        btn_frame = tk.Frame(left, bg=COLORS["panel"])
        btn_frame.pack(fill="x", padx=16, pady=20)

        self._btn_generate = tk.Button(
            btn_frame, text=t(self.lang, "btn_generate"), command=self._regenerate_preview,
            bg=COLORS["accent"], fg="#0A1613", relief="flat", font=("Helvetica", 10, "bold"),
            activebackground="#46e2ca", padx=10, pady=8,
        )
        self._btn_generate.pack(fill="x", pady=(0, 8))

        self._btn_export_video = tk.Button(
            btn_frame, text=t(self.lang, "btn_export_video"), command=self._export_video,
            bg=COLORS["bg_elevated"], fg=COLORS["text"], relief="flat", font=("Helvetica", 10),
            activebackground=COLORS["border"], padx=10, pady=8,
        )
        self._btn_export_video.pack(fill="x", pady=4)

        self._btn_export_pdf = tk.Button(
            btn_frame, text=t(self.lang, "btn_export_pdf"), command=self._export_pdf,
            bg=COLORS["bg_elevated"], fg=COLORS["text"], relief="flat", font=("Helvetica", 10),
            activebackground=COLORS["border"], padx=10, pady=8,
        )
        self._btn_export_pdf.pack(fill="x", pady=4)

        self._btn_reset = tk.Button(
            btn_frame, text=t(self.lang, "btn_reset"), command=self._reset_fields,
            bg=COLORS["panel"], fg=COLORS["tally"], relief="flat", font=("Helvetica", 10),
            activebackground=COLORS["bg_elevated"], padx=10, pady=6,
        )
        self._btn_reset.pack(fill="x", pady=(12, 0))

        # ---- right: preview ----
        right = tk.LabelFrame(
            body, text=t(self.lang, "section_preview"),
            bg=COLORS["panel"], fg=COLORS["accent"], bd=1, relief="solid",
            font=("Helvetica", 11, "bold"), labelanchor="nw",
        )
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self._right_frame = right

        self.preview_label = tk.Label(right, bg="#0A0A0C")
        self.preview_label.pack(fill="both", expand=True, padx=16, pady=16)

        # ---- status bar ----
        status_frame = tk.Frame(self.root, bg=COLORS["bg_elevated"])
        status_frame.pack(fill="x", side="bottom")
        self.status_label = tk.Label(
            status_frame, textvariable=self.status_var, anchor="w",
            fg=COLORS["text_muted"], bg=COLORS["bg_elevated"], font=("Helvetica", 9),
            padx=16, pady=6,
        )
        self.status_label.pack(fill="x")

    def _apply_theme(self):
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

    # ------------------------------------------------------------- data --

    def _current_data(self) -> dict:
        return {
            "project": self.vars["project"].get(),
            "scene": self.vars["scene"].get(),
            "take": self.vars["take"].get() or "1",
            "director": self.vars["director"].get(),
            "camera": self.vars["camera"].get(),
            "notes": self.vars["notes"].get(),
            "date": self.generator.get_current_date(),
            "time": self.generator.get_current_time(),
            "project_label": t(self.lang, "field_project"),
            "scene_label": t(self.lang, "field_scene"),
            "take_label": t(self.lang, "field_take"),
            "director_label": t(self.lang, "field_director"),
            "camera_label": t(self.lang, "field_camera"),
            "date_label": {"ro": "Data", "en": "Date", "es": "Fecha"}[self.lang],
            "time_label": {"ro": "Ora", "en": "Time", "es": "Hora"}[self.lang],
        }

    # ---------------------------------------------------------- preview --

    def _on_field_change(self, *_args):
        self._save_settings()
        if self._debounce_job:
            self.root.after_cancel(self._debounce_job)
        self._debounce_job = self.root.after(250, self._regenerate_preview)

    def _regenerate_preview(self):
        self.status_var.set(t(self.lang, "status_generating"))
        image = self.generator.generate(self._current_data())

        # Fit the 1920x1080 slate into the available preview area, preserving
        # aspect ratio.
        panel_w = max(self.preview_label.winfo_width(), 480)
        panel_h = max(self.preview_label.winfo_height(), 270)
        target_w = panel_w
        target_h = int(target_w * 9 / 16)
        if target_h > panel_h:
            target_h = panel_h
            target_w = int(target_h * 16 / 9)

        resized = image.resize((max(target_w, 320), max(target_h, 180)), Image.LANCZOS)
        self._preview_photo = ImageTk.PhotoImage(resized)
        self.preview_label.configure(image=self._preview_photo)

        self.status_var.set(t(self.lang, "status_generated"))

    def _increment_take(self):
        try:
            current = int(self.vars["take"].get() or "0")
        except ValueError:
            current = 0
        self.vars["take"].set(str(current + 1))

    def _decrement_take(self):
        try:
            current = int(self.vars["take"].get() or "1")
        except ValueError:
            current = 1
        self.vars["take"].set(str(max(1, current - 1)))

    def _reset_fields(self):
        for key in FIELD_KEYS:
            self.vars[key].set("1" if key == "take" else "")

    # ------------------------------------------------------------ export --

    def _run_export(self, status_key: str, work_fn, success_dialog_key: str, failure_dialog_key: str):
        """Runs `work_fn()` on a background thread so the UI doesn't freeze,
        then reports success/failure back on the main thread."""
        self.status_var.set(t(self.lang, status_key))

        def worker():
            try:
                path = work_fn()
                self.root.after(0, lambda: self._on_export_success(success_dialog_key, path))
            except ExportError as e:
                self.root.after(0, lambda: self._on_export_error(failure_dialog_key, str(e)))
            except Exception as e:  # noqa: BLE001 - surface any unexpected error, don't crash the app
                self.root.after(0, lambda: self._on_export_error(failure_dialog_key, str(e)))

        threading.Thread(target=worker, daemon=True).start()

    def _on_export_success(self, dialog_key: str, path: str):
        self.status_var.set(t(self.lang, "status_export_done", path=os.path.basename(path)))
        messagebox.showinfo(t(self.lang, "dialog_success_title"), t(self.lang, dialog_key, path=path))

    def _on_export_error(self, dialog_key: str, error: str):
        self.status_var.set(t(self.lang, "status_export_failed"))
        if error == "ffmpeg_missing":
            messagebox.showwarning(t(self.lang, "dialog_error_title"), t(self.lang, "dialog_ffmpeg_missing"))
            return
        messagebox.showerror(t(self.lang, "dialog_error_title"), t(self.lang, dialog_key, error=error))

    def _export_video(self):
        if not ffmpeg_available():
            messagebox.showwarning(t(self.lang, "dialog_error_title"), t(self.lang, "dialog_ffmpeg_missing"))
            return

        initial_dir = self.settings.get("last_export_dir") or os.path.expanduser("~")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".mov",
            filetypes=[("QuickTime ProRes", "*.mov"), ("MP4 (H.264)", "*.mp4")],
            initialdir=initial_dir,
        )
        if not file_path:
            return
        self.settings["last_export_dir"] = os.path.dirname(file_path)
        save_config(self.settings)

        data = self._current_data()
        duration = self.duration_var.get()

        def work():
            self.exporter.export_video(data, file_path, duration_seconds=duration)
            return file_path

        self._run_export(
            "status_exporting_video", work,
            "dialog_export_video_success", "dialog_export_video_failed",
        )

    def _export_pdf(self):
        initial_dir = self.settings.get("last_export_dir") or os.path.expanduser("~")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialdir=initial_dir,
        )
        if not file_path:
            return
        self.settings["last_export_dir"] = os.path.dirname(file_path)
        save_config(self.settings)

        data = self._current_data()

        def work():
            self.exporter.export_pdf(data, file_path)
            return file_path

        self._run_export(
            "status_exporting_pdf", work,
            "dialog_export_pdf_success", "dialog_export_pdf_failed",
        )

    def _export_png(self):
        initial_dir = self.settings.get("last_export_dir") or os.path.expanduser("~")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png")],
            initialdir=initial_dir,
        )
        if not file_path:
            return
        self.settings["last_export_dir"] = os.path.dirname(file_path)
        save_config(self.settings)

        data = self._current_data()

        def work():
            self.exporter.export_png(data, file_path)
            return file_path

        self._run_export(
            "status_exporting_png", work,
            "dialog_export_png_success", "dialog_export_pdf_failed",
        )

    # --------------------------------------------------------- language --

    def _set_language(self, code: str):
        self.lang = code
        self.settings["language"] = code
        save_config(self.settings)
        self._refresh_language_texts()
        self._regenerate_preview()

    def _refresh_language_texts(self):
        self.root.title(t(self.lang, "app_title"))
        self._title_label.config(text=f"🎬 {t(self.lang, 'app_title')}")
        self._left_frame.config(text=t(self.lang, "section_info"))
        self._right_frame.config(text=t(self.lang, "section_preview"))
        self._duration_label.config(text=t(self.lang, "video_duration_label"))

        for key, label_widget in self._field_rows.items():
            label_widget.config(text=t(self.lang, f"field_{key}"))

        self._btn_generate.config(text=t(self.lang, "btn_generate"))
        self._btn_export_video.config(text=t(self.lang, "btn_export_video"))
        self._btn_export_pdf.config(text=t(self.lang, "btn_export_pdf"))
        self._btn_reset.config(text=t(self.lang, "btn_reset"))

        self.status_var.set(t(self.lang, "status_ready"))

        # Menus are cheap to rebuild entirely.
        self._build_menu()

    def _show_about(self):
        messagebox.showinfo(
            t(self.lang, "menu_about"),
            t(self.lang, "about_text", version=f"v{APP_VERSION}"),
        )

    # -------------------------------------------------------------- misc --

    def _save_settings(self):
        for key in FIELD_KEYS:
            self.settings[key] = self.vars[key].get()
        save_config(self.settings)

    def _on_close(self):
        self._save_settings()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def main():
    app = ClapperboardApp()
    app.run()


if __name__ == "__main__":
    main()
