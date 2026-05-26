# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02 pick_mechanic): 4-char ID `mz6t`, family `majority-vote-stabilize`, paragraph description, novelty verdict.
- skills/code/spec-template.md, skills/code/universal-scaffold.md (in memory)
- skills/design-constraints/{checklist, composition-and-tutorial, difficulty-rules, core-knowledge-priors, forbidden-elements}.md (in memory)
- skills/conventions/reference-game-patterns.md (cached patterns for inheritance + anti-patterns)
- skills/global/{action-enum, color-legend}.md (in memory)

## Deliverables Produced
- mechanic-spec.md: full 9-section spec. EXACTLY 3 levels. Per-level: mechanics required (with `+1 or +2` math: L1=2, L2=3, L3=4), counterfactual-necessity sentences for *every* mechanic at every level (M1, M2, M3, M4 stated per L1/L2/L3), shortest witness solutions with concrete pixel coordinates, four difficulty-justification bullets per level. Win/lose predicates concrete. Novelty re-grounded against 5 priors + 2 taxonomy near-misses with distinguishing rules.

## Notes
- Tick rule design choice: win check fires *only* on ACTION5 (tick), not on every action. This is a deliberate engine-side enforcement that makes M2 (tick) structurally required; without it, click-only would be a valid alternate witness and M2 would be hidden. The pattern is uncommon in the 25 reference games (sb26 is the closest analogue — its ACTION5 = "submit row") but justified by the mechanic.
- L1 is intentionally minimal (2-action witness). L2 adds walls with the witness using tick-propagation as a shortcut over click-only (5 actions vs 6). L3 adds anchor-freeze; the trivial heuristic that fails is "click the anchor once and tick" — defeating it requires reasoning that pink is two cycle-clicks away, not one.
- Walls in L2 are *functionally* protective — they prevent the orange line from being voted to lb. Walls in L3 carry the same protection. Counterfactual no-walls ticks would actively destroy the witness state.
- Anchor freeze in L3 is necessary because without it, the (2,2) pink anchor would flip to orange during the final tick (4 orange neighbours produce a state-1 majority).
- Witness pixel coordinates use cell-centre formula: `(2 + col*8 + 4, 2 + row*8 + 4)`.
- Spec contains one inline correction note about an L2 pixel mistype; the corrected witness lines are presented immediately after.
