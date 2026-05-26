# implement-summary — qf8m

## Files written

- `prior-games/qf8m/qf8m.py` — 545 lines.
- `prior-games/qf8m/metadata.json` —
  `game_id=qf8m`, baseline_actions=[6], generation timestamp
  `2026-05-08T17:29:34Z`.

## Verification

- `ast.parse` on the .py file: clean, no SyntaxError.
- Engine instantiation: succeeds; `len(g._levels) == 3` ✓.
- Witness for L1 (2 actions): produces exact target,
  `_check_win()` returns True after the 2nd click.
- Witness for L2 (3 actions): produces exact target;
  `_check_win()` True; centred-plus pattern matches the spec.
- Witness for L3 (4 actions): produces exact target; tri-state
  cell at (2, 2) ends in state 2; `_check_win()` True.

## Plain-English summary of the implemented rule

A 5×5 grid of square tiles is rendered alongside a smaller mirror
grid showing the target pattern. The player clicks a tile to drive
the grid into the target. The level introduces new cell kinds whose
internal motif tells the player how that cell's click propagates
state changes through the grid; clicks on a designated central cell
in the final level cycle through three colour states rather than
two.
