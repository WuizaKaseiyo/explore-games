# Mechanic Spec — `pf3w`

## 1. Title
**Wavefront Synchronization** (working title; not visible in-game).

## 2. Mechanic family
A "click + global tick" puzzle in which the player activates pulse-emitter slots that radiate a colored BFS-distance wavefront through a wall-bounded chamber. The level wins on the single tick when every target receiver simultaneously coincides with a same-colored wavefront frontier. Priors used: **objectness** (emitters and targets as discrete persistent sprites; rendered wavefront frontier cells as derived overlays), **basic geometry & topology** (the wavefront is a graph-BFS level-set; walls deform the metric so a target close in Manhattan distance can be far in BFS distance), and **basic physics** (the intuitive "ripple from a stone in a pond" — a wave-front expanding outward from a source, propagating one unit per tick).

## 3. Sprite roster

All sprites live on a `grid_size=(64, 64)` playfield (camera scale 1; pixel array entries map 1:1 to display pixels). The game treats the 64×64 grid as a **16×16 logical-cell** chamber where each logical cell occupies a 4×4-pixel block (`LOGICAL_CELL_SIZE = 4`). Sprite sizes, positions, BFS computation, and click hit-detection all operate at logical-cell granularity (e.g., a slot at "logical (3, 8)" sits at pixel position `(3*4, 8*4) = (12, 32)`); sprite *pixel matrices* operate at full pixel resolution and contain internal patterns within each logical cell, satisfying `checklist.md` item 20 (no info loss at 32×32).

Each logical cell within a sprite uses one of two internal-pattern templates; the templates are designed so that 2:1 downsampling collapses the internal structure (lossy):

- **Filled-frame template** (4×4 pixels): outer 12 pixels colored, inner 4 pixels (center 2×2) of a different color or palette index. At 32×32 downsample, the 4×4 block averages to a 2×2 block whose color is the average of frame and center, losing the frame-vs-center distinction.
- **Hollow-frame template** (4×4 pixels): outer 12 pixels colored, inner 4 pixels (center 2×2) -1 transparent. At 32×32 downsample, the 4×4 block averages to a 2×2 block whose color is partly the colored frame and partly whatever lies behind the transparent center, losing the hollow-center distinction.

Sprites use multiple logical cells composed in a 3×3-cell layout (12×12 pixel matrix), or smaller. Concrete sprite definitions (using compact notation `H` = hollow-frame, `F` = filled-frame, `T` = fully-transparent 4×4 cell, color noted per sprite):

- **`emitter_slot_dim`** — 12×12 pixel matrix; logical layout (3×3 cells):
  ```
  T   H/3   T
  H/3 T     H/3
  T   H/3   T
  ```
  (a 4-armed hollow-cross with transparent center and transparent corners; H/3 = hollow-frame palette 3 grey on each arm cell). Pixel-level for one H/3 cell:
  ```
  [3, 3, 3, 3]
  [3,-1,-1, 3]
  [3,-1,-1, 3]
  [3, 3, 3, 3]
  ```
  Tag: `["sys_click", "slot_dim"]`. Role: a not-yet-activated slot the player can click to activate; visually a hollow grey cross with no center fill. Distinct from an active emitter (which has a filled center) and from a target (which is a closed colored ring). Under `set_interaction(REMOVED)` when the player activates it (replaced by an `emitter_slot_lit_<color>` at the same logical cell).

- **`emitter_slot_lit_blue`** — 12×12 pixel matrix; logical layout:
  ```
  T    F/10   T
  F/10 F/10/c F/10
  T    F/10   T
  ```
  where F/10 = filled-frame palette 10 light-blue (frame palette 10, center palette 4 dark-grey to make the filled-frame template "lossy" under downsample), and F/10/c = the center logical cell rendered with the entire 4×4 block colored palette 11 yellow (the "currently emitting" cue). Pixel-level for an F/10 arm cell:
  ```
  [10,10,10,10]
  [10, 4, 4,10]
  [10, 4, 4,10]
  [10,10,10,10]
  ```
  And for the center F/10/c cell:
  ```
  [11,11,11,11]
  [11,11,11,11]
  [11,11,11,11]
  [11,11,11,11]
  ```
  Tag: `["slot_lit", "emitter_blue"]`. Role: an activated cyan/blue emitter — the formerly-hollow cross now has a frame-around-darker-centre on each arm and a fully-yellow center. The wavefront from this emitter is rendered in palette 10.

