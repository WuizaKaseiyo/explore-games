# Mechanic Spec — `hk7v`

## 1. Title
Overhead Trolley + Hook Pick-and-Place

## 2. Mechanic family
`overhead-trolley-hook` — the player operates a Cartesian gantry from
above the playfield: a trolley slides horizontally along a fixed top
beam, a vertical rope of variable length hangs from the trolley, and a
hook at the rope's end picks up and releases coloured blocks. The
mechanic draws from §3.4 priors **objectness** (trolley, hook, rope,
blocks, walls, floor, targets are all persistent entities), **basic
physics** (released blocks fall under gravity until they rest on
floor or on top of another block; the rope is a rigid vertical
geometry that cannot pass through solid walls), and **basic geometry
& topology** (the rope-clearance constraint is a topology rule that
the rope's column at each y between trolley and hook must be free of
wall cells).

There is no agentness — no autonomous NPCs, no chasers, no patrolling
units. Every state change is deterministic given the action sequence.

## 3. Sprite roster

Grid is 64×64 directly (no upscaling); sprite sizes below are in
display pixels. All sprites use palette values 0..15 only.

- **`beam`** — 64 wide × 1 tall; palette `[3]` solid grey row.
  Tags: `["beam"]`. Role: visual top rail, non-collidable. Drawn at
  row 3, full width.

- **`trolley`** — 5 wide × 4 tall; palette `[3, -1, 14, 15, 4]`.
  Pixels:
  ```
  3 3 3 3 3
  3 14 14 14 3
  3 15 15 15 3
  -1 -1 4 -1 -1
  ```
  Tags: `["trolley"]`. Role: the player's horizontally-moving
  trolley. Trolley.y fixed at 4 (sits on row 3 beam, occupies rows
  4..7). Trolley.x = 0..59. Internal pattern: dark-grey shell
  (palette 3) with a green-and-purple core (14/15) for visual
  richness, and a single dark off-black (4) peg at the bottom-centre
  for rope attachment.

- **`hook`** — 5 wide × 4 tall; palette `[3, 4, -1]`.
  Pixels:
  ```
  -1 -1 4 -1 -1
  3 3 3 3 3
  3 4 -1 4 3
  3 4 -1 4 3
  ```
  Tags: `["hook"]`. Role: the rope's end-effector. The top-centre
  off-black peg (palette 4) is the rope-attach point. The bottom
  forms a U-shape of grey rims (3) framing two off-black inner
  pillars (4) that read as "claw arms" — distinct from any block
  silhouette.

- **`rope`** — 1 wide × *variable* tall; palette `[4]`. Tags:
  `["rope"]`. Role: visual link between trolley and hook; pixel
  array regenerated each action by the game class (one column of
  off-black 4 from row `trolley.y + trolley.h` to row `hook.y - 1`,
  inclusive). Length 0 when hook is directly below trolley
  (rope sprite has zero rows in that case → marked
  `InteractionMode.REMOVED`).

- **`floor`** — 64 wide × 1 tall; palette `[2]` light-grey. Tags:
  `["floor"]`. Role: visual ground; non-collidable (collision is
  enforced by game code, not the sprite). Drawn at row 58.

- **`block_red`** — 5 wide × 5 tall; palette `[8, 13, -1]`.
  Pixels:
  ```
  8 8 8 8 8
  8 13 8 13 8
  8 8 8 8 8
  8 13 8 13 8
  8 8 8 8 8
  ```
  Tags: `["block", "red"]`. Role: deliverable cargo; collidable;
  each cell of red 8 with maroon 13 inset markers gives internal
  pixel pattern (per checklist 20).

- **`block_blue`** — 5 wide × 5 tall; palette `[9, 10, -1]`. Same
  pattern as `block_red` but colours `(8→9, 13→10)`. Blue with
  light-blue inset markers. Tags: `["block", "blue"]`.

- **`block_yellow`** — 5 wide × 5 tall; palette `[11, 12, -1]`.
  Same pattern; yellow 11 with orange 12 inset markers. Tags:
  `["block", "yellow"]`.

