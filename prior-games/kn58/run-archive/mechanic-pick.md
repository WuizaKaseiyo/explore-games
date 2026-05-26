# Mechanic Pick — kn58

## Game ID
`kn58` (opaque, lowercase alphanumeric, 4 chars; not in 25 reference IDs, not in `prior-games/index.md`)

## Mechanic family
`anchor-pull-magnet`

## One-paragraph description

Several distinct-coloured "pawn" sprites sit on a small walled grid alongside same-coloured hollow "target" rings; the player has a single magnetic "anchor" sprite they place by clicking any empty cell (ACTION6). After every click, every pawn simultaneously slides exactly one cell along the cardinal axis whose step shrinks its Manhattan distance to the active anchor (vertical-then-horizontal tiebreak, blocked by walls). Clicking a cell that already holds the anchor removes it (no-op pull that turn). Win when every pawn rests on its same-coloured target ring; lose if the per-level step budget runs out. From L2 onward, pawns mutually block each other during the simultaneous slide (mutual collision freezes both for that tick), so the order in which the player relocates the anchor matters. From L3 onward, ACTION5 acts as a one-tick "BURST" that doubles the slide distance from 1 to 2 cells for the next pull only, AND a fixed "anti-anchor" sprite repels every pawn one cell per tick along the cardinal away-direction (always active, position fixed by the level). The active anchor is always exactly one — placing a new anchor instantly relocates it.

## Closest neighbours and concrete distinguishing rules

### Taxonomy near-misses (25 reference games)

- **ka59 (sokoban-explode-chase)** — Both have multi-pawn movement and target tiles. **Distinguishing rule:** ka59's verb is "click a pawn to make it active, arrows slide *only that pawn* one cell"; pawns push each other (sokoban). kn58's verb is "click *empty cell* to place an anchor"; pawns slide *autonomously and simultaneously* every turn toward the anchor; pawns *block* each other but never *push* each other. The player never directly moves a pawn.
- **m0r0 (mirror-orb-merge)** — Both have multi-pawn simultaneous motion. **Distinguishing rule:** m0r0's pawns mirror across quadrant axes (one direction press moves all four with reflected sign per quadrant). kn58's pawns each slide along their own gradient toward a shared anchor — direction varies per pawn per tick because each pawn computes its own "toward-anchor" axis. The motion field is radial-attractive, not axis-mirrored.
- **wa30 (lock-drag-crate)** — Both involve pawns and target rings on a grid. **Distinguishing rule:** wa30 has a single carrier walking with arrows, ACTION5 lock latches an *adjacent* crate to drag along; in kn58 the player never walks a pawn. Verbs (ACTION1-4 walk + ACTION5 lock) vs (ACTION6 click anchor + ACTION5 burst) are disjoint.
- **r11l (centroid-puppet-leg)** — Both: click + indirect motion. **Distinguishing rule:** r11l has a centroid-follow rule (head sits at the average of legs); each click *throws* a leg piece to a clicked cell. kn58 has no centroid; pawns slide one cell toward the clicked anchor. r11l clicks pick a piece then a destination; kn58 clicks place the single anchor anywhere.
- **ar25 (shape-mirror-cover)** — Different verb (move/rotate a shape) and different goal (cover dots via reflector). No anchor-pull. Pass.
- **dc22 (colour-cycle-walk)** — Avatar walks; cycles colour groups by stepping on triggers. kn58 has no avatar walk and no cycling; mechanic is purely magnetic pull from a click-placed anchor. Pass.
- **ka59/ls20** — Both involve single-step grid motion of small sprites; ls20 has shape/colour/rotation cycler-attribute matching. kn58 has none of those attributes — pawns are simply colour-tagged and immobile-until-pulled.

### Prior-games near-misses (`prior-games/index.md`)

- **kf42 (tether-pawn-cycle)** — Both have multi-coloured pawns on a small walled grid with target tiles. **Distinguishing rule:** kf42 has *two* pawns joined by a max-distance tether; verb is click-to-select-active + arrow-keys-step-active; the inactive pawn drags only when tether stretches. kn58 has *N* pawns, no tether, no select-active; verb is click-to-place-magnetic-anchor; *every* pawn slides every turn under the anchor's gradient. Different controller (player never directly steps a pawn) and different rule (gradient-pull vs tether-drag).
- **qz73 (radial-cycle-lock)** — Both have a "lock/select" feel. **Distinguishing rule:** qz73's verbs are ACTION5 cycle-the-rotor and ACTION6 lock-an-individual-tip; the actor is rotational. kn58's verb is ACTION6 place-anchor-anywhere; motion is translational along a radial gradient. No rotor in kn58.
- **kx14 (tide-tilt-buoyant)** — Vertical fluid tank with water-surface verbs. kn58 is a horizontal walled grid with magnet-pull; no fluid, no tilt. Pass.
- **qb84 (bead-lift-swap)** — Chain of beads on a fixed snaking path with lift/drop swap. kn58 has no chain, no swap, no fixed path. Pass.
- **lq5x (lantern-cone-illuminate)** — Single lantern projecting a directional cone. kn58 has no cone, no illumination, no rotation verb. Pass.
- **gv47 (seed-grow-surround-dissolve)** — Click coloured seeds to grow regions + surround pips. kn58 has no region growth, no painted territories; pawns are single-cell entities that slide. Pass.
- **hr8q (pair-blend-recipe)** — Recipe-mixing ingredient widget; no spatial gameplay. Different domain entirely. Pass.
- **ng52 (multiset-signature-classify)** — Classification by signature; no avatar, no spatial. kn58 is spatial. Pass.
- **pj7k (rolling-cube-face-paint)** — Single rolling 3×3 cube depositing face colours. kn58 has no cube, no face permutation; pawns are tiny single-cell sprites with no internal face state. Pass.
- **pz4t (anchor-pivot-place)** — *Word "anchor" overlaps* but mechanic does not. **Distinguishing rule:** pz4t's "anchor" is the *pivot offset* (which clicked pixel of a polyomino piece becomes the placement origin); the verb is click-pixel-of-component + arrows-to-translate-the-component + ACTION5-rotate, and the goal is to tile a target dark-grey region with all coloured components. kn58's "anchor" is a *standalone magnet sprite* placed at any cell on the playfield; the verb is click-empty-cell-to-place-anchor; pawns are pre-existing and slide autonomously toward it; the goal is each pawn on its same-colour target ring. Disjoint verbs, disjoint goals; the shared word is cosmetic.
- **vn8d (domino-cascade-topple)** — Single click triggers a chain reaction through pillars. kn58 has no chain reaction; pawns slide deterministically per tick under the anchor gradient and stop when they reach a wall or another pawn. Pass.
- **fz5j (phase-step-tile)** — Avatar walks tiles that pulse open/closed on per-cell periods. kn58 has no time-periodic tiles, no avatar walk, no lives. Pass.

