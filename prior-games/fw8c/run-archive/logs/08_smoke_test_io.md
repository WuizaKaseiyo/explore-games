# Step #08: smoke_test

## Inputs Consumed
- prior-games/fw8c/fw8c.py (from #07): 495-line implementation.
- mechanic-spec.md (rev 2 from #05): for witness sequences and visual sanity reference.
- skills/code/smoke-test-checks.md (from study): full check battery + custom-check templates.

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom check functions (check_arrow_moves_carrier, check_pad_pickup_sets_pigment, check_slot_consume_clears_pigment, check_door_blocks_when_unmatched). Each conforms to the strict template (≤ 5 setup actions, ONE action under test, ONE boolean assertion, deterministic). All pass.
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames per level for visual sanity.
- workspace/smoke-test-pass.md: per-level PASS verdicts for all 10 universal checks + 4 custom checks.

## Notes
- All universal checks pass: camera viewport == grid_size for every level, sprite content non-empty (6/8/10 distinct palette values), all declared actions branched and exception-free at runtime, palette in [0,15], win and lose paths present in source, all 3 level witnesses replay successfully (L1→advance, L2→advance, L3→WIN state).
- Visual sanity passed via PNG inspection of all 3 levels; sprite counts, placements, HUD presence, and absence of glyphs all confirmed.
- 4 custom checks verify the load-bearing mechanic invariants: arrow moves carrier; pad pickup ORs pigment bit; slot consume clears carrier; pigment-gated door blocks when state mismatches.
- Smoke test visit count: 1 of 6 maximum.
- Verdict: PASS. Transition to finalize.
EOF
EOF