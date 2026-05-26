# Implement summary — `pf3w`

## Files written

- `prior-games/pf3w/pf3w.py` — 534 lines.
- `prior-games/pf3w/metadata.json`.

## Plain-English mechanic summary

The player has two verbs: `ACTION6` clicks an inactive emitter slot to activate it, and `ACTION5` advances a global tick counter. Each activated emitter sends out a colored expanding outline that grows by one cell per tick, routing around obstacles. A target receiver lights up on the single tick when a same-colored expanding outline coincides with its cell. The level wins when every receiver lights up simultaneously on the same tick. Across the three levels, the player learns the place + tick verb, then learns to stagger emitter placements so multiple expansions converge on different receivers at the same moment, and finally must take wall-routing and color-matching into account to plan the right placement-and-timing combination.

## Smoke-test verification

The .py file parses as valid Python (`ast.parse` clean) and instantiates without error. Walking the witness solutions specified in `mechanic-spec.md` § 4:
- L1 witness (10 actions: ACTION6 + 9 × ACTION5) → next_level fires; level_idx = 1.
- L2 witness (11 actions: ACTION6, 2 × ACTION5, ACTION6, 7 × ACTION5) → level_idx = 2.
- L3 witness (24 actions: ACTION6@blue, 2 × ACTION5, ACTION6@magenta, 20 × ACTION5) → engine `_state = GameState.WIN`, `_win_score = 3` (all three levels cleared).

Total runtime witness: 45 actions across 3 levels, all successful.
