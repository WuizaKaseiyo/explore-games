# Implement summary — xz5g

## Files written

- `prior-games/xz5g/xz5g.py` — 479 lines.
- `prior-games/xz5g/metadata.json`.

## Plain-English summary of the implemented rule

The player solves three rotation puzzles by clicking a pivot cell
and pressing space to rotate every "rotatable" sprite 90° around
it. L1 introduces pivot-set + rotate (avatar onto colour-matched
target ring). L2 adds a second orange pawn that must also reach
its own target — every rotation moves both pawns in lockstep, so
the player must find a pivot that delivers both at once. L3 adds
a green checkpoint pad the avatar must visit en route AND a
corner widget that toggles rotation direction CW/CCW; the
checkpoint is reachable only via CCW, so the player has to
discover the toggle before the level can advance.

## Smoke results from `implement` step 5 (runtime smoke)

- AST parse: OK.
- Instantiation: OK; `len(g._levels) == 3`; current_level grid_size
  == (64, 64).
- L1 witness `[ACTION6@(32, 32), ACTION5]` → score 1, advances to L2.
- L2 witness `[ACTION6@(32, 32), ACTION5, ACTION5]` → score 2,
  advances to L3.
- L3 witness `[ACTION6@(4, 4), ACTION6@(32, 32), ACTION5, ACTION5]`
  → score 3, state WIN.
- Per-level frame render: palette range OK (in [0, 15]) at every
  level; all sprites visible.

## Issue caught during implement

`__init__` originally re-initialised `_steps_left = 0` AFTER
`super().__init__()` which calls `set_level(0) → on_set_level`;
this clobbered the budget that on_set_level had just set. Fixed
by moving the field defaults to *before* super().__init__().