## Negative similarity check (per `negative-similarity-check.md`)

Walking the eight dimensions vs the most surface-similar priors:

**vs kf42** (closest visually):
1. What's on board: pawns + targets on walled grid — SHARED.
2. Player physical input: clicking — kf42 clicks pawn to select; kn58 clicks empty cell to place anchor — DIFFERENT.
3. What level asks for: cover/match colour-paired tiles — SHARED.
4. What kills: step budget — SHARED.
5. Cast: pawns + targets + walls — SHARED. **But** kn58 also has: anchor (active sprite), anti-anchor (L3), no tether — DIFFERENT.
6. Visible visual signature: kn58 palette {2 light-grey, 5 black, 12 orange, 15 purple, 14 green, 4 off-black, 0 white, 8 red, 10 light-blue} — kf42 was {4, 8, 9} dominant. DIFFERENT (Principle 2).
7. Pixel grain: kn58's pawns are 3×3 with internal cross-marker (not plain rectangles); anchor is 5×5 with diamond-spike internal structure; targets are 3×3 hollow rings. kf42's pawns were 1×1 plain blocks. DIFFERENT (Principle 1).
8. Core dynamic: kf42 = "drag a partner via tether by stepping the active pawn"; kn58 = "place a magnetic anchor and watch every pawn slide along its own gradient". DIFFERENT (Principle 3 — fundamentally different "what is the player thinking about?").

Shared dimensions: 1, 3, 4 (and partial 5). Three dimensions but they are the lightest three (board class, generic goal class, generic lose). The three heavy dimensions (6, 7, 8) all diverge. **Pass.**

**vs ka59** (closest mechanically — multi-pawn cover-targets):
1. SHARED.
2. Click: ka59 click selects active pawn; kn58 click places anchor. DIFFERENT.
3. Cover targets: SHARED.
4. Step budget: SHARED.
5. Cast: ka59 has chaser-enemy + walls + trigger blocks; kn58 has anchor + walls + (L3) anti-anchor. DIFFERENT (no chaser; no explosion).
6. Palette: ka59 dominant {grey, dark, brick, magenta} per its level art; kn58's deliberate palette differs. DIFFERENT.
7. Pixel grain: kn58's anchor is the visual anchor of the screen — distinct multi-pixel sprite. ka59's blocks are mostly rectangles. Different focus.
8. Core dynamic: ka59 = "select a pawn, slide it three cells, push into target while dodging chaser/triggering explosions"; kn58 = "place a magnetic anchor; pawns slide by themselves; sequence anchor placements so they don't collide". DIFFERENT.

Shared: 1, 3, 4. Pass.

No prior shares 3+ heavy dimensions. **Negative similarity check passes.**

## §3.4 priors used

- **Objectness** — coherent persistent pawn sprites that move and collide.
- **Basic geometry & topology** — walls, Manhattan-distance gradient, simultaneous translation.
- **Basic physics** — magnetic-attraction-like pull (a single-cell-per-tick gradient-step rule, deterministic). The "anti-anchor" in L3 is the polar opposite (repulsion), keeping the prior pure.

No agentness needed for L1 / L2 (anti-anchor in L3 is fixed-position passive — not a chasing/patrolling NPC; can be classified under physics/objectness as a static repulsive source).

## Distinctive verb on ACTION5 (per reference patterns)

ACTION5 = "BURST": doubles the next pull's range from 1 cell to 2 cells, exactly once. Introduced in L3, it's the level's identity verb and rewards timing rather than positioning.

## Action subset

L1: `[6]` — click only.
L2: `[6]` — click only.
L3: `[5, 6]` — click + burst.

(The available_actions in `Game.__init__` will be `[5, 6]` for the entire game; the L1/L2 witness simply doesn't need ACTION5. ACTION5 fires from level 1 but does nothing semantically meaningful when no pawn benefits from doubling — though we'll wire it to be a no-op there to prevent it acting as a hidden mechanic in L1/L2. Final shape decided in `write_spec`.)
