# fz5j — Mechanic spec

## 1. Title
Phase-Step Tile Walk *(working name; not visible in-game)*

## 2. Mechanic family
`phase-step-tile`. The avatar walks a small grid populated with **periodically-pulsing tiles**: each tile has a hidden integer period n ∈ {2, 3, 4} and a hidden offset 0..n-1. The tile is *open* (walkable) at global step counter `t` iff `t % n == offset`; otherwise *closed*. A move into a closed tile is **rejected** (avatar stays put) but the step counter still increments — so a blocked attempt acts as an "implicit wait" that shifts the player's arrival on later phase tiles. Walls are permanently closed; the goal cell is permanently open.

Priors used (per `core-knowledge-priors.md`):
- **Objectness** — avatar, walls, tiles, goal exist as discrete persistent entities.
- **Basic geometry & topology** — path connectivity through a 2D grid.
- **Basic physics (temporal)** — counter-driven periodicity is a clock-rhythm prior (cycle of seasons, breathing, alternation).

No agentness (no NPCs).

## 3. Sprite roster
*(Semantic names per `code/universal-scaffold.md` § Style rules. Class name is `Fz5j`.)*

- **`avatar`** — 4×4. Open square frame palette 14 (green) with palette 4 (off-black) inner ring; transparent (-1) centre. Movable; collides with walls and closed tiles. Tags: `["player"]`.
- **`wall`** — 4×4 solid palette 4. Permanent obstacle. Tags: `["wall"]`.
- **`goal`** — 4×4 hollow palette 11 (yellow) ring with -1 centre. Walkable; reaching its cell wins the level. Tags: `["goal"]`.
- **`phase2_open`** / **`phase2_closed`** — 4×4. Open: palette 10 (light-blue) frame + palette 11 yellow centre dot. Closed: palette 5 (black) solid. Two-sprite-swap idiom (per `code/universal-scaffold.md` § Two-sprite swap): both variants pre-placed at the same cell with opposite `InteractionMode`; runtime swaps modes per step. Tags: `["phase_tile", "period_2"]`.
- **`phase3_open`** / **`phase3_closed`** — 4×4. Open: palette 6 (magenta) frame + palette 11 dot. Closed: palette 5 solid. Tags: `["phase_tile", "period_3"]`.
- **`phase4_open`** / **`phase4_closed`** — 4×4. Open: palette 12 (orange) frame + palette 11 dot. Closed: palette 5 solid. Tags: `["phase_tile", "period_4"]`.
- **`fragile_open`** / **`fragile_closed`** / **`fragile_locked`** — 4×4. Same shape as phase3 but with a SINGLE palette 8 (red) cell at the top-left corner of the frame, distinguishing fragile tiles from regular phase-3 tiles via a single inset cell (geometric mark, not a symbol or glyph). `fragile_locked` is a permanently-closed variant whose pixels are all palette 5 (black). The fragile rule (L3 only): on the first BLOCKED attempt, the cell becomes permanently `fragile_locked`. Tags: `["phase_tile", "period_3", "fragile"]`.

Each placed phase tile carries its `offset` value via per-cell level data — `level.get_data("phase_offsets")` returns a `dict[(x,y) → offset]`. `on_set_level` stamps each phase-tile instance's offset onto an in-memory dict keyed by sprite name.

Palette signature: `{1 background, 4 wall+letterbox, 5 closed, 6 magenta, 8 fragile-mark, 10 light-blue, 11 yellow goal+dot, 12 orange, 14 green avatar}`. Distinct from the kf42→vh68 cautionary `{4, 8, 9}` signature.

Pixel grain: every phase tile has internal frame+dot pattern (not flat). Avatar has internal frame+ring. Walls are solid 4×4 blocks. Visual coupling: open tiles share the yellow centre-dot motif with the goal sprite.

## 4. Level progression, mechanic enumeration, and witness solutions

