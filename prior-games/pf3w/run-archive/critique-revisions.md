# Critique revisions — pass 1

## Issue 1 (checklist item 20: visual detail floor — no info loss at 32×32)

**Section affected**: `mechanic-spec.md` § 3 Sprite roster, opening paragraph and per-sprite pixel matrices.

**Quote**: *"All sprites live in a 16×16 grid at camera scale 4 (each cell renders as a 4×4 px display block; sprites are drawn at cell-array granularity)."*

**Problem**: At `grid_size=(16, 16)` with camera scale 4, each grid-cell entry in a sprite's pixel array renders as a 4×4 px solid color block on display. There is no way to encode pixel-level variation WITHIN a single grid cell, because the sprite array's resolution equals the grid resolution. Downsampling 64×64 → 32×32 (2×2 average pool): each 4×4 single-color block averages to a 2×2 single-color block of the same color. The block-level pattern (which grid cells are colored) survives intact at 32×32. The 25 reference games avoid this by using `grid_size=(64, 64)` with logical cells = 4 (or 6 — see `sk48`'s `udenqlsrfq=6`) pixels, and designing sprites with internal pixel-level patterns INSIDE each logical cell (e.g., a 4×4 logical-cell block rendered as a colored frame around a -1 transparent center, like sk48's `qtjqovumxf`).

The wavefront sprite is the worst offender — at 16×16 grid, each frontier cell is a single 4×4 px solid block, indistinguishable from its grid-cell neighbours under 2:1 downsampling.

**Fix**: 
1. Change `grid_size = (64, 64)` for all 3 levels (matches the engine default; no `camera.width`/`height` resize needed).
2. Define `LOGICAL_CELL_SIZE = 4` as a module constant. All grid coordinates in the spec are LOGICAL-cell coords (i.e., 16 logical cells × 16 logical cells); multiply by `LOGICAL_CELL_SIZE = 4` to get pixel coords for sprite placement, BFS expansion, and click-target detection.
3. Redesign sprites at PIXEL-array level with sub-cell internal pattern per logical cell:
   - **Emitter slot dim** (3 logical cells × 3 logical cells = 12×12 pixel matrix): outer 8 pixels of each logical cell painted palette 3 grey, inner 4 pixels painted palette 4 dark-grey (frame-around-darker-centre per logical cell). The hollow center of the 3×3 logical-cell arrangement (the middle logical cell) is fully -1 transparent.
   - **Emitter slot lit blue/magenta** (12×12): each logical cell of the "+" cross has outer-frame pixels colored ring, inner-2×2 colored center. The middle logical cell has all 16 pixels colored (the active center).
   - **Target unlit** (12×12): each logical cell of the ring has frame palette `<color>`, inner -1 transparent. Middle logical cell fully -1 transparent.
   - **Target lit** (12×12): same ring frame, BUT middle logical cell has 4×4 = 16 pixels filled palette 11 yellow.
   - **Wall unit** (4×4 pixel matrix per logical cell): a single logical wall cell is rendered as `[[3,4,4,3],[4,3,3,4],[4,3,3,4],[3,4,4,3]]` — a 4×4 checker that loses the alternation under 2:1 downsampling.
   - **Wavefront sprite** (64×64 pixel matrix): for each logical-cell coord (lcx, lcy) in the current frontier, paint the 4×4-pixel block at pixels (4*lcx..4*lcx+3, 4*lcy..4*lcy+3) with a "ring" pattern: outer 12 pixels of the 4×4 block colored, inner 2×2 pixels -1 transparent. Cells off the frontier: all 16 pixels -1 transparent. The ring-within-cell pattern at the wavefront is visually a "halo" trail of cells, and the sub-pixel-cell ring loses its inner-cell detail under 2:1 downsampling (the 2×2 inner becomes 1×1, the outer 4 pixels become 2 — the ring shape collapses).

This redesign makes every gameplay-relevant sprite visibly damage when the 64×64 frame is averaged to 32×32, satisfying item 20.

**Other downstream changes from this fix**:
- BFS computation operates on logical-cell coords (16×16 logical grid).
- ACTION6 click coordinates are converted to logical-cell coords by `display_to_grid` (which returns pixel coords on a 64×64 grid) followed by integer-divide by 4 to reach logical-cell coord. Click hit-detection uses logical-cell match against slot positions.
- Sprite positions in `Level(...)` are pixel coords (multiples of 4): `slot_blue.set_position(3*4, 8*4) = (12, 32)`.

No other checklist items are affected — items 1-18 still pass after the redesign. The novelty argument is unchanged (mechanic structure is identical; only visual rendering granularity changes).

## Summary

One issue, fixable with a representational change (grid_size 16×16 → 64×64 with 4-px logical cells, sprites redesigned at pixel-array level with internal sub-cell pattern). Transition back to `write_spec` for the revision.
