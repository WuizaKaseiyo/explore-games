# tr87 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/tr87/cd924810/tr87.py`
- Lines: 1102
- Class name: `Tr87`
- available_actions: `[1, 2, 3, 4]` (UP/DOWN cycle the cursored glyph forward/backward, LEFT/RIGHT slide the cursor)
- Number of levels in source: 6
- Number of levels documented in this analysis: 3
- Imports: `NovaBaseGame`, `BlockingMode`, `Camera`, `GameAction`, `Level`, `RenderableUserDisplay`, `Sprite` from `novaengine`; `numpy as np`; `math`; `random`.

## Mechanic essence (one sentence)

A bookshelf of "input → output" rewrite rules — each rule a row of coloured glyph-cards split in the middle by a thin grey gap — sits above two horizontal tapes of cards, and the player slides a bracket-cursor along the lower tape with LEFT/RIGHT and cycles the bracketed card through its colour's seven-letter glyph alphabet with UP/DOWN until the lower tape's contents spell the exact rewrite of the upper tape under the rule set.

## Sprite roster

| sprite (obfuscated) | dims | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| `background` | 2x1 | 3 | (default) | -2 | YES | (default) | YES | horizontal letter-box separator scaled 32x to fill width — divides "rules" region from "tapes" region |
| `background2` | 1x2 | 3 | (default) | -2 | YES | (default) | YES | vertical separator (defined but never placed in any level) |
| `gyrdjxybtcmA` | 7x7 | 10 | gyrdjxybtcm | -1 | YES | (default) | YES | cyan colour-card (alphabet A backdrop) |
| `gyrdjxybtcmB` | 7x7 | 7 | gyrdjxybtcm | -1 | YES | (default) | YES | pink colour-card (alphabet B backdrop) |
| `gyrdjxybtcmC` | 7x7 | 11 | gyrdjxybtcm | -1 | YES | (default) | YES | yellow colour-card (alphabet C backdrop) |
| `iqrduxrukrk` | 11x1 | 3 | (default) | -2 | YES | (default) | YES | thin horizontal grey strip — placed inside each rule row to mark the LHS→RHS gap |
| `jpafjzbfwiqA1` | 1x1 | 8 | tjaqvwdgkxe | 1 | YES | (default) | YES (visible=False set on level start) | hidden tag-marker for double-translation rules (level 4+) |
| `jpafjzbfwiqA2` | 1x1 | 12 | tjaqvwdgkxe | 1 | YES | (default) | YES (hidden) | hidden tag-marker (level 4+) |
| `jpafjzbfwiqB1` | 1x1 | 9 | tjaqvwdgkxe | 1 | YES | (default) | YES (hidden) | hidden tag-marker (level 4+) |
| `jpafjzbfwiqB2` | 1x1 | 14 | tjaqvwdgkxe | 1 | YES | (default) | YES (hidden) | hidden tag-marker (level 4+) |
| `nxkictbbvztA1` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-A glyph #1 (T-stem with cross) |
| `nxkictbbvztA2` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-A glyph #2 (Z-zigzag) |
| `nxkictbbvztA3` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-A glyph #3 (E with prongs) |
| `nxkictbbvztA4` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-A glyph #4 (cross/plus with extra arm) |
| `nxkictbbvztA5` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-A glyph #5 (H/I bone shape) |
| `nxkictbbvztA6` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-A glyph #6 (P-with-tail) |
| `nxkictbbvztA7` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-A glyph #7 (M / inverted-U with prongs) |
| `nxkictbbvztB1` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-B glyph #1 (D-shape) |
| `nxkictbbvztB2` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-B glyph #2 (boxed-cross) |
| `nxkictbbvztB3` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-B glyph #3 (P-with-curve) |
| `nxkictbbvztB4` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-B glyph #4 (B/8 with internal cross) |
| `nxkictbbvztB5` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-B glyph #5 (Q-with-tail) |
| `nxkictbbvztB6` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-B glyph #6 (chunky diamond outline) |
| `nxkictbbvztB7` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-B glyph #7 (plus with stem-extension) |
| `nxkictbbvztC1` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-C glyph #1 (E-with-three-prongs / comb) |
| `nxkictbbvztC2` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-C glyph #2 (split-S broken in middle) |
| `nxkictbbvztC3` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-C glyph #3 (vertical I-bar with side prongs) |
| `nxkictbbvztC4` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-C glyph #4 (cross with diagonal taps) |
| `nxkictbbvztC5` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-C glyph #5 (square-bracket frame with internal dot) |
| `nxkictbbvztC6` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-C glyph #6 (C-shape with internal slash) |
| `nxkictbbvztC7` | 5x5 | 5, -1 | nxkictbbvzt | (default) | YES | (default) | YES | alphabet-C glyph #7 (split-X with empty centre) |
| `nxkictbbvztedxeenecwqa` | 9x9 | 0 | (default) | -2 | YES | (default) | YES | solid black 9x9 overlay placed during the win-animation as a halo around each consumed rule-card |
| `qvtymdcqear1` | 5x2 | 0, -1 | (default) | (default) | YES | (default) | YES | hollow palette-0 bracket — top frame above the cursored card |
| `qvtymdcqear2` | 12x2 | 0, -1 | (default) | (default) | YES | (default) | YES | wider bracket — used when the cursor spans 2 cards (alter_rules) |
| `qvtymdcqear3` | 19x2 | 0, -1 | (default) | (default) | YES | (default) | YES | widest bracket — used for 3-card spans (alter_rules with longer LHS) |

