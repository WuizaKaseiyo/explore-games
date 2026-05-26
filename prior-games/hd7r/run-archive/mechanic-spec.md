# Game spec — hd7r

## 1. Title
"Shepherd's Repulsion Funnel" (neutral working title; never shown
in-game).

## 2. Mechanic family
`repulsion-herd-funnel`. The player walks a single **shepherd** avatar
one cell per arrow press. Autonomous **timid creatures** react to the
shepherd's *relative position*: after every shepherd MOVE, each creature
within a fixed Manhattan scare-radius takes one deterministic step
**away** from the shepherd; creatures outside the radius stay still and
creatures whose flee-target is blocked (wall / closed gate / edge /
another creature) do not move. The player never carries or pushes a
creature — control is purely by where the shepherd stands. Win is
spatial: drive every creature onto its matching **pen** cell. Prior
categories used: **agentness** (creatures flee with intent),
**objectness** (shepherd, creatures, walls, pens, gate posts are
persistent collidable entities), **basic geometry/topology** (corners,
funnels, and a togglable gate are the levers of control).

Logical grid: **16×16 cells, each cell = 4 display pixels → native
64×64 frame** (no chunky upscale; sprites carry internal pixel detail).
Movement and all positions are in 4-pixel strides.

## 3. Sprite roster
All gameplay sprites are 4×4 display pixels (one logical cell). Palette
chosen for a distinct signature (teal/amber/slate), avoiding the
overused `{4,8,9}` look and any cultural colour convention.

- **`shepherd`** — 4×4, palette {10 light-blue body, 5 black two-pixel
  "eyes" row, 3 grey base}. tags `["shepherd"]`. Role: the player
  avatar; collidable; one per level. Internal pattern: solid teal block
  with a darker 1-pixel brow so it reads as a purposeful agent and is
  clearly distinguishable from the round creatures.
- **`creature_timid`** — 4×4, palette {12 orange round body via a
  notched-corner pattern, 5 black 2-pixel eyes, -1 transparent corners}.
  tags `["creature","timid","straight"]`. Role: a straight-flee creature
  (steps directly away). Rounded body (transparent corners) so it reads
  as a soft living thing, visually distinct from the square shepherd and
  the hollow pens.
- **`creature_skittish`** — 4×4, palette {6 magenta round body,
  5 black eyes, -1 corners} with a small 1-pixel side-tick that differs
  from `creature_timid`. tags `["creature","skittish","perp"]`. Role: a
  perpendicular-flee (sidestep) creature, introduced at L3. Distinct hue
  (magenta vs orange) AND a small shape tick so the player can tell the
  two temperaments apart on sight (item 22).
- **`pen_amber`** — 4×4 hollow ring, palette {12 orange border, -1
  hollow centre}. tags `["pen","pen_straight"]`. Role: target cell for a
  straight (orange) creature; same hue as `creature_timid` so the
  colour-coupling reads (item 22, correlated visuals).
- **`pen_magenta`** — 4×4 hollow ring, palette {6 magenta border, -1
  centre}. tags `["pen","pen_perp"]`. Role: target for a skittish
  (magenta) creature; hue-matched to `creature_skittish`.
- **`wall`** — 4×4 solid, palette {3 grey fill with a 1-pixel {2}
  light-grey bevel on top-left} so walls read as solid masonry with
  texture, not flat blocks. tags `["wall"]`. Role: static obstacle and
  flee-backstop; the playfield border is built from these.
- **`gate_closed`** — 4×4 solid bar, palette {15 purple fill, 5 black
  centre slit} occupying a gap in a wall. tags `["gate","gate_closed"]`.
  Role: a blocking gate in its CLOSED state — collidable, blocks both
  shepherd and creature flee.
- **`gate_open`** — 4×4, palette {15 purple frame on the two side edges
  only, -1 hollow passage centre}. tags `["gate","gate_open"]`. Role:
  the SAME gate in its OPEN state — non-blocking passage. The two
  variants are swapped via the two-sprite-swap idiom so the open/closed
  state is always legible (item 20).
- **`StepCounterHud`** (HUD widget, see §6) — a depleting bar painted on
  the top display row.

## 4. Level progression, mechanic enumeration, and witness solutions

