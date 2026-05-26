# tw94 — toroidal-wrap-playfield

## Summary

The grid is a torus: walking or pushing a crate off one edge re-enters from the opposite edge. Walls in the playfield can block direct delivery paths, forcing the player to deliver crates by routing them via the wrap-edge route. **L1** has only horizontal wrap (east-west); the vertical boundaries are hard walls. **L2** adds vertical wrap, making the playfield a full 2D torus. **L3** restricts wrap to even-numbered rows and columns: odd rows/cols become hard boundaries that don't wrap, so the player must reason about which row/col supports wrap-based delivery. Win when every target cell is covered by a crate.

## Action mapping

| Action | Semantic |
|---|---|
| ACTION1-4 | Walk player one cell in cardinal direction; if walking into a crate, push the crate one cell forward (push is the only verb) |

`available_actions = [1, 2, 3, 4]`. ACTION5/6/7 unused.

## Per-level mechanic progression

| Level | Mechanic | Specific challenge / witness |
|---|---|---|
| 1 | M1: horizontal wrap | 8×8, crate at (4,4) blocked from direct west by wall at (2,4); deliver to target at (1,4) by pushing east through the boundary wrap. Witness `[ACTION4 × 5]` (1 walk + 4 east-wrap pushes; the final push wraps from (7,4) to (0,4) and continues to (1,4)=target). |
| 2 | M2: vertical wrap added | 12×12, both axes wrap. Two crates: crate_a (10,4)→target(2,4) requires east-wrap (wall at (5,4) blocks direct west); crate_b (4,10)→target(4,2) requires south-wrap (wall at (4,5) blocks direct north). Witness: 13 walks + 4 east-wrap pushes for crate_a + 8 walks + 4 south-wrap pushes for crate_b. ~29 actions. |
| 3 | M3: row-parity wrap | 14×14, only EVEN rows wrap horizontally and only EVEN cols wrap vertically. crate_a on row 4 (even, wraps), crate_b on col 4 (even, wraps); both deliverable as in L2. Player learns by trial which rows/cols wrap (pip indicators only at even-row/col edges). Witness: similar to L2 but with 6-push counts (14-cell grid). ~33 actions. |

## Win condition

`{(t.x, t.y) for t in targets}.issubset({(c.x, c.y) for c in crates})`.

## Lose condition

`self._steps_used >= self._max_steps`. Per-level: L1=25, L2=80, L3=150.

## Internal state

- `self._steps_used: int`, `self._max_steps: int`
- Wrap rules computed from `_current_level_index` in `_wrap_enabled_h(y)` and `_wrap_enabled_v(x)` — no per-game state for wrap.

## Notable code patterns

- **Wrap-aware position arithmetic** (`_wrap_pos`): single helper computes the destination of a 1-cell move, applying wrap rules for the current axis at the current row/col. Returns `None` when wrap is disabled and the boundary is crossed (signaling movement blocked).
- **Per-level wrap rules in pure functions**: `_wrap_enabled_h(y)` and `_wrap_enabled_v(x)` return booleans based on `_current_level_index` and parity of y/x. No mutable state.
- **Atomic push with wrap**: `_attempt_move` computes the player's destination via `_wrap_pos`, then if a crate is at that cell, computes the crate's destination via the same `_wrap_pos`. Both must succeed for the push to commit. Wrap is symmetric: the same rule that lets the player walk through the boundary also lets the crate push through.
- **Pip indicators as visual cue** (item 19 no-hidden-state): 1×1 light-blue pip sprites at the edge cells of wrappable axes. At L1, pips at row-4 east-west edges only. At L2, pips at all edges (both axes wrap). At L3, pips only at even-row/col edges. Player learns which axes wrap by reading the pip layout.
- **NEW: trivial-heuristic gate** (CHECK_TRIVIAL_FAILS): trivial heuristic for L2 and L3 = `[ACTION4 × N]` ("press right always"). Verified that pressing right alone never delivers crate_b (which requires south-wrap, not east-wrap), so trivial fails. The contrast confirms L2/L3 require intentional axis-choice planning.
