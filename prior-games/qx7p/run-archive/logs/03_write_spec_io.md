# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02 pick_mechanic): qx7p / column-shift-row-align.
- skills/code/spec-template.md (9-section structure).
- skills/code/universal-scaffold.md (style rules, common patterns).
- skills/code/novaengine-api.md (sprite/level/camera/action API).
- skills/design-constraints/checklist.md (16-check authoring checklist).
- skills/design-constraints/composition-and-tutorial.md (3-level structure, +1/+2 rule).
- skills/design-constraints/difficulty-rules.md (per-level difficulty bullets).
- skills/design-constraints/core-knowledge-priors.md (allowed prior categories).
- skills/design-constraints/forbidden-elements.md (no symbols/letters/digits).
- skills/conventions/from-tech-report.md (12-question gate).
- skills/conventions/reference-game-patterns.md (recurring moves to inherit, anti-patterns to avoid).
- skills/mechanic-novelty/similarity-check.md and negative-similarity-check.md (re-run on full spec).
- prior-games/index.md (29 priors).
- 25 reference games' mechanism-details for distinguishing rules.

## Deliverables Produced
- mechanic-spec.md: full 9-section spec with 3 levels, witness solutions, per-level difficulty justification, novelty note + re-run negative-similarity check.

## Notes
- Mechanic chain: L1 = column-shift (M1, 1 mech). L2 = +bound-pair (M2, 2 mechs). L3 = +scan-line shift (M3, 3 mechs).
- L3 designed so M3 is provably necessary: bound-pair invariant `pos_a + pos_b ≡ 0 (mod 12)` is incompatible with the L3 target sum at the start scan-line offset; player MUST press ACTION5 to find a compatible offset.
- L3 has TWO bound pairs (ab + cd) on different "satisfiable offsets" so the witness must use the scan-line *cycle* to satisfy each pair at its own offset; one ACTION5 alone is insufficient.
- Visual identity: vertical band-stack columns with internal pixel structure (1-px side borders + 3-row colour bands × 12 segments × 6 wide). Bound pairs marked by orange ribbon at row 11 + orange dot endcaps; active column flanked by white highlight strips persistently for as long as it's active (per checklist item 19, no hidden state).
- Action subset = {1, 2, 6} for L1/L2; {1, 2, 5, 6} for L3. Minimal per checklist item 5.
- Step budgets: L1=40 (witness 17), L2=70 (witness 15), L3=100 (witness 23) — generous, never tight (per difficulty-rules § d).
- Sprite roster designed for visual richness: column bars have side borders + 12 distinct colour bands; target patches sit above each column for paired visual cue; scan line + carets at frame edges read as a measurement gauge (per checklist item 20-21).
