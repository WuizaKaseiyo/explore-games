# Step #08: smoke_test (visit 1)

## Inputs Consumed
- prior-games/gv47/gv47.py
- skills/code/smoke-test-checks.md (Tier-1 universal checks + custom check templates).
- workspace/mechanic-spec.md (per-level expectation reference for CHECK_VISUAL_SANITY).

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom checks (click_seed_grows_region, action5_mixes_when_in_contact, wind_extends_growth, lose_when_budget_exhausted), each with ≤5 setup actions and ONE boolean assertion.
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames for the visual-sanity pass.
- workspace/smoke-test-pass.md: all 9 universal checks + 4 custom checks PASS.

## Notes
- Visual sanity flagged a cosmetic-only adjacency between the red and purple target frames at L3 (no separator cell between them). Pip cells (9, 5) and (11, 5) remain individually addressable; not a functional failure.
- All checks PASS at visit #1. Transition to finalize.
EOF
