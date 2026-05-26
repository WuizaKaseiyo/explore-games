# Step #05: write_spec (revision round 1)

## Inputs Consumed
- workspace/critique-revisions.md (from #04)
- workspace/mechanic-spec.md (round-1 version, now overwritten)
- skills/code/spec-template.md (cached)
- skills/design-constraints/forbidden-elements.md (re-read for Issues 1, 2)
- skills/design-constraints/checklist.md (re-read for Issue 3)

## Deliverables Produced
- workspace/mechanic-spec.md — round-2 revision. Top-of-file `## Revision marks` summary; §3 and §4-Level-3 are the changed sections.

## Notes
- Issue 1 fix: `valve_closed` is now solid grey (palette 3), no X-pattern. Distinguishes from `valve_open` (green) by colour alone — same shape signals same-valve-correlated-states per checklist item 21 rule 2.
- Issue 2 fix: `pour_cursor` is now a 3×3 hollow yellow ring (no triangle, no direction). Position above the active vessel still cues "this is the focus".
- Issue 3 fix: L3 rebuilt with 4 vessels A, B, C, D, 3 valves, all initially closed. Targets 9, 9, 2, 9. Overflow cap on C at row 2. Witness 12 actions, budget 20. Buffer 8 = L1/L2 buffer (no shrink). Per-mechanic counterfactual table now enumerates all 8 plausible alternates; only 2 bypass M3 and both exceed the budget — M3 strictly necessary.
