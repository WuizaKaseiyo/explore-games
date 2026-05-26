# SUPERSEDED — see `pendulum-sync-rail.md`

> This file is retained for traceability but the mechanic is being
> dropped from the unimplemented pool. See `REVISIONS.md` for rationale
> (the hot/cold cellular automaton is functionally redundant with
> gg17 fuse-burn and gg16 wavefront-ring).

---

# (former) Heat-Diffuse-Equilibrium

## Summary

Each cell carries a binary **state** ∈ {`hot`, `cold`}. Some
cells are pinned: **source cells** are permanently hot; **sink
cells** are permanently cold; both ignore the diffusion rule.
Other cells are **valve cells** the player toggles open/closed
via click; closed valves act like walls for heat (they do not
transmit). Pressing ACTION5 advances the simulation one tick.
The tick rule is deterministic and runs in parallel from the
previous-tick state:

- A **non-pinned non-closed** cell's new state is **`cold`** if
  any of its open-valve-connected cardinal neighbours is a
  **sink-pinned** cell (cold dominates — sinks "drag" their
  neighbours cold).
- Otherwise, the cell's new state is **`hot`** if any of its
  open-valve-connected cardinal neighbours is **hot or
  source-pinned** (heat spreads).
- Otherwise, the cell stays in its previous state.

Each level shows **target cells** with a required state. The
level wins when every target cell's state equals its required
value AT THE END of an ACTION5 tick. The only failure mode is
exhausting the per-level step counter.

## Visual elements

- 8×8 inner grid; cells are 1×1.
- Hot cells render saturated-red; cold cells render pale-grey.
  The whole grid recolours after each tick.
- A **source** is a 1×1 cell with a 1-pixel white border (always
  red / hot).
- A **sink** is a 1×1 cell with a 1-pixel dark-blue border
  (always pale-grey / cold).
- A **valve** is a 1×1 cell with a small dark-grey diagonal
  marker; *open* renders normal (heat-coloured), *closed* renders
  flat-black with a 1-pixel marker.
- A **target** is a hollow 1-pixel ring; a hot-required target
  has a red ring, a cold-required target has a dark-blue ring.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION5 | Advance the simulation by one diffusion tick using the rule in the Summary (sink-adjacent → cold; else hot-adjacent → hot; else unchanged). Pinned cells (sources, sinks) keep their fixed state. | always |
| ACTION6 | Click a valve cell to toggle its open/closed state. Clicks on non-valve cells are no-ops (no step consumed). | always |

`available_actions = [5, 6]`.

## Mechanics enumeration

- **M1 — diffusion-tick:** ACTION5 advances time by 1. Each
  non-pinned non-closed cell's new state is computed in
  parallel from the previous tick's state, using the
  Summary's three-line rule (sink-priority cold; else
  hot-spread; else unchanged). Cells separated by a closed
  valve are NOT neighbours for this rule.
- **M2 — source-pin:** source cells are permanently hot and
  ignore the diffusion rule.
- **M3 — sink-pin:** sink cells are permanently cold and ignore
  the rule.
- **M4 — valve-toggle:** ACTION6 click on a valve flips its
  open/closed state. Closed valves are insulators — heat does
  not pass through them in either direction.
- **M5 — exact-target match:** the win predicate requires every
  target cell to be in its required state (hot or cold).
- **M6 — single-toggle valve (level 3+):** specific valves are
  tagged `single-toggle` — they can be toggled AT MOST ONCE per
  level. After toggling, the valve is locked in its new state
  for the rest of the level (clicking again is a no-op).
  Visualised with a small extra dot.

## Per-level progression

### Level 1 — base system (M1 + M2 + M3 + M5)
- 5×5 active region. One source; one sink. Four targets. No valves.
- **Witness:** 15 actions. The player must place walls (if available) or wait the exact number of ticks for the heat gradient to stabilize. Since there are no valves, the player must just advance the simulation until the equilibrium is reached. Wait, no valves means just clicking ACTION5. To make it non-trivial, give the player 3 valves they can place, acting as walls.
- **Mechanics required:** M1, M2, M3, M5.

### Level 2 — + M4 (valve)
- 7×7 region. One source; one sink. Four targets. Fixed valves. 
- **Witness:** 35 actions. The player must open/close valves to route the heat gradient. Closing a valve insulates a region. The player must insulate the cold targets from the source while exposing the hot targets. The topological routing of heat requires multiple valve toggles.
- **Mechanics required:** M1, M2, M3, M4, M5.

### Level 3 — + M6 (single-toggle valve)
- 8×8 region. Multiple sources/sinks, complex target layout. Single-toggle valves.
- **Witness:** 60+ actions. Single-toggle valves act as permanent commits. The player must open normal valves to flood a region with heat, let it reach equilibrium, then use a single-toggle valve to *permanently* trap the heat in that sub-region, allowing them to re-route the source elsewhere without losing the trapped state. This requires deep sequencing.
- **Mechanics required:** M1, M2, M3, M4, M5, M6.

## Win condition
After every ACTION5, walk every target cell. For each, check `heat[target.pos] == target.required_heat`. If all match, fire `self.next_level()`.

## Lose condition
`steps_used >= max_steps` → `self.lose()`. No instant-fail.

## Internal state
- `self.hot: np.ndarray[bool]` — boolean heat grid (True = hot).
- `self.sources: set[(int, int)]` — pinned hot.
- `self.sinks: set[(int, int)]` — pinned cold.
- `self.valves: dict[(int, int), Valve]` — each valve has `state: 'open' | 'closed'`, `single_toggle: bool`, `has_been_toggled: bool`.
- `self.targets: list[(Sprite, int, int, bool)]` — sprite, pos, required state (True = hot required, False = cold required).
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `gv47 — seed-grow-surround-dissolve`**: heat diffuses by a uniform local rule independent of player click position.

## Step budget
- L1: 40.
- L2: 80.
- L3: 150.

## Random-resistance
Random valve toggles produce random heat gradients; for L3 with multiple targets at different required heats, the chance of random toggling reaching the exact equilibrium is essentially zero — the player must understand which valve isolates which sub-region.

## Planning depth
- **L1:** moderate — player must predict the steady-state heat gradient.
- **L2:** deep — routing heat around obstacles while insulating cold targets.
- **L3:** very deep — single-toggle valves force order-of-operations. The player must use them to permanently capture states, creating "heat batteries" or "cold traps".
