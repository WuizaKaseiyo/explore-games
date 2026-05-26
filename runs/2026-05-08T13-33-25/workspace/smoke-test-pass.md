# smoke-test-pass — `ej4t`

12 PASS, 0 FAIL, 1 SKIPPED.

## Universal checks (10)

| # | Check | L1 | L2 | L3 | Result |
|---|---|---|---|---|---|
| 1 | CHECK_CAMERA_VIEWPORT | ✅ (12,12) | ✅ (14,14) | ✅ (16,16) | PASS |
| 2 | CHECK_SPRITE_CONTENT | ✅ 18 sprites | ✅ 22 sprites | ✅ 28 sprites | PASS |
| 3 | CHECK_ACTION_BRANCHES | — | — | — | PASS (4/4 declared actions have step branches) |
| 4 | CHECK_ACTION_RUNTIME | — | — | — | PASS (each ACTION1-4 runs without exception) |
| 5 | CHECK_PALETTE_RANGE | — | — | — | PASS (all rendered pixels in [0, 15]) |
| 6 | CHECK_WIN_PATH_EXISTS | — | — | — | PASS (`self.next_level()` present) |
| 7 | **CHECK_WITNESS_WINS** | ✅ 5 actions advance | ✅ 5 actions advance | ✅ 7 actions reach WIN | **PASS** |
| 8 | CHECK_LOSE_PATH_EXISTS | — | — | — | PASS (`self.lose()` present) |
| 9 | CHECK_CAMERA_DEFAULT | — | — | — | PASS (per-level camera resize in `on_set_level`) |
| 10 | CHECK_VISUAL_SANITY | — | — | — | SKIPPED (vision pass — manual verification) |

## Custom checks (3)

| # | Check | Result |
|---|---|---|
| 1 | wall blocks lateral movement (no out-of-grid escape) | PASS |
| 2 | extender pickup grows R by 1 | PASS (verified L2: R 1 → 2 after pickup at (5,7)) |
| 3 | shrinker trap reduces R by 1 | PASS (verified L3: R 3 → 2 after stepping on shrinker at (7,7)) |

## Witness validation detail (CHECK_WITNESS_WINS)

The new upstream witness-replay check worked end-to-end:
- **L1 witness**: `[ACTION4 × 5]` → game advanced from level 1 to level 2 (`_score: 0 → 1`).
- **L2 witness**: `[ACTION4 × 5]` → game advanced from level 2 to level 3 (`_score: 1 → 2`). Pickup at (5, 7) consumed; R grew from 1 to 2; chain push of 2 crates at (8,7)+(9,7) → (9,7)+(10,7=target).
- **L3 witness**: `[ACTION4 × 7]` → game reached WIN state (`_state: WIN`). Both extenders consumed (R: 2→3 at extender_a, →2 at shrinker, →3 at extender_b); chain push of 3 crates at (10-12, 7) → (11-13, 7=target).

All three levels solved deterministically by the spec's named witnesses — confirms spec-implementation alignment with no off-by-one or distance-convention errors.
