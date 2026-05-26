# Step #06: smoke_test

## Inputs Consumed
- prior-games/rk7x/rk7x.py (from #05).
- skills/code/smoke-test-checks.md (9 universal checks + custom-check template).

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom-check functions, each obeying the ≤ 5 setup actions / single boolean / ≤ 1s template. (off-board-click ticks; click-switch toggles; L1 minimal-solve wins; lose-on-wall.)
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames for visual-sanity inspection.
- workspace/smoke-test-pass.md: all 9 universal checks + 4 custom checks PASS. Visual sanity per level: PASS.

## Notes
- All 8 structural universal checks passed without iteration. CHECK_CAMERA_DEFAULT vacuously trivially passes because all 3 levels share grid_size (64, 64); no per-level resize required.
- Visual sanity inspection of the rendered PNGs confirmed each level's sprite roster, placement, and HUD presence match the spec §3-§4 description. Pixel-grain richness: junctions show internal blade pattern (green horizontal cross OR magenta vertical cross); stops are hollow rings; terminals are concentric squares; courier has a directional tip.
- Custom checks were chosen to test the four most essential mechanic invariants:
  1. The "wait" verb (off-board click ticks the courier).
  2. The toggle verb (click on switch swaps H/V twin states).
  3. End-to-end winnability of L1.
  4. The wall-hit lose condition.
- All four customs PASSED on first run.
- Visit count: 1/6.

Transition: → finalize.
