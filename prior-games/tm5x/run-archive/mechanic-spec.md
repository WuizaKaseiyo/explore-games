# mechanic-spec — tm5x

## 1. Title

Aura-Imprint Polarity Stamp (working title; not visible in-game).

## 2. Mechanic family

`thermal-aura-imprint` — a single pawn carries a polarity (hot
or cold) and imprints a thermal value on its current cell and the
four cardinally-adjacent cells; the player walks the pawn so that
every target ring's underlying cell reads the target's required
temperature **at some point in the run** (the target latches once
satisfied). The pawn may toggle its polarity (ACTION5) to cover
both hot and cold targets in the same level. Insulating walls (L3)
block both pawn movement and the aura.

Core-knowledge priors used (per
`design-constraints/core-knowledge-priors.md`):

- **Objectness** — pawn, targets, walls are coherent persistent
  objects.
- **Basic physics** — heat-aura around an active source is a
  recognisable physical analogue (a brazier, an ice block); the
  aura's plus-shape models a real, intuitive locality.
- **Basic geometry & topology** — at L3, walls partition the
  field; the player reasons about connected sub-regions of the
  reachable space and which polarity the pawn must hold when it
  enters each region.

## 3. Sprite roster

- **`temperature_field`** — 64×64 sprite at position (0, 0), tag
  `"thermal_field"`, layer -1 (drawn behind everything else).
  Its pixels are recomputed every step by the game class from
  the integer temperature grid `self._temperature` of shape
  (16, 16). Each thermal-cell at coords (cx, cy) renders as a
  4×4 pixel block at display position (4·cx, 4·cy) with one of
  five internal **chamfered-tile** patterns (solid centre + corner
  accent — no diagonals; the corner-accent design avoids any
  resemblance to letters such as X, per `forbidden-elements.md`):
  - `-2` (deep cold): `[[10, 4, 4, 10], [4, 4, 4, 4], [4, 4, 4, 4], [10, 4, 4, 10]]` — solid off-black with light-blue corner accents.
  - `-1` (cool): `[[0, 10, 10, 0], [10, 10, 10, 10], [10, 10, 10, 10], [0, 10, 10, 0]]` — solid light-blue with white corner accents.
  - `0` (neutral): `[[1, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 1]]` — solid white with off-white corner accents.
  - `+1` (warm): `[[0, 7, 7, 0], [7, 7, 7, 7], [7, 7, 7, 7], [0, 7, 7, 0]]` — solid pink with white corner accents.
  - `+2` (hot): `[[7, 8, 8, 7], [8, 8, 8, 8], [8, 8, 8, 8], [7, 8, 8, 7]]` — solid red with pink corner accents.
  Internal pattern variation (corner accents, not flat fill)
  satisfies `checklist.md` item 20 (no chunky uniform-colour
  blocks). The chamfered design reads visually as "tile" not as
  "letter".
- **`pawn_hot`** — 4×4 sprite, tag `"player"`, layer 2.
  `[[5, 8, 8, 5], [8, 7, 7, 8], [8, 7, 7, 8], [5, 8, 8, 5]]` —
  black-bordered red avatar with a uniform-pink (palette 7)
  inner 2×2. No diagonal pattern — the inner 2×2 is solid pink,
  the four corners are solid black (palette 5), the outer 8 cells
  of the border are solid red (palette 8). Reads as a small
  bordered icon. The pink inner-fill is the hot-polarity cue.
- **`pawn_cold`** — 4×4 sprite, tag `"player"`, layer 2.
  `[[5, 9, 9, 5], [9, 10, 10, 9], [9, 10, 10, 9], [5, 9, 9, 5]]`
  — black-bordered blue avatar with a uniform-light-blue (palette
  10) inner 2×2. Same structure as `pawn_hot`, swap palette
  blue→light-blue for cold. The light-blue inner-fill is the
  cold-polarity cue. Hot pip (pink) and cold pip (light-blue) are
  visually distinct at a glance — checklist item 19 (no hidden
  state) and item 21 (UI teaches role).
- **`target_hot`** — 4×4 ring, tag `"target"`, role `+2`,
  layer 1. `[[14, 14, 14, 14], [14, 8, 8, 14], [14, 8, 8, 14], [14, 14, 14, 14]]`
  — green frame with red centre.
- **`target_warm`** — 4×4 ring, tag `"target"`, role `+1`,
  layer 1. `[[14, 14, 14, 14], [14, 7, 7, 14], [14, 7, 7, 14], [14, 14, 14, 14]]`
  — green frame with pink centre.
- **`target_cold`** — 4×4 ring, tag `"target"`, role `-2`,
  layer 1. `[[14, 14, 14, 14], [14, 9, 9, 14], [14, 9, 9, 14], [14, 14, 14, 14]]`
  — green frame with blue centre.
