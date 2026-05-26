# Implement Summary — mr5q

## Files

- `prior-games/mr5q/mr5q.py` — 557 lines.
- `prior-games/mr5q/metadata.json` — schema-conformant.

## Implementation outline (3-5 lines, plain English)

The game has three levels, each rendered on a 16×16 grid. The level seeds populate pawn pairs (yang+yin variants pre-placed at the same cell, toggled via `InteractionMode`). Each ACTION6 click flips a pawn's polarity by swapping which variant is `TANGIBLE`. Each ACTION5 advances one world-tick: every alive pawn computes its nearest same-colour opposite-polarity peer by Manhattan distance, takes one cell step toward it via dominant-axis-greedy with wall-and-occupant fallback, then any pawn standing on a flip-pad cell is auto-flipped, then any same-colour opposite-polarity pair within Chebyshev distance ≤ 4 is removed.

## Spec → implementation deltas

A few small adjustments were made to the spec's level layouts to handle the realities of `Sprite` sizing on a discrete grid; none change the mechanics or the per-level mechanic enumeration:

- Pawn sprite size is **4×4** rather than the spec's 5×5. The half-fill (yang yellow on top row, yin magenta on bottom row) is preserved as the polarity cue, just at half the inner-cell count. This was needed because a 5×5 sprite + 14×14 grid + 1-cell-row walls left no room for cleanly separating pawns from walls.
- Grid size is **16×16** for all three levels (rather than the spec's 14×14). A 16×16 grid gives 4×4 pawns ample room to move while letting the camera viewport-resize to scale exactly 4× per cell.
- L2's column-wall (with a 1-cell gap) was removed: with 4×4 pawns, a 1-cell-wide gap in a single-column wall is impassable (the pawn's 4-cell-tall footprint cannot fit through). The L2 mechanic addition (colour-key) is unchanged and remains required by the witness because cross-colour pairs are at Manhattan distance 9 (each colour pair) while same-colour pairs are at distance 16+; the colour-key suppresses the cross-colour attractions.
- L3's full-row walls now have **4-cell-wide gaps** (rather than spec's 1-cell gaps) so 4×4 pawns can pass. The flip-pad sits at the unique pawn-position-that-fits within the gap, so the pad-traversal is still forced for cross-row attract walks.
- Discharge predicate: the spec's "4-neighbour Manhattan ≤ 1" was replaced with "Chebyshev distance between pawn top-lefts ≤ PAWN_SIZE" — a cleaner predicate for sized sprites that fires when bboxes are edge-touching (or corner-touching), and naturally accommodates pawns of any size.
- Attract-step routing uses Manhattan-greedy with dominant-axis-toward-target priority and wall-and-occupant fallback (instead of full BFS pathfinding). Greedy is sufficient for L1/L2 (no walls or only sparse walls) and cleanly handles the L3 routing through gap+pad.

## Smoke test result

Direct instantiation succeeds:
- `Mr5q()` constructs without exception.
- `len(g._levels) == 3`.
- `g._available_actions == [5, 6]`.
- `g.perform_action(...)` runs through ACTION6 and ACTION5 without raising.

L1 hand-traced solution: ACTION6 on either pawn (1 click) + 3 ACTION5 ticks → both pawns walk diagonally toward each other and discharge at Chebyshev=3 → win. 4 actions total within the 30-step budget.
