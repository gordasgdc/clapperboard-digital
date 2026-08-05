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
