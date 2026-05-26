# kp9z — grain-accumulate-topple

## Summary
The player drops grains onto designated source cells with a click. Each
cell holds a non-negative integer count visualised as up to four sub-cell
pips inside a bordered tile. When a cell exceeds capacity (4), it
topples — its count resets to zero and one grain is delivered to each of
its four cardinal neighbours, producing a deterministic cascade. Sinks
absorb every delivered grain; redirectors topple at capacity 1 and
forward their single grain in their declared cardinal exit direction.
**Clicking a redirector rotates its exit direction 90° clockwise**, so
the player must orient redirectors correctly before triggering a topple
that flows through them. The strict win predicate requires every cell
to end at exactly its declared target count; cascade by-products on
non-target cells are irreversible, so the player must reason about
cascade structure before clicking.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 (on source) | Drop one grain on the clicked source; run the cascade to completion. | clicked cell has type `source` |
| ACTION6 (on redirector) | Rotate the clicked redirector's exit direction 90° clockwise (north → east → south → west → north). | clicked cell has type `redirector` |
| ACTION6 (elsewhere) | No-op. Still consumes one step of the budget. | always |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Base dynamic system: drop + topple-on-cap-4. | Single source at (1, 1) on a 4×4 board; 4 cardinal targets each with target_count=1; step budget 8. Witness `[ACTION6@(27, 27) × 4]` — 4 clicks on the source produce one topple, fanning 1 grain to each cardinal target. |
| 2 | Adds sink — cells that absorb every delivered grain without re-emitting. | 5×5 board with two sources at (1, 2) / (3, 2); three sinks at (0, 2) / (2, 2) / (4, 2) along the central column; four targets at the diagonal cardinals of each source; step budget 16. Witness `[ACTION6@(32, 22) × 4, ACTION6@(32, 42) × 4]` — each source toppled exactly once, the central-column sinks absorbing the on-axis cardinals while the diagonal-cardinal targets each receive exactly 1. |
| 3 | Adds rotatable redirector — capacity-1 cell whose exit direction the player can change by clicking it (90° clockwise per click). | 5×5 board with one source at (2, 2); two redirectors at (1, 2) and (2, 3) both starting in south orientation (the wrong direction); two sinks at (2, 1) and (3, 2) covering the source's other cardinals; two targets at (0, 2) and (2, 4) — each two cells from the source, reachable only via a correctly-oriented redirector; step budget 18. Witness `[ACTION6@(32, 22) × 2, ACTION6@(42, 32) × 3, ACTION6@(32, 32) × 4]` — rotate (1, 2) twice to reach north (south → west → north), rotate (2, 3) three times to reach east (south → west → north → east), then drop on the source four times to topple it through the now-correctly-oriented redirectors. The naive heuristic "drop first" fails because the (1, 2) redirector starts pointing south, sending its forwarded grain back into the source — leaving source at 1 grain and strict-failing the win predicate. |

## Win condition

After every action's cascade resolves, the predicate is: every conceptual
cell's current grain count equals its declared target count, where
target_count = 0 for any cell not explicitly designated TARGET. Triggers
`self.next_level()`; on the last level, `self.win()` fires through the
base class.

## Lose condition

`self.steps_left ≤ 0` at the end of a step that did not also satisfy the
win predicate triggers `self.lose()`. There is no instant-fail collision
or hazard.

## Internal state

- `grain_counts: dict[(row, col), int]` — current grain count per
  conceptual cell. Mutated on click (drop) and during the cascade
  (`_resolve_cascade`).
- `cell_types: dict[(row, col), str]` — per-cell type designation:
  `"regular" | "source" | "target" | "sink" | "redirector"`.
  Static per level.
- `redirector_orientations: dict[(row, col), str]` — current exit
  direction (`"north" | "south" | "east" | "west"`) for every redirector
  cell. Mutated when the player clicks a redirector.
- `target_counts: dict[(row, col), int]` — declared target count per
  cell (0 for non-targets). Static per level.
- `cell_sprites: dict[(row, col), Sprite]` — handle to the placed cell
  sprite for runtime pixel mutation.
- `steps_left: int`, `max_steps: int` — step budget tracking.
- `anchor: tuple[int, int]` — game-grid offset of cell (0, 0)'s sprite.
- `board_size: int` — N (4 for L1, 5 for L2/L3).
- HUD `_hud: StepCounterHud` — renders the bottom-row depleting bar.

## Notable code patterns

- **Per-cell sprite with runtime pixel mutation**: each conceptual cell
  is one 10×10 sprite. Static features (frame, type center, frame-edge
  notch, target pip slots) are baked into the sprite at level-build
  time; current-grain pip slots are mutated in `_refresh_cell_pixels()`
  after every action, painting the 4 cardinal-mid 2×2 slots yellow as
  the count rises.
- **Shape-as-meaning via frame-edge notches**: cell types differentiate
  on shape, not just colour. Source has a top-edge magenta notch; sink
  has a left-edge blue notch; redirector_south has a bottom-edge
  orange notch; target has 1..4 green corner pips; regular has nothing.
  Without colour, every type is pairwise distinguishable from its pixel
  matrix alone. Survives 2×2 pool to 32×32.
- **Bounded cascade resolution**: `_resolve_cascade` loops up to
  `board_size² × 8` times, in each pass scanning every cell for over-
  capacity (or count ≥ 1 for redirectors) and toppling once. Per the
  abelian property of the sandpile, the final state is order-
  independent, so a simple sweep-until-stable is sufficient. The bound
  prevents infinite loops if a future variant introduced a non-
  conserving rule.
- **Strict win predicate as cascade-shaper**: the win condition checks
  every cell, not just the targets. This makes sinks and redirectors
  counterfactually necessary: any cascade-byproduct landing on a
  non-target REGULAR cell is a strict failure, so non-target cardinals
  of sources MUST be sinks (or redirectors) for a winning configuration
  to exist. The L2/L3 layouts exploit this to force the player through
  a specific cascade topology.
- **Click-only interaction**: `available_actions=[6]` keeps the verb
  vocabulary minimal — the only thing the player can do is choose
  *where* to click. The cell-type system, not the action enum, is what
  carries the game's complexity.