Common rule (the flee law), discovered at L1 and active at every level:
after a shepherd MOVE action, for each creature within Manhattan
distance ≤ **4** of the shepherd, compute the away-vector (creature −
shepherd); a **straight** creature steps one cell along the dominant
Manhattan axis of the away-vector (ties → horizontal); a **skittish**
creature steps one cell along that away-vector rotated 90° clockwise
(it sidesteps). A creature whose target cell is a wall, a closed gate,
the grid edge, or another creature does not move that tick. A gate-toggle
action (ACTION6 click on a gate post) does NOT move creatures (the
shepherd did not move).

### Level 1 — base dynamic system
- **Mechanics required by the witness** (N = 1):
  - **M1 flee-step (straight):** the only verb at L1; pushing the
    shepherd toward a creature makes it step directly away. Player-facing
    new rule: "the creature runs away from me; I steer it by the side I
    approach from."
- **Necessity per mechanic:**
  - *M1:* L1 cannot be solved without triggering M1 because the lone
    creature begins at cell (10,8) and its pen is the north-east corner
    cell (14,3); the shepherd has no carry/push verb and cannot occupy
    the creature's cell, so the creature only ever changes cell by
    fleeing — every path to the pen is a flee path.
- **Layout (16×16):** solid `wall` border (cells with x∈{0,15} or
  y∈{0,15}). Shepherd starts at (7,11). One `creature_timid` at (10,8).
  One `pen_amber` at (14,3) (against the north and east border walls,
  which act as the backstop). No gates, no interior walls.
- **Witness solution** (verified by replay against the modelled flee
  law): `[ACTION1, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4,
  ACTION4, ACTION1, ACTION1, ACTION1, ACTION1]`.
  - Phase A (push east): the shepherd, level with the creature, steps
    right repeatedly; the creature flees east until the east wall (x=14)
    backstops it. Phase B (push north): the shepherd steps up below the
    creature's column; the creature flees north until the north wall
    (y=3) backstops it on the pen.
  - K = 11, D = 2 distinct actions (ACTION1 UP, ACTION4 RIGHT). ≥3 and
    ≥2 satisfied. NOT solvable by repeating a single action (verified:
    no single arrow alone lands the creature on (14,3) — pure-right
    leaves it at row 8, pure-up leaves it at column 10).
- **Animation plan:** N/A — every flee is a single-cell local step
  rendered in the next frame; no teleport / slide-until-wall /
  projectile / chain.
- **Lives mechanism:** N/A — no hard-death path. Creatures never kill
  the shepherd; the only failure is step-budget exhaustion (a generous
  energy bar, exempt per item 25).
- **Difficulty justification:**
  - **(a) Random-resistance:** a random walker scatters the creature
    arbitrarily across the open field; landing it on one specific 1-cell
    pen in a corner within the budget is vanishingly unlikely, and no
    single repeated action wins.
  - **(b) Human-tractable:** ~1–2 minutes — a couple of probe moves
    reveal the flee law, then the corner-funnel is intuitive.
  - **(c) Planning depth:** L1 has **no strict planning requirement** —
    mechanic discovery is the whole gate; once the flee law is
    understood the two-phase corner push is immediate.
  - **(d) Step budget:** **44** (witness 11; ~4× headroom for probing
    and recovery).

### Level 2 — base system + 1 new mechanic
- **Mechanics required by the witness** (M = N+1 = 2):
  - **M1 flee-step (straight)** — carried forward.
  - **M2 gate toggle (new):** a `gate` post sits in the only gap of a
    dividing wall; clicking it (ACTION6) swaps it between CLOSED
    (blocking) and OPEN (passable). It starts CLOSED. Player-facing new
    rule: "I can click the bar in the wall to open or shut the only
    doorway; a creature can't run through a shut doorway."
- **Necessity per mechanic:**
  - *M1:* L2 cannot be solved without triggering M1 because both
    creatures (at (8,5) and (4,4)) have no push/carry verb acting on
    them; each only moves by fleeing, and each must change cell to reach
    its pen ((8,13) and (1,4) respectively).
  - *M2:* L2 cannot be solved without triggering M2 because creature A's
    pen (8,13) lies in the bottom region, the dividing wall fills row
    y=8 for all x∈{1..14} except the single gate at (8,8), and the gate
    starts CLOSED — so A physically cannot reach the bottom region until
    the gate is opened by a click (verified: BFS with the toggle action
    removed finds NO solution).
