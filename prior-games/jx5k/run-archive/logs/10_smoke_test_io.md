# Step #10: smoke_test (visit 1)

## Inputs Consumed
- prior-games/jx5k/jx5k.py: just-implemented source.
- skills/code/smoke-test-checks.md: 10 universal checks + custom-check template.
- workspace/mechanic-spec.md: per-level expected layouts and witnesses.

## Deliverables Produced
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames per level.
- workspace/smoke-test-custom.py: 4 custom-check functions matching the spec's mechanic invariants.
- workspace/smoke-test-pass.md: per-check verdict table; all 10 universal checks pass, all 4 custom checks pass.

## Notes
- Visit count: 1 / 6 (cap is 6).
- All universal checks pass on the first run — no fix iteration needed.
- Custom checks are minimal-template-conforming (≤ 5 setup actions, single boolean assertion each, deterministic).
- Vision-pass observations: each level renders with rich internal sprite detail (checker-pattern node interior + grey pip markers + green HUD strip); no level shows uniform-colour cell-blocks (per checklist item 20). Palette diversity is good — L1 uses `{1, 3, 4, 9, 14}` (5 distinct), L2/L3 use `{1, 3, 4, 8, 9, 14}` (6 distinct).