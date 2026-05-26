# Step #06: smoke_test

## Inputs Consumed
- prior-games/wt39/wt39.py (from #05 implement).
- prior-games/wt39/metadata.json (from #05 implement).
- workspace/mechanic-spec.md (from #03 write_spec).
- skills/code/smoke-test-checks.md (from #01 study).

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom checks (slide, bumper, thaw, lose).
- workspace/smoke-test-pass.md: all 9 universal + 4 custom checks pass.
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames.

## Notes
- All universal checks pass on first attempt. No fix-loop required.
- All 4 custom checks pass on first attempt.
- Visual sanity: each level's render matches its spec section's described sprite set and coarse placement. No forbidden glyphs.
- Visit count: 1/6.
EOF