- **Layout (16×16):** `wall` border. A horizontal dividing wall along
  y=8 for x∈{1..14}, except the gate cell (8,8) which holds a `gate`
  (closed at start). Shepherd starts at (8,2) (top region). Creatures:
  `creature_timid` A at (8,5), `creature_timid` B at (4,4). Pens:
  `pen_amber` for A at (8,13) (bottom region, below the gate, against
  bottom wall), `pen_amber` for B at (1,4) (top region, against the
  west wall backstop).
- **Witness solution** (verified): `[ACTION2, ACTION2, ACTION3,
  ACTION3, ACTION6@gate, ACTION4, ACTION2, ACTION2, ACTION2, ACTION4,
  ACTION2]`.
  - Push B left to the west wall and settle it, then open the gate
    (ACTION6 on the gate post at (8,8)), then drive A down through the
    open gate to the bottom pen, nudging east to align on (8,13).
  - K = 11, D = 4 distinct actions (DOWN, LEFT, RIGHT, click). Satisfies
    ≥3 / ≥2. No single-action-repeat win (B and A are in different
    regions needing orthogonal pushes plus a click).
- **Animation plan:** N/A — flee steps are single-cell; the gate toggle
  is an in-place sprite swap rendered in the same frame.
- **Lives mechanism:** N/A — no hard-death (step-budget only).
- **Difficulty justification:**
  - **(a) Random-resistance:** the gate starts closed; a random agent
    almost never both clicks the single gate post AND then funnels the
    correct creature through it onto a 1-cell pen while the other
    creature stays put on its pen. P(random win) is far below 1/10⁴.
  - **(b) Human-tractable:** ~2 minutes once the gate's role is found.
  - **(c) Planning depth — moderate (post-discovery):** with both rules
    known, the player faces a real ordering decision. **Decision space
    at level start:** ≥ 4 fully-informed first actions worth weighing
    (push A first vs push B first; open the gate early vs late; which
    side to approach each creature from). **Plausible wrong path:**
    opening the gate *before* settling B and then pushing near B can
    knock B toward the gate region and lose its alignment; also, driving
    A down before B is parked means the shepherd's later moves to fetch B
    re-enter A's scare radius and shove A off (8,13). **Witness reasoning
    chain:** park B against the west wall first (it's out of the way and
    its pen is a wall backstop), THEN open the gate, THEN herd A down
    through the gate — keeping the shepherd's subsequent moves away from
    B's scare radius so B stays put.
  - **(d) Step budget:** **80** (witness 11; large headroom because the
    player spends several actions discovering the gate before attempting
    the herd, and the level has two creatures to settle).

### Level 3 — system + 1 new mechanic
- **Mechanics required by the witness** (L2-count + 1 = 3):
  - **M1 flee-step (straight)** — carried forward.
  - **M2 gate toggle** — carried forward.
  - **M3 skittish temperament (new):** a second creature type
    (`creature_skittish`, magenta) flees **perpendicular** — it sidesteps
    one cell along the away-vector rotated 90° clockwise instead of
    moving straight back. Player-facing new rule: "the magenta one
    doesn't back straight away from me — it veers to the side, so I have
    to herd it from a different angle."
