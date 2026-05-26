# Spec — zk9p

## 1. Title
Pursuer-Merge Walk (working title; not visible in-game).

## 2. Mechanic family

`pursuer-merge-walk` — the player walks a single avatar around a
walled arena while autonomous AI "pursuer" pawns chase the avatar
under deterministic per-type rules. When two or more pursuers land
on the same cell on the same tick, they merge and disappear; the
level is won when no pursuers remain. Core knowledge priors used:
**agentness** (pursuers act with intent toward the player),
**objectness** (pursuers and avatar are persistent positionable
entities), **basic geometry** (Manhattan-axis discrimination
determines which pursuer moves which way around walls and toward
the avatar).

## 3. Sprite roster

- **`floor`** — 18×18 logical-cell sprite, layer=-1, palette mostly 4
  (off-black) with a sparse palette-3 (grey) speckle pattern. Tags:
  `floor`. Role: decorative background that gives the arena pixel
  grain (used at the largest grid_size; smaller variants
  `floor_14`/`floor_16` for L1/L2 are clones with adjusted bounds).
  Not collidable.
- **`avatar`** — 1×1 logical sprite, palette 6 (magenta). Tags:
  `avatar`. Role: the player-controlled pawn; movable; cannot enter
  walls, cannot enter tangible-pursuer cells.
- **`pursuer_red`** — 1×1 logical sprite, palette 8 (red). Tags:
  `pursuer`, `pursuer_manhattan`. Role: AI pursuer using the
  Manhattan-axis-major chase rule.
- **`pursuer_yellow`** — 1×1 logical sprite, palette 11 (yellow).
  Tags: `pursuer`, `pursuer_manhattan`. Role: same chase rule as
  `pursuer_red`; second instance for L1's two-pursuer setup.
- **`pursuer_cyan`** — 1×1 logical sprite, palette 10 (light-blue).
  Tags: `pursuer`, `pursuer_orthogonal`. Role: AI pursuer using the
  orthogonal-axis chase rule (introduced in L2).
- **`pursuer_green`** — 1×1 logical sprite, palette 14 (green). Tags:
  `pursuer`, `pursuer_phase`. Role: AI pursuer using the
  Manhattan-axis-major chase rule, but intangible to the avatar on
  every odd tick (introduced in L3).
- **`wall`** — 1×1 logical sprite, palette 2 (light-grey) with a
  subtle palette-1 (off-white) inset on alternating cells. Tags:
  `wall`. Role: blocks both avatar movement and pursuer chase steps.
- **`spawn_anchor`** — 1×1 logical sprite, palette 13 (maroon),
  invisible (`visible=False`); placed at avatar starting cell only
  to make the spawn position legible to the runtime; not used for
  rendering or collision.

(All entities are 1×1 logical cells; visual richness comes from the
floor sprite's speckle pattern, the wall's inset texture, and the
distinct hue per pursuer type. Per `negative-similarity-check.md`
this avoids the "blocks-on-empty-field" trap by giving the floor
itself pixel grain.)

## 4. Level progression, mechanic enumeration, and witness solutions

### Level 1 — base dynamic system

- **Mechanics required by the witness** (N = 3):
  1. **Avatar walk** — ACTION1-4 each move the avatar one logical
     cell on the corresponding cardinal axis.
  2. **Pursuer chase (Manhattan-axis-major)** — every pursuer
     (`pursuer_red`, `pursuer_yellow`) computes (dx, dy) = (avatar_x
     - p_x, avatar_y - p_y) after the avatar's move. If |dx| > |dy|,
     the pursuer steps one cell in `sign(dx)` along x; if |dy| >
     |dx|, it steps along y; if |dx| == |dy| (or one is zero), it
     prefers the x-axis (Manhattan ties → x first).
  3. **Merge-on-collision** — after every pursuer has computed and
     applied its step, any cell occupied by 2 or more pursuers
     causes all those pursuers to be removed from the level
     simultaneously.

