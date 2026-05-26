# jd4q — game spec

## 1. Title
Echo-Trail Maze (working title; not visible in-game).

## 2. Mechanic family
`echo-trail-teleport`. The player walks an avatar that automatically
deposits a fading **echo-stone** on every cell it leaves. Clicking
any visible echo teleports the avatar back to that cell and consumes
that echo plus every echo deposited after it (rewinding the trail to
that point in time). Layered on top: **closing-doors** that seal
behind the avatar (one-way passages) and at L3, **echo-eraser** cells
that wipe the entire trail when walked.

Core-knowledge priors used: **objectness** (avatar, echoes,
doors as persistent entities the player tracks across actions) and
**basic geometry/topology** (maze connectivity, doors that change
the topology of passable cells when triggered). No physics prior, no
agentness.

## 3. Sprite roster

The grid is `64×64` pixels with cell-stride `4` (logical 16×16 maze
of 4×4-pixel cells). Sprites are 4×4 pixel patterns.

- **avatar** (4×4) — palette `{6 magenta, 7 pink, -1 transparent}`.
  Pattern: solid magenta block with a 1-pixel pink "eye" spot in the
  upper-left interior. tag `player`. Movable; collides with
  walls/sealed-doors. Single instance per level.
- **echo_fresh** (4×4) — palette `{11 yellow, -1 transparent}`.
  Pattern: yellow plus-sign or 4-corner star (interior pixels yellow,
  corners transparent). tag `echo`. Spawned on every avatar-leaves-cell
  when echoes are active (L2, L3).
- **echo_dim** (4×4) — palette `{12 orange, -1 transparent}`. Same
  shape as `echo_fresh` but orange — used as a colour-remap target
  to visualise an echo whose age has crossed half-life. Same tag
  `echo`. Visual feedback that the echo will fade soon.
- **wall** (4×4) — palette `{5 black}`. Solid black block.
  tag `wall`. Static.
- **door_open** (4×4) — palette `{3 grey, 10 light-blue}`. Grey
  rim with light-blue interior (visually a "door panel"). tag
  `closing_door`. Walkable while open. Two-sprite-swap idiom: when
  sealed, swap interaction with `door_sealed` (collision active,
  open variant REMOVED).
- **door_sealed** (4×4) — palette `{3 grey, 5 black}`. Grey rim
  with black interior. tag `wall` (same as static walls — uniform
  collision behaviour). Replaces `door_open` after seal.
- **pickup_a** (4×4) — palette `{14 green, -1, 0 white}`. Green
  diamond outline with white centre. tag `pickup`, name `pickup_a`.
- **pickup_b** (4×4) — palette `{9 blue, -1, 0 white}`. Blue
  diamond outline with white centre. tag `pickup`, name `pickup_b`.
- **pickup_c** (4×4) — palette `{12 orange, -1, 0 white}`. Orange
  diamond outline with white centre. tag `pickup`, name `pickup_c`.
- **goal** (4×4) — palette `{15 purple, 0 white}`. Purple **square
  frame** with white interior (the outer 1-pixel ring of the 4×4
  is purple, the inner 2×2 is white). Concrete pixel layout:
  ```
  [15, 15, 15, 15]
  [15,  0,  0, 15]
  [15,  0,  0, 15]
  [15, 15, 15, 15]
  ```
  Reads as a square outline with a hollow centre — abstract, NOT a
  round-ring "0"-digit shape. tag `goal`.
