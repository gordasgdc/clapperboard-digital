# 🎬 Clapperboard Digital

[🇷🇴 Română](README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md)

**Una claqueta digital para el set de rodaje — sustituye a la claqueta clásica.**
Genera una pantalla con la información del rodaje (proyecto, escena, toma, fecha, hora) que filmas al inicio de cada clip.

---

## 📦 Descargar e instalar

La última versión está disponible en [Releases](https://github.com/gordasgdc/clapperboard-digital/releases).

| Plataforma | Archivo | Instalación |
|---|---|---|
| **Mac** | `ClapperboardDigital.pkg` | doble clic → sigue el instalador |
| **Windows** | `ClapperboardDigital.exe` | doble clic para ejecutar |

## 🚀 Características

- **Vista previa en vivo** — mira la pantalla actualizarse al instante mientras rellenas los campos
- **Exportación de vídeo** — MOV (ProRes) o MP4 (H.264), con duración personalizable
- **Exportación PDF** — un documento limpio, listo para imprimir
- **Exportación de imagen** — PNG a 1920×1080
- **Toma rápida** — botones +/− para avanzar el número de toma
- **RO / EN / ES** — interfaz completa, cambiable sin reiniciar
- **100% local** — sin cuenta, sin necesidad de conexión a internet
- **Gratis y de código abierto** (MIT)

## ⚠️ FFmpeg (solo para exportación de vídeo)

La exportación de vídeo requiere **FFmpeg** instalado por separado en tu sistema:

- **Mac**: `brew install ffmpeg`
- **Windows**: descárgalo de [ffmpeg.org](https://ffmpeg.org) y añádelo al PATH

Si no se encuentra FFmpeg, la app muestra un mensaje claro con instrucciones — la exportación de PDF e imagen funciona sin ninguna dependencia adicional.

## 📖 Cómo se usa

1. **Rellena la información** — proyecto, escena, toma, director, cámara, notas
2. **Comprueba la vista previa** — se actualiza automáticamente, en vivo
3. **Exporta** — como vídeo, PDF o imagen
4. **Filma la pantalla** — al inicio del clip, como referencia de montaje

## 🛠️ Stack técnico

- Python + Tkinter (interfaz nativa, multiplataforma)
- Pillow para la generación de la imagen
- FFmpeg para la exportación de vídeo (dependencia externa, opcional)
- ReportLab para la exportación PDF
- PyInstaller para la distribución (.app/.pkg en Mac, .exe en Windows)

## 💻 Ejecutar desde el código fuente (desarrollo)

```bash
git clone https://github.com/gordasgdc/clapperboard-digital.git
cd clapperboard-digital
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python backend/app.py
```

## 📁 Estructura del proyecto

```
clapperboard-digital/
├── .github/workflows/       # build-mac.yml, build-windows.yml
├── backend/                 # app.py, clapperboard.py, export.py, config.py, translations.py
├── docs/                    # página de presentación (GitHub Pages)
├── build/                   # archivos .spec de PyInstaller
├── icon/                    # iconos de la app
├── requirements.txt
├── CHANGELOG.md
└── LICENSE
```

## 🏷️ Publicar una nueva versión

```bash
git add .
git commit -m "Describe tus cambios"
git push origin main

git tag -a v1.0.0 -m "Descripción de la versión"
git push origin v1.0.0
```

> Nota de Git: crea la etiqueta **después** de `git push`, nunca antes.

## 👤 Autor

**Cristi Gordas (GDC)** — colorista y editor de vídeo

- [GitHub](https://github.com/gordasgdc)
- [Facebook](https://web.facebook.com/cristiGDC)
- [YouTube](https://www.youtube.com/@cristigordas)

## 📄 Licencia

MIT — ver [LICENSE](LICENSE).
