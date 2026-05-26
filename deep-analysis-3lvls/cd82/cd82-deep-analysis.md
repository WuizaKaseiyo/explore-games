# cd82 — deep analysis

> **3-LEVELS-ONLY NOTE.** This analysis was authored against the
> original full reference games (6+ levels each). Our generated
> games target only **L1, L2, L3** — so any content below that
> describes "level 4+", "L4+", "L5+", sprite rows annotated
> "(level 4+ only)" / "(level 5+ only)", action-handler branches
> for late levels, or internal-state flags gating late-level
> behaviour describe content NOT present in the truncated 3-level
> versions used by the harness. Read the L1/L2/L3 sections as
> primary; treat L4+ references as historical context only.


## Source meta
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/cd82/fb555c5d/cd82.py`
- Lines: 781
- Class name: `Cd82`
- available_actions: `[1, 2, 3, 4, 5, 6]` (UP/DOWN/LEFT/RIGHT cycle the tank around the orbit, ACTION5 fires the basket, ACTION6 clicks)
- Number of levels in source: 6
- Number of levels documented in this analysis: 3
- Imports: `ActionInput`, `NovaBaseGame`, `Camera`, `GameAction`, `Level`, `RenderableUserDisplay`, `Sprite` from `novaengine`; `numpy as np`; `cast` from `typing`.

## Mechanic essence

A small 10×10 canvas sits in the middle of the screen and a paint-tank rides on an 8-slot ring that orbits the canvas's perimeter — four axial slots at the mid-edges and four diagonal slots at the corners. Pressing the four arrow keys nudges the tank one slot at a time around the ring (treating the eight slots as the eight non-centre cells of a 3×3 compass). The player can click one of the coloured swatches lined up at the top of the screen to pick up that dye (a small underline indicator slides under the chosen swatch); when the tank fires, it charges inward toward the canvas and on contact splashes either one straight half of the canvas (if it was on an axial slot — top, bottom, left or right half) or one triangular wedge (if it was on a diagonal slot — a corner-cornered triangle), painting those cells in the picked-up colour.

Two firing routes coexist. Pressing the FIRE key (ACTION5) launches the basket itself — a sliced rectangle for axial slots, a hollow diamond for diagonal slots — straight at the canvas. From level 3 onward an additional arrow-tank avatar appears at the four axial slots; clicking that arrow-tank with ACTION6 fires a smaller sub-stripe of paint along its edge of the canvas. The level is won when the canvas's painted pattern — ignoring the cells lying on the canvas's two diagonals — matches the per-level target image displayed on the gallery shelf to the right.

## Sprite roster

| sprite (obfuscated) | dims | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| `ctwspzkygu` | 6x5 | 0, 2, 15, -1 | (default) | 2 | YES | (default) | YES | arrow-tank avatar — appears at the 4 axial orbit slots (level 3+); clickable to fire a sub-paint-stripe |
| `eoqnvkspoa-pqwme1-1` | 10x10 | 0, 15 | (default) | (default) | YES | (default) | YES | L1 target — horizontal split, palette-0 top half + palette-15 bottom half |
| `eoqnvkspoa-pqwme2-1` | 10x10 | 0, 12, 15 | (default) | (default) | YES | (default) | YES | L2 target — anti-diagonal triangle split with palette-12 lower wedge + palette-15 upper wedge + palette-0 small corner |
| `eoqnvkspoa-pqwme3-1` | 10x10 | 8, 12, 14, 15 | (default) | (default) | YES | (default) | YES | L3 target — multi-quadrant pattern combining 4 colours |
| `eoqnvkspoa-pqwme4-1` | 10x10 | 9, 11, 12, 15 | (default) | (default) | YES | (default) | YES | L4 target (out of scope) |
| `eoqnvkspoa-pqwme5-1` | 10x10 | 8, 9, 12, 14 | (default) | (default) | YES | (default) | YES | L5 target (out of scope) |
| `eoqnvkspoa-pqwme6-1` | 10x10 | 0, 8, 11, 14, 15 | (default) | (default) | YES | (default) | YES | L6 target (out of scope) |
| `gkyfnkvrty` | 64x18 | 3, 4, -1 | (default) | -1 | YES | (default) | YES | gallery-shelf UI frame — palette-3 background panel with palette-4 borders that frames the target preview to the right of the canvas |
| `oaoosfneq-laopvne` | 17x17 | 2, 15, -1 | (default) | 2 | YES | (default) | YES | diagonal basket — hollow palette-15 diamond with palette-2 outline; used at the 4 diagonal orbit slots (1, 3, 5, 7) |
| `oaoosfneq-oaanwen` | 14x9 | 2, 15 | (default) | (default) | YES | (default) | YES | horizontal basket — palette-15 rectangle with palette-2 outline; used at the 4 axial orbit slots (0, 2, 4, 6) |
| `pqkenviek` | 5x5 | 0, 4 | (default) | (default) | YES | (default) | YES | colour swatch — palette-4 hollow square with palette-0 (or recoloured) interior; the player clicks one to pick up its dye colour |
| `xytrjjbyib` | 10x10 | 0 | (default) | (default) | YES | (default) | YES | central canvas — initially solid palette-0; cells get recoloured by basket and arrow-tank fires |
| `ydiwkzjkgl` | 5x1 | 0 | (default) | (default) | YES | (default) | YES | swatch underline — a single 5-pixel-wide bar that slides under the currently-selected swatch as a "you picked this colour" indicator |

### `ctwspzkygu` — arrow-tank avatar (level 3+)
- Pixel pattern: 6 cols × 5 rows. Row 0-2 form the body — palette-2 sides (cols 0 and 5) with a palette-15 fill (cols 1-4). Row 3 has the front-face: `[2, 2, 0, 0, 2, 2]` — two palette-0 "eyes" between palette-2 cheeks. Row 4 has the wheel-base: `[-1, 2, 2, 2, 2, -1]` — four palette-2 cells flanked by transparent. Reads as a small palette-15 cabin with two black eyes and a wheelbase, encased in palette-2 trim.
- Where it appears: L3 (1 copy at (29, 18) rotated 180°). Same in L4-6 (out of scope).
- Role: at axial orbit slots (0, 2, 4, 6) only. The `eanmnpxtyi` helper repositions the tank to face the canvas based on which axial slot the basket is in. Clicking the tank via ACTION6 calls `qbiojckwxl` → `gfjfyvajah` → animation in `jgclfnjrnk` that drives the tank inward to the canvas, paints a 3-wide × 4-tall sub-stripe on the corresponding edge via `coublenfir`, then retracts.
- Visual-vs-functional read:
  - At-rendered-scale shape: small filled cabin-with-wheels glyph; rotates 90/180/270 to face the four axial directions.
  - Palette signature: 0, 2, 15. Palette 15 shared with both basket sprites (`oaoosfneq-*`) and most target sprites; palette 2 shared with the basket outlines.
  - Nearest-other-sprite check: visually distinct from baskets (which are flat rectangles or diamonds without any "eyes" detail). The two black-eye dots and the wheelbase make the tank readable as a vehicle.
- Visual contrast notes: against the palette-5 background, the palette-15 body and palette-2 sides read crisply; the eye-and-wheel detail makes the tank more "object-like" than the baskets.

### `eoqnvkspoa-pqwme1-1` — L1 target (horizontal halves)
- Pixel pattern: 10×10. Top 5 rows palette-0 (black), bottom 5 rows palette-15 (white). Reads as a horizontal split.
- Where it appears: L1 only (1 copy at (3, 3)).
- Role: target image. The win predicate `wvrremwltt` compares the canvas (`xytrjjbyib`) cell-by-cell against this target, ignoring the cells lying on either of the canvas's two diagonals (the X-cross mask in `poqpfcjieu`). When all non-X cells match, `next_level()`.
- Visual-vs-functional read:
  - At-rendered-scale shape: 10×10 filled square with a horizontal palette-0 / palette-15 split.
  - Palette signature: 0, 15. Palette 0 shared with canvas's initial state; palette 15 shared with basket fill.
  - Nearest-other-sprite check: the canvas itself starts as the same palette-0 fill; only the "stripe of palette-15 on the bottom half" distinguishes the L1 target visually.
- Visual contrast notes: rendered inside the gallery-shelf panel (`gkyfnkvrty`) on the right-side strip; visually obvious which half is which.

### `eoqnvkspoa-pqwme2-1` — L2 target (diagonal triangle split)
- Pixel pattern: 10×10. Anti-diagonal split — upper-right palette-15 wedge + lower-left palette-12 wedge + a small palette-0 corner triangle at the lower-left edge.
- Where it appears: L2 only (1 copy at (3, 3)).
- Role: target image for L2.
- Visual-vs-functional read:
  - At-rendered-scale shape: triangular split with a stepped diagonal boundary.
  - Palette signature: 0, 12, 15.
  - Nearest-other-sprite check: distinguishable from L1's straight horizontal split by the diagonal boundary.

### `eoqnvkspoa-pqwme3-1` — L3 target (multi-quadrant)
- Pixel pattern: 10×10. Top-left palette-15, top-middle palette-12 stripe, central palette-15, top-right transitions to palette-14 in a sloped band, bottom-right palette-14 with a palette-8 staircase along the lower-left.
- Where it appears: L3 only (1 copy at (3, 3)).
- Role: target image for L3.
- Visual-vs-functional read:
  - At-rendered-scale shape: complex four-region pattern with stepped diagonals.
  - Palette signature: 8, 12, 14, 15.
  - Nearest-other-sprite check: visually denser than L1/L2 — more colours, more boundary segments.

### `eoqnvkspoa-pqwme4-1` — L4 target (out of scope)
- Pixel pattern: 10×10 with palettes 9, 11, 12, 15.
- Where it appears: L4 only.
- Role: out of scope.

### `eoqnvkspoa-pqwme5-1` — L5 target (out of scope)
- Pixel pattern: 10×10 with palettes 8, 9, 12, 14.
- Where it appears: L5 only.

### `eoqnvkspoa-pqwme6-1` — L6 target (out of scope)
- Pixel pattern: 10×10 with palettes 0, 8, 11, 14, 15.
- Where it appears: L6 only.

### `gkyfnkvrty` — gallery-shelf UI frame
- Pixel pattern: 64×18. Mostly palette-3 (grey) with a palette-4 (off-grey) inset along the top — a vertical column of palette-4 at columns 16-17 from rows 0-15, plus a thick palette-3 region to its right (cols 18-63, rows 0-9), plus another palette-3 region in the bottom-left (rows 16-17, cols 0-17). Reads as a layered shelf-and-frame UI.
- Where it appears: every L1-3 level (1 copy at default position). L4-6 use it too (same).
- Role: cosmetic UI frame. Sits behind the target image (`eoqnvkspoa-*`) on the right side of the screen, providing the "gallery shelf" visual context. The target image renders on top of this frame at (3, 3).
- Visual-vs-functional read:
  - At-rendered-scale shape: large flat panel with horizontal stripes and vertical accent.
  - Palette signature: 3, 4. Palette 3 also matches `PADDING_COLOR = 4`... actually wait, `PADDING_COLOR = 4` and the frame uses palette-3 + palette-4. Palette 3 is unique to this frame; palette 4 is shared with the colour-swatch outline.
  - Nearest-other-sprite check: distinct large UI panel; nothing else has 64×18 dimensions.
- Visual contrast notes: against the palette-5 background, the palette-3 panel reads as a dimmer slab.

### `oaoosfneq-laopvne` — diagonal basket
- Pixel pattern: 17×17 hollow palette-2 outline forming a diamond, with palette-15 interior fill. The shape is a tilted square — diagonal lines of palette-2 connecting the top point to the right point to the bottom point to the left point, with palette-15 cells inside the diamond.
- Where it appears: dynamically spawned by `elltphoitr` at every level when the orbit slot is one of the diagonal slots (1, 3, 5, 7). Initial level position is in `nicoqsvlg` per slot. Layer 2.
- Role: the basket variant for diagonal orbit slots. Recoloured at spawn time via `color_remap(15, knqmgavuh)` so its interior fill matches the currently-selected dye colour. When ACTION5 fires, the basket animates in `hhjooisvrs` — moves 7 cells in the slot's direction (`dx, dy` from `nicoqsvlg`), then back. At the apex of the inward motion (frame 7), `rtjwayrycq` paints the canvas's diagonal triangle in the dye colour.
- Visual-vs-functional read:
  - At-rendered-scale shape: hollow diamond / rotated square.
  - Palette signature: 2, 15 (recoloured).
  - Nearest-other-sprite check: the horizontal basket `oaoosfneq-oaanwen` is a flat axis-aligned rectangle. Diamond vs rectangle is the visual distinction.
- Visual contrast notes: the recoloured fill makes the basket's identity obvious — it always shows the currently-loaded dye colour.

### `oaoosfneq-oaanwen` — horizontal basket
- Pixel pattern: 14 cols × 9 rows. Outermost ring of palette-2; interior 12×7 palette-15 fill. The bottom row (row 8) is solid palette-2 (the "lid" or open mouth). Reads as a flat rectangular tray.
- Where it appears: dynamically spawned by `elltphoitr` when the orbit slot is one of the axial slots (0, 2, 4, 6). Rotated to face the canvas (180° at top, 270° at right, 0° at bottom, 90° at left). Recoloured per active dye.
- Role: the basket variant for axial orbit slots. Same firing animation as the diagonal basket, but `rtjwayrycq` paints a half (5 rows or 5 cols) of the canvas instead of a triangle.
- Visual-vs-functional read:
  - At-rendered-scale shape: rectangular tray with one open edge.
  - Palette signature: 2, 15 (recoloured to dye).
  - Nearest-other-sprite check: distinguishable from the diamond basket by axis-alignment.

### `pqkenviek` — colour swatch
- Pixel pattern: 5×5 hollow palette-4 outer ring + 3×3 palette-0 inner fill. The interior is recoloured per placement (`color_remap(0, 15)`, `color_remap(0, 12)`, etc.) to display the swatch colour.
- Where it appears: every L1-3 level — multiple copies in a horizontal row at y=2. L1 has 2 swatches (palettes 0 and 15) at (35, 2), (41, 2). L2 has 3 swatches (0, 15, 12) at (32, 2), (38, 2), (44, 2). L3 has 7 swatches (0, 15, 12, 11, 14, 8, 9) at (21, 2)..(57, 2) in 6-cell stride.
- Role: clickable colour-picker. Click a swatch via ACTION6 → `qbiojckwxl` reads `swatch.pixels[2, 2]` (the centre pixel) as the new active dye colour `knqmgavuh`. The underline `ydiwkzjkgl` slides under the clicked swatch as a visual marker.
- Visual-vs-functional read:
  - At-rendered-scale shape: 5×5 hollow palette-4 frame with coloured interior.
  - Palette signature: 4 (frame, fixed) + interior (variable, identifies the colour).
  - Nearest-other-sprite check: distinct — only swatches use the 5×5 hollow-frame template.
- Visual contrast notes: clear colour identity per swatch via the inner fill; player can read which colour each one is.

### `xytrjjbyib` — central canvas
- Pixel pattern: 10×10 solid palette-0 (initially).
- Where it appears: every L1-3 level (1 copy at (27, 34)).
- Role: the painting target. Cells are recoloured in-place by `rtjwayrycq` (basket fires — half or triangle) and `coublenfir` (arrow-tank fires — 3×4 sub-stripe). Win when the canvas pattern matches the per-level target (excluding the X-cross diagonal cells).
- Visual-vs-functional read:
  - At-rendered-scale shape: 10×10 filled palette-0 square (initial); during play, partially painted with the dye colours.
  - Palette signature: starts at 0; ends with up to 7 colours depending on level.
  - Nearest-other-sprite check: visually it's a smaller square in the middle; the target-preview sprite to the right (`eoqnvkspoa-*`) is the comparison reference.

### `ydiwkzjkgl` — swatch underline
- Pixel pattern: 5×1 solid palette-0.
- Where it appears: every L1-3 level (1 copy initially under the leftmost swatch).
- Role: visual marker for the currently-selected swatch. When the player clicks a swatch in `qbiojckwxl`, the underline is repositioned to `(swatch.x, swatch.y + 5)` — i.e. directly below the clicked swatch.
- Visual-vs-functional read:
  - At-rendered-scale shape: thin 5-pixel-wide horizontal bar.
  - Palette signature: 0.
  - Nearest-other-sprite check: distinct — only the underline is 5×1.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (64, 64)
- Number of sprites placed: 7 — 1 target (`eoqnvkspoa-pqwme1-1` at (3, 3)), 1 UI frame (`gkyfnkvrty`), 1 horizontal basket (`oaoosfneq-oaanwen` at (25, 24) rotated 180°), 2 colour swatches (`pqkenviek` palette-0 at (35, 2), `pqkenviek` palette-15 at (41, 2)), 1 canvas (`xytrjjbyib` at (27, 34)), 1 swatch underline (`ydiwkzjkgl` at (41, 7)).
- Composition by role: 1 painting target + 1 UI frame + 1 active basket (placeholder; `gpfahgizbk` will replace it at level start with the slot-0 basket via `elltphoitr`) + 2 colour swatches + 1 canvas + 1 underline.
- Level data: none.
- Spawn position(s): no avatar in the conventional sense; the orbiting basket starts at slot 0 (`xwmfgtlso = 0`). Per `nicoqsvlg[0]`, slot 0 is `("horizontal", 25, 24, 180, 0, 1)` — a horizontal basket positioned above the canvas at (25, 24), rotated 180° (facing the canvas), with motion direction (0, 1) (downward into the canvas on FIRE).
- Per-cell layout (coordinate listing):
  - Target `eoqnvkspoa-pqwme1-1`: (3, 3), 10×10.
  - UI frame `gkyfnkvrty`: default (0, 0), 64×18.
  - Active basket (slot 0, horizontal at top): (25, 24), 14×9.
  - Swatches: (35, 2) palette-0, (41, 2) palette-15.
  - Canvas: (27, 34), 10×10.
  - Underline: (41, 7), 5×1 (initially under the palette-15 swatch).
  - Initial active dye `knqmgavuh` = 15 (palette-15) per `__init__`.
- Mechanic introduced relative to the previous level: this is the first level — introduces the **8-slot orbit + basket-fire + colour-pick** mechanic.
  - 8-slot ring: the basket lives at one of 8 positions around the canvas. Slot 0 = horizontal-top, slot 1 = diagonal-NE, slot 2 = horizontal-right, slot 3 = diagonal-SE, slot 4 = horizontal-bottom, slot 5 = diagonal-SW, slot 6 = horizontal-left, slot 7 = diagonal-NW.
  - 3×3 compass mapping: `nfhykrqjp` maps slot 0..7 to (col, row) in a 3×3 grid where (0,1), (0,2), (1,2), (2,2), (2,1), (2,0), (1,0), (0,0) are the 8 ring slots and (1,1) is the empty centre.
  - Arrow keys (ACTION1-4) move the basket one cell in the 3×3 compass via `nqhfiooufi` — UP→(col, max(0, row-1)), etc. The (1,1) centre is rejected; otherwise the new (col, row) is reverse-looked-up via `fbnqejrbl` to get the new slot index.
  - Click a swatch (ACTION6) → set `knqmgavuh` to the swatch's centre-pixel colour, slide the underline under it, respawn the basket recoloured.
  - FIRE (ACTION5) → `nlvliaznao` starts the firing animation; `hhjooisvrs` advances the basket 7 cells inward then 7 back, painting the canvas at the apex via `rtjwayrycq` — a horizontal basket at axial slot paints 5 rows or 5 cols of the canvas in the dye colour.
- Specific challenge: the L1 target has the top half black (palette-0) and the bottom half white (palette-15). The canvas starts all palette-0 (already top-half-correct). The player must paint the bottom half palette-15. Using a horizontal basket from the bottom slot (slot 4, accessed by orbiting around to the bottom of the canvas) and firing with palette-15 picked, the bottom 5 rows are painted palette-15. Done.
- Estimated optimal action count: ~6-10 (orbit ~3-4 arrow presses to reach slot 4, click palette-15 swatch if not already loaded, fire). The 100-step budget is generous.

### Level 2
- `grid_size`: (64, 64)
- Number of sprites placed: 8 — same as L1 but with 3 swatches (palettes 0, 15, 12 at (32, 2), (38, 2), (44, 2)) and target `eoqnvkspoa-pqwme2-1`. Underline starts at (38, 7) (under palette-15).
- Composition by role: 1 target + 1 UI frame + 1 basket placeholder + 3 swatches + 1 canvas + 1 underline.
- Level data: none.
- Spawn position(s): basket at slot 0 (top-axial); active dye starts palette-15.
- Per-cell layout:
  - Target `eoqnvkspoa-pqwme2-1`: (3, 3) — anti-diagonal split with palette-15 upper wedge, palette-12 lower wedge, palette-0 small corner.
  - UI frame: default.
  - Basket: slot 0.
  - Swatches: 3 at row 2.
  - Canvas: (27, 34).
  - Underline: (38, 7).
- Mechanic introduced relative to L1: **Diagonal-slot painting**. Pressing arrow keys can move the basket to a diagonal slot (1, 3, 5, 7). At a diagonal slot, `elltphoitr` swaps the basket sprite to `oaoosfneq-laopvne` (the diamond). On FIRE, `rtjwayrycq` paints a triangular wedge of the canvas (cells along the diagonal) in the dye colour. Plus a third colour (palette-12) is now in the swatch row.
- Specific challenge: produce the anti-diagonal target with palette-12 lower wedge + palette-15 upper wedge (and the small palette-0 corner remains because the canvas starts palette-0 there). Use diagonal-slot fires from corners with the right dye colours. Likely solution: load palette-12, fire from slot 5 (SW-diagonal), painting the lower-left triangle. Then load palette-15, fire from slot 1 (NE-diagonal), painting the upper-right triangle. The X-cross cells are excluded from the win predicate.
- Estimated optimal action count: ~10-15.

### Level 3
- `grid_size`: (64, 64)
- Number of sprites placed: 13 — 1 ctwspzkygu (the arrow-tank, at (29, 18) rotated 180°), 1 target `eoqnvkspoa-pqwme3-1`, 1 UI frame, 1 basket placeholder, 7 swatches (palettes 0, 15, 12, 11, 14, 8, 9 at x=21..57 stride 6, y=2), 1 canvas, 1 underline at (27, 7) (under palette-0).
- Composition by role: 1 target + 1 UI frame + 1 basket placeholder + 1 arrow-tank + 7 swatches + 1 canvas + 1 underline.
- Level data: none.
- Spawn position(s): basket at slot 0; active dye starts palette-15.
- Mechanic introduced relative to L2: **Arrow-tank firing** (`ctwspzkygu`). The arrow-tank avatar appears at axial slots only. The `eanmnpxtyi` helper repositions it to the appropriate offset relative to the basket's slot — `(yelyowpnp + offset_x, dzhdlpimn + offset_y)` per `wtkhwwfjfa[xwmfgtlso]`. Clicking the arrow-tank via ACTION6 (route through `qbiojckwxl` → `gfjfyvajah`) fires it inward toward the canvas: `jgclfnjrnk` advances the tank 7 cells in the slot's direction `azzmpqldgu` over many ticks, calls `coublenfir` at the apex which paints a 3-wide × 4-tall sub-stripe on the corresponding canvas edge in the dye, then retracts. So the arrow-tank fires a smaller, narrower paint patch than the basket — useful for fine adjustments.
  - Plus 7 colours instead of 3 → much more colour combinations.
- Specific challenge: the L3 target is a multi-region pattern with 4 colours (8, 12, 14, 15). The player needs to fire the basket multiple times from different slots with different dyes, possibly using the arrow-tank for fine corrections. Order matters — later fires can over-paint earlier ones.
- Estimated optimal action count: ~25-40.

Levels 4, 5, 6 exist but are excluded per skill scope.

## Action handlers

### ACTION1 / ACTION2 / ACTION3 / ACTION4 (UP / DOWN / LEFT / RIGHT — orbit step)
- Trigger: `self.action.id in [GameAction.ACTION1, ACTION2, ACTION3, ACTION4]`.
- Branches inside `step()`: first the lose check (`_action_count >= iewrsdwok`); then the firing-animation guards (`edjesyzxk` for basket fire, `yfobpcuef` for arrow-tank fire). If neither animation is in progress, dispatch to `nqhfiooufi(action_id)`:
  - Look up current slot's (col, row) in `nfhykrqjp`.
  - Apply the direction: ACTION1 → (col, max(0, row-1)); ACTION2 → (col, min(2, row+1)); ACTION3 → (max(0, col-1), row); ACTION4 → (min(2, col+1), row).
  - If the new (col, row) is (1, 1) (the centre), reject silently.
  - Otherwise look up the new slot via `fbnqejrbl[(col, row)]`. If different from current, set `xwmfgtlso = new_slot` and call `azhynfjdiz()` which removes the old basket, calls `elltphoitr()` to spawn a new basket at the new slot's position (using `nicoqsvlg[new_slot]`), and `eanmnpxtyi()` to reposition the arrow-tank if applicable.
- Increment `iieoxmyyd` (orbit-step counter — gates valid actions). Call `complete_action()`.
- State mutations: read `xwmfgtlso`, `nfhykrqjp`, `fbnqejrbl`, animation flags. Written: `xwmfgtlso`, basket sprite (removed and re-added), `iieoxmyyd`. The `eanmnpxtyi` may add/remove the arrow-tank too.
- Side effects on sprites: old basket removed; new basket added with `color_remap(15, knqmgavuh)`. Optionally arrow-tank repositioned/added/removed.
- Engine effects: none direct (no win/lose check on orbit step). `lose()` triggers from the budget check at top of `step()`.
- Pre-conditions / gating: rejected silently during firing animations or if the move would land on the centre slot.

### ACTION5 (FIRE basket)
- Trigger: `self.action.id == GameAction.ACTION5`.
- Branches: `nlvliaznao()` reads `nicoqsvlg[xwmfgtlso]` for the basket's anchor (sbyehouke, ukfstuctm) and motion type (`fmlnncybz` = "horizontal" or "diagonal"). Stores the anchor in `qsiruivbj`. Sets `edjesyzxk = True`, `fbdgdkqzm = 0` (animation tick), `mqivutapf = 1` (forward direction), `errfuhupi = 7` (peak distance). Resets `aalpkuosy = False` (paint-not-yet-applied flag).
- Subsequent ticks (driven by `hhjooisvrs` while `edjesyzxk` is True): advance the basket in (dx, dy) from `nicoqsvlg`. At tick 7 (peak), if not yet painted, call `rtjwayrycq` which paints the canvas — a 5-row or 5-col half (for horizontal slot) or a triangular wedge (for diagonal slot, using one of 4 fill-by-row patterns based on rotation 0/90/180/270). Then reverse direction. At tick 0 again, snap basket back to anchor, end animation, call `wvrremwltt` for win check.
- State mutations: `qsiruivbj`, `edjesyzxk`, `fbdgdkqzm`, `mqivutapf`, `errfuhupi`, `aalpkuosy`, basket position, canvas pixels.
- Engine effects: `next_level()` if `wvrremwltt` finds the canvas matches the target; `lose()` if budget exhausted.
- Pre-conditions / gating: silently no-op if the firing animation is already in progress.

### ACTION6 (click)
- Trigger: `self.action.id == GameAction.ACTION6`.
- Branches: `qbiojckwxl(x, y)` converts display to grid via `camera.display_to_grid`; finds the sprite at the grid cell with `ignore_collidable=True`. If the hit sprite is `ctwspzkygu` (the arrow-tank), look up the slot index from rotation (180→0, 270→2, 0→4, 90→6) and call `gfjfyvajah(slot)` which sets `yfobpcuef = True`, `wbcnpqkvw = 0` (animation tick), `hcmkqabzb = 1` (forward), `bjgtofqhv = arrow_tank`, `iswxsbrge = slot`. The arrow-tank fire animation runs in `jgclfnjrnk` over subsequent ticks — moves the tank 7 cells inward (offset in `azzmpqldgu`), at tick 7 calls `coublenfir` which paints the 3×4 sub-stripe on the corresponding canvas edge, then retracts. End-of-animation calls `wvrremwltt` for win check.
- If the hit sprite is `pqkenviek` (a colour swatch), read `swatch.pixels[2, 2]` as the new active dye `knqmgavuh`. Move the underline (`ydiwkzjkgl`) to `(swatch.x, swatch.y + 5)`. Call `azhynfjdiz()` to respawn the basket recoloured.
- Set `qnjvedxjm = True` (gates valid actions to "next must be ACTION5" if just clicked the arrow-tank; otherwise allows continued orbit).
- State mutations: `knqmgavuh`, `ydiwkzjkgl.position`, basket recoloured, possibly `yfobpcuef`/`bjgtofqhv`/`iswxsbrge`/`frnnxdfwb`, `qnjvedxjm`.
- Engine effects: at end of arrow-tank animation, `wvrremwltt` may call `next_level()`.
- Pre-conditions / gating: silent no-op if click misses any sprite.

## HUD widgets

### `aunldyudeb` — bottom-row depleting step bar
- Class name (obfuscated): `aunldyudeb`.
- Render-pixel range: row 63 (the very bottom row of the 64-tall frame), all 64 columns.
- What value it displays: `current_steps / qawfmbcuvz` (initial 100). Decremented every tick at the top of `step()` via `pioabixlyc(iewrsdwok - _action_count)`.
- Visual style: row 63 — palette-4 (off-grey) for the leading remaining-budget cells; palette-5 (background) for the depleted portion. The palette-4 segment shrinks from the right edge as the budget drains.
- Update points: `pioabixlyc` is called from (a) `__init__` and `on_set_level` (resets to max), and (b) the very first line of `step()` (per-tick refresh).
- Where it is registered: instantiated in `__init__` as `self.qzgkhffci = aunldyudeb(qawfmbcuvz=100)` and added via `Camera(... interfaces=[self.qzgkhffci])`.

## Internal state — exhaustive

| attr (obfuscated) | semantic name | type | initial value | written by | read by | role |
|---|---|---|---|---|---|---|
| `nicoqsvlg` | orbit_slot_table | `list[tuple[str, int, int, int, int, int]]` | 8 entries (one per slot) | `__init__` | `elltphoitr`, `nlvliaznao`, `hhjooisvrs`, `rtjwayrycq` | per-slot (basket_kind, x, y, rotation, dx, dy) |
| `nfhykrqjp` | slot_to_3x3_cell | `dict[int, tuple[int, int]]` | 8 entries | `__init__` | `nqhfiooufi` | maps slot 0..7 → (col, row) in compass |
| `fbnqejrbl` | 3x3_cell_to_slot | `dict[tuple[int, int], int]` | inverted from `nfhykrqjp` | `__init__` | `nqhfiooufi` | reverse map for orbit-step lookup |
| `xwmfgtlso` | current_orbit_slot | int | 0 | `__init__`, `on_set_level`, `nqhfiooufi` | many | which of the 8 slots the basket is at |
| `knqmgavuh` | active_dye_colour | int | 15 | `__init__`, `on_set_level`, `qbiojckwxl` | `elltphoitr`, `eanmnpxtyi`, `coublenfir`, `rtjwayrycq` | the picked-up dye palette |
| `lqrdkjrsl` | (unused in scope) | int | 1 | `__init__` | (none) | dead state |
| `edjesyzxk` | basket_firing_in_progress | bool | False | `__init__`, `on_set_level`, `nlvliaznao`, `hhjooisvrs` | `step` | gates the basket-fire animation |
| `fbdgdkqzm` | basket_anim_tick | int | 0 | `__init__`, `nlvliaznao`, `hhjooisvrs` | `hhjooisvrs` | basket-fire animation counter |
| `mqivutapf` | basket_anim_direction | int | 1 | `__init__`, `nlvliaznao`, `hhjooisvrs` | `hhjooisvrs` | +1 forward, -1 reverse |
| `errfuhupi` | basket_peak_distance | int | 0 | `__init__`, `nlvliaznao` | `hhjooisvrs` | how many cells inward the basket travels (=7) |
| `qsiruivbj` | basket_anchor | tuple[int, int] | (0, 0) | `__init__`, `nlvliaznao`, `hhjooisvrs` | `hhjooisvrs` (snap-back) | the basket's pre-fire position |
| `aalpkuosy` | basket_paint_done | bool | False | `__init__`, `nlvliaznao`, `hhjooisvrs` | `hhjooisvrs` | True after `rtjwayrycq` was called this fire |
| `yfobpcuef` | tank_firing_in_progress | bool | False | `__init__`, `on_set_level`, `gfjfyvajah`, `jgclfnjrnk` | `step` | gates the arrow-tank-fire animation |
| `wbcnpqkvw` | tank_anim_tick | int | 0 | `__init__`, `on_set_level`, `gfjfyvajah`, `jgclfnjrnk` | `jgclfnjrnk` | tank-fire counter |
| `hcmkqabzb` | tank_anim_direction | int | 1 | `__init__`, `on_set_level`, `gfjfyvajah`, `jgclfnjrnk` | `jgclfnjrnk` | +1/-1 |
| `bjgtofqhv` | tank_being_fired | `Sprite \| None` | None | `__init__`, `on_set_level`, `gfjfyvajah`, `jgclfnjrnk` | `jgclfnjrnk` | the arrow-tank sprite during firing |
| `iswxsbrge` | tank_slot | `int \| None` | None | `__init__`, `on_set_level`, `gfjfyvajah`, `jgclfnjrnk` | `jgclfnjrnk`, `coublenfir` | which slot the firing tank is at |
| `frnnxdfwb` | tank_anchor | tuple[int, int] | (0, 0) | `__init__`, `on_set_level`, `gfjfyvajah` | `jgclfnjrnk` | tank's pre-fire position for snap-back |
| `fgtugjktu` | tank_paint_done | bool | False | `__init__`, `on_set_level`, `gfjfyvajah`, `jgclfnjrnk` | `jgclfnjrnk` | True after `coublenfir` was called this fire |
| `yxjfgsdkm` | tank_present_in_level | bool | False | `__init__`, `on_set_level` | `eanmnpxtyi` | True iff the level placed a `ctwspzkygu` sprite (L3+) |
| `iewrsdwok` | max_steps | int | 100 | `__init__` | `step` | step budget |
| `qzgkhffci` | step_counter_HUD | `aunldyudeb` | `aunldyudeb(100)` | `__init__`, `on_set_level`, `step` | render | the bottom-row bar |
| `iieoxmyyd` | orbit_step_count | int | 0 | `__init__`, `on_set_level`, `step` | `_get_valid_actions` | counts orbit steps since last fire — gates valid action set |
| `qnjvedxjm` | just_clicked_tank | bool | False | `__init__`, `on_set_level`, `step` | `_get_valid_actions` | True after clicking the arrow-tank; gates next action to ACTION5 only |
| (inherited) `_action_count` | engine action counter | int | 0 | engine | `step` (lose check) | budget enforcement |

## Win condition

Plain English: the canvas pattern (excluding cells lying on either of its two diagonals — i.e. an X-shaped cross of cells is masked out) must equal the per-level target pattern.

Literal condition: `wvrremwltt()` (lines 718-731):
```python
notymrgpnm = self.current_level.get_sprites_by_name("xytrjjbyib")
vstazxqstp = [s for s in self.current_level.get_sprites() if s.name.startswith("eoqnvkspoa-")]
optphfbnep = notymrgpnm[0].pixels
pvdfcqjxfe = vstazxqstp[0].pixels
poqpfcjieu = np.ones((10, 10), dtype=bool)
for i in range(10):
    poqpfcjieu[i, i] = False
    poqpfcjieu[i, 9 - i] = False
