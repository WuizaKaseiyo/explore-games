# Step #05: write_spec (revision after critique #1)

## Inputs Consumed
- workspace/critique-revisions.md (visit #1): two issues — (1) L3 BURST not exercised; (2) anti-anchor described as "X".
- workspace/mechanic-spec.md (prior draft): the doc being revised.

## Deliverables Produced
- workspace/mechanic-spec.md (in-place edits): M6 dropped, `available_actions` reduced to `[6]`, anti-anchor description rewritten ("corner-dot frame with inner block"), L3 mechanic count adjusted from 7 to 6 (+1 promotion), reserved pawn_green/target_green removed, L3 §Necessity rewritten to drop M6 paragraph and add stronger M7 justification, planning-depth witness-pair commute test rewritten for action 7 ↔ 8 swap, step-budget calibration note added, ACTION5 references removed from §5 and §6.

## Notes
- Revision marker added at the top of §2 explaining the change for traceability.
- After this revision, kn58 is a pure-click game (`available_actions = [6]`) — distinguishing it from the BURST-using sketch. Click-only puts it in the same family as ft09, lp85, vc33, sb26, sc25, su15, r11l (5/25 pure-click; 7/25 click-and-undo) — well-attested.
- Witness sequences unchanged: L1=8 actions, L2=21 actions, L3=12 actions.
- Will re-enter critique_spec for visit #2.
