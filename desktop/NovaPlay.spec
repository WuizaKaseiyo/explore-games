# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller build spec for the NovaPlay desktop player.

Build (from the repo root, with the project .venv active or referenced):

    .venv/bin/pyinstaller desktop/NovaPlay.spec --noconfirm

Output:
    dist/NovaPlay/            onedir bundle (Windows/Linux: ship this folder)
    dist/NovaPlay.app         macOS app bundle (built additionally on darwin)

Only each game's <id>.py and metadata.json are bundled — the PNG screenshots,
run-archives, logs and mechanism-detail docs are NOT needed by the player, so
the app stays lean. Games are loaded at runtime via read_text()+exec(), so the
.py files ride along as data files (not frozen modules); novaengine/novacore
ARE frozen so the exec'd game code can `import novaengine`.
"""

import sys
from pathlib import Path

ROOT = Path(SPECPATH).resolve().parent  # SPECPATH = repo-root/desktop


def _game_datas(subdir: str) -> list[tuple[str, str]]:
    """Bundle only metadata.json + sibling *.py for every game under `subdir`,
    preserving the relative directory layout so local_dir lookups resolve."""
    out: list[tuple[str, str]] = []
    base = ROOT / subdir
    for meta in base.rglob("metadata.json"):
        rel = meta.parent.relative_to(ROOT)
        out.append((str(meta), str(rel)))
        for py in meta.parent.glob("*.py"):
            out.append((str(py), str(rel)))
    return out


datas = _game_datas("prior-games") + _game_datas("game_sources_3_lvls")

hiddenimports = [
    "play",
    "novaengine", "novaengine.base_game", "novaengine.camera", "novaengine.enums",
    "novaengine.interfaces", "novaengine.level", "novaengine.sprites",
    "novacore", "novacore.base", "novacore.local_wrapper", "novacore.models",
    "novacore.remote_wrapper", "novacore.rendering", "novacore.scorecard",
    "novacore.wrapper",
]

a = Analysis(
    [str(ROOT / "desktop" / "launcher.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=["imageio", "imageio_ffmpeg", "tkinter", "matplotlib", "IPython", "pytest"],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="NovaPlay",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name="NovaPlay",
)

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="NovaPlay.app",
        icon=None,
        bundle_identifier="com.novaplay.player",
        info_plist={
            "CFBundleName": "NovaPlay",
            "CFBundleDisplayName": "NovaPlay",
            "CFBundleShortVersionString": "0.1.0",
            "CFBundleVersion": "0.1.0",
            "NSHighResolutionCapable": True,
            "LSMinimumSystemVersion": "11.0",
        },
    )
