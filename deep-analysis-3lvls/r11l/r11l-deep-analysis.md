# r11l — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/r11l/aa269680/r11l.py`
- Lines: 1822
- Class name: `R11l`
- available_actions: `[6]` (only `GameAction.ACTION6`, the click action)
- Number of levels in source: 6
- Number of levels documented in this analysis: 3
- Imports: `ActionInput`, `NovaBaseGame`, `Camera`, `GameAction`, `Level`, `RenderableUserDisplay`, `Sprite` from `novaengine`; `numpy as np`; `TypedDict` from `typing`.

## Mechanic essence (one sentence)

A pink-eyed colored ring hovers at the average of two or three matching colored footprints, and clicking a footprint and then clicking a destination drags it across a winding corridor — sliding the ring with it — until every ring sits inside its same-colored target ring without straying into the cyan no-go zone.

## Sprite roster

| sprite (obfuscated) | dims | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| `bdkaz-kpaac` | 5x5 | 6, 15, -1 | (default) | 1 | YES | (default) | YES | white head ring with pink eye (white-team head) |
| `bdkaz-pgknepyzud` | 5x5 | 6, 8, 9, -1 | (default) | 1 | YES | (default) | YES | half-azure half-blue head ring (level 4+) |
| `bdkaz-qniqj` | 5x5 | 6, 12, -1 | (default) | 1 | YES | (default) | YES | purple head ring with pink eye |
| `bdkaz-qniqjgigctpgknekpaac` | 5x5 | 6, 12, 14, 15, -1 | (default) | 1 | YES | (default) | YES | mixed purple/orange/white head (level 4+) |
| `bdkaz-ttyiazjgrp` | 5x5 | 6, 11, 14, -1 | (default) | 1 | YES | (default) | YES | green/orange head (level 4+) |
| `bdkaz-yukft` | 5x5 | 0, -1 | (default) | 1 | YES | (default) | YES | black head ring (level 5+) |
| `bdkaz-yukft-2` | 5x5 | 0, -1 | (default) | 1 | YES | (default) | YES | duplicate black head (level 5+) |
| `bdkaz-zjgrp` | 5x5 | 6, 14, -1 | (default) | 1 | YES | (default) | YES | orange head ring with pink eye |
| `bdkazLeg-kpaac` | 5x5 | 0, 15, -1 | sys_click | (default) | YES | (default) | YES | white footprint (clickable) |
| `bdkazLeg-pgknepyzud` | 5x5 | 0, 9, -1 | sys_click | (default) | YES | (default) | YES | blue footprint (level 4+) |
| `bdkazLeg-qniqj` | 5x5 | 0, 12, -1 | sys_click | (default) | YES | (default) | YES | purple footprint |
| `bdkazLeg-qniqjgigctpgknekpaac` | 5x5 | 0, 15, -1 | sys_click | (default) | YES | (default) | YES | mixed-team footprint (level 4+) |
| `bdkazLeg-ttyiazjgrp` | 5x5 | 0, 14, -1 | sys_click | (default) | YES | (default) | YES | orange-tinted footprint (level 4+) |
| `bdkazLeg-yukft` | 5x5 | 0, 4, -1 | sys_click | (default) | YES | (default) | YES | yellow-cored footprint (level 5+) |
| `bdkazLeg-yukft-2` | 5x5 | 0, 4, -1 | sys_click | (default) | YES | (default) | YES | duplicate yellow-cored footprint (level 5+) |
| `bdkazLeg-zjgrp` | 5x5 | 0, 14, -1 | sys_click | (default) | YES | (default) | YES | orange footprint |
| `bvzgd-Level1` | 73x73 | 2, -1 | (default) | 2 | YES | (default) | YES | red corridor wall outline (used L1, L2) |
| `bvzgd-Level5` | 73x73 | 2, -1 | (default) | 2 | YES | (default) | YES | red corridor wall outline (used L3, L5, L6) |
| `bvzgd-Level6` | 73x73 | 2, -1 | (default) | 2 | YES | (default) | YES | red corridor wall outline (unused in L1-3) |
| `bvzgd-Level7` | 73x73 | 2, -1 | (default) | 2 | YES | (default) | YES | red corridor wall outline (level 4+ only) |
| `kzeze-anqcf` | 7x7 | 15, -1 | (default) | (default) | YES | (default) | YES | hollow X-shaped target token (level 4+) |
| `kzeze-kpaac` | 7x7 | 15, -1, -2 | (default) | (default) | YES | (default) | YES | white target ring (filled diamond w/ white border) |
| `kzeze-kpaaczjgrppgkne` | 7x7 | 9, 14, 15, -1, -2 | (default) | (default) | YES | (default) | YES | tri-color target ring (level 6) |
| `kzeze-pgknepyzud` | 7x7 | 8, 9, -1, -2 | (default) | (default) | YES | (default) | YES | azure/blue target ring (level 4+) |
| `kzeze-qniqj` | 7x7 | 12, -1, -2 | (default) | (default) | YES | (default) | YES | purple target ring |
| `kzeze-qniqjgigctpgknekpaac` | 7x7 | 12, 14, 15, -1, -2 | (default) | (default) | YES | (default) | YES | tricolored target ring (level 4+) |
| `kzeze-ttyiaPinkpgkne` | 7x7 | 6, 10, 11, -1, -2 | (default) | (default) | YES | (default) | YES | pink/green/cyan target (level 6) |
| `kzeze-ttyiazjgrp` | 7x7 | 11, 14, -1, -2 | (default) | (default) | YES | (default) | YES | green/orange target (level 4+) |
| `kzeze-zjgrp` | 7x7 | 14, -1, -2 | (default) | (default) | YES | (default) | YES | orange target ring |
| `mpjrv-bdkaz` | 5x5 | 0, -1 | (default) | 100 | YES | (default) | YES | black pulse halo around head (collision warning) |
| `mpjrv-kzeze` | 7x7 | 0, -1 | (default) | (default) | YES | (default) | YES | black pulse halo around target ring (settle warning) |
| `qtwnv-Level2` | 35x40 | 10, -1 | (default) | (default) | YES | (default) | YES | cyan no-go region for L2 |
| `qtwnv-Level3` | 73x44 | 10, -1 | (default) | (default) | YES | (default) | YES | cyan no-go region for L2 (used at level index 1) |
| `qtwnv-Level4` | varies | 10, -1 | (default) | (default) | YES | (default) | YES | cyan no-go region (level 4+) |
| `qtwnv-Level5` | varies | 10, -1 | (default) | (default) | YES | (default) | YES | cyan no-go region for L3 |
| `qtwnv-Level7` | varies | 10, -1 | (default) | (default) | YES | (default) | YES | cyan no-go region (level 4+ only) |
| `txxvz-anqcf` | 3x7 | 10, -1 | (default) | (default) | YES | (default) | YES | small cyan X marker (level 4+ only) |
| `xigcb-gigctpgknezzepw` | 5x5 | 0, 10, -1 | (default) | (default) | YES | (default) | YES | half-cyan paint stamp (level 5+) |
| `xigcb-kpaaczzepw` | 5x5 | 0, 15, -1 | (default) | (default) | YES | (default) | YES | half-white paint stamp (level 6) |
| `xigcb-Maroon` | 5x5 | 0, 13, -1 | (default) | (default) | YES | (default) | YES | half-maroon paint stamp (level 6) |
| `xigcb-pgknezzepw` | 5x5 | 0, 8, -1 | (default) | (default) | YES | (default) | YES | half-azure paint stamp (level 6) |
| `xigcb-qniqj` | 5x5 | 0, 12, -1 | (default) | (default) | YES | (default) | YES | half-purple paint stamp (level 6) |
| `xigcb-ttyiazzepw` | 5x5 | 0, 11, -1 | (default) | (default) | YES | (default) | YES | half-green paint stamp (level 6) |
| `xigcb-txxvzpgkne` | 5x5 | 0, 9, -1 | (default) | (default) | YES | (default) | YES | half-blue paint stamp (level 5+) |
| `xigcb-txxvzpgkneBottom` | 5x5 | 0, 9, -1 | (default) | (default) | YES | (default) | YES | half-blue paint stamp (level 6) |
| `xigcb-txxvzPink` | 5x5 | 0, 6, -1 | (default) | (default) | YES | (default) | YES | half-pink paint stamp (level 6) |
| `xigcb-txxvzpyzud` | 5x5 | 0, 8, -1 | (default) | (default) | YES | (default) | YES | half-azure paint stamp (level 5+) |
| `xigcb-txxvzttyia` | 5x5 | 0, 11, -1 | (default) | (default) | YES | (default) | YES | half-green paint stamp (level 5+) |
| `xigcb-txxvzzjgrp` | 5x5 | 0, 14, -1 | (default) | (default) | YES | (default) | YES | half-orange paint stamp (level 5+) |
| `xigcb-zjgrp` | 5x5 | 0, 14, -1 | (default) | (default) | YES | (default) | YES | half-orange paint stamp (level 6) |

