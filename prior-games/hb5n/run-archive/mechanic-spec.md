# hb5n — mechanic spec

## 1. Title

**Polyomino Threader** — an irregular-shaped walking avatar that
translates and rotates to fit its silhouette into a target slot,
growing mid-level via pickups, with pivot-reset cells that
relocate the rotation centre to a different body cell, unlocking
new silhouette shapes. (Working title, NOT visible in-game.)
*Revised in pass #1: changed L3 mechanic from "rotation-lock"
(failed counterfactual necessity) to "pivot-reset".*

## 2. Mechanic family

The avatar is a rigid polyomino (3 cells initially) that walks 1
cell per arrow press and rotates 90° clockwise about its anchor
cell with ACTION5. The level wins when the avatar's current cell
footprint coincides exactly with a target SLOT sprite of matching
silhouette-and-orientation. Mid-level GROWTH pickups extend the
polyomino by one cell (a 4th cell appears at a fixed relative
offset to the anchor); PIVOT-RESET cells transfer the anchor
designation to a different body cell, opening up a new
silhouette-rotation space inaccessible from the original pivot.

**Core-knowledge priors used** (per
`design-constraints/core-knowledge-priors.md`):

- *Basic geometry & topology*: rigid-body rotation in 90°
  increments, congruence of silhouettes (the win predicate is
  silhouette equality up to translation+rotation).
- *Objectness*: the polyomino is a coherent persistent entity
  that moves, collides as one, and accumulates cells.

## 3. Sprite roster

Logical grid is 16×16 cells; each cell is 4×4 display pixels, so
the playfield occupies the full 64×64 frame with no letter-box.
Every gameplay sprite is multi-pixel with internal pattern, per
checklist item 20.

Palette plan (deliberately distinct from the over-used
`{4 wall, 8 red, 9 blue}` cautionary signature):

- 1 (off-white) — playable floor background
- 2 (light grey) — secondary floor accent
- 3 (grey) — target-slot outline
- 4 (off-black) — wall-frame
- 5 (black) — wall-fill
- 8 (red) — avatar-frame
- 12 (orange) — avatar-anchor accent
- 13 (maroon) — avatar-body accent
- 14 (green) — growth-pickup frame
- 11 (yellow) — growth-pickup centre
- 6 (magenta) — pivot-reset pattern

### Sprites

