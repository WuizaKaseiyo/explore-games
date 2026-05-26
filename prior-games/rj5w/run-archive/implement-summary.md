# Implement summary — `rj5w`

## Files written
- `prior-games/rj5w/rj5w.py` — 443 lines.
- `prior-games/rj5w/metadata.json` — standard schema.

## Plain-English mechanic recap (no cell-level coordinates)
The player slides a thin fold-line cursor across a paper-coloured
sheet and presses commit to **reflect every (unlocked) pawn across
the line**. A pawn that moves onto its colour-matched target
becomes locked and is not affected by subsequent folds. The level
is won when every pawn coincides with its same-colour target. L1
exposes a single fold direction; L2 introduces a perpendicular
fold-line and a click-to-toggle which axis is active; L3 adds the
lock-on-target behaviour and requires the player to fold along
the same axis twice in a row to undo a partial move while a
locked pawn stays in place.

## Smoke test
- `ast.parse` succeeds (valid Python 3 syntax).
- Instantiation succeeds; engine reports level count = 3.
- All three witness solutions ran end-to-end via
  `perform_action(...)`:
  - L1 (3 actions: `[ACTION3, ACTION3, ACTION5]`) wins and advances
    to L2.
  - L2 (7 actions: `[ACTION4, ACTION4, ACTION5, ACTION6@(20, 30),
    ACTION2, ACTION2, ACTION5]`) wins and advances to L3.
  - L3 (12 actions: `[ACTION4×4, ACTION5, ACTION5,
    ACTION6@(20, 28), ACTION2×4, ACTION5]`) wins → final
    `GameState.WIN`.
- After L3 the lock count was 3 (green, yellow, purple, all
  locked on their targets).
- Two implementation bugs caught and fixed during the smoke test:
  1. `__init__` was overwriting `self.step_budget` to 0 *after*
     `super().__init__` (which had already run `on_set_level`).
     Fixed by setting per-level state attributes before
     `super().__init__`.
  2. `step()` was decrementing the step budget on the engine's
     internal `RESET` action. Fixed by short-circuiting `step()`
     for `GameAction.RESET`.
- `__pycache__` cleaned after the runtime test.
