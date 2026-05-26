# implement-summary.md

## Files written
- `prior-games/tk6n/tk6n.py` (716 lines)
- `prior-games/tk6n/metadata.json`

## Summary of implemented rule

Avatar walks one cell per arrow press and carries a single thrown
projectile. ACTION5 launches the projectile in the avatar's facing
direction; the projectile travels outbound a level-data-fixed
number of cells, then returns by greedy-Manhattan-step toward the
avatar's current cell. The projectile lights any colored target it
overlaps along either leg. The catch occurs when the projectile and
the avatar coincide on a cell. Tall walls block the projectile;
short walls let it fly over. A guard sprite, present in the third
level only, walks a deterministic patrol and is frozen on contact
with the projectile.

## Smoke test verification
- `ast.parse` accepted the module (no SyntaxError).
- Instantiation of `Tk6n()` returned 3 levels.
- L1 witness (13 actions) advances avatar to L2.
- L2 witness (33 actions) advances to L3.
- L3 witness (70 actions) wins the environment.
- All three witnesses fit comfortably under their per-level
  step_budgets (30 / 60 / 100).
