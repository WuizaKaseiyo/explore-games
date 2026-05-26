# cn04 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/cn04/65d47d14/cn04.py`
- Lines: 681
- Class name: `Cn04`
- available_actions: `[1, 2, 3, 4, 5, 6]` (UP/DOWN/LEFT/RIGHT, ACTION5=rotate, ACTION6=click)
- Number of levels in source: 5
- Number of levels documented in this analysis: 3
- Imports: `ActionInput`, `NovaBaseGame`, `Camera`, `GameAction`, `Level`, `RenderableUserDisplay`, `Sprite` from `novaengine`; `numpy as np`; `from numpy import ndarray`.

## Mechanic essence (one sentence)

A handful of coloured glyphs sit scattered on a coloured floor with tiny orange nubs poking off their edges, and clicking one lets the player slide it with the arrow keys or spin it ninety degrees so each glyph's nubs end up kissing exactly one nub of a neighbour — when no orange nub is left dangling, the level is solved.

## Sprite roster

| sprite (obfuscated) | dims | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| `aznnuvumhs` | 5x3 | 8, 13, -1 | sys_click | (default) | YES | (default) | YES | maroon block-glyph with 4 orange nubs (top+bottom corners) |
| `dnkiufrohe` | 5x4 | 8, 14, -1 | sys_click | (default) | YES | (default) | YES | green forked Y-glyph (level 5+) |
| `dzfylahsaw` | 4x7 | 8, 14, -1 | sys_click | (default) | YES | (default) | YES | green serpent vertical bar with 2 inward nubs (L1) |
| `eetyyobbee` | 5x2 | 8, 12, -1 | sys_click | (default) | YES | (default) | YES | purple horizontal bar with 2 nubs (unused in L1-3) |
| `ezhdijgxgn` | 8x5 | 6, 8, -1 | (default) | (default) | YES | (default) | YES | magenta L-shape with 2 nubs (unused in L1-3) |
| `fcdadbjhyk` | 6x6 | 8, 10, -1 | sys_click | (default) | YES | (default) | YES | cyan q-shape with 4 nubs (unused in L1-3) |
| `fjxymoivnf` | 11x11 | 8, 11, -1 | sys_click | (default) | YES | (default) | YES | yellow seahorse-like glyph with 5+ nubs (unused in L1-3) |
| `glojtydbea` | 4x7 | 8, 14, -1 | sys_click | (default) | YES | (default) | YES | green right-angle corner with 2 nubs (L2) |
| `gqxqpkuwab` | 5x3 | 8, 11, -1 | sys_click | (default) | YES | (default) | YES | yellow rectangle with 2 bottom nubs (L3) |
| `grpgefeksy` | 7x7 | 8, 11, -1 | sys_click | (default) | YES | (default) | YES | yellow figure-8/B-glyph with 5 nubs (L2) |
| `hjqjqsmhmf` | 3x5 | 8, 12, -1 | sys_click | (default) | YES | (default) | YES | purple vertical bar with 2 right-side nubs (L3) |
| `kddtjradhp` | 5x5 | 7, 8, -1 | sys_click | (default) | YES | (default) | YES | pink Γ-shape with 2 nubs (unused in L1-3) |
| `kodeocvgpm` | 6x5 | 7, 8, -1 | (default) | (default) | YES | (default) | YES | pink L-shape with 2 nubs (unused in L1-3) |
| `lejuhuvrjg` | 3x6 | 8, 15, -1 | sys_click | (default) | YES | (default) | YES | purple-15 vertical bar with 2 right-side nubs (L2) |
| `lxgvcnpsir` | 4x6 | 8, 12, -1 | sys_click | (default) | YES | (default) | YES | purple flat-rectangle with 2 nubs (level 5+) |
| `nhppemmlcd` | 5x4 | 8, 10, -1 | sys_click | (default) | YES | (default) | YES | cyan horizontal bar with 4 nubs (top+bottom) (L3) |
| `oncjjftokv` | 1x5 | 8, 11 | sys_click | (default) | YES | (default) | YES | yellow vertical pillar with 2 end nubs (level 5+) |
| `rlaifclqmn` | 5x6 | 8, 14, -1 | sys_click | (default) | YES | (default) | YES | green cradle/J-shape with 2 nubs (unused in L1-3) |
| `supigciwwi` | 6x6 | 8, 10, -1 | sys_click | (default) | YES | (default) | YES | cyan partial-frame with 2 nubs (level 5+) |
| `udepuflbbb` | 7x5 | 8, 14, -1 | sys_click | (default) | YES | (default) | YES | green T-with-stand glyph with 2 nubs (level 4+) |
| `vmgdxvpgkh` | 6x5 | 8, 12, -1 | sys_click | (default) | YES | (default) | YES | purple E-shape with 2 right-side nubs (L1) |
| `ygyvhkssnz` | 7x7 | 8, 15, -1 | sys_click | (default) | YES | (default) | YES | white-15 spiral/G-shape with 2 nubs (level 4+) |
| `zhhaofpbyw` | 2x6 | 8, 11 | sys_click | (default) | YES | (default) | YES | yellow narrow vertical strip with 2 end nubs (level 4+) |

