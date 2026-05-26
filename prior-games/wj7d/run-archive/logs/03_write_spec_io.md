# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02): wj7d / fold-crease-overlay
- skills/code/spec-template.md (the 9-section spec template)
- skills/code/universal-scaffold.md (file structure + style rules)
- skills/code/novaengine-api.md (API cheatsheet)
- skills/design-constraints/composition-and-tutorial.md (level structure)
- skills/design-constraints/checklist.md (16-item gate)
- skills/design-constraints/difficulty-rules.md (per-level difficulty
  bullets a/b/c/d)
- skills/design-constraints/forbidden-elements.md
- skills/design-constraints/core-knowledge-priors.md
- skills/global/{action-enum,color-legend,paths}.md (palette + slot
  conventions)

## Deliverables Produced
- mechanic-spec.md: 9-section spec with full sprite roster, 3 levels
  with witness solutions and per-level mechanic enumeration, action
  mapping, HUD/state, win/lose, novelty note.

## Notes
- Decided 4-pixel arrow steps (compromise between native-64×64 grain
  and human-size action counts). Witness lengths: L1=6, L2=16, L3=9.
- Per-level mechanic counts: L1=2, L2=3, L3=5. Promotions: +1, +2.
- Strict counterfactual necessity argued per mechanic per level by
  naming the specific cell/sprite/rule that blocks each alternate path.
- Lose conditions handle both step exhaustion and unwinnable-state
  detection (no soft-lock wait-out).
- The state-machine for ACTION6 (stamp-select / crease-select /
  crease-reorient / deselect) is a touch complex; clear visual cues
  (halo on stamp; crease yellow when selected) keep it legible.
