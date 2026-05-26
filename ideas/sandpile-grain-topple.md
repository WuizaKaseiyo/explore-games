# SUPERSEDED — see `counterweight-beam-balance.md`

> This file is retained for traceability but the mechanic is being
> dropped from the unimplemented pool. See `REVISIONS.md` for rationale
> (Abelian threshold-redistribution cascade is the same family as
> vn8d domino-cascade-topple and gg17 fuse-burn-ignite).

---

# (former) Sandpile-Grain-Topple

## Summary

Every grid cell can hold 0–3 stationary grains, visualised as 1-3
small same-colour pixels stacked inside the cell. The player has
one base verb: **drop a grain** on a cell via ACTION6. If the
target cell already held 3 grains, the drop pushes it to 4 — the
cell instantly **topples**: all 4 grains leave, sending one to each
of the 4 cardinal neighbours; the toppled cell becomes empty. If
any neighbour now holds 4, it topples in turn — the cascade
continues until every cell holds ≤ 3 grains (the *Abelian sandpile
relaxation*).

Each level shows **target cells** that demand an exact resting
grain count (1, 2, or 3 grains shown as a ring of "ghost dots"
around the target). The level wins when every target's actual
grain count equals its required count after the cascade settles.

## Visual elements (distinct from prior corpus)

- 9×9 inner grid of pale-grey **floor cells**, each ~6 display
  pixels per cell.
- A grain is a single dark-blue pixel; cells with 1/2/3 grains show
  1/2/3 stacked dark-blue pixels in fixed sub-positions of the cell.
- A **target indicator** floats around each target cell — a 1-pixel
  outline with N small "ghost" dots (yellow) corresponding to the
  required grain count. When the cell holds the matching number of
  blue grains, the yellow ghosts turn green (visual confirmation).
- **Walls** are solid black 1-cell sprites — grains landing on a
  wall are absorbed (lost to the system).
- **Sinks** (level 3) are dark-purple cells — when a grain enters,
  it is consumed and the sink emits a 1-frame pulse.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION6 | Click cell `(x, y)` to drop one grain there. If the cell now holds ≥ 4, topple-cascade resolves before the step ends. | always; clicking a wall is a free no-op (no step consumed). |

`available_actions = [6]`. No avatar, no rotation, no commit phase.

## Mechanics enumeration

- **M1 — drop-grain:** ACTION6 click adds 1 grain to the clicked
  cell; the cell's visual representation increments.
- **M2 — topple-cascade:** any cell with ≥ 4 grains immediately
  toppling — sending one grain to each cardinal neighbour, leaving
  itself empty. Toppling is iterative until no cell has ≥ 4
  grains. Order of toppling does not affect the final state
  (Abelian property).
- **M3 — wall-absorb:** grain that would enter a wall cell is lost
  (it never accumulates; the wall stays empty).
- **M4 — exact-count target:** target cells need exactly N grains
  AT REST (after the cascade completes). Over- or under-shooting
  fails the target.
- **M5 — sink-channel:** sink cells *consume* every grain that
  enters them (similar to walls, but the player can deliberately
  use sinks to drain excess grain mid-cascade and steer the path
  of the cascade).

## Per-level progression (mechanic +1 / +2)

### Level 1 — base system (M1 + M2 + M4)
- 5×5 active region. One target cell at (4, 2) requiring 2 grains.
  No walls, no sinks, no obstacles.
- **Witness:** drop 5 grains at (2, 2). The cascade toppling
  (2, 2) sends 1 to each of (1, 2), (3, 2), (2, 1), (2, 3). Five
  total drops produce the right resting count at (4, 2):
  click (2, 2) ×5 → cascades produce grain at (4, 2) and other
  cells; precise count at (4, 2) is 2.
- (Specific witness drop sequence is engineered in spec writing
  to land exact counts — the harness's `critique_spec` checks.)
- **Mechanics required:** M1 (drop), M2 (cascade), M4 (target).

### Level 2 — + M3 (walls confine cascade)
- 7×7 region. Two targets — one at (1, 5) needing 1 grain, another
  at (5, 5) needing 3 grains. A wall cell at (3, 5) splits the
  centre row into a left and right corridor.
- **Witness:** drops engineered so cascades on each side fill
  exactly the matching target. The wall ensures grains do not
  bleed across — without the wall, the cascade would over-fill
  one target.
- **Mechanics required:** M1, M2, M3, M4.

### Level 3 — + M5 (sinks) + extended composition
- 9×9 region with three targets and two sinks. Targets need
  (1, 1, 2) grains; sinks at (4, 1) and (4, 7) drain over-spill.
- **Witness:** the player must place drops such that the cascade
  *uses* sinks to drain excess; if a sink is left untouched, an
  adjacent target over-fills. Mis-ordering drops causes a target
  to over-shoot before the sink absorbs spillover, and the
  Abelian property guarantees that final-count matters but
  *which cells topple* depends on starting layout — the player
  must choose drop cells whose toppling routes pass through the
  sinks before reaching the over-fill target.
- **Mechanics required:** M1, M2, M3, M4, M5.

## Win condition
After every cascade settles (no cell has ≥ 4 grains), check every
target sprite. For each target, `count_grains_at(target.x,
target.y) == target.required_count`. If all targets match, fire
`self.next_level()`.

## Lose condition
- `steps_used >= max_steps` triggers `self.lose()`.
- An *over-fill* lose is OPTIONAL and gated per-level — for L3, if a
  target's grain count exceeds its required count after a cascade
  AND no sink is reachable from the over-filled cell, the level is
  unrecoverable; the engine could mark this as a lose, but a
  cleaner policy is to permit reset and only lose on step
  exhaustion.

## Internal state
- `self.grains: dict[(int, int), int]` — current grain count per
  cell.
- `self.walls: set[(int, int)]` — wall cells (level 2+).
- `self.sinks: set[(int, int)]` — drain cells (level 3+).
- `self.targets: list[Sprite]` — target sprites; each carries
  `required_count: int`.
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `vn8d — domino-cascade-topple`**: vn8d is a 1-D *line* of
  dominoes that topples under a single click; burst-pads splay 4
  ways and rotator-pads turn corners. Sandpile is fundamentally
  *2D Abelian threshold-redistribution*: every cell accumulates
  and topples symmetrically when ≥4 grains, not when struck by a
  neighbour topple alone. The Abelian relaxation makes order
  irrelevant for the final state; vn8d is order-dependent.
- **vs `gv47 — seed-grow-surround-dissolve`**: gv47 grows by
  cardinal expansion of a region; sandpile redistributes
  individual grains via threshold rule.
- **vs `cd82 — orbit-fire-paint`**: cd82 paints triangular wedges;
  sandpile redistributes 1-pixel grains by topple.
- **vs `dc22 — colour-cycle-walk`**: cycling state of wedge-blocks;
  no grain redistribution.

## Step budget
- L1: 12 (witness ~5 drops; cushion for exploration).
- L2: 18.
- L3: 30.

## Random-resistance
A random clicker drops grains at uniformly random cells; the chance
of producing exact target counts in a constrained grid drops
exponentially with the number of targets and the asymmetry of
target counts. Solving L3 requires deliberate *route planning*
through sinks — random clicks almost never yield the exact resting
count.