### `aznnuvumhs` — maroon block with 4 corner nubs (unused in L1-3)
- Pixel pattern: 5×3; row 0 has nubs at cols 0 and 2 (`8, -1, 8`), rows 1-2 are solid maroon (13), row 3 has hollow centre (`13, -1, 13`), row 4 has nubs at cols 0 and 2.
- Where it appears: not placed in any of L1-3.
- Role: unused colour-13 block-glyph kept in the sprite library.
- Visual-vs-functional read: at-rendered-scale shape: filled-with-corners glyph; palette signature: 8 (nub), 13 (maroon body); 8 is shared with **every** other sprite as the universal "tab" marker. Nearest-other-sprite check: `eetyyobbee` is also a small filled bar with palette-8 nubs but uses palette-12 (purple) instead of 13 (maroon); player tells them apart by body colour.
- Visual contrast notes: maroon (13) is a rare body colour in this game's roster — most others use 11, 12, 14, 15 — so this one stands out if placed.

### `dnkiufrohe` — green forked Y-glyph (level 5+ only)
- Pixel pattern: 5×4; corners at row 0 are `8, 14, -1, 14, 8`; columns 1 and 3 are continuous `14`; row 3 has a fused base `-1, 14, 14, 14, -1`. So a Y-shape with two upper arms ending in nubs and a stem at bottom.
- Where it appears: not placed in any of L1-3 (level 5).
- Role: out of scope.
- Visual-vs-functional read: filled, hollow centre, Y-form; palette 14 (green) + 8 (nub). Nearest-other-sprite: `dzfylahsaw` is also green with hollow body and nubs; tells apart by Y-fork vs vertical bar.
- Visual contrast notes: same green as `dzfylahsaw`, `glojtydbea`, `rlaifclqmn`, `udepuflbbb`.

### `dzfylahsaw` — green vertical-rail glyph (L1)
- Pixel pattern: 4 cols × 7 rows. Cols 1 and 3 are continuous palette-14 from row 0 to row 6; row 0 has cap `-1, 14, 14, 14`; row 6 has cap `-1, 14, 14, 14`. Two side-nubs at (col 0, row 2) and (col 0, row 4) (palette 8). The pattern reads as a hollow vertical I-beam with 2 left-side nubs.
- Where it appears: L1 only (1 copy at (12, 9)).
- Role: one of two pieces in L1; movable interactable. The 2 left-side nubs must each find a partner.
- Visual-vs-functional read: hollow rail glyph; palette 14 + 8. Nearest-other: `glojtydbea` is also a green nubbed glyph but L-shaped instead of I-shaped; tells apart by overall outline.
- Visual contrast notes: against L1 background palette-10 (cyan), green-14 contrasts well; orange-8 nubs are very salient on the cyan floor.

### `eetyyobbee` — purple horizontal bar (unused in L1-3)
- Pixel pattern: 5×2. Row 0 is solid `12,12,12,12,12`, row 1 is `12, 8, -1, 8, 12` (purple body with two nubs poking down).
- Where it appears: not placed in any of L1-3.
- Role: unused.
- Visual-vs-functional read: filled bar with downward nubs; palette 12 + 8. Nearest-other: `gqxqpkuwab` is also a small bar with 2 nubs but in palette 11 (yellow); tells apart by colour.
- Visual contrast notes: purple-12 is also used by `vmgdxvpgkh`, `hjqjqsmhmf`, `lxgvcnpsir`.

### `ezhdijgxgn` — magenta L-shape with 2 nubs (unused in L1-3)
- Pixel pattern: 8×5. Col 0 is mostly palette-6 (magenta) running rows 1-4; row 4 extends `6,6,6,6,6,6,6,8` so an L hooks right and ends with a nub. A nub at (col 0, row 0) too. So two nubs at the L's free ends.
- Where it appears: not placed in L1-3.
- Role: unused.
- Visual-vs-functional read: open L-frame; palette 6 + 8. **No `sys_click` tag** — only sprite without it (along with `kodeocvgpm`). This is the only structural difference; in this game it doesn't matter because `step()` reads `get_sprite_at(..., ignore_collidable=True)` which ignores the tag-based selection gate.
- Visual contrast notes: magenta-6 is unique to this sprite in the roster — distinct.

### `fcdadbjhyk` — cyan q-glyph (unused in L1-3)
- Pixel pattern: 6×6. A near-closed cyan-10 ring with one nub at (col 4, row 0), nub at (col 0, row 4), nub at (col 5, row 4), nub at (col 4, row 5). Reads as a "q" with 4 nubs around its perimeter.
- Where it appears: not placed in L1-3.
- Role: unused.
- Visual-vs-functional read: hollow ring/loop; palette 10 + 8. Nearest-other: `nhppemmlcd` (also cyan), `supigciwwi` (also cyan); tells apart by q-form vs horizontal bar vs frame.

### `fjxymoivnf` — yellow seahorse-like 11x11 (unused in L1-3)
- Pixel pattern: large 11×11 yellow body with multiple internal hollows; nubs scattered at (5,0), (7,0), (1,6), (8,5), (0,7), (10,7), (7,10).
- Where it appears: not placed in L1-3.
- Role: unused (large sprite).
- Visual-vs-functional read: complex filled body with many interior hollows; palette 11 + 8. Nearest-other: `grpgefeksy` is also yellow (11) with multiple nubs; tells apart by overall silhouette.

### `glojtydbea` — green corner-piece (L2)
- Pixel pattern: 4 cols × 7 rows. Col 3 is continuous palette-14 rows 0-5; row 6 is solid `14,14,14,14`. Forms a flag-pole / right-angle. Nubs at (col 2, row 0) and (col 0, row 5).
- Where it appears: L2 only (1 copy at (12, 4)).
- Role: one of three movable pieces in L2.
- Visual-vs-functional read: open right-angle; palette 14 + 8. Nearest-other: `dzfylahsaw` is also green I-beam with side nubs; tells apart by L-frame vs I-frame.

