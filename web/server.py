"""Tiny stdlib HTTP backend for the web player.

The NovaPlay games are Python/novaengine, so the game logic runs here
(server-side, one in-memory session per browser tab) and the browser
only renders frames + sends actions. No third-party web framework — just
http.server + json. Run from anywhere:

    .venv/bin/python web/server.py [--port 8000]

then open http://localhost:8000/ . Needs the same env as play.py
(novaengine + novacore are vendored at the repo root; numpy/pydantic/
requests/python-dotenv come from the .venv).

API:
    GET  /api/games                      -> {"games": [{id, short, group, title}]}
    POST /api/new    {id}                -> {session, frames, state, actions, w, h}
    POST /api/step   {session, action, x?, y?} -> {frames, state}
    POST /api/reset  {session, full?}    -> {frames, state}
    POST /api/level  {session, level}    -> {frames, state}   (0-based jump)

A frame is {"w", "h", "px"} where px is a row-major string of w*h hex
chars (one per cell, palette index 0-15).
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Make the vendored novaengine/ and novacore/ (repo root) importable
# regardless of where this script is launched from.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import numpy as np  # noqa: E402
from novacore import NovaHub, OperationMode  # noqa: E402
from novaengine import GameState  # noqa: E402

logging.getLogger().setLevel(logging.WARNING)  # quiet novacore INFO chatter

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
_HEXCHARS = "0123456789abcdef"
_WIN_STATES = {"WIN", "GAME_WON"}
_LOSE_STATES = {"GAME_OVER", "LOSE", "FAILED"}

# ---------------------------------------------------------------------
# Catalog + game sessions
# ---------------------------------------------------------------------
_catalog: list[dict] = []          # [{hub, game_id, short, group, title}]
_by_id: dict[str, dict] = {}
_sessions: dict[str, dict] = {}    # sid -> {env, buf, lock}
_sessions_lock = threading.Lock()
_SESSION_CAP = 64                  # evict oldest beyond this


def build_catalog() -> None:
    seen: set[str] = set()
    for group, sub in (("generated", "prior-games"),
                        ("reference", "game_sources_3_lvls")):
        d = os.path.join(ROOT, sub)
        if not os.path.isdir(d):
            continue
        try:
            hub = NovaHub(operation_mode=OperationMode.OFFLINE, environments_dir=d)
        except Exception:
            continue
        for e in sorted(hub.available_environments, key=lambda x: x.game_id):
            gid = e.game_id
            if gid in seen:
                continue
            seen.add(gid)
            entry = {
                "hub": hub,
                "game_id": gid,
                "short": gid[:4],
                "group": group,
                "title": (getattr(e, "title", None) or "").strip(),
            }
            _catalog.append(entry)
            _by_id[gid] = entry


def _encode_frame(arr) -> dict:
    a = np.asarray(arr)
    if a.ndim != 2:
        a = a.reshape(a.shape[-2], a.shape[-1])
    h, w = int(a.shape[0]), int(a.shape[1])
    flat = np.clip(a, 0, 15).astype(int).ravel()
    px = "".join(_HEXCHARS[v] for v in flat)
    return {"w": w, "h": h, "px": px}


def _state_dict(sess) -> dict:
    fd = sess.get("last_fd")
    game = sess["env"]._game
    if fd is not None:
        state_name = fd.state.name
        level = int(fd.levels_completed) + 1
        win_levels = int(fd.win_levels)
        last = fd.action_input.id.name if fd.action_input is not None else "—"
    else:
        state_name = "NOT_FINISHED"
        level = int(getattr(game, "_score", 0)) + 1
        win_levels = int(getattr(game, "_win_score", 0))
        last = "—"
    return {
        "level": level,
        "state": state_name,
        "win_levels": win_levels,
        "last_action": last,
        "won": state_name in _WIN_STATES,
        "lost": state_name in _LOSE_STATES,
    }


def _drain_frames(sess) -> list[dict]:
    frames = [_encode_frame(f) for f in sess["buf"]]
    sess["buf"].clear()
    if not frames and sess.get("last_frame") is not None:
        frames = [_encode_frame(sess["last_frame"])]
    if frames:
        sess["last_frame"] = sess["buf"][-1] if sess["buf"] else None
    return frames


def new_session(game_id: str) -> dict:
    entry = _by_id.get(game_id)
    if entry is None:
        raise KeyError(game_id)
    buf: list = []

    def renderer(steps, fd):
        for f in fd.frame:
            buf.append(f.copy() if hasattr(f, "copy") else np.asarray(f).copy())
        sess["last_fd"] = fd

    env = entry["hub"].make(game_id, renderer=renderer)
    sess = {"env": env, "buf": buf, "last_fd": None, "last_frame": None,
            "lock": threading.Lock()}
    buf.clear()
    env.reset()
    sid = uuid.uuid4().hex[:16]
    with _sessions_lock:
        if len(_sessions) >= _SESSION_CAP:
            _sessions.pop(next(iter(_sessions)))
        _sessions[sid] = sess
    actions = sorted({int(getattr(a, "value", a))
                      for a in getattr(env._game, "_available_actions", []) or []})
    frames = [_encode_frame(f) for f in buf]
    buf.clear()
    return {"session": sid, "frames": frames, "state": _state_dict(sess),
            "actions": actions, "short": entry["short"], "title": entry["title"]}


def _level_jump(env, target: int) -> None:
    game = env._game
    levels = getattr(game, "_levels", None)
    clean = getattr(game, "_clean_levels", None)
    if not levels or clean is None or not (0 <= target < len(levels)):
        return
    levels[target] = clean[target].clone()
    game.set_level(target)
    game._state = GameState.NOT_FINISHED
    game._score = target
    game._next_level = False


def do_action(sess, action: int, x=None, y=None) -> dict:
    env = sess["env"]
    with sess["lock"]:
        sess["buf"].clear()
        if action == 6:
            env.step(6, data={"x": int(x or 0), "y": int(y or 0)})
        else:
            env.step(action)
        frames = [_encode_frame(f) for f in sess["buf"]]
        sess["buf"].clear()
    return {"frames": frames, "state": _state_dict(sess)}


def do_reset(sess, full: bool) -> dict:
    env = sess["env"]
    with sess["lock"]:
        sess["buf"].clear()
        if full:
            env.reset()
            frames = [_encode_frame(f) for f in sess["buf"]]
        else:
            env._game.level_reset()
            frame = env._game.camera.render(env._game.current_level.get_sprites())
            frames = [_encode_frame(frame)]
        sess["buf"].clear()
    return {"frames": frames, "state": _state_dict(sess)}


def do_level(sess, level: int) -> dict:
    env = sess["env"]
    with sess["lock"]:
        sess["buf"].clear()
        _level_jump(env, int(level))
        frame = env._game.camera.render(env._game.current_level.get_sprites())
        sess["buf"].clear()
    return {"frames": [_encode_frame(frame)], "state": _state_dict(sess)}


# ---------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------
_CTYPES = {".html": "text/html", ".js": "text/javascript",
           ".css": "text/css", ".png": "image/png", ".ico": "image/x-icon"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        n = int(self.headers.get("Content-Length", 0) or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception:
            return {}

    def _serve_static(self, path: str):
        if path in ("/", ""):
            path = "/index.html"
        rel = path.lstrip("/")
        full = os.path.normpath(os.path.join(STATIC_DIR, rel))
        if not full.startswith(STATIC_DIR) or not os.path.isfile(full):
            self.send_error(404)
            return
        ext = os.path.splitext(full)[1]
        with open(full, "rb") as fh:
            data = fh.read()
        self.send_response(200)
        self.send_header("Content-Type", _CTYPES.get(ext, "application/octet-stream"))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/api/games":
            self._json({"games": [
                {"id": e["game_id"], "short": e["short"],
                 "group": e["group"], "title": e["title"]}
                for e in _catalog
            ]})
            return
        self._serve_static(self.path.split("?")[0])

    def _session(self, body):
        sid = body.get("session")
        sess = _sessions.get(sid)
        if sess is None:
            self._json({"error": "unknown or expired session"}, 404)
        return sess

    def do_POST(self):
        body = self._read_json()
        try:
            if self.path == "/api/new":
                self._json(new_session(body.get("id", "")))
            elif self.path == "/api/step":
                sess = self._session(body)
                if sess is not None:
                    self._json(do_action(sess, int(body.get("action", 0)),
                                         body.get("x"), body.get("y")))
            elif self.path == "/api/reset":
                sess = self._session(body)
                if sess is not None:
                    self._json(do_reset(sess, bool(body.get("full", False))))
            elif self.path == "/api/level":
                sess = self._session(body)
                if sess is not None:
                    self._json(do_level(sess, int(body.get("level", 0))))
            else:
                self.send_error(404)
        except KeyError:
            self._json({"error": "unknown game id"}, 404)
        except Exception as e:  # surface engine errors to the client
            self._json({"error": f"{type(e).__name__}: {e}"}, 500)


def main() -> None:
    ap = argparse.ArgumentParser(description="web backend for the NovaPlay player")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()
    build_catalog()
    print(f"catalog: {len(_catalog)} games")
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"serving on http://{args.host}:{args.port}/  (Ctrl-C to stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")
        srv.shutdown()


if __name__ == "__main__":
    main()
