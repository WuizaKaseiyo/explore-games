# `hl4n` — Implement Summary

## Files
- `prior-games/hl4n/hl4n.py` — 394 lines.
- `prior-games/hl4n/metadata.json`.

## Plain-English summary
Each level shows a grid of cells framed by clickable tint markers along the top and left edges. Clicking a marker cycles its tint and recolors the cells in its row or column according to a per-level combiner rule (row-only, column-overrides-row, or brighter-of-the-two). Several cells carry ringed targets in a required tint; the level wins when every ringed target's underlying cell displays its required color. A step-counter HUD bar drains per click; running out of steps loses the level.

## Verification
- `python -c "import ast; ast.parse(...)"` — syntax OK.
- `Hl4N()` instantiated successfully; 3 levels; sprite counts 75 / 85 / 87 (cells + markers + locks per spec).
- Drove the L1, L2, L3 witness sequences via `perform_action(...)`. Final state: `GameState.WIN`. Total actions used: 6 (L1) + 10 (L2) + 15 (L3) = 31 — exactly matches each level's planned witness length from the spec.
- `__pycache__` cleanup completed.
