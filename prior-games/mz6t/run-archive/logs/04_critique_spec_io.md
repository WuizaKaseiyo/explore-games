# Step #04: critique_spec

## Inputs Consumed
- mechanic-spec.md (from #03 write_spec): full 9-section spec for `mz6t`.
- skills/design-constraints/{checklist, composition-and-tutorial, difficulty-rules, core-knowledge-priors, forbidden-elements}.md (in memory)
- skills/mechanic-novelty/{similarity-check, negative-similarity-check, taxonomy-of-25-games, prior-games-index-format}.md (in memory)
- skills/global/action-enum.md (in memory)
- prior-games/index.md (in memory; already novelty-checked at #02)

## Procedure
Walked checklist.md items 1-22 adversarially against `mechanic-spec.md`. Re-ran similarity-check (positive) and negative-similarity-check on the fleshed-out spec. Verified counterfactual necessity per (mechanic, level) pair by walking each named alternative strategy concretely. Re-examined the L3 M4 (anchor freeze) borderline at length — the initial walkthrough flagged it as borderline because a greedy "click each diff cell" alternate seemed to win without freeze; closer re-examination showed that the greedy alternate also flips `(2,2)` to state-1 during the final tick (not state-2 = pink), so it fails the target match — making M4 strictly necessary after all.

## Deliverables Produced
- critique-pass.md: ✅ verdict on every checklist item plus a per-mechanic-per-level table for item 12 (counterfactual necessity), plus a re-run of positive and negative similarity-checks. Concludes PASS with one note on L3 planning depth (shallow but acceptable given the cellular-automaton mechanic's natural limits).

## Notes
- L3 (c) planning depth is the only item with a written caveat. The CA-majority mechanic fundamentally limits how much a tick can save clicks: 3-of-4 majority means seed cells must be densely planted, so "click everything + tick" is comparable in length to "click strategic seeds + tick to fill". I evaluated several alternative L3 designs (multiple anchors, stubborn cells, passive cells, alternative anchor target colours) and none produced significantly deeper post-discovery planning without breaking strict counterfactual necessity for M4. Accepting L3's planning depth as "shallow but acceptable".
- The L3 M4 strict-necessity argument was tightened during this walkthrough — the borderline initial reading was wrong; verified that ALL alternate winning paths require the freeze to keep `(2,2)` at state 2 through the final tick.
- Single critique visit (1 of 10 budget); transitioning straight to `implement`.
