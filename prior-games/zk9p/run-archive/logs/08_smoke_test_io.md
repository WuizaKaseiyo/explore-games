# Step #08: smoke_test

## Inputs Consumed
- prior-games/zk9p/zk9p.py
- prior-games/zk9p/metadata.json
- workspace/implement-summary.md
- skills/code/smoke-test-checks.md (universal checks 1-9 plus custom-check template)
- workspace/mechanic-spec.md (visual sanity grounding for §4 layout claims)

## Deliverables Produced
- workspace/smoke-test-custom.py — 4 custom checks (check_up_moves_avatar, check_pursuer_chases_after_avatar_move, check_l1_minimal_solve_advances_level, check_lose_at_budget). Each conforms to the strict template (≤5 setup actions, 1 action under test, 1 boolean assertion).
- workspace/smoke-test-pass.md — all 9 universal checks + 4 custom checks PASS on first visit.
- workspace/smoke-frames/level_{1,2,3}.png — initial-frame renders for each level (used by CHECK_VISUAL_SANITY and useful for novelty comparison in future runs).

## Notes
- Universal static checks (CAMERA_VIEWPORT, SPRITE_CONTENT, ACTION_BRANCHES, ACTION_RUNTIME, PALETTE_RANGE, WIN/LOSE_PATH, CAMERA_DEFAULT) all pass on first run.
- Visual sanity: all 3 rendered frames match the spec's §4 per-level layout claims (entity count, coarse positioning, HUD presence, no glyphs).
- Custom checks confirm the four essential mechanic invariants: avatar movement, pursuer chase, merge → next_level wiring, step-budget → lose wiring.
- Visit count: 1/6. Plenty of headroom but unused.
- Transition: finalize.
