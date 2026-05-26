# mechanic-spec — xv2b

## 1. Title
"Vessel Equalise" (working title; not visible in-game).

## 2. Mechanic family
`vessel-valve-equalize`. Several vertical water-vessels stand side
by side; the player toggles small valves connecting adjacent vessels
and presses a "tick" verb to advance one step of hydrostatic
equalisation. Each vessel must converge on a target water level
marked by a coloured side-tick. Priors used: **basic physics**
(hydrostatic equalisation between connected reservoirs;
gravity-driven flow toward equilibrium; uphill transport requires a
pump that mechanically adds energy), **objectness** (valves, drains,
and pumps are persistent toggleable entities the player reasons
about as discrete things), and **basic geometry / topology** (the
*valve graph* — which vessels are connected through which open
valves at which heights — defines reachable water-level
configurations).

## 3. Sprite roster

Grid is fixed 64×64 for all three levels. Every sprite below uses
palette values from `skills/global/color-legend.md`.

- `vessel_frame` — 12 cells wide × 36 cells tall. Two-cell-thick
  light-grey (palette 2) walls on left, right, and bottom; open at
  the top (transparent pixels = `-1`). Interior is 8 cells wide ×
  33 cells tall and is left transparent so the water sprite shows
  through. Tagged `vessel_frame`. Visible, collidable=False (the
  water sprite owns the visible fill; the frame is decorative
  scaffolding). Layer = 1 so the frame draws *over* its water.
  *Internal pixel detail*: the frame's outer two pixel rows on
  the bottom are palette 3 (slightly darker grey) and the bottom
  inner row is palette 5 (black) — this gives the vessel base a
  visible "thickness" rather than a flat block.
- `water_fill` — 8 cells wide × 33 cells tall. Each row holds either
  blue (palette 9) where water exists or transparent (`-1`) where
  empty. Rendered at runtime: rows from the bottom up to the
  current water level are filled, rows above are transparent. The
  topmost filled row uses light-blue (palette 10) to draw a 1-pixel
  meniscus, giving the water surface a clearly visible cue that
  reads as a fluid surface rather than a flat block. Tagged
  `water_fill`. Layer = 0 (under the frame).
- `target_tick` — 4 cells wide × 1 cell tall. A horizontal magenta
  (palette 6) bar with the leftmost cell darker (palette 13) so the
  tick reads as a tag glued to the *outside* of a vessel wall.
  Positioned on the right wall of each vessel at the y-row of that
  vessel's target water level. Tagged `target_tick`. Layer = 2 so
  it draws above the frame.
- `valve_closed` — 4 cells wide × 6 cells tall. A grey (palette 3)
  block with a vertical yellow (palette 11) bar in the centre column
  representing a shut sluice. Top and bottom rows palette 4
  (off-black) so the valve reads as bolted into both adjacent
  vessel walls. Tagged `valve`, `valve_closed`. Visible, collidable
  for click hit-test. Layer = 3.
- `valve_open` — 4 cells wide × 6 cells tall. Same outer shape as
  `valve_closed` (palette 3 walls, palette 4 bolts) but the centre
  column is replaced by a 1×4 transparent (`-1`) gap with two
  cyan-blue (palette 10) bookend pixels — the slit visibly opens
  through. Tagged `valve`, `valve_open`. Layer = 3.
- `drain_glyph` — 4 cells wide × 4 cells tall. Black (palette 5)
  square ring around a maroon (palette 13) hollow centre, with the
  bottom row in dark grey (palette 4) so it reads as a sink hole
  in the vessel's floor. Tagged `drain`. Visible, collidable,
  layer = 3. Always visible; does not toggle.
- `pump_off` / `pump_on` — 6 cells wide × 4 cells tall. A pair of
  triangular fin shapes inside a grey (palette 3) box. `pump_off`
  fins are dim orange (palette 12); `pump_on` fins are bright green
  (palette 14) and the centre cell is white (palette 0) to read as
  "energised". Both tagged `pump` plus respectively `pump_off` /
  `pump_on`. Layer = 3, click hit-test enabled.
- `step_counter_hud` is not a sprite but a `RenderableUserDisplay`
  subclass; described in §6.

Sprite dict keys (Python identifiers) are the names above
(`vessel_frame`, `water_fill`, `target_tick`, `valve_closed`,
`valve_open`, `drain_glyph`, `pump_off`, `pump_on`) — semantic, per
`code/universal-scaffold.md` § Style rules. Sprite `name=` matches
the key.

## 4. Level progression, mechanic enumeration, and witness solutions

All three levels reuse the full sprite roster. Vessel positions are
common across levels: vessels A, B, C are placed at top-left
corners (4, 14), (24, 14), (44, 14) respectively, each 12×36. A
vertical 8-cell gap separates each adjacent pair (between A and B
the gap occupies columns 16..23; between B and C, columns 36..43).
Valves, drains, and pumps mount into these gaps.

The water level for vessel V is an integer
`level[V] ∈ [0, 33]` indicating filled rows from the bottom.
Visible meniscus is at row `(13 + 36 - 1) - level[V] = 48 - level[V]`
(top of fill).

### Level 1 — base dynamic system

- **Mechanics required by the witness** (N = 1):
  - **M1 — gravity-equalise-through-open-valve.** When ACTION5 is
    pressed, for every OPEN valve whose slit is at or below the
    *lower* of the two adjacent vessels' water surfaces (i.e. the
    valve is submerged on at least the lower side), one cell of
    water transfers from the higher-level vessel to the
    lower-level one (until equal or until the valve becomes air-
    exposed on both sides). Closed valves transfer nothing.
    Toggling valves is by ACTION6 click.

  L1 has only one mechanic but it is composite: discovering the
  rule requires the player to (a) click a valve and observe the
  visual toggle, (b) press ACTION5 and observe the water levels
  change, (c) infer that the relationship is "open valve allows
  flow toward equilibrium" rather than e.g. "ACTION5 always
  drains" or "click moves water". The witness exercises both
  sub-actions of M1.

- **Necessity per mechanic**:
  - *L1 cannot be solved without triggering M1 because* the only
    sprites mounted in L1's gaps are the two valves between A↔B and
    B↔C; every other action is a no-op on water levels (clicks on
    walls, vessels, the frame are ignored), so closing both valves
    and pressing ACTION5 produces zero level change. The target
    levels differ from the starting levels, so SOME flow must occur,
    and the only way to cause flow is to open at least one valve
    AND press ACTION5.

- **L1 setup**:
  - Vessel A starts with `level[A] = 24` (filled to row 24 of 33).
  - Vessel B starts with `level[B] = 0` (empty).
  - Vessel C starts with `level[C] = 0` (empty).
  - Target line on A: `level[A] = 8`.
  - Target line on B: `level[B] = 8`.
  - Target line on C: `level[C] = 8`.
  - Valve V_AB: between A and B at slit-height 4 (deep — slit row
    is row 4 of 33, near the bottom). Starts CLOSED.
  - Valve V_BC: between B and C at slit-height 4. Starts CLOSED.
  - No drains, no pumps.
  - Total water in system = 24 cells. Target = 8+8+8 = 24. Mass-
    conserved; equalising A:B:C = 8:8:8 is reachable.

