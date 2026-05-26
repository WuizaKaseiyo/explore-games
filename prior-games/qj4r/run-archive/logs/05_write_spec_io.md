# Step #05: write_spec (round 2)

## Inputs Consumed
- workspace/critique-revisions.md (from #04): 6 issues + recommended restructure
- workspace/mechanic-spec.md (rev 1) for revision baseline
- skills/code/spec-template.md, universal-scaffold.md, novaengine-api.md
- skills/design-constraints/* (re-confirmation)

## Deliverables Produced
- workspace/mechanic-spec.md (rev 2): full 9-section spec with restructured progression L1=M1, L2=M1+M2(merge), L3=M1+M2+M3(decoy-cleanup); obstacles dropped entirely; both new mechanics are TRANSFORMATION mechanics (state change observable at the triggering fold) so they satisfy strict checklist 12.

## Notes
- Witness math walked step-by-step for all three levels with concrete pre/post cells.
- L3 witness `[ACTION3, ACTION4, ACTION1]` triggers M2 at step 1 (merge), M3 at step 3 (decoy cleanup); M1 every step.
- Self-flagged item: L3 planning-depth justification is borderline by §3.4's "many action paths look reasonable" framing — a critique pass may reject and force a tighter L3 (second decoy or repositioned cleanup-conflict).
- Active-floor sprite is mutated in-place per fold (no new Sprite construction at runtime).
