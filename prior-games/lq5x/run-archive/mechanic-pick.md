# mechanic-pick — lq5x · lantern-cone-illuminate

## 1. ID

**`lq5x`** — 4 lowercase alphanumeric characters, not a recognisable
English word, not present in the 25 reserved reference IDs
(ar25 bp35 cd82 cn04 dc22 ft09 g50t ka59 lf52 lp85 ls20 m0r0 r11l
re86 s5i5 sb26 sc25 sk48 sp80 su15 tn36 tr87 tu93 vc33 wa30), not
present in `prior-games/index.md` (kf42, qz73, kx14, qb84).

## 2. Mechanic family

**`lantern-cone-illuminate`** — three-word hyphenated tag naming
the active object (lantern), the directional structure (cone), and
the verb (illuminate).

## 3. One-paragraph description

A single small "lantern" pawn lives inside a darkened walled maze
on a 16×16 playfield. The lantern always emits a directional
**rectangular cone** of "lit" cells extending up to **range R** in
its current facing direction; the cone reveals everything in
straight-line-of-sight inside that quadrant and is blocked by maze
walls. The player has two basic verbs: **arrow keys (ACTION1-4)
walk the lantern one cell** in the corresponding cardinal
direction, while **ACTION5 rotates the cone facing 90° clockwise**
through the four cardinal headings. Scattered around the maze are
**target rings** of various colours; a target counts as "lit"
when, at any single tick after the action, it sits inside the
cone's lit area AND the cone's current colour matches the
target's colour. From level 2 onward the cone has a *finite range*
R that starts short and grows by one cell each time the lantern
walks over a **wax pickup** (a small spot sprite consumed on
contact). From level 3 onward the maze contains stationary
**colour filters**: when the cone's lit area passes over a filter
cell, the cone's colour for that tick becomes the filter's
colour, then reverts when the lantern next moves or rotates
through a different filter (or away from any filter). The level
ends in win when every target has been lit-with-matching-colour
at least once; it ends in loss when the per-level step counter
drains. ACTION6 / ACTION7 are NOT in the action set.

## 4. Action set

**`available_actions = [1, 2, 3, 4, 5]`**

| Slot | Verb | Effect |
|---|---|---|
| 1 | UP | Walk lantern one cell up; cone facing unchanged. Movement rejected silently if blocked by wall or playfield bound. |
| 2 | DOWN | Walk lantern one cell down. |
| 3 | LEFT | Walk lantern one cell left. |
| 4 | RIGHT | Walk lantern one cell right. |
| 5 | (rotate cone) | Rotate cone facing 90° clockwise: N → E → S → W → N. Lantern position unchanged. |

Each action consumes one step from the level budget. After every
action the engine recomputes the cone, paints the lit cells onto
the frame, evaluates the "matched-target" predicate, and either
fires `next_level()` (win) or runs out the step counter (loss).

This is **the only action shape `[1,2,3,4,5]` across all 4
priors** — kf42, kx14, qb84 use `[1,2,3,4,6]` or `[1,2,3,4]` and
qz73 uses `[5,6]`. Action signature alone is a clean divergence.

## 5. Per-level progression (mechanics summary)

L1 carries N=2 base mechanics (walk + cone-rotate); L2 carries
N+1=3 (adds wax-pickup-extends-range); L3 carries N+2=4 (adds
filter-changes-cone-colour). Every mechanic listed at a level is
required by that level's witness — no hidden mechanics.

