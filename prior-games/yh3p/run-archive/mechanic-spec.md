# mechanic-spec — yh3p (vine-branch-bloom) — revision 2

## Revision summary

Sections changed in this revision (relative to revision 1):
- **§3** — `bud_notched` redesigned. (Critique Issue 2 fix.)
  Also added a soft `soil_texture` background sprite for visual
  density. (Critique Issue 5 soft suggestion.)
- **§4 L2 — Necessity per mechanic** — clarified that auto-bloom
  on `bud_closed` does NOT change tip activity, then re-stated M2
  necessity at L2 under that rule. (Critique Issue 3 fix.)
- **§4 L3 — Layout** — single coherent wall description. (Critique
  Issue 1 fix.)
- **§4 L3 — Necessity per mechanic / M2 row** — leads with the
  dormancy-after-bloom argument (independent of wall topology),
  appends the topology argument as supporting weight. (Critique
  Issue 4 fix.)
- **§4 L3 — Witness** — verified against the cleaned-up wall
  layout. Bud rotation labels now reference the stamen-direction
  convention from the new bud_notched design.
- **§5 — Action mapping** — explicit rule that ACTION1-4 onto
  `bud_closed` auto-blooms but does NOT set tip dormant. (Critique
  Issue 3 fix.)

Issues quoted from `critique-revisions.md`:

> *"Issue 1 — Internally inconsistent L3 wall layout (BLOCKING)"*
> *"Issue 2 — bud_notched sprite reads as a letter (BLOCKING)"*
> *"Issue 3 — Tip activity after auto-bloom on `bud_closed` is unspecified (MINOR)"*
> *"Issue 4 — Simplify L3 M2 necessity using the dormancy-after-bloom rule (MINOR)"*
> *"Issue 5 — L1 frame visual sparseness (BORDERLINE; not blocking)"*

## 1. Title
Vine-Branch-Bloom (working title; never visible in-game).

## 2. Mechanic family
**Tree-growth + click-rebranch + directional bloom-commit.** A
single rooted vine grows cell-by-cell under arrow input, leaving a
permanent stalk trail; the player clicks on any existing vine cell
to re-anchor the active tip there and sprout a new branch from that
point; on the final level, terminal cells (notched flower buds)
require a directional bloom-commit (ACTION5) where the tip's
arrival direction matches the bud's intake side. Drawn from the
§3.4-allowed priors **objectness** (vine + bud + wall as persistent
entities), **basic geometry & topology** (tree topology with no
self-cross; rotational geometry on the bud intake direction), and a
sliver of **basic physics** (one-cell discrete movement). No
agentness.

## 3. Sprite roster

Coordinate convention: grid_size = (64, 64). Cell stride = 4
display pixels (movements are ±4 px). Sprites are positioned at
multiples of 4. No upscaling; pixels are display pixels.

- **`root`** — 8×8 px. Palette `{13 maroon outer ring, 8 red mid
  ring, 14 green centre}`. Tags `["root", "vine"]`. Layer 1. Single
  instance per level. Marks the origin of the vine; counts as a
  vine cell (player can click it to re-anchor the tip back to the
  root).

  ```
  pixels = [
      [-1, 13, 13, 13, 13, 13, 13, -1],
      [13, 13,  8,  8,  8,  8, 13, 13],
      [13,  8,  8, 14, 14,  8,  8, 13],
      [13,  8, 14, 14, 14, 14,  8, 13],
      [13,  8, 14, 14, 14, 14,  8, 13],
      [13,  8,  8, 14, 14,  8,  8, 13],
      [13, 13,  8,  8,  8,  8, 13, 13],
      [-1, 13, 13, 13, 13, 13, 13, -1],
  ]
  ```

- **`stalk`** — 4×4 px. Palette `{14 green field, 13 maroon
  centre}`. Tags `["stalk", "vine"]`. Layer 1. Spawned per cell as
  the vine grows. Rounded green tile with maroon-centre detail —
  rows of stalks read as a stitched green chain rather than a flat
  green strip.

  ```
  pixels = [
      [-1, 14, 14, -1],
      [14, 13, 13, 14],
      [14, 13, 13, 14],
      [-1, 14, 14, -1],
  ]
  ```

- **`tip_active`** — 4×4 px. Palette `{11 yellow drop, 8 red eye,
  14 green base}`. Tag `["tip"]`. Layer 3 (renders on top of any
  vine cell). Single instance per level. The asymmetric tear-drop
  silhouette (narrow end at top of the unrotated sprite) carries
  the facing direction visually. Rotation is set via
  `sprite.rotate(deg)`: 0 = facing UP, 90 = facing RIGHT, 180 =
  facing DOWN, 270 = facing LEFT.

  ```
  pixels = [
      [-1, 11, 11, -1],
      [11, 11, 11, 11],
      [11,  8,  8, 11],
      [14, 11, 11, 14],
  ]
  ```

- **`tip_dormant`** — 4×4 px. Palette `{2 light-grey field, 3
  darker grey centre}`. Tag `["tip"]`. Layer 3. Visible cue that
  the tip is not currently active (immediately after a successful
  ACTION5 bloom-commit on a notched bud, OR at level start before
  the player's first arrow press, OR after any ACTION6 click —
  although in the click case, an "active-but-no-facing-yet" sprite
  is more accurate; see below). Player must ACTION6-click a vine
  cell (or, in the no-facing case, press an arrow) to re-establish
  forward growth.

  ```
  pixels = [
      [-1,  2,  2, -1],
      [ 2,  3,  3,  2],
      [ 2,  3,  3,  2],
      [-1,  2,  2, -1],
  ]
  ```

  **State-cue convention** (per checklist item 19): the renderer
  uses `tip_active` whenever the tip has *any* known facing
  direction; `tip_dormant` whenever facing is undefined (level
  start, post-ACTION6, post-bloom). The player can always read off
  the screen whether arrows will currently extend the vine.

