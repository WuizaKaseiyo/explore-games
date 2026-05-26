# mechanic-pick

## Game ID
`qx7p`

ID checks:
- 4 lowercase alphanumeric characters.
- Not in the 25 reserved reference IDs (ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15, tn36, tr87, tu93, vc33, wa30).
- Not in `prior-games/index.md` (kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, vn8d, fz5j, kn58, bx84, wt39, zk9p, rk7x, gx7m, vp6h, kp9z, zd7m, lv4k, xn5p, mr5q, pf3w, tg6w, vd3g, jd4q, ek73).
- Not an English word (`qx7p` is opaque).

## Mechanic family
`column-shift-row-align`

## Description (one paragraph)
The playfield shows a row of 3-5 tall vertical "columns", each painted
as a stack of differently-coloured horizontal segments (a vertical
bar-code). A horizontal "scan line" cuts across all columns at one
specific row. The cells of each column intersected by the scan line
display whichever segment of that column is currently aligned with the
line. The player clicks a column to make it active (visually
highlighted), then ACTION1/ACTION2 shift the active column up/down by
exactly one segment, scrolling the colour-band sequence past the scan
line. Below the playfield is a "target strip" showing the colour
pattern the scan line must match, cell-for-cell, for the level to
advance. There is no avatar, no walking, no projectile, no fluid: the
core verb is "shift this column's colour-band-stack one notch in
either direction". Difficulty grows in L2 by introducing **bound-pair
columns** (shifting one column shifts its partner column in the
opposite direction) and **blocker segments** (a special segment that,
once aligned with the scan line in a particular column, locks that
column from further shifts in that direction until other columns clear
it), and in L3 by introducing a **movable scan line** (ACTION5 shifts
the scan line itself up or down by one row, so the row at which
columns are read changes mid-puzzle).

Core-knowledge priors used: **objectness** (each column is a coherent
sliding entity), **basic geometry & topology** (scan line as a
horizontal axis, column stacks as 1D ordered lists, alignment as a
modular offset), and **basic physics** (bound-pair coupling acts like
a rigid linkage with a sign flip).

## Action mapping (anticipated; spec finalises)
- ACTION1: shift active column up by one segment.
- ACTION2: shift active column down by one segment.
- ACTION5: shift the scan line up/down (alternates direction or paired
  with another action, finalised in spec).
- ACTION6: click a column to select it as active.
- (ACTION3, ACTION4, ACTION7 unused — minimal action subset.)

## Distinguishing rules vs near-miss taxonomy entries

For each potentially-similar reference game I read both the mechanism-
details summary and the deep-analysis evidence layer.

### vs `lp85` (button-permutation-puzzle)
lp85 is a Rubik-style **horizontal+vertical row+column shift** puzzle
on a 2D grid of pawn cells: clicking a button on the perimeter shifts
the entire matching row or column by one cell, scrambling pawn
positions. The verb is "click a button → permute many cells at once".
qx7p has NO 2D pawn grid; instead it has independent vertical columns
each holding a fixed *colour-band stack*, and the verb is "click a
column then arrow-shift its band stack up or down by one segment".
lp85 evaluates win by every pawn sitting over its goal cell anywhere
in the grid; qx7p evaluates win by a single horizontal scan-line
through all columns matching a target colour pattern at exactly that
row. There is no permutation table; shifts are linear and modular per
column. Visually lp85 renders a 16×16 chunky grid of clickable
button-buttons; qx7p renders 3-5 tall thin vertical bars over a
near-empty background with a horizontal scan line.

### vs `vc33` (row-slide-pull-tab)
vc33 is a **horizontal-row-slide** puzzle: clicking a pull-tab at the
end of a row drags the entire row of stones one cell horizontally so
each stone slides to a neighbouring slot, and the goal is that each
coloured stone ends up over its same-coloured house slot at the bottom
edge. The verb is "click a tab → translate one row by one cell".
qx7p's bands move VERTICALLY rather than horizontally, and what is
moved is a column of *colour segments* (not pieces atop a row). vc33's
goal is "every stone over its house" (positional matching of pieces to
slots); qx7p's goal is "scan-line row equals target colour pattern"
(pattern matching across a fixed row). vc33 has no scan line, no
indicator beam, no segments-stack-per-column.

### vs `tr87` (tape-rewrite-rule)
tr87 cycles symbol cards on a horizontal tape against rewrite rules.
The verb is "ACTION1/2 cycles a card forward/backward through a
seven-glyph alphabet". qx7p's columns are NOT cycling symbols; they
are scrolling a *colour-band stack* past a fixed indicator. tr87's
puzzle is symbolic (find a rewrite that satisfies grammar rules) while
qx7p's is geometric (align the colour band on the indicator row to a
target). The near-miss is in the verb shape (arrow-keys cycle
something) but the operands and goal are entirely different.