- **`target_cool`** — 4×4 ring, tag `"target"`, role `-1`,
  layer 1. `[[14, 14, 14, 14], [14, 10, 10, 14], [14, 10, 10, 14], [14, 14, 14, 14]]`
  — green frame with light-blue centre.
- **`target_<X>_satisfied`** — same shape as `target_<X>`, but
  the green frame is replaced with palette `11` (yellow), and
  the centre keeps the temperature colour. Persistent visual
  cue per `checklist.md` item 19 (no hidden state). Used by
  swapping the unsatisfied sprite to REMOVED and the satisfied
  variant to TANGIBLE on latch.
- **`wall_insulator`** — 4×4 block, tag `"wall"`, layer 3.
  `[[5, 5, 5, 5], [5, 3, 3, 5], [5, 3, 3, 5], [5, 5, 5, 5]]`
  — black-bordered grey block. Renders as solid and "blocking";
  visually distinct from any temperature pattern (no palette 8/7/0/10/4-non-bordering; uses 5+3).
- **`step_counter_hud_widget`** — `RenderableUserDisplay`
  subclass (not a Sprite). Renders a depleting bar at display
  row 0 in palette `{5 black, 0 white}` proportional to
  `(step_budget - action_count) / step_budget`.

All sprites use only palette 0..15. No transparent (-1) usage in
this roster. No real-world clipart, no letters/digits-as-glyphs,
no recognisable cultural conventions
(per `forbidden-elements.md`).

## 4. Level progression, mechanic enumeration, and witness solutions

All three levels share `grid_size=(64, 64)`. The thermal-cell grid
is a logical 16×16 subdivision (each cell = 4×4 display pixels).
Movement is ACTION1-4, each shifts the pawn by ±4 pixels (one
thermal cell) per press. Pawn starts on a 4-pixel-aligned position;
all targets and walls are 4-pixel-aligned.

### Level 1 — base dynamic system

**Layout**
- Pawn at thermal-cell (8, 8) hot. Display position (32, 32).
- One `target_hot` at thermal-cell (8, 13). Display position
  (32, 52). Required value +2 (matching `target_hot`).
- No walls.
- step_budget = 24.

**Mechanics required by the witness** (N = 2):

1. **Walk the pawn (ACTION1-4).** Each press shifts the pawn 4
   pixels (one thermal cell) cardinally; movement is rejected if
   the destination thermal cell is out of grid bounds.
2. **Aura-imprint with polarity (passive rule, exercised every
   step).** After each action, the temperature grid is recomputed
   from scratch: every cell is 0 except the pawn's thermal cell
   (set to `+2 * polarity`) and the four cardinal neighbours
   (set to `+1 * polarity`). Targets check their underlying cell's
   value; on first match-with-required, they latch into the
   `_satisfied` set permanently and swap to the gold-frame
   visual cue.

**Necessity per mechanic** (counterfactual, per checklist
item 12):

- *Walk*: L1 cannot be solved without triggering walk because the
  pawn starts at thermal cell (8, 8) and `target_hot` is at
  thermal cell (8, 13); the only way to get the pawn (or its
  +2 imprint cell) to coincide with the target is to walk 5
  cells DOWN. With zero walks, the pawn never reaches a position
  whose imprint covers the target.
- *Aura-imprint*: L1 cannot be solved without the aura-imprint
  rule because target_hot's required value is +2 and the only
  cell that ever takes a +2 value is the pawn's own thermal
  cell; without the imprint rule, every cell stays at 0 and
  the target never latches.

**Witness solution** (shortest action sequence that wins L1):

```
ACTION2, ACTION2, ACTION2, ACTION2, ACTION2
```

5 actions, all DOWN. After action 5, the pawn is at thermal
cell (8, 13); the imprint sets cell (8, 13) to +2; target_hot
matches and latches; all targets satisfied → `next_level()`.

**Difficulty justification**:

- **(a) Random-resistance**: a random 5-action policy on a 5-action
  alphabet [1,2,3,4,5] has probability `(1/5)^5 ≈ 0.032%` per
  trial of stumbling onto exactly DOWN×5. Even random WALK
  with no toggles would need to traverse 5 cells in the right
  direction without backtracking — `(1/4)^5 ≈ 0.1%`. Within the
  step budget of 24, random would explore but not reliably win.
- **(b) Human-tractable**: A first-time human reads the pawn at
  centre, the target ring 5 cells below, presses DOWN a few
  times to see the avatar walking, and notices the cells under
  the avatar turning hot-red. They reach the target ring,
  observe its frame turn gold, and the level advances. ~30-60
  seconds.
- **(c) Planning depth**: **No strict planning required at L1.**
  The L1 difficulty is entirely mechanic-discovery: discover
  that walking imprints heat, and that putting the pawn on the
  target latches it. Once known, the win is near-immediate (one
  action sequence, no branching).
