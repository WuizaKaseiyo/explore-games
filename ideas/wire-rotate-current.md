# Wire-Rotate-Current

## Summary

The grid hosts **fixed-position wire cells** of a few shapes:
*straight* (2 collinear endpoints), *bend* (2 perpendicular
endpoints), *T-junction* (3 endpoints), and *cross* (4 endpoints,
two passes that DO NOT mix). Each wire cell can be rotated to one
of its valid orientations by clicking it (each click advances the
orientation by 90°). A few cells are **sources** (continuously
emit a coloured current at one fixed orientation) and **sinks**
(consume current of one specific colour).

Current propagates instantly along connected wire endpoints. Two
wire cells are *connected* if they are orthogonally adjacent AND
their facing endpoints (one's east-pointing endpoint and the
neighbour's west-pointing endpoint, etc.) both exist after their
current rotation.

The level wins when every sink has its required-colour current
delivered AT THE END of the most recent action. The only failure
mode is exhausting the per-level step counter.

## Visual elements

- 8×8 inner grid; wire cells are 1×1 sprites coloured grey when
  uncharged and tinted with the source colour when charged.
- A wire's *endpoints* are 1-pixel coloured stubs poking out from
  one of the 4 cell edges (a straight wire = stubs out the N and
  S edges; a bend = stubs out the N and E edges; a T = stubs out
  three edges; a cross = stubs out all four).
- A **source** is a square 1×1 sprite with a saturated coloured
  ring; its single endpoint stub points in a fixed direction.
- A **sink** is a hollow ring of the required colour; it lights
  up bright when correctly charged.
- The wire frame between un-meeting endpoints stays grey (no
  current).

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION6 | Click any wire cell to rotate its orientation +90° clockwise. The orientation cycles through the wire's valid orientations (straight = 2, bend = 4, T = 4, cross = 1 — clicking a cross is a no-op). | always; clicks on empty cells, sources, or sinks are no-ops with no step consumed. |

`available_actions = [6]`.

## Mechanics enumeration

- **M1 — wire-rotate:** ACTION6 click rotates the clicked wire's
  orientation by +90° CW.
- **M2 — connectivity-propagation:** after every rotation, the
  engine recomputes the connected-component graph of wire endpoints;
  any wire cell reachable (along connected endpoints) from a source
  takes that source's colour; cells reachable from multiple sources
  are flagged "shorted" and stay grey (visual: dark-red flicker).
- **M3 — sink-colour-match:** a sink is satisfied iff (1) at least
  one of its endpoints is connected to a source, AND (2) the
  delivered colour equals the sink's required colour.
- **M4 — cross-cell (level 2+):** the *cross* wire allows two
  perpendicular currents to coexist without mixing — the two axes
  are independently propagated. This lets two colours pass through
  the same cell.
- **M5 — short-circuit penalty (level 3+):** when two
  different-colour currents would charge the SAME wire cell
  (any non-cross wire cell — straight, bend, or T) via different
  endpoints, that cell becomes `shorted`: it carries no colour
  itself AND it does NOT propagate current beyond. Sinks
  reachable only through a shorted cell receive no current.
  Cross cells (M4) are the ONE exception: a cross cell carries
  two perpendicular currents independently and never shorts.
  The propagation rule run after each rotation is therefore:
  (1) BFS forward from each source along its connected
  same-colour endpoints; (2) any wire cell reached by two
  distinct source colours from non-cross-cell perpendicular
  axes is marked `shorted` and removed from the BFS frontier;
  (3) sinks evaluate their receiving colour from the surviving
  BFS.

## Per-level progression

### Level 1 — base system (M1 + M2 + M3)
- 1 source, 1 sink. Multiple straight and bend wires. 
- **Witness:** 15 actions. The player must rotate the wires to form a continuous path from source to sink. Since each rotation is an action, the player must optimize the number of rotations.
- **Mechanics required:** M1, M2, M3.

### Level 2 — + M4 (cross-cell)
- 2 sources, 2 sinks. Their paths must cross. 
- **Witness:** 35 actions. The player must route two currents using a cross-cell. They must carefully rotate the surrounding cells so that the correct colors are fed into the cross-cell without mixing.
- **Mechanics required:** M1, M2, M3, M4.

### Level 3 — + M5 (short-circuit penalty + composition)
- 4 sources, 4 sinks. Complex geometry.
- **Witness:** 60+ actions. The short-circuit penalty means any mixing of currents immediately kills both paths. The player must plan the routing of all four colours *together* and exploit cross-cells to separate paths. A single greedy rotation might create a transient short circuit, so the player must orchestrate the sequence of rotations.
- **Mechanics required:** M1, M2, M3, M4, M5.

## Win condition
After every ACTION6, recompute the wire connectivity graph; for each sink, check whether it receives current of its required colour. If every sink is satisfied, fire `self.next_level()`.

## Lose condition
`steps_used >= max_steps` → `self.lose()`. Misclicks are no-cost.

## Internal state
- `self.wires: dict[(int, int), WireCell]` — each `WireCell` carries a `kind: str` (straight/bend/t/cross) and an `orientation: int`.
- `self.sources: list[(Sprite, int, int, int, int)]` — sprite, position, colour, fixed orientation.
- `self.sinks: list[(Sprite, int, int, int)]` — sprite, position, required colour.
- `self.charged: dict[(int, int), int]` — current colour per energised wire cell; recomputed each step.
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `sp80 — pour-shelf-route`**: Wire-rotate is rotation-only (no placement), with **instant** propagation after every rotation, and no spill / spill-count / tilt mechanic.

## Step budget
- L1: 40.
- L2: 80.
- L3: 150.

## Random-resistance
A random clicker rotates wires uniformly; the chance of all sinks being satisfied at any single random state falls exponentially with sink count (each sink demands the right colour AND right connectivity). Random play essentially never hits the L3 multi-source separation simultaneously.

## Planning depth
- **L1:** moderate — trace a single path visually and execute.
- **L2:** deep — route two paths in tandem, solving the intersection constraint.
- **L3:** very deep — naive greedy routing causes a short circuit. The player must treat all paths as a single interconnected topological puzzle.
