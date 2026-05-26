# Constellation-Edge-Build

## Summary

The grid contains a small set of fixed **dot sprites** (each a
2×2 coloured pip). The player builds a graph by clicking pairs
of dots: clicking the first dot selects it (it lights up); the
next click on a different dot creates an **edge** between them
— a 1-pixel coloured line drawn straight between the two dot
centres along the shortest cardinal-or-diagonal path. Edges
cannot cross each other geometrically (any new edge whose
straight line crosses an existing edge is rejected as a no-op
and the selection clears).

Each level shows a **target graph** depicted as a small
side-panel: which dots must be connected by an edge in the
finished arrangement. The level wins when the live edge-set
exactly matches the target edge-set (no extras, none missing)
AND the no-crossing constraint is preserved at every step.

The only failure mode is exhausting the per-level step counter.

## Visual elements

- 14×14 grid; pale-grey background.
- Dots are 2×2 saturated-colour cells at fixed positions.
- A **selected dot** has a 1-pixel white outline (visual cue).
- An **edge** is a 1-pixel line between dot centres, painted in
  the dot pair's blended colour (or a neutral grey for L1).
- A **target side-panel** in the bottom-right corner depicts the
  required graph: same dot positions at scale, edges drawn as
  thin lines.
- A **rejected click** flickers (1-frame red flash on the second
  dot) and the selection clears.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION6 | Click pixel `(x, y)`. If it lands on a dot AND no dot is selected, select that dot. If a dot is already selected and the click lands on a *different* dot AND the straight edge between them does not cross any existing edge AND that edge is not already in the live set, add the edge; selection clears. If the click lands on the same dot already selected, deselect it. If the click misses any dot, no-op. If the new edge would cross an existing edge or duplicate one, reject with a flicker; selection clears (the rejected click consumes a step). | always |
| ACTION5 | DELETE the most-recently-added edge (single-step undo of edges). | only if the live edge-set is non-empty |

`available_actions = [5, 6]`. No avatar.

## Mechanics enumeration

- **M1 — dot-select:** ACTION6 click on a dot selects it (or
  toggles selection if it was already selected).
- **M2 — edge-build:** a click on a second different dot creates
  the edge between selected and second dot — provided the edge
  doesn't cross any existing edge and isn't a duplicate.
- **M3 — no-crossing constraint:** edges are straight lines
  (segments) between dot centres; an edge that would cross any
  existing edge is rejected.
- **M4 — match-target-graph:** the win predicate compares the
  set of live `frozenset({dot_a, dot_b})` edges to the level's
  target set.
- **M5 — undo-edge:** ACTION5 removes the most-recent edge.
  Useful when the player paints themselves into a non-target
  configuration that they need to back out of.
- **M6 — fixed-edges (level 2+):** specific edges are
  pre-existing AT LEVEL START — they cannot be removed by
  ACTION5 (visualised in dark-grey rather than coloured).
  These pre-existing edges constrain which other edges the
  player can add (because of M3, no-crossing).
- **M7 — colour-pair edges (level 3+):** each potential edge has
  a *required colour* — only edges drawn between specific
  dot-colour pairs (e.g. orange-to-blue is allowed; blue-to-blue
  is not) can be added. Visualised by greyed-out target lines
  in the side-panel.

## Per-level progression

### Level 1 — base system (M1 + M2 + M3 + M4)
- 8 dots arranged in a star pattern. Target: a specific 6-edge non-crossing graph. The geometry is designed so that building certain target edges first will geometrically block the ability to select intermediate dots for other edges.
- **Witness:** Player must build the edges from the inside out. 12 clicks (6 edges).
- **Mechanics required:** M1, M2, M3, M4.

### Level 2 — + M5 (undo) + M6 (fixed edge)
- 12 dots; 3 fixed-edges creating a maze-like barrier. Target requires an 8-edge path that weaves between the fixed edges. A naive greedy approach will inevitably cross a fixed edge or box in a required dot.
- **Witness:** ~20 clicks (10 edges). The player must carefully sequence edge builds, and will likely need ACTION5 (undo) when they trap a dot behind their own built edges.
- **Mechanics required:** M1, M2, M3, M4, M5, M6.

### Level 3 — + M7 (colour-pair constraint)
- 15 dots in 4 colours. Target is a complex 12-edge graph. M7 requires edges to connect specific colour pairs (e.g., Red-Blue, Blue-Green). The fixed edges and spatial arrangement mean that the "obvious" dot to connect to is the wrong colour, forcing a zigzag routing through intermediate dots.
- **Witness:** ~30 clicks. Extreme order-dependency; building the perimeter first cuts off the required Red-Blue interior connection.
- **Mechanics required:** M1, M2, M3, M4, M5, M6, M7.

## Win condition
After every ACTION6 that produces an edge-add or an ACTION5 that produces an edge-remove, compare the live edge-set to the target edge-set. If equal, fire `self.next_level()`.

## Lose condition
`steps_used >= max_steps` → `self.lose()`. Misclicks (clicks on empty cells, duplicate edges) consume 1 step each.

## Internal state
- `self.dots: list[Dot]` — each dot has `pos: (int, int)` and `colour: int`.
- `self.edges: list[Edge]` — each edge has `dot_a, dot_b`, `is_fixed: bool`, `colour: int`.
- `self.selected: Dot | None`.
- `self.target_edges: set[frozenset[Dot]]`.
- `self.allowed_colour_pairs: set[frozenset[int]]` (level 3+).
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `loop-crossover-flip`**: constellation BUILDS a graph from scratch with a strict no-crossing constraint, whereas loop-crossover modifies existing intersections.
- **vs `tn36`**: tn36 builds a program; constellation builds a spatial geometry graph.

## Step budget
- L1: 30.
- L2: 60.
- L3: 100.

## Random-resistance
Random clicking will almost immediately create edge crossings that block further progress. The exact target edge-set is impossible to hit by chance.

## Planning depth
- **L1:** moderate — player must realise that drawing a long edge cuts the board in half and prevents drawing crossing edges later.
- **L2:** deep — fixed edges act as walls; player must plan a topological routing.
- **L3:** very deep — colour constraints force counter-intuitive routing, requiring the player to look 3-4 edges ahead to avoid boxing themselves in.
