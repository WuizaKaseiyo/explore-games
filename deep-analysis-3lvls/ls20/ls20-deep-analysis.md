# ls20 — deep analysis

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
- File: /Users/nickhe/Programming/NovaPlay-Agents/game_sources/ls20/9607627b/ls20.py
- Lines: 2042
- Class name: Ls20
- available_actions: [1, 2, 3, 4]   (passed as `available_actions=[1, 2, 3, 4]` to `super().__init__`)
- Number of levels in source: 7   (more than 3; levels 4-7 exist but are excluded per skill scope)
- Number of levels documented in this analysis: 3
- Imports: `math`, `numpy as np`, `typing.{List, Optional, Set, Tuple}`. From `novaengine`: `NovaBaseGame`, `BlockingMode`, `Camera`, `GameAction`, `Level`, `RenderableUserDisplay`, `Sprite`.

## Mechanic essence (one sentence)

A small magenta-yellow avatar wanders a wall-bound maze in five-pixel hops, and stepping onto a coloured cycler-tile rolls its shape, hue, or rotation one notch through a fixed alphabet — the level is solved when the avatar's current shape-colour-rotation triplet matches the target imprinted on a goal pad it then walks onto, while pushable spring-plates shove the avatar across long corridors and step-refill pickups top up its dwindling action budget.

## Sprite roster

The `sprites = {...}` dict has 36 entries.