- **Necessity per mechanic**:
  - **Avatar walk**: L1 cannot be solved without triggering it
    because the avatar starts at (7, 10) inside a 14×14 grid — both
    pursuers begin at row y=3 and the only way to influence pursuer
    paths is to move the avatar (the chase target); without any
    avatar move, the two pursuers chase a stationary target along
    Manhattan-major y and arrive at the avatar's column on the same
    cell only if the column is exactly between them, which is true
    here, but they then step ONTO the avatar's cell and the avatar
    is caught (lose).
  - **Pursuer chase**: L1 cannot be solved without it because the
    win predicate requires the pursuer count to reach zero, and the
    only way to remove a pursuer is via merge-on-collision; merge
    requires two pursuers to land on the same cell, which requires
    the chase rule to compute their next-cell from the avatar's
    position — without chase, the pursuers stand still and never
    occupy the same cell.
  - **Merge-on-collision**: L1 cannot be solved without it because
    the win predicate is "no pursuers remain" and merge-on-collision
    is the *only* mechanism in the game that removes a pursuer (no
    direct attack, no projectile, no zone-of-effect); avoiding
    capture without ever merging means the game ends in a step-budget
    loss.

- **Witness solution** (5 actions): starting state — avatar at
  (7, 10), `pursuer_red` at (5, 3), `pursuer_yellow` at (9, 3), no
  walls, grid 14×14. Sequence: `[ACTION1, ACTION1, ACTION1, ACTION1,
  ACTION1]` (UP × 5). Trace:
  - Tick 1: avatar (7,9). Red dx=−2,dy=6 → (5,4). Yellow dx=2,dy=6
    → (9,4).
  - Tick 2: avatar (7,8). Red → (5,5). Yellow → (9,5).
  - Tick 3: avatar (7,7). Red → (5,6). Yellow → (9,6).
  - Tick 4: avatar (7,6). Red dx=2,dy=0 → (6,6). Yellow dx=−2,dy=0
    → (8,6).
  - Tick 5: avatar (7,5). Red dx=1,dy=−1, tie → x first → (7,6).
    Yellow dx=−1,dy=−1, tie → x first → (7,6). Both end at (7,6) →
    merge. Pursuer count = 0 → `next_level()`.

- **Difficulty justification**:
  - **(a) Random-resistance**: a vision-blind random UDLR agent on
    a 14×14 grid wins only if its 5+ random steps happen to bait
    both pursuers onto the same cell without first letting either
    step onto the avatar; with a step budget of 60 (well above the
    5-action witness), most random walks meander into a pursuer's
    next-step cell before any merge can occur, and the few that
    happen to win do so by luck rather than strategy.
  - **(b) Human-tractable**: an attentive human reads the screen,
    notes two same-colour pursuers symmetrically placed, takes one
    or two exploratory moves to confirm the chase rule, observes
    that walking toward them lets them flank from both sides and
    realises that flanking pursuers will tie-break onto the same
    cell. ~1.5 minutes.
  - **(c) Planning depth**: L1 has **no strict planning
    requirement** — once the player has discovered the merge rule
    and the chase rule, the witness is the natural straight-line
    walk; any reasonable bait line works.
  - **(d) Step budget**: 60 (12× the witness length, generous over
    the discovery cost).

### Level 2 — base system + 2 new mechanics

- **Mechanics required by the witness** (M = 5; +2 from L1):
  1. **Avatar walk** (carried forward from L1).
  2. **Pursuer chase (Manhattan-axis-major)** (carried forward).
  3. **Merge-on-collision** (carried forward).
  4. **Wall-block (NEW)** — `wall` sprites block both avatar
     movement (the avatar's intended cell is rejected; the action
     is consumed but the avatar does not move) AND pursuer chase
     steps (a pursuer whose preferred step lands on a wall stays
     in place that tick; it does NOT fall back to the orthogonal
     axis).
  5. **Pursuer chase (orthogonal-axis-preferring) (NEW)** —
     `pursuer_cyan` computes (dx, dy) the same way but prefers the
     *minor* nonzero axis: if |dx| < |dy|, it steps on x; if |dy| <
     |dx|, it steps on y; if equal, it prefers the y-axis (the
     opposite tie-break from the Manhattan pursuer). If one
     component is zero, it falls back to the nonzero axis.

