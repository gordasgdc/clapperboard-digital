# Icons

`icon.png` (1024×1024) is the master icon — a black clapperboard slate with
yellow diagonal stripes, matching the app's own generated screen and the
`icon.icns` / `icon.ico` already included in this folder.

If you ever need to regenerate `icon.icns` / `icon.ico` from `icon.png`:

## From macOS
```bash
mkdir icon.iconset
sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png
iconutil -c icns icon.iconset -o icon.icns
rm -rf icon.iconset
```

## From any platform with Python + Pillow
```bash
pip install pillow
python - <<'PY'
from PIL import Image
img = Image.open("icon.png")
img.save("icon.ico", sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
PY
```

Until `icon.icns` / `icon.ico` exist, the build still works — the PyInstaller
specs fall back to the default icon automatically if the files are missing.
