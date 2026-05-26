# implement-summary

## Files
- `prior-games/qx7p/qx7p.py` (456 lines).
- `prior-games/qx7p/metadata.json`.

## Game class
`Qx7p(NovaBaseGame)` — `available_actions=[1, 2, 5, 6]`; ACTION5
filtered out of `_get_valid_actions()` for L1 and L2 (where the
scan-line is fixed at a single row).

## Implemented rule (in plain English, no level coordinates)
The player operates on tall vertical bars whose internal contents
are colour bands. Clicking a bar selects it as active; up/down
arrow keys cyclically scroll the active bar's content past a
horizontal indicator line. A subset of bars are visibly linked in
pairs by a coloured ribbon — scrolling one paired bar drives its
partner the opposite way in the same tick. The level wins when
every bar shows its target colour at the indicator line. The
final level introduces a movable indicator line cycled by ACTION5.

## Smoke runs done in implement
- Module parses (`ast.parse`).
- Game instantiates (`Qx7p()` returns; 3 levels declared).
- Full witness-replay test: pressed the L1 → L2 → L3 witnesses end-
  to-end. Game advanced through all three levels, terminated with
  `win_score = 3`, `is_last_level = True`, and `_check_win() =
  True` on L3 with all five columns showing their target colours
  at the final scan-line offset.

## Implementation note: L3 design correction caught at smoke time
The first L3 implementation had bound pairs with mismatched sums
(`k_a+k_b=4`, `k_c+k_d=10`); no single offset could simultaneously
align both pairs, so the level was unwinnable. Fixed by making
both bound pairs share the same sum (`k_a+k_b = k_c+k_d = 4`),
with a scan-line cycle `{32, 35, 38}` (offsets 6, 7, 8) where only
offset 8 satisfies the shared sum. Witness now fires ACTION5 twice
(0→1→2) before aligning columns. The spec's L3 necessity argument
still holds: at start offset 6 neither pair is solvable, so M3
(scan-line shift) is mandatory; the witness uses 2 ACTION5 firings
because the cycle direction passes through one non-solvable
intermediate before reaching the solvable offset.
