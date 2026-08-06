# Changelog

All notable changes to Clapperboard Digital are documented here.

## [1.1.0] — Unreleased

### Added
- **Quick templates**: Nuntă, Reclamă, Interviu, Documentar built in, with `{placeholder}` prompts (e.g. "Nunta {client}"); fully manageable (add/edit/delete) from Settings
- **Take history**: tracks the highest take reached per project/scene, viewable and reloadable from Settings → Istoric take-uri
- **QR code embedding**: optional checkbox to bake a scannable QR (project/scene/take/director/camera/date/time) into the generated screen, video, and PDF exports
- **Fullscreen slate view**: dedicated fullscreen window for filming the screen directly, exit via Esc or click
- **Appearance customization**: background/text/accent/footer colors, sans-serif or serif font, optional logo overlay — Settings → Personalizare aspect
- **Import from GDC Production Manager**: pick a project from a GDC PM JSON export to prefill the slate
- Window resized to fit all the new controls without clipping

## [1.0.0] — Unreleased

First public version.

### Added
- Live-updating slate preview (project, scene, take, director, camera, date, time, notes)
- Video export (MOV/ProRes, MP4/H.264) via FFmpeg, with graceful detection and a clear
  installation message when FFmpeg isn't available
- PDF export (clean, print-ready single page)
- PNG image export (1920×1080)
- Quick take +/− stepper
- RO/EN/ES interface, switchable live without restarting the app
- Settings persisted between sessions (project, scene, director, camera, language, last export folder)
- Background-threaded exports so the interface never freezes
- GitHub Actions workflows for automated Mac and Windows builds on tag push
- GitHub Pages presentation site (`docs/index.html`)