- **`avatar_l3`** — 3-cell L polyomino, base rotation 0. Pixel
  matrix 8×8 (anchor cell at sprite-pixel offset (4,0)–(7,3)):
  ```
  8  8  8  8  8  8  8  8
  8 13 13  8  8 12 12  8
  8 13 13  8  8 12 12  8
  8  8  8  8  8  8  8  8
  8  8  8  8 -1 -1 -1 -1
  8 13 13  8 -1 -1 -1 -1
  8 13 13  8 -1 -1 -1 -1
  8  8  8  8 -1 -1 -1 -1
  ```
  Body cells B (top-left, sprite (0..3, 0..3)) and C (bottom-left,
  sprite (0..3, 4..7)) use the red-frame + maroon-centre pattern;
  anchor cell A (top-right, sprite (4..7, 0..3)) uses the red-frame
  + orange-centre pattern so the player can see which cell is the
  rotation pivot from a static frame. Tags: `["avatar"]`,
  `["sys_click"]` not needed (avatar is not clickable). `layer=2`.

  At runtime the avatar's pixels are rebuilt by `np.rot90(base, k)`
  for the current rotation `k`, and its `(x, y)` position is
  adjusted so the anchor's display pixel stays at `(anchor_x * 4,
  anchor_y * 4)` regardless of orientation.

- **`avatar_j4`** — 4-cell J polyomino (post-pickup form). Same
  cell-pattern convention; pixel matrix 8×12. Used after L2/L3
  pickup consumption. Anchor cell visually retains the
  orange-centre pattern; the new D cell (relative offset (-1, -1)
  in rotation 0, i.e. cell to the upper-left of the anchor) uses
  the maroon-centre body pattern.

- **`wall`** — 1×1 logical wall tile (4×4 pixels). Internal
  brick pattern:
  ```
  5 4 5 5
  5 4 5 5
  4 4 4 4
  5 5 4 5
  ```
  Off-black-on-black bricks; reads as a stone tile. Tag:
  `["wall"]`. `collidable=True`. `layer=-1`.

- **`target_slot_l_rot270`** — outline of the 3-cell L at rotation
  270 (anchor at top-left of slot, B below, C to the right of B).
  Pixel matrix 8×8 with dim outline (palette 3) and `-1` interior:
  ```
   3  3  3  3 -1 -1 -1 -1
   3 -1 -1  3 -1 -1 -1 -1
   3 -1 -1  3 -1 -1 -1 -1
   3  3  3  3 -1 -1 -1 -1
   3  3  3  3  3  3  3  3
   3 -1 -1  3  3 -1 -1  3
   3 -1 -1  3  3 -1 -1  3
   3  3  3  3  3  3  3  3
  ```
  Tag: `["target"]`. `collidable=False`. `layer=0`.

- **`target_slot_j_rot180`** — outline of the 4-cell J at rotation
  180 (3 cells in a vertical line east of anchor, anchor itself
  west). Used in L2.

- **`target_slot_t_b_pivot_rot90`** — outline of the 4-cell T
  shape at the B-pivot's rotation 90 (anchor at one cell with 3
  body cells: A east-of-anchor, C west-of-anchor, D north-of-
  anchor — i.e. cells at relative offsets (0,0), (1,0), (-1,0),
  (0,-1) from the new B-anchor). Used in L3. Drawn as a dim
  palette-3 outline with `-1` interior.

  *(Replaces the earlier draft's `target_slot_j_rot90`, which was
  reachable from the A-pivot J without M4 and therefore did not
  make M4 strictly necessary.)*

- **`growth_pickup`** — single 1×1 logical cell (4×4 px) with
  internal pattern:
  ```
  14 14 14 14
  14 11 11 14
  14 11 11 14
  14 14 14 14
  ```
  Green frame, yellow centre. Tag: `["pickup"]`. `collidable=False`.
  `layer=0`. When the anchor walks onto a pickup, the pickup is
  consumed (sprite set to `InteractionMode.REMOVED`) and the
  avatar gains a 4th cell at the fixed relative offset (-1, -1)
  from the anchor (visually: north-west of anchor at rotation 0).

- **`pivot_reset`** — single 1×1 logical cell (4×4 px) with a
  centre-cross magenta pattern, distinguishable from any wall or
  pickup:
  ```
  4 6 6 4
  6 6 6 6
  6 6 6 6
  4 6 6 4
  ```
  Tag: `["pivot_reset"]`. `collidable=False` (passable underfoot).
  `layer=0`. When the avatar's anchor enters a pivot-reset cell,
  the anchor designation transfers to the cell at rotation-0
  relative offset (-1, 0) (the "B" cell). The avatar's
  `relative_cells` list is re-baselined so that B becomes (0, 0)
  and the prior anchor A becomes (1, 0). After consumption the
  sprite is set to `InteractionMode.REMOVED`. Visually: the
  orange-centred anchor pattern moves to the new anchor cell;
  the previous A cell becomes maroon-centred (body).

  *Replaces the earlier draft's `rotation_lock` sprite, which was
  removed in revision pass #1 after the critique flagged its
  counterfactual non-necessity. See `critique-revisions.md`
  for the full reasoning.*

- **`step_counter_overlay`** — `RenderableUserDisplay` subclass
  painting row 63 (bottom row) of the frame: the leftmost
  `current/max × 64` pixels in palette 14 (green), the remaining
  pixels in palette 4 (off-black). Drives the visible step budget.

## 4. Level progression, mechanic enumeration, and witness solutions

EXACTLY 3 levels. Grid size `(16, 16)` at all 3 levels (no
per-level resize); camera viewport `(64, 64)` (no resize needed —
the engine renders the 16×16 logical grid at 4× scale).

### Level 1 — base dynamic system

**Layout**: outer wall ring (rows/cols 0 and 15 are walls).
Playfield rows 1..14, cols 1..14 open with a uniform
off-white background (palette 1). Avatar `avatar_l3` placed with
anchor at logical cell `(2, 2)`, rotation 0. Target slot
`target_slot_l_rot270` placed at logical cell `(12, 12)`. No
pickups, no rotation-lock cells.

The L's 4 rotations (cell offsets relative to anchor; anchor at
(0,0); 90° CW formula `(x, y) → (-y, x)`):
- rot 0: A(0,0), B(-1,0), C(-1,1) — "B east-of body, C south-of B"
- rot 90: A(0,0), B(0,-1), C(-1,-1)
- rot 180: A(0,0), B(1,0), C(1,-1)
- rot 270: A(0,0), B(0,1), C(1,1) — target shape for L1

**Mechanics required by the witness** (N = 2):

- **M1 — Walking**: ACTION1/2/3/4 translates the polyomino by 1
  logical cell in that cardinal direction; rejected if any body
  cell (anchor included) would collide with a wall or fall
  off-grid.
- **M2 — Rotating-self**: ACTION5 rotates the polyomino 90° CW
  about the anchor cell; rejected if any post-rotation body cell
  would collide with a wall or fall off-grid.

**Necessity per mechanic**:

- L1 cannot be solved without triggering M1 because the avatar's
  anchor starts at (2, 2) and the target slot's anchor is at
  (12, 12); the anchor needs to move by `(+10, +10)` cells and
  only ACTION1..4 translate the polyomino. No "rotation about a
  non-anchor cell" alternative exists.
- L1 cannot be solved without triggering M2 because the avatar
  starts at rotation 0 and the target slot's silhouette is the
  L at rotation 270; rotations 0, 90, 180 all map to silhouettes
  distinct from the target's. ACTION5 is the only verb in
  `available_actions` that changes rotation. The target slot's
  cell coordinates (12,12), (12,13), (13,13) coincide with the
  avatar's cells only at rotation 270 (cells A(0,0), B(0,1),
  C(1,1) relative).

**Witness solution** (23 actions, anchor and rotation evolve):

```
[ACTION4]×10  (anchor 2→12 east, rotation stays 0,
               body cells stay west and south-west of anchor)
