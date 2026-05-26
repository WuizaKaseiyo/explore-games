# implement-summary — `ej4t`

## Files

- `prior-games/ej4t/ej4t.py` — 296 lines
- `prior-games/ej4t/metadata.json` — schema-conformant

## Implementation summary

The game class `Ej4t` extends `NovaBaseGame` with `available_actions=[1, 2, 3, 4]` (cardinals only). On every directional action, the player either walks (if destination cell is empty), or attempts to push a chain of crates beginning at the target cell. The chain push only commits when every crate in the chain (after the first) sits within Manhattan distance R of the player at action-time; if any link is out of range, the entire push is rejected (atomic). Walking onto an extender pickup grows R by 1 and removes the pickup; walking onto a shrinker trap reduces R by 1 (one-shot, the trap stays visible as a grey "spent" cell). A `RingOverlayHud` paints a translucent halo around every cell within R of the player so the player can always see the current ring size; `StepCounterHud` paints a depleting bar on row 63. Win predicate: every target's (x, y) is occupied by a crate. Lose predicate: `_steps_used >= _max_steps`.

## Verifications

- AST parse: ✅ OK (no SyntaxError)
- Runtime instantiation: ✅ OK (`g = Ej4t()` — 3 levels, L1 grid (12,12) with 18 sprites)
- `available_actions = [1, 2, 3, 4]`
