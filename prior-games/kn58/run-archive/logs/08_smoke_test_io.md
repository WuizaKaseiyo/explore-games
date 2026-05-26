# Step #08: smoke_test

## Inputs Consumed
- prior-games/kn58/kn58.py (from #07 implement).
- workspace/mechanic-spec.md (for visual-sanity comparison).
- skills/code/smoke-test-checks.md (procedure + custom-check templates).

## Deliverables Produced
- workspace/smoke-frames/level_{1,2,3}.png — rendered initial frames at 512×512 (8× upscale).
- workspace/smoke-test-custom.py — 4 custom checks (anchor-pull, match-stick, collision-block, lose-at-budget).
- workspace/smoke-test-pass.md — all 9 universal + 4 custom checks PASS.

## Notes
- Visit count: 1.
- All universal checks passed without modification.
- All 4 custom checks passed first try.
- Visual sanity: each level's PNG matches the spec's described layout.
- Transition to `finalize`.
