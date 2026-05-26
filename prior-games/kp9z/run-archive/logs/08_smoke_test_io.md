# Step #08: smoke_test

## Inputs Consumed
- prior-games/kp9z/kp9z.py (under test)
- workspace/mechanic-spec.md (for visual sanity comparison)
- skills/code/smoke-test-checks.md (universal check protocol + custom-check template)

## Deliverables Produced
- workspace/smoke-test-runner.py: universal-check runner (8 checks).
- workspace/smoke-test-custom.py: 4 custom checks (drop-increments-source, l1-minimal-solve, sink-absorbs, redirector-forwards).
- workspace/render-frames.py: renders initial frames for all 3 levels.
- workspace/smoke-frames/level_{1,2,3}.png: rendered 512×512 PNGs.
- workspace/smoke-test-pass.md: full pass report.

## Notes
- All 8 universal checks pass cleanly.
- All 4 custom checks pass.
- Visual sanity inspection: all 3 levels render correctly per the spec; cell types are pairwise visually distinguishable via colour + frame-edge notch / corner pip features.
- The cleaned-up __pycache__ from implement was recreated by smoke test; will clean again before finalize.
- `python` was used in CWD = repo root (`/Users/nickhe/Programming/NovaPlay-Agents`).