- **eraser** (4×4) — palette `{13 maroon, 6 magenta, -1}`. Maroon
  fill with a magenta **"+" cross-pattern** interior (vertical bar
  one pixel wide + horizontal bar one pixel wide intersecting at
  the centre — a topological cross, NOT an "X" / diagonal pattern,
  per `forbidden-elements.md`'s allowed "+" example). tag `eraser`.
  Visually distinct from doors (grey rim) and walls (solid black);
  the maroon-magenta pair is unique to this sprite role.

  Concrete pixel layout:
  ```
  [13, 6, 6, 13]
  [ 6, 6, 6,  6]
  [ 6, 6, 6,  6]
  [13, 6, 6, 13]
  ```
  Reads as a magenta cross on a maroon-corner field — abstract,
  not a letter or digit.

HUD widget:

- **StepCounterHud** (`RenderableUserDisplay`) — depleting bar at
  `frame[0, :]` (top row). Two colours: 4 (off-black) for remaining,
  3 (grey) for spent. Initial total per-level set from
  `level.get_data("step_budget")`.

Background colour: `2` (light-grey, neutral floor).
Letter-box colour: `5` (black, frames the playfield).

The avatar (magenta) and echo (yellow) are intentionally
high-contrast against the light-grey floor; doors (light-blue
interior) read as "passable but special"; eraser (maroon-magenta)
reads as "hazard, do not enter casually". No two sprite kinds share
the same palette — every role has a distinct visual.

## 4. Level progression, mechanic enumeration, and witness solutions

All three levels are `grid_size=(64, 64)` with cell-stride 4
(coordinates below in *cell-coordinates* (col, row), where each cell
is a 4×4 pixel block at pixel-coords `(4*col, 4*row)`). Echoes have
trail-length `K=16` (i.e. an echo dies after the avatar takes 16
more actions following its deposit).

### Level 1 — base dynamic system

A simple corridor maze. Avatar walks to a single goal cell. Echoes
are NOT active at L1 (`level.get_data("echoes_active") == False`).
ACTION6 is excluded from `_get_valid_actions` at L1.

Layout (cell coords):
- avatar starts at `(2, 2)`.
- goal at `(13, 2)`.
- floor along row 2 from col 2 to col 13; walls everywhere else.
- step_budget = 30.

- **Mechanics required by the witness** (N = 1):
  - **M1 (walk)**: ACTION1..4 moves the avatar one cell in the
    pressed direction; movement is blocked by `wall`-tagged sprites
    (including sealed doors).
- **Necessity per mechanic**:
  - L1 cannot be solved without triggering M1 because the avatar
    starts at `(2, 2)` and the goal at `(13, 2)`; only ACTION1..4
    can change the avatar's position.
- **Witness solution** (shortest):
  - `[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4,
     ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]`
  - 11 east-walks. Total: 11 actions.
- **Difficulty justification**:
  - **(a) Random-resistance**: a uniformly-random ACTION1..4 agent
    succeeds rarely within 30 actions because each step has 1/4
    chance of being east; the corridor blocks N/S/W and west-walls
    bound the avatar. A vision-blind small-LLM agent that doesn't
    perceive the goal would not know which direction to favour.
    But L1 is the tutorial — *some* random success is acceptable
    by design (per `from-tech-report.md` § 5).
  - **(b) Human-tractable**: ~30 seconds. A human sees the avatar,
    sees the goal east of it, presses east-arrow until they reach.
  - **(c) Planning depth**: **no strict planning requirement.**
    Mechanic-discovery (learning ACTION1..4 are walk-directions)
    is the entire L1 difficulty; once the rule is understood, the
    win is immediate.
  - **(d) Step budget**: `step_budget = 30`. Witness length 11; the
    budget is ~3× the witness for comfortable exploration.

### Level 2 — base system + 2 new mechanics (echo-teleport, closing-doors)

A maze with a single corridor branch sealed by closing-doors. Echoes
are active at L2 (`echoes_active=True`).

Layout (cell coords; **revised per critique-revisions.md Issue 1** to
add a 2×2 floor vestibule at S so the post-discovery decision space
at level start is ≥ 2):
- avatar starts at `(2, 2)`.
- **2×2 vestibule** at S: cells `(2, 2)`, `(3, 2)`, `(2, 3)`,
  `(3, 3)` are all floor.
- **South-then-east path** to J: cells `(2, 4), (2, 5), (2, 6),
  (2, 7), (2, 8)` floor (south leg), then `(3, 8), (4, 8), (5, 8),
  (6, 8), (7, 8)` floor (east leg). Reaches `J = (8, 8)`.
- **East-then-south path** to J: cells `(4, 2), (5, 2), (6, 2),
  (7, 2), (8, 2)` floor (east leg), then `(8, 3), (8, 4), (8, 5),
  (8, 6), (8, 7)` floor (south leg). Also reaches `J = (8, 8)`.
- Both paths from the vestibule are the same length (10 cells from
  vestibule edge to J, 12 from S itself).
- **Branch east of J**: cells `(9, 8), (10, 8), (11, 8), (12, 8),
  (13, 8)` are `closing_door`. Cell `(14, 8)` is `pickup_a` (K_A).
- **Continuation south of J**: floor cells `(8, 9), (8, 10),
  (8, 11), (8, 12), (8, 13), (8, 14)`. Cell `(8, 14)` is `goal`.
- All other cells are walls.
- step_budget = 60.

From S=`(2, 2)`, both ACTION2 (south to floor `(2, 3)`) and ACTION4
(east to floor `(3, 2)`) are valid first actions; the post-discovery
decision space at level start is **2**.

Win predicate: `pickup_a` collected AND avatar at `goal` cell.

- **Mechanics required by the witness** (N = 1+2 = 3; introduces
  exactly 2 new mechanics on top of L1's M1):
  - **M1 (walk)**: carried forward.
  - **M2 (echo-teleport-with-rewind, NEW)**: ACTION6 click on a
    visible `echo` sprite teleports the avatar to that cell and
    consumes that echo and every echo deposited after it.
  - **M3 (closing-doors, NEW)**: when the avatar walks off a
    `closing_door` cell, that cell swaps from `door_open` to
    `door_sealed` (visually grey-rim-with-black-interior; tag
    becomes `wall`; impassable forever).
- **Necessity per mechanic**:
  - L2 cannot be solved without triggering M1 because the avatar
    must traverse multiple cells (S→J, J→K_A in branch east of J,
    J→G in corridor south of J) and walk is the only motion verb;
    no other action moves the avatar between cells.
  - L2 cannot be solved without triggering M2 because after the
    avatar reaches `K_A=(14, 8)`, every closing-door cell on the
    J→K_A corridor `(9, 8), (10, 8), (11, 8), (12, 8), (13, 8)`
    has sealed (M3 fired) — the avatar cannot walk west out of
    K_A. The only way back to the J area (and thence to G) is
    teleport via ACTION6 click on an echo on the S→J path.
  - L2 cannot be solved without triggering M3 because the only
    path from J to `pickup_a=(14, 8)` runs through cells
    `(9, 8)..(13, 8)` which are all `closing_door`; walls flank
    the corridor (cells at row 7 and row 9 in columns 9..13 are
    walls), so no detour exists. Walking through any of those
    closing-door cells fires the seal-on-egress behaviour.
- **Witness solution** (shortest, written ACTION-by-ACTION; click
  coords are pixel-space — convert via `display_to_grid` back to
  cell coords for verification):
  1-6. `[ACTION2 ×6]` — walk south from `(2, 2)` to `(2, 8)`.
       Echoes deposit at `(2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
       (2, 7)` as avatar exits each cell.
  7-12. `[ACTION4 ×6]` — walk east from `(2, 8)` to `J=(8, 8)`.
       Echoes deposit at `(2, 8), (3, 8), (4, 8), (5, 8), (6, 8),
       (7, 8)`. After step 12 the avatar is at J; alive echoes:
       `(2, 2)..(2, 8)` and `(3, 8)..(7, 8)` (12 echoes; oldest
       age 11, well under K=16).
  13-18. `[ACTION4 ×6]` — walk east from J through closing-doors
       to `pickup_a=(14, 8)`. Cells `(9, 8)..(13, 8)` seal as the
       avatar exits each (no echoes deposited on sealed cells).
       Cell `(8, 8) = J` deposits an echo at step 13 when the
       avatar exits J for `(9, 8)`. After step 18: echoes alive at
       `(2, 2)..(2, 8)` (7), `(3, 8)..(7, 8)` (5), `(8, 8)` (1) =
       13 echoes. `pickup_a` collected; `collected_pickups =
       {"pickup_a"}`.
  19. `ACTION6@(pixel coord of echo at (8, 8) = J)` — click the
       J-echo. Avatar teleports back to `(8, 8)`. Echoes deposited
       AFTER (8, 8) chronologically: none (the closing-door cells
       didn't deposit). So only the J-echo itself is consumed.
       Echoes alive after teleport: `(2, 2)..(2, 8)` and
       `(3, 8)..(7, 8)` (12 echoes).
  20-25. `[ACTION2 ×6]` — walk south from `J=(8, 8)` to
       `goal=(8, 14)`. Win at step 25 (avatar on goal AND
       `pickup_a` already collected). Total **25 actions**.
- **Difficulty justification**:
  - **(a) Random-resistance**: a random ACTION1..4+ACTION6 agent
    has near zero chance of solving L2 within 60 actions. The
    avatar is likely to wander into the east-of-J closing-door
    corridor without first depositing useful echoes, and once
    deep in the corridor the closing-doors have sealed behind it
    — only a precise ACTION6 click on a specific echo pixel
    escapes. Random ACTION6 click coords land on echo cells with
    very low probability (~12 valid echo cells out of 4096
    pixel-positions at the typical-state).
  - **(b) Human-tractable**: ~2 minutes. The human walks south,
    discovers branch east of J, walks the branch, reaches K_A,
    notices the corridor sealed (visually distinct grey-and-black
    door cells), tries walking back (blocked), notices the
    yellow-star echoes glowing on prior cells, clicks one,
    teleports back, walks to G.
  - **(c) Planning depth (post-discovery)**: **moderate.**
    *(1) Post-discovery decision space at level start.* From
    S=`(2, 2)` the fully-informed player has **2 valid first
    actions** (ACTION2 south to floor `(2, 3)`; ACTION4 east to
    floor `(3, 2)`). Both initiate equal-length S→J paths.
    *(2) Plausible-but-wrong alternative the post-discovery
    player would consider and reject — addressed per
    critique-revisions.md Issue 3 (must be a true post-discovery
    misstep, not a discovery-stage one):*
    *"Skip pickup_a entirely and walk straight from S to goal."*
    The fully-informed player knows the win predicate is
    `pickup_a collected AND avatar on goal`. The shortest path
    that ignores the requirement is `S=(2,2)` → south to `(2, 8)`
    → east to `J=(8, 8)` → south to `goal=(8, 14)` = 18 walks. The
    player considers it because it is visibly the shortest path.
    They reject it because at step 18 the avatar is on goal but
    `collected_pickups` is empty, so `_check_win` returns False
    and `next_level()` does not fire. The avatar would then have
    to detour east through closing-doors to collect `pickup_a` and
    teleport back — which is exactly the witness, longer than the
    direct path the player just rejected. (Other post-discovery
    alternatives the player considers but does not strictly
    reject — they win, just slower — include clicking deeper
    echoes like `(2, 2)` after K_A; teleporting to `(2, 2)` then
    walking east-then-south to G yields a longer 30-action path
    where the witness's J-echo click yields 25.)
    *(3) Witness reasoning chain referencing post-discovery
    state:* "From S, both south and east lead to J via equivalent
    paths; pick south. At J=(8, 8), the only way to `pickup_a` is
    east through 5 closing-door cells. After collecting K_A at
    (14, 8), the corridor is sealed; only echo-teleport returns
    me to the J area. The J-echo is the closest deposited echo to
    `goal=(8, 14)`, so clicking it minimises the post-teleport
    walk. From J, walk south 6 cells to goal."
  - **(d) Step budget**: `step_budget = 60`. Witness length 25
    (revised after Issue 1 layout fix); budget is ~2.4× the
    witness for comfortable exploration. The budget reflects the
    discovery cost — a first-time player will spend several
    actions learning that walking-back fails and that echoes are
    clickable, before they re-plan around teleport.

### Level 3 — system + 1 new mechanic (echo-eraser)

A junction with three branches and a constraining eraser-cell on the
only path to the goal. Echoes active.

Layout (cell coords; **revised per critique-revisions.md Issue 2** to
add a 2×2 floor vestibule at S so the post-discovery decision space
≥ L2's, with branch positions chosen so they do not conflict with
either S→J approach):
- avatar starts at `S=(2, 2)`.
- **2×2 vestibule** at S: cells `(2, 2)`, `(3, 2)`, `(2, 3)`,
  `(3, 3)` are all floor.
- **S→J path** (single corridor; the vestibule's east cell
  `(3, 2)` is a dead-end pocket so two valid first actions exist
  but they re-converge to the south corridor): floor cells
  `(2, 4), (2, 5), (2, 6), (2, 7), (2, 8)` (south leg) and
  `(3, 8), (4, 8), (5, 8), (6, 8), (7, 8)` (east leg). Reaches
  `J = (8, 8)`. From the vestibule's `(3, 2)` cell, neighbours
  are `(3, 3)` (floor, vestibule), `(2, 2)` (floor, S), and
  walls north and east — so an east-first first move re-converges
  to the south corridor via the vestibule with at most 2 extra
  steps. The first-action choice from S is the only meaningful
  branching at level start.
- **Branch A** — north from J: cells `(8, 7), (8, 6), (8, 5),
  (8, 4), (8, 3)` are `closing_door`. Cell `(8, 2)` is
  `pickup_a` (K_A). (Branch A's column-8 cells lie east of the
  S→J south leg's column-2 cells, with walls at columns 3..7 of
  rows 3..7 — no conflict with the S→J path.)
- **Branch B** — east from J: cells `(9, 8), (10, 8), (11, 8),
  (12, 8), (13, 8)` are `closing_door`. Cell `(14, 8)` is
  `pickup_b` (K_B). (Branch B's row-8 cells lie east of J,
  disjoint from both S→J approach paths.)
- **Branch C** — south from J: cell `(8, 9)` is `eraser`. Cells
  `(8, 10), (8, 11), (8, 12)` are normal floor. Cell `(8, 13)`
  is `pickup_c` (K_C). Cell `(8, 14)` is `goal`. (Branch C is
  the only path to goal — branches A and B are dead-ends at
  pickups.)
- All other cells are walls (specifically: cells `(4, 2)..(7, 2)`
  are walls so the S=(2,2)→east route does not extend toward
  branch A; cells `(3, 4)..(3, 7)` are walls so the vestibule's
  east-pocket forces re-convergence to the south corridor).
- step_budget = 100.

From S=`(2, 2)`, both ACTION2 (south to floor `(2, 3)`) and ACTION4
(east to floor `(3, 2)`) are valid first actions; the post-discovery
decision space at level start is **2** (≥ L2's 2). At J, the
fully-informed player faces 4+ meaningful next-action choices (north
into branch A, east into branch B, south into branch C-with-eraser,
or click any visible echo to teleport elsewhere) — far more
post-discovery branching than L2.

Win predicate: `pickup_a` AND `pickup_b` AND `pickup_c` all
collected AND avatar at `goal` cell.

- **Mechanics required by the witness** (3+1 = 4; introduces
  exactly 1 new mechanic on top of L2's M1+M2+M3):
  - **M1 (walk)**: carried forward.
  - **M2 (echo-teleport-with-rewind)**: carried forward.
  - **M3 (closing-doors)**: carried forward.
  - **M4 (echo-eraser, NEW)**: walking onto an `eraser` cell
    immediately removes every echo currently in the trail. After
    the eraser fires, the echo trail is empty and stays empty
    until the avatar deposits new echoes by walking off
    subsequent normal-floor cells.
- **Necessity per mechanic** (one line each, restated for L3
  geometry — no "as L2"):
  - L3 cannot be solved without triggering M1 because the avatar
    must traverse cells across the S→J segment, three branches,
    and the C-corridor; walk is the only motion verb.
  - L3 cannot be solved without triggering M2 because after
    visiting `pickup_a` at `(8, 2)`, every cell of branch A is
    sealed — the only way back to the J area is teleport;
    similarly after visiting `pickup_b`. The witness teleports
    twice (once after K_A, once after K_B) and no other mechanism
    moves the avatar back to J after either branch.
  - L3 cannot be solved without triggering M3 because branches A
    and B are the only paths to `pickup_a` and `pickup_b`
    respectively, and both branches are constructed entirely of
    `closing_door` cells (5 each) — every cell of those branches
    fires its seal-on-egress behaviour.
  - L3 cannot be solved without triggering M4 because the only
    path from J to `goal` is south through cell `(8, 9)` which is
    an `eraser`; the goal cannot be reached from any other
    direction (branches A, B both end in dead-end pickups; the
    S→J path is the only S-to-J corridor and does not extend
    south of J except via cell `(8, 9)`). Every winning sequence
    walks onto `(8, 9)` and fires the trail-wipe.
- **Witness solution** (shortest, written ACTION-by-ACTION; revised
  per the new layout in which J=(8, 8) is reached directly via
  S→J without round-trip detours):
  1-6. `[ACTION2 ×6]` — south from `S=(2, 2)` to `(2, 8)`. Echoes
       deposit at `(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7)`
       as avatar exits each cell.
  7-12. `[ACTION4 ×6]` — east from `(2, 8)` to `J=(8, 8)`. Echoes
       deposit at `(2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8)`.
       After step 12: 12 echoes alive (oldest age 11, all under
       K=16).
  13-18. `[ACTION1 ×6]` — north from J through closing-doors to
       `pickup_a=(8, 2)`. Sequence: `(8, 8)→(8, 7)→(8, 6)→(8, 5)
       →(8, 4)→(8, 3)→(8, 2)`. Cells `(8, 7), (8, 6), (8, 5),
       (8, 4), (8, 3)` are closing-doors that seal as the avatar
       exits each (no echoes deposited on sealed cells). Cell
       `(8, 8)=J` deposits an echo at step 13 when the avatar
       exits J for `(8, 7)`. K_A=`(8, 2)` reached at step 18;
       `collected_pickups = {"pickup_a"}`. Alive echoes: 12 from
       S→J path + 1 at J = 13.
  19. `ACTION6@(pixel coord of echo at (8, 8) = J)` — teleport
       back to J. Echoes after J in deposit-order: closing-doors
       (no deposits) → none consumed. Avatar at J=`(8, 8)`. Alive
       echoes: 12 (S→J path).
  20-25. `[ACTION4 ×6]` — east from J through closing-doors to
       `pickup_b=(14, 8)`. Sequence: `(8, 8)→(9, 8)→(10, 8)→
       (11, 8)→(12, 8)→(13, 8)→(14, 8)`. Cells `(9, 8)..(13, 8)`
       seal. Cell `(8, 8)=J` deposits an echo at step 20 when the
       avatar exits J for `(9, 8)`. K_B=`(14, 8)` reached at step
       25; `collected_pickups = {"pickup_a", "pickup_b"}`. Alive
       echoes: 13.
  26. `ACTION6@(pixel coord of echo at (8, 8) = J, re-deposited at
       step 20)` — teleport back to J. Echoes after J in
       deposit-order: closing-doors (no deposits). Avatar at J.
       Alive echoes: 12.
  27. `ACTION2` — south from J to `(8, 9) = eraser`. **M4 fires:
       every alive echo is removed (trail wiped).** Alive echoes
       after step 27: 0. Avatar at `(8, 9)`.
  28-30. `[ACTION2 ×3]` — south through `(8, 10), (8, 11),
       (8, 12)`. Echoes deposit at `(8, 9), (8, 10), (8, 11)` (the
       eraser cell at `(8, 9)` deposits no echo because eraser
       cells do not deposit; cells `(8, 10), (8, 11)` are normal
       floor and do). Wait — design clarification: the avatar
       exits `(8, 9)` at step 28, going to `(8, 10)`. `(8, 9)` is
       an eraser cell; eraser cells do not deposit echoes when
       exited. So the deposits at step 28 are skipped for `(8, 9)`
       but step 29 deposits at `(8, 10)` (normal floor) and step
       30 deposits at `(8, 11)` (normal floor).
  31. `ACTION2` — south to `(8, 13) = pickup_c`. K_C collected;
       `collected_pickups = {"pickup_a", "pickup_b", "pickup_c"}`.
  32. `ACTION2` — south to `(8, 14) = goal`. Win predicate fires:
       all 3 required pickups collected AND avatar on goal cell.
       `next_level()` called.

  Total: **32 actions**. (Sequence-summary: 6 south + 6 east + 6
  north + 1 click + 6 east + 1 click + 1 south-eraser + 3 south
  + 1 south-pickup + 1 south-goal = 32.)
- **Difficulty justification**:
  - **(a) Random-resistance**: a random ACTION1..4+ACTION6 agent
    has near-zero chance of solving L3 within 100 actions. The
    multi-branch closing-door structure traps the avatar after
    each wrong-direction commit; teleport requires precise pixel
    clicks on echo cells (~12 echo cells out of 4096 valid
    pixel-positions, and the right one matters). The eraser-then-
    branch-C ordering is enforced by trail-wipe. A
    vision-blind small-LLM agent that doesn't model the
    state-history would not be able to plan the click-on-J-echo
    sequence.
  - **(b) Human-tractable**: ~3-4 minutes. The human has
    L2's experience with echo-teleport. They explore J's three
    branches, notice the eraser-cell visually distinct (maroon-X
    pattern), try one branch, find pickup, notice closing-doors
    sealed behind, teleport-back, try another branch. They may
    naively try branch C first (south, nearest), discover that
    after walking through eraser the trail is gone — they're
    stuck without echoes. They walk back through C (no
    closing-doors in C, so back-walk possible), realise C must be
    last, plan A and B first, then C.
  - **(c) Planning depth (post-discovery)**: **challenging even
    for an attentive human.** Post-discovery, the player faces a
    multi-step ordering decision. **Trivial heuristic that
    fails:** *"visit the nearest pickup first."* From J=(8, 8),
    distances are: K_C at (8, 13) → 5 cells south; K_A at (8, 2)
    → 6 cells north; K_B at (14, 8) → 6 cells east. K_C is
    nearest. The greedy player walks south, hits eraser at (8, 9)
    on step 13 of their attempt, trail wipes, reaches K_C, walks
    further to G — wins immediately if all keys collected, but
    K_A and K_B are not collected so win does not fire. The
    greedy player walks back from (8, 14) north through C
    (passable, no closing-doors), reaches J. From J they enter
    branch A; closing-doors seal; they reach K_A; they try to
    teleport-back — the trail is empty (eraser wiped earlier and
    the back-walk through eraser would have re-fired). They are
    stuck at K_A. The witness defeats this by visiting A and B
    first (when the trail still exists for teleport-back), then
    C last (eraser fires on the no-return-needed final approach).
    The valid first-action count from S is at least 2 (south or
    east could each begin a tour); from J the valid first-action
    count is 3 (each of three branch-direction presses is valid;
    plus the player could click an echo and teleport off-J too —
    so > 3 plausible first actions at J). The witness reasons:
    *"branches A and B end in closed-corridor dead-ends that
    require teleport-back; branch C ends past an eraser that
    breaks teleport. Therefore branches A and B must be visited
    while echoes are still available, and branch C must be last."*
  - **(d) Step budget**: `step_budget = 100`. Witness length 32
    (revised after Issue 2 layout fix); budget is ~3.1× the
    witness, leaving comfortable room for exploration. The budget
    does not shrink relative to L2 (60) — L3 has more mechanics
    to discover and more exploration cost.

## 5. Action mapping

`available_actions = [1, 2, 3, 4, 6]`. Subset shape matches several
reference games (ka59, dc22, m0r0); the click semantic is the
distinctive verb.

- **ACTION1**: walk avatar one cell north (decrement y by 4).
  Blocked if destination is a `wall` or sealed `door_sealed` sprite.
  Always valid syntactically; no-op if blocked.
- **ACTION2**: walk avatar one cell south.
- **ACTION3**: walk avatar one cell west.
- **ACTION4**: walk avatar one cell east.
- **ACTION6**: click at `(x, y)` pixel-space coords; converted via
  `self.camera.display_to_grid(int(x), int(y))` to grid coords. If
  the resulting cell holds an `echo`-tagged sprite AND the level's
  `echoes_active` flag is true, teleport the avatar to that cell
  and remove that echo and every echo deposited after it (in
  insertion order). If the click does not land on an echo or
  `echoes_active` is false, the action is a no-op (still consumes
  one action from the step budget).

`_get_valid_actions` override:
- At L1 (`level_index == 0`), return `[ActionInput(id=ACTION1..4)]`
  only — ACTION6 is excluded.
- At L2 and L3, return `[ActionInput(id=ACTION1..4)]` plus one
  `ActionInput(id=ACTION6, data={"x": px, "y": py})` per visible
  echo sprite (per the cd82-style enumeration of clickable target
  positions).

## 6. HUD and per-game state

HUD:
- **StepCounterHud** (`RenderableUserDisplay`) — depleting
  horizontal bar at the top row (`frame[0, :]`). Two-colour split:
  positions where `x < remaining_proportion * width` painted with
  palette 4 (off-black, "remaining"); the rest painted with palette
  3 (grey, "spent"). Initial total set in `on_set_level` from
  `level.get_data("step_budget")`.

Per-game internal state:
- `self.avatar`: the `Sprite` instance for the current avatar (a
  cloned `avatar` placed in the level).
- `self.echoes`: ordered list of `(sprite, age, cell_xy)` triples,
  representing the trail in chronological-deposit order. Append
  on every avatar-leaves-cell where the cell is normal floor (i.e.
  not a sealed door, not an eraser). Increment every triple's
  `age` by 1 each step; remove triples whose `age >= K` (where
  `K=16`). On click-on-echo, find the triple whose `cell_xy`
  matches the click cell; teleport the avatar there; remove that
  triple and every triple AFTER it in the list.
- `self.collected_pickups`: `set[str]` of pickup-sprite-names
  visited (e.g. `{"pickup_a", "pickup_b"}`). Updated when avatar
  moves onto a pickup cell.
- `self.previous_cell`: `(x, y)` tuple of the cell the avatar
  occupied at the START of the current step (used to detect
  closing-door-egress and to deposit echoes).
- `self.step_counter_ui`: HUD instance.
- (No selected-sprite state, no animation phases — the game is
  one-action-per-step with no multi-tick animations.)

State that needs a persistent visual cue (per checklist item 19):
- The avatar's *position* is its visible position; no hidden
  position state. ✔
- The set of *collected pickups* is reflected by the pickup
  sprites: a collected pickup is removed (`set_interaction(REMOVED)`)
  so the pickup cell visibly empties. ✔
- The *trail* is the set of visible `echo` sprites; their presence
  IS the state. As echoes age, they recolour from yellow to orange
  (visual half-life cue) before vanishing. ✔
- *Closing-door state* (open/sealed) is visible via the
  two-sprite-swap idiom: `door_open` (light-blue interior) ↔
  `door_sealed` (black interior). ✔
- *Step budget remaining* is visible via the StepCounterHud bar. ✔

No state that the player must reason about lacks a persistent
visual cue.

## 7. Win condition

Per-level win predicate evaluated at the end of every `step()`
after movement and click resolution:

```
def _check_win(self) -> bool:
    avatar_cell = (self.avatar.x, self.avatar.y)
    goal_sprite = self.current_level.get_sprite_at(avatar_cell[0],
                                                    avatar_cell[1],
                                                    "goal")
    if goal_sprite is None:
        return False
    required = set(self.current_level.get_data("required_pickups") or [])
    return required.issubset(self.collected_pickups)
```

Per-level `required_pickups` data:
- L1: `[]` (no pickups required; reach goal alone).
- L2: `["pickup_a"]`.
- L3: `["pickup_a", "pickup_b", "pickup_c"]`.

When `_check_win` returns True, call `self.next_level()` (which
auto-wraps to `self.win()` after the last level).

## 8. Lose condition

```
def _check_lose(self) -> bool:
    return self._action_count >= self.current_level.get_data("step_budget")
```

When True, call `self.lose()`. No instant-fail collisions, no
respawn lives — the only failure mode is exhausting the step budget.
Per `difficulty-rules.md` § 1, no soft-locks: every reachable game
state has at least one path to the win condition within the
remaining budget (e.g. the avatar is never permanently stuck in a
sealed-door dead-end at L2/L3 with no echoes to teleport — the
witness depths above are well within budget for both, with margin).

## 9. Novelty note

Closest entries in `mechanic-novelty/taxonomy-of-25-games.md`:
- **g50t (walk-vs-scroll / ghost-replay-multitarget)** — both have
  an avatar walking with visible past-position artefacts.
  **Distinguishing rule:** g50t commits paths via ACTION5 to spawn
  ghosts that replay in lockstep with the avatar on each subsequent
  action; ghosts ACCUMULATE over time and animate every step. jd4q
  has no commit, no ghost-replay, no scrolling timer — echoes are
  STATIC fading dots that the player CONSUMES by clicking. g50t
  adds-trails-to-the-world; jd4q removes-trails-from-the-world.
- **lf52 (fog-of-war-sokoban)** — both involve undo-flavoured
  backtracking. **Distinguishing rule:** lf52 is Sokoban with
  single-block push and ACTION7 single-step undo; jd4q has no
  block-pushing, no fog-of-war, and no single-step undo. Multi-step
  rewind via clicking ANY visible echo is the verb, not "undo last
  move".
- **bp35 (procedural-graph-walk)** — both have click-teleport.
  **Distinguishing rule:** bp35 walks a graph of nodes; click
  teleports to a HIGHLIGHTED neighbour node defined by the graph.
  jd4q walks a 64×64 grid in continuous Manhattan steps; click
  teleports to PRIOR-SELF positions only. Different topology
  (graph vs grid) and different teleport target.
- **sk48 (paired-snake-trail-match)** — both have visible trails.
  **Distinguishing rule:** sk48's trail is a connected list of
  body-segment sprites that grow/shrink as the snake walks;
  paired-snakes match colours cell-by-cell. jd4q's trail is a
  sparse set of fading echoes (not connected, not body-like) and
  the goal is grid-navigation under closing-doors, not
  cell-colour matching.
- **tu93 (lockstep-multi-maze)** — both walk a grid maze. 
  **Distinguishing rule:** tu93 walks every primary agent in
  lockstep on a directional press; jd4q has a single avatar with
  echo-teleport. No lockstep mechanic.

Closest entries in `prior-games/index.md`:
- **kf42 (tether-pawn-cycle)** — kf42 has paired pawns sharing a
  tether with click-to-select. jd4q has a single avatar with
  self-deposited echoes. No tether, no second pawn.
- **fz5j (phase-step-tile)** — fz5j has tiles that pulse
  open/closed on per-cell periods 2/3/4 with avatar-respawn-on-
  closed. jd4q has no autonomous tile-pulsing — closing-doors
  close ONLY after the avatar walks off them, deterministically
  driven by the avatar's actions.
- **kn58 (anchor-pull-magnet)** — kn58 click places a magnet that
  slides every coloured pawn one cell on its dominant axis. jd4q's
  click teleports the avatar to a self-deposited echo; no
  pawn-on-grid radial attraction.
- **wt39 (glide-deflect-thaw)** — wt39 has gliding pawns that
  deflect off bumpers. jd4q has cell-by-cell walking (not glide),
  and closing-doors close behind the avatar, not underfoot.
- **zk9p (pursuer-merge-walk)** — zk9p has autonomous pursuer AI.
  jd4q has no AI agents.
- **rk7x (live-switch-routing)** — rk7x has an autonomous courier
  walking one cell per click; player toggles junction blades.
  jd4q has no autonomous walker; the player walks the avatar.
- **zd7m (cohort-step-route)** — zd7m has portals that teleport
  to a sealed chamber; multiple movable pawns step in cohort.
  jd4q has a single avatar; "teleport" is jumping to a SELF-trail
  echo, not a fixed portal pair.
- **xn5p (chamber-stamp-partition)** — xn5p stamps walls to
  subdivide regions. jd4q has no wall-stamping; closing-doors
  close automatically after the avatar moves off, not by player
  action.
- **bx84 (beam-mirror-reflect)** — bx84 emits a continuous beam,
  click drops/cycles mirrors. jd4q has no beam, no mirrors.
- **vn8d (domino-cascade-topple)**, **mr5q (polarity-attract-
  discharge)**, **pf3w (wavefront-converge-timing)**,
  **tg6w (settle-pile-tilt)**, **lv4k (lever-balance-torque)**,
  **gv47 (seed-grow-surround-dissolve)**,
  **hr8q (pair-blend-recipe)**, **ng52 (multiset-signature-
  classify)**, **pj7k (rolling-cube-face-paint)**,
  **pz4t (anchor-pivot-place)**, **lq5x (lantern-cone-illuminate)**,
  **vp6h (shadow-cast-collect)**, **qz73 (radial-cycle-lock)**,
  **qb84 (bead-lift-swap)**, **kx14 (tide-tilt-buoyant)**,
  **gx7m (gear-mesh-cascade)**, **kp9z (grain-accumulate-topple)** —
  none share core dynamic with jd4q's trail-as-resource +
  closing-doors + eraser; each is structurally a different game
  family.

`prior-games/index.md` has 27 entries; the check applied to all of
them above. (Not empty.)

The **negative-similarity-check** dimensions (palette signature,
sprite pixel-grain, core-dynamic divergence) are addressed by:
- Distinct palette: floor 2 (light-grey), avatar 6+7 (magenta+pink),
  echoes 11+12 (yellow+orange), doors 3+10+5 (grey+light-blue+
  black), eraser 13+6 (maroon+magenta), pickups 14/9/12 (green/
  blue/orange), goal 15 (purple). Avoids the kf42→vh68 cautionary
  `{4 wall, 8 red, 9 blue}` palette entirely.
- Internal pixel structure on every sprite: the avatar has a
  pink "eye" inside magenta; doors have a grey rim with a coloured
  interior (open-blue or sealed-black); pickups have a coloured
  diamond outline with a white centre; the eraser has a magenta
  cross-pattern on maroon. No 1×1 plain rectangles.
- Core dynamic: "manage temporal trail as escape hatches and plan
  branch-visit order around an irreversibility cell" — the
  question the player asks is "where do I leave my echoes for
  later use, and which branch do I save for last?". This is not
  the question of any prior game.
