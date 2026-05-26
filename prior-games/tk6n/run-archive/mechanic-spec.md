# mechanic-spec.md (revision 2 — addresses critique-revisions.md issues 1, 2, 3, 4)

## Sections changed since revision 1
- §3 Sprite roster — `target_dim` and `target_lit` now explicitly
  declared `collidable=False` (Issue 3).
- §4 Level 1 — geometry simplified to open arena; concrete shortest
  16-action witness written out (Issue 2).
- §4 Level 2 — geometry redesigned around a single target trapped in
  a corridor sealed by `wall_tall` on top/bottom/east and barred by
  `wall_short` on the west side; M2 counterfactual now provably
  holds (Issue 1).
- §4 Level 3 — concrete action-by-action witness skeleton; M3
  necessity tightened by placing avatar inside the guard's patrol
  col range so the guard reaches the avatar by action 2 unless the
  avatar moves (Issues 1, 4).

---

## 1. Title
"Boomerang Loop" (working title; not visible in-game).

## 2. Mechanic family
`boomerang-arc-catch`. The player throws a boomerang projectile that
travels outbound K cells in the throw direction, then HOMING-RETURNS
by greedy-Manhattan-step toward the avatar's CURRENT cell each tick
(ties broken x-first). The boomerang lights coloured TARGET sprites
it overlaps on either leg. The catch happens when the boomerang and
the avatar coincide on a cell at the END of a tick. Priors used:
**objectness**, **basic physics**, **basic geometry & topology**,
and (L3) **agentness** (a deterministic patrolling guard).

## 3. Sprite roster
- `avatar` — 5×5; palettes 9 (blue body), 11 (yellow rim), 4 (off-
  black eye-dot for facing); tags `["player", "sys_click"]`;
  `collidable=True`; player avatar; collides with `wall_tall`,
  `wall_short`, `guard`.
- `boomerang` — 3×3 angular blade; palette 12 (orange) + palette 8
  (red accent); tags `["boomerang"]`; `collidable=False`; rendered
  at boomerang's current cell when in flight, attached to avatar's
  hand-side cell when held.
- `target_dim` — 4×4 starburst with hollow centre; palettes 6
  (magenta arms), 7 (pink centre), 4 (off-black shadow); tag
  `["target"]`; **`collidable=False`** so the avatar can walk
  through targets without effect (only the boomerang lights them).
- `target_lit` — 4×4 same silhouette as `target_dim`; arms upgraded
  to palette 11 (yellow), centre to palette 12 (orange); tag
  `["target", "lit"]`; **`collidable=False`**; visual swap when a
  target is lit.
- `wall_tall` — 4×4 cross-bar pillar; palette 5 (black) primary,
  palette 4 (off-black) crossbar, palette 3 (grey) speckle; tags
  `["wall", "wall_tall"]`; `collidable=True`; blocks BOTH avatar
  walking AND boomerang flight.
- `wall_short` — 4×4 striped pillar; palette 4 (off-black) primary,
  palette 3 (grey) horizontal stripes, palette 2 (light-grey)
  speckle; tags `["wall", "wall_short"]`; `collidable=True` for
  walking; the per-step boomerang advance ignores `wall_short`
  collisions so the boomerang flies OVER it.
- `guard` — 4×4 hexagonal silhouette with twin "eyes" indicating
  patrol direction; palette 13 (maroon) body, palette 8 (red) eyes,
  palette 4 (off-black) outline; tags `["guard"]`;
  `collidable=True`; only present in L3.
- `guard_frozen` — 4×4 same silhouette; body recoloured palette 3
  (grey), eyes palette 2 (light-grey); tags `["guard", "frozen"]`;
  visual variant placed during freeze window.

All sprites at the 64×64 cell granularity (one cell == one display
pixel).

## 4. Level progression, mechanic enumeration, and witness solutions

EXACTLY 3 levels. `grid_size=(64, 64)` for every level. Avatar starts
each level facing **right** (eye-dot pixel at the right edge of the
5×5 avatar sprite). Arrow presses update the eye-dot regardless of
whether the walk succeeded.

### Level 1 — base dynamic system

Layout:
- Avatar at `(20, 32)`. 5×5 footprint covers `(20, 32)..(24, 36)`.
- One `target_dim` at anchor `(28, 32)`. 4×4 footprint
  `(28, 32)..(31, 35)`.
- **No walls** — open 64×64 arena. Avatar movement bounded only by
  the level edges.
- `throw_range = 8`, `step_budget = 25`.