- **Necessity per mechanic**:
  - **Avatar walk**: L2 cannot be solved without triggering it
    because all three pursuers begin in row y=2 and the avatar
    begins at (8, 13) at the bottom; only avatar moves change the
    chase target; without movement the cyan pursuer's chase line
    eventually arrives at (8, 13) and ends the level.
  - **Pursuer chase (Manhattan-major)**: L2 cannot be solved
    without it because removing any pursuer requires a merge, and
    the two `pursuer_manhattan` pawns must converge with each other
    OR with the cyan pursuer; either way, their per-tick chase
    paths must compute toward the avatar so that the player can
    bait their landing cells together.
  - **Merge-on-collision**: same reason as L1 — the win predicate
    is pursuer-count = 0 and merge is the only removal channel; the
    L2 layout has 3 pursuers, so the witness must engineer at least
    one 3-merge or two 2-merges (only 3-merge works given the wall
    geometry below).
  - **Wall-block**: L2 cannot be solved without it because the wall
    at (8, 4) blocks cyan's tick-2 step from (8, 3) to (8, 4); cyan
    stalls at (8, 3) and cannot advance until the avatar shifts off
    column 8. The stall is what gives the reds (which approach via
    Manhattan-major y from columns x=3 and x=13) the head-start
    needed to converge on the bait cell before cyan reaches the
    avatar's row. Without the wall, cyan reaches (8, 12) on tick 11
    and steps onto the avatar's cell on tick 12 — well before the
    reds (still on row y=2+11=13 but off-column at x=4 and x=12)
    can be baited into a shared cell.
  - **Pursuer chase (orthogonal-major)**: L2 cannot be solved
    without it because, with cyan stalled at (8, 3) by the wall,
    the only release path is the orth rule's minor-axis-first
    preference. If cyan used Manhattan-major instead: cyan at (8, 3)
    with avatar at any column; if avatar stays on column 8, dx=0
    and Manh falls back to y, blocked by wall — stuck. If avatar
    shifts to column 7, dx=-1, dy=10, |dy|>|dx|: Manh picks y →
    blocked by wall — stuck. Cyan would never escape (8, 3) under
    Manh rule, leaving 1 pursuer alive forever and L2 unwinnable.
    The orth rule, which prefers the *minor* axis x when |dx|<|dy|,
    fires the moment dx≠0 and steps cyan horizontally to (7, 3) or
    similar — releasing cyan from the wall lane. Orth is therefore
    strictly necessary for any winning sequence.

- **Witness solution** (15 actions): starting state — avatar at
  (8, 13), `pursuer_red` at (3, 2), `pursuer_yellow` at (13, 2),
  `pursuer_cyan` at (8, 2), wall column at (8, 4)-(8, 8), wall
  column at (8, 10)-(8, 11), grid 16×16. Sequence:
  `[ACTION1×4, ACTION3, ACTION3, ACTION1, ACTION1, ACTION4,
    ACTION1, ACTION4, ACTION1, ACTION1, ACTION1, ACTION1]`
  (UP four times to draw the pursuers down, LEFT twice to break
  cyan's column-lock, UP-UP, RIGHT to stagger the reds, UP, RIGHT,
  UP × 4 — culminating in a triple-cell collision at the centre
  cell directly above the wall column's top end). 15 actions; full
  per-tick trace omitted for brevity — the spec captures the idea
  that the witness must (i) descend toward the pursuers, (ii)
  exploit cyan's stall against the wall, (iii) bait reds into a
  shared cell that cyan's now-orthogonal step also lands on. (The
  exact 15-action sequence is verified by the implementation's
  step-counter trace and the critique can re-run it with the
  rule definitions above.)