### `background` — palette-3 horizontal letter-box (every L1-3 level)
- Pixel pattern: 2x1 of palette-3 (grey), placed at scale=32 → renders as a 64-wide × 32-tall block filling the upper or lower half of the frame.
- Where it appears: every level (always at y=34 in L1-3, y=37/38/41 in L4-6).
- Role: visual divider between the "rules" region (top) and the "tapes" region (bottom). Read at level start to find the y-cutoff for separating rule-glyphs from tape-glyphs.
- Visual-vs-functional read: at-rendered-scale a 32-pixel solid grey horizontal strip; reads as a flat shelf-line. Palette-3 also matches the global `PADDING_COLOR` so it blends seamlessly with the letter-box. Nearest-other-sprite: `iqrduxrukrk` is also palette-3 but a thin 11x1 strip — different role (rule-internal LHS/RHS gap), placed inside the rules region.
- Visual contrast notes: against palette-2 (game background), palette-3 reads as a darker grey shelf.

### `background2` — vertical version of background (defined but unused)
- Pixel pattern: 1x2 palette-3.
- Where it appears: never placed.
- Role: dead sprite.
- Visual-vs-functional read: identical palette signature to `background` — would be visually indistinguishable on rendering.

### `gyrdjxybtcmA` — cyan colour-card backdrop (every L1-3 level)
- Pixel pattern: 7x7 solid palette-10.
- Where it appears: heavily used in L1, L3 (multiple copies as alphabet-A backdrops); also placed below the background line as bottom-tape backdrops.
- Role: the visual backdrop telling the player "this card belongs to alphabet A". The 5x5 glyph (`nxkictbbvztA*`) is overlaid on top; together they form a "card" = (cyan, glyph-1..7).
- Visual-vs-functional read: at-rendered-scale a 7x7 cyan square. Palette signature: 10 alone. Tag `gyrdjxybtcm` is shared with B and C variants. The colour is the alphabet identifier; the glyph is the letter identifier. Player learns "cyan = A alphabet, pink = B alphabet, yellow = C alphabet". Nearest-other-sprite: `gyrdjxybtcmB` (pink) and `gyrdjxybtcmC` (yellow) — same shape, different colour.
- Visual contrast notes: cyan-10 against palette-2 background reads boldly; the overlaid black glyph is salient on cyan.

### `gyrdjxybtcmB` — pink colour-card backdrop
- Pixel pattern: 7x7 solid palette-7.
- Where it appears: every L1-3 level.
- Role: alphabet-B backdrop. Glyphs `nxkictbbvztB*` overlay on top.
- Visual-vs-functional read: 7x7 pink square. Nearest-other: `gyrdjxybtcmA` and `gyrdjxybtcmC` — same shape different palette. Pink-7 contrasts with black glyphs.

### `gyrdjxybtcmC` — yellow colour-card backdrop
- Pixel pattern: 7x7 solid palette-11.
- Where it appears: L2 and L3 (used heavily for alphabet-C cards).
- Role: alphabet-C backdrop.
- Visual-vs-functional read: 7x7 yellow square. Yellow-11 contrasts with black glyphs.

### `iqrduxrukrk` — palette-3 horizontal LHS/RHS rule-gap
- Pixel pattern: 11x1 palette-3.
- Where it appears: every L1-3 level (multiple copies, one per rule).
- Role: marks the gap inside a single rule row that separates the LHS card sequence from the RHS card sequence. Placed at y=middle-of-rule-row, spanning 11 cells of horizontal gap. The on_set_level function uses the iqrduxrukrk's left edge to find the LHS sprite (`get_sprite_at(left_edge_x, y, "nxkictbbvzt")`) and walks left to assemble the LHS chain; uses the right edge to find the first RHS card and walks right.
- Visual-vs-functional read: at-rendered-scale a thin grey horizontal strip. Visually unobtrusive — looks like a faded background line. Functionally critical: it's the rule-parser's separator. Nearest-other-sprite: `background` (also palette-3) is the rule/tape divider — same colour, different role; player tells them apart by length (background is full-width, iqrduxrukrk is 11px wide).
- Visual contrast notes: blends with background-3 region; visible only as a thin gap inside each rule.

### `jpafjzbfwiqA1` — hidden palette-8 tag-marker (level 4+)
- Pixel pattern: single cell palette-8 (orange).
- Where it appears: not placed in L1-3. Set `visible=False` at level start regardless.
- Role: out of scope — used by `lonhgifaes` helper in `bsqsshqpox` for the `double_translation` rule chain (level 4+).
- Visual-vs-functional read: invisible (visible=False); never rendered.

### `jpafjzbfwiqA2` — hidden palette-12 tag-marker (level 4+)
- Pixel pattern: single cell palette-12.
- Where it appears: not placed in L1-3.
- Role: out of scope.

### `jpafjzbfwiqB1` — hidden palette-9 tag-marker (level 4+)
- Pixel pattern: single cell palette-9.
- Where it appears: not placed in L1-3.
- Role: out of scope.

### `jpafjzbfwiqB2` — hidden palette-14 tag-marker (level 4+)
- Pixel pattern: single cell palette-14.
- Where it appears: not placed in L1-3.
- Role: out of scope.

### `nxkictbbvztA1` — alphabet-A letter #1
- Pixel pattern: 5x5; vertical stem of palette-5 in col 2, with a horizontal cross-piece at row 2 and a wider base across row 4. Reads as a "T with stem and base".
- Where it appears: L1, L3 (in rule rows and on the bottom tape).
- Role: glyph #1 of the A alphabet. Cycled by `wpbnovjwkv` (incrementing/decrementing the trailing digit modulo 7).
- Visual-vs-functional read: 5x5 black-on-cyan glyph, only renderable on top of `gyrdjxybtcmA` (since both share a 7x7 vs 5x5 size and the glyph is centred on the colour-block by the level placement). Palette signature: 5 + transparent. Nearest-other: `nxkictbbvztB1`, `nxkictbbvztC1` — different alphabets, different shapes. Within alphabet A, the 7 glyphs (A1..A7) are visually distinct shapes designed to be distinguishable at 5x5.
- Visual contrast notes: black on cyan reads cleanly.

