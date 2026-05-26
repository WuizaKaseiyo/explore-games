# Step #04: critique_spec (round 1)

## Inputs Consumed
- workspace/mechanic-spec.md (from #03 write_spec)
- workspace/mechanic-pick.md (cached from #02)
- skills/design-constraints/checklist.md (full re-walk against all 22 items)
- skills/design-constraints/forbidden-elements.md (specifically items 7, 21)
- skills/design-constraints/difficulty-rules.md (specifically item 18)
- skills/mechanic-novelty/{similarity-check.md, negative-similarity-check.md} (full re-walk against full spec)
- prior-games/index.md (cached)
- skills/global/{action-enum.md, color-legend.md, paths.md} (cached)

## Deliverables Produced
- workspace/critique-revisions.md — 3 issues flagged, all with concrete fix suggestions.

## Notes
- Issue 1: `valve_closed` X-pattern reads as the Latin letter "X" — forbidden per §3.4. Fix: solid grey (palette 3) instead.
- Issue 2: `pour_cursor` downward triangle is a directional arrow — forbidden cultural convention. Fix: hollow yellow square (no direction).
- Issue 3: L3's M3 is not counterfactually necessary — the "open A-B only, isolate C" alternate fits the 19-action budget without ever firing the overflow cap. Fix: add a 4th vessel D at L3, bump budget to 20.
- All other checklist items (1-22) pass on a re-walk.
- Novelty check still PASS — adding a 4th vessel doesn't introduce new overlap with any taxonomy entry or prior.
- Transitioning back to `write_spec` for revision (revision visit #1 of allowed 10).