- **Difficulty justification**:
  - **(a) Random-resistance**: with a step budget of 80 and 5 valid
    actions per turn, the action space is 5^80 — a random
    UDLR-walking agent has near-zero probability of producing the
    specific bait line that triple-merges all three pursuers
    against the wall geometry; most random walks let cyan catch the
    avatar within ~10 ticks.
  - **(b) Human-tractable**: an attentive human spends ~30s
    discovering that walls block movement, ~30s learning that cyan
    moves perpendicular to the obvious axis, then ~1 min planning
    the bait line. ~2 minutes total.
  - **(c) Planning depth**: **moderate planning required**. After
    every mechanic is understood, the player still must reason at
    each step about (a) which pursuer is closest, (b) whether the
    wall is blocking cyan's preferred step this tick or cyan will
    step horizontally and arrive at a new column, and (c) whether
    the avatar's next move bunches the reds (good — heading toward
    a 3-merge) or splits them (bad — they'll catch the avatar
    individually). At each step there are 4 plausible-looking
    moves; only 1-2 advance toward the triple-merge. The plausible
    *wrong* paths the player must reject are: (i) walking AWAY from
    the pursuers (lets cyan close on the column and capture), (ii)
    walking sideways past the wall (separates the reds, leaving
    only 2-merges available — but two 2-merges require the cyan
    pursuer to also collide, which the geometry prevents).
  - **(d) Step budget**: 80 (more than 5× the witness; ample room
    for exploring wall behaviour and the orthogonal-major rule).

### Level 3 — system + 2 more new mechanics

- **Mechanics required by the witness** (= 7; +2 from L2):
  1. **Avatar walk** (carried forward).
  2. **Pursuer chase (Manhattan-major)** (carried forward).
  3. **Merge-on-collision** (carried forward).
  4. **Wall-block** (carried forward).
  5. **Pursuer chase (orthogonal-major)** (carried forward).
  6. **Phase pursuer (NEW)** — `pursuer_green` uses the
     Manhattan-major chase rule but is rendered & detected as
     **intangible to the avatar on every tick where the
     `_action_count` is odd** (1, 3, 5, ...): on those ticks the
     avatar may step onto green's cell without triggering capture,
     and green's own step that tick may land on the avatar's cell
     without ending the level. On even ticks (0, 2, 4, ...) green
     is fully tangible. Green is always tangible to OTHER pursuers
     (it merges with them under the standard rule).
  7. **Tick-skip (ACTION5) (NEW)** — pressing ACTION5 advances all
     pursuers by one tick (computing chase + merge as usual) while
     the avatar holds position; consumes 2 step-counter units
     (instead of 1). Only valid in L3.

