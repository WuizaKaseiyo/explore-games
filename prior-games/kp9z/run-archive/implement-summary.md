# Implement summary — kp9z

## Files written
- `prior-games/kp9z/kp9z.py` — 354 lines.
- `prior-games/kp9z/metadata.json` — schema-conformant.

## Verification
- `ast.parse` on the .py file: OK (no SyntaxError).
- Runtime instantiation of `Kp9z()`: OK; reports 3 levels and
  `available_actions=[6]`; `game_id="kp9z"`.

## What it implements
A small per-cell-counter puzzle on a 4x4 (L1) and 5x5 (L2/L3) grid where
each cell carries a non-negative integer. The player's only action is a
click on certain "input" cells, which adds 1 to that cell's count. When a
cell exceeds its capacity it redistributes its count to its 4 cardinal
neighbours, potentially triggering further redistributions in a
deterministic cascade. Two further cell types modulate the cascade: one
absorbs everything delivered to it, the other forwards a single delivered
unit in a fixed cardinal direction. The win predicate is strict: every
cell must end at exactly its declared target count, so over-shooting is a
real failure mode.