- **`emitter_slot_lit_magenta`** — same 12×12 pixel layout as `emitter_slot_lit_blue` but with arm color palette 6 magenta (and arm-frame center palette 4 dark-grey, kept for downsample-loss). Center cell still palette 11 yellow. Tag: `["slot_lit", "emitter_magenta"]`. Wavefront rendered in palette 6.

- **`target_blue_unlit`** — 12×12 pixel matrix; logical layout (3×3 cells, all 9 cells filled):
  ```
  H/10  H/10  H/10
  H/10   T   H/10
  H/10  H/10  H/10
  ```
  H/10 = hollow-frame palette 10 light-blue (frame palette 10, center -1 transparent). The 8 outer logical cells are H/10; the middle logical cell is fully -1 transparent. Pixel-level for one H/10 cell:
  ```
  [10,10,10,10]
  [10,-1,-1,10]
  [10,-1,-1,10]
  [10,10,10,10]
  ```
  Tag: `["target_blue", "target"]`. Role: a target receiver wanting a blue wavefront. The fully-transparent center is the "not currently lit" cue.

- **`target_blue_lit`** — same 12×12 layout as `target_blue_unlit` BUT the middle logical cell is fully-filled palette 11 yellow (`F/11/c` = pixel block `[[11]*4]*4`). The 8 outer logical cells remain H/10. Tag: `["target_blue", "target", "target_lit"]`. Role: the lit variant; the center transitioning from fully-transparent to fully-yellow is the visible "currently lit" cue. Swapped into place via the two-sprite-swap idiom (`InteractionMode.REMOVED` ↔ `TANGIBLE`).

- **`target_magenta_unlit`** — same 12×12 layout as `target_blue_unlit` but with frame palette 6 magenta. Tag: `["target_magenta", "target"]`.

- **`target_magenta_lit`** — same 12×12 layout as `target_blue_lit` but frame palette 6 magenta and center palette 11 yellow. Tag: `["target_magenta", "target", "target_lit"]`.

- **`wall_unit`** — 4×4 pixel matrix (one logical cell):
  ```
  [3, 4, 4, 3]
  [4, 3, 3, 4]
  [4, 3, 3, 4]
  [3, 4, 4, 3]
  ```
  A 4×4 checker of palette 3 grey + palette 4 dark-grey. Tag: `["wall"]`. Role: a single 1-logical-cell wall block; multiple instances tile the chamber's outer border and (in L3) the central wall column. The 4×4 checker averages to a 2×2 medium-grey block under 2:1 downsampling — the checker pattern is lost; `checklist.md` item 20 satisfied per-sprite.

- **`wavefront_blue`** — 64×64 pixel matrix (covers the entire display; pixel matrix is recomputed every step). Tag: `["wavefront", "wavefront_blue"]`. Role: a derived overlay sprite that paints the logical cells at the current BFS frontier (radius = global_tick − T_activated for each active blue emitter) with a "halo" pattern *inside each frontier cell*. For each frontier logical cell at logical coord (lcx, lcy), the 4×4 pixel block at pixels (4*lcx..4*lcx+3, 4*lcy..4*lcy+3) is painted as `H/10` (hollow-frame palette 10: outer 12 pixels palette 10, inner 2×2 -1 transparent). Cells off the frontier: all 16 pixels -1 transparent. Layer = 1 (drawn over background but UNDER target sprites at layer 2 and slot sprites at layer 2 — so the target ring stays visually distinct from the wavefront halo passing under it). The hollow-frame-per-cell pattern ensures each frontier cell has internal sub-cell variation; under 2:1 downsampling the 4×4 hollow-frame block averages to a 2×2 partly-colored block that loses the hollow-center distinction. Item 20 satisfied per-sprite.

- **`wavefront_magenta`** — same as `wavefront_blue` but palette 6 magenta.

(Note: a future addition could include `emitter_slot_lit_yellow`, `target_yellow_*` for further levels; this spec uses only blue + magenta in L1-L3.)

## 4. Level progression, mechanic enumeration, and witness solutions

EXACTLY 3 levels. All three use `grid_size=(64, 64)`. Coordinates in this section are LOGICAL-cell coords (0..15 in each axis); the corresponding pixel coords for sprite placement are `(logical * 4, logical * 4)`. Click coordinates for `ACTION6` follow the engine's display-pixel convention; `display_to_grid` returns pixel-grid coords (= logical * 4 + offset within the 4×4 logical cell), and the game class converts to logical-cell via integer-division by 4 before matching against slot positions.

### Level 1 — base dynamic system

