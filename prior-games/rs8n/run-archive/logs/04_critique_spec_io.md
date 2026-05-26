# Step #04: critique_spec

## Inputs Consumed
- mechanic-spec.md (from #03 write_spec): 9-section spec
- mechanic-pick.md (from #02 pick_mechanic): novelty argument (re-validated against full spec)
- skills/design-constraints/checklist.md (items 1-22)
- skills/design-constraints/forbidden-elements.md (re-applied to sprite roster pixel patterns)
- skills/mechanic-novelty/* (re-applied to full spec)
- skills/mechanism-details/ls20.md, dc22.md (consulted for shifter-vs-cycler distinguishing rule)

## Deliverables Produced
- critique-revisions.md: 3 issues found — (1) wall at (2,10) contradicts L3 witness step 8; (2) `item_yellow_xcross` reads as letter X (forbidden-elements item 7); (3) `item_orange_diag` reads as directional arrow (forbidden-elements item 7). All other 19/22 checklist items pass. Verdict REJECT.

## Notes
- L3 alternate-strategy enumeration (α through η) confirmed witness uniqueness post-fix.
- Issue 1 is structural (impossible avatar position); Issues 2, 3 are forbidden-elements pixel-pattern violations. All three fixable in a single revision pass.
- Transition back to write_spec for revision (visit count 1/10).

