# sk48 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/sk48/41055498/sk48.py`
- Lines: 988
- Class name: `Sk48`
- available_actions: `[1, 2, 3, 4, 6, 7]` (UP/DOWN/LEFT/RIGHT, ACTION6 = click-to-switch-snake, ACTION7 = undo)
- Number of levels in source: 8
- Number of levels documented in this analysis: 3
- Imports: `NovaBaseGame`, `Camera`, `GameAction`, `Level`, `RenderableUserDisplay`, `Sprite` from `novaengine`; `from novaengine.enums import ActionInput`; `numpy as np`; `math`.

## Mechanic essence (one sentence)

Two coloured snake-heads lie at opposite ends of a tiled floor with their bodies stretched out across coloured floor-tiles, and the player's UP/DOWN/LEFT/RIGHT keys grow or retract the active snake one segment at a time (perpendicular keys shimmy the whole body sideways past an anchor stone) until every segment of one snake covers a tile whose colour matches the corresponding segment-tile of the other snake.

## Sprite roster

| sprite (obfuscated) | dims | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| `ejlpqgojjt` | 6x6 | 4, 6, -1 | epdquznwmq | 2 | YES | (default) | YES | orange snake-head with 4-coloured eye recess |
| `elmjchdqcn` | 6x6 | 8, -2 | elmjchdqcn | 2 | YES | (default) | YES | floor tile (palette-8 default; gets `color_remap`-ed to 14, 9, 8, 12 per placement) |
| `hspquzcixt` | 1x1 | 4 | (default) | -1 | YES | (default) | YES | single palette-4 cell scaled 64x to draw a wide horizontal floor band below row 53 |
| `irkeobngyh` | 2x8 | 2, 3 | irkeobngyh | -1 | YES | (default) | YES | side-anchor stone (palette-2 caps + palette-3 middle); enables perpendicular sideways shimmy |
| `jjkoyaqhkh` | 11x12 | 5, -1 | (default) | -2 | YES | (default) | YES | hollow palette-5 frame (defined but never placed in any level) |
| `jvsnmrqbrb` | 6x6 | 4 | jtteddgeyl | -1 | YES | (default) | YES | floor tile palette-4 (defined but never placed) |
| `kevthtkmzm` | 4x4 | 0, -2 | (default) | 2 | YES | (default) | YES | match-checkmark overlay — 2x2 palette-0 inside a -2 transparent ring; used to mark a segment as colour-matching its twin |
| `ksixfnredk` | 7x7 | 4 | jtteddgeyl | -1 | YES | (default) | YES | square palette-4 base scaled 6x → renders as a 42x42 floor field |
| `mkgqjopcjn` | 6x6 | 5 | mkgqjopcjn | (default) | YES | (default) | YES | mid-grey wall (level 5+ only) |
| `pkzxknabii` | 6x6 | 8, -1, -2 | (default) | 3 | YES | (default) | YES | dashed-edge palette-8 frame with hollow centre (defined but never placed) |
| `qtjqovumxf` | 6x6 | 2, 3, -2 | qtjqovumxf | (default) | YES | (default) | YES | snake-body segment — alternating palette-2/palette-3 stripe pattern over -2 transparent borders |
| `rtwdndlhdf` | 5x5 | 4 | jtteddgeyl | -1 | YES (false) | (default) | YES | smaller palette-4 floor tile (collidable=False); scaled 6x in L1 (=30x30 floor band) |
| `udbuodqlxv` | 6x6 | 4, 15, -1 | epdquznwmq | 2 | YES | (default) | YES | white snake-head (level 6+) |
| `xtuqlbebvk` | 6x6 | 5, 10, -1 | epdquznwmq | 2 | YES | (default) | YES | grey snake-head with cyan eye (level 4+) |
| `yukipuenar` | 64x1 | 3 | (default) | -1 | YES | (default) | YES | horizontal palette-3 line at y=53 — placed at level start, removed in `on_set_level` (line 638) |
| `zkekdulqku` | 6x6 | 5, 11, -1 | epdquznwmq | 2 | YES | (default) | YES | grey snake-head with yellow eye |

### `ejlpqgojjt` — orange snake-head
- Pixel pattern: 6x6 outer ring of palette-6 (magenta-orange); inner 4x4 of palette-4 with a 2x2 hole of palette-6 in the dead centre. Reads as an orange-frame square with a coloured cabochon in the middle.
- Where it appears: every L1-3 level (always 2 copies — one above row 53, one below).
- Role: snake-head — the entity the player controls. Its rotation determines the body chain direction (`hhvuoijeua[rotation]` maps 0→(1,0), 90→(0,1), 180→(-1,0), 270→(0,-1)). Its position is the start of the body chain; following segments are at +6-pixel multiples of the rotation direction.
- Visual-vs-functional read: at-rendered-scale, orange picture-frame square. Layer 2 means it renders above body segments. Tag `epdquznwmq` (snake-head tag) is shared with the other 3 head variants. Centre pixel `pixels[2, 2]` = palette-6, used for pairing — every head finds its twin by matching centre pixel.
  - At-rendered-scale shape: filled square-with-cabochon.
  - Palette signature: 4 + 6. Palette 6 also appears in itself only (unique among heads).
  - Nearest-other-sprite check: `udbuodqlxv` (white version, palette 4 + 15), `xtuqlbebvk` (grey-cyan, 5 + 10), `zkekdulqku` (grey-yellow, 5 + 11) — same shape, different palette.