EXACTLY 3 levels. All levels declare `grid_size=(64,64)` (full 64-px frame, no camera resize); each "logical cell" is 4×4 px, sprites placed at multiples of 4. This matches the wa30 idiom (cell stride `celomdfhbh = 4`).

Convention: `step_counter` starts at 0 at level start; each ACTION-N (whether move succeeds or is rejected) increments to 1, 2, ... A phase-tile's `is_open(t)` is checked at the counter value AFTER the increment (so the first action's destination is checked at t=1).

### Level 1 — base dynamic system

Layout (logical cells):
- Wall ring around grid (cells x∈{0,15}, y∈{0,15}).
- Avatar at (1,5).
- Goal at (14,5).
- Phase-2 (offset 0) at (4,5) and (10,5).
- All other cells open floor.

Step budget: 22.

- **Mechanics required by the witness** (N=2):
  1. **Avatar walk** — ACTION1-4 attempts to move one cell; succeeds iff destination walkable; counter ticks regardless.
  2. **Phase-2 gate** — phase-2 tile walkable iff `step % 2 == offset`; closed phase-2 rejects move (counter still ticks).
- **Necessity per mechanic**:
  - Walk: only displacement primitive.
  - Phase-2 gate: tiles at (4,5) and (10,5) sit on the only path through row 5; both must be crossed.
- **Witness** (14 actions, all `ACTION4`):
  ```
  [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
  ```
  Trace: t=1: R→(2,5). t=2: R→(3,5). t=3: R-attempt (4,5) phase-2-off-0; 3%2=1 → blocked. t=4: R-retry; 4%2=0 ✓ → move. t=5..8: R→(5..8,5). t=9: R-attempt (10,5)? No — (9,5) at t=9 first then (10,5) at t=10. Let me recount: t=5..9 = R into (5,5),(6,5),(7,5),(8,5),(9,5). t=10: R-attempt (10,5) phase-2-off-0; 10%2=0 ✓ → move. t=11..14: R→(11,5),(12,5),(13,5),(14,5)=goal. Win at t=14.
- **Difficulty justification**:
  - **(a) Random-resistance**: random uniform on `[1,2,3,4]` produces a 2D random walk on a 14×14 interior; expected first-passage to column 14 is O(width²). Budget 22 is far below O(14²)=196. Vision-blind agents have no signal to bias toward right; near-zero solve probability.
  - **(b) Human-tractable**: ~1 minute. Two pulsing tiles teach the rule fast; bounce-on-blocked is unmissable.
  - **(c) Planning depth**: near-zero — mechanic discovery is the difficulty. Greedy "always R" with implicit-bounce-tick wins.
  - **(d) Step budget**: 22 (witness 14, slack 8 = 57%). Generous.

### Level 2 — base system + 1 new mechanic

Layout:
- Wall ring.
- Avatar at (1,5). Goal at (14,5).
- Phase-2 (offset 0) at (4,5).
- Phase-3 (offset 1) at (8,5) — open at `t % 3 == 1`.
- Phase-2 (offset 0) at (12,5).

Step budget: 30.

- **Mechanics required by the witness** (N+1 = 3): adds 1 new.
  1. Avatar walk *(carried)*.
  2. Phase-2 gate *(carried)*.
  3. **Phase-3 gate** *(NEW)* — phase-3 tile walkable iff `step % 3 == offset`. Up to 2 retries per crossing.
- **Necessity per mechanic**:
  - Walk: as L1.
  - Phase-2 gate: required at (4,5) and (12,5).
  - Phase-3 gate: required at (8,5) — only path between the two phase-2 tiles.
- **Witness** (16 actions, all `ACTION4`):
  ```
  [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
  ```
  Trace: t=1: R→(2,5). t=2: R→(3,5). t=3: R-blocked (4,5) (3%2=1). t=4: R (4,5) (4%2=0 ✓). t=5..7: R→(5,5),(6,5),(7,5). t=8: R-attempt (8,5) phase-3-off-1; 8%3=2 → blocked. t=9: R-retry; 9%3=0 → blocked. t=10: R-retry; 10%3=1 ✓ → move. t=11..13: R→(9,5),(10,5),(11,5). t=14: R-attempt (12,5) phase-2-off-0; 14%2=0 ✓ → move. t=15: R→(13,5). t=16: R→(14,5)=goal.
