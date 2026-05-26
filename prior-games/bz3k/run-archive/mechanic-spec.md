# Mechanic Spec — `bz3k` (revision 1)

**Revision marker.** This spec is revision 2. Round-1 critique
addressed via revision 1 (changes detailed in earlier marker).
Round-2 critique flagged a residual vy-bypass in L3 between the
wall column at x=32 and the cap-band at x=28; revision 2 closes
it by redesigning L3 as a 1-cell-tall horizontal corridor (only
y=32 is playable). Sections changed in revision 2: §4 Level 3
Layout, Necessity (M2, M3 paragraph). Witness arithmetic
unchanged.

## 1. Title
Drift-Impulse Cardinal (working title; not visible in-game).

## 2. Mechanic family
A single avatar carries persistent integer cardinal velocity
`(vx, vy)` that survives between turns. Each arrow press applies a
±1 impulse to the matching velocity component, then the avatar
slides — first horizontally by `vx` cells, then vertically by `vy`
cells — with collision handling per-axis. Targets latch only on
**speed-zero arrival** (vx == vy == 0 in the target cell). Two
interacting tile types refine the mechanic in later levels.

**Core knowledge priors used:** primarily *physics* (intuitive
inertia and momentum conservation; collision-and-stop), with
secondary *objectness* and *geometry*. No agentness; no acquired
symbolic knowledge.

## 3. Sprite roster

The grid is 64×64 (no camera scaling; 1 cell = 1 display pixel).
Sprites are designed at the display-pixel resolution per checklist
item 20.

**Logical vs. visual size.** Each gameplay element (avatar, cap,
flipper, target, hazard cell) has a single-cell *logical*
position used for game-logic checks (collision, cap/flipper/target
overlap, hazard contact). The *visual* footprint of each sprite
may span multiple cells around that logical centre to provide
internal pixel detail. The implementation uses the avatar's
logical centre cell to evaluate cap/flipper/target/hazard
overlaps, not the full visual bounding box. This keeps the
"single-cell chokepoint" geometry of §4 internally consistent
with checklist-20-compliant multi-pixel sprite visuals.

- **`player`** (5×5; palette 12 orange body, palette 4 off-black
  outline + 1 internal palette-2 light-grey speck on upper-left
  corner): the avatar. Asymmetric blob (the upper-left speck
  breaks rotational symmetry so the player can read orientation
  from the avatar alone). 1-pixel off-black outline. Tags:
  `["player"]`. Layer 3.
- **`wall`** (variable rectangles; palette 4 off-black with
  palette 3 grey internal "brick" texture every 3 pixels):
  immovable collision walls. 8-pixel-thick borders + texture
  lines so the surface reads as a thick bricked frame. Tags:
  `["wall"]`. Layer 0.
- **`target`** (5×5; palette **11 yellow** ring around palette 0
  white centre + four palette-11 yellow corner pixels): the
  destination. Hollow ring shape. (Yellow chosen to avoid the
  green-means-go cultural convention; the hollow-ring shape
  carries the "this is a destination" cue.) Tags: `["target"]`.
  Layer 1.
- **`hazard`** (5×5; palette **13 maroon** outer ring + palette
  4 off-black inner spike pattern — four inward-pointing dark
  triangles): a deadly tile. The spike SHAPE carries the "this
  hurts" cue through visual physical intuition; the maroon
  colour avoids the red-means-danger cultural convention. Tags:
  `["hazard"]`. Layer 2.
- **`cap_band`** (**1×1** single cell; palette 11 yellow body
  with palette 4 off-black 1-pixel border on top and bottom
  edges): velocity-cap tile. The "speed-bump" reading comes from
  placing multiple `cap_band` instances side-by-side to form a
  visible band. Tags: `["cap_band"]`. Layer 1.
- **`flipper_plate`** (5×5; palette 15 purple background with
  palette 6 magenta **bowtie** pattern — two facing equilateral
  triangles meeting tip-to-tip at the centre, the left-pointing
  triangle on the right half and the right-pointing triangle on
  the left half — and a palette-4 1-pixel border around the
  plate): velocity-reverser tile. The bowtie's "compress / pinch
  inward" geometry reads as "things passing through here get
  reversed". No straight diagonal lines forming an "X" or any
  other letter shape. Tags: `["flipper"]`. Layer 1.