- Visual contrast notes: against palette-5 background, orange-6 is loud and unmistakable. The cabochon centre is the player's directional indicator for which-snake-am-I.

### `elmjchdqcn` — coloured floor target tile
- Pixel pattern: 6x6 with -2 transparent border (4-cell-thick? No — the 6x6 has -2 in row 0, row 5, col 0, col 5; interior 4x4 is palette-8). The palette-8 is recoloured per placement via `color_remap(None, X)` to 8/9/12/14 etc.
- Where it appears: every L1-3 level — multiple copies per level. Always paired in two rows: an "upper" row (y < 53) and a "lower" row (y ≥ 53), so each snake's segments align with a colour-row.
- Role: target tile that records a colour value. The win predicate compares the colour of each upper-row tile under one snake's segment with the colour of the corresponding lower-row tile under the other snake's segment; when they match, the segment "fits".
- Visual-vs-functional read: at-rendered-scale, a coloured 4x4 square (with 1-pixel transparent border) — looks like a flat coloured floor tile. Tag `elmjchdqcn` distinguishes from snake-bodies. The colour is the *only* identifier — two tiles with the same colour are interchangeable from the win-predicate's perspective.
  - At-rendered-scale shape: filled small square (4x4 inside 6x6).
  - Palette signature: 8/9/12/14 (recoloured per placement). Each placement uses one of these.
  - Nearest-other-sprite check: only itself; tag-distinguished.
- Visual contrast notes: against palette-5 background and palette-4 floor-band, the bright colours (8 = orange, 9 = blue, 12 = purple, 14 = green) stand out as game-relevant tiles.

