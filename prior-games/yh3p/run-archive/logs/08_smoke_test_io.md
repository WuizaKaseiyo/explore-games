# Step #08: smoke_test (visit 1)

## Inputs Consumed
- prior-games/yh3p/yh3p.py: the implementation under test.
- workspace/mechanic-spec.md: spec witnesses + structural claims.
- skills/code/smoke-test-checks.md: 10 universal checks + custom-check authoring rules.

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom checks (extend-moves-tip, wall-blocks-extend, click-resets-facing, bloom-requires-facing-match) — all PASS.
- workspace/smoke-test-pass.md: tabulated results for 10 universal checks across 3 levels + 4 custom checks; all PASS.
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames of each level for visual verification.

## Notes
- All 10 universal checks pass cleanly. Witness routes (12/29/40 actions) replay successfully from L1 → L2 → L3 → all buds bloomed.
- Visual sanity inspection caught one borderline issue: tip_dormant initially used palette {2, 3} which blended into the light-grey background, making the dormant tip hard to see. Applied a minor 1-line palette change (outer cells palette 2 → 0 white) — gives high-contrast white+grey checkered appearance. Re-rendered; all levels now visually clean.
- After the tweak, re-ran custom checks and instantiation — all still pass.
- Visit count: 1/6.
