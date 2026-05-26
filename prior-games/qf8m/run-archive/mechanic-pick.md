# mechanic-pick — qf8m

## ID

`qf8m` — 4 chars, lowercase, alphanumeric, not an English word, no
collision with the 25 reference games or with any of the 50 entries
in `prior-games/index.md`.

## Mechanic family tag

`rook-cross-toggle`

## One-paragraph description

Each level renders a small grid of square tiles (5×5 or 6×6
visible cells), where every tile holds a discrete *state* picked
from a small palette (binary in L1; tri-state on L3). The player
clicks a tile (ACTION6); the click does not act locally — it
toggles the *state of every tile in the clicked tile's row AND
every tile in its column*, sweeping a "rook-cross" of state
changes outward. The player's job is to drive the entire grid's
state pattern to a *target pattern* shown alongside the
playfield, picking the right sequence of click-cells to flip
the right rows+columns into alignment. The dynamic the player
must internalise is: each click is a *long-reach* flip, not a
local one — every click affects 2N-1 tiles (where N is the side
of the grid), so individual tiles are over-determined and the
solution lives in the linear-algebra structure (Z_2 in L1/L2,
Z_3 in L3) of which row+column compositions reach the target.

## Action mapping (intended)

| Action | Semantic |
|---|---|
| ACTION6 | click a tile → toggle the state of every tile in the clicked tile's row and column (2N-1 tiles flipped) |