- **`target_red`** — 7 wide × 1 tall; palette `[8, -1]`. Pixels:
  ```
  8 8 -1 8 -1 8 8
  ```
  Tags: `["target", "red"]`. Role: visual marker on floor for
  red drop-zone; non-collidable; placed at row 57 (just above
  floor) so a deposited 5-wide block resting at floor sits
  centred over it leaving 1 cell of target colour visible at each
  end (the marker pattern reads as "matched red drop here").

- **`target_blue`** — 7 wide × 1 tall; palette `[9, -1]`. Same
  pattern. Tags: `["target", "blue"]`.

- **`target_yellow`** — 7 wide × 1 tall; palette `[11, -1]`. Same
  pattern. Tags: `["target", "yellow"]`.

- **`wall`** — 3 wide × 36 tall; palette `[4, 5]`. Repeating 3×2
  internal pattern:
  ```
  4 5 4
  4 4 4
  ```
  Tags: `["wall"]`. Role: a vertical pillar that the rope cannot
  pass through. Used in L2 and L3. Off-black 4 with black 5 dots
  for grain (per checklist 20). Collidable, but collision is
  game-enforced (only rope cells and carried-block cells are
  checked against wall cells; trolley above the wall and floor
  below the wall are unaffected).

The "two sprite kinds with different roles must look different"
rule (checklist 21) is satisfied: every sprite kind has its own
shape and palette, and same-kind variants (block_red vs block_blue
vs block_yellow; target_red vs target_blue vs target_yellow) share
shape but differ in palette to communicate "same role, different
colour pairing".

## 4. Level progression, mechanic enumeration, and witness solutions

All three levels share `grid_size=(64, 64)` so the camera does not
upscale. The trolley/beam/hook scaffold is identical across levels;
only the block/target/wall configuration varies.

### Level 1 — base dynamic system

Layout: beam row 3 across full width; trolley starts at `(x=0, y=4)`;
hook starts at `(x=0, y=8)` (rope length 0); floor at row 58; one
`block_red` at `(x=14, y=53)`; one `target_red` at `(x=43, y=57)`.
No walls.

- **Mechanics required by the witness** (N = 1):
  1. **M1 — overhead-manipulator** (the L1 base dynamic system: a
     small interacting system of trolley H + hook V + grab/release).
     The witness must move the trolley horizontally, the hook
     vertically, grab the block, and release the block. All four
     sub-verbs of M1 are exercised.

  Per the revision in `critique-revisions.md` issue 1, M2
  (colour-pairing) is intentionally NOT introduced at L1 because
  L1 has only one colour and the colour comparison's distinguishing
  behaviour (a *failed* match) cannot be triggered by any L1
  input sequence — leaving M2 decoratively listed at L1 would
  violate checklist 12. M2 is introduced at L2.

- **Necessity per mechanic** (counterfactual, per checklist item 12):

  - L1 cannot be solved without triggering M1 because the only way
    to relocate `block_red` from `(14, 53)` to the target column
    `x=44` is via the trolley/hook/grab system — the player has no
    walking avatar, no click-to-place primitive, and no other input
    that can move blocks. Removing M1 leaves the player with no
    means at all to alter `block_red`'s position; the win predicate
    (block at target column) fails by default. Plausible alternates
    a player might try: (a) "spam ACTION5 from start" — fails
    because there is no block under the hook at trolley.x=0 to
    grab; (b) "raise hook" — already at minimum (rope length 0);
    (c) "move trolley to x=44 without grabbing" — block_red stays
    at (14, 53), win predicate sees block.x=14 ≠ 44, fails. Each
    plausible alternate trips on a sub-verb of M1.

- **Witness solution** (87 actions, shortest):

  ```
  ACTION4 ×14   # trolley x: 0 → 14
  ACTION2 ×41   # hook y: 8 → 49 (lower onto block_red top)
  ACTION5 ×1    # grab block_red
  ACTION4 ×30   # trolley x: 14 → 44 (carrying block at floor level)
  ACTION5 ×1    # release: block already at (44, 53), on target
  ```

  After release, win predicate: block_red at (44, 53), target_red
  at (43, 57); block_red.x (44) == target_red.x + 1 (43+1) ✓;
  block_red.y == 53 ✓; colour pair ✓. `self.next_level()` fires.

