"""Frozen-app entry point for the NovaPlay desktop player.

Thin wrapper around play.py. The packaged app (PyInstaller .app / .exe /
AppImage) may be launched from any working directory, but play.py finds the
game corpus through RELATIVE paths (``prior-games/``, ``game_sources_3_lvls/``)
resolved against the cwd — and novacore stores each game's ``local_dir`` as the
relative path where its ``metadata.json`` was found. In a frozen build those
folders are bundled as data files under ``sys._MEIPASS``; we chdir there before
handing off so every relative lookup resolves against the bundle.

In dev (unfrozen) this just chdirs to the repo root, so
``python desktop/launcher.py`` behaves exactly like ``python play.py``.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _resource_root() -> Path:
    """Directory that contains prior-games/ and game_sources_3_lvls/."""
    if getattr(sys, "frozen", False):
        # PyInstaller unpacks bundled datas under _MEIPASS.
        return Path(getattr(sys, "_MEIPASS", os.path.dirname(sys.executable)))
    # Dev mode: repo root is the parent of this desktop/ dir.
    return Path(__file__).resolve().parent.parent


def _strip_macos_psn_args() -> None:
    """Drop the ``-psn_*`` argument macOS sometimes hands a bundled app, so
    play.py's argparse parser does not choke on it."""
    sys.argv = [sys.argv[0]] + [a for a in sys.argv[1:] if not a.startswith("-psn")]


def _selftest() -> int:
    """Headless build smoke test: scan the bundled corpus, then fully load,
    reset and step one game so the read_text()+exec() path and the frozen
    novaengine import are both exercised. Prints PASS/FAIL, returns an exit
    code. Used by CI to verify a packaged build before publishing."""
    from novacore import NovaHub, OperationMode

    def say(msg: str) -> None:
        # Windowed (console=False) builds can have sys.stdout == None; the
        # exit code is the source of truth, so never let a print crash us.
        try:
            print(msg, flush=True)
        except Exception:
            pass

    total = 0
    sample = None
    for sub in ("prior-games", "game_sources_3_lvls"):
        if not os.path.isdir(sub):
            continue
        hub = NovaHub(operation_mode=OperationMode.OFFLINE, environments_dir=sub)
        for e in hub.available_environments:
            total += 1
            if sample is None:
                sample = (hub, e.game_id)
    if total == 0 or sample is None:
        say("SELFTEST FAIL: no games found in bundle")
        return 1

    hub, gid = sample
    env = hub.make(gid)
    if env is None or getattr(env, "_game", None) is None:
        say(f"SELFTEST FAIL: could not load game {gid}")
        return 1
    fd = env.reset()
    if fd is None or not fd.frame:
        say(f"SELFTEST FAIL: {gid} reset produced no frame")
        return 1
    h, w = fd.frame[-1].shape
    say(f"SELFTEST PASS: {total} games; loaded {gid}; frame {w}x{h}")
    return 0


def main() -> None:
    root = _resource_root()
    sys.path.insert(0, str(root))  # make play / novaengine / novacore importable in dev
    os.chdir(root)
    _strip_macos_psn_args()

    if "--selftest" in sys.argv:
        sys.exit(_selftest())

    import play  # imported after chdir; resolves bundled or repo-root modules

    play.main()


if __name__ == "__main__":
    main()
