# Step #05: write_spec (revision 1)

## Inputs Consumed
- critique-revisions.md (from #04): 2 issues to fix
- previous mechanic-spec.md (from #03): the artifact being revised
- skills/design-constraints/{checklist,difficulty-rules,composition-and-tutorial}.md (re-read for L3 redesign)
- skills/code/spec-template.md

## Deliverables Produced
- mechanic-spec.md (revised). Changes:
  - Section 4 / Level 3: Option A applied. Walls dropped. L3 has +1 new mechanic (lock-on-target) only. Yellow target moved from (28, 28) to (36, 28) so the V-fold at F_v=32 lands yellow on its target and locks it. M4 (lock) is now unambiguously counterfactually required: the witness's double-V-fold + final-H-fold pattern depends on green and yellow being locked after the first V-fold.
  - Section 4 / Level 2 / *Difficulty justification* / (c) plausible-but-wrong: replaced the stage-conflated "commit V at F_v=30 immediately" with a post-discovery V-only-translation argument: a fully-informed player who understands V-fold arithmetic might attempt to solve L2 using only V-folds (translation by composition); they reject this on arithmetic grounds (V-folds preserve rows and the pawns' rows must change), forcing the H-fold and axis-toggle path.
  - Section 3 (sprite roster): wall sprite removed.
  - Top of spec: added a "Revision 1" header marking the change set and citing the critique issues.

## Notes
- L3 mechanic count: 4 mechanics (M1 V-fold, M2 H-fold, M3 axis-toggle, M4 lock-on-target). +1 from L2's 3 mechanics. Within the +1-or-+2 rule (allowed by `composition-and-tutorial.md`).
- Yellow now visibly exercises both V-fold (movement) and lock-on-target (lock after movement) — its trajectory in the witness goes (28,28) → (36,28)=target → LOCK → stays for the second V and the H.
- All other sections unchanged from the previous spec (action mapping, HUD, win/lose, novelty).
- Re-walked checklist items 1–21 mentally; all pass on the revised spec. Novelty checks unchanged (drop of walls doesn't affect taxonomy/prior-game distinguishing rules).
