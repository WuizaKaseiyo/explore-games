# Step #10: smoke_test (visit 1 of max 6)

## Inputs Consumed
- prior-games/bz3k/bz3k.py (from #09 implement)
- mechanic-spec.md (rev 2) — for witness sequences and visual expectations
- skills/code/smoke-test-checks.md — universal check definitions
- workspace/smoke-test-custom.py (authored inline this state)

## Deliverables Produced
- smoke-test-custom.py: 4 custom checks
  (arrow_applies_impulse, consecutive_arrows_accumulate,
  cap_clamps_velocity, flipper_negates_velocity).
- smoke-test-pass.md: all 10 universal + 4 custom checks PASS.
- smoke-frames/level_{1,2,3}.png: rendered initial frames per level.

## Notes
- All 3 spec witnesses replay end-to-end and reach GameState.WIN.
- Custom checks confirm the four mechanic invariants directly:
  ±1 impulse per press; cumulative velocity; cap clamps to 1;
  flipper negates.
- Visual sanity vision-pass confirmed all 3 levels render
  per-spec layout (open arena → wall-column-passage →
  corridor with cap+flipper+hazard).
- Transition condition met. Proceeding to finalize.
