# Step #06: smoke_test (visit 1/6)

## Inputs Consumed
- prior-games/yf3h/yf3h.py: the just-implemented game.
- prior-games/yf3h/metadata.json.
- workspace/mechanic-spec.md (carried): per-level descriptions for CHECK_VISUAL_SANITY.
- skills/code/smoke-test-checks.md (carried): 9 universal checks + custom-check rules.

## Deliverables Produced
- workspace/smoke-test-failures.md: 7 visual-sanity failures on L3 (sprite overlaps, OOB placement, pip-overlap with multi-resonator) + 1 custom check failure (phase_delay_tile click no-op due to interaction=INTANGIBLE blocking get_sprite_at).
- workspace/smoke-test-custom.py: 4 custom checks (action counter, arm-emitter toggle, phase-delay-tile toggle, L1 minimal solve).
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames for visual inspection.

## Notes
- All 8 programmatic universal checks PASSED on first run; visual sanity failed on L3 only.
- Visit count: 1/6 — transitioning to fix_implementation.