[ACTION2]×10  (anchor (12,2)→(12,12) south)
[ACTION5]×3   (rotation 0→90→180→270; final cells
               (12,12), (12,13), (13,13) match target slot)
```

After each action, the win predicate `_check_win()` compares the
avatar's current cell set to the target slot's cell set; equality
fires `self.next_level()` on action 23.

**Difficulty justification** (per `difficulty-rules.md` § 2):

- **(a) Random-resistance**: a uniformly random action sequence
  has near-zero chance of (i) navigating to (12, 12) without
  running out of steps AND (ii) firing ACTION5 exactly 3 times
  at the end (not in the middle, which would force re-rotations
  that may collide with walls along the south corridor). The
  probability is bounded above by `(1/5)^(23) ≈ 3.4e-17` for any
  fixed-length path, vanishingly small.
- **(b) Human-tractable**: an attentive human reads the avatar's
  L-shape and the target's L-shape outline from the static
  initial frame, attempts a walk, discovers ACTION5 rotates the
  avatar (visual feedback: orange anchor-pixel pivots), and
  solves in ~1-2 minutes.
- **(c) Planning depth**: NO STRICT PLANNING REQUIREMENT for L1
  (per `difficulty-rules.md` § 2c L1 guidance). The whole
  difficulty is discovering the rotate-self verb; once
  understood, the walk-then-rotate sequence is trivial to
  execute.
- **(d) Step budget**: **`step_budget = 50`** (generous over the
  23-action witness; leaves ample room to explore the rotate
  verb early without running out).

### Level 2 — base system + 1 new mechanic

**Layout**: outer wall ring (rows/cols 0 and 15). Playfield rows
1..14, cols 1..14 open. Avatar `avatar_l3` placed with anchor at
`(2, 2)`, rotation 0. Growth pickup `growth_pickup` placed at
`(4, 2)`. Target slot `target_slot_j_rot180` placed with anchor at
`(12, 12)` — cells `{(12,12), (13,12), (13,11), (13,13)}`.

The 4-cell J's rotations (after pickup, the avatar's relative
cells become A(0,0), B(-1,0), C(-1,1), D(-1,-1) in rotation 0;
the D cell is the new fourth):

- rot 0: A(0,0), B(-1,0), C(-1,1), D(-1,-1) — shape `D/BA/C-`
- rot 90: A(0,0), B(0,-1), C(-1,-1), D(1,-1) — shape `CBD/.A.`
- rot 180: A(0,0), B(1,0), C(1,-1), D(1,1) — shape `.C/AB/.D` ← target
- rot 270: A(0,0), B(0,1), C(1,1), D(-1,1) — shape `.A./DBC`

**Mechanics required by the witness** (N+1 = 3; L2 introduces 1
new mechanic):

- **M1 — Walking** (carried from L1)
- **M2 — Rotating-self** (carried from L1)
- **M3 — Growth-pickup consumption** (new): when the anchor cell
  coincides with a `growth_pickup` sprite's cell, the pickup is
  consumed (visual: pickup sprite becomes invisible / `REMOVED`),
  and the avatar acquires a 4th cell at relative offset `(-1, -1)`
  from the anchor. The rotation is preserved across the growth
  event. After consumption, all subsequent rotations operate on
  the 4-cell J (about the same anchor cell).

**Necessity per mechanic**:

- L2 cannot be solved without triggering M1 because the avatar's
  anchor must travel from (2, 2) to (12, 12) (10 east + 10
  south), and only ACTION1..4 translate the polyomino.
- L2 cannot be solved without triggering M2 because the target
  slot's silhouette is the 4-cell J at rotation 180, and the
  avatar (after pickup) is at rotation 0; only ACTION5 changes
  rotation. The J's rotations 0, 90, 270 produce different
  cell-sets, none matching the target's
  `{(12,12),(13,12),(13,11),(13,13)}`.
- L2 cannot be solved without triggering M3 because the target
  slot has 4 cells and the avatar starts the level with 3 cells
  (the 3-cell L). The win predicate requires the avatar's cell
  set equals the target slot's cell set — a 3-cell set can never
  equal a 4-cell set. The ONLY way to gain a 4th cell is to walk
  the anchor onto the pickup at (4, 2); the pickup is the unique
  4th-cell source on the level.

**Witness solution** (22 actions):

```
[ACTION4]×2   (anchor (2,2)→(4,2); on entering (4,2) the
               pickup is consumed, avatar becomes 4-cell J at
               rotation 0 with new cell D at (3,1))