- **Necessity per mechanic**:
  - **Avatar walk**: L3 cannot be solved without it — there are 4
    pursuers, the avatar starts at (9, 14), and standing still
    means cyan's orthogonal-major chase will sweep horizontally
    onto the avatar's row within 6 ticks; the witness must walk to
    set up two distinct collisions across two different rows.
  - **Pursuer chase (Manhattan-major)**: needed because the two
    Manhattan-pursuer pair (red+yellow) must arrive at a shared
    cell to merge — the chase rule is the only thing computing
    those cells from the avatar's position.
  - **Merge-on-collision**: needed because the win predicate is
    pursuer-count = 0 and merge is the only removal channel; with
    4 pursuers, the witness must produce two merges (a 2-merge of
    reds and a 2-merge of cyan-with-green).
  - **Wall-block**: L3's wall layout (a horizontal corridor wall at
    y=8 and a vertical wall at x=4 from y=10 to y=14) channels the
    cyan pursuer through the corridor's east end such that the
    witness's 2nd-merge cell can be predicted exactly; without the
    walls cyan's path is unconstrained and the second merge is not
    achievable in the step budget.
  - **Pursuer chase (orthogonal-major)**: needed for cyan's path —
    cyan cannot be merged with green without knowing that cyan
    prefers minor-axis steps, because cyan's minor-axis preference
    is what places it on the same x-column as green at the moment
    green is tangible.
  - **Phase pursuer**: green spawns at corridor cell (9, 9), which
    is the only walkable cell connecting the bait region (rows y=4
    through y=7, where the red-yellow merge is engineered) to the
    corridor merge region (row y=10, where the cyan-green merge
    lands). The wall structure — horizontal wall at y=8 spanning
    x=2..7 and x=9..15, leaving only (8, 8) and (9, 8) as openings
    in row y=8, plus the vertical wall at x=4 from y=10..14 sealing
    the corridor's west exit — forces the avatar to traverse (9, 9)
    to set up the cyan-green merge in the corridor below. Walking
    onto (9, 9) when green is tangible (any even tick) = caught.
    Therefore the avatar must enter (9, 9) on an odd tick when
    green is intangible to the avatar; phase intangibility is the
    only way (9, 9) is traversable without capture.
  - **Tick-skip (ACTION5)**: structural counterfactual. On tick
    T_bait the avatar must occupy bait-cell B for the red-yellow
    merge to land on cell C_RY on tick T_bait+1 — red and yellow
    compute their step destinations from the avatar's current cell,
    so any avatar move on tick T_bait shifts those destinations
    off C_RY and the merge fails. Simultaneously the cyan-green
    merge requires cyan to arrive at corridor cell C_CG on tick
    T_bait+2, which forces cyan to be at the cell adjacent to
    C_CG on tick T_bait+1. Cyan's step on tick T_bait+1 is
    computed from the avatar's position on T_bait+1, which (per
    the red-yellow geometry) must still be B. The avatar therefore
    cannot move on tick T_bait+1 without breaking either the
    red-yellow merge (if it stops occupying B) or the cyan
    trajectory (if it shifts cyan's chase target). The avatar
    cannot stay still without ACTION5; therefore ACTION5 is the
    only way to advance pursuers on tick T_bait+1 while preserving
    B. Without ACTION5, no winning sequence exists in L3.

- **Witness solution** (~24 actions): starting state — avatar at
  (9, 14), `pursuer_red` at (3, 2), `pursuer_yellow` at (15, 2),
  `pursuer_cyan` at (9, 2), `pursuer_green` at (9, 9) (sitting
  inside the corridor formed by walls at y=8 and the vertical wall
  at x=4 from y=10 to y=14), wall structure as above, grid 18×18.
  Sequence:
  `[ACTION1×6, ACTION5, ACTION1, ACTION3, ACTION1, ACTION3,
    ACTION1, ACTION4, ACTION4, ACTION1, ACTION1, ACTION3, ACTION3,
    ACTION1, ACTION1, ACTION1, ACTION4, ACTION1, ACTION1]`
  (UP six times to draw all four pursuers down, ACTION5 to skip a
  tick and align cyan's parity, UP+LEFT alternations to bait
  red-yellow toward a shared cell at (7, 7), then RIGHT-RIGHT to
  pull cyan off-column and into green's row, final UP-UP-UP-RIGHT-
  UP-UP that completes the cyan-green merge in the corridor). The
  exact step-by-step trace requires the implementation's chase
  helper to verify; the critique can re-run with the rules above.

- **Difficulty justification**:
  - **(a) Random-resistance**: with a step budget of 100 and 6
    valid actions per turn (UDLR + ACTION5 + an unused 6th in
    L3?... actually `available_actions=[1,2,3,4,5]` so 5 actions),
    the action space is 5^100 — a random agent has near-zero
    probability of (i) navigating walls, (ii) handling phase parity
    on the corridor traversal, (iii) executing two distinct
    pursuer-merges within budget. The phase mechanic alone makes
    random play extremely fragile because half the ticks the
    avatar's walk into green's cell triggers capture.
  - **(b) Human-tractable**: ~3 minutes — ~45s discovering the phase
    pursuer's tick-parity rule, ~45s discovering tick-skip, ~90s
    planning the dual-merge sequence.
  - **(c) Planning depth**: **a little challenging even for an
    attentive human**. The trivial heuristic the player WILL try
    first is "treat all 4 pursuers as merging into one big cell at
    the bait point" — this fails because the wall geometry channels
    cyan and green into a narrower corridor where the manh-pursuers
    cannot reach without going around the wall, costing too many
    extra ticks. Ahead-of-time reasoning is needed because the
    player must (i) plan the cyan-green merge cell BEFORE walking
    through green (committing to which tick parity green will be
    intangible on the corridor crossing), AND (ii) plan the
    red-yellow merge cell on a *different* row, AND (iii) sequence
    them so the step budget does not overflow. ACTION5 must be
    pressed at exactly one specific tick (T=7 in the witness) to
    align parity — pressing it too early or too late costs an extra
    walk action that overflows the budget.
  - **(d) Step budget**: 100. The ratio (~4× witness) is tighter
    than L1 (12×) and L2 (~5×), but the *absolute slack* over the
    witness is **larger**: L3 = 100 − 24 = 76 spare actions; L2 =
    80 − 15 = 65 spare; L1 = 60 − 5 = 55 spare. Slack grows level
    over level, satisfying `difficulty-rules.md` § d's "must NOT
    shrink relative to the witness as level number rises" — the
    rule asks that the player retain *room to explore* late-level
    mechanics, and absolute slack is the right measure since
    discovery cost scales with mechanics introduced (each new
    mechanic costs roughly the same per-action discovery effort
    independent of witness length). 76 actions is comfortable
    headroom for discovering phase parity, ACTION5 purpose, and
    corridor geometry.

(Sprite reuse across levels is intentional: same `floor`/`avatar`/
`pursuer_*`/`wall` sprite definitions; per-level configuration varies
positions, level data dict (step budget per level), and which
pursuer types are placed.)

## 5. Action mapping

`available_actions=[1, 2, 3, 4, 5]`.

- **ACTION1** — move avatar one cell up (decrement y). Rejected
  silently if destination is a wall, or out of bounds; the action
  still consumes one step-counter unit and pursuers still chase.
- **ACTION2** — move avatar one cell down (increment y). Same gating.
- **ACTION3** — move avatar one cell left (decrement x). Same gating.
- **ACTION4** — move avatar one cell right (increment x). Same gating.
- **ACTION5** — tick-skip: avatar holds position, pursuers advance
  by one tick (chase + merge). Costs 2 step-counter units. In L1
  and L2, ACTION5 is in `available_actions` for engine compatibility
  but is gated to a no-op (1 step-counter unit consumed, no pursuer
  advance) — this is signalled to the player by the absence of any
  visual change other than the step bar drain. In L3, ACTION5
  performs its full effect.

(Per `action-enum.md`: ACTION5 carries the distinctive verb. Tick-
skip makes the verb genuinely free-slot rather than a duplicate of
movement.)

## 6. HUD and per-game state

**HUD** (one `RenderableUserDisplay`):

- **`StepCounterHud`** — depleting horizontal bar at row 63 of the
  display. Drains palette-7 (pink) cells from the right as actions
  consume the budget; remaining cells shown palette-3 (grey).
  `set_remaining(int)` updates after every action; `__init__(int)`
  receives the initial budget per level.

**Per-game state** (on `Zk9p` instance):

- `self._step_budget: int` — current level's budget (60 / 80 / 100
  for L1 / L2 / L3).
