# Step #05: write_spec (revision 1)

## Inputs Consumed
- workspace/critique-revisions.md (from #04 critique_spec): 6 issues, 4 substantive (1, 2, 3, 4) and 2 deferred (5, 6).
- workspace/mechanic-spec.md (pass 1): used as base, sections §1, §2, §4 L1, §5–§9 carried forward; §3, §4 L2 (a), §4 L3 rewritten.
- skills/design-constraints/{checklist,composition-and-tutorial,difficulty-rules}.md.
- skills/code/spec-template.md.

## Deliverables Produced
- workspace/mechanic-spec.md (rev 1): clean L3 design built around colour-locks (Issue 1 fix); drafting iterations purged from §4 (Issue 2 fix); L2 (a) random-resistance reframed without `5⁶` arithmetic (Issue 3 fix); §3 explicit layer ordering (Issue 4 fix); L3 trivial-heuristic + commute-test re-derived against the locks layout (Issue 6 fix).

## Notes
- L3 strict-necessity argument now rests on the convention "removing a mechanic = removing the gating logic but keeping the sprite". Under that convention, locks become permanent walls when their mechanic is removed, making targets at (1, 0) and (3, 0) unreachable. The argument is robust against the Issue 1 critique.
- L1 and L2 layouts unchanged. L3 layout is now {cube at (0, 0); targets (1, 0)=14 + (3, 0)=8 + (3, 1)=11; locks at (1, 0)=14 and (3, 0)=8}.
- Witness lengths: L1=2, L2=6, L3=6. Step budgets: L1=50, L2=80, L3=100. Budgets do not shrink.
