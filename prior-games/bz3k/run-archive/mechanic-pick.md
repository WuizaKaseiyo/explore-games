# Mechanic Pick

## 4-character ID
`bz3k`

Verified: not in 25-game reserved list, not in `prior-games/index.md` (60 entries scanned), not an English word, lowercase alphanumeric, 4 chars.

## Mechanic family
`drift-impulse-cardinal`

## One-paragraph description
A single avatar carries persistent integer cardinal velocity `(vx, vy)` that
**survives between turns**. Each arrow press applies a ±1 impulse to the
matching velocity component (↑: vy-=1, ↓: vy+=1, ←: vx-=1, →: vx+=1) and
THEN slides the avatar by `(vx, vy)` cells, one cell at a time, with
per-cell collision: a wall stops the avatar at the wall and zeroes the
matching velocity component, a hazard ends the level. The avatar's
velocity is surfaced visually by a persistent trailing **wake** of pixels
emanating from the avatar's rear (opposite to current velocity), with wake
length matching `|vx|+|vy|` and wake orientation reflecting the velocity
direction. Targets latch only on **speed-zero arrival** (vx == vy == 0 in
the destination cell), so the player must plan a deceleration phase before
parking on a target. L1 introduces drift-impulse alone in a small open
arena with one target. L2 adds a **velocity-cap band** — a thin striped
cell strip that clamps `max(|vx|, |vy|)` to a level-specific cap when the
avatar passes through (the cap forces threading at low speed past tight
hazard-pinches). L3 adds a **velocity-flipper plate** — a hatched cell
that negates BOTH velocity components when entered (a brake-and-turn-
around in one cell), creating routing problems that demand using the
plate to reverse direction without expending arrow impulses.

## Core knowledge prior alignment
- **Physics** (intuitive momentum / inertia / collision-and-stop) is the
  primary prior. The avatar behaves like a frictionless puck on a rink.
- **Objectness** (the avatar is a coherent persistent entity; walls and
  hazards are coherent obstacles).
- **Geometry** secondarily: cap-bands and flipper-plates are local
  geometric features whose effect is positional.

No agentness (no NPCs); no advanced topology required; no acquired
symbolic knowledge. Conforms to `core-knowledge-priors.md`.

## Novelty checks

### Against the 25 reference taxonomy (positive `similarity-check`)

Candidates flagged by the family-level scan:

- **m0r0 (mirror-orb-merge)**. Family: deterministic-paired-pawn motion.
  Description-level match? NO. m0r0 has 2-4 orbs that move in mirror-axis
  lockstep across quadrants; arrows move all orbs simultaneously with axis
  flips; ACTION6 lock-onto-post-stone toggles mode. Drift-impulse has ONE
  avatar with persistent velocity that arrows IMPULSE; nothing mirrored,
  no quadrants, no second orb. Distinguishing rule (concrete): m0r0's
  motion is single-cell-per-action and resets to zero between actions;
  drift-impulse's velocity is multi-cell-per-action and *persists across
  actions*, accumulating over multiple presses.
- **tu93 (maze-pickup-train)**. Family: trail-pickup. NOT a match. tu93
  has a 3-cell-tall pawn that hops 3 px along value-2 corridors and
  collects a duckling-train of objects; drift-impulse has no train, no
  corridor-typing — the avatar just drifts on a normal grid.

No reference game has persistent inter-turn velocity. The closest
"motion" priors all reset to rest at action end.

### Against `prior-games/index.md` (60 entries; positive check)

Flagged by the family-level scan as needing description-level
distinguishing rules:

- **wt39 (glide-deflect-thaw)**. Closest in feel. Description: "pawn
  glides in pressed direction until wall; angled bumpers deflect 90°;
  L2 adds bumpers, L3 adds brittle thaw-tiles that crack after one
  slide." Distinguishing rule (concrete): in wt39, each arrow press
  fires a *single one-shot glide* in the pressed direction that runs
  until a wall is hit, after which velocity is zero again — no momentum
  carries over between actions. In drift-impulse, the avatar's velocity
  is a *persistent two-axis vector* that survives every action;
  successive presses *accumulate*; ↑ then → produces simultaneous
  northwest motion via `(vx=+1, vy=-1)` rather than two separate east
  and north slides. Walls in drift-impulse zero only the matching
  velocity *axis*, not all motion.

- **kn58 (anchor-pull-magnet)**. Description: "click any cell to place
  a single magnetic anchor; every coloured pawn slides one cell along
  its dominant Manhattan axis toward it." Distinguishing rule: kn58's
  motion is anchor-induced (pawn slides toward the latest click), single
  cell per click, applied to multiple pawns. Drift-impulse motion is
  arrow-thrust-induced on a single avatar, scales with accumulated
  velocity (multi-cell per press), and obeys persistent inertia rather
  than per-click attraction.