- **(d) Step budget**: 24 (~5× witness). Generous over witness
  to allow exploration of sideways walks before committing to the
  DOWN sequence.

### Level 2 — base system + 1 new mechanic

**Layout**
- Pawn at thermal-cell (8, 8) hot. Display position (32, 32).
- `target_hot` at thermal-cell (3, 8). Required value +2.
- `target_cold` at thermal-cell (13, 8). Required value -2.
- No walls.
- step_budget = 50.

**Mechanics required by the witness** (M = 3 = N + 1, +1 from L1):

1. **Walk the pawn** (carried forward from L1).
2. **Aura-imprint with polarity** (carried forward from L1).
3. **Polarity toggle (ACTION5).** ACTION5 toggles the pawn's
   `_polarity` between +1 (hot) and -1 (cold) and swaps the
   on-screen pawn variant (pawn_hot ↔ pawn_cold) so the player
   sees the polarity change on the avatar.

**Necessity per mechanic** (counterfactual, per checklist
item 12):

- *Walk*: L2 cannot be solved without walk because both targets
  sit 5 cells away from the pawn's start position; without
  walking, the pawn's imprint never covers either target cell
  (start cell (8,8) is not the location of either target ring).
- *Aura-imprint*: L2 cannot be solved without aura-imprint
  because both targets require values (`+2` and `-2`) that
  only ever appear at the pawn's own thermal cell while the
  pawn carries the matching polarity; without the imprint rule,
  every cell stays at 0.
- *Polarity toggle*: L2 cannot be solved without ACTION5
  because the pawn starts hot (polarity +1), so any imprint
  on the pawn's cell while hot is +2; the pawn cannot produce
  a -2 reading at target_cold without first toggling polarity
  to cold. Plausible alternate: walk to target_cold while still
  hot — the imprint sets target_cold's cell to +2, which
  doesn't match the required -2, so target_cold never latches
  and L2 stays unwon. The only path to the -2 imprint is
  ACTION5 followed by walking to target_cold.

**Witness solution** (shortest action sequence that wins L2):

```
ACTION3, ACTION3, ACTION3, ACTION3, ACTION3,    # walk LEFT 5×
ACTION5,                                         # toggle to cold
ACTION4, ACTION4, ACTION4, ACTION4, ACTION4,
ACTION4, ACTION4, ACTION4, ACTION4, ACTION4     # walk RIGHT 10×
```

16 actions. After action 5, pawn at thermal cell (3, 8); imprint
sets (3, 8) to +2; target_hot matches and latches. After action
6 (ACTION5), pawn flips to cold; the imprint at (3, 8) is now
-2 — but target_hot is already latched (latch is permanent). After
actions 7..16, pawn walks RIGHT to (13, 8); the imprint at
(13, 8) is -2; target_cold matches and latches; all satisfied.

**Difficulty justification**:

- **(a) Random-resistance**: a random 16-action policy from a
  5-action alphabet succeeds with probability `(1/5)^16 ≈ 6e-12`.
  The polarity toggle adds a discrete decision the random policy
  has no incentive to make at the right moment. Within the 50-step
  budget, random exploration won't reliably stumble onto both
  latches in either order with the polarity toggle in between.
- **(b) Human-tractable**: A first-time human reads two targets
  on opposite sides of the pawn (cold-blue ring left or right vs
  hot-red ring on the other side). They walk to one — that
  satisfies. They walk to the other — it doesn't satisfy because
  the underlying cell shows the wrong colour. They notice the
  pawn pip colour (magenta-hot) and infer ACTION5 must change
  polarity (the only unused action). They press ACTION5, see the
  pip turn purple, walk to the other target. Estimated ~90-120s
  including the discovery moment.
- **(c) Planning depth (post-discovery)**:
  - **Post-discovery decision space at level start.** A fully-
    informed player knows ACTION5 toggles polarity and that walking
    onto a target imprints the pawn's polarity-value. From start
    they face FOUR plausible first-move directions
    (UP/DOWN/LEFT/RIGHT) plus ACTION5 — count = 5. Two of those
    five are useful: walk LEFT toward target_hot first, or walk
    RIGHT toward target_cold first (with ACTION5 inserted before
    or after).
  - **Plausible-but-wrong alternative**: walk RIGHT to target_cold
    while still hot. Imprint reads +2; target_cold needs -2; no
    latch. Wasted 10 cells, must walk back 10 cells to reach
    target_hot (which still works), and then must use ACTION5 +
    walk RIGHT 10 cells again — total ≥ 30 actions vs witness 16.
    Not a fail, but significantly worse.
  - **Witness's reasoning chain**: walk to target_hot first
    *while polarity is already hot* (saves a toggle); satisfy
    it; then ACTION5 once; then walk to target_cold. The
    fully-informed player is reasoning about polarity-state-at-
    target-cell, not about discovery — the post-discovery
    failure mode is "going to the wrong target first or
    forgetting to toggle".
