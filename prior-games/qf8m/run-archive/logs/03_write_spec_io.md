# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02 pick_mechanic): family `rook-cross-toggle`, ID `qf8m`
- skills/code/spec-template.md: 9-section format
- skills/code/universal-scaffold.md: code structure constraints
- skills/code/novaengine-api.md: API surface
- skills/design-constraints/{checklist, composition-and-tutorial, difficulty-rules, core-knowledge-priors, forbidden-elements}.md
- skills/global/{action-enum, color-legend}.md
- skills/conventions/reference-game-patterns.md (recurring design moves to inherit)

## Deliverables Produced
- mechanic-spec.md: full 9-section spec; witness verified by hand-derivation
  in the appended Notes section. Levels: L1 = 1 mechanic (rook-flip);
  L2 = 2 mechanics (+ bishop-flip); L3 = 3 mechanics (+ tri-state cell at (2,2)).
  Witness lengths: 2 / 3 / 4 actions. Step budgets: 25 / 50 / 60.

## Notes
- Decision: kept grid_size constant at 5×5 across all 3 levels. This keeps
  the discoverability gradient about *new mechanics*, not *bigger grid* —
  satisfies §3.4's anti-pattern (single-mechanic-scale-up rejection).
- Decision: ACTION6-only `available_actions=[6]`. Slot 5 omitted because
  the distinctive verb is encoded into the click-target's CELL TYPE
  (rook/bishop/tri-state). Slot 7 omitted because re-clicking is its own
  undo for binary cells, and tri-state is forgiving via re-cycle.
- Decision: visual identity = internal motif (+ for rook, X for bishop,
  ring for tri-state) carried across both dark and lit sprite variants of
  each kind, so the player can always read off "what kind of cell is
  this" regardless of state. Per checklist 21 — sprite UI ≈ sprite role.
- Targets are derived by *running the witness on paper* and tabulating
  the XOR; the Notes appendix shows the full derivation tables for L1,
  L2, L3. Targets are reachable by construction.
- Counterfactual necessity: L2's bishop is forced by row-parity argument
  (target rows have mixed parity → unreachable by rook-only); L2's rook
  is forced by row-2 reach argument (3 same-row lit cells can't be
  cleanly produced by bishops in the budget). L3's tri-state is forced
  by the (2,2) target being state 2, which requires exactly 2 flips
  touching (2,2) — no other count produces state 2.
- Tri-state cell click semantics worked out: a tri-state cell is touched
  by clicks landing on rook OR bishop tiles whose flip-region includes
  (2,2) (i.e., the click is on a cell in row 2, col 2, main diagonal
  i-j=0, or anti-diagonal i+j=4). In L3 the tri-state cell IS clickable
  but the witness never clicks it directly (no need).
