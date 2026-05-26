# implement-summary

## Files written
- `prior-games/kx14/kx14.py` — 512 lines.
- `prior-games/kx14/metadata.json` — schema-conformant.

## Plain-English summary
The player controls a fluid surface in a vertical tank by raising or
lowering it; coloured balls float on the surface and slide horizontally
when a tilt is applied. Solid bars inside the tank constrain how the
surface and the balls can travel through certain columns. A click on a
ball pins it in place against both surface changes and tilts, enabling
arrangements that aren't possible by motion alone. Each level resolves
when every coloured ball sits in its same-coloured target ring.

## Verification

- **Syntactic parse:** `python -c "import ast; ast.parse(...)"` → SYNTAX OK.
- **Runtime smoke (instantiation):** `Kx14()` constructs without raising; level count = 3; action subset `[1, 2, 3, 4, 6]`.
- **L1 witness simulation:** 9-action sequence (4 ACTION1 + 5 ACTION4) completes L1 and transitions to L2 (`level_idx=1`).
- **L2 witness simulation:** 15-action sequence (3 ACTION1 + 2 ACTION4 + 3 ACTION1 + 7 ACTION4) completes L2 and transitions to L3 (`level_idx=2`).
- **L3 witness simulation:** 21-action sequence (anchor ACTION6 + 4 ACTION1 + 5 ACTION3 + anchor ACTION6 + unanchor ACTION6 + 2 ACTION2 + 5 ACTION4 + 2 ACTION1) completes L3 with `state=GameState.WIN`.
- All witnesses produce final ball positions that match the per-level target rings; colour-strict win predicate fires correctly.
