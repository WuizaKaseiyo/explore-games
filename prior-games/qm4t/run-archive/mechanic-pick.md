# Mechanic Pick

## Game ID
**qm4t**

Verified: not in the 25 reference IDs, not in `prior-games/index.md`'s
`game_id` column (last appended row at 2026-05-07T22:11:11Z). Not an
English word; lowercase alphanumeric; 4 chars.

## Mechanic family
**convex-pen-trap**

## One-paragraph description

Several coloured "critter" sprites scatter on the playfield. The
player places **vertex-posts** (one per click on an empty cell) to
define the corners of a convex polygon. As soon as three or more
posts have been placed, the engine renders the **convex-hull
polygon** of all current posts as a single-pixel outline, plus a
faint inside-tint for visibility. ACTION5 **commits** the pen:
every critter sprite whose centre lies STRICTLY INSIDE the convex
hull is "captured" (removed). Each level shows a tally HUD of the
required per-colour capture counts; capturing a critter whose
colour is not on the tally costs a strike (3 strikes → lose).
Clicking on a post that is already placed picks it up and removes
it (so the player can revise the polygon before committing). The
game is won when the tally is satisfied (all required-colour
captures done). The mechanic is pure GEOMETRY + OBJECTNESS: a
literal point-in-convex-hull test with no time evolution, no
chemistry, no growth — the player's planning task is to position
3-or-more vertices so the convex hull contains exactly the right
multiset of critters.

## Action subset
`available_actions = [5, 6]`. Pure click + freedom-slot commit.
The distinctive verb (ACTION5) is **commit-pen**: trigger the
inside-polygon evaluation and capture. ACTION6 (click) is the
multipurpose place / pickup interaction.

## Per-level sketch (informs `write_spec`)

- **L1** — Single critter colour. 3-4 same-coloured critters
  scattered. Player places 3 posts → triangle → commit captures
  all. Tutorial of the pen-and-commit ritual.
- **L2** — Two critter colours; tally requires only one. Decoy
  critters of the other colour mixed in such that no triangle
  enclosing all targets misses every decoy. Witness must lift one
  post and re-place it OR add a 4th post (using convex-hull
  reshape) so the polygon's corner cuts the decoy out.
- **L3** — Three colours, of which two are required (different
  per-colour counts) and the third forbidden. Add **patroller
  critters** (forbidden colour) that walk a fixed 1-cell-per-turn
  cycle along a small loop. The convex polygon containing all
  targets ALWAYS overlaps the patroller loop on most cycle phases
  — the player must time the commit such that, at the moment
  ACTION5 fires, every patroller is on a loop cell that lies
  outside the chosen polygon.

The L3 composition exercises pen-placement (L1) + colour
discrimination (L2) + patroller-timing (L3) all together.

## Similarity check — taxonomy of 25 reference games

Walking `mechanic-novelty/similarity-check.md` against every
taxonomy row:

- **Family-level matches:** none. No reference family contains the
  words "pen", "convex", "hull", "polygon", "vertex", or "trap".
- **Description-level near-misses (consulted
  `skills/mechanism-details/<id>.md` and the deep-analysis layer
  for each):**
  - **su15** (radial-blast-capture). Verb: click any cell to
    detonate a radial vacuum that sucks fruit toward the click
    centre. Win = collect all fruit. Distinguishing rule: su15's
    capture region is a **fixed-radius disk centred on the click
    point**, automatically; qm4t's capture region is a
    **player-defined convex polygon** of variable shape
    constructed across multiple clicks. su15 is single-click +
    radius; qm4t is multi-click + commit. su15's primary
    difficulty is targeting; qm4t's primary difficulty is
    geometric reasoning about which vertex configuration
    produces the desired hull.
  - **ar25** (shape-mirror-cover). Verb: nudge a shape across a
    mirror axis to align "8" connectors. Distinguishing rule:
    ar25 manipulates one MOVABLE SHAPE per move and the
    "polygon" of interest is the mirrored ghost; qm4t places
    multiple INDEPENDENT POSTS whose convex hull is the polygon
    of interest. ar25 wins on alignment-of-pixels; qm4t wins on
    spatial inclusion of a multiset.
  - **r11l** (centroid-puppet-leg). Verb: click leg, click
    target → leg flies to target dragging head along.
    Distinguishing rule: r11l moves a single tethered leg to a
    target; qm4t deposits stationary vertex-posts. r11l's
    mechanic is centroid-follow; qm4t's is convex-hull
    inclusion.
  - All other 22 references diverge on family AND on the three
    similarity-check sub-questions (verb / win / constraint).

## Similarity check — `prior-games/index.md` (34 priors)

- **Family-level matches:** none. No prior contains the words
  "pen", "convex", "hull", "polygon", "vertex", "trap", or
  "enclose".
