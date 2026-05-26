# Step #08: smoke_test (visit 1/6)

## Inputs Consumed
- prior-games/pn5d/pn5d.py
- workspace/mechanic-spec.md (round 2)
- skills/code/smoke-test-checks.md (full)

## Deliverables Produced
- workspace/smoke-test-runner.py — single-shot test runner.
- workspace/smoke-test-custom.py — 4 custom checks.
- workspace/smoke-frames/level_{1,2,3}.png — rendered initial frames per level.
- workspace/smoke-test-pass.md — full pass report.

## Notes
- All 10 universal checks passed on first attempt. All 4 custom checks passed.
- HUD bar rendering: technically present at row 63 (palette 4 on palette 5 background). Contrast is subtle in the rendered PNG due to similarity of off-black (0x3C) and black (0x00). Not a failure per CHECK_VISUAL_SANITY guidance — the HUD is "visible somewhere on the frame".
- CHECK_WITNESS_WINS replayed all 3 spec witnesses end-to-end:
  - L1: 4 pours → score 0 → 1 ✓
  - L2: 10-action sequence → score 1 → 2 ✓
  - L3: 12-action sequence → score 2 → 3 + state WIN ✓
- All rendered frames look spec-aligned: vessels in upper playfield row, cursor above, valves in gaps, target pips inside right walls, overflow lip outside C's left wall (L3 only).
- No `__pycache__` cleanup needed since no test scripts wrote .pyc files outside the runner's standard locations.
- Transitioning to `finalize`.