| Level | Mechanics in play | New | Witness sketch |
|---|---|---|---|
| 1 | walk + cone-rotate | (base) | 2 target rings placed in opposite quadrants of the maze; the lantern starts mid-maze with cone facing N. The witness must walk to a vantage cell where one rotation aligns the cone over both targets — i.e. one rotation is required, and so is at least one walk. ~6-9 actions. |
| 2 | walk + cone-rotate + wax-pickup | wax pickup grows R | 3 targets, initial R=2 (cone too short to reach the far targets). 2 wax pickups scattered. Witness must collect at least one pickup before walking to vantage; routing is non-trivial because in the unlit area the player must plan based on inferred maze shape from prior cone observations. ~12-16 actions. |
| 3 | walk + cone-rotate + wax-pickup + filter-cone-colour | colour filter alters cone colour | 4 targets of 2 different colours. 2 colour filters in the maze + 2 wax pickups. Witness must visit the filters in a *specific* order so that when the cone next sweeps each target the cone's colour matches the target's colour. Commuting the order of two adjacent filter visits (or reordering "wax-pickup vs filter-visit") changes the cone-colour history at the next sweep step and breaks at least one target's match. Greedy "go to the nearest target" strategies fail because they ignore the colour-state requirement. ~18-22 actions. |

L2's planning bar: the witness cannot be solved by single-step
greedy or by "spam ACTION5" — wax pickups extend range only
when collected, so the player must reason about which pickup
extends range enough to make which target reachable at the
current cone facing.

L3's strict-deeper bar: the witness has at least one pair of
adjacent actions whose order *matters* — swapping them changes
which colour the cone has when sweeping the next target, breaking
the level. The trivial heuristic L3 defeats: **"after each move,
illuminate whichever target is currently in the cone, in any
order."** This fails because the cone colour at the moment of
sweep may not match the target colour, and re-aligning afterwards
costs steps the budget cannot absorb.

## 6. Similarity sweep

Per `mechanic-novelty/similarity-check.md`. Family tag and
description checked against every taxonomy row + every
prior-games row.

### 6a. Taxonomy near-misses

Family-level matches against `cycler-`, `walk-`, `pawn-`,
`maze-`-prefixed entries trigger description-level checks. The
following rows are flagged as worth examining:

#### `ls20` — cycler-attribute-match

ls20 description: *"a magenta-yellow avatar wanders a wall-bound
maze in five-pixel hops; stepping onto a coloured cycler-tile
rolls its shape, hue, or rotation one notch through a fixed
alphabet; reach the goal pad with the avatar's
shape-colour-rotation triplet matching the imprinted target."*

- **Win condition match**: ls20 wins when the avatar reaches a
  goal cell with matching attributes; lq5x wins when every
  target is *lit-with-matching-colour*. **Different**: ls20 is a
  navigation-with-attribute-tracking puzzle on a SINGLE goal
  cell; lq5x is a *visibility/illumination* puzzle covering
  multiple targets simultaneously (or sequentially over the
  run). The avatar in ls20 carries the colour state on its body;
  the lantern in lq5x carries no body colour — colour state
  lives on the *cone*, which is an emitted projection.
- **Primary action match**: ls20 is pure-arrow `[1,2,3,4]`;
  lq5x is `[1,2,3,4,5]` adding cone-rotate. **Different
  action shape**.
- **Primary constraint match**: ls20 cycles attributes by
  *stepping on tiles*; lq5x cycles cone facing by *pressing
  ACTION5* (an explicit dedicated verb), and cone colour changes
  not by stepping but by the cone *passing over* a stationary
  filter. **Different**: in ls20 the avatar's state changes when
  it moves over a tile; in lq5x the cone's state changes when
  the *cone* (a non-avatar projection extending up to range R)
  intersects a filter cell. The lantern itself never changes
  state from stepping on filters.

**Distinguishing rule (cited in spec §9)**: lq5x's puzzle is a
*line-of-sight cone-aiming* puzzle whose colour state lives on
the projected cone (not on the avatar) and whose
verb-cardinality is +1 (an explicit ACTION5 rotation). ls20 is a
*navigation-with-on-body-attribute-cycling* puzzle whose
colour/shape/rotation state lives on the avatar and is exclusively
mutated by stepping on cyclers.

#### `bp35` / `lf52` — procedural-graph-walk(-undo)