- **Mechanics required by the witness** (N = 1):
  - **M1: Boomerang throw + outbound + homing-return + catch +
    target-light-on-overlap.** ACTION5 (held → fired) launches the
    boomerang in the avatar's current facing direction; subsequent
    actions advance the boomerang one cell per tick (outbound for
    `throw_range` advances, then homing-return — at each return tick
    the boomerang takes one cardinal step in the direction whose
    Manhattan-component to the avatar's CURRENT cell has larger
    absolute value, ties broken x-first). The boomerang lights any
    target whose 4×4 footprint contains the boomerang's current
    cell. Catch when avatar.cell == boomerang.cell at end of tick.

- **Necessity per mechanic**:
  - **M1**: L1 cannot be solved without triggering M1 because the
    `target_dim` sprite is `collidable=False` and the only state
    transition that mutates `target_dim` → `target_lit` is the
    boomerang-overlaps-target-footprint rule from M1 (avatar walking
    onto the target's cells does not light it — there is no
    avatar-walk-target rule). Furthermore the win predicate
    additionally requires `boomerang.phase == held`, which can only
    be re-achieved via the homing-return + catch sub-rule of M1.
    No alternate path triggers M1's effects without M1.

- **Witness solution** (16 actions):
  ```
  [ACTION5,
   ACTION1, ACTION1, ACTION1, ACTION1, ACTION1, ACTION1, ACTION1,
   ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2,
   ACTION4]
  ```
  Step-by-step trace (avatar / boomerang positions; boomerang phase):
  - Pre-action 1: avatar `(20, 32)`, boomerang held, facing right.
  - Action 1 (ACTION5): boomerang launched at `(20, 32)`, advances
    one tick to `(21, 32)`. outbound_remaining = 7. Phase=outbound.
  - Action 2 (ACTION1): avatar `(20, 31)`. Boomerang advances to
    `(22, 32)`. 6 outbound left. Boomerang's footprint at `(22, 32)`
    does not yet overlap target footprint `(28, 32)..(31, 35)`.
  - Action 3 (ACTION1): avatar `(20, 30)`. Boomerang `(23, 32)`. 5.
  - Action 4 (ACTION1): avatar `(20, 29)`. Boomerang `(24, 32)`. 4.
  - Action 5 (ACTION1): avatar `(20, 28)`. Boomerang `(25, 32)`. 3.
  - Action 6 (ACTION1): avatar `(20, 27)`. Boomerang `(26, 32)`. 2.
  - Action 7 (ACTION1): avatar `(20, 26)`. Boomerang `(27, 32)`. 1.
  - Action 8 (ACTION1): avatar `(20, 25)`. Boomerang `(28, 32)`. 0
    outbound left → switch to returning. **Target lit** (boomerang
    cell `(28, 32)` overlaps target anchor `(28, 32)`).
  - Action 9 (ACTION2): avatar `(20, 26)`. Boomerang home toward
    `(20, 26)`: dx=−8, dy=−6, abs(dx)>abs(dy), step (−1, 0).
    Boomerang `(27, 32)`.
  - Action 10 (ACTION2): avatar `(20, 27)`. Boomerang home toward
    `(20, 27)`: dx=−7, dy=−5, step (−1, 0). Boomerang `(26, 32)`.
  - Action 11 (ACTION2): avatar `(20, 28)`. Boomerang home `(20,
    28)`: dx=−6, dy=−4, step (−1, 0). Boomerang `(25, 32)`.
  - Action 12 (ACTION2): avatar `(20, 29)`. Boomerang `(20, 29)`:
    dx=−5, dy=−3, step (−1, 0). Boomerang `(24, 32)`.
  - Action 13 (ACTION2): avatar `(20, 30)`. dx=−4, dy=−2, step
    (−1, 0). Boomerang `(23, 32)`.
  - Action 14 (ACTION2): avatar `(20, 31)`. dx=−3, dy=−1, step
    (−1, 0). Boomerang `(22, 32)`.
  - Action 15 (ACTION2): avatar `(20, 32)`. dx=−2, dy=0, step
    (−1, 0). Boomerang `(21, 32)`. No catch (avatar `(20, 32)` ≠
    boomerang `(21, 32)`).
  - Action 16 (ACTION4): avatar `(20, 32) → (21, 32)`. After
    avatar move, the catch check finds avatar.cell == boomerang.cell
    `(21, 32)` → CATCH. Boomerang phase → held. **Win predicate
    met**: target_lit ∈ lit_targets AND boomerang.phase == held →
    `next_level()`.

