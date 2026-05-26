# implement-summary — gv47

## Files

- `prior-games/gv47/gv47.py` — 564 lines.
- `prior-games/gv47/metadata.json` —
  schema-conformant.

## Implemented rule (plain English)

Each level seats coloured "seed" sprites on a small wall-bound grid.
Clicking a seed expands its persistent connected region by one cardinal
ring of currently-uncoloured non-wall cells. ACTION5 fires a global
"mix" event that fuses any pair of contacting different-coloured
regions into a single new region, recolouring both into a derived
colour from a per-level mixing table. A level wins when every "target"
sprite's pip cell carries paint of the pip's colour; level 3 also has
a stationary wind-strip sprite that biases each grow ring to extend
one extra cell eastward.

## Smoke verification (run during implement)

- `python -c "import ast; ast.parse(...)"` → parses cleanly.
- `Gv47()` instantiates; `len(g._levels) == 3`.
- `set_level(0)`, `set_level(1)`, `set_level(2)` all run; cameras
  resize to (12, 12) per level.
- L1 click sequence at (14, 14) × 15 transitions to L2 (level 1) —
  the win predicate fires.
- L2 alternating-yellow/blue clicks followed by ACTION5 produces a
  unified green region whose painted set includes (6, 7) — the L2
  green target's pip cell.
- L3 single yellow grow expands the region by 17 cells (vs ~12
  without wind), confirming wind-bias is active.

`__pycache__` cleanup ran.