[ACTION4]×8   (anchor (4,2)→(12,2))
[ACTION2]×10  (anchor (12,2)→(12,12))
[ACTION5]×2   (rotation 0→90→180; final cells
               {(12,12),(13,12),(13,11),(13,13)} match target)
```

**Difficulty justification**:

- **(a) Random-resistance**: with 6 active actions on average and
  a 22-action witness, random-policy success probability is
  bounded above by `(1/6)^(22) ≈ 7.8e-18`. The pickup acquisition
  step is also a non-trivial constraint — random play that skips
  cell (4, 2) never grows the avatar.
- **(b) Human-tractable**: ~2 minutes. The human reads the
  pickup's distinct green-and-yellow sprite as "consumable",
  walks onto it once, observes the new body cell appearing
  upper-left of the anchor (visual feedback: a 4th red+maroon
  cell sprite appears), then composes walk + rotate as in L1.
- **(c) Planning depth**: MODERATE planning required
  (post-discovery). With every mechanic understood, the
  fully-informed player still faces:
  - **Post-discovery decision space at level start**: 4 valid
    first actions (ACTION1 blocked by wall, but ACTION2/3/4 all
    geometrically legal at (2,2); ACTION5 legal; the player
    must choose between them). Count = 4. Reasoning chain: the
    pickup is at (4, 2) east of the start; rotating before
    pickup would put the avatar in rotation 90+ which still has
    cells in the upper region — the player must reason about
    whether reaching the pickup is more efficient before vs.
    after rotation. Witness reasoning: walking east to consume
    pickup first is shorter (no wasted rotations) than rotating
    first then walking; the witness commits east first.
  - **Plausible-but-wrong alternative**: rotate twice immediately
    at (2, 2) to reach rotation 180, then walk east. This walk
    is geometrically blocked because at rotation 180 the body
    extends to col anchor+1; the body cells will collide with
    walls in narrow spots (none on this open L2 level, but the
    pickup still needs to be consumed). Crucially, rotating
    BEFORE consuming the pickup means the post-pickup growth
    direction is the same (rel (-1, -1) in CURRENT rotation), so
    the post-rotation pickup-growth lands at a DIFFERENT
    absolute cell than the witness's pre-rotation growth — the
    final J-shape doesn't match the target slot. The
    fully-informed player must realise pickup-direction is
    rotation-dependent and pre-pickup rotation breaks the plan.
- **(d) Step budget**: **`step_budget = 60`** (generous over the
  22-action witness; allows the player several wasted moves to
  explore the pickup before committing).

### Level 3 — system + 1 new mechanic

*(Revision pass #1: this section was rewritten after
`critique-revisions.md` flagged the previous M4 = "rotation-lock"
as not strictly counterfactually necessary. The new M4 is
"pivot-reset" — see `critique-revisions.md` for the full
diagnosis.)*

**Layout**: 16×16 grid; outer wall ring (rows/cols 0 and 15).
Internal layout deliberately kept SIMPLE so M4's geometric
necessity (silhouette type) is the load-bearing planning
challenge — not maze navigation. A pair of small isolated wall
clusters at `(8, 5)..(8, 6)` (2 cells) and `(13, 6)..(13, 7)`
(2 cells) provides modest pathing texture without constraining
the witness route.

Concrete sprite placements:

- Avatar `avatar_l3` with anchor at logical `(3, 3)`, rotation 0.
  Body cells at `(2, 3)` and `(2, 4)`.
- Growth pickup `growth_pickup` placed at `(5, 3)`.
- Decorative wall clusters at `(8, 5)`, `(8, 6)`, `(13, 6)`,
  `(13, 7)`.
- Pivot-reset cell `pivot_reset` placed at `(10, 10)`.
- Target slot `target_slot_t_b_pivot_rot90` placed such that the
  T-silhouette's cells are `{(12, 12), (12, 13), (11, 12),
  (13, 12)}` — anchor (B-pivot) at `(12, 12)` for the B-pivot
  rotation-90 cell layout (B at (0,0), A at (0,1), C at (-1,0),
  D at (1,0) — relative to the new B-anchor at (12, 12)).

**The 4-cell J's silhouettes by pivot and rotation** (relative
cells, with anchor at (0, 0); cell letters are: A = original
anchor, B = pickup-time east-of-A body cell — wait, B is at
(-1, 0) relative to A in rot 0; C = (-1, 1); D = (-1, -1)):

A-pivot relative cells (default after M3 consumption):
- rot 0: A(0,0), B(-1,0), C(-1,1), D(-1,-1) — `D./BA/C.`
- rot 90 CW: A(0,0), B(0,-1), C(-1,-1), D(1,-1) — `CBD/.A.`
- rot 180: A(0,0), B(1,0), C(1,-1), D(1,1) — `.C/AB/.D`
- rot 270: A(0,0), B(0,1), C(1,1), D(-1,1) — `.A./DBC`

After M4 (pivot-reset) consumption, anchor designation transfers
from A to B; the relative-cells list re-baselines as:

B-pivot relative cells:
- rot 0: B(0,0), A(1,0), C(0,1), D(0,-1) — vertical T pointing up:
  ```
  . D .
  B A .
  . C .
  ```
  (cells: B(0,0), A(1,0) east, C(0,1) south, D(0,-1) north)
- rot 90 CW: B(0,0), A(0,1), C(-1,0), D(1,0) — horizontal T pointing south:
  ```
  C B D
  . A .
  ```
  (cells: B(0,0), A(0,1) south, C(-1,0) west, D(1,0) east) ← target shape
- rot 180: B(0,0), A(-1,0), C(0,-1), D(0,1) — vertical T pointing down
- rot 270: B(0,0), A(0,-1), C(1,0), D(-1,0) — horizontal T pointing north

**Critical observation**: the A-pivot J's 4 silhouettes ALL have a
"L-shape" or "J-shape" character (an asymmetric piece with one
"hook" cell). NONE of the A-pivot silhouettes is a T (which has
3-cell line + 1 perpendicular cell). The target slot's silhouette
is a T (4-cell, with one cell perpendicular to a 3-cell line).
Therefore the target slot is **geometrically unreachable** from
the A-pivot J at any rotation or position. The avatar MUST switch
to the B-pivot (via M4) to ever produce a T silhouette.

**Mechanics required by the witness** (M-count = L2-count + 1 = 4;
L3 introduces 1 new mechanic):

- **M1 — Walking** (carried from L1/L2)
- **M2 — Rotating-self** (carried from L1/L2)
- **M3 — Growth-pickup consumption** (carried from L2)
- **M4 — Pivot-reset** (new): when the avatar's anchor cell enters
  a `pivot_reset` sprite's cell, the anchor designation transfers
  to the cell at the current rotation-0 relative offset `(-1, 0)`
  (the B cell). The relative-cells list is re-baselined so that
  B becomes the new (0, 0) anchor and the prior A becomes
  (1, 0). The pivot-reset sprite is consumed (set to
  `InteractionMode.REMOVED`). Visually: the orange-centre
  anchor-marker migrates to the new anchor cell.

**Necessity per mechanic**:

- L3 cannot be solved without triggering M1 because the avatar's
  anchor must travel from `(3, 3)` to `(12, 12)` — a Manhattan
  distance of `9+9 = 18` cells — and only ACTION1..4 translate.
  No rotation or pivot-reset alone moves the anchor; only walking
  does.
- L3 cannot be solved without triggering M2 because the target
  silhouette is the B-pivot T at rotation 90 — the B-pivot's
  rotations 0, 180, 270 produce DIFFERENT T-orientations (cells
  in different absolute positions) that do not match the target
  slot's specific cell set. Only the B-pivot rotation 90 produces
  the cells `{(0,0), (0,1), (-1,0), (1,0)}` matching the target
  at anchor (12, 12). Therefore the witness must press ACTION5
  at least once after the pivot-reset to advance the B-pivot
  rotation from 0 to 90.
- L3 cannot be solved without triggering M3 because the target
  has 4 cells; the avatar starts with 3. The pickup at `(5, 3)`
  is the unique 4th-cell source in the level. Without the
  pickup, the avatar is a 3-cell L and can never match a 4-cell
  target.
- L3 cannot be solved without triggering M4 because the target
  silhouette is a T-shape (3-in-line + 1 perpendicular). Per the
  "Critical observation" above, the A-pivot J's 4 rotations are
  all L/J-shaped (asymmetric) — none of them is a T. Therefore
  the avatar's cell set at any A-pivot rotation cannot equal
  the target's cell set, REGARDLESS of where the anchor sits on
  the playfield. The ONLY way to produce a T-silhouette is to
  switch to the B-pivot via M4. The pivot-reset cell at
  `(10, 10)` is the unique pivot-reset source on the level.
  Without consuming this cell, M4 is never triggered and the
  target is geometrically unreachable.

**Witness solution** (20 actions):

```
[ACTION4]×2   (anchor (3,3)→(5,3); on entering (5,3) the pickup
               is consumed, avatar becomes 4-cell A-pivot J at
               rotation 0; new D cell appears at (4, 2))