### `gqxqpkuwab` — yellow flat rectangle (L3)
- Pixel pattern: 5×3. Rows 0-1 are solid `11,11,11,11,11`, row 2 is `-1, 8, -1, 8, -1` — two downward nubs.
- Where it appears: L3 only (1 copy at (11, 4)).
- Role: one of three pieces in L3.
- Visual-vs-functional read: filled bar with downward nubs; palette 11 + 8. Nearest-other: `eetyyobbee` (purple flat bar with 2 down-nubs); tells apart by colour.

### `grpgefeksy` — yellow B/8-glyph (L2)
- Pixel pattern: 7×7. Yellow-11 figure-8 silhouette with 5 nubs in irregular positions: (col 1, row 1), (col 6, row 1), (col 0, row 3), (col 4, row 6).
- Where it appears: L2 only (1 copy at (4, 11)).
- Role: one of three pieces in L2; the "hub" sprite — has more nubs than the others, so it acts as the central node every other sprite must contact.
- Visual-vs-functional read: closed-loop yellow glyph with multi-direction nubs; palette 11 + 8. Nearest-other: `fjxymoivnf` is much larger but same colour; tells apart by size.

### `hjqjqsmhmf` — purple vertical bar (L3)
- Pixel pattern: 3×5. Cols 0-1 are solid palette-12; col 2 alternates `-1, 8, -1, 8, -1` — two right-side nubs.
- Where it appears: L3 only (1 copy at (5, 5)).
- Role: one of three pieces in L3.
- Visual-vs-functional read: filled vertical bar with side nubs; palette 12 + 8. Nearest-other: `vmgdxvpgkh` is also purple but E-shaped; tells apart by E vs bar.

### `kddtjradhp` — pink Γ-shape (unused in L1-3)
- Pixel pattern: 5×5. Row 0 is `7,7,7,7,8`; col 0 is solid `7` rows 0-4; (col 0, row 4) is a nub. Forms a pink-7 right angle / Γ with 2 nubs at the open ends.
- Where it appears: not placed in L1-3.
- Role: unused.
- Visual-vs-functional read: open right-angle; palette 7 + 8. Nearest-other: `kodeocvgpm` (also pink, also Γ-form, mirrored).

### `kodeocvgpm` — pink mirrored Γ-shape (unused in L1-3)
- Pixel pattern: 6×5. Col 5 has nub at (col 5, row 0), pink at rows 1-3, palette-7 at row 4; row 4 is `8, 7, 7, 7, 7, 7`. Mirror of `kddtjradhp`.
- Where it appears: not placed in L1-3.
- Role: unused. **No `sys_click` tag** (only this and `ezhdijgxgn` lack it).
- Visual-vs-functional read: open right-angle; palette 7 + 8. Nearest-other: `kddtjradhp` (mirror image, same colour) — visually nearly identical except for chirality.

### `lejuhuvrjg` — purple-15 vertical bar with 2 right-side nubs (L2)
- Pixel pattern: 3×6. Col 0 is solid palette-15 rows 0-5; col 2 has palette-15 at rows 0-1 and palette-8 at rows 3, 5 (right-side nubs).
- Where it appears: L2 only (1 copy at (3, 3)).
- Role: one of three pieces in L2.
- Visual-vs-functional read: hollow rail glyph; palette 15 + 8. **Palette 15** is the "white-purple" hue; this is the only sprite using it on L2 (background is 12, so 15 contrasts as a slightly lighter tone). Nearest-other: `ygyvhkssnz` (also 15, but spiral/G-shaped, level 4+ only).
- Visual contrast notes: against L2's purple-12 background, palette-15 contrasts sufficiently but not boldly.

### `lxgvcnpsir` — purple flat rectangle (level 5+)
- Pixel pattern: 4×6. Row 0 `8, 12, 12, 12`; col 1 and col 3 run `12` down; row 5 `8, 12, 12, 12`. Reads as a hollow rectangle frame with 2 nubs.
- Where it appears: not placed in L1-3.
- Role: out of scope.