| sprite (obfuscated) | dims | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| `ajdspzphhd` | 1×11 | {14} | xfmluydglp | default | True | default | False | invisible bounding-box edge of an 11×11 push corridor (top/bottom of cyclers cluster) |
| `eqatonpohu` | 10×10 | {5} | eqatonpohu | 1 | True | default | True | overlay block ("badge background") used to flash gray on misuse, recoloured to 0 then 5 at hint events |
| `fesygzfqui` | 5×5 | {4, -2} | ihdgageizm | -5 | True | default | True | wall variant (right edge transparent strip) — partial HUD/wall |
| `fywfjzkxlm` | 3×3 | {0, -1} | – | default | True | default | True | candidate goal/avatar shape (T-glyph) — entry in the 6-shape pool |
| `ghizzeqtoh` | 10×10 | {0, -1} | ghizzeqtoh | 5 | True | default | False | hidden 10×10 hollow ring (frame around the badge, drawn invisible) |
| `gngifvjddu` | 3×3 | {0, -1} | – | default | True | default | True | candidate avatar shape #0 (diagonal glyph) |
| `grcpfuizfp` | 3×3 | {0, -1} | – | 1 | True | default | True | candidate avatar shape #4 (corner-diagonal glyph) |
| `hahdypcdru` | 1×21 | {14} | xfmluydglp | default | True | default | False | invisible bounding-box edge of a 21×21 push corridor |
| `hoswmpiqkw` | 7×7 | {0, -1} | hoswmpiqkw | -1 | True | default | False | hidden hint highlight ring; toggled visible when avatar matches a target |
| `ihdgageizm` | 5×5 | {4} | ihdgageizm | -5 | True | default | True | filled wall block (the playfield's primary blocker) |
| `irgjxweouz` | 1×29 | {14} | xfmluydglp | default | True | default | False | invisible bounding-box edge of a 29×29 push corridor |
| `kapcaakvb_b` | 5×5 | {1, -2} | gbvqrjtaqo | default | True | default | True | pushable plate "bottom" variant (1-row strip on top edge — push-down spring) |
| `krdypjjivz` | 5×5 | {4, -2} | ihdgageizm | -5 | True | default | True | wall variant (top-edge transparent strip) |
| `kvynsvxbpi` | 3×3 | {0, -1} | kvynsvxbpi | default | True | default | True | candidate avatar shape #2 (back-diagonal glyph); also the runtime shape-template anchor (replaced via `.pixels = self.ijessuuig[...].pixels.copy()`) |
| `lujfinsby_t` | 5×5 | {1, -2} | gbvqrjtaqo | default | True | default | True | pushable plate "top" variant (push-up spring) |
| `mkfbgalsbe` | 3×3 | {0, -1} | – | default | True | default | True | candidate avatar shape #2 (T glyph) |
| `mkjdaccuuf` | 5×5 | {0, -2} | ttfwljgohq | -1 | False | default | True | shape-cycler interactor (cycles avatar shape index) |
| `mxfhnkdzvf` | 5×5 | {4, -2} | ihdgageizm | -5 | True | default | True | wall variant (bottom-edge transparent strip) |
| `neltxxziap` | 1×11 | {14} | xfmluydglp | default | True | default | False | invisible bounding-box edge of an 11×11 push corridor (alternate orientation) |
| `njpewhmtfd` | 7×7 | {5, -1} | vjotnebuqo, vfkkzdgxzx | -3 | True | default | True | "second" goal-target ring variant tagged with both vjotnebuqo and vfkkzdgxzx (fades when target is satisfied) — defined but not placed in levels 1-3 |
| `nnjhdcanjk` | 3×3 | {0, -1} | – | default | True | default | True | candidate avatar shape #3 (mirrored diagonal glyph) |
| `npxgalaybz` | 3×3 | {11, -1} | npxgalaybz | -1 | False | default | True | step-counter refill pickup (cyan ring); consumed on overlap |
| `nszegiawib` | 9×9 | {3, -1} | – | -4 | True | default | True | textured "marker" panel (3-coloured background tile) — visual sign/sigil at the goal |
| `rhsxkxzdjz` | 5×5 | {0, 1, -2} | rhsxkxzdjz | -1 | True | default | True | rotation-cycler interactor (rotates avatar 90 deg per step) |
| `rjlbuycveu` | 5×5 | {5} | rjlbuycveu | -3 | False | default | True | gray goal pad (target square the avatar must reach) |
| `sfqyzhzkij` | 5×5 | {12, 9} | sfqyzhzkij | default | True | default | True | the player avatar (top half magenta-12, bottom half yellow-9; rendered template overwritten at runtime) |
| `soyhouuebz` | 5×5 | {-2, 9, 14, 0, 8, 12} | soyhouuebz | -1 | False | default | True | colour-cycler interactor (cycles avatar palette index) — multi-colour glyph |
| `sqpmiygfvh` | 1×1 | {11} | – | 3 | True | default | True | overlay flash (1×1 cyan); scaled to 64 to flash full screen on life loss |
| `tihiodtoj_l` | 5×5 | {1, -2} | gbvqrjtaqo | default | True | default | True | pushable plate "left" variant (push-left spring) |
| `ubspnhafvq` | 3×3 | {0, -1} | – | -2 | False | default | True | candidate avatar shape #5 (open-corner glyph) |
| `ubyunwkbpx` | 5×5 | {4, -2} | ihdgageizm | -5 | True | default | True | wall variant (left-edge transparent strip) |
| `vjotnebuqo` | 7×7 | {5, -1} | vjotnebuqo | -3 | True | default | True | gray hollow ring framing the goal pad (visible always until target consumed) |
| `wgmbtyhvbc` | 3×3 | {0, -1} | wgmbtyhvbc | 10 | True | default | True | preview/HUD glyph rendered next to step bar — shows current avatar shape mini icon |
| `xfmluydglp` | 11×11 | {14, -1} | xfmluydglp | default | True | default | False | invisible 11×11 push-corridor bounding box for cycler clusters |
| `xvrpzkggig` | 64×64 | {5, 4, -1} | – | default | True | default | True | letterbox / playfield outer frame (full-frame backdrop with HUD bay at bottom-left and gray padding strip on left) |
| `yjgargdic_r` | 5×5 | {1, -2} | gbvqrjtaqo | default | True | default | True | pushable plate "right" variant (push-right spring) |

### `ajdspzphhd` — push-corridor edge (11-cell horizontal strip)
- Pixel pattern: 1×11 row of value 14 (brown).
- Where it appears: not placed in levels 1, 2, or 3.
- Role: invisible bounding-box demarcating an 11×11 cluster of cyclers (used by the pushable-plate engine `twkzhcfelv`/`dboxixicic` to locate which interactor belongs to which corridor); visibility is False so it never renders.
- Visual-vs-functional read: invisible, so no on-frame appearance. A player would never see this; only the engine reads it.
  - At-rendered-scale shape: not rendered.
  - Palette signature: {14}; shared with other xfmluydglp-tagged corridor edges (hahdypcdru, irgjxweouz, neltxxziap, xfmluydglp).
  - Nearest-other-sprite check: `xfmluydglp` itself, the 11×11 hollow-frame counterpart; differentiator is dimensionality (this is an edge strip, that is a closed rectangle).
- Visual contrast notes: never visible; functional only.

### `eqatonpohu` — gray badge background block
- Pixel pattern: filled 10×10 block of value 5 (gray).
- Where it appears: levels 1, 2, 3 each place one at (1, 53). Always 1 copy.
- Role: HUD-area "badge" background that lives in the bottom-left corner of the play frame; on a "false success" event it is colour-remapped to 0 (black, momentarily) via `htkmubhry_2.color_remap(None, 0)` then back to 5 after the flash interval.
- Visual-vs-functional read: yes — a solid gray 10×10 swatch in a fixed corner reads as a UI badge, not a gameplay object.
  - At-rendered-scale shape: solid filled square.
  - Palette signature: {5}; shared with `rjlbuycveu` (goal pad) and `vjotnebuqo` (goal ring) and the gray padding side of `xvrpzkggig`.
  - Nearest-other-sprite check: `rjlbuycveu` (5×5 of value 5) — different size and corner-anchored placement, but the shared colour 5 is a confusion risk if either appears mid-board.
- Visual contrast notes: contrasts only against the bottom-left HUD bay's value-4 frame; would blend with any other gray sprite.

### `fesygzfqui` — wall variant (right-edge transparent strip)
- Pixel pattern: 5×5; columns 0-3 are value 4 (orange), column 4 is -2 (engine reserved padding).
- Where it appears: level 3 has 1 copy at (4, 5). Not placed in levels 1 or 2.
- Role: wall block, same `ihdgageizm` tag, used to draw a wall whose right edge is "shaved" so it abuts another wall cleanly.
- Visual-vs-functional read: yes — reads as a wall fragment.
  - At-rendered-scale shape: filled rectangle, slightly narrower than 5 cells.
  - Palette signature: {4, -2}; -2 is engine padding, so visible value is just 4.
  - Nearest-other-sprite check: `ihdgageizm` (5×5 solid 4) — visually almost identical at game scale; the 1-column gap is hard to spot, but functionally both are equivalent walls.
- Visual contrast notes: contrasts strongly against background 3.

### `fywfjzkxlm` — candidate avatar shape, T-glyph
- Pixel pattern: 3×3 with -1, 0, -1 / -1, 0, -1 / 0, 0, 0 (an upside-down T).
- Where it appears: not placed directly into any level; lives in the runtime shape pool `ijessuuig[1]` and is loaded into the avatar's pixels via the shape-cycle mechanic.
- Role: one of 6 selectable avatar glyph templates (shape index 1).
- Visual-vs-functional read: yes — small black glyph; reads as a "shape token".
  - At-rendered-scale shape: hollow / glyph.
  - Palette signature: {0, -1}; black on transparent, recoloured at runtime via `color_remap(0, color)` to current avatar colour.
  - Nearest-other-sprite check: `mkfbgalsbe` (3×3 with two vertical bars + bottom) — both T-like; distinguishable only because they are alternated by the shape-cycler, never present simultaneously on the avatar.
- Visual contrast notes: shape distinction only matters at the avatar position; any glyph contrast against background 3 is fine in palettes 8/9/12/14.

### `ghizzeqtoh` — hidden 10×10 hollow ring around badge
- Pixel pattern: 10×10; outer 1-pixel ring of value 0 (black) on -1 transparent inside.
- Where it appears: levels 1, 2, 3 each place one at (1, 53), co-located with `eqatonpohu`.
- Role: a hidden frame around the badge, set invisible by default (`visible=False`); engine code may set it visible briefly on hint flashes.
- Visual-vs-functional read: not visible by default; would read as a 1-pixel black outline if shown.
  - At-rendered-scale shape: hollow ring.
  - Palette signature: {0, -1}.
  - Nearest-other-sprite check: `hoswmpiqkw` (7×7 hollow ring) — same hollow style, different size and position.
- Visual contrast notes: only relevant when toggled on; contrasts against the gray badge it overlays.

### `gngifvjddu` — candidate avatar shape, diagonal-corner glyph
- Pixel pattern: 3×3 with [0,0,-1]/[-1,0,0]/[0,-1,0].
- Where it appears: in `self.ijessuuig[0]`, never placed directly; loaded into the avatar via the shape pool.
- Role: avatar shape index 0.
- Visual-vs-functional read: small abstract glyph; reads as "shape A".
  - At-rendered-scale shape: glyph.
  - Palette signature: {0, -1}; recoloured at runtime.
  - Nearest-other-sprite check: `nnjhdcanjk` (3×3 mirrored variant) — both are diagonal arrangements; visually similar enough that the player must read the exact glyph.
- Visual contrast notes: as a 3×3 glyph, only distinguishable when avatar colour is high-contrast against 3.

### `grcpfuizfp` — candidate avatar shape, corner-diagonal
- Pixel pattern: 3×3 with [-1,0,-1]/[0,0,-1]/[-1,0,0].
- Where it appears: in `self.ijessuuig[4]`; never placed directly.
- Role: avatar shape index 4.
- Visual-vs-functional read: glyph token.
  - At-rendered-scale shape: glyph.
  - Palette signature: {0, -1}.
  - Nearest-other-sprite check: `gngifvjddu` and `nnjhdcanjk`; the 6-shape pool is intentionally close-packed and hard to read.
- Visual contrast notes: relies on avatar colour vs background 3.

### `hahdypcdru` — invisible 21-cell push-corridor edge
- Pixel pattern: 1×21 row of value 14.
- Where it appears: not placed in levels 1, 2, or 3.
- Role: same xfmluydglp role as `ajdspzphhd`, scaled to 21 cells.
- Visual-vs-functional read: invisible.
  - At-rendered-scale shape: not rendered.
  - Palette signature: {14}.
  - Nearest-other-sprite check: `ajdspzphhd`, `irgjxweouz`, `neltxxziap`.
- Visual contrast notes: never visible.

### `hoswmpiqkw` — hint highlight ring
- Pixel pattern: 7×7 with outer 1-pixel ring of 0 (black) on -1 transparent.
- Where it appears: levels 1, 2, 3 each place 1 copy near the goal target (level 1 (33,9), level 2 (13,39), level 3 (53,49)). Initially `visible=False`.
- Role: hint glyph; toggled visible by `vqfjzzkhid()` only when the avatar's current shape/colour/rotation already matches the target's `kvynsvxbpi/GoalColor/GoalRotation`. Hidden again on level transitions or life loss.
- Visual-vs-functional read: when shown, reads as "you have the right configuration — go here".
  - At-rendered-scale shape: hollow ring.
  - Palette signature: {0, -1}.
  - Nearest-other-sprite check: `ghizzeqtoh` (10×10 hollow ring) — same style; differs by size and position.
- Visual contrast notes: black ring against gray (5) goal pad; high contrast.

### `ihdgageizm` — primary wall block
- Pixel pattern: filled 5×5 of value 4 (orange).
- Where it appears: massively across all three levels (level 1 ≈110+ copies, level 2 ≈110+ copies, level 3 ≈80+ copies). Forms the maze walls.
- Role: maze wall; `txnfzvzetn` rejects movement into any sprite tagged `ihdgageizm`.
- Visual-vs-functional read: yes — solid orange blocks read as walls immediately.
  - At-rendered-scale shape: filled square.
  - Palette signature: {4}; same colour as wall variants `fesygzfqui`, `krdypjjivz`, `mxfhnkdzvf`, `ubyunwkbpx`.
  - Nearest-other-sprite check: the four wall variants — all share value 4 and the same `ihdgageizm` tag, so they unify visually as one wall family.
- Visual contrast notes: orange-on-background-3 is the dominant level structure; high readability.

### `irgjxweouz` — invisible 29-cell push-corridor edge
- Pixel pattern: 1×29 column of value 14.
- Where it appears: not placed in levels 1, 2, or 3.
- Role: xfmluydglp-tagged invisible bounding for very long push corridors.
- Visual-vs-functional read: invisible.
  - At-rendered-scale shape: not rendered.
  - Palette signature: {14}.
  - Nearest-other-sprite check: other xfmluydglp invisible edges.
- Visual contrast notes: never visible.

### `kapcaakvb_b` — pushable plate, bottom-direction
- Pixel pattern: 5×5; row 0 is value 1 (white), rows 1-4 are -2 (engine padding/transparent).
- Where it appears: level 3 has 1 copy at (54, 4). Not in levels 1 or 2.
- Role: a pushable interactor (`gbvqrjtaqo` tag) attached to the `twkzhcfelv` push engine; the trailing `_b` in its name signals the push direction is +y (down) — `twkzhcfelv.__init__` reads the last char of name and sets dy=+1.
- Visual-vs-functional read: a thin white bar at the top of a 5-cell square reads as a button/plate edge.
  - At-rendered-scale shape: striped (one-row fill).
  - Palette signature: {1, -2}; white reads on background 3.
  - Nearest-other-sprite check: `lujfinsby_t` (white bar at bottom), `tihiodtoj_l` (white bar on right), `yjgargdic_r` (white bar on left); all are the same plate family rotated.
- Visual contrast notes: white on background 3 is high-contrast.

### `krdypjjivz` — wall variant (top-edge transparent strip)
- Pixel pattern: 5×5; row 0 is -2, rows 1-4 are value 4.
- Where it appears: not placed in levels 1, 2, or 3.
- Role: same as `ihdgageizm`, tagged identically; for level layouts that need a wall whose top row is "open".
- Visual-vs-functional read: reads as a wall fragment.
  - At-rendered-scale shape: filled, slightly clipped.
  - Palette signature: {4, -2}.
  - Nearest-other-sprite check: `ihdgageizm`, `mxfhnkdzvf`, `ubyunwkbpx`, `fesygzfqui`.
- Visual contrast notes: same as `ihdgageizm`.

### `kvynsvxbpi` — back-diagonal avatar glyph (and runtime shape-anchor)
- Pixel pattern: 3×3 with [0,-1,-1]/[-1,0,-1]/[-1,-1,0] (back-diagonal).
- Where it appears: levels 1, 2, 3 each place 1 copy as the per-level shape anchor (level 1 at (35,11), level 2 at (15,41), level 3 at (55,51)). At runtime the engine takes this sprite as a placeholder and loads the actual goal shape into its `pixels` from the shape pool.
- Role: per-target "expected shape" template — visually a glyph showing what shape the avatar must adopt to satisfy the corresponding `rjlbuycveu` goal pad. Also lives in the shape pool but the level-data key `"kvynsvxbpi"` indexes into the shape pool.
- Visual-vs-functional read: yes — small glyph next to the goal ring telegraphs "match this glyph".
  - At-rendered-scale shape: glyph.
  - Palette signature: {0, -1} as defined; runtime recoloured to the goal colour via `color_remap(0, GoalColor)`.
  - Nearest-other-sprite check: each of the other 5 candidate avatar shapes — all share the 3×3 + value-0 + -1 footprint.
- Visual contrast notes: rotation and recolour at runtime distinguish target glyphs; against background 3 the glyph reads in palette 8/9/12/14.

### `lujfinsby_t` — pushable plate, top-direction
- Pixel pattern: 5×5; rows 0-3 are -2, row 4 is value 1.
- Where it appears: not placed in levels 1, 2, or 3.
- Role: pushable plate that travels upward (-y) when the avatar collides; `_t` suffix → dy = -1.
- Visual-vs-functional read: thin white bar at the bottom of a 5×5 square.
  - At-rendered-scale shape: striped.
  - Palette signature: {1, -2}.
  - Nearest-other-sprite check: the other plate variants `kapcaakvb_b`, `tihiodtoj_l`, `yjgargdic_r`.
- Visual contrast notes: white on 3 reads cleanly.

### `mkfbgalsbe` — candidate avatar shape, T-glyph (downward)
- Pixel pattern: 3×3 with [0,-1,0]/[0,-1,0]/[0,0,0].
- Where it appears: in `self.ijessuuig[2]`; never placed directly.
- Role: avatar shape index 2.
- Visual-vs-functional read: glyph token.
  - At-rendered-scale shape: glyph.
  - Palette signature: {0, -1}.
  - Nearest-other-sprite check: `fywfjzkxlm` is its mirror; both are π-shaped at low res.
- Visual contrast notes: same as other glyphs.

### `mkjdaccuuf` — shape-cycler interactor
- Pixel pattern: 5×5 with -2 background and a tiny "L" of value 0 at offsets {(1,1),(2,2),(2,3),(3,2)}.
- Where it appears: not placed in levels 1, 2, or 3.
- Role: when avatar enters this cell, `txnfzvzetn` increments `self.fwckfzsyc` (current shape index) modulo 6; the avatar's pixels are replaced by `ijessuuig[fwckfzsyc].pixels`.
- Visual-vs-functional read: small glyph; reads as an interactor token.
  - At-rendered-scale shape: glyph.
  - Palette signature: {0, -2}.
  - Nearest-other-sprite check: `rhsxkxzdjz` (rotation-cycler) and `soyhouuebz` (colour-cycler) — all are 5×5 interactor sprites with -2 padding and an inner glyph; players must learn each glyph's effect.
- Visual contrast notes: requires recognising the specific inner glyph.

### `mxfhnkdzvf` — wall variant (bottom-edge transparent strip)
- Pixel pattern: 5×5; rows 0-3 are 4, row 4 is -2.
- Where it appears: level 3 has 1 copy at (54, 0). Not in levels 1 or 2.
- Role: wall variant.
- Visual-vs-functional read: wall fragment.
  - At-rendered-scale shape: filled.
  - Palette signature: {4, -2}.
  - Nearest-other-sprite check: other wall variants.
- Visual contrast notes: same as `ihdgageizm`.

### `neltxxziap` — invisible 11-cell push-corridor edge (column orientation)
- Pixel pattern: 11×1 column of value 14.
- Where it appears: not placed in levels 1, 2, or 3.
- Role: xfmluydglp-tagged corridor bounding edge.
- Visual-vs-functional read: invisible.
  - At-rendered-scale shape: not rendered.
  - Palette signature: {14}.
  - Nearest-other-sprite check: other xfmluydglp edges.
- Visual contrast notes: never visible.

### `njpewhmtfd` — secondary goal ring (with vfkkzdgxzx tag)
- Pixel pattern: 7×7 ring of value 5 with -1 interior.
- Where it appears: not placed in levels 1, 2, or 3.
- Role: a goal-ring variant carrying both `vjotnebuqo` and `vfkkzdgxzx` tags; `pbznecvnfr()` looks up the `vfkkzdgxzx` tag to fade the ring after a target is consumed.
- Visual-vs-functional read: identical visual to `vjotnebuqo`; reads as a goal ring.
  - At-rendered-scale shape: hollow ring.
  - Palette signature: {5, -1}.
  - Nearest-other-sprite check: `vjotnebuqo` — same pixels, different tag. Players cannot tell them apart.
- Visual contrast notes: gray ring on background 3.

### `nnjhdcanjk` — candidate avatar shape, mirrored diagonal
- Pixel pattern: 3×3 with [-1,0,0]/[0,-1,0]/[-1,0,-1].
- Where it appears: in `self.ijessuuig[3]`; never placed directly.
- Role: avatar shape index 3.
- Visual-vs-functional read: glyph token.
  - At-rendered-scale shape: glyph.
  - Palette signature: {0, -1}.
  - Nearest-other-sprite check: `gngifvjddu` is the near-mirror.
- Visual contrast notes: as other glyphs.

### `npxgalaybz` — step-counter refill pickup
- Pixel pattern: 3×3 of value 11 (cyan) with center -1 (transparent), forming a small ring.
- Where it appears: level 1 places 0; level 2 places 2 copies (15,16) and (40,51); level 3 places 2 copies (35,16) and (20,31).
- Role: pickup. When avatar overlaps it, `txnfzvzetn` calls `self._step_counter_ui.kbkdzqocik(self._step_counter_ui.osgviligwp)` (refill steps to max), removes the sprite, and stores it on `self.ofoahudlo` for re-add on life loss.
- Visual-vs-functional read: distinct cyan ring stands out from the 4-orange-walls / 5-gray-goal palette; reads as "collectible".
  - At-rendered-scale shape: hollow ring (3×3 with hole).
  - Palette signature: {11, -1}; cyan unique to this sprite at its layer.
  - Nearest-other-sprite check: no other cyan glyph in the roster — visually unique.
- Visual contrast notes: cyan vs background 3 is high-contrast and unique.

### `nszegiawib` — sigil panel (textured background tile)
- Pixel pattern: 9×9 of value 3 with the top edge interrupted by 5 cells of -1 (so a 3-coloured panel with a notch on top).
- Where it appears: level 1 at (32, 8) rotated 180; level 2 at (12, 38); level 3 at (52, 48). Always 1 copy per level, placed under the goal ring.
- Role: decorative backdrop highlighting the goal location.
- Visual-vs-functional read: reads as a flat panel; rotation gives the notch direction a hint of orientation.
  - At-rendered-scale shape: filled square (with single-row notch).
  - Palette signature: {3, -1}; value 3 == BACKGROUND_COLOR, so most of it is invisible against the background.
  - Nearest-other-sprite check: nothing else has a 9×9 footprint or the notch.
- Visual contrast notes: low contrast (matches background); the notch is the only on-screen distinction.

### `rhsxkxzdjz` — rotation-cycler interactor
- Pixel pattern: 5×5; -2 background with arrow-like 0 + 1 glyph: top-cell {(2,1)=0}, mid {(1,2)=1, (2,2)=0, (3,2)=0}, bottom {(2,3)=1}.
- Where it appears: level 1 at (19, 30); level 2 at (49, 45); level 3 at (49, 10). 1 copy per level.
- Role: when avatar enters cell, `txnfzvzetn` does `self.cklxociuu = (self.cklxociuu + 1) % 4`, then `htkmubhry.set_rotation(dhksvilbb[cklxociuu])` (rotates the avatar preview glyph by 90°). Also calls `vqfjzzkhid()` afterwards to trigger hint visibility check.
- Visual-vs-functional read: arrow-glyph reads as "rotate" — moderately functional.
  - At-rendered-scale shape: glyph.
  - Palette signature: {-2, 0, 1}; black + white on padding.
  - Nearest-other-sprite check: `mkjdaccuuf` (shape cycler) and `soyhouuebz` (colour cycler) — three distinct interactor glyphs, each 5×5 with -2 padding.
- Visual contrast notes: arrow shape distinguishable but similar in scale to other interactors.

### `rjlbuycveu` — goal pad
- Pixel pattern: filled 5×5 of value 5 (gray).
- Where it appears: level 1 at (34, 10); level 2 at (14, 40); level 3 at (54, 50). 1 copy per level.
- Role: target square. The avatar must arrive at this position with matching shape/colour/rotation. When avatar enters with mismatch, the engine flashes `htkmubhry_2` to 0 and triggers a "false success" interval (`akoadfsur = 5`). When avatar enters with matching configuration, `pbznecvnfr()` marks the target consumed and removes the pad from the level.
- Visual-vs-functional read: solid gray square reads as a "platform" / "destination" in the corner of the goal cluster.
  - At-rendered-scale shape: filled square.
  - Palette signature: {5}; same gray as `eqatonpohu` (badge bg) and `vjotnebuqo` ring.
  - Nearest-other-sprite check: `eqatonpohu` — both filled gray; located in different parts of frame, but a player might confuse a stray pad with the badge.
- Visual contrast notes: gray on background 3; visually distinct only because the goal ring `vjotnebuqo` frames it.

### `sfqyzhzkij` — player avatar (template only)
- Pixel pattern: 5×5; top 2 rows value 12 (purple/magenta), bottom 3 rows value 9 (yellow). At runtime, `qetwzqzzik()` overwrites `htkmubhry.pixels` (which is a *different* sprite — `wgmbtyhvbc`) and `htkmubhry` is the avatar preview, while `gudziatsk` is this `sfqyzhzkij` sprite that physically moves on the playfield. `gudziatsk` is the runtime player.
- Where it appears: levels 1, 2, 3 — 1 copy per level (level 1 at (34,45), level 2 at (29,40), level 3 at (9,45)).
- Role: physical avatar token; moves in 5-cell steps via `set_position` in `step()`.
- Visual-vs-functional read: yes — large two-tone block reads as the player.
  - At-rendered-scale shape: filled, two-stripe.
  - Palette signature: {12, 9}.
  - Nearest-other-sprite check: `soyhouuebz` (5×5 with palette 9/14/0/8/12) — both share warm colours; differentiated by `sfqyzhzkij`'s clean 2-stripe vs `soyhouuebz`'s noisy interior.
- Visual contrast notes: 12+9 against background 3 is high-contrast; nothing else is two-stripe.

### `soyhouuebz` — colour-cycler interactor
- Pixel pattern: 5×5; -2 frame, inner 3×3 with palette {9, 14, 0, 8, 12} arranged as a colour cluster.
- Where it appears: level 3 at (29, 45). Not placed in levels 1 or 2.
- Role: when avatar enters, `txnfzvzetn` does `lwphyolnjb = (self.hiaauhahz + 1) % len(self.tnkekoeuk)`; remaps avatar's preview pixels from old colour to new; updates `hiaauhahz`. Also rechecks `vqfjzzkhid()`.
- Visual-vs-functional read: multi-colour 5×5 reads as "colour swatch" / palette.
  - At-rendered-scale shape: textured.
  - Palette signature: {-2, 9, 14, 0, 8, 12}; explicitly references all 4 colour-cycle values, signposting "this changes colour".
  - Nearest-other-sprite check: `mkjdaccuuf` and `rhsxkxzdjz` — all 3 interactors share -2 frame; `soyhouuebz` is the most colourful and most legible.
- Visual contrast notes: high contrast — the only multi-coloured interactor.

### `sqpmiygfvh` — life-loss flash overlay
- Pixel pattern: 1×1 of value 11 (cyan).
- Where it appears: not placed in levels via the level constructor; instead added at runtime in `on_set_level` via `self.aqdxgoyvu = sprites["sqpmiygfvh"].clone(); self.current_level.add_sprite(self.aqdxgoyvu); self.aqdxgoyvu.set_visible(False)`.
- Role: full-screen flash on life loss; on lose-step `set_scale(64)`, `set_position(0,0)`, `set_visible(True)` for `xvzyzqolqz = 5` frames.
- Visual-vs-functional read: a 5-frame full-cyan flash reads as a "you lost a life" cue.
  - At-rendered-scale shape: single-cell base, scaled.
  - Palette signature: {11}; cyan, shared with `npxgalaybz` (refill pickup).
  - Nearest-other-sprite check: `npxgalaybz`; both cyan but different scale and behaviour (one is on-board pickup, this is full-screen flash).
- Visual contrast notes: total screen flood; intentionally jarring.

### `tihiodtoj_l` — pushable plate, left-direction
- Pixel pattern: 5×5; columns 0-3 are -2, column 4 is value 1.
- Where it appears: not placed in levels 1, 2, or 3.
- Role: gbvqrjtaqo plate, dx = -1 due to `_l` suffix.
- Visual-vs-functional read: white bar on right edge.
  - At-rendered-scale shape: striped vertical.
  - Palette signature: {1, -2}.
  - Nearest-other-sprite check: other plates.
- Visual contrast notes: white on 3.

### `ubspnhafvq` — candidate avatar shape, open corner
- Pixel pattern: 3×3 with [0,0,0]/[-1,-1,0]/[0,-1,0].
- Where it appears: in `self.ijessuuig[5]`; never placed directly.
- Role: avatar shape index 5. Note: levels 1 and 2 set `kvynsvxbpi: 5` in level data → expected shape is index 5 = this glyph.
- Visual-vs-functional read: glyph token.
  - At-rendered-scale shape: glyph.
  - Palette signature: {0, -1}.
  - Nearest-other-sprite check: `mkfbgalsbe`.
- Visual contrast notes: glyph contrast as others.

### `ubyunwkbpx` — wall variant (left-edge transparent strip)
- Pixel pattern: 5×5; column 0 is -2, columns 1-4 are 4.
- Where it appears: not placed in levels 1, 2, or 3.
- Role: wall variant.
- Visual-vs-functional read: wall fragment.
  - At-rendered-scale shape: filled.
  - Palette signature: {4, -2}.
  - Nearest-other-sprite check: other wall variants.
- Visual contrast notes: same as `ihdgageizm`.

### `vjotnebuqo` — goal ring
- Pixel pattern: 7×7 ring of value 5 (gray) with interior -1 (transparent).
- Where it appears: level 1 at (33, 9); level 2 at (13, 39); level 3 at (53, 49). 1 copy per level.
- Role: visual frame for the goal pad. Set invisible on life loss; set visible again on respawn. Removed/hidden when the corresponding goal is consumed (only the variant tagged `vfkkzdgxzx`, which `vjotnebuqo` itself is not, remains).
- Visual-vs-functional read: yes — hollow gray ring reads as "destination marker".
  - At-rendered-scale shape: hollow ring.
  - Palette signature: {5, -1}.
  - Nearest-other-sprite check: `njpewhmtfd` (identical pixels but extra `vfkkzdgxzx` tag).
- Visual contrast notes: gray ring on background 3.

### `wgmbtyhvbc` — avatar preview HUD glyph
- Pixel pattern: 3×3 with [0,-1,0]/[-1,0,-1]/[0,-1,0] (X shape).
- Where it appears: levels 1, 2, 3 each place 1 copy at (3, 55) with `set_scale(2)`. So rendered as 6×6.
- Role: the runtime "current shape preview" — `qetwzqzzik` writes `self.htkmubhry.pixels = self.ijessuuig[fwckfzsyc].pixels.copy()` and `htkmubhry.color_remap(0, current_color)`. `htkmubhry` is the alias for this sprite. The HUD widget renders it into the bottom HUD bay.
- Visual-vs-functional read: yes — small replica next to the step bar reads as "your current avatar config".
  - At-rendered-scale shape: glyph (post-runtime overwrite, this is whichever shape player has selected).
  - Palette signature: {0, -1} as defined; recoloured at runtime.
  - Nearest-other-sprite check: `kvynsvxbpi` — both 3×3 glyphs; the difference is location (kvynsvxbpi is on-field next to goal, this is in HUD).
- Visual contrast notes: scaled 2× and rendered into the HUD region.

### `xfmluydglp` — invisible 11×11 push-corridor frame
- Pixel pattern: 11×11 hollow frame; outer ring of value 14, inner -1.
- Where it appears: not placed directly in levels 1, 2, or 3 (the `xfmluydglp` tag is shared with the corridor edges, but no full frame appears in those levels).
- Role: in `on_set_level`, the engine iterates `current_level.get_sprites_by_tag("xfmluydglp")` and pairs them with cyclers (`ttfwljgohq`/`soyhouuebz`/`rhsxkxzdjz`) to construct `dboxixicic` patroller objects; these would shift the cycler within the corridor. In levels 1-3 there are no xfmluydglp-tagged sprites placed, so `wsoslqeku` ends up empty.
- Visual-vs-functional read: invisible.
  - At-rendered-scale shape: not rendered.
  - Palette signature: {14, -1}.
  - Nearest-other-sprite check: other xfmluydglp invisible variants.
- Visual contrast notes: never visible.

### `xvrpzkggig` — playfield letterbox / outer frame
- Pixel pattern: 64×64. Top-left strip (cols 0-3, rows 0-50) is value 5 (gray); rows 51-62 form a value-4 (orange) HUD bay outlined in cols 0-11 with interior -1; the bottom-right region (rows 51-62, cols 12-63) is filled value 5; the rest is -1 (transparent — the playfield window).
- Where it appears: levels 1, 2, 3 each place 1 unmoved copy via `sprites["xvrpzkggig"].clone()`.
- Role: provides the visual frame around the playfield, gray padding on the left, and the HUD bay at the bottom-left where the step counter and lives are drawn.
- Visual-vs-functional read: reads as the "border / dashboard" — the frame around the active play region.
  - At-rendered-scale shape: large filled regions; multi-cell mosaic.
  - Palette signature: {5, 4, -1}; gray + orange.
  - Nearest-other-sprite check: nothing else is full-frame; visually unique.
- Visual contrast notes: gray + orange against the inner 3-background; the HUD bay's orange outline is a visual anchor.

### `yjgargdic_r` — pushable plate, right-direction
- Pixel pattern: 5×5; column 0 is value 1, columns 1-4 are -2.
- Where it appears: level 3 at (8, 5). Not in levels 1 or 2.
- Role: gbvqrjtaqo plate, dx = +1 due to `_r` suffix.
- Visual-vs-functional read: white bar on left edge.
  - At-rendered-scale shape: striped vertical.
  - Palette signature: {1, -2}.
  - Nearest-other-sprite check: other plate variants.
- Visual contrast notes: white on 3.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (64, 64)
- Number of sprites placed: 121 (counted in source: 1 eqatonpohu + 1 ghizzeqtoh + 1 hoswmpiqkw + 113 ihdgageizm + 1 kvynsvxbpi + 1 nszegiawib + 1 rhsxkxzdjz + 1 rjlbuycveu + 1 sfqyzhzkij + 1 vjotnebuqo + 1 wgmbtyhvbc + 1 xvrpzkggig).
- Composition by role: 1 player avatar (`sfqyzhzkij` at (34,45)), 1 goal pad (`rjlbuycveu` at (34,10)), 1 goal ring (`vjotnebuqo` at (33,9)), 1 sigil panel (`nszegiawib` at (32,8)), 1 hint ring (`hoswmpiqkw` at (33,9), invisible by default), 1 expected-shape glyph (`kvynsvxbpi` at (35,11)), 1 rotation-cycler (`rhsxkxzdjz` at (19,30)), ~113 wall blocks (`ihdgageizm`), 1 outer frame (`xvrpzkggig`), 1 HUD avatar-preview (`wgmbtyhvbc` at (3,55) scale 2), 1 badge background + frame (`eqatonpohu` + `ghizzeqtoh` at (1,53)).
- Level data:
  - `StepCounter: 42` — initial step budget.
  - `kvynsvxbpi: 5` — the expected avatar shape index = 5 (`ubspnhafvq` glyph).
  - `GoalColor: 9` — the expected avatar colour index = 9 (yellow).
  - `GoalRotation: 0` — the expected avatar rotation = 0°.
  - `StartShape: 5` — avatar starts as shape 5.
  - `StartColor: 9` — avatar starts as colour 9.
  - `StartRotation: 270` — avatar starts rotated 270°. To win the player must rotate to 0° (i.e. 1 invocation of the rotation-cycler).
  - `Fog: False` — no fog overlay.
  - `StepsDecrement: 1` — each move decrements the step counter by 1 instead of the default 2.
- Spawn position(s): player at (34, 45).
- Per-cell layout: grid is 64×64 — too large for ASCII; coordinate listing of non-wall sprites:
  - Player avatar `sfqyzhzkij`: (34, 45).
  - Goal pad `rjlbuycveu`: (34, 10).
  - Goal ring `vjotnebuqo`: (33, 9).
  - Sigil panel `nszegiawib` (rotated 180): (32, 8).
  - Hint ring `hoswmpiqkw` (invisible): (33, 9).
  - Expected-shape glyph `kvynsvxbpi`: (35, 11).
  - Rotation-cycler `rhsxkxzdjz`: (19, 30).
  - Badge `eqatonpohu` + frame `ghizzeqtoh`: (1, 53).
  - HUD preview `wgmbtyhvbc`: (3, 55).
  - Outer frame `xvrpzkggig`: (0, 0).
  - Walls (`ihdgageizm`): occupy cells along all four boundaries (x=4 column, x=59 column, y=0 and y=55 rows partially) and form interior maze structure across rows 5-50.
- Mechanic introduced relative to the previous level: this is level 1; the level introduces:
  - basic 5-cell stepping motion via `available_actions=[1,2,3,4]`,
  - the "match shape + colour + rotation" target predicate,
  - the rotation-cycler interactor (`rhsxkxzdjz`),
  - the step-counter HUD with `StepsDecrement=1`,
  - lives (3) via `self.aqygnziho = 3`.
- Specific challenge: starting at (34,45), the player must navigate through the maze to step onto the rotation-cycler at (19,30) to advance avatar rotation from 270° → 0° (3 invocations: 270→0 wraps around 360, but the sequence is 0,90,180,270 mod 4 — starting at index 3, +1 → index 0 → rotation 0°), then move to the goal pad at (34,10) with shape=5, colour=9, rotation=0. The hint ring `hoswmpiqkw` toggles visible the moment the avatar's configuration matches the target, helping the planner.
- Estimated optimal action count: roughly 15-20 (path through cycler then goal, cell-stride 5).

### Level 2
- `grid_size`: (64, 64)
- Number of sprites placed: 117 (counted: 1 eqatonpohu + 1 ghizzeqtoh + 1 hoswmpiqkw + 105 ihdgageizm + 1 kvynsvxbpi + 2 npxgalaybz + 1 nszegiawib + 1 rhsxkxzdjz + 1 rjlbuycveu + 1 sfqyzhzkij + 1 vjotnebuqo + 1 wgmbtyhvbc + 1 xvrpzkggig).
- Composition by role: 1 player (`sfqyzhzkij` at (29,40)), 1 goal pad (at (14,40)), 1 goal ring (at (13,39)), 1 sigil panel (at (12,38)), 1 hint ring (at (13,39)), 1 expected-shape glyph (at (15,41)), 1 rotation-cycler (`rhsxkxzdjz` at (49,45)), 2 step-refill pickups (`npxgalaybz` at (15,16) and (40,51)), ~105 wall blocks, 1 outer frame, 1 HUD preview, 1 badge.
- Level data:
  - `StepCounter: 42`.
  - `kvynsvxbpi: 5` — expected shape = 5.
  - `GoalColor: 9` — expected colour = 9.
  - `GoalRotation: 270` — expected rotation = 270°.
  - `StartShape: 5`, `StartColor: 9`, `StartRotation: 0`.
  - `Fog: False`.
  - (no `StepsDecrement` key) — `wbcenorpju` defaults `efipnixsvl = 2`, i.e. each move costs 2 steps.
- Spawn position(s): player at (29, 40).
- Per-cell layout: 64×64 — coordinate listing:
  - Player: (29, 40). Goal: (14, 40). Goal ring: (13, 39). Hint ring: (13, 39). Expected-glyph: (15, 41). Sigil: (12, 38). Rotation-cycler: (49, 45). Refills: (15, 16), (40, 51). Badge: (1, 53). HUD preview: (3, 55). Outer frame: (0, 0). Walls: dense maze.
- Mechanic introduced relative to the previous level:
  - `npxgalaybz` step-refill pickup is introduced (consumed on overlap; refills step counter to max).
  - Default step-decrement returns to 2 per move (the `StepsDecrement` key is absent), so the budget is *tighter* per action than level 1.
  - The rotation goal flips: the player must end at rotation 270°, requiring 3 cycler invocations (0→90→180→270).
- Specific challenge: navigate to the rotation-cycler in the bottom-right corner, stepping there 3 times to advance rotation from 0° to 270°, then traverse the maze to the goal in the bottom-left. Two refill pickups along the way let the player "reset" their step budget if they detoured. Balancing rotation count against step depletion is the puzzle.
- Estimated optimal action count: roughly 30-40 (longer corridor, 3 cycler hits, double-cost moves).

### Level 3
- `grid_size`: (64, 64)
- Number of sprites placed: 95 (counted: 1 eqatonpohu + 1 fesygzfqui + 1 ghizzeqtoh + 1 hoswmpiqkw + 80 ihdgageizm + 1 kapcaakvb_b + 1 kvynsvxbpi + 1 mxfhnkdzvf + 2 npxgalaybz + 1 nszegiawib + 1 rhsxkxzdjz + 1 rjlbuycveu + 1 sfqyzhzkij + 1 soyhouuebz + 1 vjotnebuqo + 1 wgmbtyhvbc + 1 xvrpzkggig + 1 yjgargdic_r).
- Composition by role: 1 player (`sfqyzhzkij` at (9,45)), 1 goal pad (at (54,50)), 1 goal ring (at (53,49)), 1 sigil panel (at (52,48)), 1 hint ring (at (53,49)), 1 expected-shape glyph (at (55,51)), 1 rotation-cycler (at (49,10)), 1 colour-cycler (`soyhouuebz` at (29,45)), 2 step-refills (at (35,16) and (20,31)), 1 down-pushable plate (`kapcaakvb_b` at (54,4)), 1 right-pushable plate (`yjgargdic_r` at (8,5)), 2 wall-variant fragments (`fesygzfqui` at (4,5), `mxfhnkdzvf` at (54,0)), ~80 wall blocks.
- Level data:
  - `StepCounter: 42`.
  - `kvynsvxbpi: 5` — expected shape = 5.
  - `GoalColor: 9` — expected colour = 9.
  - `GoalRotation: 180` — expected rotation = 180°.
  - `StartShape: 5`, `StartColor: 12` (purple/magenta — different from goal!), `StartRotation: 0`.
  - `Fog: False`.
  - (no `StepsDecrement`) — default 2 per move.
- Spawn position(s): player at (9, 45).
- Per-cell layout: 64×64 — coordinate listing:
  - Player: (9,45). Goal: (54,50). Goal ring/sigil/hint: (53,49)/(52,48)/(53,49). Expected-glyph: (55,51). Rotation-cycler: (49,10). Colour-cycler: (29,45). Refills: (35,16),(20,31). Plates: kapcaakvb_b (54,4) [pushes down], yjgargdic_r (8,5) [pushes right]. Wall variants: fesygzfqui (4,5), mxfhnkdzvf (54,0). Badge: (1,53). HUD preview: (3,55). Outer frame: (0,0).
- Mechanic introduced relative to the previous level:
  - The colour-cycler interactor (`soyhouuebz` tag) is introduced — cycles avatar colour through the 4-element list `[12, 9, 14, 8]` modulo 4.
  - Pushable plates (`gbvqrjtaqo` tag, types `kapcaakvb_b` and `yjgargdic_r`) are introduced — when the avatar collides with one, the `twkzhcfelv` push engine slides the plate (and any sprite carried) up to 11 cells in the plate's direction until a wall stops it.
  - The starting colour (12) differs from the target colour (9): the player must invoke the colour-cycler at least once.
- Specific challenge: Starting at (9,45) with shape=5, colour=12, rotation=0; the player must reach colour=9 (one colour-cycler hit at (29,45)), rotation=180 (two rotation-cycler hits at (49,10)), and end on the goal pad at (54,50). The two pushable plates create dynamic obstacles/shortcuts that must be navigated around (the engine spawns animated push events that lock the player out for `qeekhxkoad=8` frames per push).
- Estimated optimal action count: roughly 45-60 (long corridor, multiple cyclers, double-cost moves, possible plate detours).

Levels 4..7 exist but are excluded per skill scope.

## Action handlers

NovaBaseGame is constructed with `available_actions=[1, 2, 3, 4]`. The `step()` method (lines 1890-1992) dispatches based on `self.action.id`:

```
hnrvmfooc = 0; feyjbrwyb = 0; etvjlacrau = False
if   action == ACTION1: feyjbrwyb = -1; etvjlacrau = True
elif action == ACTION2: feyjbrwyb = +1; etvjlacrau = True
elif action == ACTION3: hnrvmfooc = -1; etvjlacrau = True
elif action == ACTION4: hnrvmfooc = +1; etvjlacrau = True
```

Note that `step()` first handles three pending-animation states before reaching the dispatch:
1. If `self.euemavvxz` (active push events) is non-empty, advance each push by one tick; when all complete, run `txnfzvzetn(player.x, player.y)` and `complete_action()`. Return.
2. If `self.ebfuxzbvn > 0` (life-loss flash counter), decrement; on reaching 0 hide overlay, show preview, `complete_action()`. Return.
3. If `self.akoadfsur > 0` (false-success flash counter), decrement; on reaching 0 reset badge and hide hint widgets, `complete_action()`. Return.

After dispatch sets a direction, the engine:
- Calls `arilbvrrme.step()` for each `dboxixicic` patroller (no-op in levels 1-3 because `wsoslqeku` is empty).
- Computes destination `(juldcpkjse, ullicjtklz) = (player.x + dx*5, player.y + dy*5)`.
- Calls `txnfzvzetn(juldcpkjse, ullicjtklz)` which scans sprites in that 5×5 region and may set `bwdzgjttjp` (blocked) and `yubyobdoss` (refilled).
- If not blocked, `player.set_position(dst)`. If blocked, undo all `dboxixicic.fwtnsrvkrz()` patroller moves.
- If a plate (`twkzhcfelv`) collision is detected via `prpxgfxlcm(player)`, append it to `euemavvxz` and return.
- If `pbznecvnfr()` returns True (all targets matched), call `next_level()` and `complete_action()`. Return.
- Else if `bkuguqrpvq` (a derived flag = "step counter hit zero this turn AND no refill"), trigger life loss: decrement `self.aqygnziho`; if 0 → `self.lose()`; else flash `aqdxgoyvu`, hide preview, restore counters, respawn player at `(ltwrkifkx, zyoimjaei)`. Return.
- Else `complete_action()`.

### ACTION1
- Trigger: `self.action.id == GameAction.ACTION1`.
- Branches inside `step()`: sets `feyjbrwyb = -1`, `etvjlacrau = True`. Then drops through to the common move pipeline: scan target cell, move if clear, handle interactors (cyclers, refill, plates), check win/lose.
- State mutations: reads `self.gudziatsk.x/y` (player pos), `self.gisrhqpee/tbwnoxqgc` (player size). Writes `self.gudziatsk` position; possibly `self.fwckfzsyc` (shape index), `self.hiaauhahz` (colour index), `self.cklxociuu` (rotation index), `self.aqygnziho` (lives), `self.ebfuxzbvn` (flash counter), `self.akoadfsur` (false-success counter), `self.lvrnuajbl` (per-target consumed flags), `self.euemavvxz` (push queue).
- Side effects on sprites: `gudziatsk.set_position(dst)`; on cycler hit, `htkmubhry.color_remap(...)`, `htkmubhry.set_rotation(...)`, or `htkmubhry.pixels = ...`. On false-success, `htkmubhry_2.color_remap(None, 0)`. On goal consumption, removes `plrpelhym[i]` and `srgbthxut[i]` from level. On refill, `current_level.remove_sprite(refill)`. On plate collision, `aqxtoxeino.move(dx,dy)` while plate animates.
- Engine effects: may call `self.next_level()` (level cleared via `pbznecvnfr`), `self.lose()` (lives==0), `self.complete_action()` (turn end).
- Pre-conditions / gating: rejected silently if destination cell contains a `ihdgageizm` wall or an unmatched goal pad (`rjlbuycveu` whose target predicate isn't satisfied — sets `bwdzgjttjp=True` AND triggers false-success flash).

### ACTION2
- Trigger: `self.action.id == GameAction.ACTION2`. Sets `feyjbrwyb = +1` (move down by `tbwnoxqgc=5` cells in y).
- Branches inside `step()`: identical pipeline to ACTION1 with feyjbrwyb=+1.
- State mutations / side effects / engine effects / gating: identical to ACTION1, but the destination is `(player.x, player.y+5)`.

### ACTION3
- Trigger: `self.action.id == GameAction.ACTION3`. Sets `hnrvmfooc = -1` (move left by 5 cells in x).
- Branches inside `step()`: identical pipeline.
- State mutations / side effects / engine effects / gating: identical to ACTION1; destination `(player.x-5, player.y)`.

### ACTION4
- Trigger: `self.action.id == GameAction.ACTION4`. Sets `hnrvmfooc = +1` (move right by 5 cells in x).
- Branches inside `step()`: identical pipeline.
- State mutations / side effects / engine effects / gating: identical; destination `(player.x+5, player.y)`.

ACTION5, ACTION6, ACTION7 are not registered. The source does not define handlers for them; if the harness sends one, the `etvjlacrau` flag stays False and the engine immediately calls `complete_action()` and returns (early-out at line 1933-1935).

## HUD widgets

One `RenderableUserDisplay` subclass: `hbuhvkxlhc` (lines 1470-1530).

- Class name: `hbuhvkxlhc` (constructed in `Ls20.__init__` as `self._step_counter_ui = hbuhvkxlhc(self, osgviligwp)` and registered via `Camera(interfaces=[self._step_counter_ui])`).
- Render-pixel range on the 64×64 frame:
  - Step bar: rows 61-62, columns 13 to 13+osgviligwp (osgviligwp = StepCounter from level, up to 42). Each step is 1 column wide × 2 rows tall, value 11 (cyan) for remaining or 3 (background) for spent. Actual columns used: 13-54 when osgviligwp=42.
  - Lives indicators: rows 61-62, columns 56,57 / 59,60 / 62,63 — 3 dots each 2×2, value 8 (red) if `self.aqygnziho > i`, value 3 otherwise.
  - Avatar preview (`htkmubhry`): rows 55..55+height, columns 3..3+width (rendered in fog mode only — `if vjhajnbdzr.oeuabekjf:` block). In levels 1-3 fog is False, so the avatar preview is not drawn by the HUD. The `wgmbtyhvbc` sprite at (3,55) — placed directly into the level — is what the player sees as the preview.
  - Fog overlay: when `oeuabekjf` is True, every pixel further than 20.0 from the player centre is overwritten with value 5 (gray fog). Levels 1-3 set `Fog: False`, so this branch is inactive.
- What value it displays: `self.current_steps` (remaining step budget) and `self.vjhajnbdzr.aqygnziho` (lives).
- Visual style: depleting horizontal bar (1-cell wide × 2-tall segments) for steps; 3 small 2×2 red dots for lives. Multi-cell mosaic.
- Update points:
  - `kbkdzqocik(value)` clamps `current_steps` to [0, max] — called on refill pickup (sets to max) and on life loss (resets to max).
  - `mfyzdfvxsm()` decrements `current_steps -= efipnixsvl`; called once per move from `step()`.
  - `vytykscvhe(efipnixsvl)` sets per-action decrement amount; called from `wbcenorpju()` whenever `on_set_level` (re)reads `StepsDecrement`.
  - `nzukewekzr()` resets to max on level set.
  - `aqygnziho` is mutated in `step()` directly (decrement on life loss; initialised to 3 in `on_set_level`).
- Where it is registered: `Camera(width=16, height=16, background=BACKGROUND_COLOR, letter_box=PADDING_COLOR, interfaces=[self._step_counter_ui])` in `Ls20.__init__`.

## Internal state — exhaustive

Attributes initialised on `self` in `__init__`, populated in `on_set_level`, or mutated by `step()` and helpers reachable from levels 1-3.

| attr (obfuscated) | semantic name | type | initial value | written by | read by | role |
|---|---|---|---|---|---|---|
| `_step_counter_ui` | step counter HUD | `hbuhvkxlhc` | `hbuhvkxlhc(self, levels[0]["StepCounter"])` | `__init__` only | `wbcenorpju`, `step`, `txnfzvzetn` | the HUD widget reference |
| `ijessuuig` | shape pool | `List[Sprite]` | 6-entry list of [gngifvjddu, fywfjzkxlm, mkfbgalsbe, nnjhdcanjk, grcpfuizfp, ubspnhafvq] | `__init__` only | `on_set_level`, `txnfzvzetn`, `qetwzqzzik` | source of avatar pixel templates |
| `tnkekoeuk` | colour cycle | `List[int]` | `[12, 9, 14, 8]` | `__init__` only | `on_set_level`, `txnfzvzetn`, `qetwzqzzik`, `step` | the 4-state colour cycle for avatar/goal |
| `dhksvilbb` | rotation cycle | `List[int]` | `[0, 90, 180, 270]` | `__init__` only | same as above | the 4-state rotation cycle |
| `oeuabekjf` | fog flag | `bool` | False | `__init__`, `on_set_level` (= `level.get_data("Fog")`) | `hbuhvkxlhc.render_interface` | enables fog-of-war overlay (False in L1-3) |
| `gudziatsk` | player avatar sprite | `Sprite` (`sfqyzhzkij`) | `on_set_level`: `current_level.get_sprites_by_tag("sfqyzhzkij")[0]` | `on_set_level`, `step` | `step`, `txnfzvzetn`, `pbznecvnfr`, `hbuhvkxlhc.render_interface` | physical avatar |
| `gisrhqpee` | avatar width | `int` | `gudziatsk.width` (= 5) | `on_set_level` | `step`, `txnfzvzetn` | move stride x |
| `tbwnoxqgc` | avatar height | `int` | `gudziatsk.height` (= 5) | `on_set_level` | `step`, `txnfzvzetn` | move stride y |
| `htkmubhry` | avatar preview sprite | `Sprite` (`wgmbtyhvbc`) | `current_level.get_sprites_by_tag("wgmbtyhvbc")[0]` | `on_set_level`, `qetwzqzzik`, `txnfzvzetn`, `step` | `hbuhvkxlhc.render_interface`, `step` | the HUD preview glyph |
| `htkmubhry_2` | badge background sprite | `Sprite` (`eqatonpohu`) | `current_level.get_sprites_by_tag("eqatonpohu")[0]` | `on_set_level`, `txnfzvzetn`, `step` | (none external) | flashes black on false-success |
| `tsynhckng` | badge frame sprite | `Sprite` (`ghizzeqtoh`) | `current_level.get_sprites_by_tag("ghizzeqtoh")[0]` | `on_set_level`, `vqfjzzkhid`, `step` | (rendered) | toggled visible by hint logic |
| `srgbthxut` | per-target expected-shape glyphs | `List[Sprite]` (`kvynsvxbpi` tagged) | from `get_sprites_by_tag("kvynsvxbpi")` | `on_set_level`, `step`, `pbznecvnfr` | `pbznecvnfr` | the small glyph showing what the goal expects |
| `plrpelhym` | per-target goal pads | `List[Sprite]` (`rjlbuycveu`) | from `get_sprites_by_tag("rjlbuycveu")` | `on_set_level`, `pbznecvnfr` | `txnfzvzetn`, `vqfjzzkhid`, `pbznecvnfr`, `step` | the goal pad sprites |
| `lvrnuajbl` | per-target consumed flags | `List[bool]` | `[False] * len(plrpelhym)` | `on_set_level`, `step`, `pbznecvnfr` | `vqfjzzkhid`, `pbznecvnfr` | flips to True when target met |
| `fwckfzsyc` | current shape index | `int` | `0` in on_set_level, then overwritten by `qetwzqzzik` from `StartShape` data | `on_set_level`, `qetwzqzzik`, `txnfzvzetn` | `bejndxqqzf`, `txnfzvzetn` | which shape the avatar currently is |
| `hiaauhahz` | current colour index | `int` | `0` then overwritten from `StartColor` | same | `bejndxqqzf`, `txnfzvzetn` | which colour the avatar is |
| `cklxociuu` | current rotation index | `int` | `0` then overwritten from `StartRotation` | same | `bejndxqqzf`, `txnfzvzetn` | which rotation |
| `drtdqwdbc` | grid width | `int` | `current_level.grid_size[0]` (=64) | `on_set_level` | (currently unused in step paths) | grid bounds |
| `qlgmdayuo` | grid height | `int` | `current_level.grid_size[1]` (=64) | `on_set_level` | (unused) | grid bounds |
| `ehwheiwsk` | per-target rotation index list | `List[int]` | per-target indices into `dhksvilbb` from `GoalRotation` | `on_set_level` | `bejndxqqzf` | expected rotation per target |
| `yjdexjsoa` | per-target colour index list | `List[int]` | per-target indices into `tnkekoeuk` from `GoalColor` | `on_set_level` | `bejndxqqzf` | expected colour per target |
| `ldxlnycps` | per-target shape index list | `List[int]` | from `level.get_data("kvynsvxbpi")` | `on_set_level` | `bejndxqqzf`, `on_set_level` | expected shape per target |
| `aqdxgoyvu` | life-loss flash overlay sprite | `Sprite` (`sqpmiygfvh`) clone | `on_set_level` adds clone, sets invisible | `on_set_level`, `step` | `hbuhvkxlhc.render_interface` (indirectly) | full-screen cyan flash |
| `aqygnziho` | lives | `int` | 3 | `on_set_level`, `step` | `hbuhvkxlhc.render_interface`, `step` | depletes on step-budget exhaustion; 0 → lose |
| `ofoahudlo` | refill pickups consumed this life | `List[Sprite]` | `[]` | `on_set_level`, `txnfzvzetn`, `step` | `step` (re-add on life loss) | for "rewind on death" |
| `byotxmvkt` | targets consumed this life | `List[Sprite]` | `[]` | `on_set_level`, `pbznecvnfr`, `step` | `step` (re-add on life loss) | targets restored if life lost mid-level |
| `alsxlhizr` | per-target glyphs consumed this life | `List[Sprite]` | `[]` | `on_set_level`, `pbznecvnfr`, `step` | `step` (re-add on life loss) | mirror of byotxmvkt for srgbthxut |
| `ebfuxzbvn` | life-loss flash counter | `int` | 0 | `on_set_level`, `step` | `step`, `hbuhvkxlhc.render_interface` | counts down 5 frames |
| `akoadfsur` | false-success flash counter | `int` | 0 | `on_set_level`, `txnfzvzetn`, `step` | `step` | counts down 5 frames |
| `ltwrkifkx` | respawn x | `int` | `gudziatsk.x` at level start | `on_set_level` | `step` (life-loss respawn) | initial player x |
| `zyoimjaei` | respawn y | `int` | `gudziatsk.y` at level start | `on_set_level` | `step` | initial player y |
| `wsoslqeku` | patroller list | `List[dboxixicic]` | built from xfmluydglp + cycler pairs (empty in L1-3) | `on_set_level`, `step` | `step` | moving cyclers |
| `hasivfwip` | pushable plate engines | `List[twkzhcfelv]` | one per `gbvqrjtaqo` sprite | `on_set_level`, `step` | `step` | plate push-back logic |
| `euemavvxz` | active push animations | `List[xajlyftlyn]` | `[]` | `on_set_level`, `step` | `step` | queue of in-progress pushes |
| `_levels` (inherited) | level list | `List[Level]` | from base | `on_set_level` clones from `_clean_levels` | base | levels |
| `_clean_levels` (inherited) | clean snapshots | `List[Level]` | from base | (read only) | `on_set_level` | source of truth for re-clone |
| `_current_level_index` (inherited) | active level index | `int` | from base | base | `on_set_level`, `vqfjzzkhid` | which level is active |

## Win condition

The win predicate is `pbznecvnfr()` (lines 2020-2038):
1. For each goal pad index `i`, if not already consumed (`lvrnuajbl[i]` False) AND avatar is exactly on top of the pad (`gudziatsk.x == plrpelhym[i].x AND gudziatsk.y == plrpelhym[i].y`) AND `bejndxqqzf(i)` (avatar's current shape, colour, and rotation indices match the per-target expected indices): mark consumed (`lvrnuajbl[i] = True`), remove the pad and the expected-glyph sprite from the level, and hide the corresponding `vjotnebuqo`/`hoswmpiqkw` sprites if they carry the `vfkkzdgxzx` tag.
2. After scanning, if every entry in `lvrnuajbl` is True, return True.

In `step()` (lines 1956-1959), if `pbznecvnfr()` returns True, the engine calls `self.next_level()` and `self.complete_action()`.

`bejndxqqzf(i)` (line 2017-2018): `self.fwckfzsyc == self.ldxlnycps[i] AND self.hiaauhahz == self.yjdexjsoa[i] AND self.cklxociuu == self.ehwheiwsk[i]`.

Win conditions across levels 1-3 are structurally identical: arrive at the goal pad with matching shape, colour, and rotation. The specific (shape, colour, rotation) tuple differs per level via the level data.

## Lose condition

In `step()` lines 1960-1965: if `bkuguqrpvq` is True (computed as `not yubyobdoss and not _step_counter_ui.mfyzdfvxsm()` — i.e. no refill picked up this step AND the step counter hit zero or below), then `self.aqygnziho -= 1`. If `self.aqygnziho == 0`, call `self.lose()` and `self.complete_action()`.

So lose = "step counter ran out 3 times without ever winning a level". Each intermediate failure (lives 3 → 2 → 1) instead respawns the player at `(ltwrkifkx, zyoimjaei)`, restores consumed targets and refills, resets the step counter to max, and triggers a 5-frame cyan flash via `aqdxgoyvu`.

The avatar can never be killed by collision with a wall or hazard — the maze blocks movement but does not deplete lives.

## Resource economy

- Depleting resource: YES — step counter.
  - Variable: `self._step_counter_ui.current_steps`, max `osgviligwp` (= `StepCounter` level-data, 42 in all of L1-3).
  - Visual representation: cyan horizontal bar at rows 61-62 in the bottom-left HUD bay.
  - Trigger to deplete: `_step_counter_ui.mfyzdfvxsm()` is called once per successful action, decrementing by `efipnixsvl` (= `StepsDecrement` from level data, default 2; level 1 sets it to 1).
  - Threshold: when `current_steps < 0` AND no refill consumed, this counts as a "depletion event" → life loss.
  - Refill: `npxgalaybz` pickups (level 2: 2 of them; level 3: 2; level 1: 0) reset `current_steps` to max via `kbkdzqocik(osgviligwp)`.
- Accumulating resource: YES — per-target consumption progress (`lvrnuajbl`).
  - Variable: `self.lvrnuajbl`, a list of bools, one per `rjlbuycveu` goal pad.
  - Visual: the goal pad and its expected-glyph sprite are removed from the level when consumed; in some configurations `vjotnebuqo` rings hide. Levels 1-3 each have exactly 1 goal, so this collapses to "0 / 1".
  - Trigger to accumulate: avatar steps onto a goal pad with matching configuration (`pbznecvnfr` predicate) → `lvrnuajbl[i] = True`.
  - Threshold for winning: all entries True → `next_level()`.
- Lives mechanic: YES — 3 lives.
  - `self.aqygnziho = 3` initialised in `on_set_level`.
  - A life is lost when the step counter depletes without a refill that turn.
  - Final game-over when `aqygnziho` hits 0 → `self.lose()`.
- Resource interaction: depletion (step bar) feeds the lives counter; lives ≥ 1 → respawn with full step counter and restored level state. Lives = 0 → game over. Accumulating resource (targets consumed) gates next-level transition. The accumulating resource is per-life-revertible: on respawn, `byotxmvkt` and `alsxlhizr` are re-added to the level (consumed targets reappear).

## Action-budget signature

- Default budget per level: 42 steps (`StepCounter: 42` in all three documented levels' `data={...}`).
- Whether budget tightens or shifts across levels 1-3:
  - Level 1: 42 steps, decrement = 1 per action → effectively 42 moves.
  - Level 2: 42 steps, decrement = 2 (default) → effectively 21 moves.
  - Level 3: 42 steps, decrement = 2 → effectively 21 moves.
  So the budget tightens between L1 and L2 (per-action cost doubles) and stays tight at L3.
- Per-level vs. per-environment: per-level (each `on_set_level` calls `wbcenorpju` to re-read `StepCounter` and `StepsDecrement` from the level's `data` dict and reset `current_steps`).
- Decrement rate per action: 1 if `StepsDecrement: 1` is in level data, otherwise 2 (default in `wbcenorpju`).
- Refill mechanism: `npxgalaybz` pickups reset `current_steps` to max on contact (consumed pickup is removed from level and stashed for life-loss restoration).

## Notable code patterns / techniques

- **Tag-based polymorphism in `txnfzvzetn`**: a single helper (`mrznumynfe(x, y, w, h)`) returns sprites overlapping a 5×5 region; the helper then dispatches on `mvcsnkcqz.tags` membership (`"ihdgageizm"` → wall, `"rjlbuycveu"` → goal, `"npxgalaybz"` → refill, `"ttfwljgohq"` → shape-cycler, `"soyhouuebz"` → colour-cycler, `"rhsxkxzdjz"` → rotation-cycler). Adding a new interactor type is a matter of adding a tagged sprite and a new branch.
- **Direction encoded in sprite name suffix**: `twkzhcfelv` reads the last char of `sprite.name` (`_t`, `_b`, `_l`, `_r`) to set push direction `(dx, dy)`. This couples sprite identity to behaviour without extra metadata.
- **Per-life rewind via pop-stack lists**: `ofoahudlo`, `byotxmvkt`, `alsxlhizr` accumulate sprites the player consumed during this life; on life loss, they are re-`add_sprite`d to the level. This is a clean "save state at level start, restore on retry" without a deep level clone.
- **Avatar identity = mutable shape/colour/rotation indices**: `self.fwckfzsyc/hiaauhahz/cklxociuu` decouple the visible avatar state from its on-board sprite. The avatar sprite's pixels and rotation are recomputed by `qetwzqzzik` from these indices, so the game logic only ever compares small integers.
- **Push animation as a coroutine queue**: `step()` checks `if self.euemavvxz` first; while non-empty, the engine ticks the animation queue and short-circuits the action. Cubic easing (`mfnyvivrar`) gives smooth visuals while the player is locked out for `qeekhxkoad=8` frames.
- **HUD widget reads game-class attributes directly**: `hbuhvkxlhc.render_interface(frame)` accesses `self.vjhajnbdzr.gudziatsk.x/y` (player position) and `self.vjhajnbdzr.aqygnziho` (lives). The HUD widget holds a back-reference to the game object — straightforward but creates strong coupling.
- **Hint highlighting via `vqfjzzkhid()`**: when the avatar's configuration matches a target's expected configuration (and the target is not yet consumed), the engine sets a hidden `hoswmpiqkw` ring visible. This is an active hint to the planner: "you're now correctly configured, walk to here".
- **`get_sprite_at(x-1, y-1, tag)`** (`pbznecvnfr` and `vqfjzzkhid`): the engine queries the level for a tagged sprite at a position offset by (-1, -1) — likely because the goal-ring sprites are placed one cell up-left of the goal pads they frame.

## Anti-patterns / lessons

- 80-110+ wall sprites per level: the playfield is densely tiled with `ihdgageizm` 5×5 walls. A generated 3-level game should not require this many sprite placements to define a maze; consider procedural wall generation or larger wall tiles.
- Five wall variants (`ihdgageizm`, `fesygzfqui`, `krdypjjivz`, `mxfhnkdzvf`, `ubyunwkbpx`) that all share the same tag and look near-identical at scale. A generated game should pick one wall sprite and stick with it.
- The runtime player sprite (`gudziatsk`, derived from `sfqyzhzkij`) and the HUD preview sprite (`htkmubhry`, derived from `wgmbtyhvbc`) are different sprites — but the player's *visual identity* (shape pixels, colour, rotation) is set on the HUD preview, not on the on-board avatar. The on-board avatar always renders as the literal `sfqyzhzkij` (12+9 stripes). This means the player must look at the HUD widget to see what shape/colour/rotation they currently are. A generated game should either keep the avatar's visual in sync or pick one canonical visual and not split.
- Six candidate avatar shapes (`gngifvjddu`/`fywfjzkxlm`/`mkfbgalsbe`/`nnjhdcanjk`/`grcpfuizfp`/`ubspnhafvq`) are all tiny 3×3 glyphs that share value 0 + value -1 — visually indistinguishable in a thumbnail. A generated game with a shape-matching mechanic should use bolder, larger, more distinctive glyphs.
- The colour-matching mechanic mixes palette index 8 (red) into the cycle alongside 12, 9, 14 — risks the cultural "red = danger" association even though red here means just one of four states.
- The hint-ring (`hoswmpiqkw`) only fires for level 0 (`vqfjzzkhid` early-returns when `level_index > 0`), so levels 2 and 3 lose a major UX cue. A generated game should either fire hints on all levels or remove the hint mechanic entirely.
- The rendering uses a Camera with `width=16, height=16` but the actual frame produced is 64×64 pixels (HUD, frame, etc., draw to a 64×64 array). This means `Camera(width=16, height=16)` is a logical sub-window; downstream agents need to handle the "1 cell = 4 pixels" zoom. A simpler generated game might prefer `width=64, height=64` and 1:1 pixel mapping.
- Sprite naming convention is fully obfuscated random tokens. While necessary for the dataset, generated games' level definitions become unreadable; the directional plate trick (`_t/_b/_l/_r` suffix as behaviour) reads as a hack on top of opaque names.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES (rows 61-62, columns 13..54 in the bottom-left HUD bay).
- Has lives mechanic: YES (3 lives; tracked in `self.aqygnziho`).
- Has click-to-select (uses ACTION6): NO (ACTION6 is not in `available_actions`).
- Has tag-based grouping (uses `level.get_sprites_by_tag`): YES (extensively, in `on_set_level`, `txnfzvzetn`, `vqfjzzkhid`, `pbznecvnfr`, `step`).
- Uses ACTION5 (modal): NO.
- Uses ACTION6 (click): NO.
- Uses ACTION7: NO.
- Has level data dicts (uses `level.get_data` / `level.set_data`): YES (`level.get_data` for `StepCounter`, `StepsDecrement`, `kvynsvxbpi`, `GoalColor`, `GoalRotation`, `StartShape`, `StartColor`, `StartRotation`, `Fog`).
- Multi-mechanic per level (vs. single mechanic per level): YES — level 1 has movement + rotation cycler; level 2 adds refill pickups; level 3 adds colour cycler + pushable plates. Each level layers on a new mechanic.
- Tutorial level appears solvable by random play: NO — even with `StepsDecrement: 1` (42 moves) and 3 lives, the player must navigate a tight corridor and invoke a specific cycler exactly once before reaching the goal; random walk is unlikely to satisfy the (shape, colour, rotation) predicate at the right cell within 42 × 3 = 126 actions.
- Has a depleting resource: YES — kind: step counter (with refills).
- Has an accumulating resource: YES — kind: per-target consumed flags (with revert-on-life-loss).
- Sprite shape convention used: mixed (filled walls + hollow rings + tiny glyphs + striped plates + textured interactors).
- HUD position: bottom (specifically bottom-left, rows 51-63, cols 0-63).
- Palette size used: 10 (distinct palette values appearing in any sprite, excluding `-1` transparent and `-2` engine padding: {0, 1, 3, 4, 5, 8, 9, 11, 12, 14}).
- Background colour value: 3.
- Padding / letter-box colour value: 3.
- Number of distinct mechanics introduced across levels 1-3: 4 (basic movement + rotation cycler at L1; step-refill pickups at L2; colour cycler + pushable plates at L3).
- Number of levels documented: 3.

(End of file.)
