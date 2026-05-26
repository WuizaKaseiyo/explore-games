# Pendulum-Sync-Rail

*(Replaces `heat-diffuse-equilibrium.md`. Real-world inspiration:
Galileo's coupled-pendulum experiments, Huygens' synchronisation of
two clocks resting on the same beam. Side view, kinetic.)*

## Summary

A wooden **rail** runs horizontally across the playfield. Three to
five **pendulums** hang from the rail at fixed pivot points; each
pendulum is a thin pixel rope ending in a coloured bob. Each
pendulum has a **phase** in `{-2, -1, 0, +1, +2}` (left swing →
centre → right swing); on every tick the phase progresses one step
through the cyclic sequence `-2 → -1 → 0 → +1 → +2 → +1 → 0 → -1 →
-2 → …`. The bob's *visible position* is the phase value.

The player's verb is **push**: ACTION6 click on a pendulum bob shoves
it forward by one phase step (advances its position in the cycle).
Ticks are commanded by ACTION5. The level wins when the live phase
pattern matches the level's target signature at the END of any tick.

## Visual elements (distinct from prior corpus)

- 64×64 canvas oriented as a **side view**: the rail is a 1-pixel-tall
  wood-brown line at row 12; pendulums hang downward into the lower
  3/4 of the canvas. The full corpus has zero side-view games — this
  alone breaks visual sameness.
- Each pendulum is rendered as:
  - a **rope** of stippled grey pixels from the pivot down to the
    bob, drawn at the angle implied by the current phase (so phase
    `-2` shows the rope swept ~30° to the left, phase `+2` ~30° to
    the right);
  - a 3×3 **bob** in the pendulum's own colour (one per pendulum:
    e.g. crimson, ochre, teal, navy, plum).
- Below the playfield, a **phase-meter strip** shows each pendulum's
  current phase as a 1-pixel pip on a 5-cell scale. The level's
  target is shown as **outlined** pips on the same strip — so the
  player can read at-a-glance "how far each pendulum is from
  target". The strip is 1 pixel tall per pendulum.
- L2 introduces **rail couplings**: pendulums sharing a rail segment
  are linked by a small dot rendered on the rail between their
  pivots. This is the visual cue that they will phase-pull each
  other.
- L3 introduces:
  - **Heavy bob**: rendered as a 3×3 bob with a bold black outline.
    Pushing this bob takes 2 clicks to advance 1 phase.
  - **Damper clip**: rendered as a small grey C-bracket on the
    pendulum's rope. Clicking ACTION6 on a pendulum **with a
    bracket present** clips it (the bracket closes onto the rope)
    and freezes the pendulum's phase forever. Clipping costs 3
    actions but removes the pendulum from rail coupling.
- A small **tick counter** sits along the bottom rim — small dark
  notches accumulate one per ACTION5 press, capped by the level
  budget.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION5 | Advance the simulation by one tick. Every non-clipped pendulum's phase progresses through the sequence (with rail-coupling adjustment on L2+). | always |
| ACTION6 | Click a pendulum bob to push: heavy bobs need 2 clicks for 1 phase shift; on L3 if the pendulum has a damper clip, this instead clips it (3 step cost). Clicks on rope or rail without a bob are no-ops. | always; clicks off bob = no-op, no step. |

`available_actions = [5, 6]`.

## Mechanics enumeration

- **M1 — phase tick:** ACTION5 advances every pendulum's phase by
  one position in the cycle `[-2, -1, 0, +1, +2, +1, 0, -1]`
  (period 8). Phases are computed in parallel from the previous
  tick.
- **M2 — push:** ACTION6 click on a non-heavy bob advances the
  phase by one position in the same cycle (does not advance time).
- **M3 — match-target:** the win predicate compares each
  pendulum's current phase to the level's target phase. All must
  match at the end of a tick.
- **M4 — rail coupling (level 2+):** pendulums on the same rail
  segment apply mutual phase-pull every ACTION5 tick. After the
  default phase advance, each coupled pendulum shifts its phase
  +1 toward its neighbour's phase if they differ by ≥ 2 (capped
  to one position per tick). Multiple neighbours: the largest
  pull wins (ties go in pendulum-index order). Couplings are
  fixed by level data — the rail is segmented so some adjacent
  pendulums are coupled and others are not.
- **M5 — heavy bob (level 3+):** a heavy bob requires two clicks
  to advance one phase position. Internal counter `heavy_charge ∈
  {0, 1}`; clicks add 1 mod 2; on transition 1→0 the phase
  advances. (Tracked per heavy bob.)
- **M6 — damper clip (level 3+):** if a pendulum has a `clip_
  available: true`, ACTION6 click on it (after one push setup
  click as a "warning" frame to prevent misclicks) clips the
  pendulum: phase frozen forever, removed from rail coupling,
  cost 3 steps. Clipping is irreversible. Visualised by closing
  the C-bracket onto the rope.

## Per-level progression