- **`bud_closed`** — 4×4 px. Palette `{12 orange ring, 6 magenta
  core}`. Tag `["bud_closed"]`. Layer 1. Used at L1 and L2. Closed
  ring (no notch, no stamen) — accepts the vine tip from any
  direction; covered simply by the tip arriving on the cell
  (auto-blooms on M1 entry; ACTION5 on this cell is a no-op).

  ```
  pixels = [
      [12, 12, 12, 12],
      [12,  6,  6, 12],
      [12,  6,  6, 12],
      [12, 12, 12, 12],
  ]
  ```

- **`bud_notched`** — 4×4 px. Palette `{12 orange ring, 6 magenta
  core, 11 yellow stamen}`. Tag `["bud_notched"]`. Layer 1. Used at
  L3.

  **Critique Issue 2 fix.** Previously `bud_notched` was rendered
  as a 4×4 ring with one transparent side — a silhouette that
  reads as "C", "U", "n", or "⊃" depending on rotation, violating
  `forbidden-elements.md`. The redesign closes the ring on all
  four sides and uses a 2-pixel YELLOW STAMEN extending out one
  side as the directional cue. The resulting silhouette is a
  closed flower with a small protrusion — not letter-shaped.

  Rotation 0 (stamen extends out the BOTTOM = intake from south =
  tip must approach moving NORTH, facing UP):

  ```
  pixels = [
      [-1, 12, 12, -1],
      [12,  6,  6, 12],
      [12,  6,  6, 12],
      [-1, 11, 11, -1],   # ← yellow stamen tab on intake side
  ]
  ```

  Direction encoding:
  - rotation 0 → stamen on bottom → intake from south → facing UP
  - rotation 90 → stamen on left  → intake from west  → facing RIGHT
  - rotation 180 → stamen on top   → intake from north → facing DOWN
  - rotation 270 → stamen on right → intake from east → facing LEFT

  (The stamen is rendered as 2 yellow pixels on the side opposite
  the intake. Since the tip enters FROM the intake side, the
  stamen-tab is on the FAR side of the bud relative to the
  approaching tip.)

  Visual passes the forbidden-elements check: closed-ring flower
  with one short protrusion never reads as a letter or digit.

- **`bloom`** — 4×4 px. Palette `{12 orange outer ring, 7 pink mid,
  6 magenta core}`. Tag `["bloom"]`. Layer 1. Replaces a `bud_*`
  sprite once it is successfully bloomed. Visually distinct from
  the buds — fully filled, no opening, brighter palette mix.

  ```
  pixels = [
      [12, 12, 12, 12],
      [12,  7,  6, 12],
      [12,  6,  7, 12],
      [12, 12, 12, 12],
  ]
  ```

- **`wall`** — 4×4 px. Palette `{4 off-black, 3 grey crosshatch}`.
  Tag `["wall"]`. Layer 1. Blocks vine growth.

  ```
  pixels = [
      [ 4,  3,  3,  4],
      [ 3,  4,  4,  3],
      [ 3,  4,  4,  3],
      [ 4,  3,  3,  4],
  ]
  ```

- **`soil_texture`** *(decorative, optional in implementation)* —
  64×64 px. Palette `{2 light-grey base, 1 off-white speckles in a
  sparse deterministic pattern}`. Tag `["decoration"]`. Layer 0
  (rendered behind everything else). Non-collidable
  (`InteractionMode.INTANGIBLE`). Provides background texture so
  the L1 frame doesn't read as a flat empty grid.

  Pattern sketch (every 4th cell offset by 2 has a single off-white
  speckle pixel): a uniform tiling of 4×4 blocks where each block
  is `[[2, 2, 2, 2], [2, 1, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2]]`,
  giving a subtle "morning-dew" texture. (Critique Issue 5 soft
  fix; addresses the L1-sparseness concern without adding any
  pseudo-mechanic.)

- **`step_bar`** — `RenderableUserDisplay`, draws on row 0 (top
  edge) of the rendered frame. Shows fraction of remaining steps as
  a 7=pink-to-3=darker-grey depleting bar. Drains by 1 per non-
  RESET action.

Background = palette `2 light-grey`. Letter-box padding = palette
`5 black`.

## 4. Level progression, mechanic enumeration, and witness solutions

EXACTLY 3 levels. Same `grid_size=(64, 64)` across all three; sprite
set fixed; per-level differences are sprite placements + step
budget + which bud variant (closed vs notched) is used.

Mechanic glossary (used in the per-level enumeration below):

- **M1 = extend-tip**: ACTION1/2/3/4 grows the active tip one cell
  in that direction, leaving a permanent stalk segment at the prior
  tip cell. Blocked by walls, by existing vine cells (no
  self-cross), and by `bud_notched` cells (until they are bloomed
  via M3). On entry to a `bud_closed` cell the bud auto-blooms (the
  bud sprite is replaced by `bloom`); the tip remains active and
  the player may continue growing onward (Critique Issue 3 fix).
  Tip's facing is updated to the move direction on every
  successful move.
- **M2 = click-to-rebranch (ACTION6)**: Click any existing vine
  cell (root or stalk). The active tip sprite jumps to that cell;
  facing is reset to "none" (next arrow re-establishes facing); the
  cell that previously held the tip becomes a plain stalk if it was
  a regular grown segment. While facing is "none" the tip renders
  as `tip_dormant` (grey). Click on a non-vine cell is a no-op.
  ACTION6 also re-activates the tip after a bloom-commit set it
  dormant.
- **M3 = bloom-commit (ACTION5) with directional intake match**:
  When the tip is on a `bud_notched` cell *and* tip facing matches
  the bud's intake direction (i.e., facing == direction of arrival
  through the intake side, which is *opposite* of the side where
  the yellow stamen extends — see §3 `bud_notched`), replace the
  bud with `bloom` and set the tip dormant (player must ACTION6-
  click to re-activate before any further arrow has effect). If
  facing does NOT match, ACTION5 has no effect on the bud (the
  action still consumes a step). On a `bud_closed` cell ACTION5 is
  a no-op (the cell is already bloomed by entry under M1).