- **Difficulty justification**:
  - **(a) Random-resistance**: random on [1,2,3,4] in 14×14 interior; same argument as L1 but harder due to 3-period gating making ineffective-action proportion higher.
  - **(b) Human-tractable**: ~2 minutes. Magenta phase-3 tile pulses 3× slower than blue phase-2 — visually distinct cycling rate.
  - **(c) Planning depth — NON-TRIVIAL**: per-step reasoning chain: at each cell along the witness path, the player must (1) identify the next phase tile by colour, (2) compute its period and offset by observing the pulse, (3) compute their arrival step from the current step + cells-to-tile, (4) decide whether direct walk lands on `t%n==offset` and if not, accept N-1 worth of in-place retries. Why no single-step heuristic wins: spam-the-new-verb fails because there's no verb beyond walk; "follow the colour" fails because the *same* colour (magenta) means *different* open-residues at different cells (offsets vary); a 1-action lookup table fails because every action's correctness depends on `step_counter mod {2,3}` AND the next-tile residue. The reasoning chain is "I am at column k step t; my next phase-tile is at column k+d offset o period p; my arrival is step t+d; if (t+d)%p == o, walk; else implicitly-wait by retrying at the cell-before-the-tile until residue matches; budget the retries."
  - **(d) Step budget**: 30 (witness 16, slack 14 = 87%). Generous; accommodates a first-time player needing several actions to discover the period-3 rule.

### Level 3 — system + 2 new mechanics

Layout:
- Wall ring.
- Avatar at (1,1). Goal at (10,14).
- Walls at row 2 (cells (2,2) through (13,2)) — EXCEPT cells (1,2) and (10,2) which are open. Forces the row-1 corridor to extend right to (10,1) before the avatar can drop south.
- Walls at (9,3..11) and (11,3..11) bracket the col-10 corridor on both sides; col-10 itself is open from (10,2) down to (10,14).
- Phase-2 (offset 0) at (4,1).
- Phase-3 (offset 1) at (9,1).
- Phase-4 (offset 1) at (10,5) — open at `t % 4 == 1`.
- **Fragile phase-3** (offset 0) at (10,12) — period-3 rule + on the FIRST blocked attempt, the cell becomes permanently `fragile_locked` (rendered with a darker frame), making L3 unsolvable from then on. The fragile rule forces the player to plan exact residue at this cell, not retry-in-place.
- All other interior cells open floor.

Step budget: 40.

- **Mechanics required by the witness** (= L2-count + 2 = 5):
  1. Avatar walk *(carried)*.
  2. Phase-2 gate *(carried)*.
  3. Phase-3 gate *(carried)*.
  4. **Phase-4 gate** *(NEW)* — phase-4 tile walkable iff `step % 4 == offset`. Up to 3 retries per crossing.
  5. **Fragile phase-3** *(NEW)* — a phase-3 tile with the additional rule that the first blocked attempt locks it permanently closed. Forces the player to reason about cumulative residue at this cell — retry-in-place is forbidden, so the upstream phase-tile retry counts must add up to a residue the fragile cell accepts on first try.

- **Necessity per mechanic**:
  - Walk: as L1/L2.
  - Phase-2-(4,1): on the row-1 corridor; cannot be bypassed.
  - Phase-3-(9,1): on the row-1 corridor; cannot be bypassed.
  - Phase-4-(10,5): on the col-10 corridor (the only southbound path through the row-2 wall gap at (10,2)); cannot be bypassed.
  - Fragile phase-3-(10,12): the only floor cell connecting the upper col-10 corridor to the bottom-row goal-bound segment. Cannot be bypassed AND cannot be retried — must align first try.
  
