# Step #05: write_spec (revision after critique #1)

## Inputs Consumed
- mechanic-spec.md (existing draft from #03)
- critique-revisions.md (issues #1, #2, #3 from #04)
- skills/code/spec-template.md (re-applied)
- skills/design-constraints/{checklist,difficulty-rules,
  composition-and-tutorial,forbidden-elements,core-knowledge-priors}.md
- skills/code/{universal-scaffold,novaengine-api}.md (re-applied)

## Work
- Issue #1 (L2 planning depth): repositioned blue stamp from
  (44, 24) to (24, 24) so its body collides with red's required
  pre-fold destination (cols 24..29 rows 20..25). Repositioned
  shadows so reflection arithmetic stays on the integer grid
  given 6×6 stamps and 4-px arrow steps (parity fix; shadows
  must sit at odd y when stamps are on the 4-px grid).
  Updated the witness, counterfactuals, and added an explicit
  "harder-first heuristic fails by collision" trivial-heuristic
  argument that's a genuine post-discovery failure (the player
  needs to OBSERVE the rejection, not just compute the
  collision in advance).
- Issue #2 (L3 planning depth): replaced the "use default
  H crease for both" discovery-stage heuristic with the
  "click any convenient crease cell to re-orient" heuristic.
  Recomputed L3 layout so the unique correct V-crease column
  is **col 33** — NOT a natural midpoint (col 32) or any
  other "convenient" cell. Walked through 4 plausible wrong
  click columns and demonstrated each one leaves the red
  shadow uncovered.
- Issue #3 (per-level data): added explicit per-level data
  dict listing in § 4 (step_budget, crease_movable,
  crease_orient, crease_pos, auto_select_stamp).

Verified arithmetic for all three witnesses end-to-end.
Witness lengths: L1=6, L2=16, L3=9. Step budgets: 30/50/60.

## Deliverables Produced
- mechanic-spec.md (rewritten clean): 9-section spec with
  fixed L2/L3 layouts and full arithmetic verification.

## Notes
- 6×6 stamps + 4-px arrow steps → reflected top-left y is
  always odd (because 2R − y_s − 5 is odd when R, y_s on
  4-px grid). All shadow y/x positions chosen to be odd
  to make reflection land exactly.
- Stamp y bound to [1, 58] to avoid the HUD row 0.
- No new mechanics introduced; the +1-or-+2 inheritance
  rule is preserved (L1=2, L2=3, L3=5).
