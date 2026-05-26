# Wavefront-Ring-Expand

## Summary

The grid has a single **emitter sprite** that the player relocates
by clicking. Pressing ACTION5 emits a **wave**: a ring of "wave
cells" that expands outward by exactly 1 cell of Chebyshev radius
per ACTION5 tick. Multiple waves can be in flight at once (each
emitted by an ACTION5 press). Waves stop when their radius equals
the per-level **wave reach** R or when every cell on their
current ring is blocked by a wall.

Each cell on the wave's ring **flips the state of every switch
cell it touches** that turn. Switch cells have two states (off /
on); flipping toggles them. Walls block a wave cell from
propagating beyond — but the wave still exists in unblocked
arcs of the ring.

The level wins when every switch is in its required state AT THE
END of the most recent action. The only failure mode is
exhausting the per-level step counter.

## Visual elements

- 12×12 inner grid with pale-grey floor.
- The **emitter** is a small 2×2 dark-purple cross sprite.
- **Wave cells** render as bright-yellow 1-pixel cells along the
  current ring. They live for ONE turn — the next ACTION5
  expands them outward, leaving the previous ring as cleared.
- **Switches** are 1×1 cells with a binary visual: dark-grey
  outline = off, saturated colour = on. Each switch carries a
  required-colour ring around it indicating its target state.
- **Walls** are solid black 1×1 cells.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION5 | Tick the simulation by one frame. Every in-flight wave's ring expands by Chebyshev radius +1; switches whose cell intersects the new ring toggle state. Waves whose radius reached the per-level reach R disappear after this tick. | always |
| ACTION6 | Click cell `(x, y)`. If the clicked cell is empty (no wall, no switch), the emitter relocates there AND immediately emits a new wave starting at radius 0 (the emitter cell itself, no flips). If the clicked cell is a wall or switch, no-op. | always |

`available_actions = [5, 6]`. No avatar.

## Mechanics enumeration

- **M1 — emit-wave:** ACTION6 click on an empty cell relocates
  the emitter and starts a new wave there.
- **M2 — wave-tick-expand:** ACTION5 advances every active wave
  by one Chebyshev radius. The new ring is the set of cells at
  Chebyshev distance R from the wave's source where R is the
  pre-tick radius + 1.
- **M3 — switch-flip:** every wave cell that lands on a switch
  cell toggles that switch's state.
- **M4 — wall-block:** a wave cell that would expand into a
  wall cell is suppressed — that arc of the ring is "cut." The
  rest of the ring continues unaffected. (Note: this means
  walls do NOT cast a shadow on cells beyond — the wave
  re-fills the cone behind a wall on subsequent ticks. This
  makes the rule local and cleanly implementable.)
- **M5 — wave-reach-limit (level 2+):** each wave has a
  per-level maximum radius R; after expanding to R the wave
  disappears (no further flips).
- **M6 — toggle-once cell (level 3+):** specific switches are
  tagged `single-flip` — they refuse to toggle on the SECOND
  wave-impact (their flip-history counter caps at 1). Visualised
  with a small dark-purple dot inside the switch.

## Per-level progression

### Level 1 — base system (M1 + M2 + M3)
- 8×8 active region. 1 switch requiring "on". Wave reach R = 8.
- **Witness:** 15 actions. The player must position the emitter and emit a wave. To make it non-trivial, add 3 switches that must be hit. The player must find a central location to emit the wave so it hits all 3 switches before they expire.
- **Mechanics required:** M1, M2, M3.

### Level 2 — + M4 (walls) + M5 (reach limit)
- 10×10 region. 4 switches. Walls partition the grid. Wave reach R = 5.
- **Witness:** 35 actions. The player must emit waves from multiple locations because the walls block the waves. They must carefully sequence the emits and ticks to ensure the waves reach their targets without accidentally double-hitting switches and turning them back off.
- **Mechanics required:** M1, M2, M3, M4, M5.

### Level 3 — + M6 (single-flip cell) + composition
- 12×12 region. 6 switches: 3 single-flip and 3 normal. 
- **Witness:** 60+ actions. Single-flip cells are highly restrictive. The player must choose emit positions and timings such that single-flip cells are touched ONCE and only once, while normal switches can be hit multiple times as long as they end up in the correct state. This requires orchestrating intersecting wave rings.
- **Mechanics required:** M1, M2, M3, M4, M5, M6.

## Win condition
After every ACTION5, walk every switch sprite. If every switch is in its required state, fire `self.next_level()`.

## Lose condition
`steps_used >= max_steps` → `self.lose()`. No instant-fail collision.

## Internal state
- `self.emitter_pos: tuple[int, int]` — the emitter's current cell.
- `self.waves: list[Wave]` — each `Wave` has `source: tuple[int, int]`, `radius: int`, `reach: int` (the level's per-wave max).
- `self.switches: list[Switch]` — each switch carries `pos`, `state: bool`, `target_state: bool`, `single_flip: bool`, `flip_count: int`.
- `self.walls: set[(int, int)]`.
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `gv47 — seed-grow-surround-dissolve`**: Wavefront emits a transient 1-tick ring, not a persistent region.

## Step budget
- L1: 40.
- L2: 80.
- L3: 150.

## Random-resistance
Random emit-and-tick has very low probability of toggling each switch the right number of times — most random sequences leave switches in arbitrary states. Single-flip cells (L3) make random play essentially zero-success.

## Planning depth
- **L1:** moderate — must calculate Chebyshev distances.
- **L2:** deep — plan multiple emit-and-tick episodes around walls.
- **L3:** very deep — single-flip cells force the player to choose emit positions that make each pass count exactly once. Intersecting wave rings require deep temporal planning.
