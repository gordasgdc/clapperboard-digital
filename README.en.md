# 🎬 Clapperboard Digital

[🇷🇴 Română](README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md)

**A digital clapperboard for the film set — replaces the classic slate.**
Generates a shoot-information screen (project, scene, take, date, time) that you film at the start of every clip.

---

## 📦 Download & install

The latest version is available in [Releases](https://github.com/gordasgdc/clapperboard-digital/releases).

| Platform | File | Install |
|---|---|---|
| **Mac** | `ClapperboardDigital.pkg` | double-click → follow the installer |
| **Windows** | `ClapperboardDigital.exe` | double-click to run |

## 🚀 Features

- **Live preview** — watch the screen update instantly as you fill in the fields
- **Video export** — MOV (ProRes) or MP4 (H.264), with a customizable duration
- **PDF export** — a clean, print-ready document
- **Image export** — 1920×1080 PNG
- **Quick take** — +/− buttons to advance the take number
- **RO / EN / ES** — full interface, switchable without restarting
- **100% local** — no account, no internet connection required
- **Free and open-source** (MIT)

## ⚠️ FFmpeg (video export only)

Video export requires **FFmpeg** installed separately on your system:

- **Mac**: `brew install ffmpeg`
- **Windows**: download from [ffmpeg.org](https://ffmpeg.org) and add it to PATH

If FFmpeg isn't found, the app shows a clear message with instructions — PDF and image export work with no extra dependencies.

## 📖 How to use

1. **Fill in the info** — project, scene, take, director, camera, notes
2. **Check the preview** — updates automatically, live
3. **Export** — as video, PDF, or image
4. **Film the screen** — at the start of the clip, as an editing reference

## 🛠️ Tech stack

- Python + Tkinter (native, cross-platform interface)
- Pillow for image generation
- FFmpeg for video export (optional external dependency)
- ReportLab for PDF export
- PyInstaller for packaging (.app/.pkg on Mac, .exe on Windows)

## 💻 Running from source (development)

```bash
git clone https://github.com/gordasgdc/clapperboard-digital.git
cd clapperboard-digital
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python backend/app.py
```

## 📁 Project structure

```
clapperboard-digital/
├── .github/workflows/       # build-mac.yml, build-windows.yml
├── backend/                 # app.py, clapperboard.py, export.py, config.py, translations.py
├── docs/                    # presentation page (GitHub Pages)
├── build/                   # PyInstaller .spec files
├── icon/                    # app icons
├── requirements.txt
├── CHANGELOG.md
└── LICENSE
```

## 🏷️ Releasing a new version

```bash
git add .
git commit -m "Describe your changes"
git push origin main

git tag -a v1.0.0 -m "Version description"
git push origin v1.0.0
```

> Git note: create the tag **after** `git push`, never before.

## 👤 Author

**Cristi Gordas (GDC)** — colorist and video editor

- [GitHub](https://github.com/gordasgdc)
- [Facebook](https://web.facebook.com/cristiGDC)
- [YouTube](https://www.youtube.com/@cristigordas)

## 📄 License

MIT — see [LICENSE](LICENSE).
