# Step #04 + #06: critique_spec (round 1 + round 2)

## Inputs Consumed
- workspace/mechanic-spec.md (the 9-section spec)
- workspace/mechanic-pick.md (novelty argument)
- skills/design-constraints/checklist.md (items 1-22)
- skills/design-constraints/composition-and-tutorial.md
- skills/design-constraints/difficulty-rules.md
- skills/design-constraints/forbidden-elements.md
- skills/design-constraints/core-knowledge-priors.md
- skills/mechanic-novelty/{taxonomy-of-25-games, similarity-check, negative-similarity-check, prior-games-index-format}.md
- prior-games/index.md

## Deliverables Produced
- workspace/critique-revisions.md (round 1): one issue flagged — L3's Replay-walls was dormant in the witness (checklist 11/12 violation). Suggested concrete L3 v4 layout with detour wall at `(24, 36)` and replay-wall at `(44, 16)`, plus revised witness.
- workspace/critique-pass.md (round 2): all 22 checklist items pass; novelty confirmed; transition to implement.

## Notes
- Visit count tracked: 2 entries in state_log.md for `critique_spec` rows. Under cap of 10.
- Round-1 issue was caught by item 12's strict counterfactual rule applied to carried-forward mechanics: for Replay-walls to be "necessary" in L3, the witness must trigger its distinguishing behavior (a wall-induced skip during replay). The original L3 v3 layout had walls placed defensively but dormant in the witness, violating item 11's "no mechanic may drop out" rule.
- Round-1 fix was concrete: introduce a between-anchors detour wall that forces the actor to add DOWN+RIGHT+UP entries to the tape, then place a replay-wall in shade_yellow's path that skips the RIGHTs, leaving the trailing UP to land shade_yellow at target_yellow at `(40, 12)`.
- All 6 enumerated alternate strategies for L3 (including yellow-first, UP-detour, anchor-skipping) verified to fail by concrete cell-by-cell trace; only the witness (or close variants) reliably places shade_yellow at target_yellow.
- Per the state spec ("Be patient — a low-quality game that limps through the gates is worse than no game at all"), the round-1 issue was caught and revised cleanly rather than rubber-stamped.
