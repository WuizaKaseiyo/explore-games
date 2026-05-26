# Smoke test PASS — gx7m

Visit count: 1/6.

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64, 64) == level.grid_size (64, 64) per level. |
| CHECK_SPRITE_CONTENT | 8 | 9 | 12 | distinct non-letter-box palette values per level (≥ 2 threshold). |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | `GameAction.ACTION6` referenced in source. |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | ACTION6 ran without exception. |
| CHECK_PALETTE_RANGE | 0..12 | 0..11 | 0..15 | within [0, 15] per level. |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` and `self.win()` both reachable. |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` reachable on `_action_count >= step_budget`. |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | levels share `grid_size=(64, 64)` so per-level resize is a no-op; the `on_set_level` body still mutates `self.camera.width`/`height` defensively. |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | Rendered initial frames at `workspace/smoke-frames/level_*.png` match the spec's per-level layout: L1 = 3 plain discs in a row with south indents and a step-counter bar; L2 = pink + magenta-ratchet (yellow tang east) + lblue, indents at south/east/west; L3 = 5 discs in a row with magenta-ratchet (yellow tang) and clutch-green (purple lever), indents in the spec's specified compass positions. No catastrophic rendering bugs; no sprite resembles a letter or digit. |

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| `check_disc_click_rotates_90_cw` | r0=0 r1=90 | A disc-hub click rotates the disc by 90° CW. |
| `check_cascade_flips_sign_at_neighbor` | pink_delta=90 lblue_delta=270 | The clicked disc's neighbour rotates in the opposite direction (sign flip across the mesh-edge). |
| `check_ratchet_hub_click_is_noop_when_blocked` | before=[0, 0, 0] after=[0, 0, 0] | A click on the ratchet's hub while its state is BLOCKED leaves every disc unchanged. |
| `check_clutch_disengage_isolates_subgraph` | orange_before=0 orange_after=0 | After the clutch is disengaged, an lblue-hub click does NOT propagate through the clutch to orange (mesh edge removed). |

All universal and custom checks pass on first visit. Transition to `finalize`.
