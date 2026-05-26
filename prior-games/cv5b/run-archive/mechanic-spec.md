# mechanic-spec — cv5b

## 1. Title
Arc-Launch Target Practice.

## 2. Mechanic family
**arc-launch-target.** A movable launcher walks the playfield (basic
physics + objectness) and fires a marble along a *parabolic arc* from
launcher to a clicked landing cell (basic physics — gravity-bound
trajectory; basic geometry — apex height vs barrier height). Power-cycle
adjusts both range and apex (geometry). Shields block any path
(objectness + topology). At L3, a wind-band column deflects the arc by
+1 cell (basic physics — directional advection). Priors used:
**objectness, basic geometry+topology, basic physics**.

## 3. Sprite roster
- `launcher_p1` — 6×6, palette {12 orange frame, 11 yellow charge dot ×1
  in dot row}, tags=[`launcher`,`launcher_p1`]; the active launcher when
  power=1; placed visible at level start, the other two variants placed
  at the same cell with `InteractionMode.REMOVED`.
- `launcher_p2` — 6×6, frame 12, two yellow dots in dot row, tags=[
  `launcher`,`launcher_p2`].
- `launcher_p3` — 6×6, frame 12, three yellow dots in dot row, tags=[
  `launcher`,`launcher_p3`].
- `marble` — 2×2 solid white (palette 0), tags=[`marble`]; spawned during
  fire animation, removed at end. `InteractionMode.INTANGIBLE` so it
  passes through other sprites for visual.
- `arc_dot` — 1×1 maroon (palette 13), tags=[`arc_preview`]; many
  instances rendered along the parabola for preview, refreshed each
  step.
- `shield` — 2×6 vertical bar, palette 5 black, tags=[`shield`,`block`];
  blocks both player walking and arc trajectory.
- `target_ring` — 3×3 ring (hollow centre, palette 7 pink frame),
  tags=[`target`,`target_ring`]; placed so that the SPRITE's
  (target.x+1, target.y+1) is the "target_centre"; the level config
  records target_centre coordinates (e.g. `(24, 50)`); arc landing
  predicate is `arc_end_cell == target_centre`. (Issue 4 — fixed: 3×3
  ring with explicit centre semantics.)
- `wind_marker` — 2×8 vertical column with palette 10 light-blue
  alternating with palette 1 off-white in a stippled pattern,
  tags=[`wind`]; visual indicator of the wind region; intangible (does
  not block walk).
- `step_counter_ui` — RenderableUserDisplay drawing at row 0 a
  proportional bar in palette 0 / palette 4.
- `ground` — 64×2 strip palette 14 green, rows 51-52 (subtle decoration;
  intangible).

Internal pixel pattern for `launcher_p3` (illustrative; the actual array
is in the source):
```
 .  12 12 12 12  .
12  12 11 11 12 12
12  11 11 11 11 12
12  11 11 11 11 12
12  12 12 12 12 12
 .  12 12 12 12  .
```
`launcher_p2` has only the middle two columns of the dot rows in 11;
`launcher_p1` has only the centre two cells of the inner dot row in 11.

Palette signature: `{10 light-blue sky, 14 green ground, 12 orange
launcher, 11 yellow charge dots, 13 maroon arc, 5 black shield, 7 pink
target, 0 white marble, 1 stipple-light, 4 hud-fill}`. Distinct from
prior `{4,8,9}` cautionary signature.

## 4. Level progression, mechanic enumeration, and witness solutions

Grid size 64×64 across all 3 levels (default camera, no resize). Sky
palette 10 background; ground rows 51-52 (decorative); launcher and
ground targets sit at row 50.

**Power table** (revised per critique Issue 2):
| Power | Apex | Range (max horizontal distance launcher→landing) |
|---|---|---|
| 1 | 3 | 16 |
| 2 | 8 | 24 |
| 3 | 15 | 36 |

**Mechanic counts after revision (Issue 1, 3):** L1=1 (arc-fire),
L2=3 (+walk +power-cycle, +2), L3=5 (+shield-blocks-arc
+wind-deflects-arc, +2). Both inc within +1 or +2 rule.