### vs `dc22` (colour-cycle-walk)
dc22 has cycle-trigger pads scattered across a maze; stepping on one
cycles every wedge-block of that colour to its next state. The active
agent is a walking pawn. qx7p has no avatar, no walking, no scattered
trigger pads; the player directly shifts columns by clicking-and-arrowing.
The cycle in dc22 is global per-colour; in qx7p the shifts are local
per-column.

### vs `ls20` (cycler-attribute-match)
ls20 has a walking avatar with three cyclable attributes (shape /
colour / rotation) that get incremented by stepping on matching
cycler tiles, and pellets that need a triple-equality match. qx7p has
no avatar, no per-pellet tri-attribute, and no traversal; columns
shift independently and the win condition is row-pattern match.

### vs `qz73` (radial-cycle-lock — prior game)
qz73 rotates a single radial rotor of coloured tips around a central
pivot and locks individual tips. Its mechanic is **rotational** around
a single shared centre. qx7p is **linear** along independent vertical
axes; there is no central pivot, no radial geometry, and no per-tip
locking. Visually qz73 has pawns radiating outward from a centre;
qx7p has straight vertical bars.

## Distinguishing rules vs near-miss prior-games entries

### vs `kp9z` (grain-accumulate-topple), `vd3g` (mound-marble-routing), `gv47` (seed-grow), `vn8d` (domino-cascade)
These are all *cellular-automaton / cascading* mechanics where state
propagates across cells. qx7p has NO propagation, NO cascades, NO
fluid- or grain-flow; each column shift moves *only* that column (or
its rigid bound partner) by exactly one segment. There is no per-cell
state-update rule; all action effect is contained in the named
column(s). Visually those priors render dense grids; qx7p renders a
small number of tall thin bars.

### vs `tr87` / `lp85` (revisited at prior-games scale)
Already addressed above; relevant here only because lp85 is in the
reference set, and the scoreboard of permutation-style puzzles is what
qx7p might be confused for at family-name level. The concrete
difference is: lp85's permutation tables are global with up to 8-12
buttons each pre-baked; qx7p has no permutation tables at all — every
click+arrow is a deterministic +1 / −1 shift on a single linear stack.

### vs `mr5q` (polarity-attract-discharge), `m0r0` (mirrored-quad)
These are *coupled-motion* mechanics where a single input moves
multiple entities under a sign rule. qx7p's L2 bound-pair mechanic
*is* a coupled-motion concept and I want to call it out specifically:
the difference is that mr5q couples pawn *walking* under polarity, and
m0r0 couples avatar *walking* under quadrant mirrors — both with
WASD-driven motion of avatars across a maze. qx7p's bound-pair couples
*column-segment-shifts* with no avatars at all and the partnered
columns visibly slide in opposite directions in the same animation
tick. The shared dimension is "one input affects two entities", but
the entities (columns vs avatars), the dynamic (segment-shift vs
walking), and the visual signature (vertical bars vs corridor pawns)
are all different.

## Negative-similarity-check (8-dimension comparison)

Walked against the priors most likely to share surface features
(lp85, vc33, tr87, ls20, qz73, mr5q, dc22):

| Dim | Description | Shared with any single prior? |
|---|---|---|
| 1 | What is on the board | Vertical colour-band columns + scan line + target strip. Distinct — no prior has vertical-band columns. |
| 2 | What the player physically does | Click column + arrow-shift up/down. lp85 uses click-only; vc33 click-pulls a row tab; tr87 arrow-cycles a horizontal card. None use "click then up/down arrow" on a vertical band stack. |
| 3 | What the level asks for | Scan-line row equals target pattern. Distinct (no prior matches a horizontal scan-line through aligned bars). |
| 4 | What kills the player | Step counter (universal). Match — but this is universal so doesn't count alone. |
| 5 | Cast of supporting elements | Bound-pair columns, blocker segments, movable scan line. None of these specific elements appear in a single prior. |
| 6 | Visible visual signature | Tall thin vertical bars over near-empty background with one horizontal indicator row. Distinct from every prior screenshot examined (ek73, jd4q, vd3g, lv4k, pf3w, gx7m, bx84, qz73, kp9z, zd7m, xn5p). |
| 7 | Pixel grain of primary sprites | Each column will be ~6 cells wide × ~28 cells tall with internal segment pattern (each segment ~4 cells tall × 6 cells wide); rich enough per checklist item 20. |
| 8 | Core dynamic | "Slide each band stack to bring the right segment into a fixed window, with bound pairs and a movable window adding composition." No prior centres on this dynamic. |

No single prior shares 3+ dimensions. Negative-similarity test passes.

## Open spec questions (resolved in `write_spec`)
- Exact column count per level (3 / 4 / 5).
- Number of segments per column (~10-14).
- Indicator scan-line row position per level.
- Step budget per level.
- Visual identity of bound-pair sigil and blocker-segment sigil.
- Whether ACTION5 is "shift indicator up" only with a wrap-around, or
  toggled with ACTION3/ACTION4.