### `nhppemmlcd` — cyan horizontal bar with top+bottom nubs (L3)
- Pixel pattern: 5×4. Row 0 `-1, 8, -1, 8, -1` (2 top nubs); rows 1-2 solid `10,10,10,10,10`; row 3 `-1, 8, -1, 8, -1` (2 bottom nubs).
- Where it appears: L3 only (1 copy at (9, 11)).
- Role: one of three pieces in L3; centre-piece of the puzzle (has 4 nubs vs neighbours' 2).
- Visual-vs-functional read: filled bar with vertical nubs; palette 10 + 8. Nearest-other: `eetyyobbee`, `gqxqpkuwab` are also flat bars with 2 nubs; tells apart by total nub count and palette.

### `oncjjftokv` — 1-wide yellow pillar (level 5+)
- Pixel pattern: 1×5. Row 0 `8`, rows 1-3 `11`, row 4 `8`. A 1-pixel-wide yellow line with end nubs.
- Where it appears: not placed in L1-3.

### `rlaifclqmn` — green cradle/J-shape (unused in L1-3)
- Pixel pattern: 5×6. Col 4 runs palette-14 down full height; row 5 is solid `14,14,14,14,14`. Reads as an open J. Nubs at (col 3, row 0) and (col 0, row 3).
- Where it appears: not placed in L1-3.

### `supigciwwi` — cyan partial-frame (level 5+)
- Pixel pattern: 6×6. Mostly hollow rectangle in palette 10 with 2 nubs at (col 5, row 0) and (col 5, row 5).
- Where it appears: not placed in L1-3.

### `udepuflbbb` — green T-with-stand (level 4+)
- Pixel pattern: 7×5. Top row `8, -1, -1, -1, -1, -1, 8`; rows 1-4 form a T-shape; nubs at top-left and top-right corners.
- Where it appears: not placed in L1-3.

### `vmgdxvpgkh` — purple E-shape (L1)
- Pixel pattern: 6×5. Col 0 is solid palette-12 rows 0-4; row 0 `12,12,12,-1,-1,-1`; row 1 `12,-1,12,12,12,8` (right-side nub); row 2 `12,-1,-1,-1,-1,-1`; row 3 `12,-1,12,12,12,8` (right-side nub); row 4 `12,12,12,-1,-1,-1`. Reads as a sideways-E with 2 right-side nubs.
- Where it appears: L1 only (1 copy at (4, 4)).
- Role: one of two pieces in L1.
- Visual-vs-functional read: comb-like filled glyph; palette 12 + 8. Nearest-other: `hjqjqsmhmf` (also purple, also right-side nubs) — but smaller and just a vertical bar.

### `ygyvhkssnz` — palette-15 spiral/G-shape (level 4+)
- Pixel pattern: 7×7 spiral made of palette-15. Two nubs.
- Where it appears: not placed in L1-3.

### `zhhaofpbyw` — narrow yellow strip (level 4+)
- Pixel pattern: 2×6. Col 0 `8, -1, -1, -1, -1, -1`; col 1 `11, 11, 11, 11, 11, 8`. Thin yellow bar with 1 nub at top-left and 1 at bottom-right.
- Where it appears: not placed in L1-3.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (20, 20)
- Number of sprites placed: 2
- Composition by role: 2 movable click-selectable glyphs (1 green vertical I-beam `dzfylahsaw`, 1 purple sideways-E `vmgdxvpgkh`). Background palette 10 (cyan). No HUD glyph beyond the camera-level step counter.
- Level data: `{"BackgroundColour": 10}` — sets both `camera.background` and `camera.letter_box` to palette 10 in `on_set_level`.
- Spawn position(s): no avatar; the sprite closest to the origin (smallest x²+y²) is auto-selected on level start. With `dzfylahsaw` at (12,9) and `vmgdxvpgkh` at (4,4), `vmgdxvpgkh` (distance² = 32) is selected initially over `dzfylahsaw` (distance² = 225).
- Per-cell layout (coordinate listing, 20×20):
  - `vmgdxvpgkh` (purple E): top-left at (4, 4), occupies rows 4-8 cols 4-9 (height 5, width 6). Right-side nubs at world (10, 5) and (10, 7).
  - `dzfylahsaw` (green I-beam): top-left at (12, 9), occupies rows 9-15 cols 12-15 (height 7, width 4). Left-side nubs at world (12, 11) and (12, 13).
- Mechanic introduced relative to the previous level: this is the first level — introduces the **nub-pairing** mechanic. Each sprite has palette-8 nubs poking off its outline; the player must arrange the sprites so every nub on every sprite occupies the same cell as exactly one nub from a different sprite. Click-to-select via ACTION6, arrow-key motion via ACTION1-4, in-place rotation via ACTION5. Move attempts that would push the sprite off the 20×20 grid are silently rejected (the bounds check at lines 657-663 just no-ops).
- Specific challenge: 2 nubs on the green I-beam and 2 nubs on the purple E. The I-beam's nubs face left (col 0 within sprite), the E's nubs face right (col 5 within sprite). To pair them, slide the E rightward and/or the I-beam leftward until each E-nub aligns with an I-beam-nub. The vertical spacing of nubs is the same on both sprites (rows 1, 3 in their local frames), so once aligned horizontally and vertically the puzzle solves.
- Estimated optimal action count: ~6-10 (1 click to select either piece, ~3-6 moves to align horizontally and vertically, optional 1 click to swap selected piece for fine-tuning, plus 1 final move that triggers `exlcvhdjsf()` returning True).

### Level 2
- `grid_size`: (20, 20)
- Number of sprites placed: 3
- Composition by role: 3 movable click-selectable glyphs — `glojtydbea` (green corner), `grpgefeksy` (yellow B/8 hub with 5 nubs), `lejuhuvrjg` (purple-15 vertical with 2 nubs). Background palette 12 (purple).
- Level data: `{"BackgroundColour": 12}`.
- Spawn position(s): closest-to-origin sprite is auto-selected. `lejuhuvrjg` at (3, 3) (distance² = 18) wins.
- Per-cell layout:
  - `lejuhuvrjg` (palette-15 vertical bar): (3, 3), height 6 width 3. Right-side nubs at world (5, 6), (5, 8).
  - `grpgefeksy` (yellow B): (4, 11), height 7 width 7. 5 nubs at world (5, 12), (10, 12), (4, 14), (4, 16), (8, 17). (Computed from sprite-local nub coords (1,1),(6,1),(0,3),(0,5),(4,6).)
  - `glojtydbea` (green corner): (12, 4), height 7 width 4. Nubs at world (14, 4), (12, 9). (Sprite-local nubs at (2,0) and (0,5).)
- Mechanic introduced relative to L1: **Multi-piece nub-graph** — three sprites instead of two, and one of them (`grpgefeksy`) has 5 nubs while the other two have 2 each. The B-glyph acts as the puzzle hub: each of its 5 nubs must pair with one nub from a neighbour, but the neighbours together only supply 4 nubs (2 + 2). So at least one of the B's nubs must pair *with another nub of the B itself* (intra-sprite pairing — handled implicitly because the win check `exlcvhdjsf` only requires that no palette-8 pixel remains in a sprite's *un-overlapped* render). Re-reading the win check: actually, it iterates each sprite, walks its overlap-set `dpmge`, marks those overlap pixels as palette-3, and asks "is any palette-8 left?" So intra-sprite pairing is NOT counted (overlap requires `len(amkqyhsyhd) == 2` which means two **distinct** sprites at the same world cell). Therefore the puzzle is unsolvable as stated unless an additional nub pair shows up off-screen — i.e. the B-glyph must move so that one of its odd-numbered nubs sits *outside* the grid bounds. But the move logic rejects moves that put the sprite past the grid. So the fifth nub must be paired by clever stacking: rotation could move the B's nubs to align with both neighbours' nubs at once. Likely intended solution: ROTATE the B (or one of the others) so that the nub layout maps onto exactly 4 paired neighbour-nubs and one self-overlap that is never resolved to a palette-8 in the first place because of how the rotated `npwwu` coordinates remap. The win predicate only checks `np.any(rurikqkuoc == 8)` per sprite, so a rotated rendering where all 5 nubs land on a neighbour cell after the rotation transform is what counts.
- Specific challenge: orient the B-glyph with rotations + position so all 5 of its nubs simultaneously occupy cells with the green-corner's or purple-bar's nubs. The corner has 1 top-edge nub and 1 left-edge nub; the purple bar has 2 right-side nubs spaced 2 apart. The player must figure out which three of the B's 5 nubs pair with the bar's 2 + the corner's 2, and arrange a rotation such that the remaining nubs fall on top of unused B-pixels (which the rotation transform will mark palette-3 on the same render pass).
- Estimated optimal action count: ~12-20 (multiple click-selects to switch between sprites, several moves per sprite, 1-3 rotations).

