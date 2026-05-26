# Step #06: smoke_test

## Inputs Consumed
- prior-games/qy7w/qy7w.py
- workspace/mechanic-spec.md (for witness coordinates)
- skills/code/smoke-test-checks.md (Tier 1 universal checks + custom-check authoring rules)

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom checks (binary toggle, long toggle outer-swap, shift colour change, step budget lose).
- workspace/smoke-test-pass.md: per-check ✅/PASS table.
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames per level for visual-sanity inspection.

## Notes
- All 13 universal checks (10 named + 3 per-level expansions of CHECK_CAMERA_VIEWPORT, CHECK_SPRITE_CONTENT, CHECK_PALETTE_RANGE) PASS on first attempt.
- All 4 custom checks PASS on first attempt.
- One pre-test refinement: the `shift_green` sprite's original 6×6 cross-hatch pattern resembled a face when rendered (two black dots at top, two centre, two bottom — could be read as eyes/nose/chin). Replaced with a concentric green/black/green ring pattern that is unambiguously abstract per `forbidden-elements.md` (no real-world clipart, no cultural conventions). Re-rendered frames confirmed the new pattern is non-representational.
- Visit count to smoke_test: 1 (first entry). Cap is 6.
