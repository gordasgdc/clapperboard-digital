# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec — macOS build (.app)
# Run from the repository root:  pyinstaller build/build-mac.spec

import os

block_cipher = None
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(SPEC)), ".."))

# Fall back to PyInstaller's default icon if icon.icns wasn't committed,
# so a missing icon can never hard-fail the whole build.
_icon_path = os.path.join(ROOT, "icon", "icon.icns")
ICON = _icon_path if os.path.isfile(_icon_path) else None

a = Analysis(
    [os.path.join(ROOT, "backend", "app.py")],
    pathex=[os.path.join(ROOT, "backend")],
    binaries=[],
    datas=[],
    hiddenimports=[
        "PIL._tkinter_finder",
        "reportlab.graphics.barcode",
        "qrcode",
        "qrcode.image.pil",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ClapperboardDigital",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=ICON,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="ClapperboardDigital",
)

app = BUNDLE(
    coll,
    name="ClapperboardDigital.app",
    icon=ICON,
    bundle_identifier="com.gordasgdc.clapperboarddigital",
    info_plist={
        "CFBundleName": "Clapperboard Digital",
        "CFBundleDisplayName": "Clapperboard Digital",
        "CFBundleShortVersionString": "1.0.0",
        "CFBundleVersion": "1.0.0",
        "NSHighResolutionCapable": True,
        "LSMinimumSystemVersion": "11.0",
        "NSHumanReadableCopyright": "© Cristi Gordas (GDC)",
    },
)
