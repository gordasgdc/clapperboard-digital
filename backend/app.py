"""
Clapperboard Digital - main application window.

A focused, single-window Tkinter app: fill in the shoot info on the left,
watch the slate update live on the right, export when ready.
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog, colorchooser

from PIL import Image, ImageTk

from clapperboard import ClapperboardGenerator
from export import Exporter, ExportError, ffmpeg_available
from config import load_config, save_config, APP_VERSION
from translations import t
import templates as tpl_mod
import history as history_mod
import qr as qr_mod
import import_gdc

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
        tpl_mod.ensure_default_templates(self.settings)
        save_config(self.settings)

        self.generator = ClapperboardGenerator(customization=self.settings.get("customization"))
        self.exporter = Exporter(customization=self.settings.get("customization"))

        self.root = tk.Tk()
        self.root.title(t(self.lang, "app_title"))
        self.root.geometry("1150x820")
        self.root.minsize(900, 680)
        self.root.configure(bg=COLORS["bg"])

        self.vars = {key: tk.StringVar(value=self.settings.get(key, "")) for key in FIELD_KEYS}
        if not self.vars["take"].get():
            self.vars["take"].set("1")

        self.duration_var = tk.IntVar(value=5)
        self.qr_var = tk.BooleanVar(value=bool(self.settings.get("qr_enabled", False)))
        self.status_var = tk.StringVar(value=t(self.lang, "status_ready"))

        self._preview_photo = None  # keep a reference so Tk doesn't GC it
        self._debounce_job = None
        self._label_widgets = {}  # key -> widget, for live language switching

        self._build_menu()
        self._build_ui()
        self._apply_theme()

        for key in FIELD_KEYS:
            self.vars[key].trace_add("write", self._on_field_change)
        self.qr_var.trace_add("write", lambda *_: self._on_qr_toggle())

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
        file_menu.add_command(label=t(self.lang, "menu_import_gdc"), command=self._import_from_gdc)
        file_menu.add_separator()
        file_menu.add_command(label=t(self.lang, "menu_quit"), command=self._on_close)
        menubar.add_cascade(label=t(self.lang, "menu_file"), menu=file_menu)
        self._menu_file = file_menu

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label=t(self.lang, "menu_customize"), command=self._open_customize_dialog)
        settings_menu.add_command(label=t(self.lang, "menu_manage_templates"), command=self._open_template_manager)
        settings_menu.add_command(label=t(self.lang, "menu_history"), command=self._open_history)
        menubar.add_cascade(label=t(self.lang, "menu_settings"), menu=settings_menu)
        self._menu_settings = settings_menu

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

        # Quick templates row
        tpl_row = tk.Frame(left, bg=COLORS["panel"])
        tpl_row.pack(fill="x", padx=16, pady=(14, 4))
        self._templates_label = tk.Label(
            tpl_row, text=t(self.lang, "templates_label"),
            fg=COLORS["text_muted"], bg=COLORS["panel"], font=("Helvetica", 9),
        )
        self._templates_label.pack(anchor="w")
        self._templates_buttons_frame = tk.Frame(left, bg=COLORS["panel"])
        self._templates_buttons_frame.pack(fill="x", padx=16, pady=(4, 8))
        self._render_template_buttons()

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

        qr_row = tk.Frame(left, bg=COLORS["panel"])
        qr_row.pack(fill="x", padx=16, pady=(10, 0))
        self._qr_check = tk.Checkbutton(
            qr_row, text=t(self.lang, "qr_checkbox_label"), variable=self.qr_var,
            fg=COLORS["text_muted"], bg=COLORS["panel"], selectcolor=COLORS["bg_elevated"],
            activebackground=COLORS["panel"], activeforeground=COLORS["text"],
            font=("Helvetica", 10), anchor="w",
        )
        self._qr_check.pack(side="left")

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

        self._btn_fullscreen = tk.Button(
            btn_frame, text=t(self.lang, "btn_fullscreen"), command=self._show_fullscreen,
            bg=COLORS["bg_elevated"], fg=COLORS["amber"], relief="flat", font=("Helvetica", 10),
            activebackground=COLORS["border"], padx=10, pady=8,
        )
        self._btn_fullscreen.pack(fill="x", pady=4)

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
        image = self.generator.generate(self._current_data(), qr_image=self._current_qr_image())

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
        history_mod.upsert_history_entry(self.settings, self._current_data())
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

    # -------------------------------------------------------- templates --

    def _render_template_buttons(self):
        for widget in self._templates_buttons_frame.winfo_children():
            widget.destroy()

        templates = self.settings.get("templates", [])
        for tpl in templates:
            label = tpl_mod.template_label(tpl, self.lang)
            btn = tk.Button(
                self._templates_buttons_frame, text=label,
                command=lambda tp=tpl: self._apply_template(tp),
                bg=COLORS["bg_elevated"], fg=COLORS["text"], relief="flat",
                font=("Helvetica", 9), activebackground=COLORS["border"],
                padx=8, pady=4,
            )
            btn.pack(side="left", padx=(0, 6), pady=2)

        manage_btn = tk.Button(
            self._templates_buttons_frame, text="⚙", width=3,
            command=self._open_template_manager,
            bg=COLORS["panel"], fg=COLORS["text_muted"], relief="flat",
            font=("Helvetica", 9), activebackground=COLORS["border"],
        )
        manage_btn.pack(side="left", padx=(4, 0), pady=2)

    def _apply_template(self, template: dict):
        placeholder = tpl_mod.extract_placeholder(template.get("project", ""))
        placeholder_value = ""
        if placeholder:
            placeholder_value = simpledialog.askstring(
                tpl_mod.template_label(template, self.lang), f"{placeholder.capitalize()}:",
                parent=self.root,
            ) or ""

        filled = tpl_mod.apply_template(template, placeholder_value)
        for key, value in filled.items():
            if value:
                self.vars[key].set(value)
        self.vars["take"].set("1")

    def _open_template_manager(self):
        win = tk.Toplevel(self.root)
        win.title(t(self.lang, "menu_manage_templates"))
        win.configure(bg=COLORS["bg"])
        win.geometry("520x420")

        list_frame = tk.Frame(win, bg=COLORS["bg"])
        list_frame.pack(fill="both", expand=True, padx=16, pady=16)

        def refresh_list():
            for w in list_frame.winfo_children():
                w.destroy()
            for tpl in self.settings.get("templates", []):
                row = tk.Frame(list_frame, bg=COLORS["panel"])
                row.pack(fill="x", pady=4)
                label = tpl_mod.template_label(tpl, self.lang)
                tk.Label(
                    row, text=f"{label}  —  {tpl.get('project', '')}", anchor="w",
                    bg=COLORS["panel"], fg=COLORS["text"], font=("Helvetica", 10),
                ).pack(side="left", fill="x", expand=True, padx=10, pady=8)
                tk.Button(
                    row, text="✕", command=lambda tp=tpl: delete_template(tp),
                    bg=COLORS["panel"], fg=COLORS["tally"], relief="flat",
                    activebackground=COLORS["bg_elevated"],
                ).pack(side="right", padx=8)

        def delete_template(tpl):
            self.settings["templates"] = [x for x in self.settings.get("templates", []) if x.get("id") != tpl.get("id")]
            save_config(self.settings)
            refresh_list()
            self._render_template_buttons()

        def add_template():
            name = simpledialog.askstring(t(self.lang, "menu_manage_templates"), t(self.lang, "new_template_name"), parent=win)
            if not name:
                return
            project = simpledialog.askstring(name, t(self.lang, "field_project"), parent=win) or name
            scene = simpledialog.askstring(name, t(self.lang, "field_scene"), parent=win) or ""
            new_tpl = tpl_mod.new_template(name, project, scene, "", "", "")
            self.settings.setdefault("templates", []).append(new_tpl)
            save_config(self.settings)
            refresh_list()
            self._render_template_buttons()

        refresh_list()

        add_btn = tk.Button(
            win, text=t(self.lang, "add_template_btn"), command=add_template,
            bg=COLORS["accent"], fg="#0A1613", relief="flat", font=("Helvetica", 10, "bold"),
            padx=10, pady=8,
        )
        add_btn.pack(fill="x", padx=16, pady=(0, 16))

    # ----------------------------------------------------------- history --

    def _open_history(self):
        win = tk.Toplevel(self.root)
        win.title(t(self.lang, "menu_history"))
        win.configure(bg=COLORS["bg"])
        win.geometry("560x420")

        list_frame = tk.Frame(win, bg=COLORS["bg"])
        list_frame.pack(fill="both", expand=True, padx=16, pady=16)

        entries = self.settings.get("history", [])
        if not entries:
            tk.Label(
                list_frame, text=t(self.lang, "no_history"),
                bg=COLORS["bg"], fg=COLORS["text_muted"], font=("Helvetica", 10),
            ).pack(pady=20)
        else:
            for entry in entries:
                row = tk.Frame(list_frame, bg=COLORS["panel"])
                row.pack(fill="x", pady=4)
                tk.Label(
                    row, text=history_mod.entry_label(entry), anchor="w",
                    bg=COLORS["panel"], fg=COLORS["text"], font=("Helvetica", 10),
                ).pack(side="left", fill="x", expand=True, padx=10, pady=8)
                tk.Button(
                    row, text=t(self.lang, "load_history_btn"),
                    command=lambda e=entry: self._load_history_entry(e, win),
                    bg=COLORS["bg_elevated"], fg=COLORS["accent"], relief="flat",
                    font=("Helvetica", 9), activebackground=COLORS["border"],
                ).pack(side="right", padx=8)

        def clear_all():
            if messagebox.askyesno(t(self.lang, "menu_history"), t(self.lang, "confirm_clear_history"), parent=win):
                history_mod.clear_history(self.settings)
                save_config(self.settings)
                win.destroy()

        tk.Button(
            win, text=t(self.lang, "clear_history_btn"), command=clear_all,
            bg=COLORS["panel"], fg=COLORS["tally"], relief="flat", font=("Helvetica", 10),
            padx=10, pady=8,
        ).pack(fill="x", padx=16, pady=(0, 16))

    def _load_history_entry(self, entry: dict, window: tk.Toplevel = None):
        self.vars["project"].set(entry.get("project", ""))
        self.vars["scene"].set(entry.get("scene", ""))
        self.vars["director"].set(entry.get("director", ""))
        self.vars["camera"].set(entry.get("camera", ""))
        self.vars["notes"].set(entry.get("notes", ""))
        self.vars["take"].set(str(entry.get("takes", 1) + 1))
        if window:
            window.destroy()

    # ------------------------------------------------------------- QR ----

    def _on_qr_toggle(self):
        self.settings["qr_enabled"] = bool(self.qr_var.get())
        save_config(self.settings)
        self._regenerate_preview()

    def _current_qr_image(self):
        if not self.qr_var.get():
            return None
        return qr_mod.generate_qr_image(self._current_data())

    # -------------------------------------------------------- fullscreen --

    def _show_fullscreen(self):
        win = tk.Toplevel(self.root)
        win.attributes("-fullscreen", True)
        win.configure(bg="black")
        win.focus_force()

        image = self.generator.generate(self._current_data(), qr_image=self._current_qr_image())
        screen_w = win.winfo_screenwidth()
        screen_h = win.winfo_screenheight()
        target_w = screen_w
        target_h = int(target_w * 9 / 16)
        if target_h > screen_h:
            target_h = screen_h
            target_w = int(target_h * 16 / 9)
        resized = image.resize((max(target_w, 320), max(target_h, 180)), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized)

        label = tk.Label(win, image=photo, bg="black")
        label.image = photo  # keep reference
        label.pack(expand=True)

        hint = tk.Label(
            win, text=t(self.lang, "fullscreen_hint"), fg="#888888", bg="black", font=("Helvetica", 10),
        )
        hint.place(relx=0.5, rely=0.98, anchor="s")

        def close(_event=None):
            win.destroy()

        win.bind("<Escape>", close)
        win.bind("<Button-1>", close)
        label.bind("<Button-1>", close)

    # ------------------------------------------------------- customize ----

    def _open_customize_dialog(self):
        current = dict(self.settings.get("customization", {}))
        working = dict(current)

        win = tk.Toplevel(self.root)
        win.title(t(self.lang, "customize_title"))
        win.configure(bg=COLORS["bg"])
        win.geometry("420x480")

        body = tk.Frame(win, bg=COLORS["bg"])
        body.pack(fill="both", expand=True, padx=18, pady=18)

        swatches = {}

        def make_color_row(label_key, settings_key):
            row = tk.Frame(body, bg=COLORS["bg"])
            row.pack(fill="x", pady=6)
            tk.Label(
                row, text=t(self.lang, label_key), anchor="w", width=22,
                bg=COLORS["bg"], fg=COLORS["text_muted"], font=("Helvetica", 10),
            ).pack(side="left")
            swatch = tk.Label(
                row, bg=working.get(settings_key, "#000000"), width=6, relief="flat",
                highlightthickness=1, highlightbackground=COLORS["border"],
            )
            swatch.pack(side="left", padx=8, ipady=6)
            swatches[settings_key] = swatch

            def pick(sk=settings_key, sw=swatch):
                color = colorchooser.askcolor(color=working.get(sk, "#000000"), parent=win)
                if color and color[1]:
                    working[sk] = color[1]
                    sw.configure(bg=color[1])

            swatch.bind("<Button-1>", lambda e, p=pick: p())

        make_color_row("customize_bg", "bg")
        make_color_row("customize_text", "text")
        make_color_row("customize_accent", "accent")
        make_color_row("customize_footer", "footer")

        font_row = tk.Frame(body, bg=COLORS["bg"])
        font_row.pack(fill="x", pady=(14, 6))
        tk.Label(
            font_row, text=t(self.lang, "customize_font"), anchor="w", width=22,
            bg=COLORS["bg"], fg=COLORS["text_muted"], font=("Helvetica", 10),
        ).pack(side="left")
        font_choice = tk.StringVar(value=working.get("font_style", "sans_bold"))
        font_options = {
            t(self.lang, "customize_font_sans"): "sans_bold",
            t(self.lang, "customize_font_serif"): "serif",
        }
        reverse_options = {v: k for k, v in font_options.items()}
        font_menu = ttk.Combobox(
            font_row, values=list(font_options.keys()), state="readonly", width=18,
        )
        font_menu.set(reverse_options.get(font_choice.get(), list(font_options.keys())[0]))
        font_menu.pack(side="left")

        logo_row = tk.Frame(body, bg=COLORS["bg"])
        logo_row.pack(fill="x", pady=(14, 6))
        tk.Label(
            logo_row, text=t(self.lang, "customize_logo"), anchor="w",
            bg=COLORS["bg"], fg=COLORS["text_muted"], font=("Helvetica", 10),
        ).pack(anchor="w")

        logo_path_var = tk.StringVar(value=working.get("logo_path", ""))
        logo_label = tk.Label(
            logo_row, textvariable=logo_path_var, anchor="w", wraplength=380,
            bg=COLORS["bg"], fg=COLORS.get("text_faint", COLORS["text_muted"]),
            font=("Helvetica", 8),
        )
        logo_label.pack(anchor="w", pady=(4, 4))

        def choose_logo():
            path = filedialog.askopenfilename(filetypes=[("PNG", "*.png")], parent=win)
            if path:
                working["logo_path"] = path
                logo_path_var.set(path)

        def remove_logo():
            working["logo_path"] = ""
            logo_path_var.set("")

        logo_btns = tk.Frame(logo_row, bg=COLORS["bg"])
        logo_btns.pack(anchor="w")
        tk.Button(
            logo_btns, text=t(self.lang, "customize_choose_logo"), command=choose_logo,
            bg=COLORS["bg_elevated"], fg=COLORS["text"], relief="flat", padx=8, pady=4,
        ).pack(side="left", padx=(0, 6))
        tk.Button(
            logo_btns, text=t(self.lang, "customize_remove_logo"), command=remove_logo,
            bg=COLORS["panel"], fg=COLORS["tally"], relief="flat", padx=8, pady=4,
        ).pack(side="left")

        def do_save():
            working["font_style"] = font_options.get(font_menu.get(), "sans_bold")
            self.settings["customization"] = working
            save_config(self.settings)
            self.generator = ClapperboardGenerator(customization=working)
            self.exporter.update_customization(working)
            self._regenerate_preview()
            self.status_var.set(t(self.lang, "customize_saved"))
            win.destroy()

        def do_reset():
            from config import DEFAULT_SETTINGS
            default_custom = dict(DEFAULT_SETTINGS["customization"])
            working.clear()
            working.update(default_custom)
            for key, swatch in swatches.items():
                swatch.configure(bg=working.get(key, "#000000"))
            font_menu.set(reverse_options.get(working.get("font_style", "sans_bold"), list(font_options.keys())[0]))
            logo_path_var.set("")

        btn_row = tk.Frame(win, bg=COLORS["bg"])
        btn_row.pack(fill="x", padx=18, pady=(0, 18))
        tk.Button(
            btn_row, text=t(self.lang, "customize_reset"), command=do_reset,
            bg=COLORS["panel"], fg=COLORS["text_muted"], relief="flat", padx=10, pady=8,
        ).pack(side="left")
        tk.Button(
            btn_row, text=t(self.lang, "customize_save"), command=do_save,
            bg=COLORS["accent"], fg="#0A1613", relief="flat", font=("Helvetica", 10, "bold"),
            padx=10, pady=8,
        ).pack(side="right")

    # ------------------------------------------------------- import GDC ---

    def _import_from_gdc(self):
        path = filedialog.askopenfilename(
            title=t(self.lang, "import_gdc_choose_file"),
            filetypes=[("JSON", "*.json")],
        )
        if not path:
            return

        try:
            projects = import_gdc.load_gdc_projects(path)
        except import_gdc.ImportError_:
            messagebox.showerror(t(self.lang, "dialog_error_title"), t(self.lang, "import_gdc_invalid_file"))
            return

        if not projects:
            messagebox.showinfo(t(self.lang, "import_gdc_title"), t(self.lang, "import_gdc_no_projects"))
            return

        win = tk.Toplevel(self.root)
        win.title(t(self.lang, "import_gdc_title"))
        win.configure(bg=COLORS["bg"])
        win.geometry("460x420")

        tk.Label(
            win, text=t(self.lang, "import_gdc_select_project"), anchor="w",
            bg=COLORS["bg"], fg=COLORS["text_muted"], font=("Helvetica", 10),
        ).pack(fill="x", padx=16, pady=(16, 6))

        list_frame = tk.Frame(win, bg=COLORS["bg"])
        list_frame.pack(fill="both", expand=True, padx=16)

        listbox = tk.Listbox(
            list_frame, bg=COLORS["panel"], fg=COLORS["text"], relief="flat",
            selectbackground=COLORS["accent"], selectforeground="#0A1613",
            font=("Helvetica", 10), highlightthickness=1, highlightbackground=COLORS["border"],
        )
        listbox.pack(fill="both", expand=True)
        for p in projects:
            suffix = f" — {p['client_name']}" if p.get("client_name") else ""
            listbox.insert("end", f"{p['title']}{suffix}")

        def do_import():
            selection = listbox.curselection()
            if not selection:
                return
            project = projects[selection[0]]
            form_data = import_gdc.project_to_form_data(project)
            for key, value in form_data.items():
                self.vars[key].set(value)
            self.vars["take"].set("1")
            self.status_var.set(t(self.lang, "import_gdc_success"))
            win.destroy()

        tk.Button(
            win, text=t(self.lang, "import_gdc_import_btn"), command=do_import,
            bg=COLORS["accent"], fg="#0A1613", relief="flat", font=("Helvetica", 10, "bold"),
            padx=10, pady=8,
        ).pack(fill="x", padx=16, pady=16)

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
        qr_image = self._current_qr_image()

        def work():
            self.exporter.export_video(data, file_path, duration_seconds=duration, qr_image=qr_image)
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
        qr_image = self._current_qr_image()

        def work():
            self.exporter.export_pdf(data, file_path, qr_image=qr_image)
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
        qr_image = self._current_qr_image()

        def work():
            self.exporter.export_png(data, file_path, qr_image=qr_image)
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
        self._btn_fullscreen.config(text=t(self.lang, "btn_fullscreen"))
        self._btn_reset.config(text=t(self.lang, "btn_reset"))
        self._templates_label.config(text=t(self.lang, "templates_label"))
        self._qr_check.config(text=t(self.lang, "qr_checkbox_label"))
        self._render_template_buttons()

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
        history_mod.upsert_history_entry(self.settings, self._current_data())
        save_config(self.settings)
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def main():
    app = ClapperboardApp()
    app.run()


if __name__ == "__main__":
    main()
