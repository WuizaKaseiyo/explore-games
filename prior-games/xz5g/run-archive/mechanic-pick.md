# Mechanic pick

## Game ID

**xz5g** — 4-char, opaque, alphanumeric, not in 25 reference list, not
in `prior-games/index.md` (45 entries), not in any of the 9 untracked
prior-games directories (`gh4r, hp9c, lz7q, qd6n, tc8s, tx4q, vk6m,
vw3p, xv4n`).

## Seed

(autonomous) — no user-provided seed.

## Mechanic family

**arena-pivot-rotate**

## One-paragraph description

The player solves spatial puzzles by repeatedly rotating the entire
playfield's contents around a player-chosen pivot cell. ACTION6 clicks
any empty cell to place a `pivot_marker` at that cell (a halo sprite
attaches to the marked cell as the persistent visual cue; clicking
another cell relocates the marker). ACTION5 commits a 90° rotation
around the marked pivot — every sprite carrying the `rotatable` tag
(the avatar plus any free pawns and rotatable walls) gets its grid
position transformed by the standard 90°-rotation around the pivot
(`(x', y') = (px + (py - y), py + (x - px))` for clockwise) AND its
sprite-rotation increased by 90°; sprites carrying the `anchor_pin`
tag stay put. The pivot marker survives the rotation, ready for the
next rotation. The avatar's identity verb is "rotate the world to
land where you need to be"; the avatar never walks (no ACTION1-4
movement). The level wins when the avatar's grid cell coincides with
the same-colour target ring; lose when the step counter exhausts.
Levels compose: L1 introduces pivot-set + commit-rotate (the base
dynamic system, two interacting mechanics); L2 adds anchor-pin
sprites that stay fixed during rotations, constraining solutions
geometrically; L3 adds a CW/CCW direction toggle (ACTION1 flips
the next rotation's direction; an indicator sprite shows current
direction) plus multiple movable pawns each needing simultaneous
delivery to its own colour-matched target.

## Closest taxonomy near-misses + concrete distinguishing rules

### vs `vy3k` — region-swap-arrange (prior-games, 2026-05-08)

**vy3k**: 4 fixed quadrant centers; ACTION6 click selects a quadrant;
ACTION5 with ONE quadrant selected rotates that quadrant's
`rotatable` sprites 90° CW *contained inside that quadrant only*;
with TWO quadrants selected, swaps avatars between them. Discrete
4-choice cognitive task.