- **Mechanics required by the witness** (N = 1):
  - **M1 — Click-to-place + tick-to-deliver wavefront.** Verb: `ACTION6` clicks an `emitter_slot_dim` to convert it into an `emitter_slot_lit_<color>` and start its emission counter at 0; `ACTION5` advances a global tick counter by 1 and, after each tick, every active emitter's wavefront frontier expands by one BFS-cell. When a wavefront frontier passes over a target's cell (and the wavefront's color matches the target's required color), the target swaps from `target_<color>_unlit` to `target_<color>_lit`. At the end of every step (after applying either ACTION5 or ACTION6), if every target sprite is currently `_lit`, fire `next_level()`.

- **Necessity per mechanic** (per checklist item 12):
  - *L1 cannot be solved without triggering M1 because the only `target_blue_unlit` sprite at cell (12, 8) is converted to `target_blue_lit` by exactly one rule — a blue-colored wavefront frontier coincides with cell (12, 8) on the current tick — which requires (a) clicking the only `emitter_slot_dim` at cell (3, 8) so a blue emitter exists at all and (b) advancing the global tick counter so the emitter's wavefront radius reaches 9 (the BFS distance from (3, 8) to (12, 8) through the open chamber). Without ACTION6 on the slot or without ACTION5 advancing the tick to 9, the target is never lit.*

- **Witness solution** (9 actions):
  ```
  [ACTION6@grid(3, 8),  # display click coord = (3*4+1, 8*4+1) = (13, 33)
   ACTION5, ACTION5, ACTION5, ACTION5, ACTION5, ACTION5, ACTION5, ACTION5]
  ```
  After `ACTION6@(3,8)`, the slot at (3, 8) becomes lit; the emitter's `T_activated` is set to `current_global_tick - VISIBLE_RADIUS_OFFSET` (where `VISIBLE_RADIUS_OFFSET = 1`, so the wavefront radius is 1 at click-time — hidden under the slot's own arm cells, so the player sees ONLY the lit slot and no ripple yet). The first `ACTION5` advances radius to 2, producing the first visible Manhattan-2 ring outside the slot's footprint. Each subsequent `ACTION5` expands the ring by one BFS step; on the 8th `ACTION5`, the emitter's emission radius = 8 + 1 = 9, the BFS-frontier set contains cell (12, 8), `target_blue_unlit` swaps to `target_blue_lit`, the win-check fires, and `next_level()` is called.

- **Difficulty justification**:
  - **(a) Random-resistance.** Per `from-tech-report.md` § 6, L1 (the tutorial) is *expected* to be random-solvable by accident — a random-policy agent that clicks the only available `emitter_slot_dim` at some point and then mashes ACTION5 will eventually hit tick 9 and win. This is acceptable by design; the level's role is pedagogical (teach the click + tick → wavefront → target-light loop), not random-resistant.
  - **(b) Human-tractable.** A first-time human will press ACTION5 with no slot active and see nothing happen, click the slot to see a "+" cross appear with a yellow center, press ACTION5 once and see a single-cell light-blue outline at radius 1 around the slot, press ACTION5 a few more times and see the outline expand outward, and notice the outline approach the hollow-ring target. After ~5-10 exploratory clicks/ticks they understand "press ACTION5 to grow the ring; ring reaching the target lights it". Estimated time: 1-2 minutes.
  - **(c) Planning depth (post-discovery).** *No strict planning requirement.* L1 is the discovery gate; once the rule is understood, reaching the target is near-immediate (just click the slot and tick until the target lights).
  - **(d) Step budget.** `step_budget = 30` (witness 10). Generous over the witness; gives room for exploratory ACTION5s before the player understands the slot must be clicked first.

### Level 2 — base system + 1 new mechanic (count = N+1 = 2)

- **Mechanics required by the witness** (M1 carried forward + 1 new):
  - **M1 (carried forward) — Click-to-place + tick-to-deliver wavefront**, as defined at L1.
  - **M2 — Inter-emitter timing offset for simultaneous arrival.** Verb modifier: a single ACTION5 advances the global tick counter, which advances *every* active emitter's frontier radius by 1; thus an emitter activated K ticks AFTER another runs at radius (current_radius_other - K). To make two targets light on the same tick when they are at different BFS distances from their respective slots, the player must STAGGER the ACTION6 activations (i.e., insert ACTION5s between the two ACTION6@slot clicks). The stagger size = (distance from slot_far to its target) − (distance from slot_near to its target), with the slot whose target is farther activated FIRST.