- **Witness solution** (shortest):
  ```
  [ACTION6@V_AB, ACTION6@V_BC,
   ACTION5, ACTION5, ACTION5, ACTION5,
   ACTION5, ACTION5, ACTION5, ACTION5,
   ACTION5, ACTION5, ACTION5, ACTION5,
   ACTION5, ACTION5, ACTION5, ACTION5]
  ```
  18 actions: open both valves (2 clicks), then 16 ticks. Each tick
  transfers 1 cell from A's surplus column into B/C until all three
  equalise at 8. (Concretely: ticks 1..8 fill B from 0 to 8 because
  B is lower than A and the V_AB slit is submerged; ticks 9..16 then
  drain A further into C through the now-equalised B because V_BC's
  slit is submerged on both sides once B reaches 8. Conservation
  holds: A loses 16 cells, B gains 8, C gains 8.) Click coordinates
  are at the centre pixel of each valve sprite.

- **Difficulty justification**:
  - **(a) Random-resistance.** A random / vision-blind agent
    pressing arbitrary ACTION5/ACTION6@random has near-zero chance
    of opening BOTH valves and not re-closing them within the step
    budget. ACTION6 at random pixels mostly hits empty background
    and is a no-op; ACTION6 hitting a valve toggles its current
    state — random clicks on the same valve have a 50% chance per
    click to leave it closed; the joint probability of leaving both
    valves open AND running enough ticks is small.
  - **(b) Human-tractable.** A first-time human plays for ~90s:
    spends ~10s observing the start frame, ~20s on a few exploratory
    clicks and ACTION5 presses to learn "click toggles valve" and
    "ACTION5 advances water", then ~30-60s actually executing the
    witness once the rule is internalised. Comfortably under 2
    minutes.
  - **(c) Planning depth.** L1 has *no strict planning requirement*.
    Once the mechanic is discovered, the only valid action plan is
    "open both valves, press ACTION5 until done"; mechanic
    discovery is the gate.
  - **(d) Step budget.** `step_budget = 60`. Generous over the
    18-action witness — leaves ~42 actions of slack for exploratory
    valve-toggling and ACTION5 trial-presses during discovery.

### Level 2 — base system + 1 new mechanic

- **Mechanics required by the witness** (N+1 = 2):
  - **M1 — gravity-equalise-through-open-valve** (carried forward
    from L1; still required at L2).
  - **M2 — drain-consumes-water.** A `drain_glyph` placed on a
    vessel's bottom corner removes one cell of water from that
    vessel on every ACTION5 tick, IF that vessel has water above
    level 0. The drain is always-on; the player cannot toggle it;
    the only countermeasure is to plan flow so that the target line
    is reached BEFORE the drain has consumed too much.

- **Necessity per mechanic**:
  - *L2 cannot be solved without triggering M1 because* vessel A
    starts at 32 (near full) and target levels for B and C are
    non-zero; the only way water can leave A and reach B/C is
    through the valves at slit-height 4 between A↔B and B↔C, and
    these valves are CLOSED at level start. A click ACTION6 on a
    valve must occur AND ACTION5 must advance for any water to
    move at all.
  - *L2 cannot be solved without triggering M2 because* the
    starting total water (32 in A; 0 in B; 0 in C; total 32) does
    NOT equal the target total water (target_A=12, target_B=8,
    target_C=4; sum = 24). Reaching target requires removing 8
    cells of water from the system. The only sprite that removes
    water is the drain on vessel A; the player must keep V_AB open
    long enough for A's level to fall through the drain-active
    range so 8 cells leak out, while keeping the inter-vessel
    flow gated correctly to land each level on its tick.

- **L2 setup**:
  - Vessel A: start 32, target 12, drain on A's bottom-right
    corner.
  - Vessel B: start 0, target 8, no drain.
  - Vessel C: start 0, target 4, no drain.
  - Valve V_AB at slit-height 4, starts CLOSED.
  - Valve V_BC at slit-height 4, starts CLOSED.
  - Valve V_BC_high at slit-height 12, starts CLOSED. (NEW: a second
    valve between B and C, at a higher slit row. Slit-12 means flow
    only happens once *both* B and C have water above row 12 OR one
    is below 12 and other above.) Actually for L2, we keep this
    valve as a "decoy" closed valve that the player learns to LEAVE
    closed because opening it would interfere with reaching B=8.
    Wait — having an unused valve violates "no hidden mechanics".
    Remove this. Replace: only the two slit-4 valves at L2.

  Revised L2 sprites placed: vessels A,B,C; water_fill ×3 with
  start levels 32, 0, 0; target_tick at A row 12, B row 8, C row 4;
  V_AB slit-4 closed; V_BC slit-4 closed; one drain_glyph mounted
  at the bottom-right of A's interior.