### `hspquzcixt` — wide floor band scaled 64x
- Pixel pattern: 1x1 of palette-4. Placed at (0, 54) and `set_scale(64)`.
- Where it appears: every L1-3 level (1 copy at (0, 54)).
- Role: visually marks the floor area BELOW row 53 (the lower snake's territory). It's a layer -1 sprite covering the entire bottom strip.
- Visual-vs-functional read: at-rendered-scale, a 64x1 cell scaled 64x renders as 64 pixels wide × 64 pixels tall (the scale extends both dims). Actually, `set_scale(64)` typically scales both x and y by 64x; placed at (0, 54) it covers (0, 54) to (64, 118) — but the frame is only 64x64 so the visible portion is (0, 54) to (64, 64) = the bottom 10 rows.

  Actually the scale logic in novaengine: `set_scale(N)` repeats each pixel N times in both directions. So `1x1 * 64 = 64x64` placed at (0, 54) clips to rows 54..63 (the bottom 10 rows) — which is the lower-snake floor.
- Visual contrast notes: solid palette-4 (off-grey) covers the bottom 10 rows.

### `irkeobngyh` — anchor stone
- Pixel pattern: 2x8. Top 2 rows of palette-2; middle 4 rows of palette-3; bottom 2 rows of palette-2. Reads as a vertical capsule.
- Where it appears: every L1-3 level — multiple copies (4 in L1 at (13, 32), (13, 26), (13, 20), (13, 14); 6 in L2 and L3 at (7, 38..8) in 6-pixel steps).
- Role: side-anchor that enables the snake to do a "perpendicular shimmy". When the player presses a perpendicular direction relative to the snake's facing, the source checks if there's an `irkeobngyh` at the cell in front of the segment-1 (the segment after the head); if so, ALL segments translate sideways by 6 pixels. This is how the snake "snakes around corners" without growing or shrinking.
- Visual-vs-functional read: at-rendered-scale, a tall thin vertical line — palette-2 caps with palette-3 in the middle, repeated vertically along x=13 or x=7. Reads visually as a "rail" or "track-marker". Tag `irkeobngyh` is the same as the sprite name (a code-smell — usually tag and name differ).
- Visual contrast notes: palette-3 + palette-2 against palette-5 background reads as a faint dark column.

### `jjkoyaqhkh` — hollow 11x12 frame (defined but never placed)
- Pixel pattern: 11x12 with palette-5 outer 2-cell ring; interior 7x6 transparent.
- Where it appears: never placed in any level.
- Role: dead sprite.
- Visual-vs-functional read: hollow rectangular frame; palette 5.

### `jvsnmrqbrb` — small floor tile (defined but never placed)
- Pixel pattern: 6x6 solid palette-4.
- Where it appears: never placed.
- Role: dead sprite (likely intended for a future floor variant).

### `kevthtkmzm` — match-checkmark overlay
- Pixel pattern: 4x4 with -2 transparent border and a 2x2 palette-0 (black) centre.
- Where it appears: spawned at runtime in `on_set_level` (line 670-672) — for each twin head's segment 1+, a `kevthtkmzm` clone is spawned at `(segment.x + 1, segment.y + 1)` with `set_visible(False)`. There are `len(self.mwfajkguqx[twin]) - 1` checkmark overlays per twin.
- Role: visual indicator showing "this segment's colour matches the corresponding twin segment's colour". Toggled visible by `gvtmoopqgy()` in real-time as the player moves the snake.
- Visual-vs-functional read: at-rendered-scale, a 2x2 black dot at the centre of a body segment. Palette 0 is unique to this overlay. When invisible, the segment looks normal; when visible, a black dot appears in the middle.
- Visual contrast notes: black against the dotted-grey body segment is high-contrast — clear feedback.

### `ksixfnredk` — 7x7 floor base scaled 6x
- Pixel pattern: 7x7 solid palette-4. With `set_scale(6)` at level start, becomes 42x42 visible.
- Where it appears: L2, L3 (1 copy each at (11, 6)). Also L4-8.
- Role: large palette-4 floor field underneath the snakes' play area. Tag `jtteddgeyl` is queried to find "the floor sprite" via `self.lqwkgffeb = self.current_level.get_sprites_by_tag("jtteddgeyl")[0]`. The floor's bounding box determines movement bounds (`qzvlbxkjgk` rejects moves outside).
- Visual-vs-functional read: large flat palette-4 area; same colour as `hspquzcixt` (64-wide band) so they blend visually.

### `mkgqjopcjn` — wall (level 5+)
- Pixel pattern: 6x6 solid palette-5.
- Where it appears: not placed in L1-3.
- Role: out of scope.

### `pkzxknabii` — dashed-edge palette-8 frame (defined but never placed)
- Pixel pattern: 6x6 with palette-8 dashed top+bottom rows, -1 transparent middle, -2 sides.
- Where it appears: never placed.
- Role: dead sprite.

### `qtjqovumxf` — snake-body segment
- Pixel pattern: 6x6 with -2 transparent in top 2 rows and bottom 2 rows; middle 2 rows alternate palette-3/2 stripe `[[3, 2, 2, 3, 2, 2], [2, 2, 3, 2, 2, 3]]`. Reads as a thin horizontal striped band centred vertically.
- Where it appears: every L1-3 level — many copies (one per body segment per snake). Heads attach segments dynamically at level start by walking from the head's position outward.
- Role: snake body segment. Width 6 matches the head's stride. When the snake rotates 90°, the segment also rotates so the stripe becomes vertical. Layer 1 if rotation is 0/180 (horizontal), 0 if rotation is 90/270 (vertical) — this layering ensures horizontal segments render above vertical segments at intersections.
- Visual-vs-functional read: at-rendered-scale, a thin striped 6x6 cell. The stripe colours change on snake selection: the active snake's body has palette-1 (yellow) and palette-2 substitutes; the inactive has palette-3 (grey) and palette-2 — see `crbbymputr` for the recolouring logic. Player tells active vs inactive snake apart by stripe colour.
  - At-rendered-scale shape: dotted/striped horizontal band.
  - Palette signature: 2 + 3 default, recoloured to 1 + 2 when active.
  - Nearest-other-sprite check: only itself; tag-distinguished.

### `rtwdndlhdf` — 5x5 floor tile
- Pixel pattern: 5x5 solid palette-4.
- Where it appears: L1 only (1 copy at (17, 12) with `set_scale(6)` → 30x30 visible).
- Role: floor base for L1's lower-snake area.

### `udbuodqlxv` — white snake-head (level 6+)
- Pixel pattern: 6x6 with palette-15 outer ring, palette-4 inner ring, palette-15 cabochon centre.
- Where it appears: not placed in L1-3.
- Role: out of scope.

### `xtuqlbebvk` — grey-cyan snake-head (level 4+)
- Pixel pattern: 6x6 with palette-5 outer ring, palette-10 cabochon centre.
- Where it appears: not placed in L1-3.

### `yukipuenar` — y=53 horizontal divider (removed at level start)
- Pixel pattern: 64x1 of palette-3.
- Where it appears: every L1-3 level (1 copy at (0, 53)) — but `on_set_level` line 638 immediately removes it: `self.current_level.remove_sprite(self.current_level.get_sprites_by_name("yukipuenar")[0])`.
- Role: ghost sprite — only visible during level loading. The constant `fzjeqdahvs = 53` is the row threshold for distinguishing upper-snake from lower-snake. The sprite is placed and then deleted; its only purpose may be to sanity-check the level layout at design time.
- Visual-vs-functional read: invisible at runtime (removed before render). Defined for code clarity / level-design consistency.

### `zkekdulqku` — grey-yellow snake-head (L3)
- Pixel pattern: 6x6 with palette-5 outer ring, palette-11 cabochon.
- Where it appears: L3 (1 copy at (29, 0) with `set_rotation(90)`), L4 (1 copy).
- Role: a head with rotation 90° (vertical chain). Its centre pixel is palette-11. With no other head sharing palette-11 in L3, this snake has NO twin — meaning its segments are not subject to the colour-match win check.

  Wait — re-reading the `xpmcmtbcv` building logic: the loop `for bcwsrdcswp in uiomqroshp: if bcwsrdcswp.y < fzjeqdahvs:` — the `zkekdulqku` is at y=0 < 53, so it IS iterated for pairing. But its twin lookup `next((b for b in uiomqroshp if b != bcwsrdcswp and b.pixels[2, 2] == bcwsrdcswp.pixels[2, 2]), None)` returns None if no match. So `xpmcmtbcv[zkekdulqku] = None` (actually `if pphvqzjirf:` skips when None, so the entry is never set).

  So `zkekdulqku` at L3 is a snake that's controllable but doesn't contribute to the win predicate. This is unusual.

  Actually re-reading: line 654-663 builds `mwfajkguqx[head]` for ALL heads regardless of `xpmcmtbcv` status. So the `zkekdulqku` head has a body chain too. It's selectable via click but doesn't affect win.
- Visual-vs-functional read: same shape as `ejlpqgojjt` but palette 5 + 11 (grey + yellow) instead of 4 + 6 (palette + orange). Distinct cabochon colour.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (64, 64)
- Number of sprites placed: 21.
- Composition by role: 2 heads (`ejlpqgojjt` × 2 — twin pair), 6 floor target tiles (`elmjchdqcn` × 6, recoloured), 1 wide floor band (`hspquzcixt`), 4 anchor stones (`irkeobngyh` × 4 vertically stacked at (13, 14..32)), 6 body segments (`qtjqovumxf` × 6), 1 floor base (`rtwdndlhdf` scaled 6x), 1 divider line (`yukipuenar`, removed).
- Level data: `{"grouped_pauses": False, "lit_extension": True}`.
- Spawn position(s): no avatar; `vzvypfsnt` (active snake) is set to `uiomqroshp[0]` (first head in tag-order).
- Per-cell layout: upper snake at (11, 36) with body segment at (17, 36); 3 target tiles at (41, 30) palette-14, (41, 24) palette-9, (41, 18) palette-8 — but wait these are at x=41 which is far from the snake's initial body. So the upper snake must extend to reach them.

  Lower snake at (20, 56) with body segments at (26, 56), (32, 56), (38, 56). 3 lower target tiles at (26, 56) (default palette-8), (32, 56) palette-14, (38, 56) palette-9.
- Mechanic introduced relative to the previous level: this is the first level — introduces the **paired-snake colour-matching** mechanic. Two snakes share the same head-colour and centre-pixel signature; one lives in the upper region (y<53), one in the lower (y≥53). Each snake has a body of segments. The upper snake is on a horizontal column of target tiles (y=18, 24, 30) at x=41; the lower snake is on a horizontal row of target tiles (x=26..38) at y=56.

  Wait — the upper snake's body extends RIGHT (rotation 0) starting at (11, 36). So segments are at (11, 36), (17, 36), (23, 36), (29, 36)... up to wherever the chain terminates at level start. In the level data, `qtjqovumxf` is placed at (17, 36) and (11, 36) — so the chain has 2 segments: head at (11, 36), seg1 at (11, 36), seg2 at (17, 36). The chain terminates because no qtjqovumxf is placed at (23, 36).

  Wait actually — looking more carefully — the head is at (11, 36) AND a segment is at (11, 36). The level layout has overlapping positions. The chain-building code (`while kohhdjrfgt is not None`) starts at the head's position and walks +6 cells until no `qtjqovumxf` is found. So segments at (11, 36), (17, 36) → 2 segments.

  The 3 upper target tiles at (41, 18), (41, 24), (41, 30) are in a vertical column at x=41. The upper snake's body is at y=36 — different row. So the snake has to grow UP (rotate 270 to face up, then grow) to reach those tiles. But the snake has rotation 0, which is RIGHT. The 4 anchor stones at (13, 14..32) form a column at x=13 — they're left of the snake.

  Hmm, this is more complex than I first thought. The `irkeobngyh` anchor stones at x=13 don't help the snake reach the (41, _) tiles.

  Re-reading the perpendicular shimmy logic (line 772): `elif self.current_level.get_sprite_at(bcwsrdcswp.x + 2 + dx // 2, bcwsrdcswp.y + 2 + dy // 2, "irkeobngyh"):` — the anchor needs to be at offset (+2 + dx/2, +2 + dy/2) from the head. For UP press (dx=0, dy=-1, multiplied by 6 → dx_actual=0, dy_actual=-6), the anchor must be at (head.x+2, head.y+2-3) = (head.x+2, head.y-1). At head=(11, 36), that's (13, 35). The anchor at (13, 32) is NOT at exactly (13, 35) but is the closest one. The snake might not be able to shimmy up directly; it might need to shrink toward x=13 first, then shimmy.

  Actually the snake is at y=36, anchors are at y=14, 20, 26, 32. So shimmy from y=36 → y=30 would require an anchor at (13, 35); none at that exact position. But maybe the offset is slightly different, or the snake needs to be moved first.

  Honestly the exact L1 solution path is hard to derive from a static reading. The key insight is: snake grows/shrinks/shimmies on a 6-pixel grid; player must reposition both snakes so their segment-tile colours match in pairs.
- Specific challenge: align the upper and lower snake bodies so that segment-by-segment, the underlying tile-colour matches. Upper snake currently lies on (11, 36) and (17, 36) where there are no target tiles → those segments have no `vjfbwggsd` entry → 0 matches → puzzle unsolved. Player must navigate the snake to the targets at (41, 18..30).
- Estimated optimal action count: ~30-50 (multiple grow/shrink/shimmy operations to relocate the upper snake).

### Level 2
- `grid_size`: (64, 64)
- Number of sprites placed: 26.
- Composition: 2 heads (`ejlpqgojjt` × 2), 7 target tiles (`elmjchdqcn` × 7, palette 8/9/12/14), 1 wide floor band, 6 anchor stones (column at x=7), 7 body segments, 1 large floor base (`ksixfnredk` scaled 6x), 1 divider.
- Level data: `{"grouped_pauses": False, "lit_extension": True}`.
- Spawn position(s): upper snake at (5, 42), lower at (17, 56). Both rotation 0.
- Per-cell layout: upper snake bodies at (5, 42) and (11, 42). Upper targets at (29, 24), (35, 24), (41, 24), (47, 24) (palette 14, 9, 12, 8) — a horizontal row at y=24. Lower snake at (17, 56) extends right; lower targets at (23, 56), (29, 56), (35, 56), (41, 56).
- Mechanic introduced relative to L1: same mechanic, more segments per snake, more colour variety in target tiles. No new mechanic introduced.
- Specific challenge: the upper snake must reach the y=24 row (12 cells up from y=36, then 6 more to y=24 — actually y=42 to y=24 is 18 pixels = 3 shimmies). 6 anchor stones are placed in a column at x=7, providing shimmy points. Player must shimmy + grow + shimmy to align the snake.
- Estimated optimal action count: ~40-60.

### Level 3
- `grid_size`: (64, 64)
- Number of sprites placed: 32.
- Composition: 2 head twins (`ejlpqgojjt` × 2) + 1 unpaired head (`zkekdulqku` × 1 at top), 7 target tiles, 1 wide band, 6 anchor stones, 8+ body segments (some with rotation 90), 1 large floor base, 1 divider.
- Level data: `{"grouped_pauses": False, "lit_extension": True}`.
- Spawn position(s): upper snake at (5, 42), lower at (17, 56). Plus a vertically-rotated snake `zkekdulqku` at (29, 0) with rotation 90.
- Per-cell layout: upper twin snake at (5, 42); lower twin at (17, 56); a third snake (vertical) at (29, 0..24) with rotation 90 and segments at y=0, 6, 12, 18, 24. Targets at upper column (29, 6, 12, 18, 24) — wait some of these are vertical-tile-targets. Actually the targets at y=6, 12, 18, 24 with x=29 form a vertical column for the vertical snake.
- Mechanic introduced relative to L2: **Vertical snake** (rotation 90 head + vertical body). Plus a third unpaired head (`zkekdulqku` at top) that introduces a 3-snake selection challenge. Click can target any of 3 heads; the player must remember which is which and which two pair up.
- Specific challenge: identify the twin-pair (the two `ejlpqgojjt` are twins), align them, and ignore the unpaired vertical `zkekdulqku` (which doesn't contribute to the win).
- Estimated optimal action count: ~50-70.

Levels 4 through 8 exist but are excluded per skill scope.

## Action handlers

### ACTION1 / ACTION2 / ACTION3 / ACTION4 (UP / DOWN / LEFT / RIGHT)
- Trigger: `self.action.id in [GameAction.ACTION1, ACTION2, ACTION3, ACTION4]`.
- Branches inside `step()`: first the win-animation guard (`self.lgdrixfno >= 0`), the post-animation cleanup guard (`self.ljprkjlji or self.pzzwlsmdt`), and the click guard. If none match, dispatch to `self.hgivzuhjvj()` which handles all four directional actions:
  - Decrement `self.qiercdohl` by 1.
  - Compute (move_x, move_y) from action ID via `ghcqtpzzlq`.
  - Compute (dx, dy) = (move_x * 6, move_y * 6).
  - Get the active snake `self.vzvypfsnt` and its rotation-direction (base_dir_x, base_dir_y).
  - **Branch A: move parallel to facing direction** ((move_x, move_y) == (base_dir_x, base_dir_y)). Try to grow the snake by 1: check `qzvlbxkjgk(last_segment, move_x, move_y)` returns False (i.e. last segment can move forward); if so, advance every segment by (dx, dy) using `bnrdrdiakd` (which handles cascading collisions); add a new segment at the head's old position; insert into the chain.
  - **Branch B: move opposite to facing** ((move_x, move_y) == (-base_dir_x, -base_dir_y)). Retract: pop the first segment (`hadfnehqh = mwfajkguqx[active].pop(0)`), shift remaining segments back by (dx, dy).
  - **Branch C: perpendicular shimmy** — check if there's an `irkeobngyh` anchor at `(active.x + 2 + dx//2, active.y + 2 + dy//2)`. If so, call `bnrdrdiakd` on every segment in the active snake's body to move them all by (dx, dy). The anchor itself doesn't move — it's just the gate that enables sideways shift.
  - **Otherwise**: no-op.
  - For any segments newly off-floor (`pzzwlsmdt`) update overlay sprites (`rztawzist`) to show "this segment falls off".
  - For any moved sprites in `ruqrmvdjrq`, queue them in `self.ljprkjlji` for one-step incremental motion via `xqkpzztujs` (`sprite.move(3 * sign(dx), 3 * sign(dy))` — moves at half-step granularity for smoother animation).
- After motion, `gvtmoopqgy()` recomputes the colour-match and sets checkmark visibilities. If win predicate holds, set `lgdrixfno = 0` to start the win animation.
- State mutations: read `self.vzvypfsnt`, `self.mwfajkguqx`, `self.qiercdohl`. Written: `self.qiercdohl`, every segment's position, possibly new segments added, `self.ljprkjlji` queue, `self.pzzwlsmdt` (fall-off list), `self.rztawzist` (overlay sprites), `self.vjfbwggsd` (matches), `self.jdojcthkf[twin]` checkmark visibilities.
- Side effects on sprites: segments move; new `qtjqovumxf` segments may be added; `kevthtkmzm` overlays toggle visibility; `pkzxknabii` overlays may be added for falling-off segments.
- Engine effects: `next_level()` after win animation completes (35 ticks); `lose()` when `qiercdohl == 0`.
- Pre-conditions / gating: parallel-grow rejected if last segment can't advance; opposite-retract rejected if the snake is already 1-segment; perpendicular shimmy rejected if no anchor at the required offset.

### ACTION6 (click — switch active snake)
- Trigger: `self.action.id == GameAction.ACTION6`.
- Branches: read (x, y) from `action.data`; call `current_level.get_sprite_at(x, y, "sys_click")`. If the hit sprite is one of the head pairs (master or twin) AND it's not already the active snake, call `crbbymputr(master)` to switch active snake to that pair's master. Set `self.xsoixcero = True` (a flag that gates `_get_valid_actions` to return only directional actions until next non-click action — preventing rapid-fire clicks).
- State mutations: `self.vzvypfsnt`, `self.xsoixcero`, every old-active and new-active snake's body recoloured.
- Side effects on sprites: every segment of old active snake's body gets `color_remap(czlzuqtdgl, ewudeezseq)` and `color_remap(bkkcgooxqm, yykihaekwn)` (deactivation); new active snake's body gets opposite recolour.
- Engine effects: none.
- Pre-conditions / gating: silent no-op if click misses any sys_click sprite.

### ACTION7 (undo)
- Trigger: `self.action.id == GameAction.ACTION7`.
- Branches: dispatch to `uqclctlhyh()` which pops the most recent snapshot from `self.seghobzez` (the undo stack) and restores every snake's segment positions. Snapshot was pushed at the end of every action via `nixwuekdfm()`.
- State mutations: every snake's segment positions, segment count.
- Side effects on sprites: removes all current segments and re-adds at snapshot positions.
- Engine effects: none.
- Pre-conditions / gating: silent no-op if undo stack has only 1 entry (initial snapshot).

## HUD widgets

### `wrlppxgbeu` — single-row depleting step bar at row 53
- Class name (obfuscated): `wrlppxgbeu`.
- Render-pixel range: row 53 (the threshold `fzjeqdahvs = 53` — the same row that separates upper and lower snake territories).
- What value it displays: `self.qiercdohl / self.vhzjwcpmk` — proportion of step budget remaining (initial budget 196).
- Visual style: row 53 is filled with palette-3 (depleted background), then overwritten with palette-2 for the leading `qulghingmq = ceil(64 * remaining/total)` cells. The palette-2 portion shrinks from the right edge as steps deplete.
- Update points: every render frame; `qiercdohl` is decremented in `hgivzuhjvj` per directional action.
- Where it is registered: instantiated in `__init__` as `interfaces=[wrlppxgbeu(self)]` in `Camera`.

## Internal state — exhaustive

| attr (obfuscated) | semantic name | type | initial value | written by | read by | role |
|---|---|---|---|---|---|---|
| `vhzjwcpmk` | max_step_budget | int | 196 | `on_set_level` | `step`, HUD | denominator of step ratio |
| `qiercdohl` | remaining_steps | int | 196 | `on_set_level`, `hgivzuhjvj` | `step`, HUD, `_get_hidden_state` | step counter |
| `mwfajkguqx` | head_to_segments | `dict[Sprite, list[Sprite]]` | `{}` | `on_set_level`, `hgivzuhjvj`, `uqclctlhyh` | many | maps each head (snake) to its ordered list of body segments |
| `vjfbwggsd` | head_to_segment_tiles | `dict[Sprite, list[Sprite]]` | `{}` | `on_set_level`, `gvtmoopqgy` | `gvtmoopqgy`, `step` (win animation) | maps each head to the list of `elmjchdqcn` target tiles under each of its segments (None if no tile under that cell) |
| `vbelzuaian` | all_target_tiles | `list[Sprite]` | (from level) | `on_set_level` | `ebribtrdgw`, `nixwuekdfm` | all `elmjchdqcn`-tagged target tiles |
| `xpmcmtbcv` | head_to_twin | `dict[Sprite, Sprite]` | `{}` | `on_set_level` | `step`, `gvtmoopqgy`, `crbbymputr`, `_get_valid_actions` | maps each upper head to its lower twin (matching by centre-pixel colour) |
| `vzvypfsnt` | active_head | `Sprite` | `uiomqroshp[0]` | `on_set_level`, `crbbymputr` | many | the currently-selected snake; arrow keys act on this snake |
| `jdojcthkf` | twin_to_checkmarks | `dict[Sprite, list[Sprite]]` | `{}` | `on_set_level`, `gvtmoopqgy` | `gvtmoopqgy`, `step` | overlay sprites (`kevthtkmzm`) per twin showing colour-match status |
| `lqwkgffeb` | floor_base_sprite | `Sprite` | (from level) | `on_set_level` | `qzvlbxkjgk` | the `jtteddgeyl`-tagged floor sprite; defines movement bounds |
| `ljprkjlji` | pending_moves | `list[tuple[Sprite, tuple[int, int]]]` | `[]` | `on_set_level`, `hgivzuhjvj` | `step`, `xqkpzztujs` | sub-step animation queue: list of (sprite, target_position) for sprites that are mid-move |
| `hadfnehqh` | retraction_segment | `Sprite \| None` | None | `on_set_level`, `hgivzuhjvj` | `step` (cleanup) | the segment popped during retraction; held until animation completes |
| `lgdrixfno` | win_animation_tick | int | -1 | `on_set_level`, `step`, `gvtmoopqgy` | `step` | -1 = idle; 0..34 = win-animation flash tick |
| `yzyidartf` | flash_segments | `list[tuple[Sprite, int]]` | `[]` | `on_set_level`, `step` | `step` | (sprite, original_palette) pairs for the win-animation colour flash |
| `xsoixcero` | post_click_lock_flag | bool | False | `on_set_level`, `step` | `step`, `_get_valid_actions` | True after a click to gate the next action set to directional only |
| `seghobzez` | undo_stack | `list[list[tuple[Sprite, int, int, int]]]` | `[]` | `on_set_level`, `nixwuekdfm`, `uqclctlhyh` | `uqclctlhyh` | list of full-state snapshots for undo (each entry is a list of (sprite, x, y, segment_count)) |
| `rztawzist` | fall_off_overlays | `list[Sprite]` | `[]` | `on_set_level`, `bnrdrdiakd` | `step`, `hgivzuhjvj`, `bnrdrdiakd` | overlay sprites (`pkzxknabii`) shown when a segment falls off the grid |
| `pzzwlsmdt` | falling_segments | `list[Sprite]` | `[]` | `on_set_level`, `bnrdrdiakd` | `step`, `hgivzuhjvj` | segments queued to "fall off" the grid this step |

## Win condition

Plain English: the level wins when, for every twin head pair, every segment of the master snake's body is on a target tile of the same colour as the corresponding segment of the twin's body.

Literal condition: `self.gvtmoopqgy()` (lines 822-839) returns True when, for every (master, twin) pair in `self.xpmcmtbcv`:
- For every i from 0 to len(master_segments)-1:
  - master's segment i has a target tile underneath (`vjfbwggsd[master][i]` exists)
  - twin's segment i has a target tile underneath
  - both tiles have the same `pixels[1, 1]` (their core colour)

`gvtmoopqgy` returns True iff all checks pass (`nuikqmprbq`).

Called from `step()` after every directional action (line 711). On True, sets `lgdrixfno = 0` to start the 35-tick flash animation; at tick 35, calls `next_level()` (line 696).

Same predicate for L1, L2, L3.

## Lose condition

Plain English: lose if the step counter reaches 0 with the puzzle unsolved.

Literal condition: at lines 723-724 in `step()`:
```python
if self.qiercdohl == 0:
    self.lose()
```

(Or at line 744-745 for the same check after non-animation branches.)

There is no other lose path.

## Resource economy

- Depleting resource: YES — `qiercdohl` step counter (initial 196), displayed as the row-53 depleting bar. Decremented by 1 per directional action (UP/DOWN/LEFT/RIGHT). Click (ACTION6) and undo (ACTION7) do NOT decrement (they're handled by separate branches that don't call `hgivzuhjvj`).
- Accumulating resource: YES — `vjfbwggsd` accumulates per-segment match counts; `gvtmoopqgy` returns True iff all match. The match-count per head is the implicit progress counter.
- Lives mechanic: NO. Single `lose()` ends the game.
- Resource interaction with win/lose: step counter is the sole lose trigger; full-match is the sole win trigger. Independent.

## Action-budget signature

- Default budget per level: 196 (`self.vhzjwcpmk = 196` in `on_set_level`).
- Whether budget tightens or shifts across levels 1-3: NO — same 196 each level.
- Per-level vs. per-environment: per-level (reset in `on_set_level`).
- Decrement rate per action: 1 per directional action (UP/DOWN/LEFT/RIGHT). 0 per click (ACTION6) and undo (ACTION7) — these are "free" actions.
- Refill mechanism: NONE.

## Notable code patterns / techniques

- **Snake as head + segment-list**: `mwfajkguqx[head]` stores the ordered body. Grow = insert at index 0; retract = pop from index 0; perpendicular shimmy = move all in sync. Clean linked-list-as-Python-list pattern.
- **Centre-pixel head pairing** (`xpmcmtbcv`): builds head-twin pairs by matching the centre pixel `pixels[2, 2]` of each head sprite. Generalises to any number of head colours without hard-coded names.
- **Anchor-gated perpendicular shimmy**: `irkeobngyh` sprite at a specific offset enables sideways translation. Without an anchor, the player can only grow/retract.
- **6-pixel grid stride** (`udenqlsrfq = 6`): every position and offset is a multiple of 6. The 64x64 frame supports a ~10-cell logical grid.
- **Layer-by-orientation segment rendering** (line 660, 765, 867): horizontal segments get layer 1; vertical get layer 0. This ensures crossings render with horizontal-on-top.
- **Active-snake recolour via dual `color_remap`** (`crbbymputr`): when switching active snake, recolour segments via `color_remap(palette_a, palette_b)` for inactive→active and the inverse for active→inactive. The palette-set is dual: {1, 2} active, {2, 3} inactive — palette 2 is shared.
- **Undo stack via state snapshots** (`seghobzez` + `nixwuekdfm`): every action pushes a list of (sprite, x, y, segment_count) tuples; ACTION7 pops and restores. Pure positional state — no need to track diffs.
- **Sub-step animation queue** (`ljprkjlji`): instead of moving sprites in one step, queue (sprite, target_pos) tuples and advance them by half-pixel via `xqkpzztujs`. Produces smoother visual transitions.
- **`xsoixcero` post-click lock**: prevents the player from clicking multiple snakes in rapid succession; the next action after a click MUST be a directional move.
- **`_get_valid_actions` returns click-data per head** (lines 980-987): provides explicit `(x+2, y+2)` click targets per head so an LLM agent can issue ACTION6 at a known-valid centre cell.

## Anti-patterns / lessons

- **Sprite name == tag name** (`irkeobngyh`, `mkgqjopcjn`, `qtjqovumxf`, `elmjchdqcn`) — same identifier used for both. A generated game should pick distinct identifiers to avoid confusion.
- **5 dead/unused sprites** (`jjkoyaqhkh`, `jvsnmrqbrb`, `pkzxknabii` defined but mostly unused for L1-3) — cluttered library.
- **`yukipuenar` placed at level start then immediately removed** — wastes a sprite definition. Should be a comment or constant instead.
- **Unpaired heads at L3** (the vertical `zkekdulqku`) — controllable but irrelevant to the win predicate. Confusing for the player. A 3-level generated game should ensure every head is paired and contributes to win.
- **Two grids (6-pixel stride and underlying 1-pixel)** — animation logic uses half-pixel `move(3, 3)` calls that operate on an even finer grid. Generated games could simplify to single-grid stride.
- **`self.xsoixcero` flag-gated valid_actions** is an implicit state-machine layered over the action dispatch — easy to break with a single off-by-one.
- **`get_sprites_by_name("qtjqovumxf")` in `pptqisyill`** does an O(N) linear scan per call; called many times during `bnrdrdiakd` recursion. For 3-level games this is fine, but a generated game should cache.
- **Missing tag on heads at level start** — `on_set_level` line 645 appends `"sys_click"` to head tags AT RUNTIME unless the name starts with `"wallBase"`. This mutates sprites and accumulates duplicates if `on_set_level` is called more than once per game.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES (single row at y=53, depleting bar).
- Has lives mechanic: NO.
- Has click-to-select (uses ACTION6): YES (click switches active snake among twin pairs).
- Has tag-based grouping (uses `level.get_sprites_by_tag`): YES (`epdquznwmq`, `elmjchdqcn`, `jtteddgeyl`, `irkeobngyh`, `qtjqovumxf`, `mkgqjopcjn`).
- Uses ACTION5 (modal): NO.
- Uses ACTION6 (click): YES.
- Uses ACTION7: YES (undo).
- Has level data dicts (uses `level.get_data` / `level.set_data`): YES (every level has `data={"grouped_pauses": False, "lit_extension": True}` although neither flag is read by reachable code in L1-3).
- Multi-mechanic per level (vs. single mechanic per level): NO — same colour-match-snake mechanic across L1-3; L3 adds a "decoy" unpaired snake but the core mechanic is unchanged.
- Tutorial level appears solvable by random play: NO. The colour-matching predicate requires specific positional alignment; random play has near-zero success probability.
- Has a depleting resource: YES — step counter, 196 per level.
- Has an accumulating resource: YES (implicit) — segments-on-matching-tile count.
- Sprite shape convention used: mixed — filled head squares, striped body segments, hollow target tiles, anchor capsules.
- HUD position: middle (row 53, between upper-snake and lower-snake regions).
- Palette size used: 9 distinct palette values appear in placed L1-3 sprites: {2, 3, 4, 5, 6, 8, 9, 12, 14} from sprites + {0, 1, 11, 15} potential from runtime. Static = 9.
- Background colour value: 5 (`BACKGROUND_COLOR = 5`).
- Padding / letter-box colour value: 3 (`PADDING_COLOR = 3`).
- Number of distinct mechanics introduced across levels 1-3: 1 base mechanic; L3 adds the "decoy snake" sub-feature but it's not a true new mechanic.
- Number of levels documented: 3.

(End of file.)
