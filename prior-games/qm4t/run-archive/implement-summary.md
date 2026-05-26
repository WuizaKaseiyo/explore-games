# implement-summary.md

## Files written
- `prior-games/qm4t/qm4t.py` — 514 lines.
- `prior-games/qm4t/metadata.json` — game
  identity + baseline actions.

## What the implementation does
The player drops markers (vertex posts) on the playfield by clicking; the
engine renders the convex hull of all currently-placed markers as a fence
outline plus a faint inside-tint. Pressing the commit verb (ACTION5) consumes
every coloured creature whose centre lies strictly inside the fence, scoring
the matching-colour ones against per-level tally chips and racking up
strikes for the non-matching ones. Three strikes — or running out of step
budget — ends the run. Three levels escalate from a single-colour
free-shape tutorial through a multi-corner forbidden-creature decoy band
into a final layer where mobile patrollers cycle through the playfield, so
the player must time the commit to a phase when the patrollers are outside
the fence.

## Verification performed during this state
- `python -c "import ast; ast.parse(...)"` — PARSE OK.
- Runtime smoke (instantiation): `Qm4t()` constructed; 3 levels, 7/11/17
  initial sprites respectively; `available_actions = [5, 6]`.
- Per-level witness simulations (engine `perform_action` loop):
  - L1 witness `[(15,15), (50,15), (30,50)]` + `ACTION5` → 0 strikes,
    tally cleared, advance to L2.
  - L2 witness `[(12,15), (52,15), (32,55)]` + `ACTION5` → 0 strikes,
    tally cleared, advance to L3.
  - L3 witness `[(12,13), (54,13), (54,54), (12,54)]` + `ACTION5` →
    0 strikes, tally cleared, `_state = GameState.WIN`.
- Patroller cycle verified: phases 0..3 inside the centre cluster,
  phases 4..7 at the four playfield corners.
- `__pycache__` removed.

## Notes for `smoke_test`
- The L2 and L3 witness coordinates in `mechanic-spec.md` v3 were
  corrected during implement (the v3 spec had geometric mistakes — a
  quadrilateral whose right edge was at x ≈ 47, leaving yellow2 at
  x=47.5 just outside, and a left edge whose x at y=34 was ≈ 9, leaving
  maroon1 at x=10.5 inside). The corrected witnesses now match what
  the engine accepts.
