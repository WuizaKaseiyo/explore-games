# Step #05: write_spec (revision 1)

## Inputs Consumed
- critique-revisions.md (from #04): 6 issues; primary fix is M3 → stamp-toggle and clean L2 witness
- mechanic-spec.md (prior version, to revise)
- skills/code/spec-template.md, skills/design-constraints/* (re-confirmed)

## Deliverables Produced
- mechanic-spec.md (rev 1): all 9 sections; M3 simplified to stamp-toggle; layouts in lattice-grid form; concrete witnesses for L1 (2 actions), L2 (8 actions), L3 (10 actions).

## Notes
- L3 counterfactual for M3 is the trickiest; the witness includes one toggle-and-restamp pair at action 6 and the analysis claims (and intuitively confirms) that the alternative no-toggle path soft-locks the avatar. The strict checklist 12 case is somewhat dependent on layout reachability arguments.
- Spec is committed for critique pass 2.