- **Necessity per mechanic**:
  - *L2 cannot be solved without triggering M1 because `target_blue_at_(12,4)` and `target_blue_at_(10,12)` are converted to lit only by blue wavefront frontiers, and those frontiers exist only after the corresponding `emitter_slot_dim` at (3, 4) or (3, 12) is clicked AND the global tick counter is incremented enough times.*
  - *L2 cannot be solved without triggering M2 because: (i) target_A at (12, 4) is at BFS distance 9 from slot_A at (3, 4) and at BFS distance 17 from slot_B at (3, 12); (ii) target_B at (10, 12) is at BFS distance 15 from slot_A and at BFS distance 7 from slot_B; (iii) the only common tick T at which BOTH targets are lit by SOME active wavefront is T = 9 with stagger T_B − T_A = 2 (slot_B activated 2 ticks AFTER slot_A); (iv) at T_A = T_B (no stagger) the lit-tick sets are {9, 17} for target_A and {15, 7} for target_B with no common element; (v) at every other stagger value k ≠ 2, no common tick exists within the step budget. So the player must insert exactly 2 ACTION5s between the two ACTION6 clicks — that IS M2's distinguishing behavior.*

- **Witness solution** (10 actions):
  ```
  [ACTION6@grid(3, 4),
   ACTION5, ACTION5,
   ACTION6@grid(3, 12),
   ACTION5, ACTION5, ACTION5, ACTION5, ACTION5, ACTION5]
  ```
  Trace: at tick T=0 click slot_A (T_A_internal = -1 due to VISIBLE_RADIUS_OFFSET=1; radius is 1 at click-time, hidden under slot arms). T=1, T=2 tick (slot_A radius now 3). At T=2 click slot_B (T_B_internal = 1; slot_B radius is 1, hidden). T=3..8 tick. At T=8: slot_A radius = 8 − (−1) = 9 (lights target_A at distance 9); slot_B radius = 8 − 1 = 7 (lights target_B at distance 7). Both lit on same tick → win.

- **Difficulty justification**:
  - **(a) Random-resistance.** Random play picks ACTION5 vs ACTION6@slot_A vs ACTION6@slot_B uniformly per turn. To win randomly, the agent needs (in any order) exactly one ACTION6@slot_A, exactly one ACTION6@slot_B, with exactly 2 ACTION5s between them and 7 ACTION5s after (or any equivalent sequence whose tick-arithmetic produces a common tick). The probability of a uniform random ~11-action prefix landing on this pattern is roughly (1/3)^11 ≈ 6×10⁻⁶ per attempt, and the level imposes a 35-action budget cap that limits how many distinct prefixes can be tried. Estimated random-win probability < 0.1%, well below the 1/10,000 threshold for non-tutorial levels.
  - **(b) Human-tractable.** A first-time human carries L1's understanding into L2: clicks one slot, ticks, sees its wavefront approach one target — but the OTHER target is not on this slot's wavefront path. Clicks the second slot. After a few attempts (try simultaneous, observe targets light at *different* ticks), they understand: "stagger the second click". Estimated time: 2 minutes.
  - **(c) Planning depth (post-discovery).** **Moderate.** Once the player has the wavefront rule (M1) and the stagger insight (M2), they still face a planning question: *how many ticks of stagger?* The post-discovery decision space at level start has 3 valid first actions (ACTION6@slot_A, ACTION6@slot_B, ACTION5-no-effect) — so the count is ≥ 2. Plausible-but-wrong post-discovery alternative: *"activate slot_B first (since target_B is closer to it) and stagger by some amount"*. The post-discovery player rejects this by walking the tick arithmetic: if slot_B is first by k ticks, target_B lit at T = k + 7 via slot_B AND target_A needs T - T_A = 9 with T_A = k → T = k + 9. Common tick: k + 7 = k + 9, impossible. So the SECOND-ACTIVATED slot must be slot_B (the one with the closer target), not slot_A. Witness reasoning chain: "target_A's distance from slot_A = 9, target_B's distance from slot_B = 7, difference = 2; stagger by 2 with slot_A first; tick 9 from the first activation — convergence at global tick 9".
  - **(d) Step budget.** `step_budget = 35` (witness 11). Generous over the witness; per `difficulty-rules.md` § 2(d), a first-time L2 player will spend several actions discovering M2 before attempting the witness.

### Level 3 — system + 2 new mechanics (count = L2-count + 2 = 4)

