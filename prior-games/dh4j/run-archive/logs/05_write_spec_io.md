# Step #05: write_spec (visit 2, addressing critique-revisions v1)

## Inputs Consumed
- workspace/critique-revisions.md (8 issues)
- workspace/mechanic-spec.md v1 (the spec being revised)
- skills/code/spec-template.md
- skills/design-constraints/{checklist, composition-and-tutorial, difficulty-rules, forbidden-elements, core-knowledge-priors}.md
- skills/conventions/reference-game-patterns.md
- skills/global/{action-enum, color-legend, paths}.md

## Deliverables Produced
- mechanic-spec.md v2: 9-section spec with leap-over interpretation; L1 has 2 mechanics (M1 cell-pip-stride-leap, M2 goal-overlap-wins); L2 adds M3 filter-2↔3-swap; L3 adds M4 facing-pivot-stride-bonus-+1. Concrete witnesses for all 3 levels (L1=2, L2=7, L3=9 actions). Concrete coordinates for all walls, floor cells, filter, pivot, goal, avatar. HUD legend chip pixel layout specified. Abstract avatar (no face dots). Step budgets 30/50/80.

## Notes
- The critical change was switching from "wall-clamp slide" to "leap-over with destination-only block". This makes M1's variable stride uniquely necessary (because stride-1 cannot leap walls).
- Pivot redesigned to stride-bonus +1 (instead of direction-rotate). The bonus + filter combination forces L3's witness to require both M3 and M4.
- Wall thicknesses (1/2/3 rows) create a clean composition: each level requires one more "stride boost" than the last.
- L3 has two equal-length optimal witnesses (filter-first and pivot-first, both 9 actions). The planning challenge is realizing that pivot must be visited LAST before the leap.
- L1 witness is only 2 actions long but the budget is 30; per `composition-and-tutorial.md` L1 is intended to be solvable via mechanic-discovery within a few presses.
