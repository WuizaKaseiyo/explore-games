# Step #04: critique_spec

## Inputs Consumed
- mechanic-spec.md (from #03 write_spec)
- skills/design-constraints/checklist.md (1-21 items)
- skills/design-constraints/difficulty-rules.md (§ 2 critique check per-level)
- skills/design-constraints/forbidden-elements.md
- skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check}.md
- skills/mechanism-details/<id>.md and prior-games/index.md (re-checked novelty)

## Deliverables Produced
- `workspace/critique-revisions.md`: 3 issues (L2 18(d) decision space, L3 18(d) decision space, L2 wrong-alternative is discovery-stage) + 3 minor notes (eraser cross shape, goal frame shape, L2 alternates).

## Notes
Walked all 21 checklist items; novelty re-confirmed against 25 reference + 27 priors via similarity-check + negative-similarity dimensions. Most items pass:
- Items 1-9, 13-17, 19-21 all pass.
- Item 10 (composition): L2 composes walk+echo-teleport+closing-doors (closing-doors trigger seal that requires teleport that uses walked-cell echoes); L3 composes all+eraser (eraser forces visit-order around teleport availability).
- Item 11 (mechanic +1-or-+2): L1 N=1, L2 N+2=3, L3 L2+1=4. ✔
- Item 12 (counterfactual necessity): per-mechanic table with concrete cell/sprite blockers — passes with one note that M4-eraser is on the only path to G so its distinguishing-behavior fires every winning sequence per item 12 wording.
- Item 18 (difficulty floor/ceiling): L2 and L3 fail (d) decision-space count due to the start-cell layout having only 1 valid first action.

The novelty + negative-similarity walks against g50t, lf52, bp35, sk48, tu93, kf42, fz5j, kn58, wt39, zk9p, rk7x, zd7m, xn5p all pass after the fleshed-out spec. No spec-drift; L2 and L3 don't introduce any mechanic family that overlaps with priors beyond the distinguishing rules already articulated in §9.

Transitioning back to write_spec.
