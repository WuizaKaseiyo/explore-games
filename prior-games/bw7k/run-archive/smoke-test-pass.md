# Smoke test PASS

Visit count: 1/6.

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 64) == level.grid_size (64, 64) for all three |
| CHECK_SPRITE_CONTENT | 5 | 7 | 9 | distinct non-letter-box palette values per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 4 declared actions (ACTION1..4) referenced in `step()` |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions; `_action_count` advances 0→1 per action |
| CHECK_PALETTE_RANGE | 2..12 | 2..12 | 2..14 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` and `self.win()` both reachable in source |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size (64, 64); per-level camera resize NOT required (default 64×64 camera matches) |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 witness (13×UP) advanced score 0→1; L2 witness (25 actions) advanced 1→2; L3 witness (28 actions) reached state WIN |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | rendered initial frames at workspace/smoke-frames/level_*.png match the spec — see per-level notes below |

### CHECK_VISUAL_SANITY per-level notes

- **L1**: 4 sprites visible in the spec-described column x=12: actor (filled blue square, bottom), anchor_red (orange-cornered pad, middle-low), target_red (red hollow ring, middle-upper), actor_goal (blue hollow ring, top). Bottom-row step-counter bar visible. Matches spec § Levels — Level 1 layout. PASS.
- **L2**: 5 sprites: actor (filled blue square, bottom-left), anchor_red (orange-cornered pad, middle-left), target_red (red hollow ring, top-right), wall (small grey square adjacent to target, blocking the LEFT-from-(40,8) per spec), actor_goal (blue hollow ring, top-left). Bottom-row HUD visible. Matches spec § Levels — Level 2 layout. PASS.
- **L3**: 8 sprites: actor (bottom-left), anchor_red (middle-left), target_red (top-left), anchor_yellow (yellow-and-green pad middle-right), target_yellow (yellow hollow ring top-right), wall × 2 (grey squares — one mid-board acting as the between-anchors detour wall, one adjacent to target_yellow blocking the RIGHT-from-(40,16) replay path), actor_goal (top-middle). Bottom-row HUD visible. Matches spec § Levels — Level 3 layout. PASS.

## Custom checks

| Check | Observed | Passed |
|---|---|---|
| `check_up_moves_actor` | y0=56 y1=52 (Δy = −STRIDE) | ✅ |
| `check_anchor_spawns_shade` | shade_red count=1 after walking onto anchor_red | ✅ |
| `check_shade_lands_at_target_l1` | shade=(12,16) target=(12,16) — coincident | ✅ |
| `check_l1_witness_wins` | score 0→1; engine advanced past L1 | ✅ |

## Verdict

All 10 universal checks + all 4 custom checks pass. Transition to
`finalize`.
