"""
Clapperboard Digital - interface translations (RO / EN / ES).
"""

TRANSLATIONS = {
    "ro": {
        "app_title": "Clapperboard Digital",
        "menu_file": "Fișier",
        "menu_export_video": "Exportă video…",
        "menu_export_pdf": "Exportă PDF…",
        "menu_export_png": "Exportă imagine (PNG)…",
        "menu_quit": "Ieșire",
        "menu_language": "Limbă",
        "menu_help": "Ajutor",
        "menu_about": "Despre Clapperboard Digital",

        "section_info": "Informații filmare",
        "section_preview": "Previzualizare",

        "field_project": "Proiect",
        "field_scene": "Scenă",
        "field_take": "Take",
        "field_director": "Regizor",
        "field_camera": "Cameră",
        "field_notes": "Notițe",

        "btn_generate": "🎬 Generează ecran",
        "btn_export_video": "🎞️ Exportă video",
        "btn_export_pdf": "📄 Exportă PDF",
        "btn_reset": "↺ Resetează",
        "btn_new_take": "Take nou (+1)",

        "status_ready": "Gata",
        "status_generating": "Se generează ecranul…",
        "status_generated": "Ecran generat",
        "status_exporting_video": "Se exportă video…",
        "status_exporting_pdf": "Se exportă PDF…",
        "status_exporting_png": "Se exportă imagine…",
        "status_export_done": "Export finalizat: {path}",
        "status_export_failed": "Export eșuat",

        "dialog_success_title": "Succes",
        "dialog_error_title": "Eroare",
        "dialog_export_video_success": "Video exportat la:\n{path}",
        "dialog_export_pdf_success": "PDF exportat la:\n{path}",
        "dialog_export_png_success": "Imagine exportată la:\n{path}",
        "dialog_ffmpeg_missing": (
            "FFmpeg nu a fost găsit pe acest calculator.\n\n"
            "Exportul video necesită FFmpeg instalat separat.\n"
            "Mac: instalează cu 'brew install ffmpeg'\n"
            "Windows: descarcă de pe ffmpeg.org și adaugă la PATH.\n\n"
            "Exportul PDF și imagine funcționează fără FFmpeg."
        ),
        "dialog_export_video_failed": "Exportul video a eșuat:\n{error}",
        "dialog_export_pdf_failed": "Exportul PDF a eșuat:\n{error}",

        "video_duration_label": "Durată clip (secunde):",

        "about_text": (
            "Clapperboard Digital {version}\n\n"
            "Clapetă digitală pentru platoul de filmare.\n"
            "Generează un ecran cu informațiile filmării, "
            "exportabil ca video, PDF sau imagine.\n\n"
            "© Cristi Gordas (GDC)"
        ),

        "menu_settings": "Setări",
        "menu_customize": "Personalizare aspect…",
        "menu_manage_templates": "Gestionează șabloane…",
        "menu_history": "Istoric take-uri…",
        "menu_import_gdc": "Importă din GDC Production Manager…",

        "templates_label": "📋 Șabloane rapide",
        "qr_checkbox_label": "Include cod QR pe ecran",
        "btn_fullscreen": "⛶ Ecran complet",

        "new_template_name": "Nume șablon:",
        "add_template_btn": "➕ Adaugă șablon",

        "no_history": "Niciun istoric încă.",
        "load_history_btn": "Încarcă",
        "clear_history_btn": "🗑 Șterge istoric",
        "confirm_clear_history": "Ștergi tot istoricul de take-uri? Acțiunea nu poate fi anulată.",

        "customize_title": "Personalizare aspect",
        "customize_bg": "Culoare fundal",
        "customize_text": "Culoare text",
        "customize_accent": "Culoare accent (dungi/etichete)",
        "customize_footer": "Culoare footer",
        "customize_font": "Font",
        "customize_font_sans": "Sans-serif (implicit)",
        "customize_font_serif": "Serif",
        "customize_logo": "Logo (PNG, opțional)",
        "customize_choose_logo": "Alege fișier…",
        "customize_remove_logo": "Elimină logo",
        "customize_save": "Salvează",
        "customize_reset": "Resetează la implicit",
        "customize_saved": "Personalizare salvată",

        "import_gdc_title": "Importă din GDC Production Manager",
        "import_gdc_choose_file": "Alege fișierul export JSON…",
        "import_gdc_select_project": "Selectează un proiect:",
        "import_gdc_import_btn": "Importă",
        "import_gdc_invalid_file": "Fișierul nu este un export valid din GDC Production Manager.",
        "import_gdc_no_projects": "Fișierul nu conține niciun proiect.",
        "import_gdc_success": "Proiect importat cu succes.",

        "fullscreen_hint": "Apasă ESC sau click pentru a ieși",
    },
    "en": {
        "app_title": "Clapperboard Digital",
        "menu_file": "File",
        "menu_export_video": "Export video…",
        "menu_export_pdf": "Export PDF…",
        "menu_export_png": "Export image (PNG)…",
        "menu_quit": "Quit",
        "menu_language": "Language",
        "menu_help": "Help",
        "menu_about": "About Clapperboard Digital",

        "section_info": "Shoot information",
        "section_preview": "Preview",

        "field_project": "Project",
        "field_scene": "Scene",
        "field_take": "Take",
        "field_director": "Director",
        "field_camera": "Camera",
        "field_notes": "Notes",

        "btn_generate": "🎬 Generate screen",
        "btn_export_video": "🎞️ Export video",
        "btn_export_pdf": "📄 Export PDF",
        "btn_reset": "↺ Reset",
        "btn_new_take": "New take (+1)",

        "status_ready": "Ready",
        "status_generating": "Generating screen…",
        "status_generated": "Screen generated",
        "status_exporting_video": "Exporting video…",
        "status_exporting_pdf": "Exporting PDF…",
        "status_exporting_png": "Exporting image…",
        "status_export_done": "Export complete: {path}",
        "status_export_failed": "Export failed",

        "dialog_success_title": "Success",
        "dialog_error_title": "Error",
        "dialog_export_video_success": "Video exported to:\n{path}",
        "dialog_export_pdf_success": "PDF exported to:\n{path}",
        "dialog_export_png_success": "Image exported to:\n{path}",
        "dialog_ffmpeg_missing": (
            "FFmpeg was not found on this computer.\n\n"
            "Video export requires FFmpeg to be installed separately.\n"
            "Mac: install with 'brew install ffmpeg'\n"
            "Windows: download from ffmpeg.org and add it to PATH.\n\n"
            "PDF and image export work without FFmpeg."
        ),
        "dialog_export_video_failed": "Video export failed:\n{error}",
        "dialog_export_pdf_failed": "PDF export failed:\n{error}",

        "video_duration_label": "Clip duration (seconds):",

        "about_text": (
            "Clapperboard Digital {version}\n\n"
            "A digital clapperboard for the set.\n"
            "Generates a shoot-information screen, exportable "
            "as video, PDF, or image.\n\n"
            "© Cristi Gordas (GDC)"
        ),

        "menu_settings": "Settings",
        "menu_customize": "Customize appearance…",
        "menu_manage_templates": "Manage templates…",
        "menu_history": "Take history…",
        "menu_import_gdc": "Import from GDC Production Manager…",

        "templates_label": "📋 Quick templates",
        "qr_checkbox_label": "Include QR code on screen",
        "btn_fullscreen": "⛶ Fullscreen",

        "new_template_name": "Template name:",
        "add_template_btn": "➕ Add template",

        "no_history": "No history yet.",
        "load_history_btn": "Load",
        "clear_history_btn": "🗑 Clear history",
        "confirm_clear_history": "Delete all take history? This can't be undone.",

        "customize_title": "Customize appearance",
        "customize_bg": "Background color",
        "customize_text": "Text color",
        "customize_accent": "Accent color (stripes/labels)",
        "customize_footer": "Footer color",
        "customize_font": "Font",
        "customize_font_sans": "Sans-serif (default)",
        "customize_font_serif": "Serif",
        "customize_logo": "Logo (PNG, optional)",
        "customize_choose_logo": "Choose file…",
        "customize_remove_logo": "Remove logo",
        "customize_save": "Save",
        "customize_reset": "Reset to default",
        "customize_saved": "Appearance saved",

        "import_gdc_title": "Import from GDC Production Manager",
        "import_gdc_choose_file": "Choose the exported JSON file…",
        "import_gdc_select_project": "Select a project:",
        "import_gdc_import_btn": "Import",
        "import_gdc_invalid_file": "That file isn't a valid GDC Production Manager export.",
        "import_gdc_no_projects": "The file doesn't contain any projects.",
        "import_gdc_success": "Project imported successfully.",

        "fullscreen_hint": "Press ESC or click to exit",
    },
    "es": {
        "app_title": "Clapperboard Digital",
        "menu_file": "Archivo",
        "menu_export_video": "Exportar vídeo…",
        "menu_export_pdf": "Exportar PDF…",
        "menu_export_png": "Exportar imagen (PNG)…",
        "menu_quit": "Salir",
        "menu_language": "Idioma",
        "menu_help": "Ayuda",
        "menu_about": "Acerca de Clapperboard Digital",

        "section_info": "Información del rodaje",
        "section_preview": "Vista previa",

        "field_project": "Proyecto",
        "field_scene": "Escena",
        "field_take": "Toma",
        "field_director": "Director",
        "field_camera": "Cámara",
        "field_notes": "Notas",

        "btn_generate": "🎬 Generar pantalla",
        "btn_export_video": "🎞️ Exportar vídeo",
        "btn_export_pdf": "📄 Exportar PDF",
        "btn_reset": "↺ Restablecer",
        "btn_new_take": "Toma nueva (+1)",

        "status_ready": "Listo",
        "status_generating": "Generando pantalla…",
        "status_generated": "Pantalla generada",
        "status_exporting_video": "Exportando vídeo…",
        "status_exporting_pdf": "Exportando PDF…",
        "status_exporting_png": "Exportando imagen…",
        "status_export_done": "Exportación completa: {path}",
        "status_export_failed": "Exportación fallida",

        "dialog_success_title": "Éxito",
        "dialog_error_title": "Error",
        "dialog_export_video_success": "Vídeo exportado a:\n{path}",
        "dialog_export_pdf_success": "PDF exportado a:\n{path}",
        "dialog_export_png_success": "Imagen exportada a:\n{path}",
        "dialog_ffmpeg_missing": (
            "No se encontró FFmpeg en este equipo.\n\n"
            "La exportación de vídeo requiere FFmpeg instalado por separado.\n"
            "Mac: instala con 'brew install ffmpeg'\n"
            "Windows: descárgalo de ffmpeg.org y añádelo al PATH.\n\n"
            "La exportación de PDF e imagen funciona sin FFmpeg."
        ),
        "dialog_export_video_failed": "La exportación de vídeo falló:\n{error}",
        "dialog_export_pdf_failed": "La exportación de PDF falló:\n{error}",

        "video_duration_label": "Duración del clip (segundos):",

        "about_text": (
            "Clapperboard Digital {version}\n\n"
            "Una claqueta digital para el set de rodaje.\n"
            "Genera una pantalla con la información del rodaje, "
            "exportable como vídeo, PDF o imagen.\n\n"
            "© Cristi Gordas (GDC)"
        ),

        "menu_settings": "Ajustes",
        "menu_customize": "Personalizar aspecto…",
        "menu_manage_templates": "Gestionar plantillas…",
        "menu_history": "Historial de tomas…",
        "menu_import_gdc": "Importar desde GDC Production Manager…",

        "templates_label": "📋 Plantillas rápidas",
        "qr_checkbox_label": "Incluir código QR en la pantalla",
        "btn_fullscreen": "⛶ Pantalla completa",

        "new_template_name": "Nombre de la plantilla:",
        "add_template_btn": "➕ Añadir plantilla",

        "no_history": "Aún no hay historial.",
        "load_history_btn": "Cargar",
        "clear_history_btn": "🗑 Borrar historial",
        "confirm_clear_history": "¿Eliminar todo el historial de tomas? No se puede deshacer.",

        "customize_title": "Personalizar aspecto",
        "customize_bg": "Color de fondo",
        "customize_text": "Color de texto",
        "customize_accent": "Color de acento (franjas/etiquetas)",
        "customize_footer": "Color del pie",
        "customize_font": "Fuente",
        "customize_font_sans": "Sans-serif (predeterminada)",
        "customize_font_serif": "Serif",
        "customize_logo": "Logo (PNG, opcional)",
        "customize_choose_logo": "Elegir archivo…",
        "customize_remove_logo": "Quitar logo",
        "customize_save": "Guardar",
        "customize_reset": "Restablecer valores predeterminados",
        "customize_saved": "Aspecto guardado",

        "import_gdc_title": "Importar desde GDC Production Manager",
        "import_gdc_choose_file": "Elige el archivo JSON exportado…",
        "import_gdc_select_project": "Selecciona un proyecto:",
        "import_gdc_import_btn": "Importar",
        "import_gdc_invalid_file": "Ese archivo no es una exportación válida de GDC Production Manager.",
        "import_gdc_no_projects": "El archivo no contiene ningún proyecto.",
        "import_gdc_success": "Proyecto importado correctamente.",

        "fullscreen_hint": "Pulsa ESC o toca la pantalla para salir",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    dict_ = TRANSLATIONS.get(lang, TRANSLATIONS["ro"])
    text = dict_.get(key) or TRANSLATIONS["ro"].get(key) or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text
