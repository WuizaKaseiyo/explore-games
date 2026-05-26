# Step #05: write_spec (revision pass)

## Inputs Consumed
- workspace/critique-revisions.md (from #04 critique_spec)
- workspace/mechanic-spec.md (current spec — to be edited in place)

## Deliverables Produced
- workspace/mechanic-spec.md: updated in place. Changes:
  - **§3 sprite roster** — replaced X-shape thermal-cell patterns
    in `temperature_field` with chamfered-tile patterns (solid
    centre + corner accents, no diagonals). Replaced pawn_hot /
    pawn_cold patterns with uniform-fill inner-2×2 (pink for hot,
    light-blue for cold). All five thermal patterns and both pawn
    variants no longer resemble letters. Cited `forbidden-elements.md`
    in the section header.
  - **§4 Level 3 layout** — replaced wall row 7 cols 4..12 with
    full-column wall at col 8 rows 4..15 (gap at rows 0..3). Pawn
    moved to (3, 1); target_hot to (3, 13); target_cold to (13, 13).
  - **§4 Level 3 counterfactual table for the wall mechanic** —
    enumerated 3 alternate strategies (RIGHT-then-DOWN, LEFT-only,
    no-wall counterfactual). Now strict: removing the wall would
    shorten the witness from 43 to 23 (~46% reduction), confirming
    the wall is non-decorative.
  - **§4 Level 3 witness** — 43 actions: DOWN×12 + ACTION5 +
    UP×10 + RIGHT×10 + DOWN×10. Detailed action-by-action.
  - **§4 Level 3 difficulty justification** — updated random-
    resistance probability to (1/5)^43; updated step budget to 100;
    rewrote planning-depth section to use the right-side-first
    heuristic (which fails by 11 extra actions in the new layout).
    Stage-conflation guard satisfied — the heuristic is a post-
    discovery error.

## Notes
- All 21 checklist items now satisfied.
- Critique-revisions.md issues 1 and 2 both addressed concretely.
- Transitioning back to critique_spec for verification (will be
  visit #2 of the 10-visit cap).