- **Witness** (26 actions):
  ```
  R R R R R R R R R R R D D D D D D D D D D D D D D D
  ```
  Concrete trace:
  - t=1: R→(2,1). t=2: R→(3,1).
  - t=3: R-attempt (4,1) phase-2-off-0; 3%2=1 → blocked.
  - t=4: R-retry; 4%2=0 ✓ → move. (4,1) at t=4.
  - t=5..8: R→(5..8,1).
  - t=9: R-attempt (9,1) phase-3-off-1; 9%3=0 → blocked.
  - t=10: R-retry; 10%3=1 ✓ → move. (9,1) at t=10.
  - t=11: R→(10,1).
  - t=12: D→(10,2). (Floor, gap in row-2 wall.)
  - t=13: D→(10,3). t=14: D→(10,4).
  - t=15: D-attempt (10,5) phase-4-off-1; 15%4=3 → blocked.
  - t=16: D-retry; 16%4=0 → blocked.
  - t=17: D-retry; 17%4=1 ✓ → move. (10,5) at t=17.
  - t=18..23: D→(10,6..11).
  - t=24: D-attempt (10,12) FRAGILE-PHASE-3-OFF-0; 24%3=0 ✓ → move ON FIRST TRY. (10,12) at t=24. (Critical — any first-attempt residue ≠ 0 here would lock the cell and lose the level.)
  - t=25: D→(10,13). t=26: D→(10,14)=goal. WIN.

