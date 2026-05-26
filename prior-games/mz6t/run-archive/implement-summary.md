# Implement summary — `mz6t`

## Files written

- `prior-games/mz6t/mz6t.py` — 573 lines.
- `prior-games/mz6t/metadata.json` — schema-conformant.

## Implemented rule

A 5×5 grid of cells in three colour states (light-blue / orange / pink). ACTION6 click cycles the clicked cell's state by `+1 mod 3`; ACTION5 ticks the synchronous majority-vote propagation (each cell adopts whichever colour has `count ≥ 3` among its non-wall cardinal neighbours, otherwise keeps its current state). Walls are immutable cells that don't vote and aren't voted on (introduced at L2). Anchor cells freeze permanently the first time their state matches a per-cell target (introduced at L3). The win check fires only on ACTION5; the lose check fires when the per-level step budget exhausts.

## Verification

- `python -c "import ast; ast.parse(...)"` → SYNTAX OK.
- `Mz6t()` instantiates; `len(g._levels) == 3`.
- L1 witness `[click(14,14), tick]` → score 0 → 1 (advanced past L1).
- L2 witness `[click(22,6), click(6,22), click(38,22), click(22,38), tick]` → score 1 → 2.
- L3 witness `[click(22,22)×2, click(6,22), click(38,22), click(22,14), click(22,30), tick]` → state WIN, score 3.

All three spec witnesses replay deterministically and trigger the expected level transitions.
