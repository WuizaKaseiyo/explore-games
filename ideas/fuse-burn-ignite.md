# Fuse-Burn-Ignite

## Summary

The grid is laced with a network of **fuse cells** forming
connected paths and branches. Several **bomb cells** sit at the
endpoints of fuses; each bomb has a required-colour ring. The
player ignites a fuse by clicking any of the **ignition pads**
(small grey cells embedded in the fuse network). Once ignited,
fire on the fuse advances **one cell per turn** along the fuse's
graph, branching at junctions (fire fills every unburned
neighbour fuse cell at junctions on the same tick). When fire
reaches a bomb, the bomb fires and is recorded with the **turn
number** at which it fired.

The win condition: every bomb fires AND the *spread* of fire-turns
across all bombs is within a per-level tolerance (i.e. every bomb
fires within Δ turns of the others — the *synchronisation
window*). The level loses on step exhaustion.

## Visual elements

- 12×12 grid; fuse cells render as 1-pixel dark-orange filaments
  drawn between cell centres; the network is visually a graph.
- An **ignition pad** is a 1×1 dark-grey cell with a 1-pixel
  orange dot — clickable.
- An **unburned fuse** cell is dark-orange; **burning** during the
  step it ignites is bright-yellow; **burned** afterward is
  black-grey.
- A **bomb** is a 2×2 ring; unfired in pale-purple, fired in its
  required-colour solid fill.
- **Junctions** (cells with ≥ 3 fuse neighbours) render with a
  small grey dot at the centre, signalling "fire splits here."
- A **fire-turn HUD** along the bottom rim shows N small chevrons,
  one per fired bomb in the order they fired, coloured by the
  bomb's required colour.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION5 | Advance the simulation by one fuse-burn tick. Every burning fuse cell ignites all its UNBURNED fuse neighbours; bombs adjacent to a burning fuse fire. | always; if no fuse is currently burning, ACTION5 still consumes a step and ticks the global counter. |
| ACTION6 | Click an ignition pad to ignite all its connected fuse neighbours starting next ACTION5. Clicks on non-pad cells are no-ops. | always |

`available_actions = [5, 6]`. No avatar.

## Mechanics enumeration

- **M1 — pad-ignite:** ACTION6 click on an ignition pad starts a
  fire on its neighbouring fuse cells (the cell records the
  start turn).
- **M2 — fuse-burn-tick:** ACTION5 advances time by 1 turn:
  every burning cell ignites all unburned fuse neighbours. Burned
  cells do not re-ignite (they are spent).
- **M3 — branch-split:** at junction cells (≥3 fuse neighbours),
  the burning fuse propagates to all neighbours simultaneously
  (the same turn). This means a junction effectively *splits*
  the fire into multiple parallel arms.
- **M4 — bomb-fire:** when fire reaches a bomb cell, the bomb
  fires and the engine records the current turn number for that
  bomb.
- **M5 — sync-window-target (level 2+):** the win predicate
  requires every bomb to have fired AND the maximum bomb-fire
  turn minus the minimum bomb-fire turn to be ≤ a per-level
  tolerance (Δ; e.g. Δ = 0 means "all on the same turn,"
  Δ = 1 means "within one turn of each other").
- **M6 — fuse-cut (level 3+):** specific clickable **scissor
  cells** can be cut by clicking them BEFORE they burn, removing
  the fuse cell from the network (it never carries fire). After
  burning, scissor cells can no longer be cut. This lets the
  player adjust path lengths to bring sync windows in line.

## Per-level progression

### Level 1 — base system (M1 + M2 + M4 + M5)
- Two ignition pads, two non-intersecting fuse paths of different lengths leading to two bombs. The sync window requires both bombs to fire on the exact same turn (Δ=0).
- **Witness:** 15 actions. The player must count the path lengths. If path A is length 5 and path B is length 8, the player must ignite pad B, wait 3 turns, ignite pad A, and wait 5 turns.
- **Mechanics required:** M1, M2, M4, M5.

### Level 2 — + M3 (branch)
- Three pads, a highly interconnected fuse network with junctions. Four bombs.
- **Witness:** 35 actions. Igniting a pad causes fire to spread and split at junctions. The player must calculate the traversal times to all bombs from different pads and stagger the pad ignitions exactly so that the fire wavefronts reach all four bombs simultaneously. If fire reaches a bomb early, it fails the sync constraint.
- **Mechanics required:** M1, M2, M3, M4, M5.

### Level 3 — + M6 (scissor cell)
- Two pads, extremely complex network with multiple possible paths to five bombs. The natural shortest paths do not allow for a synchronized explosion regardless of ignition timing.
- **Witness:** 60+ actions. The player must use scissor cells to *cut* the shortest paths, forcing the fire to take a longer detour. By carefully pruning the graph, the player manually sculpts the path lengths so that a synchronized explosion becomes possible, then executes the staggered ignition sequence.
- **Mechanics required:** M1, M2, M3, M4, M5, M6.

## Win condition
After every ACTION5, check whether every bomb has fired. If so, compute `max_turn - min_turn` across all bombs; if `<= tolerance_delta` for the level, fire `self.next_level()`.

## Lose condition
`steps_used >= max_steps` → `self.lose()`. Once a fuse cell is burned it is spent; a poorly-timed ignition that fires bombs out-of-window leaves the level in a state where the win predicate can never fire on this attempt. The player relies on the engine's standard reset (R key) to reinitialise per-level state. There is no collision-based instant lose; only the step budget terminates a run.

## Internal state
- `self.fuse_graph: dict[(int, int), list[(int, int)]]` — adjacency of fuse cells.
- `self.burned: dict[(int, int), int | None]` — turn at which each fuse cell burned, or None if unburned.
- `self.burning: set[(int, int)]` — currently-burning frontier for the next ACTION5 tick.
- `self.bombs: dict[Sprite, int | None]` — bomb sprites mapped to their fire-turn (None if unfired).
- `self.cut_cells: set[(int, int)]` — fuse cells removed by scissor cuts (level 3+).
- `self.tick: int` — number of ACTION5 ticks since first ignite.
- `self.tolerance_delta: int` — per-level sync tolerance.
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `vn8d — domino-cascade-topple`**: vn8d is a domino chain triggered by a single click. Fuse-burn is a *time-explicit* propagation (one tick per turn) with *synchronisation* on multi-bomb timing — this timing-window goal is a novel objective shape.

## Step budget
- L1: 40.
- L2: 80.
- L3: 150.

## Random-resistance
A random clicker has near-zero chance of igniting pads at the exact relative turns to produce perfect sync. L3 requires precise topological cuts before ignition; random cuts will almost certainly sever a bomb entirely or ruin the timing.

## Planning depth
- **L1:** moderate — player must explicitly count fuse lengths and calculate the delay offset for ignitions.
- **L2:** deep — multiple overlapping wavefronts. The player must trace shortest paths on the graph to determine which pad hits which bomb first.
- **L3:** very deep — the player is co-designing the graph (via scissors) and then solving the timing puzzle on their custom graph. Commuting a cut with an ignite breaks the game (cuts must happen before fire passes).