- **Difficulty justification**:

  - **(a) Random-resistance**: with `available_actions=[1,2,3,4,5]`
    and 87 specific actions in the witness, a uniform random
    policy's chance of executing the witness is ≈ 5⁻⁸⁷ ≈ 10⁻⁶¹ —
    effectively zero. Even ignoring exact ordering, the random
    agent must (a) end with trolley at column 44 and (b) have
    block_red carried during that arrival — both joint events are
    vanishingly unlikely to happen by chance within the budget.
  - **(b) Human-tractable**: ~2 minutes once the trolley/rope/hook
    layout is read off the screen. The player presses arrows to
    learn that ACTION3/4 slide the trolley, ACTION1/2 raise/lower
    the hook, then deduces that ACTION5 grabs/releases on
    contact. Once these three are learned (~30s of exploration),
    the puzzle is mechanical.
  - **(c) Planning depth (post-discovery)**: NO strict planning
    requirement. The block's only valid resting position is the
    target column; the trolley path is a single horizontal slide.
    L1's difficulty is entirely the discovery-stage exercise of
    matching three input types to three sub-verbs.
  - **(d) Step budget**: 150 (1.7× witness's 87 — generous, allows
    several full mistakes-and-recoveries).

### Level 2 — base system + 1 new mechanic