### `bdkaz-kpaac` — white "head" ring (eye visible)
- Pixel pattern: 5x5 hollow rounded square in palette 15 (white) with a single palette-6 (pink) pixel at center; corners (-1) are transparent so it reads as a soft ring.
- Where it appears: Level 1 (1 copy, center of corridor); Level 2 (1 copy of `kpaac` + 1 of `qniqj`); Level 3 (1 copy of `kpaac` + 1 of `zjgrp`).
- Role: passive **head** sprite (`kignw` in `brdck`). It is repositioned by `bdahxidrjf` to the centroid of its colored footprints. The win predicate requires it to overlap its same-colored target ring (`xwdrv`).
- Visual-vs-functional read: a player sees a white-bordered face with a pink eye and intuitively thinks it is the avatar — but the player **cannot click it directly**; only the small footprint plus-glyphs (`bdkazLeg-*`) accept input. The head is an *output* puppet, not the controlled entity. This is the central visual-vs-functional twist of the game.
  - At-rendered-scale shape: hollow rounded square with a single dot.
  - Palette signature: 15 (white) + 6 (pink). The pink center is shared with all other `bdkaz-*` head sprites.
  - Nearest-other-sprite check: confused with `kzeze-kpaac` (also white, also a 7x7 disc with pink-eye-like core appearance) — the kzeze target however has a *filled* white interior rather than a hollow ring, and is one cell taller/wider. Players distinguish by "filled vs ringed" silhouette.
- Visual contrast notes: white (15) sits clearly on the palette-5 grey background and on the palette-2 red corridor outline; pink center adds focal accent.

### `bdkaz-pgknepyzud` — azure/blue head ring (level 4+ only — listed for roster completeness)
- Pixel pattern: 5x5 ring split diagonally between palette 9 (blue) on the left/bottom and palette 8 (azure) on the right/top, pink (6) eye.
- Where it appears: Level 4 only. Not used in levels 1-3.
- Role: same head-puppet role as `bdkaz-kpaac` for the blue/azure team in level 4+.
- Visual-vs-functional read: looks like one bicolor avatar but plays the same passive role as any other head; not directly clickable.
  - At-rendered-scale shape: hollow ring, two-tone halves.
  - Palette signature: 8, 9, 6. The dual-tone signature visually marks "team =  pgknepyzud".
  - Nearest-other-sprite check: the matching `kzeze-pgknepyzud` target ring is also two-tone azure/blue but filled; player distinguishes filled vs hollow.
- Visual contrast notes: bicolor break is distinctive against background and against monochrome heads.

### `bdkaz-qniqj` — purple head ring
- Pixel pattern: 5x5 hollow ring in palette 12 (purple) with palette-6 (pink) eye.
- Where it appears: Level 2 (1 copy).
- Role: head-puppet for the purple team, pinned to its three purple footprints.
- Visual-vs-functional read: indistinguishable in mechanic from `bdkaz-kpaac`; only the color tells the player which footprints belong to which head.
  - At-rendered-scale shape: hollow ring with central dot.
  - Palette signature: 12, 6.
  - Nearest-other-sprite check: vs `kzeze-qniqj` — same hue, distinguished by filled-vs-hollow silhouette and 7x7 vs 5x5 size.
- Visual contrast notes: purple is high contrast against grey background.

### `bdkaz-qniqjgigctpgknekpaac` — mixed purple/orange/white head (level 4+)
- Pixel pattern: 5x5 ring with diagonal palette gradient (12 purple top-left, 14 orange middle-right, 15 white bottom).
- Where it appears: Level 4 only.
- Role: head-puppet for the multi-color team.
- Visual-vs-functional read: tri-color appearance can suggest "compound" or "boss" entity, but mechanically identical to all other heads.
  - At-rendered-scale shape: hollow ring with diagonal color stripes.
  - Palette signature: 12, 14, 15, 6.
  - Nearest-other-sprite check: `kzeze-qniqjgigctpgknekpaac` mirrors the same colors as a target.
- Visual contrast notes: gradient distinguishes from monochrome heads.

### `bdkaz-ttyiazjgrp` — green/orange head (level 4+)
- Pixel pattern: 5x5 hollow ring with palette 14 (orange) on the left half and palette 11 (green) on the right half, pink (6) eye.
- Where it appears: Level 4 only.
- Role: head-puppet for green/orange team.
- Visual-vs-functional read: bicolor head, otherwise identical role.
  - At-rendered-scale shape: hollow ring with two color zones.
  - Palette signature: 11, 14, 6.
  - Nearest-other-sprite check: `kzeze-ttyiazjgrp` is the matching filled target.
- Visual contrast notes: green/orange split distinctive against red corridor outline (could blend slightly with red boundaries near orange edges).

### `bdkaz-yukft` — black head ring (level 5+)
- Pixel pattern: 5x5 ring entirely in palette 0 (black), no pink eye — interior is also black.
- Where it appears: Level 5 only (also `bdkaz-yukft-2`).
- Role: head-puppet for the "yukft" team.
- Visual-vs-functional read: solid black silhouette is striking; no eye marker.
  - At-rendered-scale shape: solid filled black square at small scale.
  - Palette signature: only 0.
  - Nearest-other-sprite check: `mpjrv-bdkaz` (collision-pulse halo) is also a black 5x5 ring with similar shape — but pulses on/off rather than persists.
- Visual contrast notes: very high contrast on grey background, but visually confusable with the warning halo `mpjrv-bdkaz`.

### `bdkaz-yukft-2` — duplicate black head (level 5+)
- Pixel pattern: identical to `bdkaz-yukft`.
- Where it appears: Level 5 only.
- Role: duplicate head with a distinct name so two black-team heads can coexist; allows `brdck` to track them as separate "color" groups.
- Visual-vs-functional read: visually identical to `bdkaz-yukft`; players distinguish by spatial proximity to associated footprints rather than by appearance.
  - At-rendered-scale shape: solid black square.
  - Palette signature: 0.
  - Nearest-other-sprite check: `bdkaz-yukft` — completely indistinguishable visually; only the name suffix `-2` separates them in `brdck` keys.
- Visual contrast notes: identical to its twin, hence ambiguous.

### `bdkaz-zjgrp` — orange head ring with pink eye
- Pixel pattern: 5x5 hollow ring in palette 14 (orange), pink (6) center.
- Where it appears: Level 3 (1 copy).
- Role: head-puppet for the orange team.
- Visual-vs-functional read: head; not clickable; mechanically identical to `bdkaz-kpaac`.
  - At-rendered-scale shape: hollow ring with eye.
  - Palette signature: 14, 6.
  - Nearest-other-sprite check: vs `kzeze-zjgrp` (filled orange target), distinguished by filled-vs-hollow.
- Visual contrast notes: orange is close to palette-2 red of the corridor outline — players may briefly mis-read it as part of the wall.

### `bdkazLeg-kpaac` — white footprint (clickable)
- Pixel pattern: 5x5 plus-shape in palette 0 (black) with single palette-15 (white) center pixel; corners transparent.
- Where it appears: Level 1 (2 copies); Level 2 (2 copies); Level 3 (2 copies). At least 2 per head for centroid.
- Role: clickable **footprint** (`mdpcc` in `brdck`). Selecting one with a click colors it inverted (palette 3 = green-ish from `color_remap(0,3)` → restored on deselect). A second click moves it; the head re-centers on the centroid of all its footprints.
- Visual-vs-functional read: small black plus sign with a colored dot in the middle reads naturally as a "footstep print" — and that intuition is exactly correct here.
  - At-rendered-scale shape: black plus glyph with a small color core.
  - Palette signature: 0, 15. After selection it flips to palette 3 (a greenish hue) — that flip is the only "selected" feedback.
  - Nearest-other-sprite check: vs `bdkazLeg-qniqjgigctpgknekpaac` (also white-cored) and `bdkazLeg-pgknepyzud` (blue-cored) — the **only** distinguishing feature is the 1x1 center pixel color, which is hard to read at 64×64 frame scale.
- Visual contrast notes: the plus-shape is consistent across all leg variants, so players must rely on the central core color or proximity to a same-color head to associate legs to teams.

### `bdkazLeg-pgknepyzud` — blue footprint (level 4+)
- Pixel pattern: 5x5 black plus glyph, palette-9 (blue) center pixel.
- Where it appears: Level 4 only.
- Role: clickable footprint for the blue team (level 4+).
- Visual-vs-functional read: same plus-shape; team identified by 1×1 color core.
  - At-rendered-scale shape: plus.
  - Palette signature: 0, 9.
  - Nearest-other-sprite check: all other `bdkazLeg-*` glyphs share the plus silhouette; distinguishable only by core color.
- Visual contrast notes: same as `bdkazLeg-kpaac`.

### `bdkazLeg-qniqj` — purple footprint
- Pixel pattern: 5x5 black plus, palette-12 (purple) core.
- Where it appears: Level 2 (3 copies).
- Role: clickable footprint for the purple team.
- Visual-vs-functional read: plus glyph, purple core dot.
  - At-rendered-scale shape: plus.
  - Palette signature: 0, 12.
  - Nearest-other-sprite check: shared plus silhouette across all `bdkazLeg-*`.
