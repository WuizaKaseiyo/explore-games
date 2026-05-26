# Step #05: implement

## Inputs Consumed
- mechanic-spec.md (from #03; layouts, witness, win/lose, HUD)
- critique-pass.md (from #04; confirms spec is implementation-ready)
- skills/code/universal-scaffold.md (file structure + style rules)
- skills/code/novaengine-api.md (API signatures)
- skills/code/id-generation.md (Pascal class naming)
- skills/global/color-legend.md
- skills/global/action-enum.md

## Deliverables Produced
- prior-games/zd7m/zd7m.py (413 lines): full game implementation.
- prior-games/zd7m/metadata.json: schema-conformant metadata.
- implement-summary.md: file paths + LOC + plain-English summary.

## Notes
- During smoke-test of L1, found bug: `next_level()` without `complete_action()`
  caused engine to re-process the action on the new level. Fixed by always
  calling complete_action before next_level (matches cn04 pattern).
- L1, L2, L3 witnesses verified end-to-end: L1→L2 (DOWN×10), L2→L3 (RIGHT×10+DOWN×4),
  L3→WIN (RIGHT×10+DOWN×4 with portal teleport). Final state GameState.WIN.
- Cohort-step processes pawns in (y, x) row-then-column order; each pawn moves
  iff its destination is free of anchors, other pawns, and grid edges.
- Portal teleport runs as a 6-frame internal animation (not visible to action
  consumer); on completion, pawn position is set to portal_b's cell.