**xz5g**: NO quadrants. Pivot is **player-chosen any cell** (4096
choices on a 64-cell grid). Rotation is **whole-arena**, not local
to a sub-region; every `rotatable` sprite anywhere on the playfield
transforms relative to the pivot. The cognitive task is *continuous
pivot search* ("which cell, when rotated around, swings the avatar
along the right arc?") — fundamentally different from vy3k's
discrete quadrant choice. There is no swap verb in xz5g. The
selection cue (a halo on the pivot cell) is one persistent sprite,
not 4 quadrant frames.

### vs `hp9c` — pinwheel-cell-rotate (prior-games, recent)

**hp9c**: ACTION6 click on an inner-3×3 cell rotates the four
**cardinal-neighbour cells** of the clicked centre one step CW
**around that centre**. Effect is local — a 4-cycle on 4 adjacent
cells. Other cells in the 5×5 board stand still. Click rotates
*tokens* (cell-state values), not sprite positions; sprites stay
geometrically in place.

**xz5g**: rotation transforms **sprite POSITIONS** (translates +
rotates the sprite around the pivot), not the values stored in
fixed cells. Effect is **whole-arena**; every `rotatable` sprite
changes grid position. Sprites get their internal pixel matrix
rotated too (`sprite.rotate(90)`), not just the cell-state value.
hp9c's 4-cycle ring vs xz5g's geometric (px + (py - y), ...)
formula are different transformations on different objects.

### vs `cn04` — nub-pair-glyph (reference)

**cn04**: rotates a SINGLE selected sprite 90° in place via
`sprite.rotate(90)`; all other sprites are untouched; selection
state is per-piece; pivot is implicitly the sprite's own centre.

**xz5g**: rotates EVERY `rotatable` sprite together, around an
EXTERNAL pivot. There is no per-sprite selection; the pivot is the
single global piece of state. The axes of rotation (per-piece
self-axis vs external pivot) are conceptually distinct.

### vs `qj4r` / `rj5w` / `wj7d` — fold/mirror family

These are **mirror reflections** across a folding axis (mirror
operation, signature group D2 reflection). xz5g is **rotation
around a point** (signature group C4 rotation). Different
geometric transformation; different invariants; different
cognitive task (fold once flips parity; rotate four times
returns).

### vs `pv5q` — pivot-rod-swing (prior-games, recent)

**pv5q**: avatar is fixed at the END of a rigid radial rod attached
to a pivot stake; arrows swing the rod one octant or extend/retract
the rod's radius; ACTION5 transfers the anchor between two stakes.
The avatar's position is *parametrically* tied to (anchor, R, θ);
the rest of the world is static.

**xz5g**: there is no rod. The avatar is a normal sprite that
happens to be `rotatable`. ACTION5 rotates **every** rotatable
sprite around the pivot — the avatar plus other pawns/movable walls
all transform together. There is no R or θ state; the pivot is
just a click-marked cell, and the rotation applies to whatever's
currently on the board. Rotation is a single-shot whole-arena
transform vs pv5q's per-step parametric swing.

### vs `qz73` — radial-cycle-lock (prior-games)

**qz73**: rotor of coloured tips at the playfield centre; rotate
the rotor and lock individual tips so they no longer rotate;
align each tip with its same-colour socket on the rim.

**xz5g**: no fixed rotor. The "rotor" is the entire arena and the
"axle" is wherever the player clicks. Tips are not pre-arranged
on a rotor; sprites are placed freely and the player chooses a
new pivot for each rotation.

## Negative-similarity check (`negative-similarity-check.md`, 8 dims)

Walking the 8 dimensions vs the closest prior, **vy3k**:

1. Board: avatar + walls + targets on grid → SHARED.
2. Input: click + ACTION5 commit → SHARED.
3. Goal: avatar on colour-matched target → SHARED.
4. Lose: step budget exhaustion → SHARED.
5. Cast: avatar + walls + targets + halo (mine) vs avatar + walls
   + targets + selection-frames (vy3k) → SLIGHTLY DIFFERENT
   (one halo vs four frames; no lock-toggle in mine).
6. Visual signature: mine uses denser 6×6+ sprites with internal
   pattern + a distinctive pivot-halo and rotation-trail-arc
   overlay (rendered as 8-tick fade) → DIFFERENT.
7. Pixel grain: planning to use 6×6 / 8×8 primary sprites with
   internal motif (avatar = 6×6 tri-quadrant pattern, targets =
   concentric hollow rings); vy3k uses 4×4 hop-grid blocks →
   DIFFERENT.
8. Core dynamic: "transform arena geometry around a chosen
   centre" → SHARED at the verb level (rotate) but **the freedom
   of pivot placement is the substantive divergence**. vy3k's
   cognitive task is "which of 4 quadrants do I touch?"; xz5g's
   is "where on a 64-cell grid do I place the pivot?", a
   continuous 2D search. The play feel is different: vy3k feels
   like flipping panels on a Rubik-style board; xz5g feels like
   spinning a globe around a chosen pin.

Shared count: 1, 2, 3, 4 (the universal "walk-grid + reach
target" base) plus partial 8 (rotate verb).
Distinct: 5, 6, 7 (visual signature, pixel grain, cast variation),
plus the freedom-of-pivot core-dynamic distinction.

Verdict: **borderline by surface signature, but core-dynamic
divergence (continuous-pivot vs discrete-quadrant) is the named
Principle 3 divergence in `negative-similarity-check.md`**. Plan
to re-run the negative test in `critique_spec` against the fully
fleshed-out spec — if L2 or L3 drift toward vy3k's discrete-choice
feel, revise.

Mitigations the spec will commit to:
- **No quadrant-like visual partitioning of the playfield**
  (no divider crosses, no per-quadrant frames).
- **Distinct visual signature**: pivot-halo (palette-7 pink ring)
  + rotation-arc trail (palette-6 magenta fade behind rotated
  sprites), neither of which appears in vy3k.
- **Different pixel grain**: 6×6 / 8×8 sprites with internal
  detail, not 4×4 hop blocks.
- **Anchor-pin sprites** as the L2-introduced mechanic — pegs
  that stay put during rotation, with no analogue in vy3k.

## Prior-games index status

`prior-games/index.md` is non-empty (45 entries). Closest
mechanic-family-tag near-misses already listed above. No exact
mechanic-family collision detected.