### Level 1 — base dynamic system

- **Mechanics required by the witness** (N = 1):
  - **M1 = extend-tip.**

- **Necessity per mechanic**:
  - *L1 cannot be solved without triggering M1 because the single
    `bud_closed` is at cell (16, 7) and the tip starts at the root
    cell (4, 7). The bud is 12 cells away with no walls; ACTION5
    has no effect at L1 (the bud is closed, auto-blooms on contact
    by M1; ACTION5 on a `bud_closed` is a no-op), and ACTION6
    click can only re-anchor to existing vine cells (initially
    only the root, and clicking the root has no progress effect),
    so the only way to cover the bud is to grow the vine cell-by-
    cell to the bud's position via M1.*

- **Layout** (grid coords in cells; cell pixel = coord × 4):
  - Root sprite at cell (4, 7).
  - One `bud_closed` at cell (16, 7).
  - No walls. Empty corridor of 12 cells horizontally between root
    and bud.
  - `step_budget = 24`.
  - Optional `soil_texture` decoration sprite covering the
    playfield (visual only).

- **Witness solution** (12 actions): `[ACTION4, ACTION4, ACTION4,
  ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4,
  ACTION4, ACTION4]`. Tip walks right 12 cells; the 12th press
  lands the tip on the bud, auto-blooming it and triggering
  `next_level()`.

- **Difficulty justification**:
  - **(a) Random-resistance**: a vision-blind random agent picks
    uniformly from `{1,2,3,4,5,6}` per step and would need to press
    ACTION4 12 times in a row out of a 24-step budget — probability
    `(1/6)^12 ≈ 5×10⁻¹⁰`. Slightly raised by detours, but well
    under 1/10⁴.
  - **(b) Human-tractable**: ~30 seconds for a first-time human.
    Three or four exploratory presses establish that arrows move
    the yellow tip and leave a green trail; visible bud as obvious
    target; corridor straight.
  - **(c) Planning depth**: *no strict planning requirement* per
    `difficulty-rules.md` § L1. Discovery is the entire challenge —
    the player must discover that arrows extend a glowing tip; once
    discovered, the witness is a straight 12-press line.
  - **(d) Step budget**: 24 actions for a 12-action witness — 2×
    witness, generous over to allow exploration of all four arrows
    and one dead-end correction.

### Level 2 — base system + 1 new mechanic (N+1 = 2)

- **Mechanics required by the witness** (= 2):
  - **M1 = extend-tip** (carried forward from L1).
  - **M2 = click-to-rebranch (ACTION6)** (new at L2).