- **`wake_pixel`** (1×1; palette 13 maroon): a single dim trail
  pixel. Visible-only (interaction=INTANGIBLE, collidable=False).
  See §6 for lifecycle. Tags: `["wake"]`. Layer 0.
- **`step_counter_hud`** + **`hud_velocity_dot`** (RenderableUserDisplay
  subclasses; not Sprites; see §6).

**Palette signature**: orange (12) + maroon (13) avatar + wake;
yellow (11) target + cap-band; purple (15) + magenta (6) flipper;
off-black (4) + grey (3) walls + hazard interior; near-white (0,
1) background. Wide range; dominant signature is
orange-on-near-white with yellow / purple accents — distinct from
prior `{4 wall, 8 red, 9 blue}` dominance.

## 4. Level progression, mechanic enumeration, and witness solutions

All three levels share `grid_size=(64, 64)`. Each level reuses the
sprite bank with different placements and per-level `level.data`;
`bz3k.on_set_level` re-initialises avatar position and `(vx, vy)`
from the level data.

### Level 1 — base dynamic system

**Layout.** Open arena bounded by `wall` on all four sides (walls
span `x ∈ [0, 7]`, `x ∈ [56, 63]`, `y ∈ [0, 7]`, `y ∈ [56, 63]`).
Player chamber is `[8, 56) × [8, 56)`. Single `target` sprite at
`(33, 32)`. Avatar starts at `(8, 32)` with `(vx, vy) = (0, 0)`.
Step budget: 30 actions.

**Mechanics required by the witness** (N = 1):
- **M1 = drift-impulse-with-speed-zero-target.** Each arrow press
  applies a ±1 impulse to one velocity component, then the
  avatar slides per-axis (horizontal by `vx`, then vertical by
  `vy`). Walls stop the avatar at the last legal cell and zero
  the matching velocity component. The target latches (firing
  `next_level()`) only when the avatar's centre enters the
  target cell with `vx == 0 AND vy == 0`.

**Necessity per mechanic:**
- *L1 cannot be solved without triggering M1* because the only
  way to leave the start cell is via an arrow press; arrow
  presses are defined to apply impulse + slide; and the target
  latch is gated on speed-zero arrival, which requires careful
  velocity management. Every legal action exercises M1.

**Witness solution** (10 actions):
```
[ACTION4 ×5, ACTION3 ×5]
```
Trace: → (vx=1, x=9). → (vx=2, x=11). → (vx=3, x=14). → (vx=4,
x=18). → (vx=5, x=23). ← (vx=4, x=27). ← (vx=3, x=30). ← (vx=2,
x=32). ← (vx=1, x=33). ← (vx=0, x=33). End: `(33, 32)` vx=0,
vy=0 → target latches.

**Difficulty justification:**
- (a) Random-resistance: a uniform-random arrow policy has near-
  zero probability of producing simultaneous vx=0 AND vy=0 at
  cell `(33, 32)` within 30 actions. A trivial spam-→ policy
  rams the east wall and never latches the target (target needs
  speed-zero entry, which spam-→ never produces because each
  press re-impulses).
- (b) Human-tractable: ~90 seconds.
- (c) Planning depth: no strict planning requirement — once the
  player understands "arrows are impulse and target wants speed
  zero", the symmetric ramp is near-immediate. L1 is the
  discovery gate.
- (d) Step budget: 30 actions (witness 10; ratio 3×).

### Level 2 — base system + 1 new mechanic

**Layout.** Same 64×64 arena. Internal wall column at `x = 32`,
`y ∈ [8, 31] ∪ [33, 56]` — leaves a 1-cell gap at `(32, 32)`. A
single `cap_band` instance at `(32, 32)` (1×1 cell; the gap
itself). `target` at `(56, 32)` — at the east wall. Avatar at
`(8, 32)` with `(vx, vy) = (0, 0)`. Step budget: 50 actions.

**Mechanics required by the witness** (N = 2; +1 over L1):
- **M1 = drift-impulse-with-speed-zero-target** (carried forward).
- **M2 = velocity-cap-band.** When the avatar's slide enters a
  `cap_band` cell during a per-axis slide, motion stops at that
  cell and the matching-axis velocity is clamped to magnitude 1
  (sign preserved): if entering during the horizontal slide,
  `vx ← sign(vx) · min(|vx|, 1)`; the perpendicular axis is
  unchanged. The remainder of the planned slide does not occur
  on this turn.

