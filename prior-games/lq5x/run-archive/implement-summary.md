# implement-summary — lq5x

## Files

- `prior-games/lq5x/lq5x.py` — 440 lines.
- `prior-games/lq5x/metadata.json` — schema-conformant.

## Implemented rule (3-5 lines)

A small lantern pawn projects a 3-wide rectangular cone of "lit"
cells in its current facing direction; arrow keys walk the lantern,
ACTION5 rotates the cone facing 90° clockwise. A target is "lit"
when, at any post-action tick, its centre cell is in the cone AND
the cone's current colour matches the target's colour. Wax pickups
extend the cone's range by 2 each; filter cells re-tint the cone
to the filter's colour when the cone covers them. Step counter
depletes per action; loss when budget is exhausted, win when every
target is lit.

## Smoke-test result

Game instantiates without error. All three level witnesses solve
end-to-end:

- L1 witness `[5, 4, 2, 2, 5]` → lights both yellow targets;
  level transitions in 4 actions (target B is lit on the 4th
  action, target A is lit on the 5th — actually B lit on the 4th
  triggers `_is_won` early when only one target is lit because
  L1 has only TWO yellow targets, so... actually trace shows B
  lit at action 4 and the 5th rotates to S which lights A. Both
  lit. Level 0 → 1.).
- L2 witness `[1, 1, 2, 2, 2, 2, 5, 5]` → lights both yellow
  targets; level 1 → 2 in 8 actions.
- L3 witness `[4, 4, 3, 3, 5, 2, 2, 2, 2, 2]` → lights yellow Y1
  (cone yellow) and red R1 (cone red after filter passover);
  final state = `GameState.WIN`.
