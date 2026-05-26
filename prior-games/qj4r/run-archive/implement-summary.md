# Implementation summary — qj4r

## Files
- `prior-games/qj4r/qj4r.py` (435 lines)
- `prior-games/qj4r/metadata.json`

## Plain-English summary
The arrows fold the active rectangular sheet across its central horizontal or vertical axis: every coloured piece on the pressed-direction half is reflected to the mirror cell of the kept half, and the pressed half is permanently retired into padding (so the active region halves with each fold). Two pieces of the same colour that arrive at the same cell collapse into one merged piece. A neutral grey decoy piece is removed when any other piece arrives on its cell. The level is won when each colour's pieces sit on its same-coloured target rings (with per-colour piece-count = target-count) and no decoys remain.

## Smoke-test results
- Instantiation: OK (level count = 3).
- L1 witness `[ACTION3]`: WIN; advanced to L2.
- L2 witness `[ACTION3, ACTION4]`: WIN; advanced to L3.
- L3 witness `[ACTION3, ACTION4, ACTION1]`: WIN; final game state = `GameState.WIN`.

All three witness sequences succeed without engine errors.