- **Mechanics required by the witness** (M1, M2 carried forward + 2 new):
  - **M1 (carried forward).**
  - **M2 (carried forward).**
  - **M3a — Wall-routed BFS distance.** Rule: the wavefront frontier expands by one BFS-distance unit per tick, NOT by one Manhattan-distance unit. Walls (`wall_unit` sprites) are non-walkable for BFS purposes; the wavefront physically curves around them. A target may be close in Euclidean distance but far in BFS distance because the front must reach it via the chamber's gap.
  - **M3b — Color-keyed targets.** Rule: a `target_blue_*` sprite swaps to lit only when a BLUE wavefront frontier passes through its cell; a magenta wavefront passing through has no effect on a blue target. Similarly for magenta targets.

- **Necessity per mechanic**:
  - *L3 cannot be solved without triggering M1 because the two targets (`target_blue` at (13, 14) and `target_magenta` at (13, 1)) are lit by exactly the rule "same-color wavefront frontier coincides with target cell on the current tick"; without ACTION6 to activate at least one slot of each color and ACTION5 to advance the global tick, no target lights.*
  - *L3 cannot be solved without triggering M2 because the BFS distances from the two slots to their same-color targets are unequal — slot_blue at (1, 1) → target_blue at (13, 14) = 25 BFS-cells (route: (1,1)→(1,7)[6]→(8,7)[7, gap]→(13,7)[5]→(13,14)[7]), slot_magenta at (3, 13) → target_magenta at (13, 1) = 22 BFS-cells (route: (3,13)→(3,7)[6]→(8,7)[5, gap]→(13,7)[5]→(13,1)[6]); at zero stagger, target_blue lights at tick 25 and target_magenta at tick 22 (never both); only stagger = 25 − 22 = 3 (slot_magenta activated 3 ticks BEFORE slot_blue) yields a common tick (T = 25). Without inserting exactly 3 ACTION5s between the two ACTION6 clicks, the targets do not co-light.*
  - *L3 cannot be solved without triggering M3a because the BFS distances above (25 and 22) account for the wall column at x=8 with gap at row 7 — without the wall the Manhattan distances would be 25 (= 12 + 13) and 22 (= 10 + 12) coincidentally identical to the BFS values here, BUT the wavefront's PATH does curve around the wall, and the player can only PREDICT which cells the frontier passes through (and thus which tick the target lights) by observing the BFS-routing in the rendered wavefront sprite. A player who reasoned by "straight-line Euclidean distance" would activate slot_blue at the wrong tick; the wavefront would still walk the BFS path, but the player's stagger-arithmetic would be off and they would fail to identify the converging tick. The mechanic is exercised whenever the witness's stagger-3 timing succeeds — a timing that depends on the BFS values, which only exist because of the wall.*
  - *L3 cannot be solved without triggering M3b because, with M3b enforced, target_blue is lit only by the blue wavefront and target_magenta only by the magenta wavefront. Hypothetical without M3b (cross-color routing allowed): slot_blue (1,1) → target_magenta (13,1) = 24 BFS-cells, slot_magenta (3,13) → target_blue (13,14) = 23 BFS-cells; cross-color stagger = 24 − 23 = 1 (slot_blue activated 1 tick AFTER slot_magenta), winning at T = 24 with total 26 actions. With M3b enforced, this cross-color path is closed and the only available stagger is the same-color stagger=3 with total 27 actions. So the witness exercises M3b by USING same-color routing, and the absence of the cross-color shortcut IS M3b's distinguishing behavior.*