**Necessity per mechanic:**
- *L2 cannot be solved without triggering M1* because every
  motion is impulse-driven (no other action types are
  available); reaching `(56, 32)` from `(8, 32)` requires
  motion.
- *L2 cannot be solved without triggering M2* because the
  internal wall column at `x = 32` blocks every row except
  `y = 32`, and the only `y = 32` cell at `x = 32` is the
  `cap_band`. Every east-west traversal must pass through
  `(32, 32)` and triggers the cap clamp. There is no other gap
  in the wall column; vertical drift cannot bypass the wall
  (every cell at `x = 32, y ≠ 32` is solid wall).

**Witness solution** (13 actions):
```
[ACTION4 ×7, ACTION4 ×6]   (i.e., ACTION4 ×13)
```
Phase 1 (reach cap, 7 actions):
- → ×6: vx ramps 1, 2, 3, 4, 5, 6; cumulative position 9, 11,
  14, 18, 23, 29.
- → 7th: vx=7, planned slide +7 from x=29: 30, 31, 32 (CAP, vx
  clamps to 1, motion stops). End: `(32, 32)` vx=1.

Phase 2 (cap to target via east wall stop, 6 actions):
- → vx=2, x=34. → vx=3, x=37. → vx=4, x=41. → vx=5, x=46.
  → vx=6, x=52. → vx=7, planned slide +7 from x=52: 53, 54, 55,
  56 (target reached) — east wall starts at x=56? No: wall at
  `x ∈ [56, 63]`, so x=56 IS wall. Pawn stops at x=55? No: the
  wall cell at x=56 is solid; pawn moving from 55 towards 56
  cannot enter 56. So pawn stops at x=55, with vx zeroed by
  the wall.
  
  Wait — re-read the layout: target is *at* `(56, 32)`. If the
  wall starts at x=56, target is *inside* the wall. Mismatch.
  Fix: place the target at `(55, 32)` (the last interior cell)
  and pawn stops at x=55 via wall stop. Updating layout: target
  at **(55, 32)**, wall at `x ∈ [56, 63]`.

Recomputed phase 2:
- → vx=2, x=34. → vx=3, x=37. → vx=4, x=41. → vx=5, x=46.
  → vx=6, x=52. → vx=7, slide +7 from 52: 53, 54, 55 (would
  continue but wall at x=56 stops pawn at x=55, vx zeroed). End:
  `(55, 32)` vx=0. **TARGET LATCHES** (target at (55, 32)).

Total: 7 + 6 = 13 actions.

**Difficulty justification:**
- (a) Random-resistance: same axis-zero requirement at target;
  cap clamp introduces forced velocity reset. Random-uniform
  player has < 1% chance of achieving speed-zero target arrival
  within 50 actions.
- (b) Human-tractable: ~2 minutes.
- (c) **Planning depth (post-discovery, REVISED).**
  *(1) Decision space at L2 start*: 4 valid first actions
  (↑↓←→), all available. Only → makes meaningful eastward
  progress; ↑/↓ adds vy that the player must zero before target
  arrival, costing extra actions.
  *(2) Plausible-but-wrong post-discovery path*: a fully-
  informed player might apply L1's symmetric ramp post-cap —
  "ramp → 5 times to vx=6, then ← 5 times to decelerate". From
  `(32, 32)` vx=1, this gives: → vx=2 x=34, → vx=3 x=37,
  → vx=4 x=41, → vx=5 x=46, → vx=6 x=52; then ← vx=5 x=57 —
  but x=56 is wall, pawn stops at x=55 vx=0. The L1-symmetric
  strategy *coincidentally* lands at the target when the wall is
  at the target cell, but with an off-by-one risk: if the player
  ramps one step less (4 ramps), the deceleration overshoots
  the target before reaching the wall and requires extra
  recovery. The witness packs the ramp tighter (6 ramps, no
  decel) to reach the wall via direct overshoot; choosing
  between "decel-symmetric" and "ram-the-wall" is a real
  post-discovery decision.
  *(3) Witness reasoning chain*: pre-cap, the player must press
  → enough times that the next slide will reach exactly `x=32`
  (cap stops the avatar; over-ramp wastes actions but cap clamps
  anyway). Post-cap from vx=1, the player chooses between (a)
  ram-east-wall via 6 ×→ which terminates at x=55 vx=0 (wall-
  zero saves the deceleration phase), or (b) symmetric decel
  which would overshoot if not carefully tuned. The wall-stop
  shortcut requires the player to NOTICE that the target is at
  the wall cell and that wall-stop zeroes vx — non-trivial post-
  discovery insight.
