# Mechanic pick

## ID
`wm6q`

Verified non-collision: not in the 25 reference IDs, not in `prior-games/index.md` (70 entries scanned). Not an English word; opaque per §3.4.

## Mechanic family
`edge-color-rotate-match`

## One-paragraph description
The playfield is a small fixed grid of square "tiles". Each tile renders four colored
bands — top/right/bottom/left edge — drawn from a 4-colour palette. The player has a
single verb: click a tile (ACTION6) to rotate that tile's *edge-colour assignment* one
notch clockwise (top←left, right←top, bottom←right, left←bottom). The tiles do not
move; only their colour assignment cycles. The win condition is purely local: every
shared edge between two adjacent tiles must carry the same colour on both sides — when
two adjacent edges agree, a continuous colour band visibly bridges the boundary, giving
direct feedback. L1 is two tiles in a row (one click on one tile aligns the shared
edge). L2 introduces a **locked tile** whose edge colours are fixed (a thick frame
pattern in its centre marks it un-rotatable); the player must rotate every neighbour to
conform to the locked tile's edges. L3 introduces a **linked pair** of tiles (a circle
mark in each pair-member's centre, same hue) that rotate in lockstep — clicking either
rotates both — so the player must coordinate joint orientations. Core knowledge priors:
*objectness* (each tile is a discrete coloured object) and *basic geometry* (90°
rotation of a 4-symmetry assignment).

## Novelty checks

### Against the 25-game taxonomy
- **cn04 — nub-pair-glyph** is the closest near-miss because both ask the player to
  match shapes/colours across tile boundaries via rotation. **Distinguishing rule:**
  cn04 has free-form jigsaw pieces that *move* across an open playfield (click-to-
  select + arrow-to-translate + ACTION5-to-rotate-the-piece-shape); the win condition
  is pixel-level "8" connectors snapping across coincident locations of two distinct
  pieces. `wm6q` has uniform fixed-position square tiles that never move (no arrow
  input, no click-to-select state); the only verb is "click rotates this tile's
  4-colour edge-assignment one notch CW", and the win condition is colour equality
  on already-adjacent boundaries. The shapes are identical from one click to the next
  — only the colour permutation rotates.
- **ar25 — shape-mirror-cover**: shape-mirror-cover involves mirror-axis play and
  arrows. Mine has no avatar, no mirror, no arrows. Not a near-miss; pass.
- **ls20 — cycler-attribute-match**: ls20 has a walking avatar that hops onto cycler
  tiles which roll attributes through a fixed alphabet, and a goal pad. Mine has no
  walker; the player is a disembodied click. Pass.
- All other taxonomy entries differ on primary-action AND on win condition; pass.

### Against the prior-games index
- **qf8m — rook-cross-toggle**: clicks tiles to flip a rook-cross pattern of CELL
  colours. **Distinguishing rule:** qf8m flips colours over a non-local cross of cells
  (the click affects a 2N-1 line); `wm6q`'s click affects exactly ONE tile (purely
  local), and what changes is not cell-colour but the *4-edge colour permutation*
  inside that one tile. qf8m has no per-tile internal-edge structure; mine does.
- **mz6t — majority-vote-stabilize**: clicks cycle a CELL through 3 colour states;
  ACTION5 ticks a global majority-vote. **Distinguishing rule:** mz6t treats each cell
  as a single colour bit and applies a global cellular-automaton rule (majority-vote
  neighbourhood); mine treats each tile as a 4-edge colour vector that rotates as one
  unit, with no automaton step (no ACTION5, no global tick).
- **xz5g — arena-pivot-rotate**: click sets a global pivot; ACTION5 rotates every
  rotatable sprite 90° around it. **Distinguishing rule:** xz5g rotates *positions* of
  many sprites about a chosen centre (a global geometric rotation of the playfield
  contents); mine rotates *edge-colour assignments within a single tile* with no
  positional change of any sprite. The "rotation" is internal-to-tile, not arena-wide.
