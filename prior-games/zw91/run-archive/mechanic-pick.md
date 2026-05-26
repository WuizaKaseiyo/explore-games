# mechanic-pick.md

## Game ID
`zw91`

Verified opaque: not in the 25 reference IDs and not in `prior-games/index.md` (33 prior entries scanned). 4-character lowercase alphanumeric, not an English word.

## Mechanic family
`inflate-fit-burst`

## One-paragraph description
The player controls a single square avatar whose **footprint size** is itself a verb. Arrows step the avatar one tile in cardinal directions; **ACTION5** cycles the avatar through three sizes (small / medium / large), expanding or contracting its rendered footprint and the cells it occupies. Bigger footprints cannot fit through narrow corridors but can push **shove-blocks** out of the way (radial slide); smaller footprints can squeeze through gaps but cannot push or fit larger sockets. The win condition for a level is that the avatar is centered on every same-shape **socket** (a hollow ring whose inner area matches one of the three sizes) at the matching size; sockets of unmatched size remain unsatisfied. At L3 a fourth mechanic enters: when ACTION5 is pressed while the avatar is already at maximum size, the avatar enters a visible **overloaded** state (halo around its footprint); the next ACTION5 fires a single-use **burst** that destroys all shove-blocks within the avatar's current footprint AND breaks one segment of an adjacent breakaway-wall, after which the avatar resets to small. Mechanics in play across levels: L1 = `move` + `size-cycle` (2). L2 = `move` + `size-cycle` + `inflate-push` (3). L3 = `move` + `size-cycle` + `inflate-push` + `overload-burst` (4). The avatar's own footprint size is the load-bearing variable: it gates what fits, what pushes, and when burst is available.

Core knowledge priors used: **objectness** (avatar, blocks, sockets, walls as persistent entities), **basic geometry / topology** (size matching at sockets, adjacency for push, inside/outside for socket fit), **basic physics** (push-block radial slide; burst-breakaway destruction). No agentness — there are no autonomous NPCs.

## Closest taxonomy entries (positive similarity check)

### s5i5 — `rod-stretch-retract` (reference)
**Description**: "Coloured rectangular rods stand on the canvas like telescoping arms with a tiny dot at each tip; clicking one half of a coloured pair-of-windows control stretches or retracts the rod of that colour one notch along its axis (rods stacked on top slide along), until every dot ends up on its matching cross-shaped target."

**Similarity**: both involve "an entity changing length/size as the load-bearing verb."

**Distinguishing rule**: in s5i5, the player operates remote click-control swatches to stretch *stationary* rods whose tips must reach targets — the player is *not* on the playfield; the rods do not move position, only length, and along a single axis. In `zw91`, **the player IS the avatar**: a single mobile pawn whose footprint cycles through 3 *radial* sizes via a modal verb (ACTION5), and the avatar both *moves* (arrows) and *resizes* (ACTION5). The win condition is the avatar's *body* fitting a socket at matching size, not a tip reaching a target. s5i5 is "manipulate distant fixtures via a remote control panel"; `zw91` is "be the avatar — change your own size to traverse and fit." Different agency, different verb axis (radial vs axial), different goal (body-in-socket vs tip-on-target).

### nb6t — `hinge-chain-reach` (prior)
**Description**: "Three rod-segments at independent hinges; rotate / extend / cycle active; carry-and-drop at L3 to deliver an item to a drop-zone."

**Similarity**: both involve "an articulating extending entity."

**Distinguishing rule**: nb6t has *multiple jointed rod-segments* with independent hinges that the player articulates by selecting and rotating each segment; the segments form a reaching arm. `zw91` has a *single self-contained avatar* whose entire footprint resizes radially in place — no hinges, no segments, no kinematic chain. nb6t plays as "operate an articulated arm"; `zw91` plays as "be a self-resizing pawn." Different cardinality (multi-segment chain vs single body), different motion model (kinematic articulation vs radial cycling), different verb scope (per-segment selection vs whole-avatar modal).

### gv47 — `seed-grow-surround-dissolve` (prior)
**Description**: "Click coloured seeds to grow regions; surround a same-coloured pip (ringed in black) with paint and the ring auto-dissolves; ACTION5 globally mixes contacting region pairs into a derived colour."

**Similarity**: both involve "size growing on a verb trigger."

**Distinguishing rule**: in gv47 the *region of paint on the canvas* is what grows under click — seeds expand outward into adjacent cells; the player is not embodied. The verb is "grow this region." In `zw91`, *the player's own avatar* changes radial size; growing is a body-property of a single entity, not a paint-spreading operation on the field. There is no painting and no region merging; sockets are explicit targets the avatar must body-fit. Different subject (canvas region vs player-pawn), different effect (paint-spread vs avatar-resize), different goal (image-completion vs body-in-socket).