- **(d) Step budget**: 50 (~3× witness). Per
  `difficulty-rules.md` § d, L2's budget must reflect "several
  actions discovering what the new mechanic does"; 50 - 16 = 34
  actions of slack accommodate exploring polarity flip.

### Level 3 — system + 1 more new mechanic

**Layout** (revised after critique-revisions Issue 2: previous
layout's wall was decorative — the witness was the same step count
with or without it. The new full-column wall genuinely lengthens
the witness by ~20 actions.)

- Pawn at thermal-cell (3, 1) hot. Display position (12, 4).
- `target_hot` at thermal-cell (3, 13). Required value +2.
- `target_cold` at thermal-cell (13, 13). Required value -2.
- 12 `wall_insulator` sprites forming a vertical column at
  thermal-cells (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9),
  (8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (8, 15) — i.e. col
  8 from row 4 down to row 15. Gap rows 0..3 (top of grid). The
  wall is contiguous and partitions the playfield's lower 12 rows
  (rows 4..15) into a left half (cols 0..7) and a right half
  (cols 9..15); the only crossings between halves are at rows
  0..3 (above the wall).
- Wall blocks pawn movement (walks into a wall cell are rejected,
  the pawn stays in place AND the action still consumes a step).
  Wall also blocks aura-imprint propagation: a pawn whose
  cardinal-neighbour cell is a wall does NOT imprint that wall
  cell (walls have no temperature) and does NOT imprint any cell
  beyond the wall (the +1 imprint stops at the wall edge — moot
  for the witness given range-1 aura but defines wall semantics).
- step_budget = 100.

**Mechanics required by the witness** (P = 4 = M + 1, +1 from L2):

1. **Walk the pawn** (carried forward from L1).
2. **Aura-imprint with polarity** (carried forward from L1).
3. **Polarity toggle (ACTION5)** (carried forward from L2).
4. **Insulator wall — movement obstacle.** Walk attempts into a
   wall cell are rejected by the engine; the pawn stays in place.
   The wall row at row 7 cols 4..12 partitions the playfield into
   a top sub-region (rows 0..6) and a bottom sub-region (rows
   8..15) for any pawn at cols 4..12; the pawn must detour
   through col 0..3 or col 13..15 to cross.

**Necessity per mechanic** (counterfactual, per checklist item 12):

- *Walk*: L3 cannot be solved without walk because the pawn
  starts at thermal cell (8, 1) and the two targets are at
  (3, 13) and (12, 13); both require pawn presence on the
  target cell to imprint. Without walking, neither target's
  cell ever takes a non-zero value.
- *Aura-imprint*: L3 cannot be solved without aura-imprint
  because both targets need polarity-driven values (+2 and -2)
  that only appear at the pawn's own thermal cell when the pawn
  carries the matching polarity. Without the imprint rule,
  every cell stays at 0.
- *Polarity toggle*: L3 cannot be solved without ACTION5
  because the pawn starts hot, but `target_cold` requires -2.
  Plausible alternate: walk to target_cold while hot — the
  imprint reads +2, target_cold needs -2, no latch. The only
  path to the -2 imprint at target_cold is ACTION5 first.
- *Insulator wall*: L3 cannot be solved without the wall
  mechanic being exercised. Plausible alternates and why each
  fails:
  1. *Walk RIGHT from (3,1) to (13,1) directly.* Pawn at col 3
     to col 13 must cross col 8. Row 1 col 8 is in the wall
     gap (rows 0..3 are gap), so this works at first — pawn
     reaches (13,1) in 10 RIGHT steps. But target_cold is at
     (13,13), still 12 cells DOWN. Walking DOWN from (13,1):
     col 13 has no wall (wall is at col 8 only); pawn can
     descend to (13,13) freely. So this strategy avoids the
     wall: 10 RIGHT + 12 DOWN = 22 moves. ACTION5 (cold) at
     start (extra 1 move) → imprint -2 at (13,13) → target_cold
     latched. Now reach target_hot at (3,13). Pawn at (13,13)
     cold. UP+LEFT detour: UP×10 to (13,3), LEFT×10 to (3,3),
     DOWN×10 to (3,13). 30 moves. ACTION5 → hot. Latch
     target_hot. Total: 1+22+30+1 = 54 moves. The witness
     (43 moves) is shorter. Critically, this alternative still
     EXERCISES the wall on the way back from target_cold to
     target_hot, since col 8 wall blocks LEFT walks at rows
     4..15. So the wall is exercised here too — just with a
     longer total witness.
  2. *Walk LEFT or stay at col ≤ 7 throughout.* Pawn at col 3
     can't walk RIGHT to (13, *) without crossing col 8. The
     gap is at rows 0..3 only. Any RIGHT walk between rows 4
     and 15 is blocked by wall. So target_cold at (13, 13) is
     unreachable without first going UP to rows 0..3.
  3. *Removing the wall entirely (counterfactual no-wall).*
     Witness becomes DOWN×12 + ACTION5 + RIGHT×10 = 23 moves.
     The actual witness with wall is 43. Wall adds 20 moves —
     a ~87% increase. Wall is non-decorative.

  The wall's distinguishing behaviour (movement-blocking on a
  cell-adjacency basis) is exercised by every walk the pawn
  attempts between target_hot at (3,13) and target_cold at
  (13,13): the only crossing is via rows 0..3, which forces
  the pawn out of its way.

