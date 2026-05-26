# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02 pick_mechanic): ID `wm6q`, family `edge-color-rotate-match`, novelty argument
- skills/code/spec-template.md: 9-section structure
- skills/design-constraints/{checklist, composition-and-tutorial, difficulty-rules, core-knowledge-priors, forbidden-elements}.md
- skills/global/{action-enum, color-legend}.md (palette + ACTION6 click conventions)
- skills/conventions/reference-game-patterns.md (HUD pattern, two-sprite-swap, multi-phase step, etc.)

## Deliverables Produced
- mechanic-spec.md: Full 9-section spec for `wm6q`. Layout: 16×16 tiles arranged in
  fixed grid positions (L1: 1×2, L2: 2×2, L3: 3×3). Single action: ACTION6 click.
  Mechanics: rotate-via-click (L1, +0), locked-tile (L2, +1), linked-pair (L3, +1).
  Per-level witness, base-assignment tables, and detailed counterfactual-necessity
  derivations included. Step budgets: L1=12, L2=25, L3=50.

## Notes
- Spent significant effort solving the L3 constraint system. Initial design failed
  the (1, 2).left ↔ (0, 2).right and the (0, 0)/(2, 2) joint-rotation constraints;
  iterated the base-colour assignments until a consistent witness exists with
  R_link = 2 (so the linked pair is genuinely required by the witness, not 0
  clicks).
- Witness lengths: L1 = 2, L2 = 5, L3 = 6. All fit comfortably under generous
  step budgets.
- Visual-discoverability cues: 6×6 black inner square = locked; 6×6 purple ring
  with off-white interior = linked-pair; otherwise off-white inner area = regular.
- Edge-band pixel layout: 3 px on each side, centre 10×10 holds the inner glyph.
- Non-locked clicks pass through to ONE tile's pixel array rebuild
  (`_paint_tile`); linked-pair clicks rebuild BOTH tiles' pixel arrays in
  lockstep.