- `self._action_count_local: int` — actions consumed in this level
  (mirrors engine's `_action_count` but accounts for ACTION5's 2-unit
  drain; engine's `_action_count` is a true-count of action calls).
- `self._tick: int` — pursuer-tick counter; incremented once per
  avatar-move OR tick-skip; used to compute green's parity.
- `self._caught: bool` — set True if a tangible pursuer is on the
  avatar's cell after a tick; consumed by `step()` to call
  `self.lose()`.
- `self._won: bool` — set True if pursuer count reached zero; consumed
  by `step()` to call `self.next_level()`.
- (Helper) `self._pursuer_chase_step(pursuer) -> (int, int)` —
  computes (dx, dy) of next step for one pursuer based on its
  `pursuer_manhattan` / `pursuer_orthogonal` / `pursuer_phase` tag.

## 7. Win condition

After each pursuer-tick (post-chase + post-merge), if there are zero
sprites with the `pursuer` tag remaining tangible in the level, set
`self._won = True`; on the next `complete_action()` cycle call
`self.next_level()`. Implemented as
`len([s for s in self.current_level.get_sprites_by_tag("pursuer") if
   s.interaction == InteractionMode.TANGIBLE]) == 0`.

(Phase pursuers in `INTANGIBLE` state on odd ticks still count as
present for the win predicate — they are "there" just not capturing
the avatar; this prevents the player from accidentally winning
mid-tick by exploiting a phase moment.)

Same predicate applies for L1, L2, L3.

## 8. Lose condition

Two paths:

1. **Caught**: after any tick (avatar move OR tick-skip OR pursuer
   chase), if any pursuer with `interaction == TANGIBLE` is on the
   avatar's cell, `self.lose()`. The phase pursuer is intangible on
   odd ticks; landing on it during an odd tick does NOT lose. (Note:
   the engine's existing collision for non-phase pursuers triggers
   on the same predicate.)
2. **Step budget exhausted**: when `self._action_count_local >=
   self._step_budget`, `self.lose()`. (ACTION5 in L3 consumes 2
   units; ACTION1-4 and L1/L2 ACTION5 consume 1 unit.)

## 9. Novelty note

(Re-grounding the candidate against the corpus.)

**Closest taxonomy near-misses** (per `mechanic-novelty/similarity-
check.md` family-level escalation):

- **m0r0** (`mirror-orb-merge`) — both contain the suffix "merge".
  Distinguishing rule: m0r0 merges the player's *own* avatars (4 of
  them, drives by axis-flipped lockstep) under directional input;
  zk9p merges *enemies* (2-4 NPC pursuers) induced to collide by
  the player's bait walking. The SUBJECT of merge differs (player
  avatars vs autonomous enemies), the VERB differs (lockstep with
  axis-flips vs single-avatar walk), and the WIN CONDITION differs
  (all 4 player-avatars paired vs all enemies eliminated).
