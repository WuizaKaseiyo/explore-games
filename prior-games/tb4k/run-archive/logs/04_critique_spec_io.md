# Step #04: critique_spec

## Inputs Consumed
- mechanic-spec.md (from #03): the spec under review.
- skills/design-constraints/checklist.md: 25 items to verify.
- skills/design-constraints/difficulty-rules.md: difficulty floor/ceiling rules.
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md.
- skills/mechanic-novelty/taxonomy-of-25-games.md.
- prior-games/index.md: cumulative corpus.
- prior-games/hb5n/mechanism-detail.md (read in #02): closest prior neighbour.

## Deliverables Produced
- critique-pass.md: all 25 checklist items pass; per-mechanic counterfactual table; per-level plausible-alternate enumeration for L2 and L3; positive + negative similarity checks re-run on the full spec.

## Notes
- Visit count: 1 (cap 10).
- One minor implementation note carried forward: reserve Bloxorz y=0 for HUD (lives pips occupy that row).
- L2 has 3 viable detour paths (mid-N, far-N, far-S), all 16 tumbles. Mid-S dies. All viable paths engage M2.
- L3 has a unique winning route through the y=3 bridge.
- All goal positions chosen to have same-parity-as-start (Bloxorz tumble physics requires this for reachability of standing).
