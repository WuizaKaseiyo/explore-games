"""Interactive pygame player + game browser for NovaPlay games.

Run from the repo root so the vendored novaengine/ and novacore/ packages
(siblings of this script) are importable:

    .venv/bin/python play.py                 # opens the game browser
    .venv/bin/python play.py --game gv47      # jump straight into a game
    .venv/bin/python play.py --list           # print the catalog and exit
    .venv/bin/python play.py --game gv47 --record   # needs imageio[ffmpeg]

The browser lists every game found under --env-dir (default prior-games,
the generated corpus) and --ref-dir (default game_sources_3_lvls, the 25
reference games). Pick one with the keyboard and play it; press Esc to
return to the browser and choose another — no need to re-run with a
different id.

Browser controls:
    ↑ / ↓          move the selection
    PageUp/PageDn  move a page; Home/End jump to first/last
    type           filter the list (matches id or title); Backspace edits
    Enter          play the highlighted game
    mouse          wheel scrolls, click a row to play it
    Esc            clear the filter if any, otherwise quit

In-game controls:
    Arrow keys   → ACTION1 / ACTION2 / ACTION3 / ACTION4
    Space        → ACTION5 (also dismisses the LEVEL UP / GAME OVER banner)
    Z            → ACTION7
    Mouse click  → ACTION6 with data = {"x": display_px, "y": display_py}
    R            → reset CURRENT level   (Shift+R → full reset to level 0)
    1 / 2 / 3    → jump directly to that level
    Esc          → back to the game browser
    Q            → quit the app

Death handling: when the game enters GAME_OVER / LOSE a banner overlays
the screen until the player presses SPACE or R (restart current level).
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np
import pygame
from novacore import NovaHub, OperationMode
from novaengine import FrameDataRaw
from novaengine.enums import GameState

# 16-colour NovaPlay palette (mirrors render_frames_terminal).
_HEX = {
    0: "#FFFFFF", 1: "#D2D2D2", 2: "#A0A0A0", 3: "#646464",
    4: "#3C3C3C", 5: "#000000", 6: "#E53AA3", 7: "#FF7BCC",
    8: "#F93C31", 9: "#1E93FF", 10: "#87D8F1", 11: "#FFDC00",
    12: "#FF851B", 13: "#921231", 14: "#4FCC30", 15: "#88379B",
}


def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


PALETTE = np.array([_hex_to_rgb(_HEX[i]) for i in range(16)], dtype=np.uint8)


def _initial_state() -> dict:
    """A fresh per-game gameplay-state dict (reset on every game load)."""
    return {
        "frame": None,
        "frame_data": None,
        "last_action": "—",
        # When the game enters GAME_OVER / LOSE, "death_pending" is set
        # True; the banner stays up and gameplay input is locked until
        # the player presses SPACE / R. Explicit dismissal — not a timed
        # auto-restart — so deaths with no visible frame change still
        # register clearly.
        "death_pending": False,
        # When the player advances to a new level, "level_up_pending" is
        # set True; the banner stays up until SPACE dismisses it. SPACE
        # while pending only dismisses — it does not fire ACTION5.
        "level_up_pending": False,
        "prev_levels_completed": None,
        # Snapshot of the frame from BEFORE each env.step(), used as a
        # fallback when post_win_frame capture fails.
        "pre_step_frame": None,
        # Post-win render of the OLD level captured by the monkey-patched
        # next_level; the LEVEL UP banner freezes on this.
        "post_win_frame": None,
        # Animation playback queue. The renderer callback fires once per
        # engine tick; multi-frame animations buffer here and play back
        # over several main-loop iterations so the player sees them.
        "pending_frames": [],
        "current_anim_frame": None,
        "anim_hold_remaining": 0,
        "in_animation_burst": False,
    }


# Mutable shared state set by the renderer callback. Reset per game via
# _reset_play_state(); helpers below read it from the module global.
_state: dict = _initial_state()


def _reset_play_state() -> None:
    _state.clear()
    _state.update(_initial_state())


# State names that should raise the GAME OVER banner.
_LOSE_STATE_NAMES = {"GAME_OVER", "LOSE", "FAILED"}
# State names that mean the player solved every level.
_WIN_STATE_NAMES = {"WIN", "GAME_WON"}
# How many main-loop iterations each animation frame is held on screen
# before the next pending frame is popped. 4 ≈ 15 fps at 60-fps loop.
ANIMATION_HOLD_TICKS = 4

# Maps the action int to the keybinding shown in the HUD.
_KEYBIND_FOR_ACTION = {
    1: "↑", 2: "↓", 3: "←", 4: "→", 5: "Space", 6: "Click", 7: "Z",
}


class _VideoRecorder:
    """Small streaming MP4 recorder for the composed pygame window."""

    def __init__(self, path: Path, fps: int) -> None:
        import imageio.v2 as imageio

        self.path = path
        self.fps = fps
        self.frame_count = 0
        self._next_capture_ms = 0.0
        self._frame_interval_ms = 1000.0 / fps
        self._writer = imageio.get_writer(
            str(path),
            fps=fps,
            codec="libx264",
            pixelformat="yuv420p",
            macro_block_size=1,
        )

    def capture(self, surface: pygame.Surface) -> None:
        now_ms = pygame.time.get_ticks()
        if now_ms < self._next_capture_ms:
            return
        self._next_capture_ms = now_ms + self._frame_interval_ms
        frame = np.ascontiguousarray(
            pygame.surfarray.array3d(surface).swapaxes(0, 1)
        )
        self._writer.append_data(frame)
        self.frame_count += 1

    def close(self) -> None:
        self._writer.close()


def _default_record_path(game: str) -> Path:
    safe_game = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in game)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return Path("recordings") / f"{safe_game}.pygame.{stamp}.mp4"


def _available_actions_line(actions) -> str:
    """Build the 'Available actions: ACTION1 (↑) · ...' HUD line."""
    ids: set[int] = set()
    for a in actions:
        ids.add(int(getattr(a, "value", a)))
    parts: list[str] = []
    for aid in sorted(ids):
        kb = _KEYBIND_FOR_ACTION.get(aid, "?")
        parts.append(f"ACTION{aid} ({kb})")
    if not parts:
        return "Available actions: (none declared)"
    return "Available actions: " + " · ".join(parts)


def _wrap_to_width(text: str, font, max_width: int, sep: str = " · ") -> list[str]:
    """Pack `text` (split on `sep`) into the fewest lines that each
    render in <= max_width pixels under `font`."""
    if not text:
        return [""]
    pieces = text.split(sep)
    lines: list[str] = []
    current = ""
    for piece in pieces:
        candidate = piece if not current else current + sep + piece
        if font.size(candidate)[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = piece
    if current:
        lines.append(current)
    return lines


def _on_frame(steps: int, fd: FrameDataRaw) -> None:
    """Renderer callback fired by the NovaHub wrapper ONCE per env.step()
    with the full per-tick frame list in fd.frame."""
    _state["frame_data"] = fd
    if not fd.frame:
        return
    copied: list = []
    for frame in fd.frame:
        if hasattr(frame, "copy"):
            frame = frame.copy()
        else:
            frame = np.asarray(frame).copy()
        copied.append(frame)
    # Drop the trailing new-level frame on a promotion so animation
    # playback finishes on the OLD level's win frame.
    prev = _state.get("prev_levels_completed")
    is_promotion = prev is not None and fd.levels_completed > prev
    if is_promotion and len(copied) >= 2:
        copied.pop()
    _state["frame"] = copied[-1]
    _state["pending_frames"].extend(copied)


def _frame_to_surface(arr: np.ndarray, target_px: int) -> pygame.Surface:
    """Convert a 64x64 palette-index array to a target_px square Surface."""
    rgb = PALETTE[arr.clip(0, 15)]            # H,W,3
    surf = pygame.surfarray.make_surface(rgb.swapaxes(0, 1))  # pygame is W,H
    return pygame.transform.scale(surf, (target_px, target_px))


def _action_label(fd: Optional[FrameDataRaw]) -> str:
    if fd is None:
        return "—"
    name = fd.action_input.id.name
    if name == "ACTION6":
        d = fd.action_input.data or {}
        return f"ACTION6 (x={d.get('x', '?')}, y={d.get('y', '?')})"
    return name


def _level_reset(env) -> None:
    """Restart the current level without jumping back to level 0."""
    game = getattr(env, "_game", None)
    if game is None:
        return
    game.level_reset()
    try:
        frame = game.camera.render(game.current_level.get_sprites())
    except Exception:
        return
    _state["frame"] = frame
    fd = _state.get("frame_data")
    if fd is not None:
        fd.state = GameState.NOT_FINISHED
    _state["death_pending"] = False
    _state["pending_frames"].clear()
    _state["current_anim_frame"] = None
    _state["anim_hold_remaining"] = 0
    _state["in_animation_burst"] = False


def _level_jump(env, target_index: int) -> None:
    """Jump directly to the level at `target_index` (0-based) with a
    fresh clone of its sprites; no-ops if out of range."""
    game = getattr(env, "_game", None)
    if game is None:
        return
    levels = getattr(game, "_levels", None)
    clean = getattr(game, "_clean_levels", None)
    if not levels or clean is None or not (0 <= target_index < len(levels)):
        return
    levels[target_index] = clean[target_index].clone()
    game.set_level(target_index)
    # set_level touches only _current_level_index/_action_count — reset
    # _state/_score/_next_level too, else the engine still believes the
    # previous WIN/GAME_OVER state and fires a spurious LEVEL UP.
    game._state = GameState.NOT_FINISHED
    game._score = target_index
    game._next_level = False
    try:
        frame = game.camera.render(game.current_level.get_sprites())
    except Exception:
        return
    _state["frame"] = frame
    fd = _state.get("frame_data")
    if fd is not None:
        fd.state = GameState.NOT_FINISHED
        fd.levels_completed = target_index
    _state["prev_levels_completed"] = target_index
    _state["level_up_pending"] = False
    _state["death_pending"] = False
    _state["pre_step_frame"] = None
    _state["post_win_frame"] = None
    _state["pending_frames"].clear()
    _state["current_anim_frame"] = None
    _state["anim_hold_remaining"] = 0
    _state["in_animation_burst"] = False


def _maybe_flag_death() -> None:
    fd = _state.get("frame_data")
    if fd is None or _state["death_pending"]:
        return
    if fd.state.name in _LOSE_STATE_NAMES:
        _state["death_pending"] = True


def _advance_anim_state() -> None:
    """Run one tick of the animation playback state machine."""
    if _state["anim_hold_remaining"] > 0:
        _state["anim_hold_remaining"] -= 1
    elif _state["pending_frames"]:
        queue_len = len(_state["pending_frames"])
        _state["current_anim_frame"] = _state["pending_frames"].pop(0)
        if queue_len >= 2 or _state["in_animation_burst"]:
            _state["in_animation_burst"] = True
            _state["anim_hold_remaining"] = ANIMATION_HOLD_TICKS - 1
        else:
            _state["anim_hold_remaining"] = 0
    elif _state["current_anim_frame"] is not None:
        _state["current_anim_frame"] = None
        _state["in_animation_burst"] = False


def _is_animating() -> bool:
    return (
        bool(_state["pending_frames"])
        or _state["anim_hold_remaining"] > 0
        or _state["current_anim_frame"] is not None
    )


def _maybe_flag_level_up() -> None:
    """Detect level promotion and raise the LEVEL UP banner."""
    fd = _state.get("frame_data")
    if fd is None:
        return
    prev = _state["prev_levels_completed"]
    cur = fd.levels_completed
    if prev is not None and cur > prev and fd.state.name not in _WIN_STATE_NAMES:
        _state["level_up_pending"] = True
    _state["prev_levels_completed"] = cur


# ---------------------------------------------------------------------
# Game catalog (the browser data model)
# ---------------------------------------------------------------------
def _build_catalog(env_dir: str, ref_dir: str) -> list[dict]:
    """Scan env_dir (generated) then ref_dir (reference) for games and
    return a flat, de-duplicated, display-ready list. Each entry keeps a
    reference to the NovaHub that owns it so entry["hub"].make(...) works.
    """
    entries: list[dict] = []
    seen: set[str] = set()
    for group, d in (("generated", env_dir), ("reference", ref_dir)):
        if not d:
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
            entries.append({
                "hub": hub,
                "game_id": gid,
                "short": gid[:4],
                "group": group,
                "title": (getattr(e, "title", None) or "").strip(),
            })
    return entries


def _filter_catalog(catalog: list[dict], query: str) -> list[int]:
    """Return catalog indices whose id/title contain `query` (substring,
    case-insensitive). Empty query → all indices."""
    q = query.strip().lower()
    if not q:
        return list(range(len(catalog)))
    out: list[int] = []
    for i, e in enumerate(catalog):
        hay = f"{e['short']} {e['game_id']} {e['title']}".lower()
        if q in hay:
            out.append(i)
    return out


def _find_in_catalog(catalog: list[dict], requested: str) -> Optional[int]:
    """Resolve a --game value to a catalog index: exact short/full match,
    else a unique '<requested>-*' prefix match. None if not found."""
    for i, e in enumerate(catalog):
        if e["game_id"] == requested or e["short"] == requested:
            return i
    pref = [i for i, e in enumerate(catalog) if e["game_id"].startswith(requested + "-")]
    return pref[0] if len(pref) == 1 else None


_GROUP_COLOUR = {"generated": (140, 220, 160), "reference": (140, 190, 240)}


def _run_menu(catalog: list[dict], fonts) -> tuple[str, Optional[int]]:
    """Render the scrollable, filterable game browser. Returns
    ("play", catalog_index) or ("quit", None)."""
    title_font, row_font, hint_font = fonts
    W, H = 860, 880
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("NovaPlay — game browser")
    clock = pygame.time.Clock()

    query = ""
    sel = 0          # index into the FILTERED list
    scroll = 0
    row_h = 26
    list_top = 104
    list_bottom = H - 16
    visible = max(1, (list_bottom - list_top) // row_h)

    while True:
        filt = _filter_catalog(catalog, query)
        if filt:
            sel = max(0, min(sel, len(filt) - 1))
        else:
            sel = 0
        # keep the selection visible
        if sel < scroll:
            scroll = sel
        elif sel >= scroll + visible:
            scroll = sel - visible + 1
        scroll = max(0, min(scroll, max(0, len(filt) - visible)))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return ("quit", None)
            elif ev.type == pygame.MOUSEWHEEL:
                sel = max(0, min(len(filt) - 1, sel - ev.y)) if filt else 0
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and filt:
                _, my = ev.pos
                if list_top <= my < list_bottom:
                    row = scroll + (my - list_top) // row_h
                    if 0 <= row < len(filt):
                        return ("play", filt[row])
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    if query:
                        query = ""
                        sel = 0
                    else:
                        return ("quit", None)
                elif ev.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if filt:
                        return ("play", filt[sel])
                elif ev.key == pygame.K_UP:
                    sel -= 1
                elif ev.key == pygame.K_DOWN:
                    sel += 1
                elif ev.key == pygame.K_PAGEUP:
                    sel -= visible
                elif ev.key == pygame.K_PAGEDOWN:
                    sel += visible
                elif ev.key == pygame.K_HOME:
                    sel = 0
                elif ev.key == pygame.K_END:
                    sel = len(filt) - 1 if filt else 0
                elif ev.key == pygame.K_BACKSPACE:
                    query = query[:-1]
                    sel = 0
                else:
                    ch = ev.unicode
                    if ch and (ch.isalnum() or ch in "-_ "):
                        query += ch.lower()
                        sel = 0
                if filt:
                    sel = max(0, min(sel, len(filt) - 1))

        # ----- render -----
        screen.fill((18, 18, 22))
        head = title_font.render("NovaPlay — pick a game", True, (235, 235, 235))
        screen.blit(head, (20, 18))
        hint = hint_font.render(
            "↑/↓ select · Enter play · type to filter · "
            "wheel/click · Esc clear/quit",
            True, (170, 170, 175),
        )
        screen.blit(hint, (20, 52))
        filt_txt = hint_font.render(
            f"filter: {query}█   ({len(filt)} shown / {len(catalog)} total)",
            True, (210, 210, 120),
        )
        screen.blit(filt_txt, (20, 76))
        pygame.draw.line(screen, (60, 60, 68), (16, list_top - 6), (W - 16, list_top - 6))

        y = list_top
        for j in range(scroll, min(len(filt), scroll + visible)):
            entry = catalog[filt[j]]
            is_sel = (j == sel)
            if is_sel:
                pygame.draw.rect(screen, (44, 52, 70),
                                 pygame.Rect(12, y - 2, W - 24, row_h))
            id_col = (255, 255, 255) if is_sel else (210, 210, 210)
            grp_col = _GROUP_COLOUR.get(entry["group"], (180, 180, 180))
            id_surf = row_font.render(entry["short"], True, id_col)
            grp_surf = hint_font.render(entry["group"], True, grp_col)
            title = entry["title"] or entry["game_id"]
            if len(title) > 64:
                title = title[:61] + "..."
            title_surf = row_font.render(title, True,
                                         (225, 225, 225) if is_sel else (165, 165, 170))
            screen.blit(id_surf, (24, y))
            screen.blit(grp_surf, (96, y + 2))
            screen.blit(title_surf, (210, y))
            y += row_h

        if not filt:
            none_surf = row_font.render("(no games match the filter)", True, (200, 120, 120))
            screen.blit(none_surf, (24, list_top + 8))

        pygame.display.flip()
        clock.tick(60)


def _run_game(entry: dict, args) -> str:
    """Play one game until the player returns to the menu or quits.
    Returns "menu" (Esc) or "quit" (Q / window close)."""
    _reset_play_state()
    hub = entry["hub"]
    game_id = entry["game_id"]

    env = hub.make(game_id, renderer=_on_frame)
    env.reset()
    # Baseline so the FIRST level transition triggers the LEVEL UP banner.
    _state["prev_levels_completed"] = 0

    raw_actions = getattr(getattr(env, "_game", None), "_available_actions", []) or []
    available_action_ids: set[int] = {int(getattr(a, "value", a)) for a in raw_actions}

    # Monkey-patch next_level to capture a render of the OLD level's
    # winning configuration before the engine advances.
    _original_next_level = env._game.next_level

    def _patched_next_level(*a, **k):
        try:
            game = env._game
            cur = getattr(game, "current_level", None)
            if cur is not None:
                _state["post_win_frame"] = game.camera.render(cur.get_sprites())
        except Exception:
            _state["post_win_frame"] = None
        return _original_next_level(*a, **k)

    env._game.next_level = _patched_next_level

    pygame.display.set_caption(f"NovaPlay — {entry['short']}")
    scale = args.scale
    game_px = 64 * scale

    font = pygame.font.SysFont("Menlo", 16) or pygame.font.SysFont(None, 18)
    small_font = pygame.font.SysFont("Menlo", 14) or pygame.font.SysFont(None, 16)

    HUD_X_PAD = 12
    HUD_TOP_PAD = 12
    HUD_BIG_LINE_H = 22
    HUD_SMALL_LINE_H = 20
    HUD_BOTTOM_PAD = 16
    N_BIG_LINES = 3

    available_actions_text = _available_actions_line(raw_actions)
    runner_line = ("Runner: Esc menu · Q quit · R reset level · "
                   "Shift+R full reset · 1/2/3 jump to level")
    max_text_width = game_px - HUD_X_PAD * 2
    actions_lines = _wrap_to_width(available_actions_text, small_font, max_text_width)
    runner_lines = _wrap_to_width(runner_line, small_font, max_text_width)
    n_small_lines = len(actions_lines) + len(runner_lines)

    hud_px = (HUD_TOP_PAD + N_BIG_LINES * HUD_BIG_LINE_H
              + n_small_lines * HUD_SMALL_LINE_H + HUD_BOTTOM_PAD)
    win_w, win_h = game_px, game_px + hud_px
    screen = pygame.display.set_mode((win_w, win_h))
    clock = pygame.time.Clock()

    recorder: Optional[_VideoRecorder] = None
    if args.record:
        record_path = (Path(args.record_out) if args.record_out
                       else _default_record_path(entry["short"]))
        record_path.parent.mkdir(parents=True, exist_ok=True)
        recorder = _VideoRecorder(record_path, args.record_fps)
        print(f"[play] recording to {record_path}")

    # Static 64x64 cell-boundary grid overlay (subtle, always on).
    grid_overlay = pygame.Surface((game_px, game_px), pygame.SRCALPHA)
    grid_color = (220, 220, 220, 50)
    for i in range(65):
        x = i * scale
        pygame.draw.line(grid_overlay, grid_color, (x, 0), (x, game_px - 1))
        pygame.draw.line(grid_overlay, grid_color, (0, x), (game_px - 1, x))

    KEYMAP = {
        pygame.K_UP: 1, pygame.K_DOWN: 2,
        pygame.K_LEFT: 3, pygame.K_RIGHT: 4,
        pygame.K_SPACE: 5, pygame.K_z: 7,
    }

    result = "quit"
    running = True
    while running:
        fd_now = _state.get("frame_data")
        is_won = fd_now is not None and fd_now.state.name in _WIN_STATE_NAMES

        _advance_anim_state()
        animating = _is_animating()

        input_locked = (
            is_won or _state["death_pending"]
            or _state["level_up_pending"] or animating
        )

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                result = "quit"
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_q:
                    result = "quit"
                    running = False
                elif ev.key == pygame.K_ESCAPE:
                    result = "menu"
                    running = False
                elif ev.key == pygame.K_r:
                    if ev.mod & pygame.KMOD_SHIFT:
                        env.reset()
                        _state["prev_levels_completed"] = 0
                        _state["level_up_pending"] = False
                        _state["death_pending"] = False
                        _state["pre_step_frame"] = None
                        _state["post_win_frame"] = None
                        _state["pending_frames"].clear()
                        _state["current_anim_frame"] = None
                        _state["anim_hold_remaining"] = 0
                        _state["in_animation_burst"] = False
                    else:
                        _level_reset(env)
                elif ev.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    target = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2}[ev.key]
                    _level_jump(env, target)
                elif _state["death_pending"] and ev.key == pygame.K_SPACE:
                    _level_reset(env)
                elif _state["level_up_pending"] and not animating and ev.key == pygame.K_SPACE:
                    _state["level_up_pending"] = False
                    _state["pre_step_frame"] = None
                    _state["post_win_frame"] = None
                    try:
                        game = env._game
                        _state["frame"] = game.camera.render(
                            game.current_level.get_sprites()
                        )
                    except Exception:
                        pass
                elif input_locked:
                    pass
                elif ev.key in KEYMAP:
                    aid = KEYMAP[ev.key]
                    if aid in available_action_ids:
                        _state["pre_step_frame"] = _state.get("frame")
                        env.step(aid)
                        _maybe_flag_death()
                        _maybe_flag_level_up()
                        _advance_anim_state()
                        animating = _is_animating()
            elif (
                ev.type == pygame.MOUSEBUTTONDOWN
                and ev.button == 1
                and not input_locked
                and 6 in available_action_ids
            ):
                mx, my = ev.pos
                if 0 <= mx < game_px and 0 <= my < game_px:
                    fx = max(0, min(63, mx // scale))
                    fy = max(0, min(63, my // scale))
                    _state["pre_step_frame"] = _state.get("frame")
                    env.step(6, data={"x": int(fx), "y": int(fy)})
                    _maybe_flag_death()
                    _maybe_flag_level_up()
                    _advance_anim_state()
                    animating = _is_animating()

        # ----- render -----
        screen.fill((24, 24, 28))
        if _state["current_anim_frame"] is not None:
            display_frame = _state["current_anim_frame"]
        elif _state["level_up_pending"]:
            if _state.get("post_win_frame") is not None:
                display_frame = _state["post_win_frame"]
            elif _state.get("pre_step_frame") is not None:
                display_frame = _state["pre_step_frame"]
            else:
                display_frame = _state["frame"]
        else:
            display_frame = _state["frame"]
        if display_frame is not None:
            screen.blit(_frame_to_surface(display_frame, game_px), (0, 0))

        screen.blit(grid_overlay, (0, 0))

        mx, my = pygame.mouse.get_pos()
        if display_frame is not None and 0 <= mx < game_px and 0 <= my < game_px:
            cx = max(0, min(63, mx // scale))
            cy = max(0, min(63, my // scale))
            palette_idx = int(display_frame[cy, cx])
            r, g, b = PALETTE[max(0, min(15, palette_idx))]
            luminance = 0.299 * int(r) + 0.587 * int(g) + 0.114 * int(b)
            outline_colour = (0, 0, 0) if luminance > 128 else (255, 255, 255)
            pygame.draw.rect(screen, outline_colour,
                             pygame.Rect(cx * scale, cy * scale, scale, scale), width=2)

        fd = _state["frame_data"]
        big_lines: list[str] = []
        if fd is not None:
            big_lines.append(
                f"level {fd.levels_completed + 1}    "
                f"state: {fd.state.name}    "
                f"win_levels: {fd.win_levels}"
            )
            big_lines.append(f"last action: {_action_label(fd)}")
        big_lines.append("")

        y = game_px + HUD_TOP_PAD
        for line in big_lines:
            txt = font.render(line, True, (220, 220, 220))
            screen.blit(txt, (HUD_X_PAD, y))
            y += HUD_BIG_LINE_H
        actions_colour = (180, 230, 200)
        runner_colour = (200, 200, 200)
        for line in actions_lines:
            txt = small_font.render(line, True, actions_colour)
            screen.blit(txt, (HUD_X_PAD, y))
            y += HUD_SMALL_LINE_H
        for line in runner_lines:
            txt = small_font.render(line, True, runner_colour)
            screen.blit(txt, (HUD_X_PAD, y))
            y += HUD_SMALL_LINE_H

        if is_won:
            big = pygame.font.SysFont("Menlo", 32, bold=True) or pygame.font.SysFont(None, 36)
            small = pygame.font.SysFont("Menlo", 18) or pygame.font.SysFont(None, 22)
            head = big.render("CONGRATULATIONS — ALL LEVELS SOLVED", True, (120, 240, 140))
            sub = small.render("Shift+R play again · Esc browser · Q quit", True, (220, 220, 220))
            mw = max(head.get_width(), sub.get_width())
            mh = head.get_height() + 8 + sub.get_height()
            box = pygame.Surface((mw + 36, mh + 28), pygame.SRCALPHA)
            box.fill((0, 0, 0, 210))
            bx = (game_px - box.get_width()) // 2
            by = (game_px - box.get_height()) // 2
            screen.blit(box, (bx, by))
            screen.blit(head, (bx + 18, by + 14))
            screen.blit(sub, (bx + (box.get_width() - sub.get_width()) // 2,
                              by + 14 + head.get_height() + 8))
        elif _state["level_up_pending"] and not animating:
            big = pygame.font.SysFont("Menlo", 32, bold=True) or pygame.font.SysFont(None, 36)
            small = pygame.font.SysFont("Menlo", 18) or pygame.font.SysFont(None, 22)
            new_level = (fd.levels_completed + 1) if fd is not None else "?"
            head = big.render(f"LEVEL UP  ->  LEVEL {new_level}", True, (120, 220, 255))
            sub = small.render("Press SPACE to proceed.", True, (220, 220, 220))
            mw = max(head.get_width(), sub.get_width())
            mh = head.get_height() + 6 + sub.get_height()
            box = pygame.Surface((mw + 36, mh + 24), pygame.SRCALPHA)
            box.fill((0, 0, 0, 200))
            bx = (game_px - box.get_width()) // 2
            by = (game_px - box.get_height()) // 2
            screen.blit(box, (bx, by))
            screen.blit(head, (bx + (box.get_width() - head.get_width()) // 2, by + 12))
            screen.blit(sub, (bx + (box.get_width() - sub.get_width()) // 2,
                              by + 12 + head.get_height() + 6))
        elif _state["death_pending"]:
            big = pygame.font.SysFont("Menlo", 36, bold=True) or pygame.font.SysFont(None, 40)
            small = pygame.font.SysFont("Menlo", 18) or pygame.font.SysFont(None, 22)
            head = big.render("GAME OVER", True, (255, 100, 100))
            sub = small.render("Press SPACE or R to restart the level.", True, (220, 220, 220))
            mw = max(head.get_width(), sub.get_width())
            mh = head.get_height() + 8 + sub.get_height()
            box = pygame.Surface((mw + 36, mh + 28), pygame.SRCALPHA)
            box.fill((0, 0, 0, 210))
            bx = (game_px - box.get_width()) // 2
            by = (game_px - box.get_height()) // 2
            screen.blit(box, (bx, by))
            screen.blit(head, (bx + (box.get_width() - head.get_width()) // 2, by + 14))
            screen.blit(sub, (bx + (box.get_width() - sub.get_width()) // 2,
                              by + 14 + head.get_height() + 8))

        pygame.display.flip()
        if recorder is not None:
            recorder.capture(screen)
        clock.tick(60)

    if recorder is not None:
        recorder.close()
        print(f"[play] saved {recorder.path} "
              f"({recorder.frame_count} frames at {recorder.fps} fps)")
    return result


def main() -> None:
    ap = argparse.ArgumentParser(
        description="pygame browser + player for NovaPlay generated and reference games")
    ap.add_argument("--game", default=None,
                    help="optionally jump straight into this game id "
                         "(4-char like 'gv47'/'cn04' or full 'cn04-65d47d14'); "
                         "omit to open the browser")
    ap.add_argument("--env-dir", default="prior-games",
                    help="primary environments root (generated games)")
    ap.add_argument("--ref-dir", default="game_sources_3_lvls",
                    help="secondary environments root (the 25 reference games)")
    ap.add_argument("--scale", type=int, default=12,
                    help="render scale; window game area = 64*scale (default 12 -> 768)")
    ap.add_argument("--list", action="store_true",
                    help="print the game catalog and exit (no window)")
    ap.add_argument("--record", action="store_true",
                    help="record each played game to an MP4 (needs imageio[ffmpeg])")
    ap.add_argument("--record-out", default=None,
                    help="output MP4 path for --record (default: recordings/<game>.<timestamp>.mp4)")
    ap.add_argument("--record-fps", type=int, default=30,
                    help="recording frame rate for --record (default: 30)")
    args = ap.parse_args()
    if args.record and args.record_fps <= 0:
        ap.error("--record-fps must be greater than 0")

    catalog = _build_catalog(args.env_dir, args.ref_dir)

    if args.list:
        for e in catalog:
            print(f"{e['short']:6} {e['group']:10} {e['title']}")
        print(f"\n{len(catalog)} games "
              f"(env-dir={args.env_dir}, ref-dir={args.ref_dir})")
        return

    if not catalog:
        print(f"ERROR: no games found under {args.env_dir} or {args.ref_dir}.")
        sys.exit(1)

    pygame.display.init()
    pygame.font.init()

    menu_fonts = (
        pygame.font.SysFont("Menlo", 22, bold=True) or pygame.font.SysFont(None, 26),
        pygame.font.SysFont("Menlo", 16) or pygame.font.SysFont(None, 18),
        pygame.font.SysFont("Menlo", 13) or pygame.font.SysFont(None, 15),
    )

    pending: Optional[int] = None
    if args.game:
        pending = _find_in_catalog(catalog, args.game)
        if pending is None:
            print(f"WARNING: '{args.game}' not found; opening the browser instead.")

    while True:
        if pending is None:
            action, idx = _run_menu(catalog, menu_fonts)
            if action == "quit":
                break
            pending = idx
        result = _run_game(catalog[pending], args)
        if result == "quit":
            break
        pending = None      # back to the browser

    pygame.quit()


if __name__ == "__main__":
    main()
