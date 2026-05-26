# Step #04: critique_spec (visit 1 of 10)

## Inputs Consumed
- mechanic-spec.md (from #03): full 9-section spec
- design-constraints/checklist.md (from study, re-grounded): 22 items
- design-constraints/forbidden-elements.md (from study): letters/digits/clipart/cultural rules
- design-constraints/difficulty-rules.md (from study): per-level budget/planning bullets
- mechanic-novelty/{similarity,negative-similarity}-check.md (from study): re-walked with full spec

## Deliverables Produced
- critique-revisions.md: 8 numbered issues with rule citations, offending sections, concrete fixes.

## Notes
- Items 1-6, 8-11, 13-18 PASS for the spec content (mostly).
- FAILED items:
  - Item 7 (forbidden elements): avatar chevron and stop-tile X-cross read as letter/symbol glyphs.
  - Item 12 / 19 (no hidden state, persistent visual cue): _direction (CW vs CCW) and _frozen_remaining lack persistent per-frame visual cues.
  - Item 20 (low-resolution): wedge tint = uniform palette 11 fill across ~35 cells; reads as coarse blocks per checklist 20.
  - Item 18.d / difficulty-rules § d (budget): L2 budget 22 < L1 budget 28 (shrinks). L3 budget 22 also less than L1 — counter to "later levels add discovery cost, more room not less" rule.
  - Spec readability: §4 Level 3 has 3 inline draft attempts, contradictory layout descriptions, internal "*Re-trace*" / "*hmm this routing failing*" markers — not a clean canonical witness.
  - Item 12 follow-up: L3 budget revision (#6 fix) must add walls to maintain M3-counterfactual under the larger budget.
- Transition back to write_spec (visit count 1 of cap 10).