Layout: same beam/trolley/floor/hook scaffold; **one** `wall` at
columns 30..32 spanning rows 20..55 (the wall's 3×36 sprite); one
`block_red` at `(x=4, y=53)` and one `block_blue` at `(x=52, y=53)`;
one `target_red` at `(x=43, y=57)` (right of wall) and one
`target_blue` at `(x=57, y=57)` (right of wall, far right).

- **Mechanics required by the witness** (N+2 = 3). Both M2 and M3
  are NEWLY INTRODUCED at L2 (per critique-revisions issue 1).
  M1 carries forward; M2 (colour-pairing) becomes non-trivial because
  two distinct colours coexist; M3 is the rope-clearance constraint:
  1. **M1 — overhead-manipulator** (carried from L1).
  2. **M2 — colour-pairing** (newly introduced at L2). The win
     predicate distinguishes red from blue: `block_red` must rest
     at the red target's column AND `block_blue` must rest at the
     blue target's column. Mismatching either pair fails the win.
  3. **M3 — rope-clearance-above-wall**. When the trolley moves
     horizontally to a column whose `trolley.x + 2` (rope's
     vertical column) coincides with a wall column AND any rope
     cell or carried-block cell would land at a row inside the
     wall's row range, the move is denied. To traverse the wall,
     the player must raise the hook (and therefore retract the
     rope) until the carried block is entirely above row 20.

- **Necessity per mechanic** (counterfactual):

  - L2 cannot be solved without triggering M1 because — same as
    L1 — there is no other input that moves blocks. M1's three
    sub-verbs (trolley H, hook V, grab/release) are all required
    by every individual block delivery: trolley H to align with
    block then with target, hook V to descend onto block then to
    rise for traversal, grab/release to actually attach and detach
    cargo. Removing any one sub-verb leaves the corresponding
    delivery infeasible.
  - L2 cannot be solved without triggering M2 because the win
    predicate now distinguishes red and blue: a winning state
    requires `block_red` at `(44, 53)` AND `block_blue` at
    `(58, 53)`. Releasing `block_blue` at `(44, 53)` (the red
    target column) leaves `block_red` undelivered AND
    `target_blue`'s column unfulfilled — the predicate fails on
    BOTH halves. The colour comparison in the win check is what
    forces the player to remember which block goes where.
  - L2 cannot be solved without triggering M3 because to deliver
    `block_red` from `(4, 53)` to the right side of the wall, the
    trolley must traverse `trolley.x ∈ {28, 29, 30}` (the cell
    columns where the rope's column `trolley.x+2 ∈ {30, 31, 32}`
    coincides with the wall). With the hook lowered to `y=49`
    (carry position for floor-level cargo), the rope occupies rows
    8..48 and the carried block occupies rows 53..57; both sets
    intersect the wall's row range 20..55. The move-validation
    rule denies these horizontal moves until the player raises
    the hook high enough that (a) the rope cells are all above
    row 20 — i.e. `hook.y - 1 < 20`, so `hook.y ≤ 20` — AND
    (b) the carried block is above row 20 — i.e. `hook.y + 4 + 4
    < 20`, so `hook.y < 12`. The binding constraint is (b);
    the witness raises hook to `y=11` before traversing.

- **Witness solution** (179 actions, shortest):

  ```
  ACTION4 ×4    # trolley x: 0 → 4 (over block_red)
  ACTION2 ×41   # hook y: 8 → 49 (onto block_red)
  ACTION5 ×1    # grab block_red
  ACTION1 ×38   # hook y: 49 → 11 (raise above wall row 20)
  ACTION4 ×40   # trolley x: 4 → 44 (cross wall while high)
  ACTION5 ×1    # release: block_red falls (44, 15) → (44, 53) onto target_red
  ACTION4 ×8    # trolley x: 44 → 52 (over block_blue), hook still y=11
  ACTION2 ×38   # hook y: 11 → 49 (onto block_blue)
  ACTION5 ×1    # grab block_blue
  ACTION4 ×6    # trolley x: 52 → 58 (no wall crossing required for this leg)
  ACTION5 ×1    # release: block_blue at (58, 53) onto target_blue
  ```

  Sum: 4+41+1+38+40+1+8+38+1+6+1 = 179.

- **Difficulty justification**:

  - **(a) Random-resistance**: P(random policy wins) ≤ 5⁻¹⁷⁹ ≈
    10⁻¹²⁵. The conjunction of "hook above wall when crossing"
    and "block carried when at target column" has effectively zero
    probability under random sampling.
  - **(b) Human-tractable**: ~2-3 minutes. The two new mechanics
    (M2 colour-pairing and M3 rope-vs-wall) are both discovered
    quickly: M2 by reading the two distinct target colours off the
    floor and pairing visually with the two distinct block colours;
    M3 the first time the player tries to slide the trolley left
    while the rope intersects the wall — the move is denied with
    no ambiguity. Once seen, the "raise before crossing" rule and
    the colour-match rule are permanent. Actual delivery is
    mechanical.
  - **(c) Planning depth (post-discovery)**: moderate. **Decision
    space at level start** = 3 valid distinct first-action moves
    (trolley right toward block_red at x=4, trolley right further
    toward block_blue at x=52 first, or lower hook in place — the
    last is a valid action but stalls progress). **Plausible-but-
    wrong alternative**: a fully-informed player might try to
    deliver `block_blue` first (it is closer to the right-side
    targets so seems "easier"); but its target_blue at x=57 is
    only 5 cells to its right, while delivering block_red (which
    must cross the wall) ALSO requires the hook-raise-cycle. The
    witness handles the wall-cross delivery FIRST (block_red),
    then the local delivery (block_blue), avoiding an extra
    raise/lower cycle. **Witness reasoning chain**: (1) at x=0,
    trolley right 4 cells to align with the supply block_red on
    the left side of the wall; (2) lower hook 41 cells down to
    grab; (3) raise hook 38 cells UP to clear wall (this is the
    rope-vs-wall mechanic forcing the order); (4) cross wall right
    40 cells; (5) release; (6) traverse right 8 to block_blue;
    (7) lower 38; (8) grab; (9) right 6 (no wall cross needed —
    block_blue's target is on the same side); (10) release.
    The plausible wrong path "deliver block_blue first then
    block_red" still works geometrically but is no shorter and
    requires the SAME hook-raise-cycle for block_red anyway —
    the player must reason that raise/lower cost is incurred
    once per wall-cross, not per delivery, and that two
    deliveries on the same side amortise no benefit.
  - **(d) Step budget**: 250 (1.4× witness's 179 — generous; the
    player has room for several wrong-direction trolley moves and
    over-lowers without busting the budget).

### Level 3 — base system + 1 more new mechanic

Layout: same scaffold; **one** `wall` at columns 30..32 spanning rows
20..55 (identical to L2); a stack of three blocks at column 4: from
top to bottom `block_yellow` at `(4, 43)`, `block_blue` at `(4, 48)`,
`block_red` at `(4, 53)`; three targets:
`target_yellow` at `(43, 57)` (right of wall),
`target_blue` at `(23, 57)` (left of wall, between supply column and
wall), and `target_red` at `(57, 57)` (right of wall, far right).

- **Mechanics required by the witness** (L2-count + 1 = 4): M1
  (overhead-manipulator, carried), M2 (colour-pairing, carried —
  three distinct colours), M3 (rope-clearance, carried — wall is
  identical to L2's, two of the three deliveries cross it), and:
  4. **M4 — gravity-stacking-disassembly**. Blocks stack
     vertically: a released block falls until its bottom row sits
     on the floor (row 57) OR on top of another block in the same
     column. While a stack exists, only the top-most block in a
     column is grabbable: lowering the hook into the column stops
     when the hook bottom reaches `(stack_top_y - 1)` (because the
     cell at `(stack_top_y, hook_x..)` is blocked by the existing
     block). To access lower blocks in the supply stack, the
     player MUST first remove every block above them.

- **Necessity per mechanic** (counterfactual):

  - L3 cannot be solved without triggering M1 because — same
    reasoning — no other input moves blocks; the win requires
    THREE blocks at three distinct target columns, each delivery
    needing trolley H + hook V + grab/release.
  - L3 cannot be solved without triggering M2 because the win
    predicate now scales to three colour pairings: red→x=58,
    blue→x=24, yellow→x=44. Mismatching any single one (e.g.
    releasing block_yellow at column 24 where target_blue lives)
    leaves both target_blue and target_yellow unfulfilled —
    `target_blue` is unfulfilled because `block_blue` is not at
    `(24, 53)`, AND `target_yellow` is unfulfilled because
    `block_yellow` is at `(24, 53)` not `(44, 53)`. The colour
    test in `_check_win` fails on both per-target predicates.
  - L3 cannot be solved without triggering M3 because the wall at
    columns 30..32 (rows 20..55) is identical to L2's and the
    same horizontal-traversal constraint applies. With supply at
    column 4 (left of wall) and `target_yellow` at column 44
    AND `target_red` at column 58 (both right of wall), at least
    TWO of the three carries must cross the wall; each requires
    raising the carried block above row 20 before traversing.
  - L3 cannot be solved without triggering M4 because the supply
    starts as a vertical stack: `block_yellow` at top (rows 43..47),
    `block_blue` in the middle (rows 48..52), `block_red` at the
    bottom (rows 53..57). The grab-validity rule requires hook
    bottom directly adjacent to a block top with no other block
    in between; from above, only `block_yellow` (top of stack)
    is reachable. ACTION2 from `hook.y = 8` stops at `hook.y = 39`
    because the cell at `(hook bottom + 1) = 43` is occupied by
    `block_yellow`. Player attempting to lower further to grab
    `block_blue` (would need `hook.y = 44`) is denied — yellow
    must be removed first. Same logic for `block_red` after
    `block_blue` is removed. Without M4 the stack would not
    exist (blocks would sit at the same spot independently);
    with M4, the disassembly order yellow → blue → red is forced
    by the geometry.

- **Witness solution** (319 actions, shortest):

  ```
  # ---- yellow (top of stack) ----
  ACTION4 ×4    # trolley x: 0 → 4
  ACTION2 ×31   # hook y: 8 → 39 (onto block_yellow top, blocked by yellow)
  ACTION5 ×1    # grab block_yellow
  ACTION1 ×28   # hook y: 39 → 11 (raise above wall)
  ACTION4 ×40   # trolley x: 4 → 44 (cross wall)
  ACTION5 ×1    # release; block_yellow falls to (44, 53) on target_yellow

  # ---- blue (now top of remaining stack: blue at y=48, red below) ----
  ACTION3 ×40   # trolley x: 44 → 4 (return left across wall, hook empty at y=11)
  ACTION2 ×33   # hook y: 11 → 44 (onto block_blue top)
  ACTION5 ×1    # grab block_blue
  ACTION4 ×20   # trolley x: 4 → 24 (no wall crossing — target_blue is left of wall)
  ACTION2 ×5    # hook y: 44 → 49 (lower for floor placement)
  ACTION5 ×1    # release; block_blue at (24, 53) on target_blue

  # ---- red (now alone on floor at column 4) ----
  ACTION3 ×20   # trolley x: 24 → 4 (return left, hook empty at y=49)
  ACTION5 ×1    # grab block_red (hook bottom 52 already adjacent to red top 53)
  ACTION1 ×38   # hook y: 49 → 11 (raise above wall)
  ACTION4 ×54   # trolley x: 4 → 58 (cross wall, far right)
  ACTION5 ×1    # release; block_red at (58, 53) on target_red
  ```

  Total: 4+31+1+28+40+1 + 40+33+1+20+5+1 + 20+1+38+54+1 = 319 actions.

  Win predicate: block_yellow at (44, 53) ↔ target_yellow at (43, 57) ✓;
  block_blue at (24, 53) ↔ target_blue at (23, 57) ✓;
  block_red at (58, 53) ↔ target_red at (57, 57) ✓.

- **Difficulty justification**:

  - **(a) Random-resistance**: P(random policy wins) ≤ 5⁻³¹⁹ ≈
    10⁻²²³. The conjunction of "stack-disassembly order respected"
    AND "every wall-crossing has hook raised" AND "every release
    is at correct colour-paired target column" makes random
    success effectively impossible.
  - **(b) Human-tractable**: ~3-4 minutes. The L3 player has
    already learned M1, M2, M3 in earlier levels; the new mechanic
    M4 (stack-disassembly) is discovered the first time they
    lower hook into the supply column and find lowering arrests
    at `hook.y=39` — visibly the hook stops above yellow rather
    than passing through. Within one or two attempts the
    "top-down disassembly" rule is internalised. The remaining
    challenge is execution discipline across three wall-cross
    cycles.
  - **(c) Planning depth (post-discovery)**: challenging.
    **Decision space at level start** = 5 valid distinct
    first-action options (trolley right toward stack at x=4;
    trolley right further toward target_blue at x=23 — but
    arriving with no block is wasted; lower hook in place at
    x=0 — wasted; raise hook — already at min; ACTION5 — no
    block under hook so no-op). After grabbing the top of stack,
    the decision space at "block in hand, hook still at y=39
    over column 4" = 3 plausible directions (release immediately,
    raise then traverse left or right). **Trivial post-discovery
    heuristic that fails**: *deliver the block whose target is
    closest to the trolley's current position*. From the start
    `trolley.x=0` the nearest target is `target_blue` at `x=23`
    (distance 23), then `target_yellow` at `x=43` (distance 43),
    then `target_red` at `x=57` (distance 57). The greedy
    "pick block_blue first, deliver it first" heuristic immediately
    breaks at action ~30: the player has lowered hook past
    `y=39` and ACTION2 is denied because `block_yellow` (top of
    stack) blocks further descent — `block_blue` cannot be reached
    until `block_yellow` is removed. **Where heuristic diverges
    from witness**: the heuristic says "lower past yellow to grab
    blue", the witness says "grab yellow first, deliver yellow,
    THEN lower for blue". The heuristic wastes some actions
    confirming the descent is blocked, then must re-converge on
    the witness's order. Crucially, the heuristic's choice does
    not lose the level, but it forces a re-plan that costs a few
    actions. The deeper planning challenge is realising that
    once stack-disassembly is forced, the order yellow → blue →
    red is fixed AND that each delivery's wall-crossing needs a
    full raise-traverse-lower cycle, so the player must
    interleave (raise, cross, lower, release, raise, return,
    lower, grab, ...) without forgetting which step is next over
    a long action sequence. The challenging aspect is the
    state-tracking under composition, not the discovery of a
    single rule.
  - **(d) Step budget**: 500 (1.6× witness's 319 — generous;
    matches the longer witness and reflects the L3-must-not-shrink
    rule of difficulty-rules.md § d).

## 5. Action mapping

`available_actions = [1, 2, 3, 4, 5]`. ACTION6 (click) and ACTION7
(undo) are NOT declared.

| Action | Semantic | Validity gate |
|---|---|---|
| ACTION1 (UP) | Raise hook by 1 cell (`hook.y -= 1`); rope shortens. | `hook.y > trolley.y + trolley.height` (rope length stays ≥ 0). |
| ACTION2 (DOWN) | Lower hook by 1 cell (`hook.y += 1`); rope lengthens. If carrying a block, the block also lowers (`block.y += 1`). | (a) `hook.y + hook.height < floor_y` (hook above floor); (b) cell `(hook.x..hook.x+hook.width-1, hook.y + hook.height)` is not blocked by any block (other than the one being carried); (c) when carrying, the carried block's bottom row at the new position is not at floor or against another block. If any check fails, the action is a no-op for that direction. |
| ACTION3 (LEFT) | Move trolley left by 1 cell (`trolley.x -= 1`). Hook + rope + carried block move with it. | (a) `trolley.x > 0`; (b) at the new position, the rope's column `trolley.x + 2` does NOT contain any wall cell at any row in `[trolley.y + trolley.h, hook.y - 1]`; (c) if carrying, the carried block at the new position does not overlap any wall cell. No-op if any fails. |
| ACTION4 (RIGHT) | Move trolley right by 1 cell. Symmetric to ACTION3. | Symmetric. |
| ACTION5 | TOGGLE grab/release. *If currently carrying*: detach the carried block; the block then falls under gravity until it rests on floor or atop another block. *Else*: if a block exists at `(hook.x..hook.x+hook.w-1, hook.y + hook.h)` (i.e. a block whose top row is one below hook bottom and whose x-range overlaps hook's x-range), grab it (set `self.carrying = block`). Otherwise no-op. | Always callable; the toggle's effect depends on game state. The "block directly below hook" check uses tag-based query `level.get_sprites_by_tag("block")` and pixel-overlap against the hook footprint. |

ACTION6 absent because all manipulation is positional via the
trolley/hook (no direct click-to-act primitive). ACTION7 absent
because there is no meaningful undo (per checklist 22 / global
action-enum strict-undo rule).

## 6. HUD and per-game state

**HUD widget — `StepCounterHud`** (subclass of
`RenderableUserDisplay`): a 32-cell wide horizontal bar centred on
row 63. Initialises with the level's `step_budget`; tracks
`current = step_budget - action_count`. Renders `current/budget`
proportion in palette `0` (white); empty cells are palette `4`
(off-black). Same template as cn04's `qdcvayjdkm` / sp80's
counter.

**Internal game-class state**:

- `self.trolley` — `Sprite` reference (always present).
- `self.hook` — `Sprite` reference.
- `self.rope` — `Sprite` reference; pixels regenerated each step
  (1×N column or `InteractionMode.REMOVED` if N=0).
- `self.carrying` — `Sprite | None`; the block currently held by
  the hook, or `None` if no block held.
- `self.walls` — `list[Sprite]`, populated in `on_set_level`.
- `self.blocks` — `list[Sprite]`, populated in `on_set_level`.
- `self.targets` — `list[Sprite]`, populated in `on_set_level`.
- `self.floor_y` — int, the floor row (58); used by physics.
- `self._step_counter_ui` — the HUD instance.

**Persistent visual cues** (per checklist 19, no hidden state):
- Hook's grab state is implicit in `self.carrying`'s presence:
  when carrying, the carried block is rendered at
  `(trolley.x, hook.y + hook.h)` — visually attached to the
  hook bottom, so the player sees "block hangs off hook". When
  not carrying, no block is below the hook.
- Hook position is always rendered at `(trolley.x, hook.y)` — the
  player always sees where the hook is.
- Rope length is rendered as a vertical column from
  `(trolley.x + 2, trolley.y + trolley.h)` to `(trolley.x + 2,
  hook.y - 1)`. The rope is a separate sprite.
- Step counter shows action budget remaining.

No other internal state is mutated by an action; therefore
checklist 19 is fully satisfied.

## 7. Win condition

Per `step()`, after handling ACTION1..5, run `_check_win()`:

```
for each target in self.targets:
    same_color_block = the unique block whose color tag matches the
                        target's color tag
    if same_color_block.x != target.x + 1: return False
    if same_color_block.y != 53: return False
    # both checks pass for this colour pair
return True
```

If `_check_win()` returns `True`, call `self.next_level()`.

Concretely:
- L1: `block_red.x == 44 and block_red.y == 53` (target_red at x=43,
  y=57; block fits with bottom on floor row 57 → block.y=53).
- L2: above AND `block_blue.x == 58 and block_blue.y == 53`.
- L3: all three blocks at their colour-paired target positions.

## 8. Lose condition

`_action_count >= step_budget` triggers `self.lose()`. No other
lose state — there is no hazard, no soft-lock (a player who places
a block at the wrong target column can grab it again and re-deliver,
within the budget).

## 9. Novelty note

### Closest taxonomy entries (the 25 reference games)

- **`wa30` (lock-drag-crate)** — closest in *delivery goal*. wa30
  has a walking pawn that latches to a crate; this game has no
  walking pawn at all and operates an overhead trolley/hook from
  above. Distinguishing rule: in wa30 the player IS the actor on
  the floor (4-pixel hops); in `hk7v` the player has no presence
  on the floor — every input drives the trolley/hook system. The
  rope-vs-wall constraint has no analogue in wa30, and the
  gravity-stacking mechanic is absent from wa30. Negative-
  similarity: shared on dim 3 (delivery goal) and dim 4 (step
  budget); diverges on dims 1, 2, 5, 6, 7, 8. < 3-dim threshold.

- **`cn04` (rotate-translate-jigsaw)** — partial overlap on the
  ACTION5-as-modal-verb idiom and click+arrow input pattern.
  Distinguishing rule: cn04's ACTION5 rotates a selected
  jigsaw piece; `hk7v`'s ACTION5 toggles grab/release on a
  hook. The whole verb cardinality differs (cn04 uses ACTION6
  click for selection; `hk7v` does not declare ACTION6 at all).

### Closest prior-games entries (`prior-games/index.md`)

- **`dj5h` (pulley-pair-platform)** — the only other prior with
  an "overhead" element. dj5h has *paired* hanging platforms
  (lifting one drops the other) and the player rides a platform.
  `hk7v` has a single rope-and-hook, no coupling, and no
  platform the player rides — the player is the trolley/hook
  operator and never appears on the playfield. Negative-
  similarity: shared dim 4 only.

- **`vt6q` (grapple-anchor-yank)** — fired grapple line.
  `vt6q`'s grapple line is *instantaneous* (single-tick fire-
  and-snap) and has a walking avatar that gets yanked. `hk7v`'s
  rope is *always present* and the hook crawls one cell per
  ACTION1/2 — there is no firing primitive and no avatar.

- **`nb6t` (hinge-chain-reach)** — articulated arm with hinges.
  Distinguishing rule: nb6t's reach is *angular* (rotate
  segments); `hk7v`'s reach is *Cartesian* (independent X/Y
  axes). nb6t's L3 has carry-and-drop, partial overlap on
  delivery goal — but the manipulator geometry is the
  fundamental divergence.