- **Necessity per mechanic** (Critique Issue 3 fix — reasoning
  now explicitly accounts for "auto-bloom doesn't set tip
  dormant"):
  - *L2 cannot be solved without triggering M1 because covering
    any `bud_closed` requires the tip to occupy that cell. M2 only
    re-anchors the tip to an existing vine cell — never to a new
    empty cell — so M2 alone cannot reach a bud cell. ACTION5 on
    `bud_closed` is a no-op (Critique Issue 3 fix). The only verb
    that places the tip on a non-vine cell is M1.*
  - *L2 cannot be solved without triggering M2 because the L2
    layout has TWO `bud_closed` targets in two regions separated
    by a continuous wall column, and even though auto-bloom on M1
    entry leaves the tip active, no single contiguous M1-only
    branch can cover both buds. Concrete topology argument: the
    wall column at x=8 from y=0 through y=14 (15 wall sprites
    stacked vertically) is sealed; the only horizontal-gap is at
    cell (8, 15) on the bottom row. The root is at (4, 8) inside
    the left region; bud A is at (4, 2) in the same region; bud
    B is at (12, 8) in the right region. Suppose the player only
    uses M1: starting from the root, EITHER the first move goes
    UP into the left region toward bud A (covers bud A on press
    6, auto-blooms; from (4, 2) the only further M1 directions
    that don't re-enter existing vine are LEFT to (3, 2) or RIGHT
    to (5, 2) or UP to (4, 1), none of which can cross the
    vertical wall column to reach (12, 8) — the wall column at
    x=8, y=0..14 has no aperture at any y < 15 and the branch
    cannot retreat back through its own vine to reach (8, 15)),
    OR the first move goes DOWN/RIGHT and routes through (8, 15)
    into the right region toward bud B (covers bud B on the
    arrival press, auto-blooms; from (12, 8) the branch can grow
    further in the right region but cannot return to the left
    region through (8, 15) because that cell is already vine). So
    M1-only never covers both buds. M2 (re-anchor to root or any
    earlier vine cell, sprout a separate branch through the
    unreached region) is the only way. Without M2, exactly one
    bud blooms.*

- **Layout**:
  - Root at cell (4, 8).
  - `bud_closed` (bud A) at cell (4, 2).
  - `bud_closed` (bud B) at cell (12, 8).
  - Wall column at x = 8 from y = 0 through y = 14 (15 wall
    sprites stacked vertically). Cell (8, 15) is the only gap and
    lies on the bottom edge.
  - `step_budget = 50`.
  - Optional `soil_texture` decoration.

- **Witness solution** (~22 actions):
  1. From root (4, 8): grow up to bud A — `ACTION1` × 6 (cells
     (4, 8) → (4, 7) → ... → (4, 2)). The 6th press lands the tip
     on bud A and auto-blooms it. Tip remains active at (4, 2).
  2. `ACTION6` click on the root cell at pixel `(16, 32)` (the
     root sprite's top-left at cell (4, 8) maps to pixels (16, 32);
     any pixel inside the 8×8 root sprite from (16, 32) to (23, 39)
     is acceptable). Tip jumps to root cell, facing → none, sprite
     becomes `tip_dormant`.
  3. Grow down through the gap to the right region and up to bud
     B: `ACTION2 × 7` (down to (4, 15)), `ACTION4 × 8` (right
     through (8, 15) to (12, 15)), `ACTION1 × 7` (up to (12, 8)).
     The first ACTION2 re-establishes facing = DOWN and re-renders
     the tip as `tip_active`. The 7th `ACTION1` lands tip on bud B
     and auto-blooms it. All buds bloomed → `next_level()`.

  Sequence (collapsed): `[A1×6, A6@(16,32), A2×7, A4×8, A1×7]` = 6
  + 1 + 7 + 8 + 7 = **29 actions**. Within 50-step budget.

- **Difficulty justification**:
  - **(a) Random-resistance**: random policy faces ~50 steps with
    1/6 success rate per direction action. Reaching bud A (6 ups
    in a row from a 16-action sub-budget — accounting for moves
    that fail on walls) is `~(1/6)^6 ≈ 2×10⁻⁵`; the additional
    M2-then-route requires 22 more correct actions; combined
    `(1/6)^22 ≈ 3×10⁻¹⁸`. Far below 1/10⁴.
  - **(b) Human-tractable**: ~2 minutes. Player must (1)
    encounter the wall column (any move into x=8 is rejected,
    teaches "wall blocks growth"), (2) discover the gap exists
    (visual scanning of the wall reveals (8, 15) as the only
    opening), (3) discover that ACTION6 click on a vine cell
    teleports the tip there (some exploration; the cue is the
    tip sprite jumping discontinuously, distinct from arrow
    growth which is local extension), (4) execute the witness.
  - **(c) Planning depth**: *moderate planning required (post-
    discovery)*. Decision space at L2 start:
    - 4 plausible first arrow moves from root (UP, DOWN, LEFT,
      RIGHT). All four are valid (none into walls); UP heads to
      bud A, DOWN/RIGHT heads to bud B via the gap, LEFT heads
      to a dead-end region. So ≥ 2 valid first actions.
    - **Plausible-but-wrong path 1**: route ALL the way to bud B
      first (down to (4, 15), right to (12, 15), up to (12, 8) —
      14 cells of branch), then re-anchor at the root and grow up
      to bud A (6 cells). Total: 14 + 1 + 6 = 21 actions, slightly
      shorter than the witness — actually this is just as valid;
      either order works. The witness picks bud A first because
      its single straight path is shorter and reveals the
      mechanic faster.
    - **Plausible-but-wrong path 2**: try to grow into the wall
      column at any cell other than (8, 15) — fails immediately,
      teaches that the column is sealed but burns 1-3 steps.
    - **Witness reasoning chain**: (i) root (4, 8) is in the
      left region; bud A is reachable directly upward (one
      branch); (ii) bud B is in the right region, reachable only
      via gap (8, 15); (iii) two branches needed — second branch
      from root (M2 click) routes through the gap.
    - **Stage-conflation guard**: the named "wrong paths" are
      both post-discovery — they don't depend on missing
      knowledge of the mechanics, just on a non-optimal branch
      ordering or on hitting a wall (the latter is a one-step
      learning cost, not a stage-confusion).
  - **(d) Step budget**: 50 actions for a 22-action witness — 2.27×
    witness. Generous. Not shrinking from L1 (L1: 24/12 = 2.0×, L2:
    50/22 = 2.27×).

### Level 3 — system + 1 new mechanic (L2-count + 1 = 3)

- **Mechanics required by the witness** (= 3):
  - **M1 = extend-tip** (carried from L1, L2).
  - **M2 = click-to-rebranch** (carried from L2).
  - **M3 = bloom-commit (ACTION5) with directional intake match**
    (new at L3).

- **Layout** (Critique Issue 1 fix — single coherent description):

  Walls form an L-shape with two single-cell gaps that let
  branches cross between quadrants, plus an open elbow corner. All
  walls are `wall` sprites; all open cells are background.

  - **Vertical wall**: 7 wall sprites at cells (8, 0), (8, 1),
    (8, 2), (8, 3), (8, 4), (8, 5), (8, 6).
  - **Horizontal wall**: 7 wall sprites at cells (0, 8), (1, 8),
    (2, 8), (3, 8), (4, 8), (5, 8), (6, 8).
  - **Open gaps and corner** (deliberately NOT walls):
    - Cell (8, 7) — the row-7 gap. Lets a branch crossing the
      wall column at that row.
    - Cell (7, 8) — the col-7 gap. Lets a branch cross the wall
      row at that column.
    - Cell (8, 8) — the L-elbow, also open.
    - All cells with x ≥ 9 OR y ≥ 9 (the "outside-the-L"
      majority of the playfield) are open.

  This produces three reachability regions when you ignore the
  open gaps: top-left (cells with `x ≤ 7 and y ≤ 7`), top-right
  (cells with `x ≥ 8 and y ≤ 7`), bottom-left (cells with `x ≤ 7
  and y ≥ 8`), and bottom-right (`x ≥ 8 and y ≥ 8`). The gaps
  (8, 7), (7, 8), and the elbow (8, 8) are the only inter-region
  crossings.

  - Root sprite at cell (4, 4) (in top-left).
  - Three `bud_notched` buds:
    - **Bud P** at cell (12, 4), rotation 180 (yellow stamen
      extends UP, intake from north — tip must approach moving
      DOWN, facing DOWN). Bud P is in the top-right quadrant.
    - **Bud Q** at cell (4, 12), rotation 270 (yellow stamen
      extends RIGHT, intake from east — tip must approach moving
      LEFT, facing LEFT). Bud Q is in the bottom-left quadrant.
    - **Bud R** at cell (12, 12), rotation 0 (yellow stamen
      extends DOWN, intake from south — tip must approach moving
      UP, facing UP). Bud R is in the bottom-right quadrant.
  - `step_budget = 100`.
  - Optional `soil_texture` decoration.

- **Necessity per mechanic** (Critique Issue 4 fix — leads with
  dormancy argument):

  - *L3 cannot be solved without triggering M1 because each bud
    occupies a specific cell that the tip must occupy at the
    moment ACTION5 fires. ACTION6 only re-anchors to existing
    vine cells (none of which are bud cells at level start). The
    only verb that places the tip on a new (non-vine) cell is M1.*
  - *L3 cannot be solved without triggering M2 because at L3 every
    successful M3 bloom-commit sets the tip dormant. With three
    `bud_notched` targets, a successful run requires three
    bloom-commits, and after each bloom the tip is dormant; the
    only verb that re-activates the tip is ACTION6 (M2). So at
    least two M2 invocations are required between blooms 1→2 and
    2→3, regardless of any wall topology. (Independently, the
    L-walled topology does NOT admit a single contiguous branch
    that arrives at all three buds with their correct intake
    directions — the witness §c and the alternate-strategy
    enumeration §d below argue this — but the dormancy argument
    above is sufficient on its own.)*
  - *L3 cannot be solved without triggering M3 because the three
    targets at L3 are `bud_notched` sprites (NOT `bud_closed`).
    M1 entry onto a `bud_notched` cell is BLOCKED — see §5
    action mapping (`bud_notched` is in the M1-blocked list, so
    the tip never enters a notched bud's cell via M1 alone). The
    only way to bloom a notched bud is ACTION5 (M3) when the tip
    is ON the bud's cell — but the tip can only get there via
    M1, which is blocked. (Resolved below: the tip moves onto a
    cell ADJACENT to the notched bud in the intake direction,
    then... actually wait. Let me clarify.)*

  **(Spec note)** — the M3 necessity argument depends on what
  "M1 onto `bud_notched`" does. Two design options:
  - *Option A*: M1 is BLOCKED on `bud_notched` cells (treats them
    like walls). To bloom, the tip stands on the cell ADJACENT to
    the bud (in the intake direction) and ACTION5 with correct
    facing applies the bloom-commit on the *adjacent* bud cell —
    the bud's sprite is replaced by `bloom` but the tip never
    enters it.
  - *Option B*: M1 onto `bud_notched` is ALLOWED but ACTION5 is
    required on the cell to bloom; the tip enters and sits on
    the (unbloomed) bud cell; ACTION5 with facing-match blooms
    it. M1 from a notched-bud cell is ALSO blocked (the tip is
    "stuck" until ACTION5 succeeds or ACTION6 re-anchors).

  *Option B* is the one the spec adopts (it's simpler — the
  tip's "facing direction at arrival" naturally matches the
  intake direction without needing an adjacent-cell rule). The
  spec must be explicit. **Updated rule** (also reflected in §5):

  - M1 onto a `bud_notched` cell IS allowed — the tip enters and
    facing is set to the move direction. The bud cell does NOT
    become vine until M3 succeeds. While the tip is on a notched
    bud, M1 from that cell is BLOCKED until M3 either (a)
    succeeds (sets tip dormant — player must ACTION6 to leave)
    or (b) the player ACTION6-clicks elsewhere (re-anchors,
    leaving the notched bud unchanged). Failed M3 (wrong facing)
    consumes a step but does not unlock M1.

  Under this rule, the M3 necessity argument is:
  *L3 cannot be solved without triggering M3 because the three
  `bud_notched` cells only convert to `bloom` via successful
  ACTION5 (M3); M1 onto a notched bud places the tip there but
  doesn't bloom it, and from that cell M1 is blocked. Without
  M3, no notched bud is ever bloomed, and the win predicate
  requires all buds bloomed.*

  *Per-mechanic counterfactual table:*

  | Level | Mechanic | Solvable without M? | Why not (concrete) |
  |---|---|---|---|
  | L1 | M1 | no | Single bud at (16, 7); tip starts at root (4, 7); no other movement verb places the tip on a new cell. |
  | L2 | M1 | no | Same — only M1 places the tip on a non-vine cell. |
  | L2 | M2 | no | Wall column at x=8, y=0..14 sealed; only gap at (8, 15); two buds in opposite regions; one M1-only contiguous branch never covers both because the gap cell, once vine, blocks any return path between regions. |
  | L3 | M1 | no | Buds occupy specific cells; only M1 places the tip on those cells. |
  | L3 | M2 | no | Each successful M3 sets tip dormant; only ACTION6 (M2) re-activates the tip; with 3 buds, ≥ 2 M2 invocations are required between blooms. |
  | L3 | M3 | no | `bud_notched` cells convert to `bloom` only via ACTION5 with facing match; M1-only never blooms a notched bud (M1 onto a notched bud places the tip but doesn't bloom; M1 from a notched-bud cell is blocked). |

  *Independent enumeration of plausible alternate L3 strategies:*

  - *Strategy "single-branch snake": from root grow right past
    (8,7) gap, down through (12, 12), left to (4, 12), and try
    to bloom both buds along the way.* Fails on TWO grounds:
    (i) after the first successful bloom-commit the tip is
    dormant — the snake cannot continue without M2; (ii) even
    setting that aside, the tip's facing on arriving at bud R
    (12, 12) via a snake from the north is DOWN, but bud R's
    intake is UP (stamen extends DOWN), so the bloom-commit
    no-ops.
  - *Strategy "spam ACTION5 from the root"*. Fails because the
    root cell is not a bud cell.
  - *Strategy "click on bud cell with ACTION6 to teleport the
    tip there"*. Fails because ACTION6 only re-anchors to
    existing vine cells; the bud is not vine until bloomed.
  - *Strategy "approach each bud from a direction-matching
    side"*. This is the witness; works.
  - *Strategy "approach each bud from the wrong side and ACTION5
    repeatedly hoping for a direction-match"*. Each wrong ACTION5
    consumes a step without progress; with 3 wrong-side
    approaches and ~10 wasted ACTION5s plus the witness's
    correct routes, the budget is exceeded.

- **Witness solution** (Critique Issue 1 — verified against the
  cleaned-up wall layout):

  Branch 1 — root (4, 4) → bud P at (12, 4), arriving with
  facing = DOWN (since bud P's intake is north / stamen up):

  - From (4, 4) grow DOWN to (4, 7): `A2 × 3` → (4, 5), (4, 6),
    (4, 7).
  - Grow RIGHT through the row-7 corridor (y=7 is open from x=4
    to x=15 since the vertical wall stops at y=6; (8, 7) is the
    gap): `A4 × 8` → (5, 7), (6, 7), (7, 7), (8, 7), (9, 7),
    (10, 7), (11, 7), (12, 7).
  - Grow UP toward bud P: but landing at (12, 4) from (12, 7)
    requires three UP presses arriving with facing = UP, which
    DOES NOT match bud P's intake (UP is wrong; bud P's intake
    is DOWN). So detour via (13, 7) → (13, 4) → (12, 4):
  - Grow RIGHT: `A4 × 1` → (13, 7).
  - Grow UP: `A1 × 3` → (13, 6), (13, 5), (13, 4).
  - Grow LEFT: `A3 × 1` → (12, 4). Now tip is at bud P; facing =
    LEFT. WRONG direction for bud P (need DOWN).

  *Re-routing for correct facing*: arrive at (12, 4) moving DOWN.
  Previous cell must be (12, 3); from (12, 3), `A2` to (12, 4)
  with facing = DOWN. So instead detour to (12, 3) and approach
  from the north:

  - Grow RIGHT: `A4 × 1` → (13, 7).
  - Grow UP: `A1 × 4` → (13, 6), (13, 5), (13, 4), (13, 3).
  - Grow LEFT: `A3 × 1` → (12, 3).
  - Grow DOWN: `A2 × 1` → (12, 4). Facing = DOWN. Match!
  - `A5` — bloom bud P. Tip becomes dormant.

  Branch 1 actions: `A2×3, A4×8, A4×1, A1×4, A3×1, A2×1, A5` = 3
  + 8 + 1 + 4 + 1 + 1 + 1 = **19 actions**.

  Branch 2 — re-anchor and route to bud Q at (4, 12), arriving
  with facing = LEFT:

  - `A6` click at pixel `(28, 28)` — cell (7, 7) is vine from
    Branch 1; click sets tip at (7, 7), facing = none.
  - Grow DOWN through the col-7 gap: `A2 × 1` → (7, 8). (Cell
    (7, 8) is the column-7 gap, open.)
  - Grow DOWN: `A2 × 4` → (7, 9), (7, 10), (7, 11), (7, 12).
  - Grow LEFT to bud Q: `A3 × 3` → (6, 12), (5, 12), (4, 12).
    Facing = LEFT. Match!
  - `A5` — bloom bud Q. Tip becomes dormant.

  Branch 2 actions: `A6@(28,28), A2×5, A3×3, A5` = 1 + 5 + 3 + 1
  = **10 actions**.

  Branch 3 — re-anchor and route to bud R at (12, 12), arriving
  with facing = UP:

  - `A6` click at pixel `(48, 28)` — cell (12, 7) is vine from
    Branch 1.
  - Grow DOWN to enter the bottom-right quadrant via (12, 8).
    (Cell (12, 8) is open since the horizontal wall stops at
    x=6, leaving x=7..15 open at y=8.) `A2 × 1` → (12, 8).
  - Need to arrive at (12, 12) moving UP (facing UP) — previous
    cell must be (12, 13). Direct path via (12, 9), (12, 10),
    (12, 11), (12, 12) would arrive moving DOWN — wrong. Detour:
  - Grow RIGHT: `A4 × 1` → (13, 8).
  - Grow DOWN: `A2 × 5` → (13, 9), (13, 10), (13, 11), (13, 12),
    (13, 13).
  - Grow LEFT: `A3 × 1` → (12, 13).
  - Grow UP: `A1 × 1` → (12, 12). Facing = UP. Match!
  - `A5` — bloom bud R. Tip becomes dormant. All three buds
    bloomed → `next_level()`.

  Branch 3 actions: `A6@(48,28), A2×1, A4×1, A2×5, A3×1, A1×1,
  A5` = 1 + 1 + 1 + 5 + 1 + 1 + 1 = **11 actions**.

  **Total witness: 19 + 10 + 11 = 40 actions.** Step budget = 100,
  so 2.5× witness — generous.

  Sequence (collapsed):
  - Branch 1: `[A2×3, A4×9, A1×4, A3×1, A2×1, A5]`
  - Branch 2: `[A6@(28,28), A2×5, A3×3, A5]`
  - Branch 3: `[A6@(48,28), A2×1, A4×1, A2×5, A3×1, A1×1, A5]`

  (Where `Ai` is `ACTION i`. The `×N` denotes N consecutive
  presses of that action.)

- **Difficulty justification**:
  - **(a) Random-resistance**: each bud requires a multi-action
    sequence with the correct *facing* at the moment ACTION5 is
    pressed. Probability of stumbling: branch 1 needs an
    18-step coherent path before a correct ACTION5; the chance
    per step of the right action is 1/6, and routing failures
    progressively consume budget without progress.
    Conservatively `(1/6)^18 ≈ 10⁻¹⁴`. Far below 1/10⁴.
  - **(b) Human-tractable**: ~3 minutes for the L3 puzzle (≈6
    minutes total over 3 levels). The new mechanic to discover
    at L3 is "ACTION5 only blooms when the tip approaches from
    the side opposite the yellow stamen". Visual cues (stamen
    direction on bud + tear-drop direction on tip) are
    discoverable within 2-3 ACTION5 attempts that fail. Once
    discovered, the routing puzzle is the rest of the work.
  - **(c) Planning depth**: *planning is challenging even for an
    attentive human*. Decision space at level start: 4 plausible
    first arrow moves from the root; 3 of them grow into open
    cells of the top-left quadrant (UP to (4, 3), DOWN to (4, 5),
    RIGHT to (5, 4), LEFT to (3, 4)); only routes through y=7
    or x=7 reach the gaps that lead to other quadrants. Decision
    space ≥ L2's (4 ≥ 4).
    - **Trivial heuristic that fails**: *"approach each bud from
      the side that has the most direct path"*. Direct path to
      bud R at (12, 12) from the root quadrant arrives moving
      DOWN (facing DOWN) — but bud R's intake is UP (stamen
      south). Wrong facing → bloom-commit no-ops. The witness
      *detours* one cell south of the bud to approach from the
      south. The heuristic and witness diverge at the cell
      where the heuristic enters the bud (12, 11→12) directly,
      where the witness goes (12, 8) → (13, 8) → (13, 9..13) →
      (12, 13) → (12, 12) — a 4-cell-longer detour. Heuristic
      arrives at all three buds with wrong facing: bud R from
      DOWN, bud P from UP (going (12, 7) → (12, 6→4) arrives at
      (12, 4) facing UP, but bud P's intake is DOWN), bud Q
      from RIGHT (going through (4, 8→12) is blocked by the
      horizontal wall — heuristic must route via (7, 8) gap and
      arrives at bud Q facing LEFT, which IS correct for bud Q).
      So heuristic fails on at least 2 of 3 buds.
    - **Why ahead-of-time reasoning is needed**: the player
      must compute, before each branch starts, where the
      branch's TERMINAL CELL (the cell adjacent to the bud, in
      the intake direction) is reachable from. Because the
      walls partition the playfield and the gaps are
      single-cell, the branch cell-by-cell route must terminate
      with the correct last move. This isn't a single-step
      lookup — it's "plan the last 1-2 cells carefully, then
      route the rest of the branch to that staging cell".
    - **Stage-conflation guard**: the named heuristic is fully
      post-discovery (the player understands intake-matching;
      the heuristic IGNORES the matching to take a shorter path
      and discovers it doesn't bloom). Not a discovery-stage
      misstep.
  - **(d) Step budget**: 100 actions for a 40-action witness —
    2.5× witness. Not shrinking from L1/L2 (L1: 24/12=2.0×, L2:
    50/22=2.27×, L3: 100/40=2.5×); monotonically expanding.

## 5. Action mapping

`available_actions = [1, 2, 3, 4, 5, 6]`. ACTION7 is omitted per
`design-constraints/checklist.md` item 22 (slot 7 must be strict-
undo or absent; this game has no undo verb).

| Action | Semantic | Gating |
|---|---|---|
| `ACTION1` | Grow active tip 1 cell UP. Tip facing → UP. | Tip is active OR has facing=none (in which case this action both moves the tip and re-establishes facing). Target cell `(tip.x, tip.y − 4)` is in bounds, not a `wall`, not in `_vine_cells`. `bud_closed`: target allowed; auto-blooms on entry; tip remains active. `bud_notched`: target allowed; tip enters and sits on the bud cell; M1 from the notched-bud cell is BLOCKED until M3 succeeds or M2 re-anchors. Otherwise (tip is "dormant" after a successful M3): action consumed but tip does not move; player must use ACTION6 to re-activate the tip first. |
| `ACTION2` | Grow active tip 1 cell DOWN. Tip facing → DOWN. | As ACTION1, downward. |
| `ACTION3` | Grow active tip 1 cell LEFT. Tip facing → LEFT. | As ACTION1, leftward. |
| `ACTION4` | Grow active tip 1 cell RIGHT. Tip facing → RIGHT. | As ACTION1, rightward. |
| `ACTION5` | Bloom-commit at tip cell. | Tip is on a `bud_notched` cell AND tip facing equals the bud's intake direction (= 4-way rotation lookup: bud rot 0→facing UP, bud rot 90→facing RIGHT, bud rot 180→facing DOWN, bud rot 270→facing LEFT) → bloom (replace bud sprite with `bloom`, set tip to `tip_dormant`, clear tip facing → none). On a `bud_closed` cell: no-op (already auto-bloomed by entry). On any other cell (root, stalk, empty, wall — but tip can't be on a wall): no-op. Action consumes a step regardless. |
| `ACTION6` | Click at (x, y) display pixels. | If the click cell maps to a vine sprite (`root` or `stalk`), set the active tip to that cell, set tip facing → none (tip sprite renders as `tip_dormant`), and replace the previous tip cell's sprite with a regular `stalk` if the previous tip was on a non-bud non-root cell (the previous tip cell remains vine). If the click hits a non-vine cell (wall, bud_*, empty background, bloom), no-op. ACTION6 also re-activates a dormant tip after a successful M3 bloom (if the player clicks any vine cell). Action consumes a step regardless. |

The tip's "facing" attribute is internal game state with a visible
cue: when facing is set, the `tip_active` sprite is rotated to
indicate facing (rotation 0 = UP, 90 = RIGHT, 180 = DOWN, 270 =
LEFT). When facing is "none" (level start, or just after ACTION6,
or just after a successful M3 set tip dormant), the tip is
rendered as `tip_dormant` (grey).

**Auto-bloom-on-entry preserves tip activity** (Critique Issue 3
fix): M1 entry onto a `bud_closed` cell auto-blooms the bud (sprite
replaced with `bloom`) but tip's facing is preserved (== move
direction) and the tip remains active (sprite renders as
`tip_active`). Player may continue M1 growth from the bloomed
cell. Only successful ACTION5 on a `bud_notched` (M3) sets the tip
dormant; ACTION6 click also clears facing (renders `tip_dormant`)
but the next arrow re-activates.