- Visual contrast notes: 1-pixel purple core is small but readable on grey.

### `bdkazLeg-qniqjgigctpgknekpaac` — multi-team footprint (level 4+)
- Pixel pattern: 5x5 plus, palette-15 (white) core (note: this looks identical to `bdkazLeg-kpaac` despite being a separate sprite).
- Where it appears: Level 4 only.
- Role: footprint for the multi-color team. The visual identity to `bdkazLeg-kpaac` is potentially confusing.
- Visual-vs-functional read: visually identical at small scale to `bdkazLeg-kpaac`, but functionally bound to a different head.
  - At-rendered-scale shape: plus glyph.
  - Palette signature: 0, 15.
  - Nearest-other-sprite check: indistinguishable from `bdkazLeg-kpaac` — players must use spatial association with the head color to disambiguate.
- Visual contrast notes: colors identical to `bdkazLeg-kpaac`.

### `bdkazLeg-ttyiazjgrp` — orange-tinted footprint (level 4+)
- Pixel pattern: 5x5 plus, palette-14 (orange) core.
- Where it appears: Level 4 only.
- Role: footprint for the orange/green team.
- Visual-vs-functional read: orange-cored plus.
  - At-rendered-scale shape: plus.
  - Palette signature: 0, 14.
  - Nearest-other-sprite check: visually identical to `bdkazLeg-zjgrp` (also orange center).
- Visual contrast notes: same as other legs.

### `bdkazLeg-yukft` — yellow-cored footprint (level 5+)
- Pixel pattern: 5x5 plus, palette-4 (yellow) core.
- Where it appears: Level 5 only.
- Role: footprint for one of the two yukft teams.
- Visual-vs-functional read: plus with yellow dot core.
  - At-rendered-scale shape: plus.
  - Palette signature: 0, 4.
  - Nearest-other-sprite check: identical to `bdkazLeg-yukft-2`.
- Visual contrast notes: yellow vs grey background reads well, but yellow vs ambient palette-5 noise can be subtle.

### `bdkazLeg-yukft-2` — duplicate yellow footprint (level 5+)
- Pixel pattern: identical to `bdkazLeg-yukft`.
- Where it appears: Level 5 only.
- Role: footprint for the second yukft team. Matches its `bdkaz-yukft-2` head.
- Visual-vs-functional read: visually indistinguishable from `bdkazLeg-yukft`; player must use proximity to the head.
  - At-rendered-scale shape: plus.
  - Palette signature: 0, 4.
  - Nearest-other-sprite check: `bdkazLeg-yukft` — fully identical.
- Visual contrast notes: same as twin.

### `bdkazLeg-zjgrp` — orange footprint
- Pixel pattern: 5x5 plus, palette-14 (orange) core.
- Where it appears: Level 3 (4 copies).
- Role: footprint for the orange team in level 3.
- Visual-vs-functional read: plus with orange core dot.
  - At-rendered-scale shape: plus.
  - Palette signature: 0, 14.
  - Nearest-other-sprite check: same hue as `bdkazLeg-ttyiazjgrp`.
- Visual contrast notes: orange center on dark plus on grey is readable.

### `bvzgd-Level1` — large red corridor outline (used L1, L2)
- Pixel pattern: 73×73 sparse mosaic of palette-2 (red) cells forming an irregular boomerang/L corridor outline; the rest is transparent (-1).
- Where it appears: Level 1 (clone at (-5,-6)); Level 2 (clone at (-6,-10) mirrored left-right).
- Role: visual **playfield boundary / wall**. The collision check `tkdffrbsnv` rejects any move that would let the selected leg overlap any `bvzgd-*` sprite — i.e. the leg cannot leave the corridor interior.
- Visual-vs-functional read: looks like a stylized red shoreline / map outline; functions as a hard wall. The visual reading as "boundary" matches its function.
  - At-rendered-scale shape: jagged irregular outline (textured ribbon of red cells).
  - Palette signature: 2.
  - Nearest-other-sprite check: vs other `bvzgd-Level*` siblings — same role, only the contour shape differs.
- Visual contrast notes: red against grey background is high-contrast; sits at layer=2 above other sprites' default layers, so it draws on top.

### `bvzgd-Level5` — red corridor outline (used L3 and beyond)
- Pixel pattern: 73×73 sparse mosaic of palette-2 cells — different boomerang shape than `bvzgd-Level1`.
- Where it appears: Level 3 (mirrored).
- Role: same as `bvzgd-Level1` — playfield wall for level 3.
- Visual-vs-functional read: jagged red border = wall; matches.
  - At-rendered-scale shape: jagged irregular outline.
  - Palette signature: 2.
  - Nearest-other-sprite check: other `bvzgd-Level*`.
- Visual contrast notes: same as `bvzgd-Level1`.

### `bvzgd-Level6` — red corridor outline (unused in L1-3)
- Pixel pattern: 73×73 jagged red outline with a different shape.
- Where it appears: not used in levels 1-3; defined but only referenced for later levels (skill scope: ignore).
- Role: would be playfield wall for some later level.
- Visual-vs-functional read: same as other `bvzgd-*`.
  - At-rendered-scale shape: jagged outline.
  - Palette signature: 2.
  - Nearest-other-sprite check: other `bvzgd-Level*`.
- Visual contrast notes: red on grey.

### `bvzgd-Level7` — red corridor outline (level 4+ only)
- Pixel pattern: 73×73 jagged red outline.
- Where it appears: Level 4 (clone), Level 5 (rotated 90°), Level 6 (rotated 180°). Not used in levels 1-3.
- Role: playfield wall reused across multiple later levels via rotation.
- Visual-vs-functional read: same as other `bvzgd-*`.
  - At-rendered-scale shape: jagged outline.
  - Palette signature: 2.
  - Nearest-other-sprite check: other `bvzgd-Level*`.
- Visual contrast notes: red on grey.

### `kzeze-anqcf` — hollow X target (level 4+)
- Pixel pattern: 7×7 with palette-15 (white) cells along both diagonals, otherwise transparent.
- Where it appears: Level 4 only (with `color_remap(None, 7)` → orange-yellow tint).
- Role: special "anqcf" target. In `tpjhojnaoa` the win loop explicitly skips heads whose key contains "anqcf" — meaning this target is exempt from the win predicate. Decorative/distractor for levels 4+.
- Visual-vs-functional read: looks like a target marker (X-spot), but is mechanically inert for win checking.
  - At-rendered-scale shape: skeletal X.
  - Palette signature: 15 (or 7 after remap).
  - Nearest-other-sprite check: `mpjrv-kzeze` (also a 7x7 X-like ring) — but mpjrv-kzeze is a black warning pulse rather than a target.
- Visual contrast notes: white-on-grey reads, but lacks the filled body of a normal target.

### `kzeze-kpaac` — white filled target ring
- Pixel pattern: 7×7 rounded-square (diamond-like silhouette) filled with palette -2 (transparent-2 / "interior" sentinel) and a white (15) palette border on the outer edge of each diagonal corner.
- Where it appears: Level 1 (1 copy at (36,18)); Level 2 (1 copy at (54,15)); Level 3 (1 copy at (31,54)).
- Role: **target ring** (`xwdrv` in `brdck`) for the white team. Win predicate per team: the head must collide with this sprite.
- Visual-vs-functional read: a filled rounded square with hollow border reads as a "goal slot" / "docking ring" — that intuition is correct.
  - At-rendered-scale shape: filled rounded square with a thin white outer rim.
  - Palette signature: 15, -2 (where -2 acts as "see-through interior" and renders as background under the renderer).
  - Nearest-other-sprite check: vs `bdkaz-kpaac` (head, 5x5 hollow ring with pink eye) — differentiated by size (7x7 vs 5x5) and by filled vs hollow body. Vs `mpjrv-kzeze` (black pulse halo, same 7x7 shape) — color (white vs black) and persistence (target persists, halo blinks).
- Visual contrast notes: white border + see-through interior reads as a "ring" against the grey background.

### `kzeze-kpaaczjgrppgkne` — tri-color target (level 6)
- Pixel pattern: 7×7 diamond border using palette 9 (blue), 14 (orange), 15 (white) on different sides.
- Where it appears: Level 6 only.
- Role: target ring for tri-color team in level 6.
- Visual-vs-functional read: tri-color border target.
  - At-rendered-scale shape: ring with three color zones.
  - Palette signature: 9, 14, 15.
  - Nearest-other-sprite check: other `kzeze-*` rings.
- Visual contrast notes: multi-color makes it easy to identify as the tri-color team's goal.

### `kzeze-pgknepyzud` — azure/blue target (level 4+)
- Pixel pattern: 7x7 ring with palette 9 (blue) on left, 8 (azure) on right.
- Where it appears: Level 4 only.
- Role: target for azure/blue team.
- Visual-vs-functional read: bicolor ring target.
  - At-rendered-scale shape: filled ring with two color halves.
  - Palette signature: 8, 9.
  - Nearest-other-sprite check: matches `bdkaz-pgknepyzud` head.