**Witness solution** (shortest action sequence that wins L3):

```
ACTION2 ×12   # DOWN ×12: (3,1) → (3,13). pawn hot, imprint at
              #            (3,13) = +2; target_hot LATCHED.
ACTION5       # toggle to cold polarity.
ACTION1 ×10   # UP ×10: (3,13) → (3,3). Cross above the wall (row 4
              #          start). Pawn passes through cells
              #          (3,12), (3,11), ..., (3,3) — col 3 has
              #          no wall.
ACTION4 ×10   # RIGHT ×10: (3,3) → (13,3). Crosses col 8 at row 3
              #            (within gap rows 0..3). Cells (4,3),
              #            (5,3), ..., (13,3) traversed.
ACTION2 ×10   # DOWN ×10: (13,3) → (13,13). Pawn cold, imprint at
              #            (13,13) = -2; target_cold LATCHED.
```

Total: 12 + 1 + 10 + 10 + 10 = **43 actions**. After action 12 the
pawn is on target_hot with hot polarity → target_hot latches.
After action 13 (ACTION5), pawn is cold. Actions 14-23 walk UP to
above the wall; actions 24-33 walk RIGHT through the gap; actions
34-43 walk DOWN to target_cold. On action 43, pawn cold imprints
-2 at (13, 13); target_cold latches; both targets satisfied →
`self.next_level()`.

**Difficulty justification**:

- **(a) Random-resistance**: a random 43-action policy succeeds
  with probability `(1/5)^43 ≈ 1e-30`. Random exploration in 100
  steps occasionally stumbles into satisfying ONE target, but
  satisfying BOTH (with the ACTION5 toggle inserted at the right
  moment, with the post-target_hot routing UP-RIGHT-DOWN through
  the gap rows 0..3) is essentially unreachable. The wall makes
  random worse than L2 because it forces a specific 30-action
  detour pattern.
- **(b) Human-tractable**: A first-time human at L3 already knows
  the L2 mechanics (walk + aura + polarity-toggle). They see the
  vertical wall column splitting the playfield, the gap at top,
  and the two targets at row 13 on opposite sides of the wall.
  They walk DOWN col 3 to target_hot (12 actions), latch it,
  toggle polarity, then route UP to the gap, RIGHT through the
  gap, DOWN to target_cold (30 actions). ~2-3 minutes total
  including the routing decision and a possible wrong attempt
  at walking RIGHT-along-row-13 first.
- **(c) Planning depth (post-discovery)**:
  - **Post-discovery decision space at level start.** Fully-
    informed player at start (3,1) hot faces FIVE plausible
    first actions: UP (move to (3,0); only useful if planning
    a top-route to target_cold first), DOWN (move toward
    target_hot at (3,13); the witness's choice), LEFT (move
    away from both targets — almost certainly wasted), RIGHT
    (move toward the gap area; could begin a target_cold-first
    route by walking RIGHT to (13,3) first), ACTION5 (toggle to
    cold; only useful if going for target_cold first). Count =
    5; per `difficulty-rules.md` § (d) L3 must have count ≥
    L2's count of 5. ✓
  - **Trivial post-discovery heuristic that fails**: greedy-by-
    polarity-savings. The fully-informed player thinks:
    "I start hot, target_cold needs cold, target_hot needs hot.
    If I go to target_hot first, I do 1 ACTION5 toggle. If I go
    to target_cold first, I do 2 ACTION5 toggles (one to flip
    to cold, one to flip back to hot for target_hot). So
    target_hot first saves 1 toggle; let me also check which is
    closer". This greedy heuristic *succeeds at the goal* of
    minimising toggles — it matches the witness's choice of
    target_hot first.
    
    A different *failing* heuristic is "shortest first leg" —
    pawn is at (3,1); target_hot is at (3,13), Manhattan 12;
    target_cold is at (13,13), Manhattan 22. Shortest-first-leg
    suggests target_hot first, which matches the witness.

    A *plausibly-failing* heuristic, the **right-side-first
    greedy**: "the pawn at (3,1) is closer to col 13 in
    horizontal terms (10 cells RIGHT vs 12 cells DOWN) — let me
    walk RIGHT first across the gap and reach target_cold
    quickly". Pawn at (3,1) hot. ACTION5 → cold. RIGHT×10 to
    (13,1). DOWN×12 to (13,13). target_cold latched. 1+10+12=23
    moves. Now target_hot. ACTION5 → hot. UP×10 to (13,3),
    LEFT×10 to (3,3), DOWN×10 to (3,13). 30 moves. target_hot
    latched. Total: 23+1+30 = 54 moves. **Witness is 43; this
    heuristic costs 11 extra moves** — significantly delays the
    win by ~26%. Inside step budget 100, both still finish, but
    the tighter the budget the more this matters.
  - **Where the heuristic diverges from the witness**: at
    action 1. The witness chooses ACTION2 (DOWN — toward
    target_hot, no toggle yet); the failing right-side-first
    heuristic chooses ACTION5 (toggle now, then RIGHT). After
    action 1, the witness pawn is at (3,2) still hot; the
    heuristic pawn is at (3,1) cold. The witness is 1 cell
    closer to target_hot AND has saved a future ACTION5 (since
    it doesn't need to flip back from cold-to-hot for
    target_hot). The heuristic is making a locally-myopic
    "minimise distance to a target" choice without thinking
    about the *return* trip from one target to the other. The
    correct ahead-of-time reasoning is: "the polarity I start
    with should match the FIRST target I latch; that target is
    target_hot since I'm already hot." This is a 2-step look-
    ahead that defeats greedy by-distance choices.

  **Stage-conflation guard.** The failing right-side-first
  heuristic above is a post-discovery error — the player KNOWS
  ACTION5 toggles polarity and that polarity must match target;
  they just choose the wrong target order. They are not
  confused by missing knowledge. ✓
