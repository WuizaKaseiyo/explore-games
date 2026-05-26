# Step #04: critique_spec

## Inputs Consumed
- workspace/mechanic-spec.md (from #03)
- skills/design-constraints/checklist.md (items 1-20)
- skills/mechanic-novelty/similarity-check.md (re-run on full spec)
- skills/mechanic-novelty/negative-similarity-check.md
- skills/design-constraints/composition-and-tutorial.md
- skills/design-constraints/difficulty-rules.md
- skills/design-constraints/forbidden-elements.md
- skills/design-constraints/core-knowledge-priors.md

## Critique walkthrough — first pass

Items 1–19 + novelty: PASS. Item 20: FAIL on shape-as-meaning sub-rule (regular/source/sink cell types differ only by 2×2 type-center colour; without colour they are indistinguishable). Wrote critique-revisions.md with concrete fix (8×8 sprite with shape-distinct interiors).

Transitioning back to write_spec for revision.

## Deliverables Produced
- workspace/critique-revisions.md: 1 issue (item 20 shape-as-meaning) + concrete 8×8 sprite redesign suggestion + sub-cell pool re-derivation under grid_size=(40, 40).

## Notes
- Counterfactual table for items 11/12 is solid; preserve in the rewrite.
- Redirector exit-direction encoding via frame-edge orange notch (instead of inside-cell asymmetry) doubly-resolves a borderline item-7 concern: the directional cue moves out of the 2×2 center area (where it could be read as a tiny arrow glyph) into a positional break-in-the-frame, unambiguously not an arrow.