- Visual contrast notes: bicolor distinguishes from neighbors.

### `kzeze-qniqj` — purple target ring
- Pixel pattern: 7×7 diamond border in palette 12 (purple), -2 interior.
- Where it appears: Level 2 (1 copy at (37,48)).
- Role: target ring for the purple team.
- Visual-vs-functional read: filled purple ring = target slot for the purple head.
  - At-rendered-scale shape: filled rounded ring.
  - Palette signature: 12, -2.
  - Nearest-other-sprite check: vs `bdkaz-qniqj` head — same color, but the head is hollow with an eye and 5x5; the target is filled and 7x7.
- Visual contrast notes: purple stands clearly on grey.

### `kzeze-qniqjgigctpgknekpaac` — tricolor target (level 4+)
- Pixel pattern: 7x7 ring with diagonal palette gradient (12, 14, 15).
- Where it appears: Level 4 only.
- Role: target for the tri-color team.
- Visual-vs-functional read: tri-color target.
  - At-rendered-scale shape: diagonal-gradient ring.
  - Palette signature: 12, 14, 15.
  - Nearest-other-sprite check: matches `bdkaz-qniqjgigctpgknekpaac` head.
- Visual contrast notes: gradient makes color-team identification easy.

### `kzeze-ttyiaPinkpgkne` — pink/green/cyan target (level 6)
- Pixel pattern: 7×7 ring using palette 6 (pink), 10 (cyan), 11 (green).
- Where it appears: Level 6 only.
- Role: target for that team in level 6.
- Visual-vs-functional read: tri-color target.
  - At-rendered-scale shape: tri-color ring.
  - Palette signature: 6, 10, 11.
  - Nearest-other-sprite check: other `kzeze-*` rings.
- Visual contrast notes: includes palette 10 (cyan) — same hue as the no-go region; risk of confusion.

### `kzeze-ttyiazjgrp` — green/orange target (level 4+)
- Pixel pattern: 7×7 ring with palette 11 (green) and 14 (orange).
- Where it appears: Level 4 only.
- Role: target for the green/orange team.
- Visual-vs-functional read: bicolor target.
  - At-rendered-scale shape: bicolor ring.
  - Palette signature: 11, 14.
  - Nearest-other-sprite check: `bdkaz-ttyiazjgrp` head.
- Visual contrast notes: green/orange split visible.

### `kzeze-zjgrp` — orange target ring
- Pixel pattern: 7×7 diamond border in palette 14 (orange), -2 interior.
- Where it appears: Level 3 (1 copy at (52,50)).
- Role: target for the orange team in level 3.
- Visual-vs-functional read: filled orange ring = orange head's destination.
  - At-rendered-scale shape: filled ring.
  - Palette signature: 14, -2.
  - Nearest-other-sprite check: vs `bdkaz-zjgrp` head — color identical, distinguishable by size (7x7 vs 5x5) and fullness.
- Visual contrast notes: orange near the red corridor outline could be momentarily mis-read.

### `mpjrv-bdkaz` — black "head pulse" halo
- Pixel pattern: 5×5 ring of palette-0 (black), with a clear interior; rendered at layer=100 so it always draws on top of the head.
- Where it appears: spawned dynamically in `zznsngfkwo` whenever the head currently overlaps a cyan no-go region (`qtwnv-*`). Used only when collision count > 0.
- Role: **collision warning halo** flashing around a head that is intersecting the no-go zone.
- Visual-vs-functional read: a sudden black ring around the head signals "you're intersecting hazard"; the visual flashing appearance correctly conveys "warning". The icon's *shape* mirrors the head's silhouette so it overlays cleanly.
  - At-rendered-scale shape: hollow ring.
  - Palette signature: 0.
  - Nearest-other-sprite check: vs `bdkaz-yukft` (the level-5+ black head) — **both are black 5x5 rings**; the difference is that `mpjrv-bdkaz` toggles on/off frame-by-frame in `zznsngfkwo`, whereas `bdkaz-yukft` is persistent. In levels 1-3 there is no `bdkaz-yukft`, so no confusion arises.
- Visual contrast notes: black against grey is high-contrast; layer=100 ensures it overlays anything it pulses on.

### `mpjrv-kzeze` — black "target settle" halo
- Pixel pattern: 7×7 black ring matching the silhouette of `kzeze-*` targets.
- Where it appears: spawned dynamically in `dkhjddmkke` when a head first collides with its target (a "you've reached the goal" pulse).
- Role: **target-arrival pulse**, flashing around a target ring while a head is sitting on it. Toggles on/off until 5 cycles complete, then disappears (the "win-armed" flag flips).
- Visual-vs-functional read: a black halo around the goal slot reads as "lock-in animation"; matches function.
  - At-rendered-scale shape: hollow 7x7 ring.
  - Palette signature: 0.
  - Nearest-other-sprite check: visually similar in shape to `kzeze-anqcf` (white 7x7 X), but distinguishable by color (black vs white) and the X vs ring pattern.
- Visual contrast notes: black on grey reads sharply.

