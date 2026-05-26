# Step #08: smoke_test

## Inputs Consumed
- prior-games/rs8n/rs8n.py (the implementation)
- prior-games/rs8n/metadata.json
- mechanic-spec.md (for witness sequences and per-level visual expectations)
- skills/code/smoke-test-checks.md (the universal-check definitions and custom-check template)

## Deliverables Produced
- workspace/smoke-test-custom.py: 3 custom checks (`check_action4_walks_east`, `check_action5_reverses_row`, `check_action_counter_decrements`).
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames per level.
- workspace/smoke-test-pass.md: 9 universal checks + 1 visual-sanity check + 3 custom checks all PASS.

## Notes
- Visit count to smoke_test: 1/6.
- The two implementation bugs (item BOUNDING_BOX, shifter ignore_collidable) had already been fixed inline during the implement state's smoke test; the smoke_test state thus saw a clean run.
- CHECK_WITNESS_WINS independently confirmed all three level witnesses produce a WIN — same as the implement-state smoke but re-run from a fresh game instance.
- Visual sanity: all three rendered frames look correct against the spec — items in the right rows/cells, anchor + shifter visually distinct from walls, HUD present, no rendering bugs.
- Transition to finalize.