### `nxkictbbvztA2` — alphabet-A letter #2
- Pixel pattern: 5x5; reads as a Z-shape with a top-right stub and a bottom-left stub plus a long diagonal stroke.
- Where it appears: L1 (twice), L5.
- Role: A alphabet glyph #2.

### `nxkictbbvztA3` — alphabet-A letter #3
- Pixel pattern: 5x5; reads as an "E" — full left column plus three horizontal prongs at top, middle, bottom.
- Where it appears: L1, L3.
- Role: A alphabet glyph #3.

### `nxkictbbvztA4` — alphabet-A letter #4
- Pixel pattern: 5x5; full middle row + full middle column with extra arms branching off → "+" with an additional vertical extension.
- Where it appears: L1, L3, L4.
- Role: A alphabet glyph #4.

### `nxkictbbvztA5` — alphabet-A letter #5
- Pixel pattern: 5x5; H-shape with full middle row, vertical bars at cols 0 and 4, and a single dot at row 2.
- Where it appears: L1, L3, L5.
- Role: A alphabet glyph #5.

### `nxkictbbvztA6` — alphabet-A letter #6
- Pixel pattern: 5x5; reads as "P" — full top row, partial right side, full middle row.
- Where it appears: L3, L4, L6.
- Role: A alphabet glyph #6.

### `nxkictbbvztA7` — alphabet-A letter #7
- Pixel pattern: 5x5; M-style with top corners, full top row, vertical legs, and a full bottom row with gap in centre.
- Where it appears: L1, L3, L4, L6.
- Role: A alphabet glyph #7.

### `nxkictbbvztB1` — alphabet-B letter #1
- Pixel pattern: 5x5; full left column + 4-cell top bar + 4-cell bottom bar + interior right side.
- Where it appears: L1, L2, L4.
- Role: B alphabet glyph #1.

### `nxkictbbvztB2` — alphabet-B letter #2
- Pixel pattern: 5x5; closed rectangle frame with internal middle column and dot.
- Where it appears: L1, L2, L6.
- Role: B alphabet glyph #2.

### `nxkictbbvztB3` — alphabet-B letter #3
- Pixel pattern: 5x5; reads as "P" with top hook curving right then down.
- Where it appears: L1, L2, L4.
- Role: B alphabet glyph #3.

### `nxkictbbvztB4` — alphabet-B letter #4
- Pixel pattern: 5x5; full middle row, full top row except outer corners, full bottom row, internal vertical strokes.
- Where it appears: L2.
- Role: B alphabet glyph #4.

### `nxkictbbvztB5` — alphabet-B letter #5
- Pixel pattern: 5x5; full top, sides, middle row, with a single tail dot at bottom-centre.
- Where it appears: L1, L2, L5.
- Role: B alphabet glyph #5.

### `nxkictbbvztB6` — alphabet-B letter #6
- Pixel pattern: 5x5; chunky diamond / hex outline with internal hollow.
- Where it appears: L1 (multiple), L2, L4, L5.
- Role: B alphabet glyph #6.

### `nxkictbbvztB7` — alphabet-B letter #7
- Pixel pattern: 5x5; cross-shape "+" with stem at top.
- Where it appears: L1, L2, L4, L6.
- Role: B alphabet glyph #7.

### `nxkictbbvztC1` — alphabet-C letter #1
- Pixel pattern: 5x5; full left column, three small horizontal prongs at rows 0, 2, 4 — comb-like.
- Where it appears: L2 (twice), L3 (multiple), L4, L6.
- Role: C alphabet glyph #1.

### `nxkictbbvztC2` — alphabet-C letter #2
- Pixel pattern: 5x5; broken S-shape with diagonal across the middle, gaps top and bottom.
- Where it appears: L2 (multiple), L3, L4.
- Role: C alphabet glyph #2.

### `nxkictbbvztC3` — alphabet-C letter #3
- Pixel pattern: 5x5; vertical I-bar of palette-5 down the middle column with horizontal taps at top and bottom.
- Where it appears: L2 (twice), L3, L6 (twice).
- Role: C alphabet glyph #3.

### `nxkictbbvztC4` — alphabet-C letter #4
- Pixel pattern: 5x5; vertical strokes at multiple columns crossing horizontal middle row → "+" with diagonal accents.
- Where it appears: L2, L3, L4.
- Role: C alphabet glyph #4.

### `nxkictbbvztC5` — alphabet-C letter #5
- Pixel pattern: 5x5; outer frame (top + sides + bottom) with single interior dot at row 2 col 2.
- Where it appears: L2 (multiple in bottom-tape area), L3 (twice), L4, L6.
- Role: C alphabet glyph #5.

### `nxkictbbvztC6` — alphabet-C letter #6
- Pixel pattern: 5x5; left column + two horizontal half-prongs creating a "C" shape with internal slash.
- Where it appears: L2, L3.
- Role: C alphabet glyph #6.

### `nxkictbbvztC7` — alphabet-C letter #7
- Pixel pattern: 5x5; corners only of two diagonals → "X" with empty centre.
- Where it appears: L2, L3.
- Role: C alphabet glyph #7.

### `nxkictbbvztedxeenecwqa` — palette-0 9x9 win-halo overlay
- Pixel pattern: solid 9x9 palette-0.
- Where it appears: never placed at level start; cloned and added during the win-animation in `step()` to highlight each consumed rule-card.
- Role: visual feedback during the level-clear animation. `step()` adds one of these per consumed card (as a halo behind it) and removes them at each animation frame transition.
- Visual-vs-functional read: solid black 9x9 — at-rendered-scale a slightly-larger-than-card black square that frames the card during animation. Layer -2 so it sits behind the colour cards.