Both: token sits on a procedurally-built coloured-node graph;
arrows walk along tracks; click teleports to neighbour;
target = procedural configuration.

- **Description-level**: bp35/lf52 are *graph-as-explicit-edge-
  set* puzzles where the player navigates structural
  constraints. lq5x is a *grid-with-line-of-sight* puzzle where
  visibility through walls is the puzzle. The "graph" in lq5x
  is the maze topology only as it gates LOS; there is no
  abstract edge-and-node graph.
- **Different on board, action set, dynamic**.

**Distinguishing rule**: lq5x has no explicit graph data
structure; the maze is a *grid* and the puzzle is what the cone
*can see* from a given (position, facing) pair. bp35/lf52's
puzzle is what graph configuration matches the level seed.

#### `tu93` — maze-pickup-train

tu93 description: *"a 3-cell-tall pawn hops three pixels at a time
along value-2 corridors carved into a maze-shaped tile; coloured
arrows it walks past either fall in step behind it like ducklings
... lead the whole train onto the goal-marker tile."*

- **Win condition match**: tu93 wants pawn-and-followers on a goal
  tile. lq5x wants every target lit with matching colour.
  **Different**.
- **Primary action**: tu93 is `[1,2,3,4]`. lq5x is
  `[1,2,3,4,5]`. Different.
- **Primary constraint**: tu93's followers chain behind the
  pawn (a Snake-like dynamic). lq5x has no followers; the cone
  is a *non-physical projection*, not a chain of pawns.

**Distinguishing rule**: lq5x has no follower/chain dynamic; its
puzzle is *projection visibility*, not *chain-of-position*
management.

#### `m0r0` — mirror-orb-merge

m0r0: two mirror-symmetric pawns; arrows move both with mirrored
input; merge them into one cell.

- **Different on every dimension**: m0r0 has 2 pawns with
  mirrored input (LEFT moves one pawn left and pulls the other
  right); lq5x has 1 pawn with normal input. m0r0 has no LOS;
  lq5x has no mirror-input dynamic.

#### `ka59` — sokoban-explode-chase

Sokoban-style pushing. lq5x has no pushing.

#### `r11l` — centroid-puppet-leg

A ring at the centroid of legs. lq5x has no centroid logic.

### 6b. Prior-games sweep

