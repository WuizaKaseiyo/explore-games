# Step #06: smoke_test

## Inputs Consumed
- prior-games/xv2b/xv2b.py + metadata.json (from #05)
- workspace/mechanic-spec.md
- skills/code/smoke-test-checks.md

## Deliverables Produced
- workspace/smoke_test_custom.py (4 custom checks)
- workspace/smoke-runner.py (orchestrator)
- workspace/smoke-test-pass.md (PASS verdict)
- workspace/smoke-frames/level_{1,2,3}.png (rendered frames for visual inspection)

## Notes
- All 10 universal checks PASS, including CHECK_WITNESS_WINS (L1=18 actions, L2=9, L3=27 — every witness advances past its level).
- All 4 custom checks PASS (valve toggle, valve flow, drain consume, pump uphill).
- Visual frames match spec: vessels arranged in 3 columns with blue water fill bars, magenta target ticks, yellow closed-valve bars, drain glyph at L2 (B's corner) and L3 (A's corner), orange pump glyph at L3, yellow HUD bar at frame bottom.
- camera renders at scale 1 (grid_size = 64x64 == camera viewport); no per-level camera resize required.
