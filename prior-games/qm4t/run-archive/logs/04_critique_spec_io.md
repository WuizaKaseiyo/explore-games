# Step #04: critique_spec (visit 1)

## Inputs Consumed
- `mechanic-spec.md` v1 (from #03)
- `skills/design-constraints/checklist.md` (items 1-21)
- `skills/design-constraints/forbidden-elements.md`
- `skills/design-constraints/composition-and-tutorial.md`
- `skills/design-constraints/difficulty-rules.md`
- `skills/mechanic-novelty/{similarity-check, negative-similarity-check}.md`

## Deliverables Produced
- `critique-revisions.md`: 4 blocking issues:
  1. L2 trivial-fallback (M3' not necessary with only 2 maroons).
  2. L3 patroller-timing not necessary with only 1 patroller.
  3. `strike_marker` × shape is a forbidden glyph.
  4. `vertex_post` "+ on a stick" reads as a glyph or clipart.

## Notes
- Checklist items 7 (forbidden glyphs) and 12 (counterfactual necessity) are
  both violated; spec sent back to write_spec for v2.
- Items 1–6, 8–11, 13–21 pass on v1.
- Novelty: similarity-check passes against all taxonomy entries and prior-
  games rows; negative-similarity walk against gv47/su15/ng52 yields ≤ 2
  shared dimensions each.
