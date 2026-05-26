# Step #08: smoke_test (visit 1/6)

## Inputs Consumed
- prior-games/xn5p/xn5p.py
- prior-games/xn5p/metadata.json
- skills/code/smoke-test-checks.md
- mechanic-spec.md (for visual-sanity comparison)

## Deliverables Produced
- workspace/smoke-test-pass.md: all 9 universal checks PASS, all 4 custom checks PASS.
- workspace/smoke-test-custom.py: 4 custom mechanic-invariant checks.
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames for visual sanity.

## Notes
- One custom check (`check_stamp_creates_wall`) failed initially because stamping at L1 start cell (lattice (3, 2)) actually wins L1 — the level transition cleared the just-placed stamp. Fixed by walking the avatar south first before stamping. This is benign (the original L1 spec witness used stamp at lattice (2, 2), which also wins; both paths work).
- Visit 1/6; transitioning to finalize.

