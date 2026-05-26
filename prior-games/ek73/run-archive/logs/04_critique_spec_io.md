# Step #04: critique_spec (visit 1)

## Inputs Consumed
- states/critique_spec.md (from harness root): the 18-item checklist + revision-cap rule.
- skills/design-constraints/checklist.md (from #01): items 1-21 (the file uses 1-21, the state file says 1-18 — read both as authoritative).
- skills/design-constraints/{composition-and-tutorial,difficulty-rules,core-knowledge-priors,forbidden-elements}.md (from #01).
- skills/mechanic-novelty/{similarity-check,negative-similarity-check,taxonomy-of-25-games}.md (from #01).
- workspace/mechanic-spec.md (from #03): the 9-section spec under review.
- workspace/mechanic-pick.md (from #02): the prior novelty argument.

## Deliverables Produced
- `workspace/critique-revisions.md`: 5 substantive issues + lighter ones, each with rule violated, offending section quoted, concrete fix. Verdict: REJECT, transition back to `write_spec`.

## Notes
- Visit count: 1 / 10.
- The spec self-flagged 2 of the 5 issues (L2 wrong-path argument; L3 sticky necessity). Found 3 more under independent review (L1 wake non-load-bearing; L3 planning-depth heuristic divergence vague; L2 spiral co-cell duplication implementation-fragile).
- Novelty re-walk passed: no taxonomy or prior-game row drifted into too-similar territory in the fleshed-out spec. Five near-miss flags from §9 (g50t / sk48 / fz5j / wt39 / zd7m) all retain valid distinguishing rules.
- Negative similarity 8-dim re-walk: closest concern remains `fz5j` at 3 shared dims (1, 2, 4); engineered divergences on dim 6/7/8 hold for the spec as a whole. Pass.
- Items 1-9, 13-17, 19-21 all pass. Failures concentrated at item 12 (L1, L3) and item 18 (L2 (c), L3 (c)).
- Transition: → write_spec (revision pass 2).