- (d) Step budget: 50 actions (witness 13; ratio ~3.8×). Generous
  over the witness for exploration and recovery.

### Level 3 — system + 1 more new mechanic (REDESIGNED)

**Layout (REVISED for round 2).** 64×64 grid. The level uses a
**1-cell-tall horizontal corridor** at `y = 32`, `x ∈ [4, 60]`
(57 cells of playable corridor). Walls fill EVERY OTHER interior
cell: walls at `(x, y)` for all `4 ≤ x ≤ 60` and `4 ≤ y ≤ 60`
with `y ≠ 32`, plus the boundary walls at `x ∈ [0, 3]`,
`x ∈ [61, 63]`, `y ∈ [0, 3]`, `y ∈ [61, 63]`. Net effect: the
corridor is a 1-row tunnel; any vy-impulse hits the ceiling
wall (at `y = 31`) or floor wall (at `y = 33`) on the very next
vertical-slide phase, immediately zeroing vy. Velocity therefore
remains horizontal throughout the level by construction.

Inside the corridor:
- Single `cap_band` cell at `(28, 32)`.
- Single `flipper_plate` cell at `(38, 32)`.
- Hazard cells at `(44, 32), (45, 32), …, (55, 32)` — 12 hazard
  cells filling the corridor east of the flipper, so any
  eastward drift past the flipper enters hazard immediately.
- `target` at `(17, 32)`.
- Avatar at `(32, 32)` with `(vx, vy) = (6, 0)` (level data
  `{"avatar_start_vx": 6}`).

Step budget: **60 actions**.

**Mechanics required by the witness** (N = 3; +1 over L2):
- **M1 = drift-impulse-with-speed-zero-target** (carried forward).
- **M2 = velocity-cap-band** (carried forward).
- **M3 = velocity-flipper-plate.** When the avatar enters a
  `flipper_plate` cell during a per-axis slide, motion stops at
  that cell and BOTH `vx` and `vy` are negated. The remainder
  of the planned slide does not occur on this turn.

**Necessity per mechanic:**
- *L3 cannot be solved without triggering M1* because every
  motion is impulse-driven; the avatar starts non-stationary
  (vx=6) so the first turn's slide already exercises M1.
- *L3 cannot be solved without triggering M2* because the
  corridor at `y = 32` is the only playable row. Every cell at
  `y ≠ 32` is wall, so any vy-impulse hits the ceiling/floor
  wall on the same turn (vy zeroed at next vertical-slide
  phase). Therefore every position the avatar can occupy lies
  on the corridor; every east-west traversal at `x = 28`
  enters the single cap cell `(28, 32)` and triggers the cap
  clamp. There is no vy-routing detour available.
- *L3 cannot be solved without triggering M3* because: with
  initial vx=+6 and no other adjustments, applying ←-impulses
  alone to decelerate from vx=+6 to vx=0 takes 6 actions during
  which the avatar accumulates +5+4+3+2+1+0 = +15 cells of
  east drift, landing at `x = 32 + 15 = 47` — *inside the
  hazard wall* at `x ∈ [44, 60]`. Every alternate strategy that
  avoids the flipper either drifts into the hazard (because the
  east-west chamber is bounded by hazard at `x ≥ 44`) or fails
  to reverse direction (since pure ←-impulse decel cannot reach
  vx ≤ 0 before the avatar enters hazard). The flipper at
  `(38, 32)` is the unique way to reverse vx without east
  hazard contact.

  Vertical-axis routing is impossible by construction (the
  corridor is 1-cell-tall and walls flank the corridor above
  and below at every x; vy cannot persist).

**Witness solution** (10 actions):

Initial: `(32, 32) vx=+6, vy=0`.
1. **ACTION4** (→). vx 6→7. Per-axis horizontal slide +7 from
   `(32, 32)`: 33, 34, 35, 36, 37, 38 (FLIPPER triggers, motion
   stops; vx ← -7, vy ← 0). End: `(38, 32) vx=-7, vy=0`.
2. **ACTION4** (→). vx -7→-6. Slide -6 from `(38, 32)`: 37, 36,
   35, 34, 33, 32. Cap cells are at x=28, not yet reached.
   End: `(32, 32) vx=-6, vy=0`.