### Level 1 — base dynamic system (single-mechanic tutorial)
- **Mechanics required by the witness (N=1):**
  - **M_arc: arc-fire.** ACTION6 fires a marble along a parabolic arc
    from launcher centre to the clicked grid cell. Arc parameter at
    fraction `s ∈ [0,1]`: `x(s) = lx + (cx-lx)*s`,
    `y(s) = round(ly + (cy-ly)*s - apex*4*s*(1-s))` where `apex` is
    the current power's apex constant. On landing, if `arc_end_cell ==
    target_centre`, that target is consumed.

- **Configuration:** Launcher_p1/p2/p3 placed at `(4, 50)` (only p1
  TANGIBLE). Target_ring at target_centre `(16, 50)`. No shield. No
  wind. Distance 12 < power-1 range 16, so default power-1 fire
  reaches.

- **Necessity per mechanic:**
  - *L1 cannot be solved without M_arc because* there is no other verb
    that triggers the target-hit predicate; walking onto a target does
    not register because target_ring is intangible to launcher walk
    and the win predicate fires only on arc-landing.

- **Witness solution:** `[ACTION6@(16, 50)]`. 1 action.

- **Difficulty justification (per `difficulty-rules.md` § 2; Issue 5):**
  - *(a) Random-resistance:* L1 is the tutorial; per from-tech-report.md
    §3.4, "Random agents can occasionally stumble into success at this
    stage, which is acceptable by design." With 4096 cells and one
    target_centre, P(random-fire-hits) ≈ 1/4096; the strict 1/10000
    random-resistance threshold applies to L2 and L3, not L1.
  - *(b) Human-tractable:* a first-time player sees launcher + target
    + arc preview dots; clicking on the target works on the first try.
    ~30 seconds.
  - *(c) Planning depth:* none — single-action win post-discovery.
  - *(d) Step budget:* `step_budget = 12` (witness 1; budget = 12×).
    Generous to allow exploratory misclicks.

### Level 2 — base system + 2 new mechanics
- **Mechanics required by the witness (M = N+2 = 3):**
  - **M_arc: arc-fire** *(carried from L1)*.
  - **M_walk: walk-launcher.** ACTION1-4 walks the active launcher one
    cell in that cardinal direction; clamped to playfield bounds (0..63
    in x and y); blocked by shield cells (introduced at L3).
  - **M_power: power-cycle.** ACTION5 cycles power `1 → 2 → 3 → 1`,
    swapping the visible launcher variant. Higher power = wider range
    AND higher apex (per power table above).

- **Configuration:** Launcher_p1/p2/p3 at `(4, 50)`. Target_a centre
  `(28, 50)`; target_b centre `(50, 50)`. No shield, no wind.

- **Necessity per mechanic:**
  - *L2 cannot be solved without M_arc because* it is the only verb
    that registers a target hit.
  - *L2 cannot be solved without M_walk because* target_b at `(50, 50)`
    is at distance 46 from launcher start `(4, 50)`, exceeding the
    longest power-3 range (36). The launcher must walk to `x ≥ 14` to
    bring distance ≤ 36 (= 50 - 14). No fire-only sequence reaches
    target_b.
  - *L2 cannot be solved without M_power because* (i) target_a at
    `(28, 50)` is at distance 24 from start, exceeding default power-1
    range (16) — power-2 (range 24) is the minimum to reach; (ii)
    target_b at `(50, 50)` from the closest fit-in-budget walked
    position (`x = 14`, distance 36) requires power-3 (range 36). No
    sequence within step_budget = 30 wins without at least one
    power-cycle.

- **Witness solution:**
  `[ACTION5,                         # cycle power 1→2
    ACTION6@(28, 50),                # fire target_a from x=4 with apex 8
    ACTION4, ACTION4, ACTION4, ACTION4,
    ACTION4, ACTION4, ACTION4, ACTION4,
    ACTION4, ACTION4,                # walk 10 right to x=14
    ACTION5,                         # cycle power 2→3
    ACTION6@(50, 50)]                # fire target_b from x=14 with apex 15
  ` 14 actions.

  **Witness verification.** From `(4, 50)` at power-2 (apex 8, range 24):
  arc to `(28, 50)`, distance 24, in range. Arc `y(s=0.5) = 50 - 8 = 42`;
  no shield, no obstacle; lands at target_a centre. ✓ Then walk 10 right
  (no shield blocking). At `(14, 50)` at power-3 (apex 15, range 36):
  arc to `(50, 50)`, distance 36, in range. `y(s=0.5) = 50 - 15 = 35`,
  no obstacle; lands at target_b centre. ✓

- **Difficulty justification:**
  - *(a) Random-resistance:* the click cell space is 4096 with 2
    target_centres registering a hit. To register, the agent also needs
    the launcher in range of each target — power-1 from start reaches
    only target cells within distance 16 (none of the targets), so
    random clicks at default power achieve P(hit) = 0. Random walks
    occasionally stumble into a position from which power-1 can reach
    target_a (e.g. x=12 distance 16 reaches), but reaching target_b
    requires walk + power-cycle in a coordinated sequence; combined
    P(random win) ≪ 1/10000.
  - *(b) Human-tractable:* observing power-cycle (3 visible launcher
    variants with 1/2/3 dots) plus arc-preview-distance teaches the
    range-vs-power link in a few exploratory fires. ~2 minutes.
  - *(c) Planning depth — moderate (post-discovery).* Post-discovery
    decision space at level start: 5 valid first actions
    (ACTION1/2/3/4 walk, ACTION5 cycle; fire at default power lands
    short of any target). Plausible-but-wrong alternative: *walk all
    the way to x=34 (30 walks) and fire at default power-1 toward
    target_b at distance 16, then walk back* — exceeds step budget 30
    when both targets are accounted for, since reaching target_a
    afterward requires walking back and is far over budget. Witness
    reasoning chain: (1) target_a at moderate distance → cycle to
    power-2 to gain range — fire; (2) target_b further away → walk
    closer rather than over-cycle (range can't be extended past 36)
    → walk; (3) cycle to power-3 for the final 36-distance shot →
    fire. Each step bounded by step budget; the player must pick the
    actions in this order because firing target_b first from start
    (any power) leaves target_a unreachable within budget.
  - *(d) Step budget:* `step_budget = 30` (witness 14; budget ≈ 2.1×).

### Level 3 — system + 2 new mechanics
- **Mechanics required by the witness (= L2-count + 2 = 5):**
  - **M_arc: arc-fire** *(carried from L1, L2)*.
  - **M_walk: walk-launcher** *(carried from L2)*.
  - **M_power: power-cycle** *(carried from L2)*.
  - **M_shield: shield-blocks-arc.** A `shield` sprite is a tall
    vertical wall (2 cols wide × 6 rows tall, palette 5 black). It
    blocks player walking onto its cells AND any arc cell that
    overlaps a shield pixel; an arc that overlaps a shield is
    absorbed (marble disappears, no target registered).
  - **M_wind: wind-deflects-arc.** A `wind_marker` column (col 36, rows
    30-50, palette stippled 1+10) deflects every fired arc that has any
    cell overlapping the wind region: the arc's final landing is shifted
    +1 cell rightward (post-application). Walks through wind cells are
    NOT deflected. The arc-preview rendering shows the wind-corrected
    landing so the player can see the predicted trajectory before
    firing.

- **Configuration:** Launcher_p1/p2/p3 at `(4, 50)`. Static shield
  occupies cols 16-17 rows 44-50 (sprite placed at `(16, 44)`, 2×6).
  Wind_marker at col 36 rows 30-50 (sprite placed at `(36, 30)`, 1×21,
  intangible). Target_ring centre `(50, 50)`.

- **Necessity per mechanic:**
  - *L3 cannot be solved without M_arc because* it is the only
    target-registering verb.
  - *L3 cannot be solved without M_walk because* target at `(50, 50)` is
    at distance 46 from launcher start, exceeding even power-3 range
    (36). Walk to `x ≥ 14` is required (at `x=14`, distance to target
    is 36 — at-the-boundary range); but walking from `(4, 50)` to
    `(14, 50)` is BLOCKED by the shield at cols 16-17 (which the
    launcher would not yet hit at x=14, but to walk further it must
    cross col 16 — which is shield territory). The launcher's only
    path to a firing position is up-and-over the shield.
  - *L3 cannot be solved without M_power because* from the closest
    feasible post-shield ground position `(20, 50)`, distance to
    target = 30; power-2 (range 24) doesn't reach; power-3 (range 36)
    does. Default power-1 reaches only 16, no usable post-shield
    position has target within 16. Power-cycle required.
  - *L3 cannot be solved without M_shield because* the shield at cols
    16-17 rows 44-50 blocks the ground walk corridor; every winning
    path either (a) walks up and around the shield (which IS the
    shield rule constraining movement) or (b) fires high-apex arcs
    (which IS the shield rule constraining low arcs). No winning
    sequence avoids the shield's behaviour.
  - *L3 cannot be solved without M_wind because* the wind column at
    col 36 lies between any post-shield launcher position
    (`x ∈ [18, 22]`) and the target at `x = 50`. A power-3 arc from
    that x-range to target naturally has its midpoint apex around
    col 32-36 with arc-y ≈ 35 (well inside wind rows 30-50). Wind
    drift +1 means: aiming at click `(50, 50)` lands at `(51, 50)` —
    miss. Aiming at `(49, 50)` (one cell left of target) lands at
    `(50, 50)` — hit. The wind-correction is mandatory.

    *Counterfactual escape attempt:* could the player fire from a
    position where the arc avoids the wind region? Wind extends rows
    30-50 (the entire vertical extent below row 30). Power-3 arc has
    midpoint apex of 15 above launcher row, reaching y ≈ 35 from row
    50 — inside the wind region. Even firing from elevated launcher
    position (e.g., row 43) would have arc y ≈ 28-30 at midpoint,
    still grazing the wind region's top. There is no fire trajectory
    from any reachable launcher position to target that avoids wind.

- **Witness solution:**
  ```
  [ACTION4, ACTION4, ACTION4, ACTION4, ACTION4,
   ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4,  # 11 right to (15, 50)
   ACTION1, ACTION1, ACTION1, ACTION1, ACTION1, ACTION1, ACTION1,
                                                          # 7 up to (15, 43)
   ACTION4, ACTION4,                                       # 2 right to (17, 43)
   ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2,
                                                          # 7 down to (17, 50)
   ACTION4,                                                # 1 right to (18, 50)
   ACTION5, ACTION5,                                       # cycle power 1→2→3
   ACTION6@(49, 50)]                                       # fire (wind-corrected aim)
  ```
  31 actions.

  **Witness verification.** From `(18, 50)` at power-3 (apex 15,
  range 36): aim at `(49, 50)`, distance 31, in range. Arc passes
  col 36 at `s = (36-18)/(49-18) = 18/31 ≈ 0.581`. Apex contrib
  `4 * 15 * 0.581 * 0.419 ≈ 14.6`. Line `y = 50 + (50-50)*0.581 = 50`.
  Arc `y = 50 - 14.6 ≈ 35.4 → row 35`. Wind region rows 30-50; row 35
  is INSIDE wind. Arc gets +1 drift. Final landing `(49+1, 50) =
  (50, 50)`, the target_centre. Hit. ✓

  Shield-clearance check: arc passes col 16 (shield col) at
  `s = (16-18)/(49-18) = -2/31 < 0`, so col 16 is NOT on the arc path
  (launcher is right of shield). No shield interaction at fire time.
  The shield mechanic is exercised by the WALK-around route earlier
  (cols 16-17 ground row blocked, forcing up-and-down path).

- **Difficulty justification:**
  - *(a) Random-resistance:* random walks have near-zero chance of
    finding the up-and-around path; the shield rejects most directional
    attempts. Random clicks face the wind-corrected aim — visually-
    obvious `(50, 50)` lands at `(51, 50)` (miss). Combined random win
    P ≪ 1/10000.
  - *(b) Human-tractable:* a player who has finished L1 and L2 already
    knows walk + power + fire. The shield is visually obvious (tall
    black bar) — the player learns it blocks both walking and arcs by
    trying once. The wind region is stippled — visually distinct —
    and the arc-preview-with-drift teaches the +1 shift after one or
    two test fires. ~3 minutes for an attentive player.
  - *(c) Planning depth — challenging post-discovery.* Decision space
    at level start: 4 valid first actions
    (ACTION1/2/3/4; fire+cycle don't help yet — target unreachable
    even at max power from x=4). **Trivial heuristic that fails:**
    *"walk-greedily-right toward target; fire when in range"*. A
    fully-informed player following this heuristic walks right
    through cols 0-15 (11 actions), then attempts ACTION4 at col
    15 — blocked by shield. Then re-routes up-and-over (7 up + 2
    right + 7 down = 16 walks), now at `(17, 50)`. Distance to
    target `(50, 50)` = 33. Cycles power 2 → 3 (2 actions); fires at
    `(50, 50)` directly (the visually-obvious aim). With wind drift,
    arc lands at `(51, 50)` — miss. Heuristic fails because it does
    not account for the wind correction. **Heuristic-vs-witness
    divergence:** at action 27 (after walking up-around-down to
    `(17, 50)` and cycling power), the heuristic clicks `(50, 50)`
    while the witness clicks `(49, 50)`. The heuristic's miss at
    that action is unrecoverable within budget because the launcher
    is at-range only from x=14..22 (post-shield positions), and a
    second fire would need another power-cycle (1 action) plus
    re-aim — putting the total over budget. The witness's choice
    requires *forward reasoning*: simulate the arc, observe arc
    cells overlap wind, predict drift, aim one cell left.
  - *(d) Step budget:* `step_budget = 50` (witness 31; budget ≈ 1.6×).
    Generous over witness; allows one or two test fires that fail
    before the player figures out the wind correction.

## 5. Action mapping
- `ACTION1`: MOVE LAUNCHER UP 1 cell. Clamped at y ≥ 0 and not into
  shield cells.
- `ACTION2`: MOVE LAUNCHER DOWN 1 cell. Clamped y ≤ 63 and not into
  shield/wind/ground.
- `ACTION3`: MOVE LAUNCHER LEFT 1 cell.
- `ACTION4`: MOVE LAUNCHER RIGHT 1 cell.
- `ACTION5`: CYCLE POWER 1→2→3→1. Swaps `launcher_pN` interaction modes;
  the active variant is the only TANGIBLE one; updates apex and range
  for next fire.
- `ACTION6`: CLICK at `(x, y)` (display pixel coords; converted via
  `camera.display_to_grid`). FIRE arc from active launcher to the
  clicked grid cell. Arc cells animated over 6 frames. Wind drift
  applied if any arc cell lies in `wind_marker` region.
- ACTION7: NOT DECLARED (no undo). Per `action-enum.md` §"Slot 7 is
  strict-undo": omitted because the game has no meaningful undo verb.
- `available_actions = [1, 2, 3, 4, 5, 6]`.

## 6. HUD and per-game state
**HUD widgets:**
- `StepCounterHud` — `RenderableUserDisplay` drawing a depleting bar at
  row 0, palette {0 white = remaining, 4 off-black = consumed}, width
  proportional to `current_steps / max_steps`.

**Internal state on the game class:**
- `power: int` (1, 2, or 3) — cycled by ACTION5; affects apex/range.
- `step_counter_ui` — HUD instance.
- `targets_remaining: list[Sprite]` — populated in `on_set_level` from
  `level.get_sprites_by_tag("target")`.
- `arc_preview_dots: list[Sprite]` — re-built each `step()` (after
  walk/cycle/fire animation completes), showing the parabolic
  trajectory at the current power and current click direction (towards
  the right edge of the playfield by default; conceptually, dots are
  optional UX sugar — NOT required for win).
- `fire_phase: int` — `-1` idle; `0..5` animation tick of the in-flight
  marble. While `fire_phase >= 0`, every `step()` advances the marble
  one arc cell, renders, and short-circuits before the next action's
  effects.
- `pending_arc_cells: list[tuple[int, int]]` — the precomputed integer
  cell sequence for the in-flight arc, including any wind-drift
  shift applied; consumed one cell per step during animation.
- Per-launcher variant sprite handles (`launcher_p1/p2/p3`) — kept
  co-located on every walk so the swap is invisible to the player
  beyond the dot pattern.

## 7. Win condition
After a fire animation completes, if the marble's final landing cell
matches the centre of any `target_ring` sprite (within the ring's 4×3
bounding box at the centre cell `(target.x+1, target.y+1)`), that
target is removed from the level and from `targets_remaining`. When
`len(targets_remaining) == 0`, call `self.next_level()` on the next
`step()` to flush the animation. After L3, the engine auto-fires
`self.win()` upon `next_level()` past the last index.

## 8. Lose condition
On every action, decrement `step_counter_ui` by 1. When `current_steps
== 0`, call `self.lose()`. There is no instant-fail collision (mis-
fired arcs simply waste an action; missed arcs are recoverable).

## 9. Novelty note

### Closest taxonomy entries (with concrete distinguishing rules)
- **`cd82` (orbit-fire-paint, ref):** cd82's tank rides an 8-slot ring
  *fixed around a central canvas* and fires *axial/diagonal slabs of
  colour into sectors of the canvas*; cv5b's launcher walks *freely on
  a 2D playfield* and fires a *parabolic-arc marble at a specific cell*.
  cd82 paints; cv5b consumes a target. cd82 has no apex/range cycle and
  no barrier-clearance.
- **`bp35` (gravity-fall-navigation, ref):** bp35's player IS the
  projectile under continuous gravity, steered by side-step inputs;
  cv5b's player walks a launcher and emits a separate marble. bp35
  routes via flippers and portals; cv5b chooses apex+range via
  power-cycle and aims at any cell.
- **`r11l` (centroid-puppet-leg, ref):** r11l drags a leg-sprite linearly
  across cells; cv5b's marble follows a curved parabola. r11l has no
  arc, no apex, no shield-clearance.

### Closest prior-game entries
- **`bx84` (beam-mirror-reflect, prior):** bx84 has a *static emitter*
  with player-placed *mirror cells* reflecting the beam at *right
  angles*; cv5b has a *mobile launcher* and a *parabolic curve* with
  no mirrors. bx84's beam is linear-segments determined by mirror
  layout; cv5b's arc is parametric in `s` with apex set by power.
- **`vt6q` (grapple-anchor-yank, prior):** vt6q's grapple line is
  *cardinal only* and *yanks an entity*; cv5b's arc is a 2D
  parabolic curve, free-angle landing, with NO yank — the marble is
  consumed at landing. vt6q has no power-cycle and no arc-clearance.
- **`qn7w` (pulse-chain-eject, prior):** qn7w propagates through
  *pre-placed ball-chains* (linear segments through pre-placed
  entities); cv5b is *free-air parabolic flight* with no pre-placed
  chain.
- **`pf3w` (wavefront-converge-timing, prior):** pf3w's wavefront is
  radially-symmetric BFS expanding from emitters; cv5b is a single
  directional curve.
- **`lq5x` (lantern-cone-illuminate, prior):** lq5x's cone is a static
  filled wedge; cv5b's arc is a single shot + animated trajectory.
- **`bz3k` (drift-impulse-cardinal, prior) and `wq3m` (current-drift-
  route, prior):** both involve drift, but on the *avatar* or *blocks*
  riding flows; cv5b's wind drifts the *arc trajectory* mid-flight,
  not a free-walking entity.

### Negative-similarity score
vs bx84 (closest visual analogue) — 2/8 dimensions shared (level goal,
lose condition); 6/8 distinct (board content, player input, support
cast, visual signature, sprite grain, core dynamic). PASS the negative
similarity gate.
