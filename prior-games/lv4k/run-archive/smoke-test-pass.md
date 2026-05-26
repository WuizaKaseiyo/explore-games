# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64,64) == grid_size (64,64) |
| CHECK_SPRITE_CONTENT | 5 | 6 | 6 | distinct non-letter-box palette values |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | declared `[6]`; ACTION6 branched in step() |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions on ACTION6 |
| CHECK_PALETTE_RANGE | 1..14 | 1..14 | 1..14 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | n/a — all levels share grid_size (64, 64) |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### Visual-sanity per-level notes

- **L1** PASS — 4 beam segments (2 left + 2 right of fulcrum), trapezoidal fulcrum-post centred below beam, 2 orange ring-weights in lower-left tray, green HUD bar at top. No glyph or letter shapes visible.
- **L2** PASS — 6 beam segments (3 left + 3 right), fulcrum centred, 1 wide blue weight + 2 orange ring-weights in tray, HUD bar visible.
- **L3** PASS — 6 beam segments, fulcrum centred, 1 orange + 3 wide blue weights in tray (4 weights total), 1 small green passenger sprite resting on beam at arm +2 (right of fulcrum), HUD visible.

The fulcrum was redesigned during this state from a triangular-headed thin-post (which read as an upward arrow) to a trapezoidal block with a darker rectangular core (no directional implication).

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_click_selects_tray_weight | selected before=None, after=Sprite | clicking a tray weight selects it |
| check_place_changes_torque | torque before=0, after=-2 | placing m1 at arm -2 changes torque to -2 |
| check_passenger_displaces_on_high_tilt | passenger before=2, after=1 | placing m2 at arm -3 (tilt=-2) shifts L3 passenger from +2 → +1 |
| check_l1_minimal_solve_advances | level before=0, after=1 | L1 4-action witness solution advances to L2 |

Visit count: 1 / 6.
