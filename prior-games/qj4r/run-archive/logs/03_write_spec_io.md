# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02): ID qj4r, mechanic family fold-mirror-pair
- skills/code/spec-template.md, universal-scaffold.md, novaengine-api.md
- skills/design-constraints/{checklist,composition-and-tutorial,difficulty-rules,core-knowledge-priors,forbidden-elements}.md
- skills/global/{action-enum,color-legend,paths}.md

## Deliverables Produced
- workspace/mechanic-spec.md: 9-section spec; cell-size = 4 px; active region 8×8 logical centred in 64×64; L1 single fold; L2 adds obstacle-fold-rejection; L3 adds same-colour-merge.

## Notes
- During drafting, several geometric pitfalls surfaced around obstacle-reflection semantics; landed on "obstacles do NOT reflect with fold; they sit at fixed absolute cells and become inactive when their cell is in the retired half". This makes M2 well-defined.
- L2 M2-necessity is borderline — both 2-step orderings win in spirit, only one is M2-rejected. This may be flagged by critique_spec item 12 (no trivial fallback) and require either a tighter L2 setup or a re-framing of the necessity argument.
- L3 4-fold witness is sketched but not fully walked. Critique will need to verify or kick back for re-design.
