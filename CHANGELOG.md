# Changelog

All notable changes to Clapperboard Digital are documented here.

## [1.1.1] — Unreleased

### Added
- **PWA language switcher** (RO/EN/ES, small pill buttons top-right, Romanian by default): the desktop app already had full RO/EN/ES translations (`backend/translations.py`) — the PWA was Romanian-only until now. Covers every label, button, dialog, toast and confirm on the slate; choice is remembered per device (localStorage)
- **PWA user guide**: an ⓘ button in the topbar opens a detailed, document-style usage guide (10 numbered steps covering the info fields, timecode, the CLAP button and its sync-friendly sound, fullscreen, QR code, history, export, language switcher, tablet install, and the local-only data model) — fully translated RO/EN/ES

### Changed
- **PWA slate redesigned to resemble a professional timecode slate** (Deity TC-SL1 reference): red LED-style timecode display (was white/yellow) with subtle dot-matrix texture and glow, a colorful chevron stripe (green/yellow/blue/red fading to grayscale, generated as SVG) replacing the diagonal yellow tape pattern, and the info fields reorganized into a white/black instrument-panel grid (Cameră/Scenă/Take, Proiect, Regizor/Notițe, Dată/Ora) instead of a plain icon+text list — removed all emoji from the slate face itself
- Director and notes are now shown live on the slate (previously only captured in the edit form and exports)
- Refined button design: removed emoji clutter from primary action buttons (Generează ecran, Exportă video/PDF, Ecran complet, Resetează), switched them to uppercase labels for a more precise, instrument-panel feel — consistent with the redesigned PWA
- **Clap sound redesigned for audio sync**: shortened from ~180ms to ~50ms with a much steeper decay, so it reads as a single sharp spike in a waveform (easy to find and align to in an editor) instead of a soft, spread-out burst

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