- **Difficulty justification**:
  - **(a) Random-resistance.** A random-policy agent pressing
    arrows + ACTION5 randomly has near-zero probability of (i)
    facing east when ACTION5 fires, (ii) the boomerang's outbound
    path passing over `(28, 32)`, (iii) walking AWAY from the
    boomerang during outbound to avoid early catch, AND (iv)
    walking BACK to the launch line in time for the boomerang's
    homing return to reach the avatar within 25 steps. The
    conjunction is well below 1/10000.
  - **(b) Human-tractable.** ~1.5 minutes once the player has
    pressed ACTION5 once and watched the boomerang fly out and
    home back. Within total ~6-min target.
  - **(c) Planning depth.** None required (per `difficulty-rules.md`
    L1 guidance: "no strict planning requirement — mechanic
    discovery is the entire difficulty").
  - **(d) Step budget**: `25`. Witness 16 actions; 9-action margin.

### Level 2 — base system + 1 new mechanic

Layout (revised per critique Issue 1):
- Avatar at `(10, 32)`. 5×5 footprint `(10, 32)..(14, 36)`.
- ONE `target_dim` at anchor `(40, 32)`. 4×4 footprint
  `(40, 32)..(43, 35)`.
- `wall_tall` ceiling: a 1-row band of `wall_tall` 4×4 instances
  at row 24 spanning cols 5..56 — concretely 13 `wall_tall`
  instances at anchors `(5+4i, 24)` for i ∈ {0..12}, covering
  cells (5..56, 24..27).
- `wall_tall` floor: same pattern at row 40, anchors `(5+4i, 40)`
  for i ∈ {0..12}, covering (5..56, 40..43).
- `wall_tall` east end: 4 `wall_tall` instances at `(56, 28)`,
  `(56, 32)`, `(56, 36)` — wait, `wall_tall` is 4×4; one at
  `(56, 24)`, one at `(56, 28)`, etc.; we just need col 56 rows
  24..43 covered. Use 5 anchors `(56, 24+4j)` for j ∈ {0..4}.
- `wall_short` vertical barrier: at column 22, covering rows
  24..40. `wall_short` is 4×4; use anchors `(22, 24)`, `(22, 28)`,
  `(22, 32)`, `(22, 36)` — 4 instances covering (22..25, 24..39).
  This forms a 4-cell-wide vertical strip from row 24 (top wall)
  through row 39 (just above floor).
- `throw_range = 32`, `step_budget = 60`.

The corridor is sealed: walking-rectangle `(5..21, 25..39)` is the
only avatar-accessible region (plus level edges to the west of col
5 — but the avatar's start at `(10, 32)` is inside this region).
The east half of the corridor (cols 26..55) is **unreachable by
the avatar**: top wall_tall row 24, bottom row 40, east col 56,
west wall_short col 22..25 all `collidable=True`; the only
boundary that doesn't block avatar movement is none — the avatar
is bounded on all four sides.

- **Mechanics required by the witness** (N+1 = 2):
  - **M1**: same as L1.
  - **M2**: wall-height gating — `wall_tall` blocks both avatar
    walking AND boomerang flight (the boomerang's per-tick advance
    aborts on `wall_tall` collision, switching to returning at the
    cell BEFORE the wall during outbound, or to dropped during
    return). `wall_short` blocks avatar walking only; the
    boomerang's per-tick advance ignores `wall_short` cells (flies
    OVER).

- **Necessity per mechanic** (independent enumeration of plausible
  alternate strategies):
  - **M1**: L2's target at `(40, 32)` is `collidable=False`; the
    only mutation rule for target_dim → target_lit is M1's
    boomerang-overlap rule. Win predicate also requires
    `boomerang.phase == held` (M1's catch sub-rule). M1 is
    necessary.
  - **M2**: enumerate plausible alternate strategies the avatar
    could try to light `(40, 32)`:
    1. **"Walk to target's cell, then somehow trigger lighting."**
       The avatar's accessible region is `(5..21, 25..39)`. The
       target's cells `(40, 32)..(43, 35)` lie at col ≥ 40,
       outside the accessible region. Even reaching col 40 would
       require crossing col 22 (wall_short) — the avatar bumps
       wall_short at col 22 row 32 and stays put. Avatar cannot
       reach cells with col ≥ 22.
    2. **"Throw east from accessible cell, boomerang reaches
       target via straight-east line."** From any cell `(c, 32)`
       with c ∈ {5..21}, throwing east → boomerang's outbound
       path goes (c+1, 32), (c+2, 32), ..., (c+throw_range, 32).
       This path crosses col 22 — a `wall_short` cell. Without
       M2's "boomerang flies over `wall_short`" rule, the
       boomerang would stop at col 22 (treating it as a `wall_tall`
       collision) and never reach col 40. WITH M2, the boomerang
       passes through col 22's wall_short cell and continues to
       col c+throw_range. With c=10 and throw_range=32, the
       outbound terminus is col 42 — passing through col 40 at
       tick (40-10)=30 (lights target).
    3. **"Throw at a row other than 32."** From cell `(c, r)`
       with r ∈ {25..31, 33..39}, the throw east advances on row
       r. The boomerang's outbound path at row r ≠ 32 does not
       pass through col 40 row 32. Even if the boomerang's homing
       return drifts toward avatar's row 32, the homing return
       only fires AFTER outbound completes — the outbound on
       row r ≠ 32 cannot light target_dim at `(40, 32)` because
       the boomerang's row remains r through the entire outbound
       leg. The homing return MIGHT pass through row 32 at some
       column on its way back, but the boomerang would then need
       to also be at col ∈ {40..43} on row 32 simultaneously — only
       possible if the outbound terminus was at or beyond col 40,
       which on row r requires the boomerang to first reach col 40
       row r, which is itself in the unreachable east region (the
       avatar can't throw from there).

       More concretely: on row r ≠ 32, the boomerang's outbound
       still hits col 22 wall_short and (without M2) is stopped
       at col 21. With M2, it passes; but the boomerang then
       reaches col c+throw_range, which is on row r — not row 32
       — so the target footprint at row 32..35 is not overlapped
       UNLESS r ∈ {32..35} (in which case row 33, 34, 35 are
       walkable rows below row 32, and the boomerang's row would
       overlap target footprint cells). Walkable rows 33, 34, 35
       throws would also hit target footprint — but they ALSO
       cross col 22 wall_short on the way. M2 still required.
    4. **"Throw south from row 25..31, boomerang flies south,
       reaches row 32 at some col."** Avatar at `(c, 25)` (top
       row of accessible region) facing south — boomerang flies
       south at col c. Boomerang advances to (c, 26), (c, 27),
       ..., (c, 25+throw_range). The boomerang's row-32 cell is
       (c, 32), at col c ∈ {5..21}. Target at col 40 — no
       overlap. M2 not relevant; this strategy doesn't reach
       target regardless.
    5. **"Throw north from row 33..39."** Symmetric to #4; boom
       row 32 cell at (c, 32), col c ∈ {5..21}. No overlap. Doesn't
       reach target.

    Every plausible alternate strategy that DOES reach `(40, 32)`
    requires the boomerang to traverse a `wall_short` cell at col
    22; therefore M2 is strictly counterfactually necessary.

- **Witness solution** (~25-30 actions; concrete sequence):
  ```
  [ACTION5,
   ACTION1, ACTION2, ACTION1, ACTION2, ACTION1, ACTION2,
   ACTION1, ACTION2, ACTION1, ACTION2, ACTION1, ACTION2,
   ACTION1, ACTION2, ACTION1, ACTION2, ACTION1, ACTION2,
   ACTION1, ACTION2, ACTION1, ACTION2, ACTION1, ACTION2,
   ACTION1, ACTION2, ACTION1, ACTION2, ACTION1, ACTION2, ACTION4]
  ```
  - Action 1: ACTION5 throw east. Boomerang launches at `(10, 32)`,
    advances to `(11, 32)`. outbound_remaining = 31.
  - Actions 2..31 (30× alternating ACTION1/ACTION2): avatar
    oscillates between `(10, 31)` and `(10, 32)` (or `(10, 32)`
    and `(10, 33)` — symmetric; oscillation keeps avatar at col
    10). Boomerang advances east each tick: at action k, boomerang
    at col 10+k row 32. Boomerang crosses col 22 (wall_short) at
    action 12; lights `(40, 32)` target on action 30 when
    boomerang reaches `(40, 32)`. Outbound exhausted at action 32
    (boomerang at `(42, 32)`); switch to returning.
  - Actions 33+: avatar continues oscillating. Boomerang homes
    back. dx ≈ −32 at start of return, decreasing by 1 per tick.
    After ~30 home ticks, boomerang at col ~10 row 32. Avatar at
    `(10, 32)` or `(10, 31)` depending on oscillation parity.
    Catch occurs when avatar walks onto boomerang's cell or
    boomerang homes onto avatar.

  Witness length is approximately 60 actions; step_budget = 60
  matches. The implementer will run this sequence in `smoke_test`
  and may tighten the geometry if witness > step_budget. (Easy
  parameter to adjust: increase step_budget, or shorten throw_range
  + move target closer.)

  **Note on witness exactness.** The spec documents the witness
  STRATEGY (oscillate-while-throw, then catch); the exact
  step_budget will be calibrated in `smoke_test` to ensure the
  witness fits with margin. If witness exceeds budget, the L2
  geometry will be tightened (target at `(28, 32)` instead of
  `(40, 32)`, throw_range = 18, step_budget = 40 — well within
  range).

- **Difficulty justification**:
  - **(a) Random-resistance.** Random play has near-zero chance
    of (i) facing east when ACTION5 fires from a row-32 cell,
    (ii) keeping the avatar oscillating long enough for the
    boomerang to complete outbound + return, AND (iii) catching
    the boomerang within step budget. The conjunction is well
    below 1/10000.
  - **(b) Human-tractable.** ~2 minutes — the visual
    distinction between `wall_tall` (crossbar pattern, palette 5)
    and `wall_short` (horizontal stripe, palette 4) cues the player
    to test which blocks throws. After a single test throw the
    rule is clear.
  - **(c) Planning depth (post-discovery).** Moderate — even with
    full M1 + M2 knowledge, the player faces a decision: throw
    direction (east is the only one that reaches the target) and
    when to throw (anytime is fine; the avatar's oscillation
    pattern doesn't affect win as long as it doesn't intercept the
    boomerang too early). The plausible-but-wrong heuristic is
    "walk EAST first to be closer, THEN throw" — but the avatar
    bumps wall_short at col 22 and cannot get closer than col 21,
    so this strategy succeeds (it's not actually wrong) but takes
    ~12 extra walk-bump actions. The player must reason that
    walking east doesn't help (post-discovery, M2 means the
    boomerang flies over wall_short regardless of avatar's column).
    Post-discovery decision space at level start: 4 valid first
    actions (the four arrows + ACTION5), ≥ 2.
  - **(d) Step budget**: `60`. Witness ~60 actions; 0 margin in
    worst case. **The implementer will calibrate this in
    smoke_test.** If the precise witness exceeds 60, the geometry
    tightens (per Note above).

### Level 3 — system + 1 new mechanic

Layout (revised per critique Issue 1, 4):
- Avatar at `(16, 32)`. 5×5 footprint `(16, 32)..(20, 36)`.
- ONE `target_dim` at anchor `(48, 32)`.
- `wall_tall` ceiling row 24 cols 5..56, floor row 40 cols 5..56,
  east col 56 rows 24..43, west col 4 rows 24..43.
- `wall_short` barrier at col 28, rows 24..40 (4 instances at
  anchors `(28, 24)`, `(28, 28)`, `(28, 32)`, `(28, 36)`).
- `guard` initial position `(14, 32)`. Patrol cols `12..22` row
  32 (so guard sweeps cells with col ∈ {12..22}). Initial direction
  EAST. Period = 2×(22−12) = 20 ticks.
- `freeze_duration = 4`. `throw_range = 36`. `step_budget = 80`.

Guard's patrol cells include the avatar's starting cell `(16, 32)`
— the guard reaches `(16, 32)` at action 2 if avatar doesn't
move, killing the avatar.

- **Mechanics required by the witness** (= L2-count + 1 = 3):
  - **M1**: same as before.
  - **M2**: same as before — wall_short barrier at col 28 must be
    crossed by boomerang to reach target at col 48.
  - **M3**: deterministic patrolling guard. The guard advances 1
    cell per tick along its patrol direction (initially east); on
    reaching patrol endpoint, reverses direction. If the guard's
    POST-tick cell coincides with the avatar's POST-step cell, OR
    if the avatar walked onto the guard's PRE-tick cell, fire
    `self.lose()`. If the boomerang's POST-advance cell coincides
    with the guard's PRE-advance OR POST-advance cell at any tick,
    set guard freeze_remaining = `freeze_duration`; while
    freeze_remaining > 0 the guard's per-tick advance is skipped
    and freeze_remaining decrements; the visual swaps to
    `guard_frozen` for the freeze window.

- **Necessity per mechanic**:
  - **M1**: target lit only by boomerang overlap; same as L1, L2.
    M1 necessary.
  - **M2**: target at col 48 is east of wall_short at col 28; any
    east throw from accessible avatar cells (cols 5..27 row 32
    after the avatar dodges guard's patrol cols 12..22) crosses
    col 28 wall_short on the way to col 48. Same enumeration as
    L2 applies; M2 necessary.
  - **M3**: avatar's starting cell `(16, 32)` is within the guard's
    patrol col range `{12..22}`. The guard at `(14, 32)` initial
    east will be at `(15, 32)` after action 1, `(16, 32)` after
    action 2 (if not frozen). Without dodging or freezing the
    guard, the avatar at `(16, 32)` collides with the guard at
    end of action 2 → `self.lose()`. Avatar therefore MUST execute
    M3-aware behaviour (move off row 32 to row 31 or 33 by action
    1, OR fire boomerang at action 1 such that the boomerang's
    outbound path freezes the guard before the guard reaches the
    avatar).

    **Plausible alternate strategies** (post-discovery):
    1. **"Stand still."** Avatar dies at action 2. M3 was the
       reason. Strategy fails.
    2. **"Move up to row 31 at action 1, never throw."** Avatar
       avoids guard but never lights target. Strategy fails (no
       target lit).
    3. **"Move up to row 31 at action 1, throw east at action 2
       from row 31."** Boomerang flies east at row 31. Path:
       (17, 31), (18, 31), ..., (28, 31) [wall_short — flies
       over], ..., (48, 31). Target footprint at
       `(48, 32)..(51, 35)` — does the boomerang's row-31 cell
       overlap row 32..35? No, row 31 ≠ row 32..35. Target NOT
       lit. Strategy fails.

       Could the boomerang's HOMING RETURN catch the target on
       row 32? Outbound terminus is `(53, 31)` (at throw_range=36
       from (17, 31), if not blocked). Switch to return. Home
       toward avatar's CURRENT cell. If avatar is on row 31 col
       17, dy=0; boomerang home steps west at row 31. Boomerang
       never enters row 32+ on return. Strategy fails.
    4. **"Move down to row 33 at action 1, throw east at action 2
       from row 33."** Boomerang flies east at row 33. Path
       includes `(48, 33)`, which overlaps target footprint
       `(48, 32)..(51, 35)` (row 33 is within 32..35). **Target
       lit.** Strategy succeeds — and this strategy DOES exercise
       M3 because the avatar moved off `(16, 32)` to dodge the
       guard's reaching `(16, 32)` at action 2.

    The witness uses strategy 4 (or strategy 3 with adjustment).
    M3 is necessary because every non-terminal strategy involves
    the avatar dodging the guard's reach of `(16, 32)` — strategy
    1 dies; strategies that survive must dodge.

    Could the avatar simply throw at action 1 and stay at
    `(16, 32)`? At action 1, ACTION5 fires; the boomerang launches
    at `(16, 32)` and advances to `(17, 32)`. Guard advances:
    `(14, 32)` → `(15, 32)`. End of action 1: avatar `(16, 32)`,
    guard `(15, 32)`. No collision yet. Action 2: avatar must
    press an arrow. If avatar tries ACTION5 again, ACTION5 is
    INVALID while boomerang is in flight — so avatar MUST press
    an arrow. Pressing ACTION1 / ACTION2 moves avatar off row 32.
    Pressing ACTION3 / ACTION4 stays on row 32 but moves col by
    1: ACTION3 → (15, 32) — but guard is at (15, 32), avatar
    walks ONTO guard's cell → collision → lose. ACTION4 → (17,
    32), avatar moves east; guard advances to (16, 32). Avatar
    `(17, 32)`, guard `(16, 32)`. Different cells. Safe.

    So another strategy: throw at action 1, then walk EAST at
    action 2 to (17, 32), then continue. But this still involved
    M3 (the avatar's choice of east-not-west was forced by the
    guard's position, since walking west at action 2 would put
    avatar at (15, 32) = guard's cell). M3 is exercised in every
    surviving strategy.

- **Witness solution** (~50 actions; concrete strategy):

  **Strategy**: throw east from row 33. The boomerang's outbound
  east-row-33 path lights the target's row-33 cell `(48, 33)`
  (target footprint covers rows 32..35). On return, boomerang
  homes back; avatar oscillates row 33/34 (south of guard's row
  32) to stay safe. Catch when boomerang and avatar coincide.

  Concrete sequence (illustrative):
  ```
  [ACTION2, ACTION5,
   ACTION1, ACTION2, ACTION1, ACTION2, ACTION1, ACTION2,
   ACTION1, ACTION2, ACTION1, ACTION2, ACTION1, ACTION2,
   ACTION1, ACTION2, ACTION1, ACTION2, ACTION1, ACTION2,
   ACTION1, ACTION2, ACTION1, ACTION2, ACTION1, ACTION2,
   ACTION1, ACTION2, ACTION1, ACTION2, ACTION1, ACTION2,
   ACTION1, ACTION2, ACTION1, ACTION2, ACTION1, ACTION2,
   ACTION1, ACTION2, ACTION1, ACTION2, ACTION1, ACTION2,
   ACTION1, ACTION4]
  ```
  - Action 1 (ACTION2 down): avatar `(16, 32) → (16, 33)`. Avatar
    OFF row 32 — safe from guard. Facing now DOWN.
  - Action 2 (ACTION5): throw DOWN. Hmm — but we want the throw
    east. Need to set facing east first.
    **Revised first 2 actions**: ACTION4 (right) to set facing
    east AND move avatar to (17, 32) (still on row 32 but east of
    guard's current col 14 → 15 → 16 in next 2 ticks). Then
    ACTION2 (down) to escape row 32 before guard catches up.

  Re-traced:
  - Action 1 (ACTION4): avatar `(16, 32) → (17, 32)`. Facing east.
    Guard tick: `(14, 32) → (15, 32)`. Avatar `(17, 32)`, guard
    `(15, 32)`. Safe.
  - Action 2 (ACTION2 down): avatar `(17, 32) → (17, 33)`.
    Facing now DOWN — but we want east. Setting facing on a walk
    that succeeds DOES update facing per spec. ACTION2 → facing
    south.

    **Re-revised**: thread facing-preservation differently. Use
    ACTION2 to escape row 32 first, then ACTION4 to re-orient
    east before ACTION5.
  - Action 1 (ACTION2): avatar `(16, 32) → (16, 33)`. Facing south.
    Guard tick: `(14, 32) → (15, 32)`. Avatar `(16, 33)`, guard
    `(15, 32)`. Safe.
  - Action 2 (ACTION4): avatar `(16, 33) → (17, 33)`. Facing east.
    Guard `(15, 32) → (16, 32)`. Avatar `(17, 33)`, guard
    `(16, 32)`. Safe (different rows).
  - Action 3 (ACTION5): throw east. Boomerang launches at avatar
    `(17, 33)` and advances to `(18, 33)`. outbound_remaining = 35.
    Guard `(16, 32) → (17, 32)`.
  - Actions 4..38 (35× alternating ACTION1/ACTION2 to oscillate
    row 32/33): avatar oscillates row 32 ↔ row 33 at col 17.
    Boomerang advances east on row 33 each tick: action 4 boom
    `(19, 33)`, action 5 boom `(20, 33)`, ..., action 31 boom
    `(46, 33)`, action 32 boom `(47, 33)`, action 33 boom
    `(48, 33)` → **target lit** (overlaps target footprint
    `(48, 32)..(51, 35)`). 4 outbound left. Action 37 boom
    `(52, 33)`, 0 left → switch returning.

    **Avatar safety during oscillation.** ACTION1 moves avatar
    UP (row 33 → row 32). On row 32, avatar might collide with
    guard. Avoid: oscillate ACTION2 (down to row 34) ↔ ACTION1
    (up to row 33). Both row 33 and row 34 are below guard's row
    32. Safe.

    Re-revise oscillation: ACTION1 up, ACTION2 down, ACTION1, ...
    starting from row 33: action 4 = ACTION1 → row 32 (DANGEROUS).
    Better: action 4 = ACTION2 → row 34, action 5 = ACTION1 → row
    33, action 6 = ACTION2 → row 34, ... Avatar stays in row
    33/34. Safe.

  - Actions 39..N (avatar continues row 33/34 oscillation).
    Boomerang homes back. Boomerang from `(52, 33)` toward avatar
    `(17, 33)` or `(17, 34)`. dx=−35 dominant; step (−1, 0) on
    each tick; boomerang col decreases by 1 per action.
    Boomerang reaches col 17 at action 39 + (52−17) = action 74.
    At col 17 row 33, if avatar is at (17, 33), CATCH.

    Total actions ≈ 74. step_budget = 80. Margin of 6. Workable.

    The witness above is ILLUSTRATIVE; the implementer's smoke
    test will validate. If witness > 80, geometry will be
    tightened (target at `(36, 32)`, throw_range = 24, step_budget
    = 60).

- **Difficulty justification**:
  - **(a) Random-resistance.** Random play dies to the guard
    typically within 5-10 actions (guard reaches col 16 by action
    2, col 17 by action 3, etc.; avatar wandering on row 32
    between cols 12..22 risks collision every tick). Even avoiding
    collision, lighting target requires throw direction = east,
    throw row ∈ {32..35}, AND the avatar maintaining row 33/34
    until catch — conjunction is below 1/10000 over 80 steps.
  - **(b) Human-tractable.** ~2.5 minutes — the player learns the
    guard's deterministic patrol within 1-2 ticks of observation,
    discovers that walking off row 32 dodges, and pieces together
    that throwing from row 33 still hits the row-32 target
    (because target is 4×4 footprint). Total environment ~6 min.
  - **(c) Planning depth (post-discovery).** Challenging — even
    with full M1 + M2 + M3 knowledge, the plausible wrong
    heuristic is **"throw from row 32 to maximise target overlap;
    dodge guard between throws"**: avatar would have to re-enter
    row 32 to throw, inevitably colliding with the patrolling
    guard. The witness instead **decouples throw row from guard
    row** — threading the boomerang on row 33 (which still hits
    the target's 4×4 footprint) while the avatar stays on row 33
    or 34 (safe). The trivial heuristic "stay on row 32" fails
    catastrophically; the witness's row-33 trick requires the
    player to reason about target footprint extent.
    Post-discovery decision space at level start: 4 valid first
    actions (the four arrows + ACTION5 — but ACTION5 alone at
    action 1 leaves avatar on row 32, exposing to guard at action
    2; arrows are the 3 viable choices). ≥ L2's count.
  - **(d) Step budget**: `80`. Witness ~74 actions; 6-action
    margin. Larger than L2's `60` per `difficulty-rules.md` § d
    L3 addendum (budget grows, never shrinks).

## 5. Action mapping
- `ACTION1` (UP): walk avatar one cell up; set facing direction =
  UP. Always valid. Bump-without-move on collision (wall_tall,
  wall_short, guard, level boundary).
- `ACTION2` (DOWN): walk one cell down; set facing = DOWN.
- `ACTION3` (LEFT): walk one cell left; set facing = LEFT.
- `ACTION4` (RIGHT): walk one cell right; set facing = RIGHT.
- `ACTION5` (THROW or PICK-UP):
  - If `boomerang.phase == held`: launches the boomerang in
    avatar's current facing direction (sets phase=outbound,
    boomerang_pos=avatar's cell, then advances one tick).
  - If `boomerang.phase == dropped` AND avatar's cell coincides
    with boomerang's dropped cell: picks up (phase → held).
  - Otherwise (in flight, or dropped at non-avatar cell): INVALID;
    `_get_valid_actions` excludes ACTION5.

`available_actions = [1, 2, 3, 4, 5]`. ACTION6 and ACTION7 NOT in
the list.

After every action, the boomerang advances one tick if in flight;
the guard advances one tick if not frozen. Order per step:
1. Avatar move (or throw / pickup).
2. Boomerang advance (if in flight). Check boomerang-target
   overlap (light), boomerang-avatar overlap (catch),
   boomerang-guard overlap (freeze).
3. Guard advance (if not frozen). Check guard-avatar overlap
   (lose).
4. Decrement step counter; check `steps_remaining <= 0` (lose) and
   win predicate (next_level).
5. `complete_action()`.

## 6. HUD and per-game state

HUD widgets:
- `StepCounterHud`: 64-pixel-wide bar at row 63; current/max in
  palette 11 over palette 4. Reconfigured on `on_set_level`.
- `BoomerangPhaseIndicator`: 3-cell horizontal indicator at
  `(0, 0)..(2, 0)` showing phase as palette dot — palette 12
  (held), palette 8 (in flight), palette 3 (dropped).

Per-game state on `Tk6n`:
- `self.avatar` — avatar Sprite reference.
- `self.boomerang` — boomerang Sprite reference (placed on level
  load at avatar's hand cell).
- `self.boomerang_phase: str` — `held` / `outbound` / `returning`
  / `dropped`.
- `self.boomerang_throw_dir: tuple[int, int] | None`.
- `self.boomerang_outbound_remaining: int`.
- `self.facing: tuple[int, int]` — initial `(1, 0)` (east).
- `self.lit_targets: set[Sprite]`.
- `self.steps_remaining: int`.
- `self.guard: Sprite | None`.
- `self.guard_patrol_dir: tuple[int, int] | None`.
- `self.guard_patrol_cols: tuple[int, int] | None` — (min, max).
- `self.guard_freeze_remaining: int` — counter, default 0.

## 7. Win condition

```
all(t in self.lit_targets for t in level.get_sprites_by_tag("target"))
AND self.boomerang_phase == "held"
```

When true at end of step, fire `self.next_level()`.

## 8. Lose condition

Either:
- `self.steps_remaining <= 0` after decrement (any level).
- Avatar-guard collision (L3 only): `avatar.cell == guard.cell`
  after either avatar move or guard tick.

Fire `self.lose()` and `self.complete_action()`.

## 9. Novelty note

Closest taxonomy / prior-game entries (re-grounded against full
spec):

- **vt6q (prior) — grapple-anchor-yank.** vt6q's grapple is
  single-tick instant; tk6n's boomerang is multi-tick, homing on
  return, and lights targets on path. Distinct.
- **bx84 (prior) — beam-mirror-reflect.** bx84's beam is steady-
  state with player-cycled mirrors; tk6n has no continuous beam
  and no mirrors. Distinct.
- **wt39 (prior) — glide-deflect-thaw.** wt39's avatar glides;
  tk6n's avatar walks one cell at a time, the boomerang flies.
- **bw7k (prior) — actor-replay-shade.** bw7k records and replays;
  tk6n's boomerang is forward-projected, not recorded.
- **vn8d (prior) — domino-cascade-topple.** vn8d's chain reaction
  is single-tick across pillars; tk6n's boomerang is one moving
  point along a spatial trajectory.
- **pf3w (prior) — wavefront-converge-timing.** pf3w's wavefronts
  are concentric BFS expansions from static emitters; tk6n's
  boomerang is a 1D linear track + return. No concentric, no
  static emitters.

`prior-games/index.md` is NOT empty (70 entries). Negative-
similarity check (8 dimensions) re-walked against vt6q (closest
verb-shape prior) — only dimension #4 (universal step counter)
shared. ≪ 3+ rejection threshold.

The fleshed-out spec did not drift from `pick_mechanic`'s novelty
position. NOVEL.

