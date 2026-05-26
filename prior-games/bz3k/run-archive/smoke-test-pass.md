# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera 64×64 == grid_size 64×64 for all levels |
| CHECK_SPRITE_CONTENT | 7 | 7 | 10 | distinct non-letter-box palette values per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | all 4 declared actions (1, 2, 3, 4) referenced in source |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | each action runs without exception, action_count increments |
| CHECK_PALETTE_RANGE | 0..14 | 0..14 | 0..15 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1→L2 (10 actions), L2→L3 (13 actions), L3→WIN (10 actions) |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels have grid_size=(64, 64); per-level resize present (defensive) |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at `workspace/smoke-frames/level_{1,2,3}.png` |

### Visual sanity per-level diagnoses
- L1 PASS — open arena with brick-textured boundary walls; orange avatar at left chamber; yellow hollow target ring near center; bottom-row green step counter HUD; top-right velocity-dot HUD anchor pixel visible (vx=vy=0). Matches spec § L1 layout.
- L2 PASS — boundary plus an internal vertical wall column with a single 5-cell-tall passage at y=30..34; yellow cap-band fills the passage; avatar in west chamber; yellow hollow target near east wall. Matches spec § L2.
- L3 PASS — 5-row horizontal corridor between thick brick wall strips above and below; corridor contains, left to right: target ring, cap-band, avatar (orange), flipper bowtie (purple/magenta), and a maroon textured hazard band. Matches spec § L3.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_arrow_applies_impulse | vx_after_one_press=1 | ACTION4 from rest produces vx=1 — impulse mechanic confirmed |
| check_consecutive_arrows_accumulate | vx_after_two_presses=2 | Two →'s accumulate to vx=2 (persistent velocity) |
| check_cap_clamps_velocity | vx_after_cap_traversal=1 | Pre-cap ramp to vx=6 then crossing cap → vx clamped to 1 |
| check_flipper_negates_velocity | vx_after_flipper=-7 | L3 starting vx=6 + → impulse + flipper hit → vx=-7 (negated) |

Visit count: 1/6.
