# Smoke test PASS

## Universal checks

| Check | L1 | L2 | L3 | Notes |
|---|---|---|---|---|
| CHECK_CAMERA_VIEWPORT | ✅ | ✅ | ✅ | camera (64,64) == grid (64,64) |
| CHECK_SPRITE_CONTENT | 8 | 8 | 9 | distinct non-letter-box palette values |
| CHECK_ACTION_BRANCHES | ✅ | ✅ | ✅ | declared=[5, 6]; both branched in step() |
| CHECK_ACTION_RUNTIME | ✅ | ✅ | ✅ | no exceptions |
| CHECK_PALETTE_RANGE | 2..13 | 2..13 | 2..13 | within [0, 15] |
| CHECK_WIN_PATH_EXISTS | ✅ | — | — | `self.next_level()` present |
| CHECK_LOSE_PATH_EXISTS | ✅ | — | — | `self.lose()` present |
| CHECK_CAMERA_DEFAULT | ✅ | — | — | all levels share grid_size 64×64; resize not required |
| CHECK_WITNESS_WINS | ✅ | ✅ | ✅ | L1 (18 actions), L2 (9 actions), L3 (27 actions) all reach next_level / WIN |
| CHECK_VISUAL_SANITY | PASS | PASS | PASS | renders match spec (3 vessels + valves + HUD on L1; +drain on L2; +drain+pump on L3); PNGs at workspace/smoke-frames/level_*.png |

### Visual sanity per-level diagnoses

- **L1**: PASS. Three identical tall vessels arranged side by side; vessel A filled with blue water about 24/30 high (meniscus visible at top), B and C empty. Magenta target ticks at row 8 on each vessel's right side. Yellow valve bars (closed) visible in both inter-vessel gaps. Step-counter HUD bar visible at bottom of frame (yellow).
- **L2**: PASS. Vessel A at 12, vessel B at 24 (taller column) with drain glyph (dark square) at B's bottom-right corner, vessel C empty. Target ticks at A=12, B=8, C=8 magenta. Two yellow valve bars (closed) visible. HUD bar at bottom.
- **L3**: PASS. Vessel A near-full (30), drain glyph at A's bottom-right. Vessels B and C empty. V_AB at mid-height (slit-15) shows yellow bar; V_BC near bottom (slit-8) shows yellow bar. Pump glyph (orange-fins-in-grey-box, OFF state) visible in upper B↔C gap. Target tick on A near floor (target = 0) magenta. HUD bar at bottom.

No catastrophic rendering issues. No sprites resemble letters/digits/clipart. Playfield fills the frame; no corner-patch bug.

## Custom checks

| Check | Observed | Notes |
|---|---|---|
| check_action6_toggles_valve | V_AB.is_open before=False after=True | ACTION6 click on the closed valve at (21, 42) toggles it open — verifies the valve hit-test + InteractionMode swap idiom. |
| check_action5_with_open_valve_transfers | A 24→23, B 0→1 | After opening V_AB on L1, one ACTION5 transfers exactly one cell A→B — verifies the per-tick valve transfer rule. |
| check_l2_drain_consumes | B 24→23 | One ACTION5 on L2 (no valves toggled) reduces B's level by exactly 1 — verifies the always-on drain rule. |
| check_l3_pump_lifts_uphill | B 8→7, C 0→1 | After staging water in B (8 cells via 22 phase-A ticks) and turning on P_BC, one ACTION5 transfers one cell B→C uphill (B=8 = V_BC slit, gravity capped) — verifies the pump's uphill-override rule. |

Visit count: 1/6.