- **tg6w (settle-pile-tilt)**. Description: "arrow press tilts the
  playfield's down direction; loose blocks slide multi-cell to settle,
  with colour-permeable rim walls and one-shot sticky-pads."
  Distinguishing rule: tg6w gravity acts on *every loose piece
  simultaneously*, slides them to rest in one shot per arrow press, and
  resets on the next arrow. Drift-impulse acts on a *single avatar* with
  *cumulative velocity* across presses; no global gravity field.

- **vt6q (grapple-anchor-yank)**. Description: "fire a directed cardinal
  grapple line; heavy anchor yanks avatar to adjacent cell, light anchor
  yanked to socket." Distinguishing rule: vt6q is single-shot grapple
  yanking with a fixed cell magnitude per fire. Drift-impulse has no
  grapple verb at all — every motion is the ambient velocity, which has
  variable magnitude and direction.

- **zd7m (cohort-step-route)**. Description: "arrows step every movable
  pawn one cell; anchors selectively block; portals teleport into a
  sealed chamber." Distinguishing rule: zd7m moves every pawn by exactly
  one cell per arrow, no momentum. Drift-impulse moves a single avatar
  by `|velocity|` cells per arrow, with that magnitude growing over
  successive presses.

- **zw91 (inflate-fit-burst)**. Avatar with cycling footprint sizes; not
  motion-based. Family-level match is shallow ("single avatar"); no
  description-level overlap.

- **kx14 (tide-tilt-buoyant)**. Vertical fluid tank with anchored balls
  and rising water surface. Different domain (fluid surface) and verbs.

No prior in the index has *persistent inter-turn velocity* on a single
avatar with *cardinal-impulse-only* control. This specific dynamic is
unrepresented.

### Negative similarity check (per `negative-similarity-check.md`)

Walking the 8 dimensions against each flagged prior + reference, the
closest case is **wt39 (glide-deflect-thaw)**:

1. **What is on the board** — both: avatar + walls + targets (+ hazards
   in later levels). SHARED.
2. **What the player physically does on input** — wt39: arrows fire a
   one-shot slide. drift-impulse: arrows apply persistent ±1 velocity
   impulse. DIFFERENT (the input feel is fundamentally different —
   accumulating throttle vs. discrete glide).
3. **What the level is asking for** — wt39: reach a target (also via
   gliding). drift-impulse: reach a target with speed-zero arrival.
   PARTIALLY SHARED (both end at target; drift-impulse adds speed
   constraint).
4. **What kills the player** — wt39: step budget + thaw-tile
   over-traversal. drift-impulse: step budget + hazards. SHARED (both
   step budget; drift-impulse adds momentum-routing-into-hazard as a
   distinct fail mode).
5. **The cast of supporting elements** — wt39: bumpers (L2),
   thaw-tiles (L3). drift-impulse: cap-band (L2),
   flipper-plate (L3). DIFFERENT (cap-band and flipper-plate
   operate on velocity *vector* state; bumpers and thaw-tiles operate
   on glide-direction and tile-durability).
6. **Visible visual signature** — wt39 has clean sliding pawn with
   simple bumpers; drift-impulse has avatar + persistent velocity-wake +
   striped cap-bands + hatched flipper-plates. The **wake trail of
   pixels behind the avatar** is a unique signature element absent from
   wt39 (which has no trail / wake). DIFFERENT.
7. **Pixel grain of primary sprites** — drift-impulse will use a
   detailful avatar (4×4 or 5×5 with internal pattern), structured
   cap-band striping, and a hatched flipper-plate. wt39's primary
   sprites are smaller and less differentiated. DIFFERENT.
8. **Core dynamic** — wt39's player-thinking is "fire-and-forget glides
   with deflection planning". drift-impulse's player-thinking is
   "manage two-axis momentum across many turns, plan deceleration before
   targets, route through caps and flippers as velocity-modifiers".
   FUNDAMENTALLY DIFFERENT — this is the load-bearing axis (Principle 3).

Sharing-count vs. wt39: dim 1, partial dim 3, dim 4. Heaviest dimensions
(6, 7, 8) all DIFFER. Below the rejection threshold of 3+ on the heavier
axes; clearly distinct.

Against all other priors and references the shared-dimension count is
lower (no other game has any form of "drift across the board" feel).

### Verdict

**NOVEL** against both the 25 reference taxonomy and the 60-entry
prior-games index, on both the positive similarity-check and the
negative-similarity check.

## Notes on visual design decisions
- The persistent-velocity *wake* (a tail of pixels behind the avatar)
  must NOT read as a directional arrow glyph (forbidden per
  `forbidden-elements.md`). Solution: the wake is a *blurry irregular
  smear* of avatar-coloured pixels with diminishing density, not a
  chevron shape. Length conveys magnitude; direction-of-emanation
  (relative to avatar) conveys velocity orientation.
- The cap-band tile is rendered as parallel diagonal stripes — abstract
  geometric pattern, not a glyph.
- The flipper-plate is rendered as a hatched cross-pattern (two diagonal
  bands crossing at right angles, no caret/arrow). Reads as "perturb
  the dynamics here", not as a letter or symbol.
