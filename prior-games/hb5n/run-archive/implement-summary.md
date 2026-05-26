# hb5n — implement summary

## Files

- `prior-games/hb5n/hb5n.py` — 471 lines.
- `prior-games/hb5n/metadata.json` — game metadata.

## Implementation summary

The avatar is rendered as a list of per-cell sprites (one anchor
sprite with an orange-centred pattern, plus one body sprite per
remaining body cell with a maroon-centred pattern). Each cell is
4 display pixels, placed on a 16×16 logical grid (grid_size
matches the 64×64 pixel frame). Geometry helpers
`_rotate_cw(rel, k)` and `_absolute_cells_for(anchor, rotation,
relative_cells)` reconstruct the avatar's footprint from a
canonical rotation-0 list of relative offsets.

Action handling: ACTION1..4 translate the anchor with collision
check against outer-boundary cells and any wall-tagged sprite at
the target cell positions; ACTION5 rotates the polyomino 90° CW
about the anchor using the same collision check applied to the
post-rotation cell set. On every action the step counter
decrements one tick. After the action lands the anchor on a
pickup or pivot-reset cell, the cell is consumed: pickup-
consumption appends a new body cell at relative offset (-1, -1)
in the rotation-0 frame and spawns a body sprite at its current
absolute position; pivot-reset re-baselines the relative-cells
list around a different body cell and swaps the two affected
sprites (replacing them with freshly-patterned clones so the
orange-centre marker migrates to the new anchor cell, and resets
rotation to 0). Win predicate is set-equality between the
avatar's current absolute cell set and the per-level target cell
set (collected from `target`-tagged sprites in `on_set_level`).

The runtime smoke test exercises the L1, L2, and L3 witnesses in
sequence: each level advances to the next on win, and the final
state is `GameState.WIN` with score 3. Edge cases verified: wall
collisions reject moves (step counter still ticks), and step
budget exhaustion fires `lose()` → `GameState.GAME_OVER`.
