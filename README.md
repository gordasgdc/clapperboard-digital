# 🎬 Clapperboard Digital

[🇷🇴 Română](README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md)

**Clapetă digitală pentru platoul de filmare — înlocuiește clasica clapetă.**
Generează un ecran cu informațiile filmării (proiect, scenă, take, dată, oră) pe care îl filmezi la începutul fiecărui clip.

---

## 📦 Descarcă și instalează

Ultima versiune este disponibilă în [Releases](https://github.com/gordasgdc/clapperboard-digital/releases).

| Platformă | Fișier | Instalare |
|---|---|---|
| **Mac** | `ClapperboardDigital.pkg` | dublu-click → urmează instalatorul |
| **Windows** | `ClapperboardDigital.exe` | dublu-click pentru a rula |

## 🚀 Caracteristici

- **Previzualizare live** — vezi ecranul actualizându-se instant, pe măsură ce completezi câmpurile
- **Export video** — MOV (ProRes) sau MP4 (H.264), cu durată personalizabilă
- **Export PDF** — document curat, gata de printat
- **Export imagine** — PNG la 1920×1080
- **Take rapid** — butoane +/− pentru a avansa numărul de take
- **RO / EN / ES** — interfață completă, comutabilă fără repornire
- **100% local** — fără cont, fără conexiune la internet necesară
- **Gratuit și open-source** (MIT)

## ⚠️ FFmpeg (doar pentru export video)

Exportul video necesită **FFmpeg** instalat separat pe sistem:

- **Mac**: `brew install ffmpeg`
- **Windows**: descarcă de pe [ffmpeg.org](https://ffmpeg.org) și adaugă la PATH

Dacă FFmpeg nu e găsit, aplicația afișează un mesaj clar cu instrucțiuni — exportul PDF și imagine funcționează fără nicio dependință suplimentară.

## 📖 Cum se folosește

1. **Completează informațiile** — proiect, scenă, take, regizor, cameră, notițe
2. **Verifică previzualizarea** — se actualizează automat, live
3. **Exportă** — ca video, PDF sau imagine
4. **Filmează ecranul** — la începutul clipului, ca referință pentru montaj

## 🛠️ Tehnologii

- Python + Tkinter (interfață nativă, cross-platform)
- Pillow pentru generarea imaginii
- FFmpeg pentru export video (dependință externă, opțională)
- ReportLab pentru export PDF
- PyInstaller pentru distribuție (.app/.pkg pe Mac, .exe pe Windows)

## 💻 Rulare din surse (pentru dezvoltare)

```bash
git clone https://github.com/gordasgdc/clapperboard-digital.git
cd clapperboard-digital
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python backend/app.py
```

## 📁 Structura proiectului

```
clapperboard-digital/
├── .github/workflows/       # build-mac.yml, build-windows.yml
├── backend/                 # app.py, clapperboard.py, export.py, config.py, translations.py
├── docs/                    # pagina de prezentare (GitHub Pages)
├── build/                   # fișiere .spec pentru PyInstaller
├── icon/                    # iconițe aplicație
├── requirements.txt
├── CHANGELOG.md
└── LICENSE
```

## 🏷️ Lansarea unei versiuni noi

```bash
git add .
git commit -m "Descriere modificări"
git push origin main

git tag -a v1.0.0 -m "Descriere versiune"
git push origin v1.0.0
```

> Notă de Git: tag-ul se creează **după** `git push`, niciodată înainte.

## 👤 Autor

**Cristi Gordas (GDC)** — colorist și editor video

- [GitHub](https://github.com/gordasgdc)
- [Facebook](https://web.facebook.com/cristiGDC)
- [YouTube](https://www.youtube.com/@cristigordas)

## 📄 Licență

MIT — vezi [LICENSE](LICENSE).
