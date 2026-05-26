# Step #06: smoke_test

## Inputs Consumed
- prior-games/mz6t/mz6t.py (from #05 implement).
- skills/code/smoke-test-checks.md (in memory).
- mechanic-spec.md (for witness sequences).

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom check functions exercising click-cycles-state, tick-propagates-majority, anchor-locks-on-target, win-fires-only-on-tick.
- workspace/smoke-test-pass.md: PASS table covering 10 universal checks (per level where applicable) + 4 custom checks.
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames for the visual-sanity pass.

## Notes
- All 9 deterministic universal checks pass cleanly. CHECK_VISUAL_SANITY (vision pass) confirms each rendered initial frame matches the spec's per-level description: sprite count, placement, HUD presence, and no catastrophic rendering bugs.
- CHECK_WITNESS_WINS replayed all three spec witnesses against the loaded game: L1 → score 1 (2 actions), L2 → score 2 (5 actions), L3 → state WIN (7 actions). All pass deterministically.
- One initial check_tick_propagates_majority failure was due to a wrong assertion in the check (was checking score advancement; level doesn't advance because (1,1) target wasn't satisfied). Corrected the assertion to read `_cell_state[(2,2)]` directly before/after the tick. Now passes.
- One pycache cleanup at end. Single smoke_test visit (1/6).

## Transition
Universal + custom checks all pass. Transition to `finalize`.