### Level 1 — base sync (M1 + M2 + M3)
- 3 pendulums on a single straight rail (fully decoupled — coupling
  is M4, not yet active). Target: all three at phase `0` (centred)
  at the end of some tick.
- Initial phases are `(-2, +1, +2)`. Through ticks, they evolve as
  `(-1, +2, +1)`, `(0, +1, 0)`, `(+1, 0, -1)`, …
  Without pushing, they never align. The player must push each
  pendulum the right number of times to sync.
- **Witness:** push pendulum-1 once, pendulum-3 twice in any
  order, then ACTION5 ticks until all three are 0 simultaneously.
  ~7 actions.
- **Mechanics required:** M1, M2, M3.

### Level 2 — + M4 (rail coupling)
- 4 pendulums on TWO rail segments (segment A holds pendulums 1,2;
  segment B holds 3,4). Couplings drag adjacent phases together.
- Target: pendulum-1 at phase `+2`, pendulum-2 at `-2`, pendulum-3
  and 4 both at `0`. The L1 strategy of "push each independently"
  fails because pendulum-1 and 2 are coupled — pushing 1 to `+2`
  drags 2 toward `+2` not `-2`.
- The player must use the *coupling itself* by pushing pendulum-2
  to a phase that, after the next tick's coupling pull, ends up
  at `-2` — i.e. plan around the pull.
- **Witness:** specific 12-action sequence interleaving pushes and
  ticks. Step budget 22.
- **Mechanics required:** M1, M2, M3, M4.

### Level 3 — + M5 (heavy) + M6 (damper)
- 5 pendulums on three rail segments (segment A: 1,2,3; segment B:
  4; segment C: 5). Pendulum-3 is heavy; pendulum-2 has a damper
  clip available.
- Target: phases `(+2, +1, 0, 0, -2)` at the chime tick (level
  data).
- The chime tick is fixed at tick 14 — the player has exactly 14
  ticks of simulation budget plus a click budget. Heavy pendulum-3
  on the centre of segment A drags 1 and 2 each tick; if the
  player clips pendulum-2 at the right moment, it frees pendulum-1
  from the chain and the heavy can be pushed solo.
- **Witness:** ~28 actions including 1 clip and several heavy
  double-pushes.
- **Mechanics required:** M1, M2, M3, M4, M5, M6.

## Win condition

After every ACTION5 tick (and after ACTION6 pushes that change
phase), check each pendulum's phase against the target. If all
match (and on L3 the chime tick is reached or already passed with
a still-matching state), fire `self.next_level()`.

## Lose condition

`steps_used >= max_steps` triggers `self.lose()`. On L3, missing
the chime tick at `tick == chime_tick` with a non-matching state
also fires `self.lose()` (no second chime).

## Internal state

- `self.pendulums: list[Pendulum]` — `colour`, `pivot_x`,
  `pivot_y`, `phase: int`, `phase_seq_index: int` (0–7),
  `heavy: bool`, `heavy_charge: int`, `clip_available: bool`,
  `clipped: bool`, `rail_segment: int`.
- `self.rail_segments: list[set[int]]` — pendulum indices per
  segment.
- `self.target_phase: list[int]`.
- `self.tick: int`.
- `self.chime_tick: int | None` (L3).
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus

- **vs `gg09 — gear-mesh-spin`**: gear-mesh propagates rotation
  through a graph at one click per turn (counter-rotation rule).
  Pendulum-sync uses a *time-cycling* phase per pendulum that
  advances on every tick — and rail coupling is an *additive*
  mutual phase-pull, not a binary gear-mesh.
- **vs `qz73 — radial-cycle-lock`**: radial-cycle-lock has tips
  cycling around a ring on ACTION5; the player toggles per-tip
  locks. Pendulum-sync's phase is a sinusoidal cycle, not a
  rotation, and rail coupling is *mutual* — you cannot solve
  pendulum-sync by locking one tip at a time.
- **vs `kx14 — tide-tilt-buoyant`**: kx14 is a buoyant-balls
  fluid tank (vertical fluid level + lateral tilt). Pendulums
  swing on independent timing cycles and couple only via shared
  rails — different physics, different visual register.

## Step budget

- L1: 14.
- L2: 30.
- L3: 60.

## Random-resistance

Random pushing toggles random pendulum phases by ±1; with 5
pendulums the chance of all matching the target at any one tick
is `1/8^5 ≈ 1/32768` per tick. Random play essentially never
solves L3 even given full budget. The damper clip in particular
is a one-shot strategic decision.

## Planning depth

- **L1:** moderate — count cycles forward to find a tick when
  all three pendulums happen to coincide.
- **L2:** deep — coupling means phase pushes propagate; the
  player must reason about the *delta* between coupled phases
  before/after each tick.
- **L3:** very deep — heavy bobs reduce the per-step efficiency,
  and the damper clip is a one-way decision that decouples a
  pendulum from the chain. The player must decide when (or
  whether) to clip given the chime tick is fixed.