### `qvtymdcqear1` — narrow bracket-cursor (1-card-wide)
- Pixel pattern: 5x2; row 0 solid palette-0 (5 cells), row 1 with palette-0 only at the two end-corners (`0, -1, -1, -1, 0`). Renders as a hollow-bottom bracket: solid top edge with two short side-arms.
- Where it appears: every L1-3 level — instantiated in `on_set_level` as `qvtymdcqear_parts[0]` (and a 180°-rotated copy as `qvtymdcqear_parts[1]`); positioned above and below the currently-selected card.
- Role: cursor indicator for the bracketed/edited card.
- Visual-vs-functional read: at-rendered-scale a 5x2 black bracket above the card and an upside-down version 2-rows below. Together they enclose the card the player is currently editing. Palette signature: 0 + transparent. Nearest-other: `qvtymdcqear2` and `qvtymdcqear3` are wider variants — used in alter_rules mode (level 5+) where the cursor spans 2 or 3 cards.
- Visual contrast notes: solid palette-0 (black) brackets on top of cyan/pink/yellow cards — high contrast, unambiguous.

### `qvtymdcqear2` — 2-card-wide bracket (level 5+ alter_rules)
- Pixel pattern: 12x2 hollow-bottom bracket.
- Where it appears: instantiated at level start but rendered only when the cursor spans 2 cards in alter_rules mode (L5+).
- Role: out of scope (the L5 alter_rules flag activates this width).

### `qvtymdcqear3` — 3-card-wide bracket (level 5+/6+)
- Pixel pattern: 19x2 hollow-bottom bracket.
- Where it appears: instantiated at level start; rendered only when alter_rules + sufficiently long LHS triggers it.
- Role: out of scope.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (64, 64)
- Number of sprites placed: 50 (1 background + 11 A-cards + 11 B-cards + 0 C-cards + 6 iqrduxrukrk + 21 nxkictbbvzt glyphs).

  Counting more carefully: 1 background, 11 gyrdjxybtcmA, 11 gyrdjxybtcmB, 6 iqrduxrukrk, 21 nxkictbbvzt cards. Total = 50.
- Composition by role: 6 rules in the upper region (each consisting of 2-card LHS + 11px gap + RHS), arranged in 3 rule rows of 2 rules each (left half x=12-32, right half x=35-55) at y=4, y=13, y=22; PLUS a 7th area below the rule shelf at y=40-52 containing 6 input-tape cards at y=41 and 5 output-tape cards at y=52.

  Background separator at (0, 34) scaled to fill width = 32-64 covers row 34-65 visually.

  Top-region rule-cards: 11 A-cards + 11 B-cards = 22 colour-card backdrops. Each card has a 5x5 glyph overlay → 22 glyph-cards in the rule region (but only 19 glyphs are placed; the source places fewer glyphs than colour-cards because some duplicate slots in rules share glyphs, e.g. nxkictbbvztA1 placed at multiple positions).

  Bottom-region tape-cards (y=40-52): 5 A-cards at y=40 + 5 B-cards at y=51 form the input/output tapes. Each tape position has a colour-card backdrop and one glyph-card on top.
- Level data: `{}` (no `data=` kwarg).
- Spawn position(s): no avatar; the cursor is implicitly placed at index 0 of `ztgmtnnufb` (the bottom-tape list, sorted by (y, x) at level start). The first L1 bottom card is at (15, 52).
- Per-cell layout (coordinate listing):
  - background: (0, 34) scaled 32x.
  - Rule-row 1 (y=4): two rules side-by-side. Left rule: card at (12,4)+glyph at (13,5) [A3], card at (22,4)+glyph at (23,5) [B6], iqrduxrukrk at (15,7), card at (35,4)+glyph at (36,5) [A5], card at (45,4)+glyph at (46,5) [B5], iqrduxrukrk at (38,7).
  - Rule-row 2 (y=13): card+glyph at (12,13)[A1], card at (22,13)+glyph at (23,14)[B1], iqrduxrukrk at (15,16), card at (35,13)+glyph at (36,14)[A4], card at (45,13)+glyph at (46,14)[B3], iqrduxrukrk at (38,16).
  - Rule-row 3 (y=22): card at (12,22)+glyph at (13,23)[A2], card at (22,22)+glyph at (23,23)[B2], iqrduxrukrk at (15,25), card at (35,22)+glyph at (36,23)[A7], card at (45,22)+glyph at (46,23)[B7], iqrduxrukrk at (38,25).
  - Bottom tape-row at y=40: 5 A-cards at x=14, 21, 28, 35, 42; glyphs at y=41 spanning these (B6 cards repeat 5x at row 40 for the input tape — wait actually the glyphs at y=41 are mixed: A4@15, A2@22, A3@29, A1@43, A5@36 according to the level data).
  - Bottom tape-row at y=51: 5 B-cards at x=14, 21, 28, 35, 42; glyphs at y=52 are B6 cards (×5).
