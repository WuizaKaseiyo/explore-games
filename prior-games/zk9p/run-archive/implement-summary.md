# Implement summary — zk9p

## Files written
- `prior-games/zk9p/zk9p.py` (434 lines)
- `prior-games/zk9p/metadata.json`

## Summary
The game class `Zk9p` exposes a 1-cell-per-tick walking avatar in
levels of increasing grid size (14×14, 16×16, 18×18). After every
avatar action a set of autonomous pursuer sprites recomputes their
chase step from the avatar's new position, applies all moves
simultaneously, and any cell that ends with two or more pursuers on
it removes those pursuers from the level. The level resolves when
no pursuers remain, or terminates when a tangible pursuer occupies
the avatar's cell or the per-level step budget is exhausted.

## Verification
- `ast.parse(...)` — PASS.
- `Zk9p()` instantiates without exception; `len(g._levels) == 3`.
- For each level: camera viewport matches `level.grid_size` after
  `set_level()`, sprite roster present, all five declared actions
  run without exception.
- L1 witness check: 4 ACTION1 (UP) presses are sufficient to merge
  red and yellow at cell (7, 5) and advance to L2. (Spec predicted
  5 — actual minimum is 4 because Manhattan-major's tie-break on
  |dx|=|dy|=2 sends both pursuers to the column 1 step earlier than
  the spec's hand-trace assumed; the witness is shorter, not longer,
  and the difficulty justification still holds.)
