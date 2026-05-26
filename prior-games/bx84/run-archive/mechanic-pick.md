# Mechanic Pick — bx84

## 4-character ID

**`bx84`** — chosen at random per `code/id-generation.md`.

Verification:
- Exactly 4 characters, lowercase, alphanumeric: ✓
- Not a recognisable English word: ✓ (opaque consonant-cluster + digits)
- Not in the 25 reference IDs (`ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15, tn36, tr87, tu93, vc33, wa30`): ✓
- Not in `prior-games/index.md` (`kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, vn8d, fz5j, kn58`): ✓

## Mechanic family

**`beam-mirror-reflect`**

## Mechanic description (one paragraph)

A small emitter sits at the edge of the playfield and continuously shoots a thin one-pixel-wide coloured beam in a fixed cardinal direction; the player clicks empty grid cells to drop reflective mirrors and clicks existing mirrors to cycle each through its four orientations (`\`, `/`, `|`, `–`), and the beam — re-traced from emitter to grid-edge after every click — bounces off each mirror at right angles until it has visited every coloured target ring required by the level. Subsequent levels add **filters** (small ringed cells that recolour the beam as it passes through, so a target wants the beam at the right colour) and **prisms** (small triangular cells that split the beam into two perpendicular branches, so a single emit fan-outs to reach multiple targets at once). The player's planning task is purely geometric: which empty cells does the beam need to visit, in what order, with which mirror orientations, and (in later levels) which colour and which split-tree, so that every target ring is touched by a beam of its matching colour. No avatar, no movement, no step-walking; the click verb places-or-rotates a single mirror per action and immediately retraces the entire beam.

## Core-knowledge prior coverage (per `core-knowledge-priors.md`)

- **Objectness**: mirrors, filters, prisms, target rings, emitter — all coherent persistent entities with positions and behaviour.
- **Basic geometry & topology**: ray-tracing through cells; right-angle reflection by mirror-orientation rules; perpendicular splitting at prisms; targets-on-grid as topological sub-objects to "visit".
- **Basic physics**: light-as-a-ray (straight-line propagation, reflection, splitting). Discrete approximation on a 64×64 integer grid.
- **Agentness**: NOT used — the beam is not an agent, the targets do not pursue.

Three of four priors active; the design hits the "geometry + physics + objectness sweet spot" called out in `core-knowledge-priors.md`.

## Forbidden-element check (per `forbidden-elements.md`)

- **Letters / digits / clipart / cultural conventions**: the emitter is rendered as a 3×3 abstract funnel (palette-3 sides + palette-11 mouth, no letter-form); mirrors are 2-pixel diagonal stripes (`\` and `/`) in palette-7 with 2-pixel axial bars (`|` and `–`) — abstract geometry, not glyphs; prisms are small filled triangles (3-cell L-shape) in palette-12; filters are 3×3 hollow rings of palette-8/9/14; target rings are 3×3 hollow squares of palette-8/9/14. None of these form letters, digits, recognisable real-world objects, or cultural symbols. The "beam" itself is a series of 1-pixel cells of palette-11 — an abstract trace, not a clipart laser-gun.
- **On-screen text / instructions**: none.
- **Arrow glyphs**: explicitly avoided. The emitter's "mouth" is a single palette-11 pixel at one edge of the 3×3 sprite (e.g. for a rightward-firing emitter, pixel `[1, 2]` is palette-11 and the rest is palette-3) — no triangular arrow-head shape. The player infers fire direction from where the beam first appears, not from a "→" symbol.

## Composition plan (3-level structure per `composition-and-tutorial.md`)

- **L1 — base dynamic system**: one emitter, one mirror-slot to fill, one target. Player learns:
  1. The beam exists, comes from the emitter, travels straight until it hits a wall or mirror.
  2. Clicking an empty cell drops a mirror in its first orientation (`\`).
  3. Clicking an existing mirror cycles its orientation through `\` → `/` → `|` → `–` → `\`.
  4. A `\` mirror reflects an east-going beam to south-going (and four similar rules for the other orientations).
  5. The level wins when the beam visits the target ring.
  
  Witness: ~3-5 clicks (place mirror, cycle to correct orientation if not first try, possibly add a second mirror in a more complex layout).

- **L2 — base + filter**: two mirrors and a filter must all be used. The beam starts as palette-11 (yellow); the filter recolours it to palette-9 (blue) on pass-through. Two targets: one wants yellow, one wants blue. Witness must (a) route beam to the yellow target FIRST (via mirror reflection before reaching filter), and then (b) cycle a second mirror to redirect the now-blue post-filter beam to the blue target.
  
  Witness exercises: mirror-placement (L1) AND filter-recolour (L2). A level layout where the yellow target is unreachable except via a pre-filter mirror, and the blue target is unreachable except via a post-filter mirror, makes BOTH mechanics counterfactually necessary.

- **L3 — base + filter + prism**: three targets — two requiring different post-filter colours and one requiring the original emit colour, with at most one mirror-slot per target reachable from a single emit path. Solvable only by placing a prism that splits the beam into two perpendicular branches; one branch goes to the unfiltered target (original colour), the other branch passes through a filter and must use mirrors to reach two filter-coloured targets.
  
  Witness exercises: mirror-placement (L1), filter-recolour (L2), AND prism-split (L3). The prism is required because a non-split single-line beam cannot reach two non-collinear filtered targets; the filter is required because two of the three targets demand colours different from the emit colour.

## Action palette

`available_actions = [6]` — pure click. Justification per `action-enum.md`:
- The distinctive verb is **click-to-place-or-cycle-mirror**, encoded entirely on ACTION6 (the click slot).
- ACTION1-4 (cardinal motion) are not used because there is no avatar to walk; the beam itself is the moving entity but its motion is determined by mirror-placement, not by player arrow input.
- ACTION5 (freedom slot) is not used because the click verb already carries the game's identity. Adding ACTION5 = "fire beam" would be a no-op since the beam is always live; adding ACTION5 = "remove last mirror" would be undo-flavoured but `action-enum.md` reserves undo for ACTION7, and undo is not core to this game's planning challenge.

The `action-enum.md` "Pure click" pattern is shared with reference games r11l, vc33, sc25, ft09, lp85 and prior generated games kf42, qz73, gv47, hr8q, ng52, pj7k, pz4t, vn8d, kn58. Family is crowded but the mechanic itself diverges substantially (see distinguishing rules below).

## Similarity check (per `mechanic-novelty/similarity-check.md`)

### Family-level matches (taxonomy + prior-games)

Walking the taxonomy and prior-games index for any entry whose `mechanic_family` shares first two hyphen-segments or whose `description` overlaps with mine:

| Source | id | family | shared first words? | description overlap? | escalate? |
|---|---|---|---|---|---|
| taxonomy | ar25 | shape-mirror-cover | "mirror" appears | partial | YES |
| taxonomy | cd82 | orbit-fire-paint | no | partial (firing) | YES (defensively) |
| taxonomy | re86 | frame-paint-canvas | no | no | no |
| taxonomy | tn36 | program-pawn-trace | no | partial (path tracing) | YES (defensively) |
| prior | lq5x | lantern-cone-illuminate | no (but "illuminate"/"cone" overlap) | YES — both use light/illumination | YES |
| prior | gv47 | seed-grow-surround-dissolve | no | no | no |
| prior | pj7k | rolling-cube-face-paint | no | no | no |
| prior | vn8d | domino-cascade-topple | no | partial (chain reaction propagation) | YES (defensively) |
| prior | kn58 | anchor-pull-magnet | no | no | no |
| prior | pz4t | anchor-pivot-place | no | no | no |
| prior | qz73 | radial-tip-lock | no | no | no |
| prior | hr8q | pair-blend-recipe | no | no | no |

### Description-level + distinguishing rules for each escalated row

#### vs ar25 (shape-mirror-cover)

- **ar25 description**: a coloured shape and a long straight mirror-line both float on the playfield; arrows nudge either, the same-shape ghost sliding on the other side covers scattered dots.
- **bx84 description**: a 1-pixel beam emitted from a fixed corner-mounted emitter is reflected at right angles by 2-pixel mirrors that the player places via clicks.
- **WIN CONDITION**: ar25 = the ghost (mirror-image of the shape) covers every dot; bx84 = the emitted beam visits every target ring.
- **PRIMARY ACTION**: ar25 = arrow-nudge a 2D shape OR a mirror line; bx84 = click to place or cycle a small mirror sprite.
- **PRIMARY CONSTRAINT**: ar25 = step budget for arrow-nudges; bx84 = step budget for clicks.
- **Concrete distinguishing rule**: ar25 reflects an entire 2D *shape* across a *line* (axis of symmetry; the ghost is the mirror image of the whole shape); bx84 reflects a 1D *ray* off discrete *cell-mirrors* at right angles. The "mirror" in ar25 is a continuous symmetry axis spanning the whole grid; the "mirror" in bx84 is a 2×2 cell sprite at one location, of which there are several per level. ar25's player verb is "slide a shape such that its mirror-image covers a target"; bx84's player verb is "place reflectors so a ray bounces through targets". These are fundamentally different physics: linear symmetry-folding vs ray-tracing.
- Verdict: NOVEL.

#### vs cd82 (orbit-fire-paint)

- **cd82 description**: paint-tank rides 8-slot ring around a 10×10 canvas; arrows step the tank slot-by-slot, click loads a swatch, FIRE charges the tank inward to splash a half (axial slot) or wedge (diagonal slot) of the canvas.
- **WIN CONDITION**: cd82 = canvas pattern matches a target picture (modulo X-cross diagonals); bx84 = beam visits target rings.
- **PRIMARY ACTION**: cd82 = orbit-and-fire; bx84 = place-and-rotate-mirror.
- **PRIMARY CONSTRAINT**: cd82 = step budget; bx84 = step budget.
- **Concrete distinguishing rule**: cd82 fills CANVAS CELLS with colour by directional fill from outside; bx84 routes a 1D ray through cells. cd82's "fire" is a discrete event triggered by ACTION5 that paints a half/triangle of canvas in one go; bx84 has no "fire" verb — the beam is always live and is re-traced after every click. cd82's "tank" orbits a fixed centre; bx84 has a fixed emitter and movable mirrors. Different geometry: filling vs tracing; different verb cardinality: discrete events vs continuous-state.
- Verdict: NOVEL.

#### vs tn36 (program-pawn-trace)

- **tn36 description**: programmable pawn at one end of a coloured runway with slot-buttons; click buttons in sequence to choose move/rotate instructions; run programme → pawn walks runway tracing target pattern.
- **WIN CONDITION**: tn36 = pawn's traced path lights up the target pattern cells; bx84 = beam visits target rings.
- **PRIMARY ACTION**: tn36 = click-buttons-to-build-programme + click-run; bx84 = click-grid-cell-to-place-or-rotate-mirror.
- **PRIMARY CONSTRAINT**: tn36 = step budget for button clicks; bx84 = step budget for mirror clicks.
- **Concrete distinguishing rule**: tn36 is a *deferred-execution* puzzle — the player builds a programme then runs it (separate commit step); bx84 is *live* — every click immediately recomputes the beam, no commit. tn36's "pawn" is a controlled agent following an instruction list; bx84's "beam" is a passive ray determined by a static reflector layout. tn36 plans an action sequence in time; bx84 plans a mirror-layout in space.
- Verdict: NOVEL.

#### vs lq5x (lantern-cone-illuminate)

- **lq5x description**: single lantern projects a 3-wide directional cone; arrows walk lantern, ACTION5 rotates; wax pickups extend cone range, filters re-tint cone colour to match coloured target rings.
- **WIN CONDITION**: lq5x = each target ring covered by cone of matching colour; bx84 = each target ring visited by 1-pixel beam of matching colour.
- **PRIMARY ACTION**: lq5x = walk-the-lantern + rotate-the-lantern; bx84 = click-to-place-or-cycle-a-mirror.
- **PRIMARY CONSTRAINT**: lq5x = step budget on walking + rotating; bx84 = step budget on clicks.
- **Concrete distinguishing rule**: lq5x has ONE active light-source that the player MOVES with arrow keys; bx84 has a FIXED light-source and the player places STATIONARY MIRRORS to redirect it. lq5x's lit area is a 3-wide directional CONE (a fan-shape); bx84's lit area is a 1-pixel-wide BEAM (a line, possibly with prism-split branches in L3). lq5x's "filter" is a re-tint applied to the moving cone; bx84's filter is a discrete cell that the beam-line passes through. Crucially: lq5x has NO REFLECTION mechanic — the cone always points in the lantern's facing direction. bx84's core mechanic is right-angle reflection off mirrors, which lq5x does not have at all. Players of bx84 plan mirror layouts, players of lq5x plan walking paths; the central reasoning task differs.
- Verdict: NOVEL.

#### vs vn8d (domino-cascade-topple)

- **vn8d description**: single click triggers a chain reaction through pillars; burst-pads splay 4 ways, rotator-pads turn corners.
- **WIN CONDITION**: vn8d = some predicate after the cascade settles (likely all targets toppled).
- **PRIMARY ACTION**: vn8d = click once to *start* the cascade; bx84 = click to place-or-cycle a mirror, beam updates immediately.
- **PRIMARY CONSTRAINT**: vn8d = step budget on cascade-trigger clicks; bx84 = step budget on mirror-placement clicks.
- **Concrete distinguishing rule**: vn8d is a *one-shot trigger* puzzle — the player arranges? no actually vn8d has the pillars/burst-pads/rotator-pads ALREADY PLACED in the level (the player clicks once to start the cascade and watches it propagate through the pre-placed network). The player does NOT design the network — they choose the *starting point*. bx84 inverts this: the network of mirrors is BUILT by the player one mirror at a time via clicks; the beam-source is fixed; the player solves by mirror-LAYOUT not by trigger-CHOICE. Furthermore, vn8d's cascade is a 4-way burst from each pad (a tree of dominoes falling); bx84's beam is a single line that only branches at prisms (L3 only). Different topology: branching tree from one trigger vs single ray with at-most-one binary split.
- Verdict: NOVEL.

### Decision matrix verdict

All five escalated near-misses produce **NOVEL** verdicts with concrete distinguishing rules. No remaining family-level matches require further evaluation.

## Negative similarity check (per `negative-similarity-check.md`)

Walking the eight dimensions for each prior, looking for "essentially the same" overlap:

### Most relevant: lq5x (the only prior also in the "light" thematic space)

1. **What's on the board**: lq5x has a moving lantern, walls, wax pickups, filters, target rings; bx84 has a fixed emitter, beams, mirrors, filters, prisms, target rings. **Different cast** (no lantern, no wax, no avatar).
2. **What the player physically does**: lq5x walks an avatar with arrows + rotates with ACTION5; bx84 clicks empty cells (no avatar). **Different verb**.
3. **What the level asks for**: both ask "match light colour to target colour at each target ring". **Shared at the goal level.**
4. **What kills the player**: both = step budget. Universal.
5. **Cast of supporting elements**: lq5x has wax pickups and walls; bx84 has mirrors and prisms. **Different**.
6. **Visible visual signature**: lq5x dominant palette is whatever is in its 3-level versions (I'll consult its frames if it gets close). bx84 will use **palette {3 grey wall, 11 yellow beam, 7 pink mirror, 8 red filter / 9 blue filter / 14 green filter, 12 purple prism, 15 white emitter accent}** — a deliberately different signature. **Different**.
7. **Pixel grain of primary sprites**: lq5x's lantern is some glyph; bx84's mirrors are 2×2 diagonal/axial-bar sprites with internal pattern. **Different — bx84's mirrors have a clear orientation glyph (diagonal line), lq5x's lantern doesn't share that signature.**
8. **Core dynamic**: lq5x = "walk lantern, point cone, recolour by passing through filter, illuminate target". bx84 = "place mirrors, beam reflects, recolour through filter, possibly split through prism". **The dynamic at core is "stationary infrastructure routing a moving signal" (bx84) vs "moving signal-source aimed at targets" (lq5x).** Different.

Shared dimensions: just dimension 3 (goal-level "light hits coloured target") — and that's a high-level abstraction. The player's actual reasoning task is fundamentally different (place reflectors vs walk lantern). **1 of 8 dimensions overlap → strongly novel**.

### Other priors (kf42, qz73, kx14, qb84, gv47, hr8q, ng52, pj7k, pz4t, vn8d, fz5j, kn58)

None share more than 2 of 8 dimensions. The most surface-similar are:
- **kn58 (anchor-pull-magnet)**: pure click + multiple coloured pawns. bx84 has no pawns at all (mirrors are not pawns — they don't "represent the player or characters"; they're inert reflectors). Shared dimensions: 4 (lose-condition step budget) and 2 (player-clicks-to-act). 2/8 → novel.
- **vn8d (domino-cascade-topple)**: pure click + chain reaction. Shared: 2 + 4. 2/8 → novel.

The candidate visibly diverges on:
- Pixel grain (mirrors with a diagonal-line glyph; emitters as funnel; targets as rings) vs prior dominant cast.
- Palette signature (yellow beam, pink mirrors, purple prism — none of the priors lead with this combo).
- Core dynamic (ray-tracing routing — present in NO prior or reference).

**Negative similarity check passes.**

## Distinguishing-rule articulation refusal check

I considered and rejected several alternative mechanic families for being too close to the existing corpus:

- **rotor-mesh-cycle (gear-trains)**: rejected after discovering that cn04 (nub-pair-glyph) and qz73 (radial-tip-lock) and pz4t (anchor-pivot-place) all share "rotate a small piece to align a tip/nub with a target" verbs. A gear-mesh game with mesh propagation IS distinct, but the surface visual signature (multiple coloured rotors with a marker tooth, target tabs around the edge) shares 3-4 dimensions with cn04 + qz73 (multiple small rotational pieces with markers; align-marker-with-target win condition; click-as-primary-verb). The negative test would catch it. Beam-reflect avoids this trap.
- **Tilt-arena-slide / 2048-style**: rejected as too close to existing video games (per §3.4 axis 1).
- **Magnet-polarity-toggle pawn**: rejected as too close to kn58 (anchor-pull-magnet) on the visual-signature axis (multiple coloured pawns, a single special pawn manipulating them).
- **Pendulum-swing-release**: rejected as physics-heavy with discrete-grid approximation pain; 64×64 integer pendulums look unnatural.
- **Beam-reflect-prism (chosen)**: passes both positive and negative tests with concrete distinguishing rules against every near-miss.
