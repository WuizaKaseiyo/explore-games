# Step #06: smoke_test

## Inputs Consumed
- `prior-games/mw8p/mw8p.py` (from #05): the generated source.
- `prior-games/mw8p/metadata.json` (from #05): metadata.
- `workspace/mechanic-spec.md` (from #03): witness sequences for
  CHECK_WITNESS_WINS (L1: `[4]*7+[1]*7`, L2: `[4]*7+[2]*7`, L3:
  `[4]*7+[1]*7`).
- `skills/code/smoke-test-checks.md`: 10 universal check definitions
  + custom-check template & constraints.

## Deliverables Produced
- `workspace/smoke-test-custom.py`: 4 custom checks
  (check_right_moves_player, check_a_eats_c_on_entry,
  check_c_kills_b_on_coincidence, check_lose_at_budget) — each
  conforming to the template's hard constraints (≤ 1s wall-clock,
  deterministic, ≤ 5 setup actions, 1 action under test, 1 boolean
  assertion, essential mechanic invariant).
- `workspace/smoke-test-pass.md`: all 10 universal checks + 4
  custom checks reported PASS.
- `workspace/smoke-frames/level_{1,2,3}.png`: rendered initial
  frames for the visual sanity pass.

## Notes
- The 4 custom checks cover the 3 mechanics (M1's pursuit verified
  indirectly via check_c_kills_b_on_coincidence which requires M1's
  pursuit to position B at C's catch cell; M2 directly; M3 directly)
  plus the budget-exhaustion lose path. The mover-basic check
  (right-moves-player) verifies the lowest-level invariant.
- CHECK_WITNESS_WINS replays the exact action sequences from spec § 4
  on a freshly-instantiated game and confirms each level's witness
  advances the engine state. L1 0→1, L2 1→2, L3 reaches `WIN`.
- CHECK_VISUAL_SANITY: each rendered frame opened and compared
  against the spec's per-level layout description. All three match:
  L1 shows the walled 3-zone playfield with B in the middle chamber
  and A in the bottom-left corridor and exit in the top-right; L2
  shows the open arena with the C/B vertical pair in col 4 and A
  and exit at opposite corners; L3 shows the row-7 creature lineup
  (A, C₁, gap, C₂, gap, B) with the wall row above row 7. No
  rendering bugs (no chunky upscale, no missing sprites, no off-
  screen placements, no glyph-resembling sprite shapes).
- Visit count: 1/6. All checks passed on first entry — no
  fix_implementation loop needed.