3. **ACTION4** (→). vx -6→-5. Planned slide -5 from `(32)`:
   31, 30, 29, 28 (CAP at (28, 32) triggers, vx clamps to -1,
   motion stops). End: `(28, 32) vx=-1, vy=0`.
4. **ACTION3** (←). vx -1→-2. Slide -2 from `(28)`: 27, 26.
   End: `(26, 32) vx=-2`.
5. **ACTION3** (←). vx -2→-3. Slide -3: 25, 24, 23.
   End: `(23, 32) vx=-3`.
6. **ACTION4** (→). vx -3→-2. Slide -2: 22, 21.
   End: `(21, 32) vx=-2`.
7. **ACTION4** (→). vx -2→-1. Slide -1: 20.
   End: `(20, 32) vx=-1`.
8. **ACTION3** (←). vx -1→-2. Slide -2: 19, 18.
   End: `(18, 32) vx=-2`.
9. **ACTION4** (→). vx -2→-1. Slide -1: 17.
   End: `(17, 32) vx=-1`. (At target cell but vx≠0; no latch.)
10. **ACTION4** (→). vx -1→0. Slide 0: stays.
    End: `(17, 32) vx=0, vy=0`. **TARGET LATCHES.**

Sequence: `→ → → ← ← → → ← → →` — 10 actions.

**Difficulty justification:**
- (a) Random-resistance: combination of forced eastward initial
  velocity + full-height hazard column + cap clamp + flipper-
  reverse + speed-zero-arrival means random-uniform play has
  effectively zero probability of avoiding hazard contact AND
  hitting flipper at the right cell AND landing speed-zero on
  the target. Estimated `P(win | random) << 1 / 10⁴`.
- (b) Human-tractable: ~3 minutes for an attentive human.
- (c) **Planning depth (post-discovery).**
  *(1) Decision space at L3 start*: 4 valid first actions; the
  meaningful choices are between → (push faster into flipper),
  ← (try to brake, drift into hazard), and ↑/↓ (try vy-routing,
  but the full-height hazard closes that detour at `x ≥ 44`).
  Post-discovery, the player must *recognise the geometry*: the
  hazard column is the load-bearing constraint that makes vy-
  routing useless and pure-decel fatal.
  *(2) Plausible-but-wrong post-discovery path*: a tempting
  greedy heuristic is "press ← to brake immediately, since the
  target is west". A fully-informed player who has played L1
  and L2 *knows* impulse-and-slide dynamics, *knows* the cap
  clamps, and *knows* the flipper exists; despite that
  knowledge, the temptation to "just brake" is strong because
  it's the most direct interpretation of "go west to the west
  target". The post-discovery player computes: "←-impulse
  brakes vx from +6 toward 0; that takes 6 presses; cumulative
  east drift = 15 cells; lands at x=47; that's INSIDE the
  hazard wall at x ∈ [44, 60]; lose." So the player must NOT
  greedy-brake — they must first commit to going FURTHER east
  (into the flipper) before reversing. This is a non-trivial
  reasoning chain post-discovery.
  *(3) Where the heuristic diverges from the witness*: the
  greedy-brake heuristic picks ← on action 1 (vx=5 after, x=37
  after slide). The witness picks → on action 1 (vx=7, hits
  flipper at x=38). On action 2: greedy picks ← again
  (vx=4, x=41 — getting closer to hazard). Witness already at
  flipper-result vx=-7 and now braking eastward. By action 3-4,
  greedy avatar is in the hazard zone and loses; witness is
  past the cap heading west.
  *Stage-conflation guard*: the greedy-brake failure is NOT a
  discovery-stage misstep. The post-discovery player understands
  every mechanic; their failure mode is mis-prioritising the
  spatial route, not mis-understanding the physics. They press
  ←-because-target-is-west despite knowing they'll drift +15
  east; the geometric arithmetic that "+15 east is fatal" is
  the actual planning challenge.
- (d) Step budget: **60 actions** (witness 10; ratio 6×).
  Generous over witness; does not shrink relative to L2 (50).

## 5. Action mapping

`available_actions = [1, 2, 3, 4]`. Click and ACTION5/7 are
absent — the entire game is cardinal-arrow only. ACTION7 is
omitted per checklist 22 (no undo verb in this game).

- `ACTION1` (UP): `vy -= 1`, then per-axis slide.
- `ACTION2` (DOWN): `vy += 1`, then per-axis slide.
- `ACTION3` (LEFT): `vx -= 1`, then per-axis slide.
- `ACTION4` (RIGHT): `vx += 1`, then per-axis slide.

