# Smoke test PASS (visit 1/6)

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64,64) == grid_size (64,64) for every level |
| CHECK_SPRITE_CONTENT | 4 | 4 | 5 | distinct non-letter-box palettes per level |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | 4 declared actions (3, 4, 5, 6); all branched in `step()` |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | every action runs without exception |
| CHECK_PALETTE_RANGE | 4..14 | 4..14 | 3..12 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` calls present |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` call present |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size (64, 64); no per-level resize needed |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | each level's witness reaches WIN/next_level |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | rendered frames at workspace/smoke-frames/level_*.png — see notes below |

### CHECK_VISUAL_SANITY notes (per-level)

- **L1**: Two open-top vessels visible side-by-side in the upper playfield (~rows 4–22). Yellow hollow cursor ring above the left vessel. Red target pips inside both vessels' right walls at mid-height (target=4). One green-block valve in the gap between vessel bases. HUD bar rendered at bottom row (palette 4 off-black on palette 5 black background — subtle contrast but technically visible). No content missing; no rendering bug. **PASS.**
- **L2**: Three open-top vessels visible. Yellow cursor above left vessel. Red target pips at three different heights (matching A=3, B=2, C=5). Two green-block valves in the two gaps. Same HUD pattern. **PASS.**
- **L3**: Four vessels. Yellow cursor above leftmost. Red target pips: three high (A=B=D=9) and one low (C=2). Three grey-block valves (closed state, distinct from L2's green ones — confirms the open/closed state-correlated colour rule reads on screen). Orange overflow-cap lip visible just outside C's left wall, above the B-C valve, distinct from the inward red target pips. **PASS.**

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| `check_pour_raises_connected_group` | before=[0,0] after=[1,1] | ACTION5 at L1 raises both connected vessels by 1 |
| `check_click_toggles_valve` | before=True after=False | ACTION6 click on a non-fixed valve flips its is_open flag |
| `check_overflow_cap_clips_surface` | C level after 5 pours with all valves open = 2 | the overflow cap on C clips its surface to 2 even when the connected group rises higher |
| `check_witness_l1_wins` | score 0 → 1 | the L1 witness (4 pours) advances past L1 |

## Verdict

ALL UNIVERSAL AND CUSTOM CHECKS PASS. Transitioning to `finalize`.
