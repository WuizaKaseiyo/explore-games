# Step #03: write_spec

## Inputs Consumed
- states/write_spec.md
- skills/code/spec-template.md
- skills/code/universal-scaffold.md
- skills/design-constraints/* (already)
- workspace/mechanic-pick.md (from #02)

## Deliverables Produced
- workspace/mechanic-spec.md: full 9-section spec for `xv2b`. L1=1 mechanic (M1 valve-equalize). L2=+1 (M2 drain). L3=+1 (M3 pump). Witness solutions written out per level (18, 9, 29 actions). Step budgets 60/70/100. Action subset [5, 6]. Per-tick semantics defined explicitly with snapshot ordering.

## Notes
- Iterated several level designs in scratch (L2/L3 mass balance) before settling on numbers that satisfy strict counterfactual necessity for both M2 and M3. Key insight: M3 (pump) is only strictly required if a target level lies above the gravity-cap imposed by V_BC's slit height. Set slit-8 with target C=10 to force pump usage for the final 3 cells.
- L3 drain rule clarified to "consume only if vessel pre-transfer level > 0" so drain stops at A=0 and does not push A below target.
- Added an early-lose check ("if total water < min_target_total → lose immediately") to avoid the no-win-waiting-room anti-pattern flagged by difficulty-rules § 1.