- **Description-level near-misses:**
  - **gv47** (seed-grow-surround-dissolve). Closest prior. gv47
    grows organic colour BLOBS that, on contact, dissolve
    same-colour pips ringed in black. Distinguishing rule:
    gv47's "surround" emerges from a **cellular-automaton-style
    region growth** triggered by clicking seeds; qm4t's
    "surround" is an **explicit geometric convex hull** computed
    from posted vertices. gv47's regions evolve over time; qm4t
    is purely static-geometry — no time evolution between commit
    presses. gv47's chemistry-mix on ACTION5 has no analogue in
    qm4t. The player's planning task is fundamentally different:
    gv47 player thinks about region shape EVOLUTION and contact
    timing; qm4t player thinks about vertex POSITIONS that
    produce a desired hull.
  - **xn5p** (chamber-stamp-partition). xn5p stamps walls to
    SUBDIVIDE a single connected region into per-colour
    sub-regions. Distinguishing rule: xn5p WRITES walls that
    cut terrain; qm4t reads SPATIAL containment of a
    player-defined polygon (non-modifying). xn5p's mechanic
    operates on a connected region's boundary; qm4t operates
    on a finite point set.
  - **ng52** (multiset-signature-classify). ng52 partitions
    objects into BINS labelled with target multiset signatures.
    Distinguishing rule: ng52's grouping is by per-object click
    assignment (attribute-based); qm4t's grouping is by spatial
    inclusion in a player-drawn convex hull (geometric). ng52
    has bins as fixed sprites; qm4t has no bins — the polygon
    is constructed dynamically.
  - **kn58** (anchor-pull-magnet). kn58 places a single
    magnetic anchor; pawns slide one cell toward it.
    Distinguishing rule: kn58 is a single click with
    automatic motion of pawns; qm4t requires multiple clicks
    that do NOT cause motion until ACTION5 commits, and the
    operation is enclosure-not-attraction.
  - **pz4t** (anchor-pivot-place). pz4t tiles a target region
    with coloured components using anchor + reflect + rotate.
    Distinguishing rule: pz4t places coloured pieces to TILE a
    region; qm4t places single-pixel POSTS to define a polygon.
    pz4t fills space with shapes; qm4t classifies points by
    inclusion in a hull.
  - All other 29 priors diverge on family AND verb AND core
    dynamic.

## Negative similarity check (`negative-similarity-check.md`)

The closest prior — gv47 (surround-and-dissolve) — was opened at
`prior-games/gv47/run-archive/smoke-frames/level_1.png`. The
rendered frame shows organic blob pieces with internal hollow
pixels (the yellow blobs with white centres) plus dark pip
sprites. Walking the eight dimensions:

1. **What is on the board.** gv47: paint blobs + ringed pips.
   qm4t: vertex-posts + critter sprites + a pen-outline. Different
   — qm4t has explicit polygon edges as visual entities, gv47
   does not.
2. **What the player physically does.** gv47: click seeds, ACTION5
   to mix. qm4t: click posts, ACTION5 to commit. SHARED at the
   "click + ACTION5" verb level. Counts as 1 shared dimension.
3. **What the level asks for.** gv47: dissolve all ringed pips.
   qm4t: capture a target multiset of critters (different from
   "all of them" — the per-colour tally introduces selectivity
   that gv47 lacks).
4. **What kills the player.** Step counter (both). Counts as
   shared.
5. **The cast of supporting elements.** gv47: paint blobs,
   ringed pips. qm4t: vertex-posts, critters, polygon outline.
   Different cast.
6. **Visible visual signature.** gv47 dominant palette is
   `{warm-yellow blobs, dark grey pips, light-grey background}`.
   qm4t's planned palette is **purple-and-cyan vertex-posts,
   green-and-orange critters with visible eye-pixels, off-white
   pen-outline on a navy-blue background** — different on every
   colour axis.
7. **Pixel grain of primary sprites.** gv47's blobs are
   filled-rectangle regions (mostly uniform colour). qm4t's
   critters carry an internal pattern (4×4 or 5×5 with
   eye-and-body internal pixels) and posts have a vertical
   3-pixel spike + cap. More structural detail. Different.
8. **The core dynamic.** gv47 is **simulation of growing
   regions and chemistry-on-contact**; qm4t is **a one-shot
   geometric inside-polygon test** with no temporal evolution
   between commits. Different.

Two dimensions shared (2 + 4: click+ACTION5 verb skeleton, step
counter lose). Below the 3-dimension threshold. Negative check
PASSES.

Also walked the same eight dimensions against su15 (radial-blast)
and ng52 (multiset-classify) — each shares ≤ 2 dimensions with
qm4t. PASSES.

## §3.4 prior compliance

- **Objectness:** ✓ critters are coherent persistent entities; posts
  too.
- **Geometry & topology:** ✓ convex-hull is a geometric primitive;
  point-in-polygon is a topological inside/outside test. THIS is
  the load-bearing prior.
- **Physics:** mild — patrollers in L3 walk on a loop (kinematic).
- **Agentness:** mild — patrollers in L3 act as autonomous mobile
  obstacles.

Two dominant priors (geometry + objectness) plus a third (agentness)
in L3, exactly the "2-3 priors" sweet spot recommended by
`core-knowledge-priors.md`.

## Forbidden-element guard

- No digits, letters, real-world clipart.
- Posts are stylised vertical fence-spike sprites — abstract; do not
  resemble any letter or digit or real-world object iconography.
- Critters are bug-like multi-pixel sprites with two eye-pixels and
  a body fill — abstract; do not represent any specific real-world
  organism or symbol.
- Pen outline is a 1-pixel-wide axis-aligned-or-diagonal segment;
  does not form any character.
- Tally HUD uses coloured swatch dots, no digits — count communicated
  by number of dots, not by digit glyphs.