- **(d) Step budget**: 100 (~2.3× witness). The L3 budget is
  larger than L2's (50) per `difficulty-rules.md` § d's
  "the budget must NOT shrink relative to the witness as
  level number rises". 100 - 43 = 57 actions of slack supports
  exploring the wall detour direction and possibly trying the
  wrong-target-first path before recovering.

## 5. Action mapping

`available_actions = [1, 2, 3, 4, 5]` — five slots, no click,
no undo. The action shape (cardinal-arrow + freedom-slot) is
intentionally distinct from the click-heavy near-misses pf3w,
kp9z, gv47, vd3g (which are all click-driven).

- `ACTION1` — walk pawn 1 thermal cell up (display y -= 4). Valid
  iff destination cell is in-bounds AND not a wall cell.
- `ACTION2` — walk pawn 1 thermal cell down (display y += 4).
  Valid iff destination cell is in-bounds AND not a wall cell.
- `ACTION3` — walk pawn 1 thermal cell left (display x -= 4).
  Valid iff destination cell is in-bounds AND not a wall cell.
- `ACTION4` — walk pawn 1 thermal cell right (display x += 4).
  Valid iff destination cell is in-bounds AND not a wall cell.
- `ACTION5` — toggle pawn polarity (`+1 ↔ -1`). Always valid.
  Side effects: swap pawn sprite (pawn_hot ↔ pawn_cold) at the
  pawn's current display position, with the inactive variant
  set to `InteractionMode.REMOVED` and the active one
  `InteractionMode.TANGIBLE`, per `universal-scaffold.md` § Two-
  sprite swap idiom.

When a movement attempt is rejected (out-of-bounds or wall
collision), the action still consumes one step — the action
counter increments and the step-counter HUD updates, but the
pawn does not move. This matches the standard behaviour in
ka59, m0r0, sk48, etc.

## 6. HUD and per-game state

**HUD**:

- `step_counter_hud_widget` — `RenderableUserDisplay` subclass.
  Renders a depleting horizontal bar at display row 0 (palette
  `5` for "remaining" portion, palette `0` for "spent"
  portion). Width 64; portion-remaining = `(step_budget -
  action_count) / step_budget * 64`. Updated every step.

**Per-game state** (mutated across actions):

- `self._polarity: int` — `+1` (hot) or `-1` (cold). Toggled by
  ACTION5. Surfaced visually by which pawn variant is active
  (pawn_hot vs pawn_cold) — checklist item 19's persistent
  visual cue.
- `self._satisfied: set[str]` — names of latched targets.
  Surfaced visually by each latched target's sprite swapping
  to its `_satisfied` variant (gold frame). Persistent.
- `self._temperature: np.ndarray` of shape (16, 16), int8.
  Recomputed in full each step from pawn position + polarity +
  walls. Not technically "state" (function of other state) but
  cached on the instance to avoid recomputation in `step()` and
  the win-check.

These three pieces of state, plus the engine-managed sprite
positions, fully determine the game's behaviour. No randomness;
no wall-clock dependence; the game is deterministic given
(initial level, action sequence) per
`design-constraints/from-tech-report.md` § 7 (validation
thresholds).