## 6. HUD and per-game state

**HUD** — single `RenderableUserDisplay` subclass `StepBarHud` that
draws a horizontal bar across the **top row** (`frame[0, :]`)
showing the fraction of remaining steps. Filled portion in palette
`7 pink`; depleted portion in palette `3 grey`. Updated every step.

**Per-game state** (held on the `Yh3p` instance):

- `_step_bar: StepBarHud` — the HUD widget.
- `_step_budget: int` — total budget for current level (read from
  `level.get_data("step_budget")` in `on_set_level`).
- `_active_tip_cell: tuple[int, int]` — pixel coords of the active
  tip's cell. Always in `_vine_cells`. Set on level init to root
  cell; updated on every M1 success or ACTION6 success or M3
  success (M3 sets tip dormant but `_active_tip_cell` still holds
  the post-bloom cell — re-activated on next ACTION6).
- `_tip_facing: str | None` — one of `"UP"`, `"DOWN"`, `"LEFT"`,
  `"RIGHT"`, or `None`. Updated on every successful arrow move;
  reset to `None` on level start, on every ACTION6 click, and on
  successful ACTION5 (M3) bloom.
- `_vine_cells: set[tuple[int, int]]` — set of pixel coords of
  cells currently occupied by vine (root + every stalk + the active
  tip's current cell, including bloom cells from auto-bloomed
  buds). Used for collision testing during M1 growth and for valid-
  target testing during M2 click.