[ACTION4]×5   (anchor (5,3)→(10,3); body cells stay west of
               anchor and span rows 2..4)
[ACTION2]×7   (anchor (10,3)→(10,10); on entering (10,10) the
               pivot-reset is consumed, anchor designation
               transfers from A to B. Pre-reset, anchor at
               (10,10), body at (9,10) (was B), (9,11) (was C),
               (9,9) (was D). Post-reset, anchor at (9,10)
               (now B), body at (10,10) (now A), (9,11) (still
               C), (9,9) (still D))
[ACTION5]×1   (rotation 0→90 in the B-pivot frame; cells
               become B(9,10), A(9,11), C(8,10), D(10,10) →
               absolute cells {(9,10), (9,11), (8,10), (10,10)})
[ACTION4]×3   (anchor (9,10)→(12,10); body cells slide east)
[ACTION2]×2   (anchor (12,10)→(12,12); final cells
               {(12,12), (12,13), (11,12), (13,12)})
```

Final cell set: `{(12,12), (12,13), (11,12), (13,12)}`. Target
slot cells: `{(12,12), (13,12), (11,12), (12,11)}`. **WAIT** —
these do not match! Let me re-verify the B-pivot rotation 90
cells.

Let me re-derive. B-pivot rot 0 relative cells:
B(0,0), A(1,0), C(0,1), D(0,-1).

Applying 90° CW formula `(x, y) → (-y, x)` to each non-anchor cell:
- A: (1, 0) → (0, 1)
- C: (0, 1) → (-1, 0)
- D: (0, -1) → (1, 0)

B-pivot rot 90 relative cells: B(0,0), A(0,1), C(-1,0), D(1,0).

At anchor (12, 12):
- B at (12, 12)
- A at (12, 13)
- C at (11, 12)
- D at (13, 12)

Cells: `{(12,12), (12,13), (11,12), (13,12)}`.

Target slot must be specified at these same cells.

**Target slot final specification**: 4-cell T silhouette with the
B-pivot anchor cell at logical `(12, 12)` and dim outline cells at
`{(12,12), (12,13), (11,12), (13,12)}`. Pixel drawing: the slot
sprite spans 3 cols (cols 11-13) × 2 rows (rows 12-13), occupying
12×8 display pixels. Pattern uses palette 3 (grey) outline with
`-1` interior.

**Difficulty justification**:

- **(a) Random-resistance**: 6 active actions, 20-action witness,
  random-policy probability `(1/6)^20 ≈ 2.7e-16`. The pivot-reset
  cell is a single-use one-shot — a random player who walks over
  it without intending to is "wasted" the pivot, and if the
  player then can't navigate to the target with the new pivot
  state, restart is the only recourse (running out the step
  budget). Furthermore, M4's silhouette-changing effect is
  geometrically gated: 75% of A-pivot rotation states are
  meaningless for the target (only the B-pivot rot 90 matches).
- **(b) Human-tractable**: ~2-3 minutes. The player reads the
  pickup as consumable (distinct green-yellow pattern), walks
  onto it, observes the new D body cell appear. Then encounters
  the pivot-reset cell (distinct magenta-cross pattern), walks
  onto it, observes the orange-centre marker migrate to the
  formerly-B cell. Then experiments with ACTION5 in the new
  pivot frame to discover the T-shape rotations.
- **(c) Planning depth**: **CHALLENGING even for an attentive
  human** (post-discovery). With every mechanic understood, the
  fully-informed player faces:
  - **Post-discovery decision space at level start**: 4 valid
    first actions at anchor (3, 3) — ACTION1 (north, body cells
    move to row 2 — ok), ACTION2 (south, body to row 4, ok),
    ACTION3 (west, body cell to col 1 = open, ok), ACTION4
    (east, body stays at col 2, ok). ACTION5 is geometrically
    legal but produces a different L-orientation; whether to
    use it pre-pickup is a real decision. Effective decision
    space: 5. Strictly ≥ L2's 4. ✓
  - **Trivial heuristic that fails**: *"rotate the avatar to
    match the target orientation as soon as possible, then walk
    to the target slot."* A fully-informed player who knows the
    target is a T-shape might think: "I should rotate to find
    the right shape first." They press ACTION5 repeatedly in
    the A-pivot frame, cycling through all 4 A-pivot J
    rotations and finding NONE of them is a T. The heuristic
    fails because the answer is not in the A-pivot's rotation
    space; the player must instead realise M4's role.
  - **Where the heuristic diverges from the witness**: at the
    pivot-reset cell. A heuristic player following "rotate to
    match" would never realise that stepping onto the
    pivot-reset cell *changes the pivot frame*, opening a new
    rotation space (B-pivot) whose rotations DO include a T.
    The witness's reasoning chain: consume pickup → walk to
    pivot-reset → step on it (M4 fires) → ACTION5 rotates in
    the new B-pivot frame → walk to target. Greedy "match the
    shape" players will run out of step budget cycling A-pivot
    rotations.
- **(d) Step budget**: **`step_budget = 80`** (generous over the
  20-action witness; allows ~60 actions of exploratory mistakes,
  including cycling A-pivot rotations before discovering M4's
  effect. Strictly ≥ L2's 60 per the no-shrink rule.)

## 5. Action mapping

The subset of `[1..7]` used: `[1, 2, 3, 4, 5]` (the avatar walks
with cardinal arrows and rotates with ACTION5; no clicks, no
undo).

- `ACTION1`: translate the polyomino 1 cell UP (decrement anchor
  y by 1, all body cells follow). Rejected if any post-move body
  cell is at a wall sprite or outside the 16×16 grid.
- `ACTION2`: translate 1 cell DOWN. Same rejection rule.
- `ACTION3`: translate 1 cell LEFT. Same rejection rule.
- `ACTION4`: translate 1 cell RIGHT. Same rejection rule.
- `ACTION5`: rotate the polyomino 90° clockwise about the current
  anchor cell (which may be A or B, depending on whether
  pivot-reset has been triggered this level). Rejected if any
  post-rotation body cell would be at a wall sprite or outside
  the grid. Rejected actions still consume one step from the
  step budget.

No context-dependent gating beyond the move/rotate validity
checks above. Every action is always *attemptable*; the engine
silently no-ops invalid moves (after decrementing the step
counter). The pivot-reset effect (M4) is triggered passively
when the anchor steps onto a `pivot_reset` cell — it is not a
separate action.

## 6. HUD and per-game state

**HUD widget**: `StepCounterOverlay(RenderableUserDisplay)` paints
row 63 (bottom row) of the frame: the leftmost `current * 64 /
max` pixels in palette 14 (green), the rest in palette 4
(off-black). Updated each `step()` based on the level's
`step_budget` data field and the action count since level start.

**Per-game state**:

- `self.avatar_anchor: tuple[int, int]` — the anchor cell's
  logical position `(col, row)`.
- `self.avatar_rotation: int` — current rotation index 0..3
  (multiples of 90°).
- `self.avatar_cells: set[tuple[int, int]]` — set of absolute
  logical cell positions the polyomino currently occupies; the
  win predicate is `self.avatar_cells == target_cells` (set
  equality).
- `self.avatar_relative_cells: list[tuple[int, int]]` — the
  polyomino's cells in relative-to-anchor coordinates at rotation
  0; updated when M3 (pickup consumption) appends a new cell.
- `self.pivot_reset_cells: set[tuple[int, int]]` — per-level cache
  of un-consumed pivot-reset cell positions, populated in
  `on_set_level`. When the anchor enters one, the cell is removed
  from this set AND the corresponding sprite is set to
  `InteractionMode.REMOVED`.
- `self.anchor_index: int` — index into `self.avatar_relative_cells`
  identifying which cell is currently the anchor. Starts at 0
  (cell A). Pivot-reset sets it to 1 (cell B); a re-baseline
  reorders the list so that index 0 is again the anchor.
- `self.target_cells: set[tuple[int, int]]` — per-level cache of
  target-slot cell positions, populated in `on_set_level` from
  the `target` sprite's pixel pattern + position.
- `self.step_budget`, `self.step_remaining`: int, decremented
  every action.
- `self.pickup_cells: set[tuple[int, int]]` — per-level cache
  of un-consumed pickup positions.

The avatar's render sprite is rebuilt each rotation by
`np.rot90(base_pixels, k=self.avatar_rotation)` and re-positioned
so the anchor's pixel offset within the sprite-pixel grid lands
at `(self.avatar_anchor[0] * 4, self.avatar_anchor[1] * 4)` in
the camera frame.

**Hidden state** returned by `_get_hidden_state()`: a small array
packing `(step_remaining, avatar_rotation, len(avatar_cells),
len(pickup_cells_remaining))` so the engine's frame+hidden-state
graph hash distinguishes states that render identically (e.g.
the avatar at the same anchor cell with rotation 0 vs rotation
180 in cases where the rotation is symmetric and the rendered
silhouette happens to be the same).

## 7. Win condition

After every action, `_check_win()` is called:

```
def _check_win(self) -> bool:
    return self.avatar_cells == self.target_cells