**Per-axis slide rule (NEW, addresses critique issue 3).**
After each impulse, the avatar slides in two phases:
1. **Horizontal phase**: move by `sign(vx) · 1` cells, repeated
   `|vx|` times. At each one-cell step, check for wall (stop and
   `vx ← 0`), `cap_band` (stop at cap cell, `vx ← sign(vx) · 1`,
   abort remaining horizontal steps), `flipper` (stop at
   flipper, `vx ← -vx`, `vy ← -vy`, abort remaining horizontal
   steps), `hazard` (`self.lose()`, halt), or `target` (no
   action; target latch is checked at end-of-turn).
2. **Vertical phase**: same as horizontal, but applied to the
   y-axis with `sign(vy)` and `|vy|`.

Target latch is evaluated AFTER both phases complete: if the
avatar's `(x, y)` equals the target sprite's position AND
`vx == 0 AND vy == 0`, the engine fires `next_level()`.

No context-gating (`_get_valid_actions` returns parent default).

## 6. HUD and per-game state

Two `RenderableUserDisplay` subclasses:

- **`StepCounterHud`** — a horizontal depleting bar in row 63
  (palette 5 black drained, palette 14 green remaining). Width
  64; fills proportional to `current/max` of remaining steps.
- **`VelocityDotHud`** — a 4×4 patch in the top-right of the
  frame (rows 0..3, cols 60..63) that surfaces the current
  `(vx, vy)` reading. Renders `min(|vx|, 3)` palette-12 dots
  along the centre column of the patch (offset above or below
  centre by sign of vy... wait — vx along x-axis. Let me
  re-state). Renders `min(|vx|, 3)` palette-12 dots along the
  centre row of the patch, fanning left for vx<0, right for
  vx>0; renders `min(|vy|, 3)` palette-12 dots along the centre
  column, fanning up for vy<0, down for vy>0. The dots form a
  cross whose extents per axis correspond to velocity magnitude.

**`wake_pixel` lifecycle (NEW, addresses critique issue 10).**
Maintained as `self.wake_pixel_sprites: list[Sprite]`.

- **At the start of each `step()`**, before applying the
  impulse: remove every sprite in `self.wake_pixel_sprites` from
  the level via `level.remove_sprite(s)`. Clear the list.
- **After per-axis slide completes**, before
  `self.complete_action()`: compute the wake position. Wake
  fans out from the cell IMMEDIATELY behind the avatar's centre,
  opposite to the velocity vector, for `|vx| + |vy|` cells. For
  pure horizontal velocity (vy=0), wake is a horizontal line of
  `|vx|` cells at `y = avatar.y + 2` (centre of the 5×5 avatar)
  starting at `x = avatar.x + 2 - sign(vx)` and stepping by
  `-sign(vx)` each cell. For pure vertical velocity, mirror
  along y. For diagonal velocity, draw two separate trails
  along each axis (one per non-zero component). Each wake_pixel
  sprite is created with `interaction=InteractionMode.INTANGIBLE`
  and `collidable=False`, then added to the level via
  `level.add_sprite(s)` and appended to
  `self.wake_pixel_sprites`.

Internal per-game state:
- `self.vx: int`, `self.vy: int` — current velocity.
- `self.wake_pixel_sprites: list[Sprite]` — see lifecycle above.
- `self.player_sprite: Sprite` — direct handle to the avatar
  (updated each `on_set_level`).
- `self.hud_step_counter: StepCounterHud`,
  `self.hud_velocity_dot: VelocityDotHud` — HUD instances.

## 7. Win condition

Per-level: `(player.x, player.y) == (target.x, target.y)` AND
`self.vx == 0` AND `self.vy == 0`, evaluated at end-of-step
after the per-axis slide. Triggers `self.next_level()`.

Game-level: completing all 3 levels triggers `self.win()`.

## 8. Lose condition

Two predicates trigger `self.lose()`:
1. **Step budget exhausted.** `self._action_count >=
   level.get_data("step_budget")` and target not yet latched.
2. **Hazard contact.** During per-axis slide, the avatar enters
   a cell occupied by a `hazard` sprite.

There is no soft-lock lose condition.

## 9. Novelty note

### Closest taxonomy entries

