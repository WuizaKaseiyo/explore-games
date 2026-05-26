# Smoke test PASS — kn58

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 64) == grid_size (64, 64) for every level |
| CHECK_SPRITE_CONTENT | 5 | 5 | 7 | distinct non-letter-box palette values |
| CHECK_ACTION_BRANCHES | ✅ | — | — | declared `[6]`, source references `GameAction.ACTION6` |
| CHECK_ACTION_RUNTIME | ✅ | — | — | ACTION6 with click data ran without exception |
| CHECK_PALETTE_RANGE | 0..12 | 2..15 | 0..15 | within [0, 15] for all levels |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | All 3 levels share grid_size (64, 64); no per-level resize required |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at workspace/smoke-frames/level_*.png |

### Visual sanity verdicts

- **L1 PASS** — Light-grey playfield bounded by black frame. Orange pawn (with internal cross-pattern) on left at logical (4, 7); orange hollow target ring on right at (11, 7). Light-blue HUD bar visible at bottom. Matches spec § L1 (single pawn + single target on bare arena).
- **L2 PASS** — T-shaped corridor visible: horizontal corridor at row 7 with a 2-cell southward pocket below cell (7, 8)-(7, 9). Orange pawn at left end (1, 7); purple pawn at right end (14, 7). HUD bar visible. Matches spec § L2 (corridor + south pocket; pawns at corridor ends to swap).
- **L3 PASS** — Open arena. Orange pawn on left at (3, 8); purple pawn at (8, 8) (overlapping target_purple — purple matched at level start per pre-stuck rule); anti-anchor (red corner-dot frame with dark inner block) visible at (10, 8); orange hollow target ring at (12, 8). HUD bar visible. Matches spec § L3 (anti-anchor + pre-stuck purple blocker + east-bound orange target).

## Custom checks

| Check | Result | Observed |
|---|---|---|
| check_anchor_pull_orange | PASS | x0=16, x1=20 (1 cell east, CELL=4) — anchor placed at (11,7) pulls orange (4,7)→(5,7) |
| check_match_sticks_pawn | PASS | level after 7 pulls = 1 — orange reaches (11, 7) and matches; level advances |
| check_pawn_pawn_collision_blocks | PASS | orange at logical (7, 8) after 5 east-pulls — blocked by stuck purple at (8, 8); no secondary axis |
| check_lose_at_budget | PASS | final state = GAME_OVER after 31 no-pull clicks — step counter exhaustion fires `lose()` |

Visit count: 1/6.