if np.array_equal(optphfbnep[poqpfcjieu], pvdfcqjxfe[poqpfcjieu]):
    self.next_level()
```

Called from the end of every basket-fire animation (`hhjooisvrs` line 684) and every arrow-tank-fire animation (`jgclfnjrnk` line 588).

The diagonal-X mask `poqpfcjieu` excludes cells (i, i) and (i, 9-i) for i in 0..9 — these are the cells that the arrow-tank doesn't paint (diagonals are deliberately ignored to allow players to use diagonal baskets without needing perfect 1-pixel alignment).

Same predicate for L1, L2, L3.

## Lose condition

Plain English: lose if the engine's `_action_count` reaches 100.

Literal condition: at the top of `step()` (lines 609-613):
```python
self.qzgkhffci.pioabixlyc(self.iewrsdwok - self._action_count)
if self._action_count >= self.iewrsdwok:
    self.lose()
    self.complete_action()
    return
```

There is no other lose path (no hazard, no per-mistake penalty).

## Resource economy

- Depleting resource (energy / step counter / lives): YES — `_action_count` (engine-managed) compared against `iewrsdwok = 100`. Decremented by 1 per ACTION1-6 (the engine increments it per `complete_action`). Threshold 100 triggers `lose()`.
- Accumulating resource (collected items, score, sequence progress): NO numeric counter. The canvas's painted state is the implicit progress signal but not exposed as a number.
- Lives mechanic (respawn cost): NO. Single `lose()` ends the game.
- Resource interaction with win/lose: step budget is the sole lose trigger; canvas-matches-target is the sole win trigger. They are independent — running out of steps cannot win the level, and reaching the target pattern ends the level immediately regardless of remaining steps.

## Action-budget signature

- Default budget per level: 100 (`self.iewrsdwok = 100` in `__init__`).
- Whether budget tightens or shifts across levels 1-3: NO — same 100 each level.
- Per-level vs. per-environment: per-level (engine resets `_action_count` to 0 at every level transition).
- Decrement rate per action: 1 per ACTION1-6. Even no-op clicks (clicks that miss every clickable) cost 1.
- Refill mechanism: NONE.

## Notable code patterns / techniques

- **8-slot orbit modelled as the 8 non-centre cells of a 3×3 compass** (`nfhykrqjp` and `fbnqejrbl`): UP/DOWN/LEFT/RIGHT arrow keys map directly to incremental cell-moves in the compass, with the centre cell rejected. This is a clean way to express "orbit one slot at a time" as a 4-direction control.
- **Per-slot lookup table** (`nicoqsvlg`): single tuple per slot encoding (basket-kind, x, y, rotation, fire-dx, fire-dy). All slot-dependent behaviour reads from this table — easy to extend to more slots if needed.
- **Per-slot tank offset table** (`wtkhwwfjfa`): only axial slots have a tank avatar; the table provides offset and rotation so the tank's position relative to the basket is consistent.
- **Two-phase animation via tick + direction** (`fbdgdkqzm/mqivutapf` for basket, `wbcnpqkvw/hcmkqabzb` for tank): forward to peak (paint), then reverse to start. Single integer counter advances; sign of the direction variable controls the move direction.
- **Animation idempotency flag** (`aalpkuosy`, `fgtugjktu`): guards against double-painting if the animation logic is re-entered.
- **Snap-back to anchor** at end of animation (`set_position(*qsiruivbj)` / `set_position(*frnnxdfwb)`): ensures the firing element returns to its exact starting position regardless of integer rounding during animation.
- **Win-check excludes the X-cross diagonals** (`poqpfcjieu` mask): pragmatic choice to make diagonal-basket fires forgiving — those firmly land triangular wedges, and the diagonals themselves are excluded from comparison.
- **Centre-pixel as colour identifier on swatches** (`swatch.pixels[2, 2]`): clean way to read the dye colour from a sprite instance without name-parsing or external state.
- **Dynamic spawn/remove of basket per orbit step** (`elltphoitr`, `azhynfjdiz`): the basket is not retained across slots — it's destroyed and re-created at every step. Clean state but slightly wasteful.

## Anti-patterns / lessons

- **Two distinct firing modes** (basket fire via ACTION5, arrow-tank fire via clicking ctwspzkygu) — overlap in functionality. The basket already paints; the tank just paints a smaller patch. For a 3-level generated game, one firing mode is enough.
- **`lqrdkjrsl = 1` defined in `__init__` but never read** — dead state.
- **Two largely-parallel animation state machines** (basket: `fbdgdkqzm/mqivutapf/errfuhupi/aalpkuosy/edjesyzxk`; tank: `wbcnpqkvw/hcmkqabzb/yfobpcuef/fgtugjktu/bjgtofqhv/iswxsbrge`) with near-identical logic. Could be unified.
- **L4-6 introduce more colours but no new mechanic** — the 6 levels feel like the same puzzle with denser colour graphs. A 3-level generated game can stop after L3 (which already adds the arrow-tank).
- **The X-cross diagonals are excluded from the win check** — visually invisible to the player but mechanically critical. Players who try to perfectly paint the centre cells are wasting effort.
- **Underline (`ydiwkzjkgl`) is a 5×1 sprite** instead of a recoloured rim around the swatch — feels like an afterthought.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES (bottom row).
- Has lives mechanic: NO.
- Has click-to-select (uses ACTION6): YES (clicks on swatches and arrow-tank).
- Has tag-based grouping (uses `level.get_sprites_by_tag`): NO. The game uses `get_sprites_by_name` exclusively (no sprite has any tag).
- Uses ACTION5 (modal): YES (FIRE basket).
- Uses ACTION6 (click): YES.
- Uses ACTION7: NO.
- Has level data dicts (uses `level.get_data` / `level.set_data`): NO.
- Multi-mechanic per level (vs. single mechanic per level): NO — same orbit-and-fire mechanic across L1-3; L2 introduces diagonal slots, L3 adds the arrow-tank.
- Tutorial level appears solvable by random play: UNKNOWN — L1 needs orbiting to bottom slot + fire with palette-15. Random arrow-key spam might land on the right slot eventually, but reaching slot 4 randomly within 100 steps with a fire that uses the right colour is not guaranteed.
- Has a depleting resource: YES — step counter, 100 per level.
- Has an accumulating resource: NO.
- Sprite shape convention used: mixed — small filled square swatches, hollow rectangular and diamond baskets, small cabin-with-eyes glyph for the tank, large flat target image, single-pixel-tall underline.
- HUD position: bottom (single row).
- Palette size used: 9 distinct palette values across L1-3 sprites — {0, 2, 3, 4, 8, 11, 12, 14, 15} (the swatch colours plus baskets and frame). Plus palette-9 in L4-5 targets (out of scope).
- Background colour value: 5 (`BACKGROUND_COLOR = 5`).
- Padding / letter-box colour value: 4 (`PADDING_COLOR = 4`).
- Number of distinct mechanics introduced across levels 1-3: 3 — orbit-and-axial-fire in L1, diagonal-fire in L2, arrow-tank fire in L3.
- Number of levels documented: 3.

(End of file.)
