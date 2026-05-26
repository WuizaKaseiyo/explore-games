# Step #06: smoke_test

## Inputs Consumed
- prior-games/rt9k/rt9k.py (from #05)
- prior-games/rt9k/metadata.json (from #05)
- mechanic-spec.md § 4 witness solutions, § 5 action mapping (used to author custom checks)
- skills/code/smoke-test-checks.md (universal-check spec + custom-check template)

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom checks (left moves avatar; LEFT-wrap changes tone; wall blocks movement; step budget decrements). Each check follows the strict template — ≤ 5 setup actions, one action under test, one boolean assertion.
- workspace/smoke-test-pass.md: PASS row for every universal check (10) + every custom check (4), with visual-sanity per-level diagnoses pointing to PNGs at workspace/smoke-frames/level_{1,2,3}.png.
- workspace/smoke-frames/level_1.png, level_2.png, level_3.png — rendered initial frames.

## Notes
- All 10 universal checks PASS first try; the witness replay is the strongest gate, and L1/L2/L3 witnesses (transcribed verbatim from `mechanic-spec.md` § 4 as `[3]*9`, `[3]*4 + [2]*12`, `[3]*4 + [1]*15`) drove the game from L1 start to WIN end without intermediate failures. This validates the implementation against the spec.
- Custom checks: chose 4 invariants — (i) basic walking, (ii) LEFT-wrap+tone-cycle (the load-bearing M1+M2 rule), (iii) wall blocking (the universal collision predicate), (iv) step-budget decrement (the lose-side resource). Skipped a "filter blocks wrong tone" check because every concrete reachable filter cell happens to be passable for the avatar's current tone within ≤ 5 setup actions; instead, the wall-block check tests the same predicate family with cleaner geometry.
- Visual sanity revealed an aesthetic-but-not-functional issue: L3 had `filter_yellow` and `filter_green` overlapping at cell (col 14, row 14). My `_filter_at` resolves overlap to green by insertion order, while the camera rendered yellow on top — a visual/behavioural mismatch that would mislead a player even though the witness path doesn't traverse the cell. Fixed by reducing the yellow strip to cols 9..13. Re-ran all checks; all PASS. The spec's counterfactual necessity argument for filter_yellow still holds because the witness exercises filter_yellow at (col 13, row 14), and alternative paths still pass through cols 9..13 row 14.
- This is a single-visit smoke pass (1 / 6 of the cap). Transitioning to `finalize`.