### Level 3
- `grid_size`: (20, 20)
- Number of sprites placed: 3
- Composition by role: 3 movable click-selectable glyphs — `gqxqpkuwab` (yellow flat bar with 2 down-nubs), `hjqjqsmhmf` (purple vertical with 2 right-nubs), `nhppemmlcd` (cyan horizontal with 4 nubs — 2 up + 2 down). Background palette 15.
- Level data: `{"BackgroundColour": 15}`.
- Spawn position(s): closest-to-origin auto-selected. `hjqjqsmhmf` at (5, 5) (distance² = 50) wins.
- Per-cell layout:
  - `hjqjqsmhmf` (purple vertical): (5, 5), height 5 width 3. Right-side nubs at world (7, 6), (7, 8).
  - `nhppemmlcd` (cyan horizontal hub with 4 nubs): (9, 11), height 4 width 5. Top-row nubs at world (10, 11), (12, 11); bottom-row nubs at world (10, 14), (12, 14).
  - `gqxqpkuwab` (yellow flat bar): (11, 4), height 3 width 5. Bottom-row nubs at world (12, 6), (14, 6).
- Mechanic introduced relative to L2: **Hub with 4 nubs that must pair with 2 + 2 from neighbours simultaneously** (4 = 2 + 2, balanced). No new tag, no level-data feature; the difficulty bump is geometric: the cyan hub sits in the middle and the two neighbours dock onto top and bottom of it.
- Specific challenge: the cyan hub `nhppemmlcd` has 4 nubs (2 top, 2 bottom). The yellow bar has 2 down-nubs that must dock onto the cyan's 2 top-nubs; the purple vertical has 2 right-side nubs that must dock onto either the top or bottom of the cyan after rotation. The player must rotate the purple bar (90°) so its 2 right-side nubs become 2 down-nubs (or up-nubs), then position both neighbours to align their nub-pairs with the cyan's nub-pairs.
- Estimated optimal action count: ~10-16 (1-2 clicks to switch pieces, ~6 moves to position, 1-2 rotations).

Levels 4, 5 exist but are excluded per skill scope.

## Action handlers

