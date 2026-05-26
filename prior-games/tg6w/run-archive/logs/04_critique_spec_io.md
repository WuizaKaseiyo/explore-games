# Step #04: critique_spec

## Inputs Consumed
- mechanic-spec.md (from #03 write_spec): full 9-section spec
- skills/design-constraints/checklist.md (full): 21 items
- skills/design-constraints/composition-and-tutorial.md, difficulty-rules.md (full): per-level structure + difficulty bullets
- skills/design-constraints/forbidden-elements.md (full): letter/digit/symbol prohibitions — flagged the X-pattern sticky-pad as a letter risk
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md (full): novelty re-check
- prior-games/index.md: re-read for any drift in distinguishing rules
- skills/code/spec-template.md (re-read): cross-reference §4 structure

## Deliverables Produced
- critique-pass.md: 21-item checklist pass with concrete row per item, per-mechanic counterfactual table for items 11-12, plausible-alternate enumeration per level, novelty re-check (4 taxonomy + 5 prior-games), negative-similarity 8-dim table. Verdict ACCEPTED; transition to implement.
- mechanic-spec.md edited in-place with two adversarial fixes:
  1. sticky_pad pixel pattern X→plus (item 7 risk: X resembles letter) — `[[6,-1,6],[-1,6,-1],[6,-1,6]]` → `[[-1,6,-1],[6,6,6],[-1,6,-1]]`. Plus-shape is explicitly permitted as a topological symbol.
  2. L3 row-3 layout typo: removed extra leading `█` from `█ █ Y █ █ █ O █` to match the 7-cell lattice.

## Notes
- One revision round (this counted as visit #1 since the fixes were applied in-place rather than transitioning back to write_spec). The remaining checklist items all passed without further structural changes.
- Stage-conflation guard (difficulty-rules.md item 18): verified that L2's "plausible-but-wrong LEFT-first" and L3's "trivial heuristic = greedy-DOWN-first" both describe POST-DISCOVERY errors, not discovery-stage missteps. L3's greedy-DOWN-first is especially good because it traps orange at the sticky-pad — a real post-discovery insight ("if I press DOWN first, orange goes to (5, 5); subsequent LEFT puts orange into the sticky") that a fully-informed player can still get wrong by not thinking ahead.
- Counterfactual necessity holds for every (mechanic, level) pair. The sticky-pad's role as the SOLE mechanism that stops yellow at (3, 5) is the load-bearing argument for M3 necessity — concrete cell citations and rule-out of every wall/border alternative.
- Novelty re-check on full spec: zd7m remains the closest concern at 3 shared dimensions; the divergent dimensions are the heavy ones (core dynamic, visual signature). Does not drift toward any prior at L2 or L3.
