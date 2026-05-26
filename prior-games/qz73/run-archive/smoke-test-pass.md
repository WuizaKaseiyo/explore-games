# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64,64) == grid_size (64,64) every level |
| CHECK_SPRITE_CONTENT | 4 | 4 | 6 | distinct non-letter-box palette values per level (≥ 2) |
| CHECK_ACTION_BRANCHES | ✅ | — | — | both declared actions (`5`, `6`) referenced as `GameAction.ACTIONn` in source |
| CHECK_ACTION_RUNTIME | ✅ | — | — | ACTION5 + ACTION6 (with `data={"x":32,"y":32}`) raised no exception |
| CHECK_PALETTE_RANGE | 2..15 | 2..15 | 2..15 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` reachable in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` reachable in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | not strictly required (all levels use 64×64), but `self.camera.width` / `.height` are still mutated in `on_set_level` |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at `workspace/smoke-frames/level_*.png` |

### Visual-sanity per-level diagnoses

- **L1 PASS** — 1 hub at centre, 1 lone orange tip at top, green tip inside an orange ring at right, purple tip inside a green ring at bottom, lone purple ring at left, orange step-bar at bottom row. Matches `mechanic-spec.md` § 4 L1: tips at slots {0:O, 2:G, 4:P}, sockets at {2:O, 4:G, 6:P}.
- **L2 PASS** — 1 hub at centre, orange tip at top (slot 0), green tip at bottom-right (slot 3), purple tip at left (slot 6) with the slot-6 purple socket halo around it, orange ring at top-right (slot 1), green ring at bottom (slot 4). Step-bar at bottom row. Matches spec § 4 L2.
- **L3 PASS** — 1 hub at centre, 5 tips at slots {0, 1, 2, 5, 7} with colours {orange, green, purple, magenta, yellow}, 5 sockets at slots {0, 2, 3, 5, 6} with colours {yellow, orange, green, magenta, purple}. Tips and sockets overlap visually at slots 0, 2, 5 (matching the spec's "starting state has 0 sockets satisfied, every match must be earned"). Step-bar at bottom row. Matches spec § 4 L3.

No catastrophic rendering bugs (no corner-patch class, no symbol-ish glyphs, no missing HUD).

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_action5_rotates_unlocked_tip | slot before=0 after=1 expected=1 | ACTION5 advances every unlocked tip's slot by +1 mod 8 |
| check_action6_toggles_lock | locked before=False after=True | ACTION6 click on a tip's centre flips its lock flag |
| check_locked_tip_does_not_rotate | locked-slot before=0 after=0 | a locked tip stays put when ACTION5 fires |
| check_l1_minimal_solve | level idx after 2xACTION5 = 1 | spec's intended L1 solution drives the engine into level 2 |

## Visit count

1/3.