### ka59 — `sokoban-explode-chase` (reference)
**Similarity**: both can destroy nearby blocks (ka59's explode-tiles vs `zw91`'s overload-burst at L3).

**Distinguishing rule**: ka59's explode-tiles are *environmental fixtures* the player walks onto; the explosion is triggered by the *level layout*, not by the player. ka59 also has chasers (autonomous AI). `zw91` has *no environmental triggers and no AI*: the burst is an *on-demand resource* the player loads by reaching max-size and fires by pressing ACTION5 once more — agency entirely on the player, single-shot per level, conditional on the size mechanic. ka59's destruction is a *consequence of position*; `zw91`'s burst is a *consequence of state-loading via the size verb*.

### ft09 — `stamp-3x3-paint` (reference)
**Similarity**: both involve a footprint that touches multiple cells.

**Distinguishing rule**: ft09's "footprint" is a 3×3 paint stamp triggered by a click at any cell; the canvas accumulates stamps to match a target image. The player is a click-cursor, not a body. In `zw91`, the avatar's footprint is *the avatar itself* (a body that occupies cells, blocks paths, fits sockets), not a paint-application area; there is no canvas, no painting, no per-stamp accumulation. ft09 is "compose an image by stamping;" `zw91` is "navigate a body whose own size is variable."

## Closest prior-games entries (positive similarity check)
Already addressed: `nb6t` (hinge-chain-reach) and `gv47` (seed-grow-surround-dissolve) above.

Two further glances:
- **pz4t anchor-pivot-place** (jigsaw): tile-placement of static pieces, no avatar resizing. Different.
- **kp9z grain-accumulate-topple**: cells overflow to cardinal neighbours when capacity hit. No avatar; different mechanic family. Different.

No prior-games entry shares the avatar-self-resize core dynamic.

## Negative similarity check (8 dimensions, against every prior)
Walking the 8 dimensions for the candidate's L1 mental rendering:

1. **What is on the board.** Single mobile avatar (square with internal cross), bordered chamber walls (brick texture), one socket-ring matching the avatar's largest size, no other elements at L1. Not the multi-pawn-on-grid pattern of kf42/vh68 caution; not a canvas or runway or rod-set.
2. **What the player physically does on input.** Arrows step the avatar; ACTION5 cycles size. Mixed arrow + modal — overlaps action-class with cn04/sp80/m0r0/wa30 but the modal verb is *self-resize*, not *select-and-rotate* / *pour* / *lock-onto-stone*.
3. **What the level is asking for.** Body-fits-socket-at-matching-size. Different from cover-targets, route-flow, paint-canvas, recipe-collect, sequence-spell, partition-region.
4. **What kills the player.** Step budget exhaustion (universal). No hazard-on-contact. No chaser. No attempt-budget.
5. **The cast of supporting elements.** Walls + socket + (L2) shove-blocks + (L3) breakaway-wall + step-counter HUD. Avatar has internal pattern (cross at any size). Sockets are hollow rings sized to match the three avatar sizes. Different from "coloured pawns + same-colour targets" (kf42/vh68).
6. **Visible visual signature.** Palette: background = 2 (light-grey), walls = 4 (off-black) with a brick texture using 5 (black) accents, avatar = 12 (orange) with 13 (maroon) cross, socket = 11 (yellow), shove-block = 15 (purple) with 6 (magenta) interior, step counter = 9 (blue) draining to 0 (white). Six distinct sprite-content palette values; no `{4,8,9}` red-blue-wall trap; no green-means-go.
7. **Pixel grain of primary sprites.** Every primary sprite has internal pixel structure: avatar has a cross marking the centre and a thicker outline at larger sizes; sockets have a hollow square ring of variable border thickness; shove-blocks have a 4-pixel cross interior; walls have a 4-cell brick repeating texture. No 1×1 or plain-fill sprites.
8. **The core dynamic.** "I am bigger or smaller, and that changes what I can do." No prior or reference game makes the player's *own footprint size* the load-bearing verb. s5i5 makes *external rods* size-variable; gv47 makes *regions on a canvas* size-variable; nb6t makes *jointed arm-segments* size-variable. None has the player-body itself as the resizable entity.

For every prior, max overlap is on dimension 4 (step-counter universal), occasionally dimension 2 (mixed arrow + modal). No prior overlaps on 3+ dimensions; the candidate diverges strongly on dimensions 5, 6, 7, 8 (the named principles).

**Verdict: NOVEL.** Pass both positive similarity check and negative similarity check.