- **vy3k — region-swap-arrange**: arrows walk an avatar; click+ACTION5 swap two
  quadrants or rotate one. **Distinguishing rule:** vy3k has an avatar and rearranges
  large blocks; mine has no avatar and operates on each tile's internal colour
  permutation only.
- **hl4n — row-col-tint-cross**: click row/column markers to cycle row/column tints;
  cells take colour from a row+column combiner. **Distinguishing rule:** hl4n's click
  acts on a row/column band (long-range), and cells derive colour from a 2-axis
  combiner; mine clicks on a single tile (local) and cycles only that tile's edge
  permutation, with no row/column inheritance and no combiner function.
- **jx5k — constellation-edge-link**: pair-click coloured nodes to *create edges*
  between them. **Distinguishing rule:** jx5k builds an arbitrary edge-graph on a
  fixed point cloud; mine has no edges to build — every adjacency is fixed by the
  grid layout, and the only player-controlled variable is the cyclic assignment of
  colours to a tile's pre-existing 4 edges.
- All other priors differ on primary-action AND mechanic family; pass.

### Negative similarity walk (against cn04 — the only ≥ 1 dimension overlap)
1. *What's on the board.* cn04 = irregular jigsaw pieces over an open playfield.
   `wm6q` = uniform 16×16 square tiles in a tight fixed grid. **Different.**
2. *What the player physically does.* cn04 = click-to-select + arrows-to-move +
   ACTION5-rotate. `wm6q` = click-only, single verb. **Different.**
3. *What the level asks.* cn04 = arrange pieces so connector pixels coincide; `wm6q`
   = adjacent edge colours match. **Similar (both are "boundary alignment" puzzles).**
4. *What kills the player.* Both step-budget. **Shared (universal).**
5. *Cast of supporting elements.* cn04 = pieces only. `wm6q` = tiles + locked tile
   + linked-pair tiles. **Different.**
6. *Visible visual signature.* cn04's L1 frame is a wide playfield of jigsaw pieces.
   `wm6q`'s L1 is a 32×16 strip of two square tiles. **Different.**
7. *Pixel grain of primary sprites.* cn04's pieces have free-form pixel shapes with
   discrete "8" connector pixels. `wm6q`'s tiles all have the same template — 4
   coloured bands of width 3 px each plus a 10×10 inner area for lock/link icons or
   negative space. **Different.**
8. *The core dynamic.* cn04 = "move and rotate the piece-bodies until they fit
   spatially". `wm6q` = "rotate the colour-permutation inside a fixed tile until the
   edges meet". **Different.**

Overlap count = 1 (dimension 3) + 1 trivially-shared (dimension 4 = step budget).
Far below the 3-dimension rejection threshold. Negative test passes.

### Negative similarity walk (against qf8m — closest prior)
1. *What's on the board.* qf8m has a grid of single-colour cells. `wm6q` has a grid
   of multi-edge tiles. **Different.**
2. *What the player physically does.* Both click. **Shared.**
3. *What the level asks.* qf8m = produce a target cell-colour pattern. `wm6q` =
   match every adjacent edge colour. **Different.**
4. *What kills the player.* Step budget. **Shared.**
5. *Cast of supporting elements.* qf8m has bishop tiles + tri-state cells. `wm6q`
   has locked tile + linked pair. **Different (no overlap in support sprites).**
6. *Visual signature.* qf8m is a flat board of single-colour cells; `wm6q` is tiles
   with internal 4-band colour structure. **Different.**
7. *Pixel grain.* qf8m has uniform-colour cells; `wm6q` has rich per-tile pixel
   structure (4 bands + inner glyph). **Different.**
8. *Core dynamic.* qf8m = "click flips a cross of cell colours" (non-local effect);
   `wm6q` = "click cycles one tile's 4-edge permutation" (purely local). **Different.**

Overlap count = 2 (dimensions 2 + 4, both universal). Pass.

### Verdict
NOVEL against the 25-taxonomy and the 70-entry prior-games corpus on both the
positive (similarity-check) and negative (negative-similarity-check) tests.
