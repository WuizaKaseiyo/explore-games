# Step #05: write_spec (revision 2)

## Inputs Consumed
- mechanic-spec.md (from #03): previous draft to revise.
- critique-revisions.md (from #04): 8 issues with concrete fixes.
- design-constraints/checklist.md, forbidden-elements.md, difficulty-rules.md, code/spec-template.md (from study).

## Deliverables Produced
- mechanic-spec.md (replaced): full 9-section spec with revision log.
  - §3 avatar redesigned to "octagon" (no letter likeness); stop_tile redesigned to 4-edge dots (topological "+", explicitly permitted by forbidden-elements).
  - §3 rotor adds direction-marker dot (palette 6 magenta); §6 RotorDirectionMarker overlay added — persistent visual cue for `_direction`.
  - §4 wedge rendering now 4-corner-dot + centre pattern per cell (textured, not flat fill).
  - §4 frozen visual cue: WedgeOverlay paints palette 7 (pink) instead of palette 11 (yellow) when freeze active.
  - §4 L3 rewritten cleanly: layout walls (3,1)(3,2)(3,4), stop-tile (2,3), switch (4,5), avatar (1,1), target (1,10); witness 15 actions traced cell-by-cell.
  - §4 budgets revised non-decreasing: L1=22 (witness 18, slack 4), L2=26 (witness 15, slack 11), L3=26 (witness 15, slack 11; budget < no-M3 alternate path of 27, forcing M3).
  - §4 L3 counterfactual enumerates alternates 1-3 and walks each to failure.

## Notes
- All 8 critique issues addressed concretely.
- L3 counterfactual path enumeration confirms: clockwise sweep with M2 = 27 actions; budget 26 < 27 forces M3.
- Palette set: {0, 3, 4, 5, 6, 7, 10, 11, 12, 14}. 10 values, no red/blue dominance.
- Witness L1=18, L2=15, L3=15 actions; budgets 22, 26, 26; non-decreasing across levels.
- Visual cues now persistent for all internal state mutated by player actions: rotor angle (notch position), direction (magenta dot), freeze (wedge tint colour).