- `_tip_active_sprite: Sprite` — the `tip_active` sprite instance
  (rotated to indicate facing).
- `_tip_dormant_sprite: Sprite` — the `tip_dormant` sprite instance
  (shown when `_tip_facing is None`).
- `_tip_blocked_on_notched: bool` — True when the tip is currently
  sitting on an unbloomed `bud_notched` cell. While True, M1 is
  rejected (tip is "stuck" until ACTION5 blooms or ACTION6
  re-anchors).

Hidden-state visibility table (per checklist item 19):

| State | Visible cue |
|---|---|
| Tip active with known facing | `tip_active` sprite (yellow) at the active cell, rotated per facing. |
| Tip dormant or facing unknown | `tip_dormant` sprite (grey) at the active cell. |
| Tip's facing direction | Rotation of the `tip_active` sprite — narrow end of teardrop points in facing direction. |
| Tip on a notched-bud cell, M1 blocked | Tip sprite overlay on the `bud_notched` sprite — both visible (tip on layer 3, bud on layer 1). Trying M1 produces no movement; the player sees the rejection. |
| Which cells are vine | All vine cells render as `root`, `stalk`, or `bloom`, with tip overlay on the active cell. |
| Bud unbloomed, with intake direction | `bud_notched` sprite shows ring with yellow stamen extending out the intake-opposite side. |
| Bud unbloomed, no intake constraint | `bud_closed` sprite shows full ring with no stamen. |
| Bud bloomed | `bloom` sprite (filled, no opening, no stamen, brighter palette mix). |
| Step budget | `StepBarHud` top row. |