### ACTION1, ACTION2, ACTION3, ACTION4 (UP / DOWN / LEFT / RIGHT)
- Trigger: `self.action.id in [GameAction.ACTION1, ACTION2, ACTION3, ACTION4]`.
- Branches inside `step()`: if `self.weqid` (selected sprite) is None, the branch falls through to the bottom of `step()` and `complete_action()` returns. Otherwise compute (dx, dy): ACTION1 → (0,-1), ACTION2 → (0,+1), ACTION3 → (-1,0), ACTION4 → (+1,0). Read `current_level.grid_size`; if None return early (defensive — doesn't reach here in normal play). Compute prospective new (x, y) = (`weqid.x + dx`, `weqid.y + dy`); if it stays inside `[0, grid_w - sprite.width] × [0, grid_h - sprite.height]`, call `self.weqid.move(dx, dy)`. **No collision check between sprites** — sprites can overlap freely (this is the entire point of the nub-pairing mechanic). After the move (or rejected attempt), call `self.gjhtwbvrel()` to recompute every sprite's nub overlap render-state, then call `self.exlcvhdjsf()` to check if no palette-8 remains anywhere; if so, `self.next_level()`. Set `self.fubdf = False`. Always falls through to `self.complete_action()` at the bottom of `step()`.
- State mutations: read `self.weqid`, `self.action.id`, `self.current_level.grid_size`. Written: `self.weqid.x`, `self.weqid.y` (via `move`), `self.dpmge` (via `gjhtwbvrel`), every `sprite.pixels` array (via `gjhtwbvrel` recolouring), `self.fubdf` (set False).
- Side effects on sprites: `weqid.move(dx, dy)`, `weqid.set_layer(4)` (was already set when selected), and inside `gjhtwbvrel` every sprite has `sprite.pixels = self.npwwu[name].copy()` then nub-overlap pixels are flipped to palette 3; the selected sprite has additional pre-recolouring (non-8 non-3 pixels become 0).
- Engine effects: `self.next_level()` if win predicate passes; otherwise no engine call beyond `complete_action()`.
- Pre-conditions / gating: rejected if `self.weqid is None`. Movement rejected if it would push sprite off the grid (silent no-op, animation still consumes the action).

### ACTION5 (rotate selected sprite by 90°)
- Trigger: `self.action.id == GameAction.ACTION5`.
- Branches: if `self.weqid is None`, no-op. Otherwise call `self.weqid.rotate(90)` (engine method on `Sprite`). Then `self.gjhtwbvrel()` and `self.exlcvhdjsf()`; if the latter is True, `self.next_level()`. Set `self.fubdf = False`.
- State mutations: read `self.weqid`. Written: `self.weqid.rotation`, `self.dpmge`, every `sprite.pixels`, `self.fubdf`.
- Side effects on sprites: `weqid.rotate(90)`.
- Engine effects: `next_level()` if win predicate passes.
- Pre-conditions / gating: rejected (silently no-op'd) if no sprite is selected. Importantly, `_get_valid_actions()` whitelists ACTION5 only when `self.fubdf` is True (i.e. immediately after a click): once the selection was made, the next action can be either a move (1-4) or a rotation (5), but NOT another click (6).

### ACTION6 (click — select / deselect sprite)
- Trigger: `self.action.id == GameAction.ACTION6`.
- Branches: read `(x, y)` from `action.data`, convert via `self.camera.display_to_grid` to grid coords. If conversion fails (off-frame), fall through. Else `quyphwtvrr = self.current_level.get_sprite_at(dqudz, uermy, ignore_collidable=True)`; this returns the topmost sprite at that grid cell regardless of collidability (so even if a sprite is collidable=True that's fine, the flag is ignored here). If the click hits the currently-selected sprite, call `self.pvrlqzlpjy()` which restores its pre-selection pixels and sets `self.weqid = None`. Otherwise call `self.lceflskdhw(quyphwtvrr)` which (a) restores the previously selected sprite if any, (b) caches `agupi[name] = sprite.pixels.copy()`, (c) recolours `sprite.pixels` so non-8 non-3 pixels become 0 (selection-highlight inversion), (d) sets `weqid.set_layer(4)` (raise selected sprite to top), (e) calls `gjhtwbvrel`. Set `self.fubdf = True`.
- State mutations: read `self.action.data`, `self.weqid`, `self.camera`, `self.current_level`. Written: `self.weqid`, `self.agupi`, `self.dpmge`, every selected sprite's `pixels` and `layer`, `self.fubdf` set True.
- Side effects on sprites: previously-selected sprite's `pixels` restored from `self.agupi[name]`; new sprite's `pixels` recoloured (non-8/non-3 → palette 0) and `set_layer(4)`.
- Engine effects: none for click — no `lose()`, no `next_level()` directly. Win check is NOT performed on click (only on move/rotate), which is correct because clicking a sprite doesn't change its world position.
- Pre-conditions / gating: rejected if click off-frame (silent no-op). Rejected if click misses every sprite (no `weqid` change).

## HUD widgets

### `qdcvayjdkm` — top-row centred step bar
- Class name (obfuscated): `qdcvayjdkm`.
- Render-pixel range: row 0 only, columns 16-47 (centred 32-pixel-wide horizontal strip on the 64-wide frame). Computed as `x_offset = (64 - 32) // 2 = 16`.
- What value it displays: `self.current_steps / self.mimisncrjk` — the proportion of step budget remaining (numerator counts down). The game writes `self._step_counter_ui.ivinkcxarj(self.guweh - self._action_count)` at the very top of every `step()`, so it updates each tick.
- Visual style: depleting horizontal bar — palette-0 (black) cells fill the **left** portion (`x < ckkdtrybdj` where `ckkdtrybdj = hsoumyqjja - ukcleokzfb` is the depleted count) and palette-4 (background-grey) fills the right portion (the remaining-time portion). Because depletion fills from the left and remaining stays on the right, the bar visually "drains from the left". (If `mimisncrjk == 0`, the function returns the frame unmodified.)
- Update points: `ivinkcxarj` is called from (a) `Cn04.on_set_level` (line 435) which sets it to `self.guweh = 150`, and (b) the very first line of `Cn04.step` (line 615).
- Where it is registered: instantiated in `Cn04.__init__` and immediately added via `pzqnb.replace_interface([self._step_counter_ui])` before `super().__init__`.

## Internal state — exhaustive

| attr (obfuscated) | semantic name | type | initial value | written by | read by | role |
|---|---|---|---|---|---|---|
| `_step_counter_ui` | step-counter HUD | `qdcvayjdkm` | `qdcvayjdkm(150)` | `__init__`, `on_set_level`, `step` | `step`, `on_set_level`, camera | renders the depleting top bar |
| `weqid` | selected_sprite | `Sprite \| None` | None | `__init__`, `lceflskdhw`, `pvrlqzlpjy`, `on_set_level` | `step`, `lceflskdhw`, `pvrlqzlpjy`, `gjhtwbvrel` | the currently-selected piece awaiting move/rotate |
| `agupi` | pre_selection_cache | `dict[str, ndarray]` | `{}` | `__init__`, `on_set_level`, `lceflskdhw`, `pvrlqzlpjy` | `pvrlqzlpjy` | snapshot of a sprite's pixels just before it became selected, used to restore its appearance on deselect |
| `npwwu` | original_pixels_cache | `dict[str, ndarray]` | `{}` | `__init__`, `on_set_level` | `gjhtwbvrel`, `exlcvhdjsf`, `lceflskdhw` | reference copy of every sprite's untouched pixel data (pre-selection-highlight, pre-overlap-recolour) used as the source of truth for nub-overlap detection |
| `dpmge` | overlap_local_coords | `dict[str, set[tuple[int, int]]]` | `{}` | `gjhtwbvrel` | `gjhtwbvrel`, `exlcvhdjsf` | per-sprite set of local-frame (x, y) palette-8 cells that overlap *another* sprite's palette-8 cell at the same world position (used to repaint those cells palette 3) |
| `mctam` | level4_blanking_active | bool | False | `on_set_level` | `lceflskdhw`, `pvrlqzlpjy`, `gjhtwbvrel` | True iff level index ≥ 4; gates the L4+ "blank everything to palette 4 except nubs" rendering branch (out of scope but present) |
| `guweh` | max_steps_per_level | int | 150 | `__init__` | `step`, `on_set_level` | step budget per level; `lose()` fires at `_action_count >= 150` |
| `fubdf` | just_clicked_flag | bool | False | `__init__`, `on_set_level`, `step` | `_get_valid_actions` | gates valid actions: True after a click → next action must be in {1,2,3,4,5}; False otherwise → all of {1..6} are valid |
| (inherited) `_action_count` | step count for current level | int | 0 | engine | `step`, `_get_hidden_state` | counts up per action; compared against `guweh` |
| (inherited) `_current_level_index` | current level | int | 0 | engine | `on_set_level`, `lceflskdhw`, `pvrlqzlpjy`, `gjhtwbvrel` | branch gate for L4+ blanking |

## Win condition

Plain English: the level wins when, after re-applying every sprite's stored "original" pixel array (`self.npwwu[name]`) and then flipping every overlap-pair palette-8 pixel to palette 3, no palette-8 pixel remains anywhere across all sprites. In other words: every nub on every sprite is paired with a nub from at least one other sprite.

Literal condition: `Cn04.exlcvhdjsf()` (line 587-611) iterates each sprite, copies `self.npwwu[sprite.name]`, walks `self.dpmge[sprite.name]` to flip those local nub coords (via the rotation transform at lines 593-603) to palette 3, and returns `False` immediately if `np.any(rurikqkuoc == 8)` for any sprite. Returns True only after every sprite passes.

`self.next_level()` is called from inside `step()` on lines 638 (after ACTION5 rotate) and 666 (after ACTION1-4 move) when `exlcvhdjsf()` returns True. **Win check is never run on click (ACTION6)** — clicking only changes selection and never moves a sprite.

Same predicate for L1, L2, L3.

## Lose condition

Plain English: lose if 150 actions are taken without the win predicate triggering.

Literal condition: at the top of `step()` (line 615), the step-counter HUD is updated; line 616-619 then check `self._action_count >= self.guweh` (150) and call `self.lose()` followed by `self.complete_action()` and return. So the very first action that pushes the count past 150 triggers the loss before any other branch runs.

There is no other lose path (no hazard sprite, no falling-off-grid penalty, no per-level budget shrinkage).

## Resource economy

- Depleting resource (energy / step counter / lives): YES — `self.guweh = 150` step budget per level, displayed by the `qdcvayjdkm` top-row HUD, decremented by 1 per action (engine increments `_action_count`), threshold for losing = 150.
- Accumulating resource (collected items, score, sequence progress): NO. There is no collected-items count, no score, no sequence progress. The only progress signal is the absence of palette-8 pixels.
- Lives mechanic (respawn cost): NO. A single `self.lose()` ends the game; there is no respawn or extra-life logic.
- Resource interaction with win/lose: the step counter is the sole lose trigger; the nub-overlap predicate is the sole win trigger. The two are independent — running out of steps cannot help you win, and an early win prematurely ends the level without using the remaining steps.

## Action-budget signature

- Default budget per level: 150 (`self.guweh = 150` in `__init__`, copied into `_step_counter_ui.mimisncrjk`).
- Whether budget tightens or shifts across levels 1-3: NO. Budget is reset to 150 at every `on_set_level`.
- Per-level vs. per-environment: per-level (`_action_count` is reset by the engine on level transition).
- Decrement rate per action: 1 per action (engine default; no override). Every action — click, move, rotate — costs 1.
- Refill mechanism: NONE. No refill in code.

## Notable code patterns / techniques

- **Palette-mark tab matching** (`gjhtwbvrel`): builds a dict keyed by `(world_x, world_y)` mapping to the list of `(sprite, local_x, local_y)` tuples that contribute palette-8 to that cell; whenever the list has length 2, both contributors get their local coord added to `self.dpmge[name]`, which gets repainted to palette 3 on the next render. This is a generic "find pixel-coincidences across overlapping sprites" pattern — useful any time a generated game wants two sprites to "click together" visually when their tab-cells align.
- **Selection highlighting via in-place pixel substitution** (`lceflskdhw`): on click, replace all non-8/non-3 pixels of the selected sprite with palette 0 (black), reverting on deselect. This is a click-feedback technique that doesn't require any additional sprite or layer. Inverse pattern in `pvrlqzlpjy`.
- **Per-sprite "original pixels" cache** (`self.npwwu`): every level start, the sprite's `pixels` array at that moment is copied and stored under its name. All subsequent overlay/highlight changes are done on copies, with `npwwu` as the reference for re-renders. This prevents accumulating recolour drift across many actions.
- **Rotation-aware coord remap** (lines 565-578 in `gjhtwbvrel`, 593-604 in `exlcvhdjsf`): given a local (x, y) overlap coord and the sprite's current rotation (0/90/180/270), compute the remapped (x', y') in the *unrotated* frame for read-back into `self.pixels`. Necessary because the engine rotates pixels at render time but `self.dpmge` keys are stored in *world* render coords.
- **`fubdf` action-gating flag**: a one-bit state machine that ensures clicks and movements alternate. After ACTION6 the next valid action set excludes ACTION6 (preventing "click click click" from soaking the budget without progressing). This pattern is a lightweight way to enforce "you must commit a movement after each selection".
- **`set_layer(4)` to raise the selected piece**: ensures the selected sprite renders on top of any overlapping neighbours, so its highlight is always visible.
- **`get_sprite_at(..., ignore_collidable=True)`**: lets clicks land on any sprite even when the sprite has `collidable=True`. This sidesteps the engine's default behaviour of treating collidables as opaque hit-testing surfaces.

## Anti-patterns / lessons

- **Two un-tagged sprites** (`ezhdijgxgn` and `kodeocvgpm`) miss the `sys_click` tag while their siblings have it. The game still selects them via `ignore_collidable=True`, but any cross-cut analysis that tries to enumerate clickable pieces by tag would miscount. Generated games should be uniform in tag application.
- **Identical-shape mirror sprites** (`kddtjradhp` vs `kodeocvgpm`) — same colour, same outline modulo chirality. Risks visual confusion if both ever appear in the same level.
- **Win predicate tied to per-sprite palette inspection rather than a global game state**: `exlcvhdjsf` re-renders every sprite from `npwwu` and checks for stray palette-8 — this is O(sprites × render_cost) per action. For a 20×20 grid with ≤ 5 sprites this is fine, but a generated game with more sprites would want a counter-based predicate.
- **Dual storage of "original pixels"** (`self.agupi` and `self.npwwu` both hold copies of `sprite.pixels` at level start) — the only difference in scope is that `agupi[name]` may be deleted on deselect while `npwwu[name]` stays. A generated game could collapse to a single dict.
- **L4+ "blanking" rendering branch** is interleaved into `lceflskdhw`, `pvrlqzlpjy`, `gjhtwbvrel`, `on_set_level` — not isolated to a single helper. Makes the L1-3 logic harder to read. Generated games should keep blanking/cosmetic-overlay logic out of the core mutation paths.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES (top row, columns 16-47, depleting horizontal bar).
- Has lives mechanic: NO.
- Has click-to-select (uses ACTION6): YES.
- Has tag-based grouping (uses `level.get_sprites_by_tag`): NO. The source uses `level.get_sprites()` and `level.get_sprite_at(..., ignore_collidable=True)`; no tag-based queries.
- Uses ACTION5 (modal): YES (rotate selected sprite 90°).
- Uses ACTION6 (click): YES.
- Uses ACTION7: NO.
- Has level data dicts (uses `level.get_data` / `level.set_data`): YES (`level.get_data("BackgroundColour")`).
- Multi-mechanic per level (vs. single mechanic per level): NO — all three levels use the same nub-pairing mechanic with click-select / move / rotate. Level differences are geometric (more pieces, more nubs per piece, balanced vs unbalanced graph), not mechanical additions.
- Tutorial level appears solvable by random play: UNKNOWN — L1 has only 2 pieces and 4 total nubs; with 150 random actions probability of reaching the target alignment is non-trivial but not high. Random would mostly burn the budget on misclicks and out-of-bounds bumps.
- Has a depleting resource: YES — step counter, 150 per level.
- Has an accumulating resource: NO.
- Sprite shape convention used: glyph (each sprite is a small irregular shape with peripheral nubs; mix of filled and hollow internal regions).
- HUD position: top.
- Palette size used: 11 distinct palette values appear across the sprite roster: {6, 7, 8, 10, 11, 12, 13, 14, 15} from sprite bodies plus {0, 4} drawn into the frame at runtime by selection-highlight and the HUD. So 11 in total.
- Background colour value: variable per level (10 in L1, 12 in L2, 15 in L3) — set via `level.get_data("BackgroundColour")`. Module constant `BACKGROUND_COLOR = 4` is overridden in `on_set_level` for every level whose data dict has the key.
- Padding / letter-box colour value: same as the per-level `BackgroundColour` (set on line 438), which is 10 / 12 / 15 for L1 / L2 / L3 respectively. Module constant `PADDING_COLOR = 4` is overridden.
- Number of distinct mechanics introduced across levels 1-3: 1 (the nub-pairing mechanic introduced in L1; L2 and L3 add more pieces and rotation pressure but no new mechanic).
- Number of levels documented: 3.

(End of file.)
