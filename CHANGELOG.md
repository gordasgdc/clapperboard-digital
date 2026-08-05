# Changelog

All notable changes to Clapperboard Digital are documented here.

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