- **`pv5q` (pivot-rod-swing)** — radial reach via swinging rod.
  Same Cartesian-vs-radial divergence as nb6t. `pv5q`'s pawn
  is on the rod end and swings around a fixed pivot; `hk7v`'s
  hook is on the rope end and slides on independent X/Y axes.

- **`wb6n` (tether-pin-wrap)** — leash from a stake to a walking
  pawn. `wb6n`'s "rope" is a leash from a STAKE on the floor to
  a walking pawn; `hk7v`'s rope hangs from a movable trolley to
  a non-walking hook. wb6n has pin-replanting; `hk7v` has rope-
  vs-wall + gravity-stacking.

The candidate's visual signature (top horizontal beam, single
small trolley moving along it, vertical rope of variable length
hanging straight down to a hook, floor with coloured blocks and
horizontal coloured-stripe targets) is unique against every prior
in the index. Negative-similarity dimensions:

- Dim 1 (board): top-beam + vertical-rope + floor-blocks layout
  is unique to `hk7v`.
- Dim 2 (input): independent-X (trolley)+Y (rope) Cartesian is
  unique.
- Dim 3 (goal): "deliver coloured blocks to coloured targets" —
  shared with wa30, kf42, and several others, but cosmetic.
- Dim 4 (lose): step budget — universal.
- Dim 5 (cast): trolley + rope + hook is unique; supporting cast
  (blocks + targets + walls) is generic.
- Dim 6 (visual signature): top beam + rope + hook + floor with
  coloured stripes is unique.
- Dim 7 (pixel grain): blocks have 2-colour 5×5 internal grid
  pattern; trolley has multi-palette internal pattern; hook is
  U-shape; targets are 7×1 striped marker. All sprites have
  internal pattern (per checklist 20).
- Dim 8 (core dynamic): "operate Cartesian gantry under rope-
  clearance constraint with gravity-driven release stacking" —
  unique combination across the corpus.

Verdict: the candidate is novel against both the taxonomy and
prior-games index, with concrete distinguishing rules vs each of
the 6 closest priors above.

`prior-games/index.md` is NOT empty (63 prior rows); the index
checks above are based on its current contents.
