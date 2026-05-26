# Step #04: critique_spec

## Inputs Consumed
- `workspace/mechanic-spec.md` (from #03 write_spec).
- `skills/design-constraints/checklist.md`: 18 items.
- `skills/design-constraints/composition-and-tutorial.md`: composition rules.
- `skills/design-constraints/difficulty-rules.md`: per-level difficulty bullets.
- `skills/design-constraints/forbidden-elements.md`: glyph/symbol bans.
- `skills/design-constraints/core-knowledge-priors.md`: 4 priors.
- `skills/mechanic-novelty/{similarity-check,negative-similarity-check}.md`.
- `skills/mechanism-details/{tu93,bp35,g50t,dc22,ls20,wa30,tr87,kx14,lq5x,vn8d,pj7k,gv47,pz4t}.md`: rerun near-miss comparisons.
- `prior-games/index.md`.

## Deliverables Produced
- `workspace/critique-pass.md`: All 18 checklist items pass; novelty NOVEL on positive + negative tests.

## Notes
- Caught issue during review: original spec had "chevron of palette 8" on the fragile tile, which could read as an arrow glyph (forbidden-elements item). Patched the spec to use a single 1×1 palette-8 cell at the top-left corner of the frame instead — geometric mark only.
- Defended item 6 (priors) on "intuitive-rules-of-physics" grounds: periodicity / clockwork rhythm is in the same family as gravity/momentum/bouncing/friction (all are rule-based temporal/spatial regularities humans intuit without instruction).
- Re-checked vs bp35's spike (newly considered): bp35's spike is unconditional touch-death; fz5j's fragile is conditional (locks only on residue mismatch; passes safely with computed residue). Distinguishing rule articulated.
- Negative-similarity recheck confirmed: closest prior tu93 shares at most 2 dimensions on the heavy axes (6/7/8 differ; 1/3/4/7 partial only).

