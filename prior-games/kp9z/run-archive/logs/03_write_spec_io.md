# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02): ID, family, novelty argument
- skills/code/spec-template.md: 9-section template
- skills/code/universal-scaffold.md: file structure rules
- skills/code/novaengine-api.md: Sprite/Level/Camera/HUD signatures
- skills/design-constraints/composition-and-tutorial.md: 3-level mechanic-inheritance rules
- skills/design-constraints/checklist.md: 20 checks (esp. items 11/12/18/20)
- skills/design-constraints/difficulty-rules.md: per-level difficulty justification
- skills/design-constraints/forbidden-elements.md: no glyphs/digits/cultural conventions

## Deliverables Produced
- workspace/mechanic-spec.md: full 9-section spec covering 3 levels with
  mechanic enumeration (L1=2, L2=3, L3=4), per-mechanic counterfactual
  necessity tables, witness solutions with explicit click coordinates,
  difficulty justifications (a/b/c/d) per level, sprite roster with 6×6
  cell sprites and pip layout, action mapping (ACTION6 only), HUD
  description, win/lose predicates, novelty cross-references.

## Notes
- Visual-detail floor (checklist item 20): 6×6 sprite at camera scale 2×
  yields 12×12 onscreen pixels per cell. Each pip = 1 sprite-pixel = 2×2
  onscreen pixels — survives 2×2 average pool. Sprite has internal
  semantic structure (corners=target, mid-edges=current, 2×2 center=type)
  carrying both type-meaning and count-meaning beyond colour.
- Click-only verb design: ACTION6 alone. The "freedom slot" ACTION5 is
  unused, but per action-enum.md this is fine for pure-click games (~6/25
  reference games use the pure-click pattern).
- Strict win condition (every cell at exact count, not just targets) was
  needed to make sink/redirector counterfactually necessary. Without
  strict win, a non-target cell could hold a stray grain and the level
  would still "win" — sink would be a no-op. Strict win forces every
  cascade-byproduct to be intentionally absorbed or routed.
- L3 planning depth: the heuristic-that-fails is "click each source 8
  times" (L2-style spam). Witness requires exactly 4 per source because
  L3 targets are unitary (count=1 each) and chain-delivered through the
  redirector — overshoot via 8-click-spam strict-fails the predicate.
- Determinism: cascades resolve in a fixed order via topological sweep
  (any topple-eligible cell, repeatedly, until no cell is over capacity).
  Per Abelian sandpile theorem the final state is path-independent. No
  randomness anywhere.
