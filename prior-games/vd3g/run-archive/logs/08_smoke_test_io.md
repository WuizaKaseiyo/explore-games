# Step #08: smoke_test

## Inputs Consumed
- prior-games/vd3g/vd3g.py: generated source.
- mechanic-spec.md: per-level witnesses extracted into the smoke runner.
- skills/code/smoke-test-checks.md: 10-check + custom-check template.

## Deliverables Produced
- workspace/smoke-test-runner.py: runs all 10 universal checks + 4 custom checks.
- workspace/smoke-test-custom.py: alias of the runner exposing the custom checks per skill spec.
- workspace/smoke-frames/level_1.png, level_2.png, level_3.png: rendered initial frames.
- workspace/smoke-test-aggregate.json: machine-readable aggregate of every check's pass/observed.
- workspace/smoke-test-pass.md: per-level + per-check summary; ALL_PASS = True.

## Notes
- All 10 universal checks PASS.
- 4 custom checks PASS:
  - click_toggles_normal_cell — clicking a HIGH normal cell flips it to LOW.
  - marble_rolls_to_dug_low — digging adjacent cell makes marble roll one cell.
  - anchor_click_flips_partner — single click on one anchor flips both linked cells.
  - lose_at_budget_exhaustion — spending budget+1 clicks fires lose().
- L1 witness 6 actions → next_level. L2 witness 32 actions → next_level. L3 witness 30 actions → WIN.
- Visual sanity inspection of level_1..3.png: each rendered frame matches the spec's per-level description (sprite count, placement, HUD presence, no rendering bug).
- Visit count for smoke_test: 1/6.