- **m0r0 (mirror-orb-merge).** Distinguishing rule: m0r0 has
  2-4 mirrored orbs that move single-cell-per-action with mirror-
  axis transformations; bz3k has ONE avatar with cumulative
  multi-cell-per-action velocity that persists between actions.
  No mirroring, no quadrants, no second orb in bz3k.
- **tu93 (maze-pickup-train).** Distinguishing rule: tu93 has
  fixed-stride hop motion (3 pixels/turn, no momentum) along
  value-2 corridor cells with pickup-train mechanic; bz3k has
  free-arena cardinal-impulse drift with cumulative velocity
  and no pickup mechanic.

### Closest prior-game entries

- **wt39 (glide-deflect-thaw).** wt39 fires a one-shot glide per
  arrow press whose velocity resets to zero between actions;
  bz3k accumulates persistent two-axis velocity across actions.
  Two successive `→` in wt39 produce two separate east slides
  (each glide-until-wall); two successive `→` in bz3k produce
  one 3-cell slide with vx=2 after the second press.
- **tg6w (settle-pile-tilt).** tg6w gravity acts on every loose
  piece simultaneously, single-shot per arrow, no momentum
  accumulation; bz3k acts on a single avatar with per-axis
  velocity that persists.
- **kn58 (anchor-pull-magnet).** kn58 motion is anchor-induced,
  single-cell-per-click on multiple pawns; bz3k motion is arrow-
  thrust on a single avatar with cumulative-velocity effects.
- **vt6q (grapple-anchor-yank).** vt6q is single-shot grapple
  yanking with fixed magnitude; bz3k has no grapple verb. Yank-
  vs-drift dynamic is fundamentally different.
- **zd7m (cohort-step-route).** zd7m moves all pawns by exactly
  one cell per arrow press, no momentum. bz3k moves a single
  avatar by `|velocity|` cells per press with velocity
  persisting and growing.
- **kx14 (tide-tilt-buoyant).** Fluid-dynamics-flavoured (water
  level, buoyant balls) vs bz3k's rigid-body-momentum.
- **ek73 (wake-trail-evade) (NEW; addresses critique issue 11).**
  ek73's wake is a *gameplay hazard* — vacated cells become
  decaying hazards behind the player and the avatar must not
  re-enter them. bz3k's wake-pixel trail is *visual-only*
  (INTANGIBLE, non-collidable) — it surfaces velocity state for
  the player but has no gameplay role; the avatar can re-cross
  any cell freely. Different gameplay-role layer.
- **jd4q (echo-trail-teleport) (NEW; addresses critique issue
  11).** jd4q's trail is a *teleport interaction surface* —
  clicking an echo cell teleports the avatar back, consuming the
  trail. bz3k has no click action and no teleport semantics —
  wake pixels cannot be interacted with at all. Different verb
  set.

### Negative similarity check

Walking the 8 dimensions against the closest analogues:

| Dimension | vs wt39 | vs ek73 | vs jd4q |
|---|---|---|---|
| 1 (board) | both pawn+walls+targets | both pawn+walls+target | both pawn+walls+target |
| 2 (input) | DIFFERENT (one-shot glide vs. cumulative impulse) | DIFFERENT (walk vs. drift) | DIFFERENT (walk+click vs. drift) |
| 3 (level ask) | partially (target-reach; bz3k adds vx=0) | DIFFERENT (avoid wake hazard vs. reach target) | DIFFERENT (escape via teleport vs. reach target) |
| 4 (kill) | both step-budget | hazard wake vs. hazard wall | step budget |
| 5 (cast) | DIFFERENT (bumpers/thaw vs. cap/flipper/wake) | DIFFERENT (decaying-hazard wake vs. visual wake) | DIFFERENT |
| 6 (visual signature) | DIFFERENT (wake-trail unique to bz3k) | partially shared (both have trails) — but ek73's wake is hazard-coloured, bz3k's is dim maroon | partially shared |
| 7 (sprite grain) | DIFFERENT | DIFFERENT | DIFFERENT |
| 8 (core dynamic) | DIFFERENT (FUNDAMENTALLY) | DIFFERENT (FUNDAMENTALLY) | DIFFERENT (FUNDAMENTALLY) |

Sharing-count for each: vs wt39 = 1 + partial; vs ek73 = 1 +
partial dim 6; vs jd4q = 1 + partial dim 6. All below the 3+
rejection threshold on heavy axes. Heaviest dimension (8 — core
dynamic) differs against ALL.

Verdict: **NOVEL** vs both 25-game taxonomy and the 60-entry
prior-games index.