`_get_hidden_state()` returns a 4×4 int16 matrix with
`[0,0] = polarity`, `[0,1] = number of latched targets`,
`[0,2] = action_count`. (The temperature grid is implicit in
the rendered frame; not encoding it in hidden_state both saves
graph-identity bandwidth and avoids over-encoding what the
player can already see.)

## 7. Win condition

After every action's effects are applied (move + recompute
temperature + check targets), the game iterates over every
`tag="target"` sprite. For each unsatisfied target T with
required value `T.required` (read from a `data` attribute on
the target's clone, or from the sprite's name suffix):

```python
cell_x, cell_y = T.x // 4, T.y // 4   # thermal-cell coords of target
if self._temperature[cell_y, cell_x] == T.required:
    self._satisfied.add(T.name)
    # swap to the satisfied-variant sprite
    self.current_level.add_sprite(sprites[f"{T.name}_satisfied"]
                                   .clone()
                                   .set_position(T.x, T.y))
    T.set_interaction(InteractionMode.REMOVED)
```

If `len(self._satisfied) == number of targets`, call
`self.next_level()`.

The predicate is testable per-target on each tick. It is
deterministic and depends only on visible state.

## 8. Lose condition

If `self._action_count >= step_budget`, call `self.lose()`. There
is no other lose condition — no hazards, no enemies, no
collision-damage. A pawn cannot be soft-locked because every
state has paths to satisfying targets (no irreversible
state changes other than target latches, which only help the
player).

## 9. Novelty note

### vs the 25-game taxonomy

Closest taxonomy entries by surface signature:

- **lq5x lantern-cone-illuminate** *(actually a prior, not the
  taxonomy — included here for completeness)* — mentioned below
  under prior-games comparison.
- **dc22 colour-cycle-walk** — pawn walks an arena scattered
  with coloured wedge-blocks and colour-wheel triggers; stepping
  on a trigger cycles every wedge of that colour. **Distinguishing
  rule**: dc22's triggers cycle DISCRETE wedge states in a fixed
  enumerated cycle; tm5x has a continuous-integer temperature
  field where the same cell takes any value in {-2..+2}
  depending purely on pawn position + polarity. dc22's cycling
  is order-dependent (each press advances one notch); tm5x's
  imprint is positional (each pawn position determines the
  field directly, no notch-counter). Different cell rule,
  different state representation, different win check.
- **re86 frame-paint-canvas** — marker walks a hidden canvas;
  on each move, marker's centre cell deposits the marker's
  colour; marker boundary extends 3 cells per move; ACTION5
  cycles which marker is active. **Distinguishing rule**: re86
  is BOOLEAN-PER-CHANNEL paint that grows to fill regions —
  once painted, a cell stays painted; the marker's shell
  extends. tm5x is INTEGER SCALAR temperature that revertS to
  0 the moment the pawn leaves; it does not paint or fill —
  the field is a function of pawn position only. re86's
  ACTION5 cycles ACTIVE-MARKER (selects which marker moves
  next); tm5x's ACTION5 toggles POLARITY (changes the imprint
  value sign). Different field model, different ACTION5
  semantic, different state-persistence rule.
- **ls20 cycler-attribute-match** — pawn walks a wall-bound
  maze; stepping onto a cycler-tile rolls the pawn's shape /
  colour / rotation through a fixed alphabet. **Distinguishing
  rule**: ls20's cycler tiles modify the PAWN'S attributes;
  tm5x's pawn has a single binary polarity attribute toggled
  only by ACTION5 (no environmental cycler tiles). ls20's
  win condition is matching pawn-attributes-to-pellet-
  attributes at each pellet; tm5x's win condition is field-
  cell-value-matches-target-required-value across multiple
  targets. Different attribute domain (3-attribute discrete
  vs 1-attribute binary), different mutation channel (env
  vs ACTION5), different win check.

The candidate's mechanic family `thermal-aura-imprint` does
NOT match any taxonomy family stem either exactly or after
hyphen-split. **Verdict against taxonomy: NOVEL.**

### vs `prior-games/index.md`

29 prior-game entries scanned. Closest neighbours:

- **pf3w wavefront-converge-timing** (2026-05-07) — click pre-
  placed slots to activate emitters; ACTION5 ticks each
  emitter's BFS-radius wavefront outward; level wins on the
  single tick when every same-coloured target receiver
  coincides with a frontier cell. **Concrete distinguishing
  rules**:
  1. *Field representation*: pf3w propagates a BOOLEAN BFS
     frontier — cells are either active-this-tick or not.
     tm5x maintains an INTEGER scalar temperature field with
     5 distinct values per cell.
  2. *Player verb*: pf3w is click-to-arm + ACTION5-to-tick
     (no walking; emitters are pre-placed). tm5x is walk-to-
     deposit + ACTION5-to-flip-polarity (no emitters; the
     pawn IS the source).
  3. *Win check*: pf3w wins on coincidence of frontier with
     receiver on a SINGLE tick. tm5x latches each target
     once cumulatively when its cell value matches; once
     latched it stays latched, and the level wins when ALL
     are latched (no single-tick coincidence requirement).