```

If True, `self.next_level()` fires. After L3 wins,
`next_level()` advances past the last level and the engine
auto-calls `self.win()`.

The predicate is *set equality* — both the cell coordinates and
the cell count must match exactly. A 3-cell avatar overlapping
3 of a 4-cell slot's cells does NOT win.

## 8. Lose condition

`_check_lose()` is called after every action:

```
def _check_lose(self) -> bool:
    return self.step_remaining <= 0 and not self._check_win()
```

If True, `self.lose()` fires. Step budget exhaustion is the only
lose path; the avatar cannot get "stuck" in a state where the win
is unreachable, because no action is irreversible: rotations are
4-cyclic (any rotation can be returned to by 3 more ACTION5s),
walking is invertible (just walk back), and pickups, once
consumed, leave the avatar in a strictly more capable state
(4-cell with growth direction fixed; the player can still rotate
the 4-cell J to match any target J-silhouette). The growth-
pickup IS irreversible in the sense that the avatar can't shrink
back to 3 cells, but the only L1 target is a 3-cell L (no pickup
exists at L1), so this doesn't matter. At L2 and L3, the target
is a 4-cell J — pickup consumption is *required*, so consuming
it can never make the win unreachable.

## 9. Novelty note

### Closest reference taxonomy entries

- **cn04 (rotate-translate-jigsaw)**: click-select then arrow-move
  then ACTION5-rotate selected pieces on a flat board; win is
  pixel-level connector-snap between pairs of pieces. **hb5n
  distinguishing rule**: no selection model, no multi-piece
  board, no connector-snap; the avatar is the only mobile
  polyomino, walks through a maze, and wins by silhouette-equals-
  slot. The ACTION5 verb rotates the AVATAR'S OWN body, not a
  selected piece's body.

- **ar25 (reflection-rotation-fit)**: click-select + arrow-move
  + ACTION5-rotate + reflector lines that mirror-copy. **hb5n
  distinguishing rule**: no reflectors, no mirror-copies; single
  concrete polyomino, no shadow counterpart.

- **tu93 (lockstep-multi-maze)**: arrow keys move every primary
  agent in lockstep, secondary species tick autonomously. **hb5n
  distinguishing rule**: single avatar, no lockstep multi-agent
  dynamic, no autonomous secondary species. The defining new
  verb is rotation-of-self, which tu93 lacks entirely.

- **None of the 25 reference games' walking avatars rotate
  themselves** (ACTION5 in walking games is reserved for
  pour/commit/lock/cycle per `skills/global/action-enum.md`).
  hb5n is the first to assign ACTION5 the semantic
  "rotate-the-avatar's-body".

### Closest prior-games entries

- **xv4n (cavity-nest-fit)**: ACTION6 click-lift, click-drop;
  ACTION5 rotates held piece; fit silhouettes into cavities by
  placement (teleportation, no walking). **hb5n distinguishing
  rule**: no clicks (`available_actions = [1, 2, 3, 4, 5]`); no
  lift/drop verb; the polyomino IS the player, walks the maze
  cell-by-cell.

- **zw91 (inflate-fit-burst)**: single avatar whose footprint
  cycles 3 discrete SQUARE sizes (1×1, 2×2, 3×3); ACTION5
  grows/pushes/bursts; goal is fitting the square avatar into a
  same-size socket. **hb5n distinguishing rule**: irregular
  polyomino (L and J), not squares; ACTION5 rotates rather than
  resizes; size change comes from one-shot pickups (M3), not a
  cycle.

- **nz3v (rotor-pivot-walk)**: 2×2 square avatar walks; ACTION5
  rotates the world's lit *wedge* (a separate sprite), not the
  avatar. **hb5n distinguishing rule**: irregular polyomino
  (not square), ACTION5 rotates the AVATAR (rigid body), not a
  wedge; no "safe-in-lit-sector" predicate. M4 (pivot-reset) is
  unique to hb5n — nz3v has no pivot-cell-transfer mechanic.

- **pv5q (pivot-rod-swing)**: a pawn at the end of a rigid
  radial rod attached to a fixed stake; ACTION5 swings or
  extends the rod, and a separate verb swaps anchor between
  multiple STAKE sprites placed on the playfield. **hb5n
  distinguishing rule**: the avatar is a 2D polyomino (not a
  1D rod anchored at one end); the pivot is one of the avatar's
  OWN CELLS (not a separate stake sprite); the pivot transfer
  happens by WALKING onto a pivot-reset cell (a passive trigger,
  not an active ACTION5 verb). pv5q's swap is an active
  ACTION5-style command on a discrete stake graph; hb5n's
  pivot-reset is a one-shot environmental consumable.

- **pz4t (anchor-pivot-place)**: click-set-anchor then
  arrow-reflect + ACTION5-rotate to tile a flat region. **hb5n
  distinguishing rule**: no click-anchor verb; no tiling goal;
  the avatar is a single walking polyomino, not multiple
  placed components.

- **nb6t (hinge-chain-reach)**: three hinged rod-segments,
  per-segment rotate/extend/cycle. **hb5n distinguishing rule**:
  single rigid polyomino, no hinges, no per-segment selection.

- **lt7m (L-jump-tour-block)**: avatar makes L-shaped knight
  jumps. **hb5n distinguishing rule**: the L-shape is the
  avatar's BODY, not its MOVE shape; the avatar walks 1 cell
  at a time, not in L-jumps.

**Verdict (per the negative-similarity-check walkthrough in
`mechanic-pick.md`)**: NOVEL — no single reference or prior shares
3+ of the 8 negative-similarity dimensions with hb5n. The core
dynamic ("thread a rigid irregular polyomino through narrow gaps
by walking + rotating the avatar's own body") is fresh against
both the 25-game taxonomy and the 81-entry prior-games index +
9 untracked recent priors.
