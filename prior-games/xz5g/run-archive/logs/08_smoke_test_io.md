# Step #08: smoke_test

## Inputs Consumed
- prior-games/xz5g/xz5g.py (the implementation)
- prior-games/xz5g/metadata.json
- mechanic-spec.md (witnesses + per-level layouts)
- skills/code/smoke-test-checks.md (10 universal + custom-check templates)
- /tmp/run_universal_checks.py (script written ad-hoc to drive all 10 universal checks)

## Deliverables Produced
- workspace/smoke-test-custom.py: 3 custom checks (pivot-set,
  rotate-action, direction-toggle) — each ≤ 5 setup actions, single
  boolean assertion, deterministic.
- workspace/smoke-test-pass.md: per-check table + visual sanity
  per-level + custom check results.
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames
  for each level (used by CHECK_VISUAL_SANITY).

## Notes
- All 10 universal checks PASS.
- All 3 custom checks PASS.
- Visit count: 1/6 (well below cap).
- Visual sanity: minor cosmetic note — at L3 the companion's
  6×6 footprint at (8, 32) overlaps the anchor_pin's 4×4
  footprint at (12, 32) at level start; this is cosmetic only
  (visit-checkpoint triggers on top-left equality, not
  footprint overlap). Documented in smoke-test-pass.md.