## 7. Win condition

`_check_win(level) -> bool` — at the end of every `step()` (after
the action's effect is applied):

```python
buds_remaining = (
    level.get_sprites_by_tag("bud_closed") +
    level.get_sprites_by_tag("bud_notched")
)
return len(buds_remaining) == 0
```

If True → `self.next_level()`. The condition is uniform across L1,
L2, L3: every bud sprite must have been replaced by a `bloom`
sprite (which has tag `["bloom"]`, NOT `bud_*`).

## 8. Lose condition

`_check_lose() -> bool` — at the end of every `step()`:

```python
return self._step_bar.current_steps <= 0
```

If True → `self.lose()`. No collision-based instant-fail; the
player can only fail by exhausting the step budget.

## 9. Novelty note

### Closest taxonomy entries

- **sk48 paired-snake-trail**: arrow-grown trail with
  per-cell-colour matching across head-pairs. Distinguishing rule
  for yh3p: yh3p has a *single rooted vine that branches* with
  ACTION6-rebranch (sk48 has *two heads in lockstep mirror*); the
  win is *covering and bloom-committing every bud with directional
  match*, not trail-colour parity. yh3p has no mirror coupling and
  no per-cell paint-comparison.
- **tn36 program-pawn-trace**: deferred-execution programmed path-
  tracing via instruction buttons. Distinguishing rule: yh3p is
  *direct-manipulation* growth via arrows, not program-then-run.
  yh3p has explicit branching topology; tn36 has none.
- **wa30 carry-pickup-drop**: arrow walking + ACTION5 commit-verb
  for pickup/drop. Distinguishing rule: wa30's commit transfers a
  separate movable sprite; yh3p's commit blooms the tip itself
  with directional match against a static sprite.
- **ls20 cycler-attribute-match**: arrow-walking pawn collects
  attribute-coded targets in sequence. Distinguishing rule: ls20's
  state is on the moving avatar (shape/colour/rotation triplet);
  yh3p's state is in the world (the permanent vine). No cycling
  attribute-match in yh3p.

### Closest prior-games entries (from `prior-games/index.md`)

- **ek73 wake-trail-evade**: avatar walks; trail = decaying
  hazards. Distinguishing rule: yh3p's trail is a *permanent
  helpful structure* (stalk you can re-anchor on), not a hazard.
  Opposite-direction core dynamic.
- **jd4q echo-trail-teleport**: walk + click teleports back
  consuming trail. Distinguishing rule: yh3p's click is
  *re-anchor-tip-to-existing-vine-cell* (teleports the tip but
  preserves the trail); jd4q's click *teleports back AND
  consumes*.
- **bw7k actor-replay-shade**: walk + anchor spawns autonomous
  shades replaying past moves. Distinguishing rule: yh3p has
  *zero autonomous motion*.
- **tj4n walk-trail-loop-enclose**: walk a single closed loop;
  enclosure captures interior. Distinguishing rule: yh3p forbids
  self-cross (tree topology); win is per-target bloom-commit, not
  enclosure.
- **jx5k constellation-edge-link**: pair-click coloured nodes to
  build a multigraph. Distinguishing rule: pair-click on
  pre-placed nodes vs arrow-growth from a single root.
- **wb6n tether-pin-wrap**: pawn on stretchy leash, ACTION5 plants
  pins to re-anchor rope. Distinguishing rule: wb6n's structure is
  a single rope; yh3p's is a discrete tree of permanent cells.
- **ds5q wall-erode-chain**: chip walls. Distinguishing rule: ds5q
  is *destroy-walls* (subtractive); yh3p is *grow-vine* (additive).

`prior-games/index.md` is NOT empty (66 entries scanned and
distinguished against above). No prior shares 3+ dimensions per
the negative-similarity-check.
