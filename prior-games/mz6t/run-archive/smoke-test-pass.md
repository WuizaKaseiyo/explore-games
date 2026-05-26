# Smoke test PASS — `mz6t`

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ 64x64 | ✅ 64x64 | ✅ 64x64 | camera viewport == level.grid_size |
| CHECK_SPRITE_CONTENT | 2 | 3 | 5 | distinct non-letter-box palette values per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | — | both ACTION5 and ACTION6 referenced in `step()` |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | — | ACTION5 and ACTION6 each run without exception |
| CHECK_PALETTE_RANGE | 4..12 | 4..13 | 4..13 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` found in source |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 (2 actions) → score 1; L2 (5 actions) → score 2; L3 (7 actions) → state WIN |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` found in source |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels use grid_size (64, 64); per-level resize not required |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec; PNGs at `workspace/smoke-frames/level_*.png` |

### CHECK_VISUAL_SANITY notes

For each level I rendered the initial frame to PNG and inspected against the spec's `## 4. Level progression` per-level layout.

- **L1 (`level_1.png`).** Sprite count: ~24 cell shapes — close to the spec's "5×5 grid minus the (1,1) and (2,2) diff cells in initial state-0 form, others in state-1 form". Sprite placement: 5×5 mosaic in the top-left half + a 5×5 quarter-scale target panel at the right ✓. HUD presence: orange step-counter bar visible along the bottom edge ✓. No catastrophic rendering — the playfield fills the left-half of the frame; the target panel is a clearly smaller mosaic to its right; nothing reads as a digit, letter, or arrow. **PASS.**
- **L2 (`level_2.png`).** Sprite count: ~21 voting cells + 4 maroon walls visible at inner-corner positions ✓. The orange `+` cross around the centre cell reads clearly. Target panel shows the full vertical column of orange + the horizontal row, as the spec describes. **PASS.**
- **L3 (`level_3.png`).** Sprite count: ~21 voting cells + 4 maroon walls + the central anchor cell visible with corner pips (palette 5, black corners). The anchor's pip motif is distinct from the surrounding voting cells. Target panel shows the central pink anchor with orange surroundings; the pink target-tile motif is differentiated. **PASS.**

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_click_cycles_state | s0=0 s1=1 | ACTION6 click on cell (0,0) advances state from 0 → 1. |
| check_tick_propagates_majority | s_before=0 s_after=1 | ACTION5 tick flips L1's `(2,2)` from state-0 to state-1 because its 4 neighbours all hold state-1 (4 ≥ 3 strict majority). |
| check_anchor_locks_on_target | locked=True, state_after_lock=2, after_extra_click=2 | L3 anchor (target state-2) locks after 2 cycle-clicks; subsequent clicks are no-ops (state stays at 2). |
| check_win_fires_only_on_tick | score_before=0 score_after_clicks=0 | L1 click sequence that would otherwise compose a winning state does NOT advance the score until ACTION5 fires — the engine-side enforcement that makes M2 strictly necessary. |

Visit count: 1/6.