| prior id | family | shared dimensions vs lq5x | distinguishing rule |
|---|---|---|---|
| kf42 | tether-pawn-cycle | step-counter-only failure axis (shared); arrow-key input (shared); two-pawn arena (NOT shared — lq5x is one pawn). 2 shared dimensions. | kf42 is a tether-pair-position puzzle (Chebyshev distance constraint between two pawns); lq5x is a single-pawn line-of-sight cone puzzle with no pair dynamic. Different verb cardinality (kf42 needs ACTION6; lq5x doesn't). |
| qz73 | radial-cycle-lock | step-counter-only failure axis (shared); ACTION5 is the rotation verb (shared as a slot, but the rotation operates on different objects). 2 shared dimensions. | qz73 rotates an 8-slot ring of tip-pieces and the player ACTION6-clicks to lock individual tips; the puzzle is which tips to lock so the rotation aligns the rest. lq5x rotates the *facing of a cone of light emitted by the lantern*, not a ring of objects, and there is no lock verb at all. |
| kx14 | tide-tilt-buoyant | step-counter-only failure axis (shared); arrow-key input (shared). 2 shared dimensions. | kx14 is a vertical fluid-tank puzzle whose ACTION1/2 raise/lower a water surface and ACTION3/4 tilt floating balls; lq5x has no fluid, no tank, no surface, no tilt — the verbs walk a pawn and rotate a cone facing. |
| qb84 | bead-lift-swap | step-counter-only failure axis (shared); arrow-key input (shared); ACTION1/2 carries a directional verb on the same slot as the navigation verb (shared as a *pattern* but the verb's referent differs). 2-3 shared dimensions. | qb84 is a chain-cursor puzzle where ACTION1/2 *swap* the cursor's bead colour with an above/below peg, and ACTION3/4 step the cursor index along the chain; lq5x's ACTION1/2 are walking, not swapping, and there is no chain-cursor abstraction at all. The colour state in qb84 lives on chain beads; in lq5x it lives on the cone projection. |

No prior shares ≥3 dimensions with lq5x. The single biggest
exposure is the universal "step-counter-only failure axis +
arrow-key input" combination, which appears in 3 of 4 priors and
is a near-universal trait of the 25 reference games as well —
not a real similarity signal.

## 7. Negative-similarity check (§negative-similarity-check.md)

Walking the eight dimensions for the candidate L1 mental render
against each prior's `level_1.png`:

### vs kf42 level_1
1. What's on the board: kf42 = 2 single-cell pawns in a walled black grid. lq5x = a small lantern + maze walls + 2 target rings + (dark) unilluminated regions. **Different texture** (lq5x has the maze and the cone overlay; kf42 has just two coloured cells).
2. Player physically does: kf42 click-then-arrow. lq5x arrow-then-rotate. Different.
3. Level asks: kf42 = both pawns on matching pads. lq5x = both target rings inside the cone. Different.
4. What kills: step counter (shared, universal).
5. Cast: kf42 = 2 pawns + 2 pads + walls. lq5x = 1 lantern + 2 target rings + walls + a *cone-overlay region*. **Different**.
6. Visual signature: kf42 is *flat black with red+blue dots*; lq5x is *dark maze with a yellow lantern and a partial-bright "lit" overlay*. **Different**.
7. Pixel grain: kf42's pawns are 2-cell-wide red/blue rectangles; lq5x's lantern is a 1-cell yellow sprite, walls are textured, lit overlay is a soft-tone wash. **Different**.
8. Core dynamic: kf42 = "drag the second pawn around without losing the colour I just set". lq5x = "where do I aim the cone so it sees both targets?". **Different**.

Shared: 1 (the universal failure axis). Distinct on 7/8 dimensions. **Pass**.

### vs qz73 level_1
1. What's on the board: qz73 = ring of 8 slots with tips/sockets at radial positions on grey background. lq5x = walled maze with lantern. **Different**.
2. Player does: qz73 ACTION5 rotate ring + click lock. lq5x walk + ACTION5 rotate cone. **Different referents**.
3. Level asks: qz73 = each socket has matching tip. lq5x = every target lit with matching colour. **Different**.
4. What kills: step counter (shared).
5. Cast: qz73 = ring + tips + sockets + hub. lq5x = lantern + maze + targets + cone overlay. **Different**.
6. Visual signature: qz73 = *grey background with isolated coloured swatches at radial slots, hollow rings*; lq5x = *dark maze with bright cone overlay*. **Different**.
7. Pixel grain: qz73 = small filled squares + hollow rings on grey. lq5x = lantern (filled) + maze (textured) + cone (translucent wash). **Different**.
8. Core dynamic: qz73 = "which tips to lock so rotation aligns?". lq5x = "where do I aim the cone?". **Different**.

Shared: 1. **Pass**.

### vs kx14 level_1
1. What's on the board: kx14 = vertical-tank cross-section with water + balls. lq5x = walled maze + lantern. **Different**.
2. Player does: kx14 ACTION1/2 raise/lower water + tilt + click anchor. lq5x walk + ACTION5 rotate cone. **Different**.
3. Level asks: kx14 = each ball on matching ring. lq5x = each target lit with matching colour. **Different**.
4. What kills: step counter (shared).
5. Cast: kx14 = water + balls + rings + platforms. lq5x = lantern + walls + targets + cone overlay. **Different**.
6. Visual signature: kx14 = *split-tank (light-grey + light-blue) with orange highlights*; lq5x = *dark maze with bright cone overlay*. **Different**.
7. Pixel grain: kx14 has large continuous fluid regions; lq5x has discrete walls + cone-cells. **Different**.
8. Core dynamic: kx14 = "route this ball up through this platform-blocked column?". lq5x = "where do I aim the cone?". **Different**.

Shared: 1. **Pass**.

### vs qb84 level_1
1. What's on the board: qb84 = serpentine chain of bead sprites + flanking peg sprites on dark grey. lq5x = walled maze with lantern. **Different**.
2. Player does: qb84 cursor-step + lift/drop swap. lq5x walk + cone-rotate. **Different**.
3. Level asks: qb84 = chain matches target sequence. lq5x = each target lit with matching colour. **Different**.
4. What kills: step counter (shared).
5. Cast: qb84 = chain beads + pegs + cursor markers + target swatch. lq5x = lantern + walls + targets + cone. **Different**.
6. Visual signature: qb84 = *dark grey background with vivid coloured dots connected by light-grey paths and pink/yellow + glyphs*; lq5x = *dark maze with cone overlay*. **Different**.
7. Pixel grain: qb84 has small filled dots + path segments + glyphs. lq5x has lantern + walls + cone overlay. **Different**.
8. Core dynamic: qb84 = "which peg do I have to swap-and-restore?". lq5x = "where do I aim the cone?". **Different**.

Shared: 1. **Pass**.

### vs ls20 level_1 (closest taxonomy near-miss)
1. What's on the board: ls20 = walled maze with avatar + cycler-tile interactors + goal pad + step bar at bottom. lq5x = walled maze with lantern + target rings + step bar + cone overlay. **Shared** ("walled maze with pawn"). 
2. Player does: ls20 = arrow-step (sometimes onto cyclers). lq5x = arrow-step + ACTION5-rotate. **Different verb cardinality**.
3. Level asks: ls20 = reach goal cell with matching attributes. lq5x = every target inside cone. **Different**.
4. What kills: step counter (shared).
5. Cast: ls20 = avatar + walls + cyclers + plates + goal pad. lq5x = lantern + walls + targets + cone overlay (no cycler-tiles, no goal pad). **Different**.
6. Visual signature: ls20 = *dark grey maze with dimly-lit grey corridors + small textured tiles + occasional bright sprites*. lq5x = *dark maze with a moving bright cone overlay*. **Adjacent but different** — ls20 doesn't have a moving lit overlay; the visual rhythm is "walk the small avatar through the grey maze" vs lq5x's "watch the cone sweep over the maze".
7. Pixel grain: ls20 avatar 2x2; lq5x lantern 1x1 plus cone wash. Both small. **Adjacent**.
8. Core dynamic: ls20 = "what attributes do I bring to the goal cell?". lq5x = "where do I aim the cone?". **Different**.

Shared: 1 (failure axis), 1 (maze + small pawn — partial). **2-2.5 dimensions**. Below the threshold of 3. **Pass**.

## 8. Verdict

Novel candidate. Proceed to `write_spec`.

## 9. Open design questions for `write_spec`

- Exact cone shape (full quadrant vs narrow rectangle): default
  to a **rectangular wedge** of width 3 cells, depth R cells,
  emitted from the lantern position in the facing direction.
- Lantern colour vs cone colour: default to the lantern itself
  rendered yellow (palette 11), the cone rendered as
  off-white (palette 1) on dark cells.
- Wax pickup visual: small filled square (palette 12 orange) of
  size 1x1.
- Filter visual: a 1-cell square in palette matching its filter
  colour (e.g. blue 9, green 14).
- Target ring visual: hollow 3x3 ring in palette matching its
  target colour.
- Maze wall visual: textured palette-3 grey walls.
- Background visual: palette-5 black.
- Step-counter HUD: bottom row depleting bar (one of the
  dominant patterns from the cross-cut analysis).

These are spec-level concerns, not blockers for the family
choice. Captured here so `write_spec` can reuse them.