- **Witness exercises every mechanic**:
  - Walk: every step.
  - Phase-2: t=4.
  - Phase-3: t=10.
  - Phase-4: t=17 (with 2 retries at t=15, 16 contributing to phase-4 gate exercise).
  - Fragile phase-3: t=24 (first-attempt success, demonstrating the rule's necessity-by-strict-residue).

- **Difficulty justification**:
  - **(a) Random-resistance**: random on `[1,2,3,4]` would (with overwhelming probability) trigger the fragile-strike on (10,12) within its first few exploration loops, locking the level. P(survive 50,000 random steps) ≈ 0; budget 40. Vision-blind agents will misidentify the fragile cell from the regular phase-3 cell (only the chevron palette-8 mark distinguishes them) and lose immediately.
  - **(b) Human-tractable**: ~3 minutes. The new phase-4 colour (orange, 4× cycle) and the fragile chevron (red mark on a magenta tile) are visually distinguishable. A human player who first attempts (10,12) at the wrong residue loses ONCE; the lose-then-retry-from-L3-restart loop is the discovery mechanic for the fragile rule. Once known, the residue computation is straightforward arithmetic.
  - **(c) Planning depth — STRICTLY DEEPER than L2**: the witness requires sequencing where ORDER of actions matters. **Trivial heuristic that fails**: the L2-winning strategy "walk forward, retry-in-place on every blocked phase tile" fails at L3 because retry-in-place at the fragile (10,12) cell is *forbidden* — the first blocked attempt is fatal. An LLM that learned "retry on block" from L1/L2 must update its policy to "compute residue before attempting the fragile cell." **Witness-pair commute test**: swap witness actions at indices 11 (R into (10,1)) and 12 (D into (10,2)). After swap: action at index 11 = D from (9,1) attempting (9,2) — (9,2) is wall → blocked, step 11 ticks, avatar stays at (9,1); action at index 12 = R from (9,1) → (10,1) succeeds at step 12. Now (10,1) at t=12 (vs t=11 in original). Step 13 D → (10,2) at t=13. Step 14..16 D → (10,3..5)? Phase-4-(10,5) attempt at t=16; 16%4=0 → blocked. t=17 retry: 17%4=1 ✓. (10,5) at t=17. (Same as original.) Continue D 7 cells to (10,12): attempt at t=17+7=24; 24%3=0 ✓. (Same.) WIN at t=26 (same total). **However**, swap at indices 12 and 13 (the D into (10,2) and the next D into (10,3)) breaks differently: at index 12, R (instead of original D) from (10,1) attempts (11,1); (11,1) is floor — succeeds! Avatar at (11,1) at t=12. Then index 13 D from (11,1) attempts (11,2); (11,2) is wall → blocked, step ticks. Subsequent witness actions assume avatar is on col-10, but it's stuck at col-11; no path to (10,12) from (11,*) within budget (interior walls bracket col-10 specifically). LEVEL UNSOLVABLE. Thus, witness actions 12 and 13 do NOT commute — order matters.
  - **(d) Step budget**: 40 (witness 26, slack 14 = 54%). Generous over the witness; the slack accommodates one mis-timed phase-4 (3 extra retries) or a few exploratory wall-bumps. Does NOT shrink relative to witness as level number rises (L1: 14/22 = 64%; L2: 16/30 = 53%; L3: 26/40 = 65%) — proportions are in same range.

## 5. Action mapping

`available_actions = [1, 2, 3, 4]`.

- **ACTION1 (UP)**: attempt to move avatar to (x, y-1).
- **ACTION2 (DOWN)**: attempt to move avatar to (x, y+1).
- **ACTION3 (LEFT)**: attempt to move avatar to (x-1, y).
- **ACTION4 (RIGHT)**: attempt to move avatar to (x+1, y).

A move "attempt" is processed as:
1. Compute destination cell.
2. If destination is out-of-grid OR a wall sprite OR a closed phase tile: REJECT (avatar stays). Step counter still increments.
3. Else if destination is goal: succeed, increment counter, fire `next_level()`.
4. Else: succeed (avatar moves), increment counter.

For the L3 fragile cell: a REJECTED move (case 2) onto a fragile-phase-3 tile triggers `fragile_strike(cell)` which permanently changes the cell's mode to `fragile_locked` (visually shown). Subsequent attempts always reject.

No ACTION5, ACTION6, ACTION7. No click. The "wait" verb is implicit (any blocked move advances the counter without moving).

## 6. HUD and per-game state

**HUD widgets** (`RenderableUserDisplay` subclasses):
- **`StepCounterHud`** — depleting horizontal bar at row 63 (bottom of frame). Two-colour: filled (palette 11 yellow) for `current_steps / max_steps` proportion; empty (palette 4 off-black) for the rest. Universal idiom from cached patterns. Updated each `step()`.

(No other HUD; the periodicity is communicated via the phase-tile sprite swaps, not via a separate widget.)

**Per-game internal state** (instance attributes on `Fz5j`):
- `_step_counter`: int, ticks from 0; equals `self._action_count` (engine-managed).
- `_phase_offsets`: `dict[str, int]` mapping phase-tile sprite name → its offset (loaded in `on_set_level`).
- `_fragile_locked`: `set[str]` of fragile-tile sprite names already struck.
- `_step_counter_hud`: `StepCounterHud` instance.

**Per-tile rendering update**: each `step()`, after the action is processed, walk all phase-tile sprites in the level. For each tile, compute `is_open = (counter % period == offset)` (using period from tag, offset from `_phase_offsets`, counter from current `_step_counter`). For each tile, `set_interaction(TANGIBLE)` for the closed-variant pixel buffer or the open-variant pixel buffer using the two-sprite-swap idiom (per `code/universal-scaffold.md` § Two-sprite swap: both variants pre-placed at same position; flip `InteractionMode` between TANGIBLE/REMOVED). Fragile tiles already in `_fragile_locked` always render as `fragile_locked` regardless of phase.

## 7. Win condition

`self.next_level()` fires when, after a successful move, the avatar's position equals the goal sprite's position (cell-equal). After L3's `next_level()` is called, the engine auto-fires `self.win()`.

## 8. Lose condition

`self.lose()` fires when EITHER:
1. The step counter reaches `max_steps` (per-level via `level.get_data("step_budget")`).
2. (L3 only) The fragile cell is in `_fragile_locked` AND the avatar is on the wrong side of it (column 10 row < 12) — no path to goal, level unsolvable. Detected by a simple post-strike reachability check: if no path exists from avatar position to goal within 4-connected open cells given the current `_fragile_locked` set, fire `lose()`.

## 9. Novelty note

### vs `taxonomy-of-25-games.md`

**tu93 (lockstep-multi-maze)**: closest taxonomy match by surface ("walk in maze with time advancing"). DISTINGUISHING RULE: tu93's antagonists are *mobile sprites* following AI (zzuxulcort/natiyqayts/vllvfeggte); fz5j has no second agent and no AI — the antagonists are *stationary cells* whose `is_open(t)` predicate flips on a global counter modulo a per-cell period. tu93 win = every primary-agent on its exit (multi-agent); fz5j win = single avatar on goal. tu93 primary verb = direction-press moves ALL primaries in lockstep; fz5j primary verb = direction-press moves single avatar.

**g50t (walk-vs-scroll)**: both have a turn-counter pressure beyond plain step budget. DISTINGUISHING RULE: g50t's pressure is a uniformly scrolling background — the world slides one cell every two turns. fz5j has no scrolling and no race; fz5j's pressure is per-cell phase, not global motion.

**dc22 (colour-cycle-walk)**: both have cells changing state. DISTINGUISHING RULE: dc22's cycler triggers fire ONLY when the player steps on a trigger (event-driven). fz5j's tiles change state autonomously every step on a deterministic period regardless of player action.

**ls20 (cycler-attribute-match)**: both involve "cycle" sprites. DISTINGUISHING RULE: ls20 cycles the avatar's attributes (shape/colour/rotation indices); fz5j has no avatar attributes; the avatar is a fixed entity, the tiles mutate.

**wa30 (lock-drag-crate)**: same pure-arrow action palette `[1,2,3,4]` (fz5j drops the [5] from wa30). DISTINGUISHING RULE: wa30's gameplay revolves around carrier-pickup-deliver (passenger tethered to carrier); fz5j has no pickup, no tether — single avatar walks alone; instead of mutating sprite-pickup state, fz5j mutates cell-phase-state.

**tr87 (symbol-cycle-rules)**: same pure-arrow palette. DISTINGUISHING RULE: tr87 cycles sprite-symbols on a tape and matches rules; fz5j has no rules, no tape, no sprite-symbol cycling — temporal cell openness is a different mechanic entirely.

### vs `prior-games/index.md`

**kx14 (tide-tilt-buoyant)**: both have time/state on a fluid axis. DISTINGUISHING RULE: kx14 simulates a continuous water surface and balls floating on it (physics simulation); fz5j has discrete cell-phase pulsing — no fluid, no buoyancy.

**lq5x (lantern-cone-illuminate)**: spatial-directional projection. DISTINGUISHING RULE: lq5x's cone is a *spatial directional* mechanic ("where am I aiming?"); fz5j is *temporal phase* ("when am I arriving?"). Different player thought-shape.

**vn8d (domino-cascade-topple)**: temporal sequencing. DISTINGUISHING RULE: vn8d is single-click-then-watch chain reaction; fz5j is move-by-move walk.

**pj7k (rolling-cube-face-paint)**: hidden-state-per-entity. DISTINGUISHING RULE: pj7k's cube has a 6-face rotation index attached to the entity; fz5j has zero per-entity hidden state — phase is a function of (cell, step counter) only.

**kf42 (tether-pawn-cycle), qz73 (radial-cycle-lock), qb84 (bead-lift-swap), gv47 (seed-grow-surround-dissolve), hr8q (pair-blend-recipe), ng52 (multiset-signature-classify), pz4t (anchor-pivot-place)**: none share core dynamic. Verified via negative-similarity-check in `mechanic-pick.md`.

### Negative-similarity recap

Negative test (per `mechanic-pick.md`): closest prior tu93 shares at most 2 of 8 dimensions (coarse "small grid + maze" + "internal pixel pattern"); below the 3-threshold. No prior overlaps on the heavy dimensions 6/7/8 (visual signature, pixel grain, core dynamic). NOVEL.