`available_actions=[6]`. No movement, no ACTION5 freedom-slot
verb — slot 5 is intentionally absent because the rook-cross
flip *is* the distinctive verb, encoded into ACTION6 by the
choice of click target. (Per `action-enum.md`'s "distinctive
verb on ACTION6" pattern observed in lp85, vc33, ft09.) ACTION7
omitted — there is no in-game undo (a wasted click costs steps
but is recoverable by re-clicking, since clicks are
self-inverse in Z_2).

## Core-knowledge priors (per `core-knowledge-priors.md`)

- **Objectness**: tiles are persistent entities at fixed cell positions.
- **Basic geometry/topology**: row/column connectivity is the
  geometric reach of a click. The "rook" topological move (any
  cell on the same row OR column is "reachable") is the
  load-bearing relation.

No physics, no agentness — clean two-prior pairing, in the
"less-explored corner" of the priors-cube per `cross-cut-frequencies.md`.

## Forbidden-elements check (per `forbidden-elements.md`)

No letters, no digits as glyphs, no clipart, no cultural
conventions. Tile palette deliberately avoids
`green=go`/`red=danger` — uses neutral hue progressions
(magenta/light-blue/pink for L3 tri-state, off-black/light-grey
for L1/L2 binary). Lock-frames in L2 are rendered as a small
internal *outline* on the tile pixels, not a "🔒" glyph.

## Positive similarity check vs the 25 reference games

Walking the taxonomy for any row whose family-tag, win
condition, or primary action overlaps:

### Near-miss 1: `ft09` (stamp-3x3-paint)
- **Family**: `stamp-3x3-paint` — click a cell, the cell's
  centre colour cycles through a small palette; a 3×3 stamp
  template determines which neighbouring cells co-cycle.
  Constraint sprites encode equality/inequality rules between
  adjacent cell centre-colours; goal is to satisfy every
  constraint cell.
- **vs qf8m**: stamp shape is **local 3×3** (or whatever the
  current template is) and configurable; mine is a **fixed
  rook-cross of length 2N-1** spanning the entire row +
  column. ft09's *win* is constraint-satisfaction over local
  inequality predicates; mine's *win* is tile-by-tile
  pattern-equality against a target image. ft09 lets the
  player pick UP NEW STAMPS (via clicking template tiles) to
  change the click-shape mid-puzzle; mine has no template-
  switching — the rook-cross shape is invariant.
- **Distinguishing rule**: *ft09's flip-region is a tunable 3×3
  mask; qf8m's flip-region is a fixed (2N-1)-cell rook-cross.
  ft09's win predicate is constraint-graph satisfaction; qf8m's
  win predicate is target-image equality.*

### Near-miss 2: `lp85` (row-col-shift-grid)
- **Family**: `row-col-shift-grid` — clicking a row's L/R button
  shifts the entire row of token positions one cell. Button
  permutations are baked into per-level lookup tables.
- **vs qf8m**: lp85 is **positional permutation** (token
  positions cyclically shift). qf8m is **state toggle** (tile
  positions stay; their colour/state flips). lp85 has external
  arrow-button sprites that the player clicks; qf8m has no
  external buttons — clicks are on the cells themselves.
- **Distinguishing rule**: *lp85 permutes positions of tokens
  along rows/columns; qf8m flips state of every tile in a
  row+column. lp85 has external L/R arrow-button sprites; qf8m
  has none — the click target IS a grid cell.*

### Near-miss 3: `vc33` (row-slide-pull-tab)
- **Family**: clicking a pull-tab at a row's end drags the
  entire row one cell in that direction.
- **vs qf8m**: vc33 is again **positional shift along ONE
  axis** chosen by which tab is clicked. qf8m: a single click
  affects BOTH row AND column simultaneously, and toggles
  state, not position.
- **Distinguishing rule**: *vc33 shifts one row OR one column
  by a click on its tab; qf8m flips one row AND one column by
  a click on a cell. Position-shift vs state-flip; one-axis vs
  two-axis.*

### Near-miss 4: `qx7p` (column-shift-row-align)
- **Family**: vertical colour-band columns slide past a
  horizontal scan line.
- **vs qf8m**: qx7p is column-only positional sliding; qf8m is
  row+column state-flipping.
- **Distinguishing rule**: *qx7p slides columns positionally
  past a scan line; qf8m flips row + column states binary/tri-
  state in place.*

### Near-miss 5: `hp9c` (pinwheel-cell-rotate)
- **Family**: clicking a non-edge cell rotates the 4-cell ring
  around it.
- **vs qf8m**: hp9c rotates a 4-cell *ring* (cyclic
  permutation of 4 surrounding cells); qf8m flips a (2N-1)-cell
  *cross* (parity change of every row+col cell).
- **Distinguishing rule**: *hp9c is a local 4-cell ring
  rotation; qf8m is a global (2N-1)-cell rook-cross flip.
  Rotation vs binary/tri-state flip; ring vs cross.*

### All other reference rows
Click-only games with state-flip semantics: none. Movement
games (ar25, m0r0, sk48, tu93, wa30, ka59, dc22, sc25, ls20,
g50t, etc.) have a player avatar and arrows, which qf8m omits
entirely. Mastermind (sb26) is a sequence-guess. Mechanic-
families with target-image goal (ft09, sb26 sort of, ar25 also
but for mirror-coverage) are addressed above.

## Positive similarity check vs `prior-games/index.md` (50 entries)

Family-level scan — looking for entries whose tag mentions
"row" or "column" or "toggle" or "flip" or "stripe" or
"target-pattern":

- **kf42** (tether-pawn-cycle): pawn movement; nothing in
  common.
- **qz73** (radial-cycle-lock): rotor-of-tips, click-and-rotate;
  different.
- **kx14** (tide-tilt-buoyant): vertical fluid; different.
- **qb84** (bead-lift-swap): pure-arrow swap-with-peg;
  different.
- **lq5x** (lantern-cone-illuminate): cone-projection;
  different.
- **gv47** (seed-grow-surround-dissolve): region-growth +
  dissolve; different.
- **hr8q** (pair-blend-recipe): click two ingredients; recipe
  combinator. Different.
- **ng52** (multiset-signature-classify): partition pool into
  bins; different.
- **pj7k** (rolling-cube-face-paint): cube rolls and stamps;
  different.
- **pz4t** (anchor-pivot-place): jigsaw tiling; different.
- **vn8d** (domino-cascade-topple): chain reaction toppling;
  different.
- **fz5j** (phase-step-tile): per-cell pulsing tiles; different.
- **kn58** (anchor-pull-magnet): magnetic anchor pulls pawns;
  different.
- **bx84** (beam-mirror-reflect): mirror beam routing;
  different.
- **wt39** (glide-deflect-thaw): inertia-glide + bumpers;
  different.
- **zk9p** (pursuer-merge-walk): autonomous pursuers + lure
  collisions; different.
- **rk7x** (live-switch-routing): courier walks; toggle blades
  to route. **Some overlap on toggle**: rk7x toggles a junction
  blade's orientation (orient-flip per cell), but this is a
  per-cell rotation, not a row+column state-flip on neighbouring
  cells. Different scope and effect.
- **gx7m** (gear-mesh-cascade): gear rotations propagate;
  different (positional rotation of gear-faces, not state-flip).
- **vp6h** (shadow-cast-collect): walk + lighting; different.
- **kp9z** (grain-accumulate-topple): cellular sand pile;
  different.
- **zd7m** (cohort-step-route): every pawn steps per arrow;
  different.
- **lv4k** (lever-balance-torque): tray weights torque-sum;
  different.
- **xn5p** (chamber-stamp-partition): wall-stamp partitioning;
  different.
- **mr5q** (polarity-attract-discharge): pawns flip polarity;
  some overlap on "flip" but mr5q's flip is per-pawn polarity
  toggle, not row+col on cells.
- **pf3w** (wavefront-converge-timing): emitter wavefronts;
  different.
- **tg6w** (settle-pile-tilt): physics settle on tilt;
  different.
- **vd3g** (valley-dig-roll): terrain HIGH/LOW + marbles;
  different.
- **jd4q** (echo-trail-teleport): walks + echo deposits;
  different.
- **ek73** (wake-trail-evade): walks + wake hazards; different.
- **tm5x** (thermal-aura-imprint): pawn imprints temperature
  on a 5-cell stamp (centre + 4 neighbours). **Closest overlap
  on "stamp"**: tm5x stamps a 5-cell plus-shape (local). qf8m
  flips a (2N-1)-cell rook-cross (global row+col, much wider
  reach). Distinguishing rule: *tm5x's stamp is a local 5-cell
  plus; qf8m's flip is a (2N-1)-cell row+column rook-cross —
  global reach, not local. tm5x stamps a value; qf8m toggles
  state.*
- **qx7p** — addressed above (taxonomy near-miss is also a
  prior; same rule applies).
- **kj82** (plank-pivot-walk): planks pivot under pawn;
  different.
- **nb6t** (hinge-chain-reach): articulated rod-arm; different.
- **qm4t** (convex-pen-trap): vertex posts → convex hull pen;
  different.
- **qn7w** (pulse-chain-eject): click pushers fire pulses
  through chains; different.
- **zw91** (inflate-fit-burst): avatar size cycle;
  different.
- **fb7t** (phase-transition-matter): heat promotes solid →
  liquid → gas; different.
- **rj5w** / **wj7d** / **qj4r** (fold family): fold/mirror;
  different.
- **jx5k** (constellation-edge-link): pair-click builds graph
  edges; different.
- **lz7q** (dual-plane-walk): day/night plane toggle;
  different.
- **hp9c** — addressed above.
- **ds5q** (wall-erode-chain): pickaxe + walls; different.
- **gh4r** (repulsion-herd-corral): warden-row/col alignment
  makes drifters flee. **Some structural overlap on "row/col
  alignment"**: gh4r aligns a warden with drifters along a
  row/col to *push* them; qf8m clicks a cell to *flip state* of
  the row+col. gh4r drives positional motion; qf8m drives state
  toggle. Mechanism is fundamentally different.
- **qd6n** (chord-pluck-strike): click strings → pulses to
  bells; different.
- **vw3p** (vessel-pour-equalize): pour between vessels;
  different.
- **xv4n** (cavity-nest-fit): silhouette tiling; different.
- **tx4q** (walk-buffer-resonator): walk + 3-slot tone buffer;
  different.
- **tc8s** (trace-enclose-territory): walk closed loops;
  different.
- **vk6m** (altitude-grip-climb): walk + grip-climb; different.

No prior in the index matches qf8m on family + win condition +
primary action; no flagged row needs more than its
distinguishing rule above.

## Negative similarity check (per `negative-similarity-check.md`)

Walking the eight dimensions vs the highest-overlap candidates
(`ft09`, `lp85`, `vc33`, `tm5x`):

| # | Dimension | qf8m | ft09 | lp85 | vc33 | tm5x |
|---|---|---|---|---|---|---|
| 1 | What is on the board | grid of state-tiles + a target-pattern board | grid of state-tiles + constraint sprites | grid of position-tokens + external buttons | row of stones + rails + pull-tabs | walk-grid + pawn |
| 2 | Player physical action | click a cell | click a cell | click a button | click a tab | walk avatar + click for polarity |
| 3 | What level asks for | match target binary/tri-state pattern | satisfy local equality/inequality constraint sprites | get tokens onto matching goal cells | get stones over slots | latch targets to (cell, polarity) values |
| 4 | What kills | step budget | step budget | step budget | step budget | step budget |
| 5 | Cast of supporting elements | tiles + lock-frames + target-display + step HUD | tiles + constraint-sprites + stamp-template tiles + step HUD | tokens + buttons + goal cells + step HUD | stones + rails + tabs + slots + step HUD | walk-grid + pawn + targets + step HUD |
| 6 | Visible visual signature (palette) | magenta + light-blue + pink + off-black + grey | mostly `{4 wall, 8, 9}` + tutorial cyan | `{4, 8, 9, 12, 14}` mixed | `{4, 8, 9, 12}` heavy | `{4, 8, 9}` + thermal hue ramp |
| 7 | Pixel grain of primary sprites | rich internal mosaic per tile (8×8 patterned) | small flat 4×4 cell-blocks (chunky upscale) | 4×4 cell-blocks | medium-grain stripes | 4×4 patterned |
| 8 | Core dynamic | rook-cross state-flip with linear-algebra solution structure | constrain-graph satisfaction via local stamp-cycle | positional permutation via baked permutations | row-stripe positional swap | thermal-aura plus-shape stamp |

Shared-dimension counts:
- vs ft09: dim 1 (grid of state-tiles) and dim 2 (click cell) →
  2 shared on the surface dims; but dim 3 (target-pattern vs
  constraint-graph) diverges, dim 6 (palette) diverges, dim 7
  (planned rich mosaic vs chunky 4×4) diverges, dim 8 (rook-
  cross vs constraint-stamp) diverges. **Total: 2 shared.**
- vs lp85: dim 4 (step budget) only; otherwise distinct. **1
  shared.**
- vs vc33: dim 4 only; otherwise distinct. **1 shared.**
- vs tm5x: dim 4 only; otherwise distinct. **1 shared.**

No prior shares 3+ dimensions, in particular no prior matches
on dim 6/7/8 (the named principles). Negative-similarity check
**passes**.

## Verdict

**NOVEL**. Family `rook-cross-toggle`, ID `qf8m`. Proceed to
`write_spec`.