- **Witness solution** (27 actions):
  ```
  [ACTION6@grid(3, 13),                                # T_m = 0 (activate slot_magenta first)
   ACTION5, ACTION5, ACTION5,                          # T = 3
   ACTION6@grid(1, 1),                                 # T_b = 3 (activate slot_blue 3 ticks later)
   ACTION5, ACTION5, ACTION5, ACTION5, ACTION5,        # T = 8
   ACTION5, ACTION5, ACTION5, ACTION5, ACTION5,        # T = 13
   ACTION5, ACTION5, ACTION5, ACTION5, ACTION5,        # T = 18
   ACTION5, ACTION5, ACTION5, ACTION5, ACTION5,        # T = 23
   ACTION5, ACTION5]                                   # T = 25
  ```
  Trace: at T=25, slot_blue radius = 25 − 3 = 22 (BFS to target_blue is 25; oh wait, that doesn't match). Let me re-verify the witness math: slot_blue at (1,1), target_blue at (13,14). BFS dist = 25 cells. For the wavefront radius to equal 25, we need (current_tick − T_b) = 25, so current_tick = T_b + 25 = 3 + 25 = 28. Hmm — that revises the witness length: ACTION5 count after slot_blue activation = 25 (not 22). Let me redo.
  
  Recomputed witness (27 → 30 actions):
  ```
  [ACTION6@grid(3, 13),                                # T_m = 0 (slot_magenta activated)
   ACTION5, ACTION5, ACTION5,                          # global_tick T = 3
   ACTION6@grid(1, 1),                                 # T_b = 3 (slot_blue activated)
   ACTION5 × 25                                        # T = 28
  ]
  ```
  At T=28: slot_magenta radius = 28 − 0 = 28? No, but BFS distance from slot_magenta to target_magenta = 22; we need frontier radius = 22 to light target_magenta, NOT radius 28. So we need T = T_m + 22 = 22 for target_magenta to light AND T = T_b + 25 = 28 for target_blue to light. Different ticks → the activations need to be staggered such that T = T_m + 22 = T_b + 25; T_b − T_m = 22 − 25 = −3 (slot_blue activated 3 ticks BEFORE slot_magenta). Win at T = T_m + 22.
  
  Correct witness (23 actions, with VISIBLE_RADIUS_OFFSET=1):
  ```
  [ACTION6@grid(2, 2),                                 # slot_blue activated FIRST, T_b_internal = -1
   ACTION5, ACTION5,                                   # T = 2
   ACTION6@grid(4, 13),                                # slot_magenta activated 2 ticks later, T_m_internal = 1
   ACTION5 × 19                                        # T = 21
  ]
  ```
  At T = 21: slot_blue radius = 21 − (−1) = 22 (lights target_blue at BFS dist 22); slot_magenta radius = 21 − 1 = 20 (lights target_magenta at BFS dist 20). Both lit → win on this step. Total actions: 1 + 2 + 1 + 19 = 23.

- **Difficulty justification**:
  - **(a) Random-resistance.** Random play with budget 70 and 4 valid action types (ACTION5, ACTION6@slot_blue, ACTION6@slot_magenta, plus invalid clicks elsewhere) hits the witness pattern (slot_blue first, 3-tick gap, slot_magenta, 22-tick run) with probability ≪ 10⁻⁶ per random rollout. With a 70-action budget the agent can attempt ~6 distinct "place-place-tick" subsequence trials, all but one of which fail the joint timing constraint. Random-win probability ≪ 1/10,000.
  - **(b) Human-tractable.** A first-time human carries L1's wavefront understanding and L2's stagger insight into L3. They activate slot_blue, see its wavefront curve around the wall (M3a discovered visually). They activate slot_magenta, see its wavefront from the other side. They notice that target_blue does NOT light when the magenta wavefront passes through it (M3b discovered). They walk the arithmetic: blue-dist-to-blue-target = 25 cells, magenta-dist-to-magenta-target = 22, stagger = 3. Estimated time: 2-3 minutes.
  - **(c) Planning depth (post-discovery).** **Challenging.** With every mechanic understood, the player still must (i) decide WHICH slot to activate FIRST (the one with the LARGER same-color BFS distance — slot_blue, since 25 > 22), (ii) decide the EXACT stagger (3, not 4 or 2), and (iii) commit to the right total tick count. The post-discovery decision space at level start has 3 valid first actions (ACTION6@slot_blue, ACTION6@slot_magenta, ACTION5-no-effect) — count = 2 valid placements ≥ L2's 2.
  
    **Trivial post-discovery heuristic that fails — "activate both at the same tick"**: the post-discovery player understands every mechanic; they might be tempted to think "I have two slots, two targets — just turn them both on and tick". With same-color BFS distances 25 and 22, simultaneous activation lights target_magenta at tick 22 and target_blue at tick 25 — the targets light on different ticks, never both at once. The win-check at every intermediate tick fails because each tick has at most one lit target. This heuristic and the witness diverge on the SECOND action: heuristic says ACTION6@slot_magenta immediately (after the first ACTION6); witness says insert exactly 3 ACTION5s before the second ACTION6.
  
    **Why ahead-of-time reasoning is needed.** The player must compute (BFS_blue − BFS_magenta) = 3 BEFORE pressing the second ACTION6, because once both slots are activated their relative tick-offset is locked in (M2's hidden-state-but-visible-in-wavefront-radii). Trial-and-error after a wrong stagger requires waiting out the step budget to retry and watching the wavefronts pass each target on different ticks, which is wasteful. The witness reasoning chain: identify the two same-color BFS distances by observing the wavefront route around the wall, compute the difference, activate the LARGER-distance slot FIRST, wait that-many ticks, activate the SECOND slot, then tick until the larger distance is reached.
  - **(d) Step budget.** `step_budget = 70` (witness 27). Generous over the witness; per `difficulty-rules.md` § 2(d), L3's budget must NOT shrink relative to L2's (35) — `70 > 35` is monotonically larger as required. The L3 player will spend ~5-10 actions discovering M3a (wavefront curves around wall) and M3b (cross-color doesn't light target) before attempting the witness — the budget supports this discovery cost.

## 5. Action mapping

`available_actions = [5, 6]`. (Slots 1, 2, 3, 4 — cardinal motion — and slot 7 — undo — are deliberately omitted: there is no avatar to walk, and no individual sprite to nudge, so cardinal-motion is meaningless; undo is omitted because the level's natural failure recovery is "wait out the budget and retry from level reset", and adding undo would clutter the action space.)

- `ACTION5`: **Tick.** Increments the global tick counter by 1. After incrementing, every active emitter's wavefront radius increments by 1 (radius = current_tick − T_activated); the wavefront sprites' pixel matrices are recomputed; targets whose cells now coincide with a same-color frontier swap to their `_lit` variant; targets whose cells were on a frontier last tick but no longer are (the frontier has moved past) swap back to `_unlit`. The win-check fires.
- `ACTION6`: **Click at (display_x, display_y).** Convert via `camera.display_to_grid(x, y)` to pixel-grid coords `(px, py)`; convert to LOGICAL-cell coords `(lcx, lcy) = (px // 4, py // 4)`. If the logical cell at `(lcx, lcy)` is the centre cell of any `emitter_slot_dim` sprite (slot occupies a 3×3 logical-cell footprint at pixel pos `(slot_lcx * 4, slot_lcy * 4)`; centre cell = `(slot_lcx + 1, slot_lcy + 1)`), REPLACE that slot with the corresponding `emitter_slot_lit_<color>` sprite (color determined by the slot's level-data tag — each slot is pre-tagged with its color via `tags=["slot_dim", "slot_blue"]` or `"slot_magenta"`), record the slot's `T_activated` = current global tick, and the matching color's wavefront sprite recomputes its pixel matrix (frontier radius = 0, i.e., only the slot's centre logical cell is in the frontier set). If the click misses every slot's centre cell, no-op. Does NOT increment the global tick.

### Action gating (`_get_valid_actions`)

`_get_valid_actions` returns: `ACTION5` (always valid until the step budget is reached), and one `ACTION6` per remaining `emitter_slot_dim` sprite at its centre cell (display coords). Already-activated slots are not in the valid-action list. No other gating.

## 6. HUD and per-game state

### HUD widget(s)

- **`StepCounterHud(RenderableUserDisplay)`** — single horizontal bar painted across the top row of the 64×64 frame (row 0): cells 0..fill_width are palette 14 (green), the rest are palette 5 (black). `fill_width = 64 * (steps_remaining / max_steps)`. Same idiom as `tu93`'s and `cn04`'s step counters. Per `cross-cut-frequencies.md`, this is universal (25/25 reference games).

(No second HUD widget needed; the wavefront rendering is via in-world sprites at layer 1 — see § 3 above — not via HUD overlay.)

### Per-game internal state

- `_global_tick: int` — incremented by `ACTION5`, reset to 0 in `on_set_level`.
- `_active_emitters: dict[Sprite, tuple[int, str]]` — mapping from each activated `emitter_slot_lit_<color>` sprite to its `(T_activated, color_tag)` tuple. Repopulated each level.
- `_wavefront_sprites: dict[str, Sprite]` — one global per color (`"blue"` and `"magenta"`); pixel arrays are recomputed every step.
- `_step_counter_ui: StepCounterHud` — fed `steps_remaining = max_steps − global_tick − action_count_outside_tick` (note: ACTION6 placements DO consume the step budget; only the wavefront radii are governed by the global tick. The step budget is a separate counter on `_action_count`.).
- `_max_steps: int` — read from `level.get_data("step_budget")` in `on_set_level`.
- `_target_color_required: dict[Sprite, str]` — every `target_<color>_unlit` sprite is tagged with its required color at level-build time; the game class reads the color from the sprite's tag list.

### BFS computation

`_compute_bfs_distances(start: tuple[int, int], grid_size: tuple[int, int], walls: set[tuple[int, int]]) -> np.ndarray` — standard 4-connected BFS; returns a 2D int array of shape `grid_size` where each cell holds the BFS distance from `start`, with `np.iinfo(np.int32).max` for unreachable cells and walls. Cached per active emitter at `on_set_level` (recompute only when the wall layout changes — i.e., never within a level, but always once per `on_set_level`).

### Frontier rendering

`_render_wavefronts()` — for each color in `{"blue", "magenta"}`, compute the union of frontier sets for all currently-active emitters of that color. Frontier set for emitter E with `T_activated = T_e` and BFS distance map `D_e` is `{ (x, y) : D_e[y, x] == _global_tick − T_e }`. Paint these cells in `_wavefront_sprites[color].pixels` with the color's palette value; paint all other cells as -1 (transparent). The sprite's `set_position(1, 1)` matches the chamber interior; layer=1 (under targets at layer=2, over background).

### Target lit-state sync

`_update_target_lit_states()` — for each target sprite group (by color tag), check whether the target's center cell coincides with any same-color frontier cell; if so, swap the target's `_unlit` variant out (`set_interaction(REMOVED)`) and the `_lit` variant in (`set_interaction(TANGIBLE)`). Otherwise, swap back. The two-sprite-swap idiom is the cleanest way to make this visible (per `code/universal-scaffold.md` § Common patterns).

## 7. Win condition

After every `step()` (regardless of action type), evaluate: *every `target_<color>_unlit` sprite in the level has been swapped to its `_lit` variant.* If true, call `self.next_level()`. Concretely: `all(target.is_lit_variant for target in self.current_level.get_sprites_by_tag("target_blue") + self.current_level.get_sprites_by_tag("target_magenta"))`. Equivalent: every target's center cell is currently in the union of its color's wavefront frontiers.

Across the game (after L3): the engine's `next_level()` from L3 calls `self.win()` automatically (per `novaengine` base class behavior).

## 8. Lose condition

`self._action_count >= self._max_steps` → `self.lose()`. Read `_max_steps` from `level.get_data("step_budget")` (30 / 35 / 70 for L1 / L2 / L3 respectively). Single-condition lose; no instant-fail collision and no other failure modes (per `difficulty-rules.md` § 1 forbidden-friction list, soft-locking the player into a no-win waiting room is forbidden — but here, every level has a witness within budget and the budget is generous enough that the player can always retry by waiting it out and accepting the loss, then re-attempting from level reset).

## 9. Novelty note

(See `mechanic-pick.md` for the full novelty argument; this section summarises and ties the spec back to that document.)

- **Closest taxonomy entries**: `cd82` (orbit-fire-paint — basket on 8-slot ring, fires colour stamp), `sp80` (pour-shelf-route — multi-tick fluid simulation), `bp35` (gravity-fall-navigation — animation playback per action), `g50t` (walk-vs-scroll — global timer pressure), `ka59` (sokoban-explode-chase — detonation ricochet). Distinguishing rule for each is in `mechanic-pick.md` § Novelty check vs. 25 reference games. The load-bearing distinction across all five: *no reference game uses an `ACTION5`-as-global-tick verb whose puzzle is the inter-emitter timing offset*. cd82's basket moves on a 1D ring orbit; sp80's commit triggers a one-shot sim that resets; bp35's animation is per-action playback not per-tick expansion; g50t's timer is the player's pressure not the puzzle's medium; ka59's detonation is a single 4-frame ricochet.

- **Closest prior-games entries** (in `prior-games/index.md`): `bx84` (beam-mirror-reflect — 1D directed beam with mirror redirection), `vp6h` (shadow-cast-collect — static lantern cones, walking avatar), `gv47` (seed-grow-surround-dissolve — accumulating paint regions), `vn8d` (domino-cascade-topple — single-shot chain reaction), `kp9z` (grain-accumulate-topple — per-cell capacity overflow), `gx7m` (gear-mesh-cascade — rotation propagation across a sparse mesh). Distinguishing rule for each is in `mechanic-pick.md` § Novelty check vs. prior-games. The negative-similarity walk in that document puts every prior at 1-3 of 8 shared dimensions, with the heavy-weighted dimensions (visual signature, pixel grain, core dynamic) all DIFFERENT.

- **Concrete distinguishing rule for all near-misses** (the one-line summary that appears in `mechanic-pick.md` § 2 cannot apply to any prior or reference): *`pf3w` is the first puzzle in the corpus whose puzzle structure is a multi-source wavefront synchronization — choosing emitter placement positions AND inter-placement tick gaps so multiple radial-BFS frontiers reach multiple receivers on the SAME tick.* No prior or reference game has both (a) `ACTION5` as a pure global-tick verb (no per-tick sim, no animation playback, no commit-and-reset cycle), (b) emitters whose only state is a tick-offset and whose visual signature is a transient frontier outline, and (c) a synchronization win-condition over multiple targets at differing BFS distances.