### `qtwnv-Level2` — cyan no-go region for L2-bound levels
- Pixel pattern: 35×40 mosaic of palette-10 (cyan) cells forming an irregular blob, with transparent (-1) elsewhere.
- Where it appears: Not used in levels 1-3 directly (it's defined but only `qtwnv-Level3`/`-Level5` are placed in levels 2 and 3 respectively).
- Role: would be cyan no-go (hazard) region.
- Visual-vs-functional read: a wide cyan smear reads as "water" or "hazard zone"; if the head hovers over it for 5 step-cycles the player loses one of 5 lives.
  - At-rendered-scale shape: irregular cyan blob.
  - Palette signature: 10.
  - Nearest-other-sprite check: other `qtwnv-Level*`.
- Visual contrast notes: cyan against grey is distinct from the red walls and the colored heads.

### `qtwnv-Level3` — cyan no-go region used in level 2
- Pixel pattern: 73×44 cyan mosaic.
- Where it appears: Level 2 (clone at (-3,22)).
- Role: cyan **no-go region**. If any head collides with this sprite, `cyaxdmynov` becomes True; the head pulses with `mpjrv-bdkaz` for 5 toggles (`wvopxkipus >= 5`), then `cjcex` flips True. After 5 such collision-events (`anzbz >= 5`), `self.lose()` is called. Until that, each collision wastes one of the player's 5 chances.
- Visual-vs-functional read: cyan blob = hazard. Matches function.
  - At-rendered-scale shape: irregular cyan blob.
  - Palette signature: 10.
  - Nearest-other-sprite check: vs other `qtwnv-Level*`.
- Visual contrast notes: cyan distinct from grey; could blend slightly with the cyan accents of `kzeze-ttyiaPinkpgkne` in later levels (not in levels 1-3).

### `qtwnv-Level4` — cyan no-go region (level 4+)
- Pixel pattern: 73×N cyan mosaic.
- Where it appears: not used in levels 1-3.
- Role: hazard region for some level.
- Visual-vs-functional read: same as `qtwnv-Level3`.
  - At-rendered-scale shape: cyan blob.
  - Palette signature: 10.
  - Nearest-other-sprite check: other `qtwnv-Level*`.
- Visual contrast notes: cyan on grey.

### `qtwnv-Level5` — cyan no-go region used in level 3
- Pixel pattern: cyan mosaic.
- Where it appears: Level 3 (clone at (-2,-2)).
- Role: same as `qtwnv-Level3` — cyan hazard sprite for level 3.
- Visual-vs-functional read: cyan no-go.
  - At-rendered-scale shape: cyan blob.
  - Palette signature: 10.
  - Nearest-other-sprite check: other `qtwnv-*`.
- Visual contrast notes: cyan on grey.

### `qtwnv-Level7` — cyan no-go region (level 4+)
- Pixel pattern: cyan mosaic.
- Where it appears: not used in levels 1-3 (placed in level 4, level 5).
- Role: hazard region for later levels.
- Visual-vs-functional read: cyan no-go.
  - At-rendered-scale shape: cyan blob.
  - Palette signature: 10.
  - Nearest-other-sprite check: other `qtwnv-*`.
- Visual contrast notes: cyan on grey.

### `txxvz-anqcf` — small cyan X marker (level 4+)
- Pixel pattern: 3 wide × 7 tall hourglass/X of palette-10 (cyan).
- Where it appears: Level 4 only.
- Role: small static cyan glyph; in level 4 it is associated with the special `anqcf` head/target pair, which is exempt from the win check.
- Visual-vs-functional read: looks like a marker/decoration.
  - At-rendered-scale shape: small cyan X.
  - Palette signature: 10.
  - Nearest-other-sprite check: shares cyan with the `qtwnv-*` hazard regions, which could mislead.
- Visual contrast notes: cyan-on-grey, but tiny.

### `xigcb-gigctpgknezzepw` — half-cyan paint stamp (level 5+)
- Pixel pattern: 5×5 corner-divided sprite — diagonal palette-10 (cyan) on one half, palette-0 (black) on the other.
- Where it appears: Level 6 only.
- Role: paintbrush stamp (level 5+ mechanic). When a head sits in `fwqwj` mode (no-target/free black-head levels), it collides with these sprites; the head's pixels are then painted with the stamp's pattern via `iciufrewti`. The stamp is then consumed/removed.
- Visual-vs-functional read: a small two-tone tile reads as "icon" or "paint chip"; mechanically it dyes the head and is collected.
  - At-rendered-scale shape: 5x5 with diagonal split.
  - Palette signature: 0, 10.
  - Nearest-other-sprite check: any other `xigcb-*` stamp.
- Visual contrast notes: cyan paint stamps may visually blur with the cyan no-go region.

### `xigcb-kpaaczzepw` — half-white paint stamp (level 6)
- Pixel pattern: 5×5 with diagonal palette-15 (white) and palette-0 (black) split.
- Where it appears: Level 6 only.
- Role: paint stamp.
- Visual-vs-functional read: paint chip; collide-to-collect.
  - At-rendered-scale shape: 5x5 split tile.
  - Palette signature: 0, 15.
  - Nearest-other-sprite check: other `xigcb-*` stamps.
- Visual contrast notes: white-on-black diagonal.

### `xigcb-Maroon` — half-maroon paint stamp (level 6)
- Pixel pattern: 5×5 split with palette-13 (maroon) and palette-0 (black).
- Where it appears: Level 6 only.
- Role: paint stamp.
- Visual-vs-functional read: paint chip.
  - At-rendered-scale shape: 5x5 split tile.
  - Palette signature: 0, 13.
  - Nearest-other-sprite check: other `xigcb-*`.
- Visual contrast notes: maroon distinct hue.

### `xigcb-pgknezzepw` — half-azure paint stamp (level 6)
- Pixel pattern: 5×5 with palette-8 (azure) and palette-0.
- Where it appears: Level 6 only.
- Role: paint stamp.
- Visual-vs-functional read: paint chip.
  - At-rendered-scale shape: 5x5 split tile.
  - Palette signature: 0, 8.
  - Nearest-other-sprite check: other `xigcb-*`.
- Visual contrast notes: azure on black.

### `xigcb-qniqj` — half-purple paint stamp (level 6)
- Pixel pattern: 5×5 with palette-12 (purple) and palette-0.
- Where it appears: Level 6 only.
- Role: paint stamp.
- Visual-vs-functional read: paint chip.
  - At-rendered-scale shape: 5x5 split tile.
  - Palette signature: 0, 12.
  - Nearest-other-sprite check: other `xigcb-*`.
- Visual contrast notes: purple/black.

### `xigcb-ttyiazzepw` — half-green paint stamp (level 6)
- Pixel pattern: 5×5 with palette-11 (green) and palette-0.
- Where it appears: Level 6 only.
- Role: paint stamp.
- Visual-vs-functional read: paint chip.
  - At-rendered-scale shape: 5x5 split tile.
  - Palette signature: 0, 11.
  - Nearest-other-sprite check: other `xigcb-*`.
- Visual contrast notes: green/black.

### `xigcb-txxvzpgkne` — half-blue paint stamp (level 5+)
- Pixel pattern: 5×5 split with palette-9 (blue) and palette-0.
- Where it appears: Level 5.
- Role: paint stamp.
- Visual-vs-functional read: paint chip.
  - At-rendered-scale shape: 5x5 split tile.
  - Palette signature: 0, 9.
  - Nearest-other-sprite check: other `xigcb-*`.
- Visual contrast notes: blue/black.

### `xigcb-txxvzpgkneBottom` — half-blue paint stamp (level 6)
- Pixel pattern: 5×5 split, blue on bottom rather than corner.
- Where it appears: Level 6 only.
- Role: paint stamp variant.
- Visual-vs-functional read: paint chip.
  - At-rendered-scale shape: 5x5 split tile.
  - Palette signature: 0, 9.
  - Nearest-other-sprite check: `xigcb-txxvzpgkne` (also blue, different split orientation).
- Visual contrast notes: blue/black with bottom-half emphasis.

### `xigcb-txxvzPink` — half-pink paint stamp (level 6)
- Pixel pattern: 5×5 split with palette-6 (pink) and palette-0.
- Where it appears: Level 6 only.
- Role: paint stamp.
- Visual-vs-functional read: paint chip.
  - At-rendered-scale shape: 5x5 split tile.
  - Palette signature: 0, 6.
  - Nearest-other-sprite check: other `xigcb-*`.
- Visual contrast notes: pink/black.

### `xigcb-txxvzpyzud` — half-azure paint stamp (level 5+)
- Pixel pattern: 5×5 split with palette-8 (azure) and palette-0.
- Where it appears: Level 5.
- Role: paint stamp.
- Visual-vs-functional read: paint chip.
  - At-rendered-scale shape: 5x5 split tile.
  - Palette signature: 0, 8.
  - Nearest-other-sprite check: `xigcb-pgknezzepw` (similar palette).
- Visual contrast notes: azure/black.

### `xigcb-txxvzttyia` — half-green paint stamp (level 5+)
- Pixel pattern: 5×5 split with palette-11 (green) and palette-0.
- Where it appears: Level 5.
- Role: paint stamp.
- Visual-vs-functional read: paint chip.
  - At-rendered-scale shape: 5x5 split tile.
  - Palette signature: 0, 11.
  - Nearest-other-sprite check: `xigcb-ttyiazzepw`.
- Visual contrast notes: green/black.

### `xigcb-txxvzzjgrp` — half-orange paint stamp (level 5+)
- Pixel pattern: 5×5 split with palette-14 (orange) and palette-0.
- Where it appears: Level 5.
- Role: paint stamp.
- Visual-vs-functional read: paint chip.
  - At-rendered-scale shape: 5x5 split tile.
  - Palette signature: 0, 14.
  - Nearest-other-sprite check: `xigcb-zjgrp`.
- Visual contrast notes: orange/black.

### `xigcb-zjgrp` — half-orange paint stamp (level 6)
- Pixel pattern: 5×5 split, palette-14 and palette-0, different orientation.
- Where it appears: Level 6 only.
- Role: paint stamp variant.
- Visual-vs-functional read: paint chip.
  - At-rendered-scale shape: 5x5 split tile.
  - Palette signature: 0, 14.
  - Nearest-other-sprite check: `xigcb-txxvzzjgrp`.
- Visual contrast notes: orange/black.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (64, 64)
- Number of sprites placed: 5
- Composition by role: 1 white head ring (`bdkaz-kpaac`) + 2 white footprints (`bdkazLeg-kpaac`) + 1 white target ring (`kzeze-kpaac`) + 1 corridor wall (`bvzgd-Level1`). No no-go region; no obstacles.
- Level data: no `Level(..., data={...})` argument is used; no `level.set_data(...)` or `level.get_data(...)` calls anywhere in the source. State is managed solely on `self`.
- Spawn position(s): there is no "player avatar" position per se. The two clickable footprints start at (5,34) and (25,57); the head puppet auto-centers at their centroid (≈(15,45)) on `on_set_level` via `bdahxidrjf`. The target ring sits at (36,18). Initial selected piece (`mjdkn`): the leg with smallest Euclidean distance to origin (sorted in `on_set_level`), highlighted by `color_remap(0,3)`.
- Per-cell layout (coordinate listing):
  - Corridor wall `bvzgd-Level1`: (-5,-6), 73×73 sparse mosaic of palette-2.
  - White head `bdkaz-kpaac`: (15,45), 5×5.
  - White footprint #1 `bdkazLeg-kpaac`: (5,34), 5×5.
  - White footprint #2 `bdkazLeg-kpaac`: (25,57), 5×5.
  - White target `kzeze-kpaac`: (36,18), 7×7.
- Mechanic introduced relative to the previous level: this is the first level — introduces the **centroid-puppet-leg** mechanic: clicking a footprint selects it; clicking again moves it; the head (`bdkaz-kpaac`) auto-recenters at the legs' centroid every move; when the head overlaps the target ring (`kzeze-kpaac`) for one settle pulse the level wins. Also introduces the corridor wall (`bvzgd-Level1`) which forbids the leg from moving outside.
- Specific challenge: figure out that the head is *not* the agent — the two plus-glyph footprints are. The player must drag both legs to positions whose midpoint lands inside the white target ring on the upper-right, while keeping each leg inside the red corridor outline.
- Estimated optimal action count: ~6 (each click is one action: 1 to select leg A, 1 to drop it near target, 1 to select leg B, 1 to drop it, plus 1-2 corrective clicks to land the centroid exactly on the target).

### Level 2
- `grid_size`: (64, 64)
- Number of sprites placed: 11
- Composition by role: 2 head rings (1 white `bdkaz-kpaac`, 1 purple `bdkaz-qniqj`) + 5 footprints (2 white, 3 purple) + 2 target rings (1 white, 1 purple) + 1 corridor wall (`bvzgd-Level1` mirrored) + 1 cyan no-go region (`qtwnv-Level3`).
- Level data: none (no `level.set_data`).
- Spawn position(s): no avatar; legs start at (43,33), (52,46), (15,4), (6,19), (47,7); heads auto-centroid in `on_set_level`. Target rings at (54,15) and (37,48). Initial selection: leg with smallest distance to origin.
- Per-cell layout (coordinate listing):
  - Wall `bvzgd-Level1` mirrored at (-6,-10).
  - White head `bdkaz-kpaac`: (48,39).
  - Purple head `bdkaz-qniqj`: (23,11).
  - White legs `bdkazLeg-kpaac`: (43,33), (52,46).
  - Purple legs `bdkazLeg-qniqj`: (15,4), (6,19), (47,7).
  - White target `kzeze-kpaac`: (54,15).
  - Purple target `kzeze-qniqj`: (37,48).
  - Cyan no-go `qtwnv-Level3`: (-3,22).
- Mechanic introduced relative to L1:
  - **Multiple color teams** — two heads, each with its own legs and target. The win predicate now requires *both* heads to settle on their respective same-color targets simultaneously.
  - **Three-leg centroid** — the purple team has three legs; the centroid is the average of three points (more leverage per leg, more degrees of freedom).
  - **Cyan no-go region** (`qtwnv-Level3`) — first appearance of the hazard region. Each head-collision with the cyan region triggers the warning pulse `mpjrv-bdkaz`; after 5 such events `self.lose()` fires.
- Specific challenge: route both heads to swap sides (the white team's target is on the upper-right corner where the purple legs sit, and vice versa) while threading the centroid past the cyan blob. Whichever team is moved first must avoid yanking the head into cyan as the other team's legs are still in the way.
- Estimated optimal action count: ~12-16 (5 legs to drag, with intermediate hops to avoid the cyan no-go).

### Level 3
- `grid_size`: (64, 64)
- Number of sprites placed: 12
- Composition by role: 2 head rings (1 white `bdkaz-kpaac`, 1 orange `bdkaz-zjgrp`) + 6 footprints (2 white, 4 orange) + 2 target rings (1 white, 1 orange) + 1 corridor wall (`bvzgd-Level5` mirrored) + 1 cyan no-go region (`qtwnv-Level5`).
- Level data: none.
- Spawn position(s): no avatar; legs at (35,32), (50,38), (12,14), (21,19), (32,7), (37,14); heads auto-centroid; targets at (31,54) (white) and (52,50) (orange). Initial selection: leg closest to origin.
- Per-cell layout (coordinate listing):
  - Wall `bvzgd-Level5` mirrored at (-5,-6).
  - White head `bdkaz-kpaac`: (42,35).
  - Orange head `bdkaz-zjgrp`: (26,13).
  - White legs `bdkazLeg-kpaac`: (35,32), (50,38).
  - Orange legs `bdkazLeg-zjgrp`: (12,14), (21,19), (32,7), (37,14).
  - White target `kzeze-kpaac`: (31,54).
  - Orange target `kzeze-zjgrp`: (52,50).
  - Cyan no-go `qtwnv-Level5`: (-2,-2).
- Mechanic introduced relative to L2:
  - **Four-leg centroid** for the orange team — averaging over four points means each individual leg has only ¼ of the leverage on the head's position; player needs more clicks per pixel of head movement.
  - **Different corridor topology** (`bvzgd-Level5` instead of `bvzgd-Level1`), with the cyan no-go positioned on the upper-left rather than across the middle.
- Specific challenge: with one team having four legs and only two targets to place precisely, the player must orchestrate finer increments of head motion. Both heads need to travel diagonally to the lower-right target zone while keeping each individual leg inside the corridor and the centroid out of the cyan region.
- Estimated optimal action count: ~16-20 (6 legs to drag, finer corrections needed to land 4-point centroid on a 7×7 target).

Levels 4-6 exist but are excluded per skill scope.

## Action handlers

### ACTION6 (the only registered action — click)
- Trigger: `self.action.id == GameAction.ACTION6` inside `step()`.
- Branches inside `step()`:
  1. If `self._action_count >= self._max_actions` → `self.lose()`, `self.complete_action()`, return.
  2. If `self.bmtib` (an animation/movement is in progress) → call `self.tpjhojnaoa()` to advance the animation; if the animation finishes (`bmtib` flips False) call `complete_action()`.
  3. Otherwise, take the click `(x, y)` from `action.data`, convert via `self.camera.display_to_grid(x, y)` to grid coords `(xyizm, rgica)`.
  4. Iterate `self.ftmaz` (the list of all `bdkazLeg-*` sprites): if the click lands inside any leg's bounding box, that leg becomes the new selected leg. Call `pprcmbqpwi(leg)` to swap palette: previous leg's `0→3` reverts via `color_remap(3,0)` becoming `0`, new leg's `0→3`. `complete_action()`.
  5. If no leg was hit but `self.mjdkn` is set, treat the click as a **drop point** for the selected leg: target position is `(xyizm - leg.width//2, rgica - leg.height//2)`. Check `tkdffrbsnv(hgenyvlspj, ftzzwdcsne)` to see if dropping there would put the leg in collision with any `bvzgd-*` (corridor wall). If it would, `complete_action()` (rejected). Otherwise call `eijzqlwbri(...)` which sets `bmtib=True`, `mkugn=current_pos`, `whfmv=target_pos`, `tjffy=0` — kicking off the slide animation. The function returns *without* calling `complete_action()`, so subsequent engine-tick `step()` calls will drive `tpjhojnaoa()` to interpolate the leg and the head.
  6. If `display_to_grid` returns falsy → `complete_action()`.
  7. If `self.mjdkn is None` and click was outside any leg → `complete_action()`.
- State mutations:
  - Read: `self._action_count`, `self._max_actions`, `self.bmtib`, `self.mjdkn`, `self.ftmaz`, `self.camera`, `self.action`.
  - Written: `self.tfhng` (selected leg index), `self.mjdkn` (currently selected leg ref), the leg sprites' `color_remap` (palette overlay 0↔3), `self.bmtib`, `self.tjffy`, `self.cjcex`, `self.xjryq`, `self.mkugn`, `self.whfmv`. During animation `tpjhojnaoa` further mutates `self.dfugm` per-team (`miwyy`, `qnpnk`, `rftjv`, `wugiv`, `meydp`), `self.cyaxdmynov`, `self.zxankdpxcx`, `self.wvopxkipus`, `self.itbwd`, `self.xymku`, `self.anzbz`, `self.winning`, `self.fwqwj`, and `self.nxahg`.
- Side effects on sprites: leg's `set_position(...)` (interpolated each tick); head's `set_position(...)` re-centroided via `bdahxidrjf` after each leg sub-step; spawn/remove of `mpjrv-bdkaz` and `mpjrv-kzeze` halos via `current_level.add_sprite` / `remove_sprite`; in the level-5+ paint mode, `iciufrewti` removes paint stamps and rewrites pixels of the head sprite.
- Engine effects:
  - `self.lose()` at line 1723 — when `self.anzbz >= 5` (5 head/no-go collisions accumulated), and at line 1783 — when `self._action_count >= self._max_actions`.
  - `self.next_level()` at line 1679 — when `self.winning` is True and no team is mid-pulse.
  - `self.complete_action()` at lines 1688, 1776, 1784, 1790, 1806, 1816, 1818, 1820, 1822 — at the end of every non-animating branch.
- Pre-conditions / gating:
  - Drop click rejected if `tkdffrbsnv` reports collision with any `bvzgd-*` wall sprite.
  - Drop click ignored entirely if `self.mjdkn is None` (no leg currently selected).
  - The animation branch (`self.bmtib` True) consumes the click event regardless of `(x, y)` content; clicks during animation are effectively no-ops aside from advancing one animation frame.

The source defines no actions beyond ACTION6.

## HUD widgets

Two `RenderableUserDisplay` subclasses are defined and both are registered.

### `bdxsqgndfy` — step counter (left-edge depleting bar)
- Class name (obfuscated): `bdxsqgndfy`.
- Render-pixel range: column 0 of the frame; rows 0..frame.shape[0]-1 (i.e. the leftmost vertical column of every row in the rendered frame). Effectively a 1-pixel-wide vertical strip.
- What value it displays: `self.current_steps / self.wudgymjmzk` — the proportion of step budget remaining. Reads from the game class via `self._step_counter_ui.fungqqyodc(self._max_actions - self._action_count)` called in `on_set_level` and at the top of every `step()`.
- Visual style: depleting solid bar — palette-0 (black) cells fill from the bottom up to height `xynkwnbamu = round(height * remaining_fraction)`; remaining cells (top of column) become palette-5 (background grey, blending in).
- Update points: `bdxsqgndfy.fungqqyodc(remaining)` is called in (a) `R11l.on_set_level` (line 1494) and (b) the very first lines of `R11l.step` (line 1781).
- Where it is registered: instantiated in `R11l.__init__` and passed into `Camera(interfaces=[self._step_counter_ui])`. Then in `on_set_level`, `self.camera.replace_interface([self._step_counter_ui, self.feqwz])` re-installs both interfaces each level.

### `lbnpnbcxsr` — connector lines between head and its legs
- Class name (obfuscated): `lbnpnbcxsr`.
- Render-pixel range: anywhere on the frame that the Bresenham line `grygtayltb` traverses between each head's center pixel and each of its leg centers — only frame cells where the existing pixel is palette-5 (background) or palette-10 (cyan no-go) get overwritten with `hadaeosria` (default palette-1). Walls (palette-2) and head/leg pixels themselves are not overwritten.
- What value it displays: visual lines connecting each head sprite to each of its leg sprites — i.e. the centroid relationship rendered as visible spokes.
- Visual style: thin (1-pixel) Bresenham lines, color palette-1.
- Update points: rendered every frame via `render_interface`; positions are pulled live from `self.imhgqwengg = self.brdck`. So whenever a head moves (centroided by `bdahxidrjf`) or a leg moves, the lines re-draw automatically.
- Where it is registered: instantiated in `on_set_level` as `self.feqwz = lbnpnbcxsr(self.brdck, self.camera)` and re-installed via `self.camera.replace_interface([self._step_counter_ui, self.feqwz])`.

## Internal state — exhaustive

| attr (obfuscated) | semantic name | type | initial value | written by | read by | role |
|---|---|---|---|---|---|---|
| `_step_counter_ui` | step-counter HUD | `bdxsqgndfy` | `bdxsqgndfy(60)` | `__init__`, `on_set_level`, `step` | `step`, `on_set_level`, `Camera` | renders depleting bar |
| `_max_actions` | step budget per level | int | 60 | `__init__` | `step`, `on_set_level` | trigger for `lose()` when exceeded |
| `mjdkn` | selected_leg | `Sprite \| None` | None | `__init__`, `pprcmbqpwi`, `step` | `pprcmbqpwi`, `tkdffrbsnv`, `eijzqlwbri`, `tpjhojnaoa`, `step` | currently highlighted leg awaiting drop click |
| `tfhng` | selected_leg_index | int | 0 | `__init__`, `on_set_level`, `step` | `step` | which entry of `ftmaz` is selected |
| `kdabh` | valid_actions_grid | `list[ActionInput]` | 256 ACTION6 inputs on a 4-pixel grid | `__init__` | `_get_valid_actions` | discretized click grid |
| `brdck` | team_groups | `dict[str, lsthwzbhjk]` | {} | `__init__`, `on_set_level` | `on_set_level`, `tpjhojnaoa`, `dkhjddmkke`, `mfrvmbaujm`, `lbnpnbcxsr.render_interface` | per-color group of head/legs/target |
| `ftmaz` | all_legs | `list[Sprite]` | [] | `__init__`, `on_set_level` | `step`, `on_set_level` | flat list of every clickable leg |
| `yhfnp` | walls | `list[Sprite]` | [] | `__init__`, `on_set_level` | `tkdffrbsnv` | the corridor `bvzgd-*` sprites used for wall collision |
| `bmtib` | is_animating | bool | False | `eijzqlwbri`, `tpjhojnaoa`, `step` | `step`, `tpjhojnaoa` | true while a leg-drag interpolation is in progress |
| `tjffy` | animation_step | int | 0 | `eijzqlwbri`, `tpjhojnaoa` | `tpjhojnaoa` | counter into the slide animation |
| `gfwuu` | animation_duration | int | 1 | `__init__` | `tpjhojnaoa` | total ticks per leg drag (set to 1 = instantaneous) |
| `mkugn` | animation_start_pos | tuple[int,int] | (0,0) | `eijzqlwbri` | `tpjhojnaoa` | leg's start position |
| `whfmv` | animation_end_pos | tuple[int,int] | (0,0) | `eijzqlwbri` | `tpjhojnaoa` | leg's drop target |
| `xjryq` | retract_after_fail | bool | False | `__init__`, `eijzqlwbri`, `tpjhojnaoa` | `tpjhojnaoa` | flag indicating animation should rewind (used when win check fails) |
| `anzbz` | hazard_collision_count | int | 0 | `on_set_level`, `tpjhojnaoa` | `tpjhojnaoa` | number of times any head hit a `qtwnv-*` no-go; lose at 5 |
| `cjcex` | post_pulse_settled | bool | False | `__init__`, `on_set_level`, `eijzqlwbri`, `zznsngfkwo`, `tpjhojnaoa` | `tpjhojnaoa` | flips True after a hazard pulse completes; gates retract animation |
| `cyaxdmynov` | hazard_pulse_active | bool | False | `__init__`, `on_set_level`, `zznsngfkwo`, `tpjhojnaoa` | `step`, `tpjhojnaoa`, `zznsngfkwo` | true while the head-on-cyan blink loop is running |
| `wvopxkipus` | hazard_pulse_phase | int | 0 | `__init__`, `on_set_level`, `zznsngfkwo` | `zznsngfkwo` | hazard-pulse counter (0..5) |
| `zxankdpxcx` | hazard_pulse_tick | int | 0 | `__init__`, `on_set_level`, `zznsngfkwo` | `zznsngfkwo` | per-tick driver of `mpjrv-bdkaz` add/remove |
| `itbwd` | hazard_focused_head | `Sprite \| None` | None | `__init__`, `on_set_level`, `tpjhojnaoa` | `zznsngfkwo` | which head is currently being pulsed by hazard halo |
| `xymku` | hazard_halo_sprite | `Sprite \| None` | None | `__init__`, `on_set_level`, `zznsngfkwo` | `zznsngfkwo` | live `mpjrv-bdkaz` clone in the level |
| `dfugm` | settle_state_per_team | `dict[str, yxyifafxdx]` | {} | `__init__`, `on_set_level`, `dkhjddmkke` | `tpjhojnaoa`, `dkhjddmkke` | per-team target-arrival-pulse state |
| `zmxct` | per_team_arrived_flag | `dict[str, bool]` | {} | `__init__`, `on_set_level` | (read implicitly via `dfugm.miwyy`) | tracks per-team arrival (initialized; not heavily mutated in observed paths) |
| `fwqwj` | per_yukft_collected_paints | `dict[str, list[str]]` | {} | `__init__`, `on_set_level`, `iciufrewti` | `iciufrewti`, `dkhjddmkke`, `tpjhojnaoa` | for `bdkaz-yukft*` heads (level 5+), records collected `xigcb-*` stamp names |
| `nxahg` | paint_stamps | `list[Sprite]` | [] | `__init__`, `on_set_level`, `iciufrewti` | `iciufrewti`, `tpjhojnaoa` | live `xigcb-*` stamps that haven't been collected yet (level 5+) |
| `winning` | win_armed | bool | False (set in `on_set_level`) | `on_set_level`, `tpjhojnaoa` | `tpjhojnaoa` | flips True when all teams meet win predicate; `next_level()` fires once mid-pulses end |
| `feqwz` | connector_renderer | `lbnpnbcxsr` | (set in `on_set_level`) | `on_set_level` | `Camera.render_interface` | HUD widget that draws lines from each head to each of its legs |

## Win condition

Plain-English: every team's head must overlap its same-color target ring (or in the level-5+ painting variant, a leg already sitting in `fwqwj` whose collected stamps' colors equal those of the target). When that holds across all teams except the special `anqcf` team (level 4+ exemption), `self.winning` flips True. After the head-arrival pulses (`mpjrv-kzeze`) finish on every team (`mtpamjnlig["miwyy"]` all False), `self.next_level()` is called.

Literal condition (in `tpjhojnaoa`, lines 1731-1756):

```
ilynklqzjc = True
for hzottalifh, data in self.brdck.items():
    vetdveuitd = data["kignw"]; jgbjlkvvvd = data["xwdrv"]
    if not jgbjlkvvvd or "anqcf" in hzottalifh: continue   # skip teams without target
    if vetdveuitd and jgbjlkvvvd:
        if not vetdveuitd.collides_with(jgbjlkvvvd): ilynklqzjc = False; break
    else:
        # level 5+ paint mode: any leg whose collected stamps match target's palette
        ...
        if not nueqxvuioh: ilynklqzjc = False; break
if ilynklqzjc: self.winning = True
```

`next_level()` at line 1679 fires only after `winning` is True AND all per-team `miwyy` are False. The win condition is identical across levels 1, 2, 3 (each level just has different head/target pairings).

## Lose condition

Two distinct triggers, both call `self.lose()`:

1. **Step-budget exhaustion** (line 1783): at the top of every `step()`, if `self._action_count >= self._max_actions` (60), `self.lose()` is called immediately.
2. **Hazard-collision overflow** (line 1723): inside `tpjhojnaoa`, after a leg-drag completes, if a head ends overlapping a `qtwnv-*` no-go region, `self.anzbz` increments. When `self.anzbz >= 5` (5 cumulative hazard collisions across the level), `self.lose()` fires.

For level 1 there is no `qtwnv-*` placed, so only the step-budget lose applies. For levels 2 and 3 both lose mechanisms are active.

## Resource economy

- Depleting resource: **YES** — step counter `self._max_actions = 60` per level, decremented implicitly as the engine increments `self._action_count` on each `complete_action()`. Visualised as the left-column depleting bar (`bdxsqgndfy`). Threshold for losing: `_action_count >= 60`.
- Accumulating resource: **YES** — hazard-collision counter `self.anzbz` (per-level, resets in `on_set_level`). Lose at `anzbz >= 5`. Also `fwqwj` collects paint stamps in level 5+ (out of scope here but exists). And `winning` itself is essentially a binary "progress reached" flag toggled when the win predicate holds.
- Lives mechanic: **NO** — there is no respawn cycle. The `anzbz` counter is bookended at 5 collisions per level but acts like a tolerance budget rather than discrete lives (no respawn between).
- Resource interaction with win/lose: action-budget depletion forces `lose()`; hazard collisions force `lose()` when their own threshold is hit; otherwise the win predicate runs each leg-drop and flips `winning=True` independently of resources. The connector renderer doesn't gate either — it's purely cosmetic.

## Action-budget signature

- Default budget per level: `_max_actions = 60` (constant set in `R11l.__init__`).
- Whether budget tightens or shifts across levels 1-3: **NO** — the field is set once at construction and never reassigned. Each level resets `_action_count` to 0 (in the engine's level-start logic) and re-syncs the HUD via `self._step_counter_ui.fungqqyodc(self._max_actions - self._action_count)` in `on_set_level`. So the budget is per-level and identical (60) across L1, L2, L3.
- Per-level vs. per-environment: per-level (counter resets each level start).
- Decrement rate per action: −1 per `complete_action()` call. Note that during a leg-drag animation the `step()` function may run multiple times before `complete_action()` is called (because `bmtib=True` returns early), but only the final tick that finishes the animation calls `complete_action()`, so the user perceives one click ≈ one action.
- Refill mechanism: none.

## Notable code patterns / techniques

- Click-to-select / click-to-drop two-step interaction via `camera.display_to_grid` → iterate `self.ftmaz` to test bounding-box hit → call `pprcmbqpwi` for select or `eijzqlwbri` for drop. The selected piece is highlighted by `color_remap(0, 3)`.
- Tag-based grouping by name prefix (a homebrew variant of tag lookup): `vwznvtelzt` strips name prefixes `bdkaz-`, `bdkazLeg-`, `kzeze-` and constructs a per-color dictionary `brdck` mapping the suffix to head/legs/target sprites — a name-driven grouping in lieu of the standard `level.get_sprites_by_tag(...)` API.
- Centroid-puppet: `bdahxidrjf` repositions a "head" sprite to the centroid of a list of "leg" sprites. Used both at level setup and after every leg move to keep the puppet in sync.
- Discretized click-grid stored as a precomputed list of `ActionInput`s on a 4-pixel grid (`for y in range(0,64,4): for x in range(0,64,4)` = 256 candidate clicks). Returned wholesale by `_get_valid_actions`.
- Bresenham line rendering inside a `RenderableUserDisplay` (the `lbnpnbcxsr.grygtayltb` method) to draw connector lines between head and legs, with selective overwrite that respects walls (palette-2) and hazards by only painting cells already at palette-5 or palette-10.
- Custom HUD bar that does not use any sprite — a single column of palette-0 cells written directly into the frame buffer (`bdxsqgndfy.render_interface`), depleting from the bottom upward.
- Two-stage animation state machine — `bmtib` gates "is animating", `xjryq` flag triggers a rewind to the original position when a tentative drop fails the global win check, `cjcex` indicates "post-pulse settled and ready to retract", and `cyaxdmynov` separates the hazard-pulse mini-state-machine from the main move animation.
- Per-team settle-pulse using a `TypedDict` `yxyifafxdx` (`dfugm`) keeping `miwyy` (engaged), `qnpnk` (cycle count), `rftjv` (tick), `wugiv` (was-engaged latch), `meydp` (live halo sprite). `dkhjddmkke` toggles `mpjrv-kzeze` halos on/off in 4-tick cycles, ending after 5 cycles.
- Extending sprite tags at runtime: `ztqyeknilb._tags = []; ztqyeknilb._tags.append("sys_click")` — modifies the sprite instance's private tags list to mark legs as clickable in `on_set_level`.
- Hidden state encoded as a small numpy array: `_get_hidden_state` returns a 4×4 int16 array with `[0,0]` = `_action_count` — a compact hidden-state signature.
- Level-end win sequencing — `winning=True` waits for every per-team `miwyy` to clear before calling `next_level()`, so the celebratory pulse plays out on every target ring before transition.

## Anti-patterns / lessons

- Forty-eight sprites total but most are duplicates of the same shape (5×5 plus glyph or 7×7 ring) re-tinted by suffix — a generated game with stricter sprite-design rules should use a smaller, more semantically distinct palette of shapes per role.
- The visual identity between `bdkaz-yukft` (the level-5 black head) and `mpjrv-bdkaz` (the hazard pulse halo) is risky — they are both 5×5 black rings; only their behavior over time disambiguates. A generated game should ensure the warning halo looks different from any persistent sprite.
- The two `bdkazLeg-yukft` variants (and `bdkaz-yukft` / `bdkaz-yukft-2` heads) are pixel-identical but mechanically separate teams. Having visually identical, mechanically different sprites is a recipe for player confusion.
- The footprint plus-glyph carries its team-color in a single 1×1 center pixel — at the rendered 64×64 scale, that one pixel is barely readable. Generated games should use a more salient color signal on clickable pieces (e.g., a 2×2 core or a colored border).
- Cyan no-go regions overlap visually with cyan accents on `kzeze-ttyiaPinkpgkne` and the `txxvz-anqcf` glyph (level 4+) — re-using palette 10 across hazards and decoratives invites confusion. A generated game should reserve the hazard palette value exclusively.
- The four `bvzgd-Level*` corridor walls are 73×73 sparse mosaics of palette-2; they are huge multi-pixel sprites that consume substantial sprite-memory and clip awkwardly at level boundaries (note the negative offsets `(-5, -6)`). A 3-level generated game should use smaller wall sprites or generate corridor outlines from a procedural mask.
- The win-check loop scans every team every tick by name-prefix string operations (`"anqcf" in hzottalifh`), which is fragile against renaming and slow if many teams are added.
- The `_get_hidden_state` returns a 4×4 array but only the (0,0) cell is populated — wastes 15 cells. Generated games should size their hidden state tightly.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: **YES** — the `bdxsqgndfy` widget renders a 1-pixel-wide vertical bar at column 0 (left edge of the 64×64 frame), depleting from the bottom upward.
- Has lives mechanic: **NO** — there is no respawn cycle; the `anzbz` hazard counter is a tolerance budget (5 cumulative hits) but does not respawn the player.
- Has click-to-select (uses ACTION6): **YES**.
- Has tag-based grouping (uses `level.get_sprites_by_tag`): **NO** — it uses `level.get_sprites_by_name` with prefix stripping (`vwznvtelzt`) instead. Equivalent intent, different API.
- Uses ACTION5 (modal): **NO**.
- Uses ACTION6 (click): **YES**.
- Uses ACTION7: **NO**.
- Has level data dicts (uses `level.get_data` / `level.set_data`): **NO** — neither call appears in the source. State lives entirely on `self`.
- Multi-mechanic per level (vs. single mechanic per level): **NO** — each level introduces one new wrinkle on the centroid-puppet base mechanic; no level layers two unrelated mechanics simultaneously within levels 1-3 (e.g., level 2 adds the no-go region; level 3 adds the four-leg centroid).
- Tutorial level appears solvable by random play: **UNKNOWN** — the click grid has 256 cells; level 1 needs ~6 actions. Random clicking may select-and-drop the right leg occasionally, but reliably landing the centroid inside a 7×7 target with random clicks within 60 actions is unlikely. Best-case justification is "no" based on combinatorics.
- Has a depleting resource: **YES** — step counter (60 actions per level).
- Has an accumulating resource: **YES** — hazard-collision counter `self.anzbz` (lose at 5).
- Sprite shape convention used: **mixed** — heads are hollow rings with a center pixel, legs are filled plus glyphs, targets are filled rings, walls are sparse mosaics, hazards are filled blobs. No single shape convention dominates.
- HUD position: **multiple** — left-edge column for the step counter; everywhere on the frame for the connector lines (which thread between head and legs).
- Palette size used: **13** — distinct palette values appearing in any sprite are: -2, -1, 0, 2, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15. Counting positive integer palette values used (excluding sentinels -1 and -2): 0, 2, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15 → **12 distinct visible palette values**.
- Background colour value: **5**.
- Padding / letter-box colour value: **5**.
- Number of distinct mechanics introduced across levels 1-3: **3** — (1) centroid-puppet leg dragging with corridor wall (L1), (2) cyan hazard no-go region with 5-strike tolerance (L2), (3) higher-arity centroid (4-leg head) (L3). Multi-team play is technically a fourth wrinkle introduced in L2 alongside the hazard.
- Number of levels documented: **3** (out of 6 total in source; capped per skill scope).

(End of file.)