- Mechanic introduced relative to the previous level: this is the first level — introduces the **rule-rewrite** mechanic. The 6 rules at the top each pair an LHS card-sequence with an RHS card-sequence. The 5-card input tape (top-of-bottom-region, y=40-46) is consumed left-to-right; for each prefix, find a rule whose LHS matches and write the rule's RHS into the output tape (bottom-of-bottom-region, y=51-57) at the corresponding position. The player edits the output tape by sliding a bracket-cursor (LEFT/RIGHT = ACTION3/4) and cycling glyphs (UP/DOWN = ACTION1/2). The bracket is rendered above and below the currently selected card. On `on_set_level`, all glyph-cards are randomly rotated 0/90/180/270 (deterministic per-level seed: 4, 2, 1 for L1, L2, L3) — so the same glyph can appear in 4 different orientations, multiplying the apparent letter count. The bottom output tape's glyphs are also randomised at level start (each card cycled 0..6 times via `wpbnovjwkv` with the same per-level random seed 7, 7, 32, 18, 23, 11 from `ripmydnety[i]`).
- Specific challenge: the player must read the 6 rules to discover which 5-card LHS-prefix-sequence describes the input tape; then construct the RHS sequence in the output tape by cycling each card's glyph through its alphabet until it matches what the rule says. Because all glyphs are randomly rotated, the player must mentally derotate to compare.
- Estimated optimal action count: each card needs ≤ 6 cycles (mod-7 alphabet) = ~6 actions per output card × 5 output cards = ~30 actions, plus ~10 cursor moves between cards = ~40 actions. The 128-step budget gives generous margin.

### Level 2
- `grid_size`: (64, 64)
- Number of sprites placed: 64 (1 background + 10 B-cards + 19 C-cards + 6 iqrduxrukrk + 28 nxkictbbvzt cards).
- Composition by role: 6 rules in upper region; tape-region with 7 input cards and 7 output cards at the bottom (more cards per tape than L1).
- Level data: `{}` (no extra data flags — same mechanic as L1).
- Spawn position(s): cursor at index 0 of bottom-tape (sorted by (y, x)).
- Per-cell layout: background at (0, 34) scaled 32x. Upper rule-region uses B-cards (alphabet B as LHS) and C-cards (alphabet C as RHS) — different alphabets than L1.
  - Rules at y=4, y=13, y=22 with 6 separators (iqrduxrukrk at y=7, y=16, y=25 in two columns).
  - Input tape at y=41: 7 cards across x=19, 26, 33, 40, 47, 54 (and one earlier).
  - Output tape at y=52: 7 cards. Each card is C-coloured → glyph from C alphabet (C5 is the most common, since each starting card is randomised by ±0..6 cycles).
- Mechanic introduced relative to L1: **alphabet shift** — instead of A→B mapping (L1), L2 uses B→C mapping. Same mechanic, different alphabet pair. More cards per tape (7 vs 5) so the rule-application chain is longer.
- Specific challenge: with 7 output cards to set, the budget cost rises proportionally. Random rotation continues to apply. Because the player has now seen the L1 mechanic, the challenge is endurance + alphabet familiarity rather than discovery.
- Estimated optimal action count: ~7 cards × 6 cycles + ~14 cursor moves = ~56 actions. Comfortable within 128.

