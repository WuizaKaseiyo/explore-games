# Step #08: smoke_test (visit 1)

## Inputs Consumed
- prior-games/kj82/kj82.py (from #07 implement)
- workspace/mechanic-spec.md (revision 2): per-level spec descriptions for visual-sanity check
- skills/code/smoke-test-checks.md (Tier 1 + custom-check templates, from #01 study)

## Deliverables Produced
- workspace/smoke-test-custom.py (4 custom checks)
- workspace/smoke-test-pass.md (full pass report)
- workspace/smoke-frames/level_1.png, level_2.png, level_3.png

## Notes
- All 10 universal checks pass; all 4 custom checks pass.
- Witness replay: L1 (6 actions) → L2 (23 actions) → L3 (18 actions) → WIN. Score progression 0→1→2→3.
- Visual sanity verified by inspecting rendered PNGs against spec descriptions; all 3 levels match.
- Visit count: 1/6 (well under cap).
- Transitioning to `finalize`.