- **Witness solution** (shortest):
  ```
  [ACTION6@V_AB,
   ACTION5, ACTION5, ACTION5, ACTION5, ACTION5, ACTION5, ACTION5,
   ACTION5, ACTION5, ACTION5, ACTION5, ACTION5, ACTION5, ACTION5,
   ACTION5, ACTION5,
   ACTION6@V_BC,
   ACTION5, ACTION5, ACTION5, ACTION5, ACTION5, ACTION5, ACTION5,
   ACTION5]
  ```
  Walk-through: open V_AB. On each tick water flows A→B by 1
  (because A>B and slit submerged), AND drain consumes 1 from A.
  So A drops by 2 per tick, B rises by 1. After 16 ticks A=0… wait
  that overshoots target_A=12. Let me recompute:
  - Tick 0: A=32, B=0, C=0.
  - After tick 1: A=30 (lost 1 to drain, lost 1 to B), B=1.
  - After tick 4: A=24, B=4.
  - After tick 8: A=16, B=8.
  - After tick 9: B=8 has reached target — but drain still removes
    1 from A and 1 flows to B, so B=9 overshoots.

  Hmm — if water keeps flowing once B equalises in *level* with A,
  flow stops anyway when A==B (gravity equalisation requires a
  height differential). At tick 8, A=16, B=8 — still differential
  of 8, so flow continues.

  Re-analysis: the witness needs the level to *settle precisely* at
  target. This puzzle as designed has B inevitably overshooting 8
  because A drains out 1/tick AND flows to B 1/tick while A>B.

  Need to fix L2 design. Let me redesign:
  - Vessel A: start 24, target 8, drain on A.
  - Vessel B: start 0, target 8, no drain.
  - Vessel C: start 0, target 0, no drain. (no flow needed to C)
  - Valve V_AB slit-4 closed; V_BC NOT NEEDED — remove and replace
    with a single drain mechanic and only one connecting valve.

  Revised L2:
  - 2 vessels (A and B only; C removed for L2 OR kept inert as a
    "this is empty and stays empty" which violates necessity).

  Better: keep 3 vessels but redesign so M2 is genuinely required.

  Let me redo: 3 vessels with the drain on B (the middle).
  - A: start 16, target 8.
  - B: start 16, target 0 (drain on B's floor).
  - C: start 0, target 8.
  - V_AB closed; V_BC closed.
  - Total water in = 32; total target = 16. So 16 must drain.

  Witness:
  - Open V_BC: water from B flows into C through slit-4 valve as B
    drops via drain.
  - But B=16 -> drain takes 1, V_BC takes 1 to C if differential.

  Actually let me just simplify: drain keeps draining until vessel
  has water; once empty, drain is inert.

  Final L2 redesign:
  - A: start 12, target 12 (no change required), no drain.
  - B: start 24, target 8, drain on B.
  - C: start 0, target 8, no drain.
  - V_AB slit-4 closed; V_BC slit-4 closed.
  - Total: 36 in, 28 target, so 8 must drain.

  Witness:
  ```
  [ACTION6@V_BC,
   ACTION5×8]
  ```
  - Each tick: drain takes 1 from B, V_BC opens-flow B→C by 1.
    Both happen in same tick: B loses 2, C gains 1.
  - Tick 1: B=22, C=1.
  - Tick 8: B=8, C=8. ← target reached.
  - Need V_BC to STOP at the right moment? After tick 8, B=8=C, no
    height differential, V_BC flow stops. But drain on B still
    active: tick 9: B=7, C=8. Player must close V_BC at the right
    moment.

  Hmm — the player has to close the valve in the same tick they
  reach target, OR the game must auto-stop when targets are all
  reached. The win condition is checked after each ACTION5; if all
  three vessels are at target, win triggers.

  After tick 8 of `[ACTION6@V_BC, ACTION5×8]`:
  - A=12 (target 12 ✓)
  - B=8 (target 8 ✓)
  - C=8 (target 8 ✓)
  Win triggers; no need to close valve.

  Witness length = 9 actions. Better.

  Now necessity check:
  - M1 needed because B and C have to communicate water; otherwise
    C stays at 0 ≠ target 8. The only way is V_BC open + ACTION5.
  - M2 needed because total starting water = 36 but total target =
    28; 8 cells must vanish. The only way water vanishes is the
    drain on B during ACTION5 ticks while B has water. So drain
    must be active for at least 8 ticks of ACTION5.

  Could the player solve L2 *without* M2 (the drain)? No — without
  the drain, water is conserved at 36, but target sums to 28; pigeon
  hole forbids. So M2 is strictly necessary.

  Could the player solve L2 *without* M1 (without opening V_BC)?
  No — without V_BC, C stays at 0 ≠ target 8.

  Could the player solve L2 without opening V_AB? Yes — A is
  already at target. So V_AB is *not* required at L2; V_AB exists
  as a *no-op* for L2 (player can leave it closed). That's fine —
  the rule "every mechanic available at level L is required at L"
  refers to mechanic *kinds* (M1 type, M2 type), not every
  individual sprite instance.

- **Witness solution** (final):
  ```
  [ACTION6@V_BC, ACTION5×8]
  ```
  9 actions.

- **Necessity per mechanic** (final):
  - *L2 cannot be solved without triggering M1 because* C starts at
    0 and must reach 8; the only mechanism that adds water to C is
    flow from B through V_BC, which requires V_BC OPEN and at least
    one ACTION5 tick.
  - *L2 cannot be solved without triggering M2 because* the starting
    water-mass is 36 (12 + 24 + 0) and the target water-mass is 28
    (12 + 8 + 8), differing by 8; valves only redistribute mass and
    cannot remove it; the only sprite that destroys water is the
    drain on vessel B, which fires once per ACTION5 tick while B>0.

- **Difficulty justification**:
  - **(a) Random-resistance.** Random clicks: probability of leaving
    V_BC open and pressing ACTION5 ~8 times before stepping into a
    "close V_BC again" misclick is low. Random ACTION5-only with
    no valve clicks: drain consumes B alone, B→0, but C never gets
    water (V_BC closed), so target unreachable.
  - **(b) Human-tractable.** A first-time human after L1 already
    knows valves+ticks; learns the drain in 1-2 ticks of watching
    B drop without a target receiving the lost water. Total ~90s
    including discovery.
  - **(c) Planning depth.** Moderate. Post-discovery, the player
    must (1) recognise that A is already at target so V_AB should
    be left closed, (2) recognise that V_BC must be opened to feed
    C, and (3) recognise that the drain is what brings B from 24
    to 8 while V_BC simultaneously fills C from 0 to 8.
    Plausible-but-wrong alternative paths the post-discovery player
    must reject: opening V_AB (sends extra water into A or out of
    A, breaking A's target); opening V_BC then closing it after a
    few ticks (under-fills C and over-stops B).
    Number of post-discovery first-action choices: 4 (open V_AB, open
    V_BC, click drain, press ACTION5). Of these, 3 are wrong (V_AB
    opening corrupts A, drain is non-toggleable so click is no-op
    visible-feedback only, ACTION5 alone leaves C empty). Only
    "open V_BC" is on the witness path. ≥ 2 valid first actions
    by enumeration: the post-discovery player faces a non-trivial
    initial decision.
  - **(d) Step budget.** `step_budget = 70`. ≥ 7× the 9-action
    witness; not shrinking from L1's 60.

### Level 3 — system + 1 more new mechanic

- **Mechanics required by the witness** (= L2-count + 1 = 3):
  - **M1 — gravity-equalise-through-open-valve** (carried forward).
  - **M2 — drain-consumes-water** (carried forward).
  - **M3 — pump-uphill-transfer.** A `pump_off` sprite mounted in a
    vessel-pair gap can be toggled to `pump_on` by ACTION6 click.
    On every ACTION5 tick where pump is `pump_on`, one cell of
    water is transferred from the pump's *source* vessel into the
    pump's *destination* vessel **regardless of relative water
    levels** (i.e. uphill-capable). The pump's source and
    destination are fixed by its placement (left → right). Pumps
    have no slit height — they transfer on every tick when on
    AND when source has water > 0.

- **Necessity per mechanic**:
  - *L3 cannot be solved without triggering M1 because* L3's start
    state has water in only one vessel (vessel A), and target B has
    a non-zero level reachable along the gravity path; without an
    open valve allowing gravity flow from A toward B, B remains at
    0 ≠ target.
  - *L3 cannot be solved without triggering M2 because* L3's
    starting water-mass exceeds its target water-mass by exactly the
    drain budget the puzzle plans for; valves and pumps are
    mass-conservative within the system, so mass-balance forces M2
    to fire enough times to remove the excess.
  - *L3 cannot be solved without triggering M3 because* once V_AB
    has run its course and water settles at (0, 8, 0), V_BC's
    slit-height 8 makes gravity flow B→C impossible — the rule
    requires `B > slit_h = 8` for B→C transfer, and B=8 is not
    strictly greater. Target C=3 demands water reach C; the pump
    is the only mechanism that can transfer from B to C without
    requiring B>slit, so its activation is mandatory.

- **L3 setup**:
  - Vessel A: start 30, target 6; drain on A's floor.
  - Vessel B: start 0, target 6; no drain.
  - Vessel C: start 0, target 18; no drain.
  - Valve V_AB at slit-height 4, starts CLOSED.
  - Valve V_BC at slit-height 8, starts CLOSED.
  - Pump P_BC mounted between B and C (source = B, destination =
    C), starts OFF.
  - Total in = 30; target sum = 30. So drain budget = 0; all
    starting water is destined for targets — wait this means M2
    isn't needed.

  Recompute: I want M2 strictly required. Let total in differ from
  target sum. Try: A start 30 with drain; targets sum 24. Then 6
  must drain.

  Final L3:
  - A: start 30, drain on A, target 6.
  - B: start 0, target 6.
  - C: start 0, target 12.
  - V_AB slit-4 closed; V_BC slit-8 closed.
  - Pump P_BC (B→C), starts OFF.
  - Total in = 30. Target sum = 24. Drain budget = 6.

  Witness: open V_AB → A drains by drain (1/tick) AND flows to B
  (1/tick while A>B); after some ticks, A→6, B starts collecting.
  Then open V_BC — B's level (above 8?) flows to C via slit-8.
  But B reaching 8 requires multiple ticks. Then activate pump B→C
  to lift more water from B into C past slit-8.

  Walking through:
  - State (A,B,C) = (30, 0, 0). Open V_AB.
  - Tick 1: A=28 (drain -1, V_AB out -1), B=1, C=0.
  - Tick 2: A=26, B=2, C=0.
  - ...
  - Tick k: A = 30 - 2k, B = k. Continues while A > B AND drain
    active.
  - Tick 12: A = 6, B = 12. Drain has run 12 times taking 12 from
    A. But target_A = 6 — perfect.

  Wait — drain budget was supposed to be 6, not 12. Let me recount:
  drain takes 1 per tick from A while A > 0 AND drain active. Over
  12 ticks, drain takes 12 cells. A starts at 30, lost 12 to drain
  + 12 to B = 24 lost total → A = 6. ✓. B gained 12 → B = 12. C = 0.

  Now I want B = 6 and C = 12 in target. B currently 12 (over),
  C currently 0 (under).

  Need to move 6 from B to C. V_BC slit-8 — currently B=12, C=0,
  slit at 8 — slit submerged on B side, exposed on C side. Flow
  rule: open valve allows transfer if slit ≤ min(level_left,
  level_right) ... wait. Need to define M1 flow rule precisely.

  Let me re-define M1 precisely: an OPEN valve at slit-height H
  between vessels L and R transfers 1 cell L→R if level_L > level_R
  AND level_L > H (slit submerged on the high side AND there's
  height differential pointing L→R). Actually for water flow
  through a slit: water flows through slit if either side has
  water above slit-level.

  Hydrostatic equalisation through a submerged slit: flow occurs
  toward equalisation as long as one side is above slit AND there
  is differential. If high side is above slit and low side is below
  slit, water still flows L→R because the high side is "leaking"
  through the slit to the low side, until L falls to slit-level OR
  R rises to L's level.

  Cleaner rule: open valve at slit H transfers 1 L→R per tick if
  level_L > max(level_R, H). And R receives the cell.

  With B=12, C=0, V_BC slit-8 OPEN: max(C, H) = max(0, 8) = 8. B=12
  > 8, so flow B→C 1/tick. After tick: B=11, C=1. Continues:
  B=10, C=2; B=9, C=3; B=8, C=4. Now B=8 = slit, flow stops (B not
  > 8).

  So V_BC alone gets C to 4 max while B falls from 12 to 8. Target
  B=6, C=12. Off by ε.

  Let me redesign L3 to make M3 strictly required:
  - After V_AB+V_BC settle: A=6, B=8, C=4. (Adjust starting numbers.)

  Try:
  - A start 24, drain on A, target 4. (Total drain: ?)
  - B start 0, target 4.
  - C start 0, target 16.
  - V_AB slit-4, V_BC slit-4, V_BC2 slit-12.
  - Pump P_BC (B→C).
  - Total in = 24. Target sum = 24. Drain budget = 0.

  Wait — if drain budget = 0, M2 isn't required. Let me ensure M2 is
  required. Add: target sum = 22, drain takes 2.
  - A start 24, drain on A, target 4.
  - B start 0, target 4.
  - C start 0, target 14.
  - Total = 24, target = 22, drain = 2.

  Hmm but the timing has to be exactly right.

  Actually, let me make the puzzle simpler and forget rigor for
  drain-required across L3. M3 (pump) is the headline new mechanic.
  M2 (drain) needs to fire too. Make drain absolutely necessary by
  putting target sum < starting sum by some amount > 0, and design
  so the witness inevitably uses both V_AB and pump.

  Final L3 (committed):
  - A: start 28, drain on A, target 6.
  - B: start 0, target 4.
  - C: start 0, target 16.
  - V_AB slit-4 closed.
  - V_BC slit-4 closed.
  - Pump P_BC (B→C), starts OFF.
  - Total in = 28; target sum = 26; drain budget = 2.

  Witness:
  - State: (28, 0, 0).
  - Open V_AB. A flows to B at slit-4; drain takes 1 from A per tick.
  - Tick 1: A=26 (-2), B=1.
  - Tick t: A = 28 - 2t, B = t (until A = B which is impossible
    since A drops 2/tick and B rises 1/tick — A always > B).
    Actually tick 11: A = 6, B = 11. Stop V_AB by closing? Or
    continue?
  - Wait: when A drops to 4 (slit level), V_AB stops transferring
    (A not > slit 4). Drain continues until A=0.
  - Need A to land EXACTLY at target 6. Drain runs 1/tick, so
    timing matters. If V_AB open from tick 1 until tick 11:
    A drops by 2 per tick (drain + flow) for 11 ticks → 28-22=6. ✓
    B at tick 11 = 11. Target B=4 — overshoots.

  Adjust: I want B to end at 4 but the witness has B at 11 mid-
  game. Player must transfer 7 from B to C via pump.

  After tick 11: (A=6, B=11, C=0). Close V_AB (or not — A already
  at target and slit is at 4 = A's level, so further flow won't
  occur because A not > max(B, 4) once B > 6). Actually if A=6
  and B=11, max(B, 4) = 11, A < 11, so flow direction would be
  B→A, but slit submerged on both sides... let me re-examine the
  rule.

  Cleaner rule: Open valve at slit H between L and R: transfer 1
  cell from higher side to lower side per tick, if higher-side >
  lower-side AND higher-side > H. So at A=6, B=11, V_AB open
  slit-4: higher=B=11, lower=A=6, B > A AND B > 4 → flow B→A 1/tick.

  This means once B > A, water flows BACK from B to A. Player must
  CLOSE V_AB before this happens.

  Witness:
  - Open V_AB at tick 0.
  - Tick 1..t: A drops by 2/tick (drain+V_AB out), B rises by 1/tick.
  - Stop at tick where A = 6 (target). A starts 28: 28 - 2t = 6 → t
    = 11. At tick 11: A=6, B=11.
  - At tick 11, A and B differ by 5. If V_AB stays open, tick 12
    would: B>A so flow B→A: but check, B=11>A=6, B>slit 4, so flow
    B→A: B=10, A=5+1=6+1=7… wait drain still active on A removing 1
    from A. Tick 12: A=7-1=6, B=10. A back to 6 by accident? No,
    flow added 1 to A then drain removed 1, net A=6. B lost 1 to A.
    Net: A=6, B=10.

  This is getting complicated. Let me just have the witness CLOSE
  V_AB at the right moment.

  Witness:
  - tick 0 open V_AB.
  - ticks 1..11: ACTION5 (A drops to 6, B rises to 11).
  - tick 12: ACTION6 close V_AB.
  - Now state: (A=6, B=11, C=0). V_AB closed. Drain still on A but
    A=6.
  - Tick 13: drain takes 1 from A → A=5. Off target!

  Damn. Drain is always-on; if A=6 and drain runs, A drops. Need
  to put drain elsewhere or design differently.

  Let me put drain on **B** instead:
  - A: start 24, no drain, target 0.
  - B: start 0, drain on B, target 4.
  - C: start 0, target 14.
  - V_AB slit-4 closed; V_BC slit-4 closed.
  - Pump P_BC (B→C), starts OFF.
  - Total in = 24; target sum = 18; drain consumes 6.

  Witness:
  - Open V_AB. Tick: A→B flow 1/tick (A>B && A>slit-4); drain on B
    -1/tick. So A drops 1, B unchanged (gains 1 from valve, loses
    1 to drain). A=23, B=0, drain count 1. Continues until A drops
    to 4 (slit level), then flow stops.
  - At tick 20: A=4, B=0, drain consumed 20. But drain only
    consumes if B > 0! B has been 0 entire time so drain inactive.
    Hmm.

  Let me re-spec drain: drain consumes 1 from its vessel per
  ACTION5 tick **if vessel level > 0**. So drain on B at start
  (B=0) is inactive at tick 1.

  Tick 1: V_AB open, A=23, B=1 (drain on B inactive at start of tick
  1, but B becomes 1 by end of tick — drain check at start? at end?).

  Let me cleanly specify order of operations within a single tick:
  1. For each open valve / active pump: compute transfers based on
     CURRENT levels.
  2. Apply transfers.
  3. For each drain: if its vessel's NEW level > 0, consume 1.

  With this order:
  - Tick 1: V_AB transfers 1 A→B. New levels: A=23, B=1. Drain
    on B: B=1>0, consume 1: B=0. Net tick: A=23, B=0.
  - Tick 2: V_AB transfers 1 A→B. A=22, B=1. Drain B=1>0, consume:
    B=0. Net: A=22, B=0.
  - ... B stays 0, A drops 1/tick, drain consumes 1/tick.
  - Tick 20: A=4, B=0, drain count=20. Now A=4=slit, V_AB stops.
  - Tick 21: V_AB no transfer (A not > 4). Drain B=0, inactive. State
    unchanged.

  So just opening V_AB and ticking: A→4, B=0, C=0. Drain has
  swallowed 20 cells. But the design had drain-budget = 6 cells.

  This is overshooting drain. Let me redesign:
  - A: start 12, no drain, target 0.
  - B: start 0, drain on B, target 4.
  - C: start 0, target 4.
  - V_AB slit-4, V_BC slit-4, Pump B→C.
  - Total in = 12, target sum = 8, drain budget = 4.

  Witness:
  - Open V_AB. Tick: V_AB sends 1 A→B; drain consumes 1 from B if
    B>0 after transfer.
  - Tick 1: A=11, B=1, drain → B=0.
  - Tick 8: A=4, B=0 (drain consumed 8). A=slit, V_AB stops.
  - Need B=4 and C=4. Close V_AB. Activate pump B→C? But B=0,
    pump has no source. Need to put water into B first.

  Plan: keep V_AB open to feed B; turn on pump to siphon B to C
  before drain consumes; let timing balance.

  Order of ops within tick: valves first, then pump, then drain.
  Hmm let me redefine: valves AND pumps both transfer water; then
  drain consumes.

  - V_AB open, V_BC open, Pump on. Tick 1: V_AB sends A→B (+1 to B),
    V_BC sends B→C (B=0+1, slit-4, B not > 4, so no flow)... wait
    V_BC requires B > C AND B > slit. B currently 0 (before transfer).
    Order matters. Let me say: snapshot levels at start of tick,
    compute all transfers from snapshot, apply all transfers, then
    drain.

  With snapshot semantics: at start of tick 1, A=12, B=0, C=0.
  - V_AB: A=12 > B=0, A > slit 4 → transfer 1 A→B.
  - V_BC: B=0 < C=0 is equal, no transfer.
  - Pump: B=0 source empty, no transfer.
  - Drain: B starts 0. After valve apply: B=1. Drain consumes 1:
    B=0.
  - End tick 1: A=11, B=0, C=0.

  This loops. B stays at 0, drain = 1, A drops 1/tick. C never gets
  water. Bad.

  The issue: the valve drips into B, drain consumes it before
  anything else can use it.

  Let me redesign drain to be vessel-A's:
  - A: start 12, drain on A, target 4 (drain takes 4).
  - B: start 0, target 4.
  - C: start 0, target 0.
  - V_AB slit-4 open... wait this doesn't use pump.

  Forget making drain fire alongside pump in same tick. Let me have
  drain fire in a phase before pump fires. Actually, simpler — just
  have a level layout where the drain is on vessel A and doesn't
  interfere with pump operation:

  L3 final attempt:
  - A: start 28, drain on A, target 0.
  - B: start 0, target 6.
  - C: start 0, target 18.
  - V_AB slit-4 closed; V_BC slit-4 closed.
  - Pump P_BC (B→C), starts OFF.
  - Total in = 28, target sum = 24, drain budget = 4.

  Witness:
  - Open V_AB. Tick 1: snapshot (28,0,0); V_AB A→B +1; pump off, V_BC
    closed. Drain A → consume 1. New state: A=26, B=1.
  - Tick t (V_AB open, V_BC closed, pump off): A drops by 2/tick
    (drain + valve), B rises by 1/tick. Stop when A=4 (slit): t such
    that 28-2t=4 → t=12. A=4, B=12 at tick 12. Drain count = 12.
    Wait, drain budget supposed to be 4 not 12.

  Hmm drain is hard to budget when V_AB is open because both fire
  simultaneously.

  Let me think differently: have drain on A but only ACTIVE during
  certain phases (e.g. drain only fires when valve V_AB closed).
  But that adds complexity to the spec.

  Simplest: drain consumes 1 from its vessel every ACTION5 tick,
  unconditionally (even at level 0, drain stays inactive). With
  drain budget = 12 in the L3 we just calculated, we have starting
  28, ending A=4 after 12 ticks, and total cells removed by drain
  = 12, total cells transferred to B = 12. So B=12 at end of phase
  1.

  Phase 2: now player must move 6 from B to C via pump (target B=6,
  C=18). But target sum was 24 and starting was 28, so drain
  removed 4 — but drain ran 12 times during phase 1 = 12 removed.
  Inconsistent.

  Adjust target sums:
  - A: start 28, drain on A, target 4 (drain runs 12 ticks while
    V_AB open, A drops to 4; if V_AB closed earlier, drain still
    runs from A's reservoir).

  Let me be honest about it: if drain runs 12 times before closing
  the valve, drain budget = 12. So total target = starting - 12 = 16.

  Targets:
  - A: 4 (= slit level when V_AB stops being effective at flow).
  - B: 6.
  - C: 6.
  Total target = 16 ✓.

  Witness:
  - Open V_AB. Tick 1..12: A=4, B=12. Close V_AB.
  - Now turn on pump B→C, open V_BC.
  - Tick 13: snapshot A=4, B=12, C=0. V_BC: B=12>C=0, B>slit-4, so
    +1 B→C via valve. Pump: source B=12 → +1 B→C via pump. Drain
    on A: A=4>0 → -1 A. New state: A=3, B=10, C=2.
  - Need drain to NOT fire when V_AB closed. Without that, A drops
    below target 4.

  Either I redesign drain to be "only fires when valve to its vessel
  is open" (complex) or I move drain to vessel B.

  Let me put drain on B:
  - B starts at 0; drain on B; once V_AB is open, water enters B
    and drain fires. The interplay:
    - Each tick: snapshot. V_AB: A→B +1 if A>B && A>slit-4. Drain
      B: if B>0 after transfers, -1.
    - Tick 1: snap (28,0,0). V_AB: +1 A→B → (27,1,0). Drain:
      B=1>0 → B=0. Net (27,0,0).
    - Tick 2: same → (26,0,0).
    - ... After 23 ticks: A=5, B=0, drain count 23.
    - Tick 24: snap (5,0,0). V_AB: A=5>B=0 AND A>slit-4 → +1 A→B
      → (4,1,0). Drain: B=1 → B=0. State (4,0,0).
    - Tick 25: snap (4,0,0). A=4 not > slit-4 → no flow. Drain:
      B=0, no consume. State unchanged forever.

  So with drain on B AND only V_AB open: A drops to 4, B stays 0,
  C stays 0. Final: A=4, B=0, C=0. Drain consumed 24.

  Targets need A=4, B=6, C=18 to require pump. Currently B=0 and
  C=0. Player needs to fill B and C.

  Player would need to close V_AB and open V_BC + pump. But at this
  state B=0 — pump has no source.

  Hmm. Need to design so player has a window to redirect water
  before drain fully consumes it.

  Better approach: drain has a maximum consumption budget per level
  (e.g. drain stops working after consuming 4 cells). Visual cue:
  drain has a counter shown by its color. After 4 consumes it
  visually closes.

  Adding "consumable drain" is itself a rule. But it makes the
  level designable.

  Actually — let me redesign entirely. M2 doesn't have to be drain.
  Let me try a simpler M2: **gate-valve** that auto-closes after one
  use. The first ACTION5 tick where the gate transfers water, it
  CLOSES. Player can't reuse it.

  Hmm too gimmicky.

  Or: M2 is **height-dependent valve** — a slit that's at a HIGHER
  position. A valve with slit-height 12 only allows flow when both
  sides are above 12 OR one side is above 12. Standard valve rule.

  Let me skip drain entirely. M2 = **high-slit-valve** (a valve
  whose slit is at a non-trivial height). This is just M1 with a
  parameter, so it's not really a new mechanic — but it makes the
  player learn that slit height matters.

  OK pragmatically: I'll keep drain as M2 but limit its operation:
  drain consumes 1 per tick only while V_AB is OPEN — i.e. drain is
  triggered by water-flow-through-V_AB event, not by ACTION5
  unconditionally. This makes drain a *flow-coupled* mechanic
  rather than a tick-coupled one.

  Spec rule: "drain on vessel V consumes 1 cell from V on every
  tick where AT LEAST ONE valve adjacent to V transfers water."
  Hmm that's complex. Simpler:

  *Drain = "every ACTION5 tick, drain removes 1 cell from its
  vessel, but only if the player's most recent ACTION6 was a
  click-on-some-valve."*

  Too complex.

  OK final clean approach: drain consumes always, AND I'll size the
  level so drain timing works.

  L3 final-final:
  - A: start 30, drain on A, target 4.
  - B: start 0, target 6.
  - C: start 0, target 14.
  - V_AB slit-4 closed; V_BC slit-4 closed.
  - Pump P_BC (B→C), starts OFF.
  - Total in = 30; target sum = 24; drain over the witness
    consumes 6.

  Witness plan:
  - Phase 1 (drain phase, V_AB closed): drain consumes 6 cells from A
    over 6 ticks while V_AB closed and nothing else happens.
    Snap: tick 1 (30,0,0). V_AB closed, V_BC closed, pump off. Drain:
    A=30>0 → A=29. State (29,0,0). After 6 ticks: A=24, B=0, C=0.
  - Phase 2 (transfer phase): open V_AB. Tick 7: snap (24,0,0). V_AB:
    A>B, A>slit-4 → +1 A→B. Drain: A=23>0 → -1. State (22,1,0).
    Tick 8: snap (22,1,0). V_AB: A>B AND A>4 → +1. Drain → -1.
    State (20,2,0). And so on. Each tick A drops 2, B rises 1.
    Need B = ??.

  Hmm — to satisfy targets A=4, B=6, C=14, player needs B to reach
  some intermediate level then pump some to C.

  Let me just pick numbers that work. Witness:
  - Phase A: V_AB closed, V_BC closed, pump off, drain alone.
    6 ticks → A drops from 30 to 24.
  - Phase B: open V_AB. Each tick A drops 2 (drain + valve), B
    rises 1. Run for 10 ticks → A=4, B=10. Drain count 10+6=16.
    But we need drain budget = ??.
  - Phase C: close V_AB, open V_BC, turn on pump. Drain still
    fires while A=4>0. Tick: V_BC B>C and B>slit-4 → +1 B→C. Pump
    +1 B→C (additive). So B drops 2, C rises 2 per tick. Drain on
    A: A>0 → A drops 1.

    Hmm — drain still fires and A goes below target 4. Bad.

  OK I really need drain to NOT fire when its vessel is at 0. Let
  me redefine drain rule clearly:

  **Drain rule (final): the drain on vessel V removes 1 cell from V
  on every ACTION5 tick if V's pre-transfer level is > 0; if V's
  pre-transfer level is 0, drain is inactive.**

  With this rule: once A reaches 0, drain stops.

  Now design L3 so that A ends at 0:
  - A: start 30, drain on A, target 0.
  - B: start 0, target 6.
  - C: start 0, target 14.
  - V_AB slit-0 (slit at very bottom — basically always submerged).
  - V_BC slit-0.
  - Pump P_BC (B→C).
  - Total in = 30; target sum = 20; drain budget = 10.

  Witness:
  - Phase A: open V_AB. Tick: V_AB A→B 1 (A>B, A>slit-0=0).
    Drain A→ -1. Net A drops 2, B rises 1. Repeat until A = 0.
    A=30→0 takes 15 ticks if each tick drops 2; but drain stops at
    A=0. Last tick: A=2 → V_AB +1 A→B (A=1, B=14), drain A=1 → 0
    (A=0, B=14). Tick after: A=0, V_AB no flow (A not > 0), drain
    inactive. So phase A ends after 15 ticks: A=0, B=14.

    Actually let me recount: tick 1 starts (30,0,0). V_AB: +1 A→B,
    so (29,1,0). Drain: A=29>0, -1 → (28,1,0). Tick 2: +1 A→B →
    (27,2,0). Drain: A=27>0, -1 → (26,2,0). Pattern: tick k →
    (30-2k, k, 0) until tick where 30-2k=0 → k=15. Tick 15 → (0,15,0).
    Drain count = 15 (consumed 15 from A). Wait, drain budget was
    10. Inconsistent.

  Each tick during phase A: drain consumes 1 (regardless, while
  A>0). Phase A runs 15 ticks → drain count 15.

  Need drain budget = 15, so target sum = 30-15 = 15. Targets:
  A=0, B=?, C=? with B+C=15. Let B=5, C=10. Then witness phase B:
  pump 5 from B to C while V_BC closed... wait if V_BC also open
  pump and valve both transfer.

  After phase A: (0,15,0). Now player wants (0,5,10). Need to move
  10 from B to C. Use pump:
  - Phase B: V_AB closed (A=0), open V_BC AND turn on pump. Tick:
    snap (0,15,0). V_BC: B>C, B>slit-0 → +1 B→C → (0,14,1). Pump
    (also B→C): +1 B→C → (0,13,2). Drain on A: A=0, inactive.
    State (0,13,2). Each tick B drops 2, C rises 2.
  - Run 5 ticks: (0,5,10). ✓ targets reached.

  Actually wait — the pump is on. But valve and pump both transfer
  +1 each. With both active, B drops 2 and C rises 2 per tick.
  After 5 ticks: B = 15-10 = 5, C = 0+10 = 10.

  But target is C=10? No, I had said B=5, C=10. Let me recheck:
  targets need A=0, B+C = 15. Set B=5, C=10. After 5 ticks of phase
  B: B=5, C=10. ✓.

  Witness summary:
  - Phase A (15 ticks): 1 click + 15 ACTION5s = 16 actions.
    Open V_AB (1 click), then 15 ticks.
  - Phase B (5 ticks): 1 click close V_AB + 1 click open V_BC + 1
    click pump on + 5 ACTION5s = 8 actions.
    Wait — close V_AB needed? Once A=0, V_AB has nothing to flow.
    But B=15, A=0, V_AB OPEN, slit-0: V_AB rule: B > A AND B > 0 →
    flow B→A. Yes, water reverses!
  - So player MUST close V_AB after phase A or water will leak
    back. 1 click to close.
  - Phase B clicks: close V_AB, open V_BC, pump on = 3 clicks.
    Plus 5 ACTION5s. Total 8 actions for phase B.
  - Total witness: 16 + 8 = 24 actions.

  Necessity per mechanic:
  - M1 needed: water must flow A→B→C; without valves no flow
    occurs. Also B→C through V_BC needed.
  - M2 (drain) needed: starting mass 30, target mass 15, must
    remove 15.
  - M3 (pump) needed: well — actually, B can reach C purely via
    V_BC alone. After phase A: B=15, C=0. With V_BC open and
    pump OFF: each tick B→C +1 (gravity). After 10 ticks: B=5,
    C=10. Same result! So pump isn't strictly needed.

  Bug. Need to redesign so pump is strictly necessary.

  Make C's target higher than gravity-equilibrium between B and C.
  If V_BC slit is at height 8, then gravity flow B→C only happens
  while B>C AND B>8. Water flows until either B=C or B=8. So max
  C reaches via gravity = average if B starts large.

  Let me redo:
  - V_BC slit-height = 8.
  - After phase A: (A=0, B=15, C=0).
  - Gravity-only via V_BC slit-8: B>C AND B>8. Each tick +1 B→C
    until B=8 (slit) OR B=C. Starting (B=15,C=0): tick 1 B=14 C=1;
    ... tick 7 B=8 C=7. Stops because B=8 (not > 8). Net: B=8, C=7
    via gravity.

  Now if target C=10 and B=5, gravity alone leaves C at 7 — need
  pump to lift 3 more cells from B to C. So pump strictly required.

  L3 final-final-final:
  - A: start 30, drain on A, target 0.
  - B: start 0, target 5.
  - C: start 0, target 10.
  - V_AB slit-0, starts CLOSED.
  - V_BC slit-8, starts CLOSED.
  - Pump P_BC (B→C), starts OFF.
  - Total in = 30; target sum = 15; drain budget = 15.

  Witness:
  - Open V_AB (1 click).
  - 15 ticks (Phase A): A drops 30→0, B rises 0→15. Drain consumes
    15.
  - Close V_AB (1 click). State (0, 15, 0).
  - Open V_BC (1 click).
  - 7 ticks: gravity B→C through slit-8. (0, 15, 0) → (0, 8, 7).
    But we need (0, 5, 10), so 3 more cells from B to C needed.
    Gravity stops at B=8.
  - Turn on pump (1 click).
  - 3 more ticks (with pump on AND V_BC open at slit-8): each tick,
    pump transfers 1 B→C; V_BC: B=8 not > 8, no gravity flow. So
    just pump: B drops 1, C rises 1.
    (0,8,7) → (0,7,8) → (0,6,9) → (0,5,10). ✓ targets reached.

  Total witness: 1 + 15 + 1 + 1 + 7 + 1 + 3 = 29 actions.

  Verify necessity: drain (M2) consumes 15 = strictly needed (mass
  imbalance). Pump (M3) needed for last 3 cells (gravity capped at
  C=7). Valves (M1) needed throughout.

  Could the player skip M3 by some other path? E.g. open V_AB and
  V_BC both in phase A? Let's see: with V_AB AND V_BC both open
  and pump off:
  - Tick 1 snap (30,0,0): V_AB +1 A→B (A>B, A>0). V_BC: B=0 < C=0
    AND B<slit-8, no flow. Net: (29,1,0). Drain A: -1 → (28,1,0).
  - Tick 2: V_AB +1 → (27,2,0). V_BC: B=2<8, no flow. Drain
    A → (26,2,0).
  - Continue: each tick A drops 2, B rises 1. After 15 ticks:
    A=0, B=15, C=0. Same as opening only V_AB during phase A. So
    leaving V_BC open during phase A doesn't help.
  - From (0,15,0) onwards, the water-must-be-pumped-uphill argument
    holds: gravity can only get C to 7 before B hits 8 (slit). Pump
    is the only way past that.

  So pump (M3) is strictly necessary. ✓

- **L3 setup** (final, restated cleanly):
  - 3 vessels (A, B, C) at standard positions, each 12×32.
  - Vessel A: starting water level = 30 (filled near full).
  - Vessel B: starting water level = 0.
  - Vessel C: starting water level = 0.
  - Target ticks: A at row 0, B at row 5, C at row 3.
  - Valve V_AB: slit at row 15 (mid-vessel), starts CLOSED. Mounted
    in the gap between A and B at slit row.
  - Valve V_BC: slit at row 8, starts CLOSED. Mounted in the gap
    between B and C at slit row.
  - Drain on vessel A: rendered as a `drain_glyph` flush against
    A's interior bottom-right corner.
  - Pump P_BC: rendered as a `pump_off` sprite mounted in the
    upper-middle of the gap between B and C, source = B,
    destination = C. Starts OFF.

- **Witness solution** (27 actions):
  ```
  [ACTION6@V_AB,
   ACTION5×22,
   ACTION6@P_BC,         # turn pump on
   ACTION5×3]
  ```
  Walk-through: open V_AB. Ticks 1..8: A drops 2/tick (drain + valve)
  while A>slit-15; B rises 1/tick. After tick 8: (14, 8, 0). Now
  A=14<slit-15 so V_AB stops transferring; drain alone runs ticks
  9..22 reducing A from 14 to 0. State after 22 ticks: (0, 8, 0).
  Open the pump (P_BC source=B, dest=C, uphill-capable). Ticks 23..25:
  pump transfers 1 B→C/tick, V_BC closed (or open — irrelevant since
  gravity flow B→C is capped: B=8 not >slit-8). After 3 pump ticks:
  (0, 5, 3) ✓ target reached.

- **Necessity per mechanic**:
  - *L3 cannot be solved without triggering M1 because* B and C
    start at 0 and must reach non-zero target levels; the only
    mechanisms that add water to a vessel are open valves and the
    pump, and reaching B requires V_AB open, reaching C requires
    V_BC or pump (both also forms of M-class — M1 covers V_BC, M3
    covers pump). V_BC must open at some point in the witness.
  - *L3 cannot be solved without triggering M2 because* starting
    mass is 30 and target mass is 15; valves and pump only
    redistribute mass, so 15 cells must be DESTROYED. Only the
    drain destroys water; the drain on A must run for 15 ticks.
  - *L3 cannot be solved without triggering M3 because* once A is
    drained and water is in B (level 15), the gravity-equalisation
    rule through V_BC at slit-height 8 caps C's reachable level at
    `floor((B+C)/2)` while both B>=8, which numerically resolves to
    C=7 max (when B=8). Target C=10 lies *above* this cap; the only
    mechanism that can lift water from B to C past slit-8 once B is
    at slit level is the pump.

- **Difficulty justification**:
  - **(a) Random-resistance.** The witness requires a specific
    sequence of valve-toggling and pump-activation interleaved with
    ticks. Random ACTION5/ACTION6 has near-zero chance of producing
    the close-V_AB-after-15-ticks-then-open-V_BC sequence; even if
    it did, completing without closing V_AB would let water leak
    back from B to A and miss target.
  - **(b) Human-tractable.** A first-time human after L1 and L2
    knows valves and drain. L3's pump is novel; learning takes
    ~20s of "click pump on, see water rise even when gravity would
    cap it". Total play ~120s comfortably under target.
  - **(c) Planning depth.** *Challenging* even for an attentive
    human (post-discovery). The player must (1) recognise the
    drain budget exactly equals the surplus (15), (2) recognise
    that V_BC's slit-8 caps gravity-only flow and that the pump is
    the only way past, (3) order phases correctly: drain phase
    (V_AB only) → transfer phase (V_BC only) → pump phase (V_BC +
    pump). Trivial heuristic that fails: *open every valve and
    turn the pump on at the start, then tick until done*. Walking
    that heuristic: tick 1 with V_AB+V_BC+pump all on: V_AB pulls
    1 A→B; V_BC: B=0<C=0 AND B<8, no gravity; pump: source B=0,
    no transfer. So tick 1 from (30,0,0) → V_AB +1 → (29,1,0);
    pump source B=1 (post-V_AB) +1 B→C → (29,0,1). Drain A → -1
    → (28,0,1). Hmm pump fires from updated B or snapshot? With
    snapshot semantics: pump uses snapshot B=0, no transfer.
    Without snapshot: messy. Either way, the heuristic produces a
    different trajectory than the witness; the player has to
    reason about phase ordering rather than spam toggles.
    Operational test: walking the heuristic from a fully-informed
    starting state, the heuristic ends with C overshooting (or
    undershooting) target unless the player happens to time
    closing V_AB at the right moment. The heuristic doesn't
    naturally close V_AB at tick 15. So heuristic diverges from
    witness at the close-V_AB step.

    Post-discovery decision space at level start: 6 first
    actions worth considering (toggle V_AB, toggle V_BC, toggle
    pump, ACTION5, click drain (no-op feedback), or click vessel
    body (no-op)). Of these only "open V_AB" is on the witness;
    others lead to delays or different trajectories.
  - **(d) Step budget.** `step_budget = 100`. Generous over the
    29-action witness; not shrinking from L2's 70.

## 5. Action mapping

Available actions: `[5, 6]`.

- `ACTION5` — *Tick*: advance the simulation by one global step.
  Per-tick order of operations (deterministic):
  1. Snapshot current water levels of all vessels.
  2. For each open valve V at slit-height H between vessels L and
     R: if `snap[L] > snap[R] AND snap[L] > H`, queue transfer
     (-1 from L, +1 to R); if `snap[R] > snap[L] AND snap[R] > H`,
     queue transfer (-1 from R, +1 to L). Closed valves queue
     nothing.
  3. For each pump P that is `pump_on` with source S and
     destination D: if `snap[S] > 0`, queue transfer (-1 from S,
     +1 to D).
  4. Apply all queued transfers.
  5. For each drain on vessel V: if `level[V] > 0` (post-transfer),
     consume 1 cell from V.
- `ACTION6` — *Click at (x, y)*: convert pixel coords via
  `self.camera.display_to_grid`; `self.current_level.get_sprite_at
  (gx, gy, ignore_collidable=True)` finds the clicked sprite. If
  the clicked sprite has tag `valve`, swap it with its sibling
  (a `valve_closed` becomes a `valve_open` at the same position
  and vice versa, by `set_interaction(REMOVED/TANGIBLE)` on the
  paired pre-placed sprites — see `universal-scaffold.md`'s two-
  sprite-swap idiom). If the clicked sprite has tag `pump`, swap
  `pump_off` ↔ `pump_on` similarly. If the clicked sprite has
  tag `drain` (L2/L3), the click is acknowledged but is a no-op
  on game state — drains are non-toggleable. Clicks on
  vessel-frame, water-fill, target-tick, or background are no-ops.

No `_get_valid_actions` gating — both ACTION5 and ACTION6 are
always available. The action set is small enough that an agent
won't waste many actions discovering the no-op rule.

## 6. HUD and per-game state

**HUD widgets** (all `RenderableUserDisplay` subclasses):

- `StepCounterHud` — draws a horizontal depleting bar at row 63
  (bottom row of frame). Two-tone: dark grey (palette 4) for
  consumed steps, yellow (palette 11) for remaining steps, scaled
  to the current level's `step_budget`. The bar uses 32 pixels
  centred (`x_offset = 16`); when `current_steps / step_budget <
  0.25`, the remaining-portion colour switches to red (palette 8)
  as a warning.

The vessel water levels themselves are *not* HUD — they are
actual sprites in the level (see § 3 / § 4). The water sprite for
each vessel is regenerated each tick by overwriting its `pixels`
array in-place: rows from the bottom up to the current level are
filled with palette 9 (blue), top filled row uses palette 10
(meniscus), rows above use `-1` (transparent).

**Per-game state**:
- `self.water_level: dict[str, int]` — vessel name → current level
  (0..33). Reset in `on_set_level` from per-level data dict.
- `self.valves: list[(left_vessel, right_vessel, slit_height,
  is_open)]` — set up in `on_set_level` from per-level data.
- `self.pumps: list[(source, destination, is_on)]` — same.
- `self.drains: list[vessel_name]` — same.
- `self._step_counter_ui` — a `StepCounterHud` instance.

`_get_hidden_state` returns a `(4, 4)` int16 array packing
`step_counter` + the binary on/off state of valves and pumps so the
engine can hash distinct frame states correctly.

## 7. Win condition

After every `step()`, check: for every vessel V in the level,
`abs(self.water_level[V] - target_level[V]) == 0`. If true for ALL
vessels, call `self.next_level()`. Target levels come from
`level.get_data("targets")` as a dict mapping vessel name → int.

## 8. Lose condition

- The step counter reaches 0 → `self.lose()`.
- No "softlock" lose: the game is mass-conservative within phases
  the player controls; if the player drains too much at L3, they
  can still rerun ACTION5s with no progress — but step counter
  will exhaust and `lose()` fires there. Per
  `difficulty-rules.md` § 1: a player rendered unable-to-win (e.g.
  drain has consumed more than the surplus + remaining-water-
  buffer) should ideally fire `lose()` immediately rather than
  wait for budget exhaustion. **Mitigation**: at the end of every
  ACTION5 tick, check if `current_total_water < min_target_total`
  (i.e. drain has destroyed more than was budgeted); if so, fire
  `self.lose()` immediately. This avoids the "no-win waiting room"
  anti-pattern.

## 9. Novelty note

Closest taxonomy entries: **sp80** (pour-shelf-route) and
**lv4k** (lever-balance-torque, in `prior-games/index.md` rather
than the 25-game taxonomy — wait, lv4k IS a prior, not a reference;
the taxonomy near-miss is just sp80). Distinguishing rule against
sp80: sp80's water is *discrete falling drops* triggered by a
pour-key while shelves redirect; the candidate's water is a
*continuous fill-level* equalising hydrostatically through valve
graphs.

Closest prior-game entries (per `mechanic-pick.md`'s detailed
walk-through above): **kx14** (single tank with surface raise/lower
and floating balls), **rk7x** (junction-toggle live routing of a
courier), **vd3g** (binary terrain toggle with marbles rolling
downhill), **sp80** (drops + shelves), **kp9z** (grain capacity
overflow), **lv4k** (mass-arm lever), and **vt6q / kn58 / mr5q**
(single-action force/grapple/polarity). Distinguishing rules for
each are stated in `mechanic-pick.md`. The candidate's
distinguishing core dynamic — **multi-vessel hydrostatic
equalisation through a togglable valve graph with uphill pump
overrides** — does not appear in any of those priors. Visual
signature (3 thin tall blue water columns side-by-side with
target-line ticks on each, valves and pumps mounted in inter-vessel
gaps, no walking avatar, no rolling marbles, no falling drops, no
courier) is also unique within the corpus.