- **kp9z grain-accumulate-topple** (2026-05-06) — click sources
  to drop grains; cells overflow at capacity 4 to 4 cardinals;
  sinks absorb. **Concrete distinguishing rules**:
  1. *Cell rule*: kp9z's per-cell rule is THRESHOLD-TOPPLE at
     capacity 4 (sandpile dynamics). tm5x's per-cell rule is
     POSITIONAL IMPRINT — pawn's thermal cell + 4 neighbours
     are imprinted directly each tick; no thresholds, no
     overflow, no avalanche.
  2. *Player verb*: kp9z is click-source-to-add + click-
     redirector-to-rotate (pure-click). tm5x is walk-to-
     deposit + ACTION5-to-flip-polarity (pure-arrow + freedom
     slot).
  3. *Value semantics*: kp9z's grain count is unsigned and
     discrete-incremental; tm5x's temperature is signed
     ({-2..+2}) and polarity-driven, switching sign requires
     ACTION5.
- **gv47 seed-grow-surround-dissolve** — click coloured seeds to
  grow regions; surrounding a same-coloured pip dissolves it.
  **Concrete distinguishing rules**:
  1. *Field representation*: gv47's field is a partition of
     cells into coloured regions (boolean per cell per
     colour). tm5x's field is a signed-integer scalar.
  2. *Cell evolution*: gv47 grows regions on click; tm5x
     imprints from pawn position every tick.
  3. *Player verb*: gv47 click; tm5x walk + ACTION5.
- **vd3g valley-dig-roll** — click cells to toggle binary
  terrain; marbles flow downhill. **Concrete distinguishing
  rules**:
  1. *Flow rule*: vd3g has gravity-biased downhill flow;
     tm5x has 4-cardinal symmetric imprint with no preferred
     axis.
  2. *Player verb*: vd3g click-to-toggle-terrain; tm5x walk
     + polarity-flip.
  3. *Object cast*: vd3g has marbles + terrain; tm5x has
     pawn + targets + walls. No marbles in tm5x; no
     temperature field in vd3g.
- **mr5q polarity-attract-discharge** — pawns flip yang/yin via
  click; per ACTION5 each walks toward nearest same-colour
  opposite. **Concrete distinguishing rules**:
  1. *Polarity locus*: mr5q's polarity is an attribute of
     ENTITIES (pawns) that drives autonomous walk. tm5x's
     polarity is an attribute of the SINGLE PAWN that drives
     the IMPRINT VALUE (pure scalar).
  2. *Field*: mr5q has no field-of-cell-state; tm5x has a
     full 16×16 thermal field rendered every tick.
  3. *Win check*: mr5q wins when same-colour pawns are
     adjacent (discharge); tm5x wins when target cells take
     specific values cumulatively.
- **lq5x lantern-cone-illuminate** — single lantern projects
  a 3-wide directional cone; arrows walk; ACTION5 rotates
  cone; wax pickups extend cone range. **Concrete
  distinguishing rules**:
  1. *Aura shape*: lq5x's cone is DIRECTIONAL (rotates by
     90° increments via ACTION5), 3-wide, with extendable
     range. tm5x's aura is OMNIDIRECTIONAL (4-cardinal-
     adjacent, fixed shape), with no rotation.
  2. *ACTION5 verb*: lq5x rotates cone direction; tm5x
     toggles polarity sign.
  3. *Field semantics*: lq5x's cone illuminates BOOLEAN
     light-on-cells (with optional re-tinting via filters);
     tm5x's aura imprints SIGNED integer values.
  4. *Win check*: lq5x is "every coloured target ring is
     illuminated by matching colour"; tm5x is "every target
     cell takes its required signed value at some point".

Negative-similarity check (per
`mechanic-novelty/negative-similarity-check.md`): walked the 8
dimensions against pf3w, kp9z, gv47, vd3g, mr5q, lq5x. The
strongest near-miss (pf3w) shares only 1-2 dimensions (the
"ACTION5 ticks the world" surface; the kill-by-step-counter
universal). Visual signature differs (smooth gradient vs
discrete frontier squares), pixel grain differs (4×4 internal
patterns per cell vs flat ground), core dynamic differs
(integer scalar imprint with cumulative latching vs boolean
frontier coincidence). **No prior shares 3+ dimensions.**

**Verdict against prior-games/index.md: NOVEL.**

### Note on first-run state of `prior-games/index.md`

`prior-games/index.md` is NOT empty — it contains 29 prior
generated games. tm5x is the 30th. The above novelty argument
considered every entry.