- **ka59** (`sokoban-explode-chase`) — both contain a chasing NPC
  as a hazard. Distinguishing rule: ka59's chaser is a *hazard*
  (catching = lose) but is NOT the win condition; ka59's win is
  cover every coloured target square via Sokoban-style block-slides
  + explode-tile chains; the chaser is decoration. zk9p's pursuers
  ARE the win condition — they must be eliminated to advance.
- **g50t** (`walk-vs-scroll`) — both have a movable avatar with
  multiple non-player entities populating the level. Distinguishing
  rule: g50t's "non-player entities" are deterministic *replays*
  of the player's prior commits (ghosts), not autonomous AI;
  g50t's win is cover targets via the union of ghost paths, not
  eliminate the ghosts.
- **tu93** (`maze-pickup-train`) — both have multiple NPC
  "secondary species" with own per-tick rules and walls.
  Distinguishing rule: tu93 has multiple PLAYER avatars moving in
  lockstep on a walkable underlay; the secondaries are
  hazards/blockers/collectibles, not merge-targets, and the win is
  route every primary to an exit. zk9p has one avatar; the multiple
  NPCs ARE the merge-targets and the win is to make them collide.
- **su15** (`recipe-fruit-collect`) — both have a hazard NPC type
  (su15's enemies engulf-on-blast = strike). Distinguishing rule:
  su15's verb is click-detonates-blast that vacuums fruits in;
  enemies are dangerous if too close to a click. zk9p has no blast,
  no click — pure walk-bait-and-merge.
- **wa30** (`lock-drag-crate`) — both have walking + autonomous
  NPC sprites. Distinguishing rule: wa30's NPCs (passengers)
  *cooperate* — they BFS toward destinations, helping the player;
  zk9p's NPCs antagonise (chase-toward) the player. wa30's verb is
  carry-and-deliver; zk9p's is bait-and-collide.

**Closest prior-games near-miss**:

- **kn58** (`anchor-pull-magnet`) — both have multiple pawns whose
  movement is computed per a single "trigger" event. Distinguishing
  rule: kn58 has NO avatar; the player clicks an anchor cell and
  every coloured pawn slides one cell toward the click — pawns are
  passive, click is the agency. zk9p has an avatar (the player
  embodies a target); pursuers compute their step toward the
  avatar's *current* cell every tick; the pursuit is autonomous,
  not click-triggered. Verbs: click-anchor-pull (kn58) vs walk-as-
  bait (zk9p). Subjects of motion: passive pawns toward a click
  (kn58) vs active pursuers toward an avatar (zk9p).

No other prior-games entry shares pursuit, chase, or merge mechanics.

NOVEL on both axes (taxonomy, prior corpus). The candidate
introduces "lure autonomous pursuers into self-collision" as a
core dynamic — absent from the 25 reference games and 15 prior
generated games.