### Level 3
- `grid_size`: (64, 64)
- Number of sprites placed: 73 (1 background + 16 A-cards + 18 C-cards + 6 iqrduxrukrk + 32 nxkictbbvzt cards).
- Composition by role: rule-region uses A and C alphabets (instead of A+B or B+C). Bottom region has 8 input cards and 8 output cards.
- Level data: `{}`.
- Spawn position(s): cursor at index 0 of bottom-tape.
- Per-cell layout: background at (0, 34) scaled 32x. Rules at y=4, y=13, y=22. Input tape at y=40 (A-cards), output tape at y=51 (A-cards too, since L3's input AND output are both A alphabet).

  Wait, looking more carefully at L3: the colour-cards placed at y=40 (input tape) are gyrdjxybtcmC (yellow), at (4,40)..(53,40). Output tape at y=51 is gyrdjxybtcmA (cyan), at (7,51)..(49,51). Plus 8 A-glyphs are placed there too. So input is C alphabet, output is A alphabet — i.e. the rules transform C → A.

  Rule-region uses A as LHS and C as RHS — wait checking again. The card layout in L3:
  - At y=4, 13, 22 (the rule rows): mix of A-cards (16 placed) and C-cards (18 placed).
  - Below y=34: A-cards at y=51 (8 copies), C-cards at y=40 (7 copies) and at y=40 (8 more, including one at (4,40)).
  
  The on_set_level partitions glyphs below background.y into bottom-tape lists. The first list (`zvojhrjxxm`) has y == min-y-below-background; the rest (`ztgmtnnufb`) has the larger y.
  
  In L3 `background.y = 34`. Below that: glyphs at y=41 (input cards) and y=52 (output cards).
  
  Counting glyphs at y=41: ~8 cards. Counting glyphs at y=52: ~8 cards. So input tape has 8, output tape has 8.
- Mechanic introduced relative to L2: **alphabet pair swap** — L3 uses C → A rules instead of B → C. Plus 8 cards per tape (longer than L2's 7).
- Specific challenge: same mechanic, slightly longer tape, slightly more rules to disambiguate.
- Estimated optimal action count: ~8 cards × 6 cycles + ~16 cursor moves = ~64 actions.

Levels 4, 5, 6 exist but are excluded per skill scope. (L4 sets `data={"double_translation": True}`, L5 sets `data={"alter_rules": True}`, L6 sets all three flags including `tree_translation`.)

## Action handlers

### ACTION1 (UP — cycle current card backward) and ACTION2 (DOWN — cycle current card forward)
- Trigger: `self.action.id in [GameAction.ACTION1, GameAction.ACTION2]`.
- Branches inside `step()`: first the win-animation guard (`self.yfetxjexviz >= 0`) — returns early without consuming budget if an animation is in progress. Otherwise compute `pxdsteijos = -1` for ACTION1 / `+1` for ACTION2. Branch on `current_level.get_data("alter_rules")` — for L1-3 this is None/False, so the source takes the simple path: `riedikehfs = self.ztgmtnnufb[self.qvtymdcqear_index]`, then `self.ztgmtnnufb[idx] = self.wpbnovjwkv(riedikehfs, pxdsteijos)`. The `wpbnovjwkv` helper extracts the trailing digit, increments/decrements modulo 7 (cycles A1→A2→...→A7→A1), creates a fresh sprite from the new name, copies position and rotation from the old sprite, removes the old sprite, adds the new one with `BlockingMode.BOUNDING_BOX`, and returns the new sprite. Decrement step budget by 1 (`upmkivwyrxz -= 1`). Call `bsqsshqpox()` to check the win predicate; if True, hide the bracket parts (`set_visible(False)`) and start the win animation by setting `yfetxjexviz = 0`, return without `complete_action()` (animation will fire `complete_action` when finished). Otherwise, fall through to the budget check at the bottom (`if upmkivwyrxz == 0: lose()`) then `complete_action()`.
- State mutations: read `self.ztgmtnnufb`, `self.qvtymdcqear_index`, `self.action.id`, `self.current_level`. Written: `self.ztgmtnnufb[idx]`, `self.upmkivwyrxz`, possibly `self.yfetxjexviz`, possibly hidden bracket sprites. Implicitly written by `wpbnovjwkv`: removes the old sprite from level and adds a new one.
- Side effects on sprites: replaces the bracketed card sprite with a new sprite of the next/previous glyph in the same alphabet; preserves position, rotation, and blocking mode.
- Engine effects: if `bsqsshqpox` returns True, hides bracket-cursor and starts win-animation that culminates in `next_level()`. If budget hits 0, calls `lose()`.
- Pre-conditions / gating: none beyond budget. The cycle wraps modulo 7 (always succeeds). For `alter_rules` mode (L5+), the same action cycles ALL cards in a rule simultaneously instead of one card.

### ACTION3 (LEFT — cursor backward) and ACTION4 (RIGHT — cursor forward)
- Trigger: `self.action.id in [GameAction.ACTION3, GameAction.ACTION4]`.
- Branches: same animation-guard. Otherwise `pxdsteijos = -1 / +1`. For L1-3 (no alter_rules), `self.qvtymdcqear_index = (self.qvtymdcqear_index + pxdsteijos) % len(self.ztgmtnnufb)`. Decrement budget. Call `pjqbnqnbsq()` to reposition the bracket-cursor sprites at the new card's location (above and below). Fall through to budget check.
- State mutations: read `self.qvtymdcqear_index`, `self.ztgmtnnufb`. Written: `self.qvtymdcqear_index`, `self.upmkivwyrxz`, `qvtymdcqear_parts[0/1].position`.
- Side effects on sprites: bracket-cursor `set_position` to wrap around the new currently-selected card.
- Engine effects: if budget hits 0, `lose()`. No win check on cursor movement (only ACTION1/2 trigger `bsqsshqpox`).
- Pre-conditions / gating: cursor index wraps modulo `len(ztgmtnnufb)` so cannot go out of bounds.

## HUD widgets

### `cjcjtddeyl` — bottom-row depleting step bar
- Class name (obfuscated): `cjcjtddeyl`.
- Render-pixel range: row 63 (the very bottom row of the 64-tall frame), all 64 columns.
- What value it displays: `self.aqrjzwnzcx.upmkivwyrxz / self.aqrjzwnzcx.vfpimnmtnta` — proportion of step budget remaining. `vfpimnmtnta` is 128 for L1-4, 256 for L5+. `upmkivwyrxz` counts down from `vfpimnmtnta` to 0.
- Visual style: row 63 is filled with palette-4 (background-grey for the depleted portion) by default, then overwritten with palette-1 (light-grey) for the leading `ysswxajmmd = ceil(64 * remaining/total)` pixels. So the LEFT segment is light-grey (full) and the right is darker (empty). As the budget drains, the light-grey segment shrinks from the right edge.
- Update points: every render frame; the value is read fresh from `self.aqrjzwnzcx.upmkivwyrxz` which is decremented in `step()` per action.
- Where it is registered: instantiated as `cjcjtddeyl(self)` and added directly to the `Camera(interfaces=[cjcjtddeyl(self)])` constructor — only one HUD class for this game.

## Internal state — exhaustive

| attr (obfuscated) | semantic name | type | initial value | written by | read by | role |
|---|---|---|---|---|---|---|
| `zdwrfusvmx` | all_glyph_cards_sorted | `list[Sprite]` | `[]` | `on_set_level` | `qrkneeaawb`, `pjqbnqnbsq` (indirectly) | every `nxkictbbvzt`-tagged sprite in the level, sorted by (y, x); used as the universe of card-sprites for the rule parser |
| `zvojhrjxxm` | input_tape_cards | `list[Sprite]` | `[]` | `on_set_level` | `bsqsshqpox`, `iwbhnvdaao` | the input tape — bottom-region cards at the smaller of the two y-rows (y=41 in L1) |
| `ztgmtnnufb` | output_tape_cards | `list[Sprite]` | `[]` | `on_set_level`, `step` | `step`, `pjqbnqnbsq`, `bsqsshqpox` | the output tape — bottom-region cards at the larger y-row (y=52 in L1); the player edits these |
| `cifzvbcuwqe` | rules | `list[tuple[list[Sprite], list[Sprite]]]` | `[]` | `on_set_level` | `step` (alter_rules), `bsqsshqpox`, `pjqbnqnbsq` (alter_rules) | list of (LHS, RHS) pairs, one per `iqrduxrukrk` separator. LHS and RHS are lists of card sprites read by walking left/right from the separator |
| `qvtymdcqear_index` | cursor_position | int | 0 | `on_set_level`, `step` (ACTION3/4) | `step`, `pjqbnqnbsq` | which entry of `ztgmtnnufb` (or all-rules-flat in alter_rules) the cursor points to |
| `qvtymdcqear_parts` | bracket_sprites | `list[Sprite]` (length 2) | `[qvtymdcqear1.clone(), qvtymdcqear1.clone().set_rotation(180)]` | `on_set_level`, `pjqbnqnbsq`, `step` (win) | `pjqbnqnbsq`, `step` | the upper and lower bracket-cursor visual sprites |
| `vfpimnmtnta` | max_step_budget | int | 128 (L1-4) or 256 (L5+) | `on_set_level` | `step`, HUD | denominator of the step-counter ratio |
| `upmkivwyrxz` | remaining_steps | int | `vfpimnmtnta` (= 128 for L1-3) | `on_set_level`, `step` (every move) | `step` (lose check), HUD, `_get_hidden_state` | budget counter; lose at 0 |
| `yfetxjexviz` | win_animation_tick | int | -1 | `on_set_level`, `step` | `step` (very first guard) | -1 = idle; 0..N = animation tick index. The animation iterates through every consumed (LHS-cards, RHS-cards) pair and recolours them through the palette sequence `[5, 8, 14, 15, 6, 9, 12, 0]` over `len(palette)-1=7` ticks per pair |
| `pvgetmhmhgk` | consumed_pairs | `list[tuple[list[Sprite], list[Sprite]]]` | `[]` | `on_set_level`, `bsqsshqpox` | `step` (animation) | the rule-application history reconstructed by `bsqsshqpox` on a successful match — pair k is the kth (input_tape_segment, output_tape_segment) consumed by rule k |
| `hgfgmiagdcc` | rule_card_groups | `list[list[Sprite]]` | `[]` | `on_set_level`, `bsqsshqpox` | `step` (animation) | the source-rule's card groups for each consumed pair (used to halo the rules during animation) |
| `crvjftupafy` | active_halo_overlays | `list[Sprite]` | `[]` | `on_set_level`, `step` (animation) | `step` (animation) | currently-spawned `nxkictbbvztedxeenecwqa` halo sprites; cleared and re-spawned at each animation pair-transition |

## Win condition

Plain English: the level wins when the contents of the output tape (`ztgmtnnufb`) are exactly the rule-rewrite of the input tape (`zvojhrjxxm`) under the placed rule set. Specifically: walking left-to-right across the input tape, the player must be able to partition it into prefix-segments where each segment matches some rule's LHS, and the corresponding output-tape segment matches the same rule's RHS.

Literal condition: `self.bsqsshqpox()` (lines 1022-1083) returns True when:
- Iterating with two pointers (`eutyeiwurz` into input tape, `pcxqrgcdzp` into output tape):
- For each iteration, find a rule (LHS, RHS) such that `iwbhnvdaao(zvojhrjxxm, eutyeiwurz, LHS)` is True (input-tape prefix matches LHS by sprite-name) AND `iwbhnvdaao(ztgmtnnufb, pcxqrgcdzp, RHS)` is True (output-tape prefix matches RHS by sprite-name);
- Advance both pointers by the lengths of LHS and RHS;
- If no rule matches at the current position, return False;
- If both pointers reach end-of-tape simultaneously, return True.

Called from `step()` at line 993 immediately after a successful UP/DOWN cycle. On True, hide bracket-cursor sprites and start the win-animation by setting `yfetxjexviz = 0`. The animation fires `next_level()` after `len(consumed_pairs) * (len(palette)-1) = N*7` ticks (lines 970-972).

(For `double_translation` and `tree_translation` flags at L4+, the predicate has additional rule-chaining logic; these are out of scope.)

## Lose condition

Plain English: lose if the step budget reaches 0 without solving the level.

Literal condition: at the bottom of `step()` (line 998-999):
```python
if self.upmkivwyrxz == 0:
    self.lose()
```

The budget decrements only on successful ACTION1-4 dispatches — not during the win-animation.

There is no other lose path (no hazard, no respawn cost).

## Resource economy

- Depleting resource (energy / step counter / lives): YES — `self.upmkivwyrxz` step counter, displayed as the bottom-row depleting bar by `cjcjtddeyl`, decremented 1 per arrow-key action, threshold 0 triggers `lose()`. Initial value 128 for L1-3 (256 for L5+).
- Accumulating resource (collected items, score, sequence progress): NO. There is no collected-item count. The output tape's correctness is binary (matches all rules or doesn't) and only assessed at the moment of an UP/DOWN cycle.
- Lives mechanic (respawn cost): NO. Single `lose()` ends the game.
- Resource interaction with win/lose: budget is the sole lose trigger; rule-rewrite match is the sole win trigger.

## Action-budget signature

- Default budget per level: 128 for L1-4, 256 for L5+ (`vfpimnmtnta = 128 if self._current_level_index <= 4 else 256` at line 945).
- Whether budget tightens or shifts across levels 1-3: NO — same 128 for L1, L2, L3.
- Per-level vs. per-environment: per-level (`upmkivwyrxz` reset to `vfpimnmtnta` at every `on_set_level`).
- Decrement rate per action: 1 per ACTION1/2/3/4. Win-animation ticks do NOT decrement the budget.
- Refill mechanism: NONE.

## Notable code patterns / techniques

- **Glyph-name string-arithmetic** (`wpbnovjwkv`): cycles a glyph by parsing the trailing digit from the obfuscated name (`nxkictbbvztA3` → digit "3"), incrementing/decrementing modulo 7, and rebuilding the name (`nxkictbbvztA{(3+1-1)%7+1}` = `nxkictbbvztA4`), then looking up the new sprite in the `sprites` dict. This is a clean stateless cycle with no separate per-card index. A generated game wanting cycling could reuse the pattern.
- **Per-level deterministic randomisation seeds** (`ofysoutulp = [4, 2, 1, 2, 12, 20]` for rotation, `ripmydnety = [7, 7, 32, 18, 23, 11]` for output-tape initial cycling): makes the level reproducible and allows tuning difficulty per level.
- **Tag-based sprite collection** (`get_sprites_by_tag("nxkictbbvzt")`, `get_sprites_by_tag("tjaqvwdgkxe")`, `get_sprites_by_tag("gyrdjxybtcm")`): clean separation of "card glyphs" vs "colour backdrops" vs "rule-marker tags".
- **Position-relative neighbour lookup** (`qrkneeaawb`): given a card sprite, find the next/previous card in the same row by checking `s.x == ekifeojqhe.x + pxdsteijos * iokndxodxw` (where `iokndxodxw=7` is the card spacing). This is a pure spatial neighbour-walk pattern — no need for a precomputed adjacency dict.
- **In-place sprite swap with retained position+rotation** (`wpbnovjwkv` lines 1004-1006): clones a fresh sprite from the dict, copies position and rotation, sets blocking mode, removes the old, adds the new. Idiomatic for "change the visual without changing the slot".
- **Bracket-cursor as two separate sprites** (`qvtymdcqear_parts[0/1]` rotated 180°): instead of a single sprite that spans both top and bottom of the cursored card, use two narrow brackets that the engine can position and render independently. Cleaner than a tall hollow-frame sprite.
- **Win-animation as state-machine in `step()`** (lines 953-973): the animation reuses the `step()` method by gating on `yfetxjexviz >= 0`. Each step-call advances one tick; the dispatch returns early before processing the action. This means animation ticks do not consume input or budget, and the player's actions during the animation are silently swallowed.
- **`get_data` flag-based mechanic gating** (`alter_rules`, `double_translation`, `tree_translation`): each level can opt into mechanic variants via boolean flags in `level.data`. The `step()` and `bsqsshqpox()` methods branch on these flags. This is a clean way to layer mechanics onto a base game.

## Anti-patterns / lessons

- **Random rotation of every glyph card** (`set_rotation(fcnjuctdrc.choice([0, 90, 180, 270]))` at line 897) — the glyph identity is encoded in the name and the rotation is decorative, but it makes the player's visual matching task much harder. For L1 this might be intentional (forces careful inspection); for a generated 3-level game this might be over-difficult — consider rotation-fixed glyphs.
- **`background2` is defined but never placed** — dead sprite. Generated games should not ship dead sprite definitions.
- **`jpafjzbfwiqA1/A2/B1/B2` are placed but `set_visible(False)` immediately** — these are tag-marker sprites used only by the L4+ `double_translation` rule chain. For a 3-level game, this whole concept is unnecessary.
- **The level data flags pile up** (`alter_rules`, `double_translation`, `tree_translation`) — three orthogonal mechanic-variants packaged as boolean flags, each adding ~30 lines of branch logic to `step()` and `bsqsshqpox()`. A 3-level generated game should pick one variant and stick to it.
- **Animation tick-count dependent on rule count** (`len(self.pvgetmhmhgk) * (len(rhoqllymmn) - 1) = 7N`) — for an N-rule level the win animation lasts 7N steps, during which the player cannot interact. For L3 with 8 cards and ~3-4 rules consumed, that's 21-28 idle ticks. Not a bug but disorienting.
- **Step budget 128 for L1-4 then 256 for L5+** — abrupt 2x jump between L4 and L5; smoother per-level tuning would be more pedagogical.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES (bottom row, full 64-pixel-wide depleting horizontal bar).
- Has lives mechanic: NO.
- Has click-to-select (uses ACTION6): NO.
- Has tag-based grouping (uses `level.get_sprites_by_tag`): YES (`get_sprites_by_tag("nxkictbbvzt")` in `on_set_level`, `get_sprites_by_tag("tjaqvwdgkxe")` for hidden marker setup).
- Uses ACTION5 (modal): NO.
- Uses ACTION6 (click): NO.
- Uses ACTION7: NO.
- Has level data dicts (uses `level.get_data` / `level.set_data`): YES (`level.get_data("alter_rules")`, `level.get_data("double_translation")`, `level.get_data("tree_translation")` — none of these are set in L1-3 but the code paths exist).
- Multi-mechanic per level (vs. single mechanic per level): NO for L1-3 — same rule-rewrite mechanic in all three levels with only the alphabet pair changing.
- Tutorial level appears solvable by random play: NO. With 7^N cycle combinations on the output tape and 6+ rules to satisfy, random play has effectively zero probability of finding the correct configuration in 128 steps.
- Has a depleting resource: YES — step counter, 128 per level (L1-4).
- Has an accumulating resource: NO (the output-tape state is not numeric; correctness is binary).
- Sprite shape convention used: mixed — colour-cards are filled 7x7 squares, glyphs are 5x5 abstract patterns (mostly hollow with strokes), brackets are hollow, separators are solid thin strips.
- HUD position: bottom (single row).
- Palette size used: 9 distinct palette values appear in placed sprites: {0, 3, 5, 7, 10, 11} from sprite bodies, plus {1, 4} drawn at runtime by the HUD; palette 8 also appears via the win-animation colour cycle `rhoqllymmn = [5, 8, 14, 15, 6, 9, 12, 0]` so the full set of palette colours that can appear on screen during a level transition is {0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15} = 14. Static (no-animation) palette use is 9 values.
- Background colour value: 2 (`BACKGROUND_COLOR = 2`).
- Padding / letter-box colour value: 3 (`PADDING_COLOR = 3`).
- Number of distinct mechanics introduced across levels 1-3: 1 (rule-rewrite mechanic; L2 and L3 just swap the alphabet pair without adding new mechanics).
- Number of levels documented: 3.

(End of file.)
