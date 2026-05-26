# Step #06: smoke_test

## Inputs Consumed
- task-overview.md, states/smoke_test.md.
- skills/code/smoke-test-checks.md.
- prior-games/hl4n/hl4n.py (the game under test).
- mechanic-spec.md (witness sequences extracted for CHECK_WITNESS_WINS and the spec descriptions used for CHECK_VISUAL_SANITY).

## Deliverables Produced
- `workspace/smoke-test-custom.py`: 4 custom check functions covering row-recolor, L2 column-override, L3 brighter-wins, L1 minimal solve.
- `workspace/smoke-test-universal.py`: scripted universal checks (CAMERA_VIEWPORT, SPRITE_CONTENT, ACTION_BRANCHES, ACTION_RUNTIME, PALETTE_RANGE, WIN/LOSE path, WITNESS_WINS, frame rendering for VISUAL_SANITY).
- `workspace/smoke-frames/level_{1,2,3}.png`: rendered initial frames for visual inspection.
- `workspace/smoke-test-pass.md`: PASS table covering 9 universal checks (all 3 levels) + 4 custom checks.

## Notes
- All checks PASS on the first visit.
- The witness sequences extracted from the spec — L1 (6 actions), L2 (10 actions), L3 (15 actions) — replayed against a fresh game instance reach `GameState.WIN` exactly as predicted.
- Visual sanity: rendered PNGs match the spec's described layout per level. L1 shows row markers only (no column markers, by design); L2/L3 show both row+column marker rails framing the playfield; lock target rings are visible at the spec-specified cell positions; HUD bar present at bottom row.
- The L3 brighter-wins rule is exercised by check_l3_brighter_wins_row_dominates and again by the L3 witness — both pass.
- No revisits needed. Visit count: 1/6.