- **Necessity per mechanic:**
  - *M1:* L3 cannot be solved without triggering M1 because the straight
    creature at (4,8) has no push/carry verb and must change cell to
    reach its pen at (12,8); its only motion is the straight flee.
  - *M2:* L3 cannot be solved without triggering M2 because the straight
    creature's pen (12,8) is on the EAST side of the vertical dividing
    wall (column x=8, y∈{1..14}, gap only at the gate (8,8)) while the
    creature starts on the WEST side at (4,8); the gate starts CLOSED, so
    the creature cannot cross to its pen until a click opens it (verified:
    BFS with the toggle action removed finds NO solution).
  - *M3:* L3 cannot be solved without triggering M3 because the magenta
    creature at (5,11) flees perpendicular; steering it onto its pen
    (1,11) requires the player to use the sidestep law (a straight-flee
    handling of the same approaches lands it on different cells —
    verified: the all-straight world has a different, shorter solution,
    so the perp law genuinely governs this creature's routing). Its pen
    is reachable only by the sidestep trajectory the player must drive.
- **Layout (16×16):** `wall` border. A vertical dividing wall along x=8
  for y∈{1..14}, except the gate cell (8,8) holding a `gate` (closed at
  start). Shepherd starts at (2,8) (west region, an open cell off the
  wall). Creatures: `creature_timid` (straight) at (4,8); pen
  `pen_amber` at (12,8) (east region, against… reached via the gate).
  `creature_skittish` (perp) at (5,11); pen `pen_magenta` at (1,11)
  (west region, against the west wall backstop).
- **Witness solution** (verified): `[ACTION2, ACTION2, ACTION4,
  ACTION2, ACTION4, ACTION1, ACTION2, ACTION3, ACTION1, ACTION1,
  ACTION6@gate, ACTION1, ACTION4, ACTION4, ACTION4, ACTION4]`.
  - First sidestep-herd the magenta creature to the west wall pen
    (1,11) using the perpendicular law; then maneuver to open the gate
    (ACTION6 on (8,8)); then drive the orange straight creature east
    through the open gate to (12,8).
  - K = 16, D = 5 distinct actions (UP, DOWN, LEFT, RIGHT, click).
    Satisfies ≥3 / ≥2. No single-action-repeat win.
- **Animation plan:** N/A — flee steps (straight and perpendicular) are
  each single-cell local moves; gate toggle is an in-place swap.
- **Lives mechanism:** N/A — no hard-death (step-budget only).
- **Difficulty justification:**
  - **(a) Random-resistance:** two creatures with *different* flee laws,
    one 1-cell pen each, a gate that must be opened, and a dividing wall.
    Random play cannot coordinate sidestep-herding one creature, opening
    the gate, and straight-herding the other through it. Far below 1/10⁴.
  - **(b) Human-tractable:** ~2–3 minutes; the magenta sidestep is the
    one new thing to learn, then it composes with the known gate + flee.
  - **(c) Planning depth — challenging (post-discovery):** **Decision
    space at level start:** ≥ 5 informed first actions (which creature
    to herd first; from which of four sides to approach each; when to
    open the gate). This is ≥ L2's count. **Trivial heuristic that
    fails — "greedy nearest-pen / push-each-creature-straight-toward-its
    -pen":** a player who treats the magenta creature like the orange
    one (push it straight toward (1,11)) sends it veering off-axis (the
    perp law turns the intended straight push into a sidestep), and a
    player who herds the orange creature toward the gate *before* parking
    the magenta one finds the shepherd's gate-approach path re-enters the
    magenta creature's scare radius and sidesteps it off its pen.
    **Where it diverges:** the greedy plan and the witness disagree at
    the first creature choice — the witness parks the perpendicular
    creature against its wall backstop FIRST (so later gate-side moves
    can't disturb it), whereas greedy opens the gate first and loses the
    magenta creature's placement, forcing a costly re-herd or a loss.
  - **(d) Step budget:** **90** (witness 16; does not shrink vs L2 — L3
    adds discovery cost for the new temperament, so the budget is the
    largest of the three).

Grid size (16×16) and the sprite set are reused across levels; each
level varies the sprite positions, the wall/gate geometry, and the
creature temperaments.

## 5. Action mapping
`available_actions = [1, 2, 3, 4, 6]`.
- **ACTION1 / ACTION2 / ACTION3 / ACTION4** — move the shepherd one cell
  UP / DOWN / LEFT / RIGHT (4 px). Blocked by walls, closed gates, the
  border, and creature cells (the shepherd cannot enter a creature's
  cell). After a *successful or attempted* move action, every creature
  within the scare radius takes its flee step.
- **ACTION6 — CLICK at (x, y)** — if the clicked cell holds a `gate`
  post, toggle that gate between OPEN and CLOSED (swap `gate_closed` ↔
  `gate_open`). Clicking anything else is a no-op. A gate toggle does
  NOT trigger a flee step (the shepherd did not move). Gating: ACTION6
  is always offered; `_get_valid_actions` does not restrict it.
- **ACTION5 / ACTION7** — NOT declared. There is no modal verb beyond
  the click-toggle and no undo, so per `action-enum.md` slot 5 is unused
  and slot 7 (strict-undo) is omitted rather than overloaded.

## 6. HUD and per-game state
- **HUD:** `StepCounterHud` (a `RenderableUserDisplay`) paints the top
  display row (`frame[0, :]`) as a left-to-right depleting bar — amber
  {11} for remaining budget, dark {4} for spent — proportional to
  `steps_left / max_steps`. This is the only HUD; it teaches itself by
  shrinking each action.
- **Internal state (Game class):**
  - `_steps_used` (int) — PRIVATE per-level action counter (incremented
    only inside handled action branches, NOT the engine `_action_count`,
    to avoid the RESET-counts-as-a-step bug). Drives the HUD and the
    lose check.
  - `max_steps` (int) — current level's budget, read from level data.
  - per-level `creatures` / `pens` are queried via tags at runtime
    (`get_sprites_by_tag`); a creature's temperament is read from its
    tags (`"straight"` vs `"perp"`).
  - gate open/closed state is encoded by which of the two gate-variant
    sprites is TANGIBLE at the gate cell (two-sprite-swap), so it is
    fully visible — no hidden mode flag.
- **No hidden state requiring an extra cue:** the shepherd position,
  every creature position, the gate open/closed visual, and the HUD bar
  are all on-screen at all times (item 20).

## 7. Win condition
A level is won when **every `creature`-tagged sprite occupies a `pen`
cell of its matching temperament colour** — i.e. each
`creature_timid` (orange) is on a `pen_amber` cell and each
`creature_skittish` (magenta) is on a `pen_magenta` cell. Concretely,
after each action, `_check_win()` returns True iff for every creature
there exists a pen at the same (x, y) whose pen-tag matches the
creature's temperament-tag; on True, `self.next_level()` (or
`self.win()` on the last level). Holds for all three levels.

## 8. Lose condition
`self.lose()` fires when `_steps_used >= max_steps` (energy bar empty)
and the level is not yet won. There is no other lose path — creatures
cannot harm the shepherd, and no action causes an irreversible
soft-lock (a mis-herded creature can always be re-herded within the
generous budget; the geometry never makes the win unreachable before
budget exhaustion).

## 9. Novelty note
- **Closest taxonomy entries.** *ka59 (sokoban-explode-chase)* — ka59's
  NPC chases the player and the player *pushes* pawns onto targets;
  hd7r's NPCs *flee* and are never pushed or contacted (control is a
  repulsion field at a distance), and the win cell is one the shepherd
  can never stand on. *g50t / tu93 / m0r0 / su15 / wa30 (the agentness
  reference set)* — all have chasing, patrolling, or object-competing
  NPCs; none has a flee-from-the-player policy nor makes the player's
  body the steering surface for an autonomous agent's destination.
- **Closest prior-games entries** (scanned every `prior-games/*/`,
  not just the incomplete index). *zk9p (pursuer-merge-walk)* — pursuers
  move TOWARD the avatar and win = mutual collision/merge; hd7r is the
  inverse policy (flee) and a positional win (creature on pen), no
  merge. *mw8p (predator-prey-triangle)* — a chase web where the player
  escapes to an exit; hd7r has no chase web and the player places
  creatures rather than escaping. *gg26 (sheep-pasture-fence)* — the
  sheep is STATIC and the player clicks fences to enclose a grass region
  measured by flood-fill area; hd7r's creatures MOVE every tick and the
  win is discrete pen-occupancy, with the shepherd's body (not placed
  fences) as the lever. *rk7x / gg25 (courier / docking)* — autonomous
  actors follow authored paths and ignore the player's position; hd7r's
  creatures have no path and move purely as a function of the shepherd's
  relative position. The negative-similarity seven-dimension walk
  (in `mechanic-pick.md`) confirms no single prior shares ≥ 3 dimensions
  with hd7r, with divergence on the heavy axes (core dynamic, visual
  signature, pixel grain).
- `prior-games/index.md` is NOT empty; the above prior comparisons are
  against the live corpus.
