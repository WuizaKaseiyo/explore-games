# zk9p — pursuer-merge-walk

## Summary
The player walks a single magenta avatar around a small wall-bounded
arena that is also inhabited by 2-4 distinctly-coloured AI "pursuer"
pawns. Each pursuer follows a deterministic per-type chase rule and
steps one cell toward the avatar after every avatar action; when two
or more pursuers land on the same cell on the same tick they all
merge and disappear. The level wins when no pursuers remain. A pursuer
landing on the avatar's cell ends the level (lose); running out of
step-budget also ends the level (lose). The player's tactical lever is
timing — walking such that two pursuers' next-tick destinations
coincide, then stepping away so they overshoot into each other.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Move avatar one cell up; advance all pursuers one tick | always; rejected silently if destination is wall or out of bounds |
| ACTION2 | Move avatar one cell down; advance all pursuers one tick | as above |
| ACTION3 | Move avatar one cell left; advance all pursuers one tick | as above |
| ACTION4 | Move avatar one cell right; advance all pursuers one tick | as above |
| ACTION5 | L3 only: tick-skip — avatar holds, pursuers advance one tick (costs 2 step-counter units). L1/L2: no-op (1-unit cost). | always |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | base dynamic: avatar walk + Manhattan-major pursuer chase + merge-on-collision | 14×14 grid, no walls; two `pursuer_manhattan` pawns flank the avatar's column. Witness `[ACTION1, ACTION1, ACTION1, ACTION1]` baits both pursuers onto cell (7, 5) for a merge. |
| 2 | + wall-block (walls block avatar and pursuer chase steps) + orthogonal-major chase rule (`pursuer_cyan` prefers minor axis) | 16×16 grid; vertical wall column at x=8 splits the upper arena and stalls cyan at (8, 3). Witness must shift the avatar off column 8 to release cyan via its minor-axis preference, then converge all three pursuers in a 3-merge. Witness sketch (see spec §4 L2): 15-action sequence beginning `[ACTION1×4, ACTION3, ACTION3, ACTION1, ACTION1, ACTION4, ACTION1, ACTION4, ACTION1, ACTION1, ACTION1, ACTION1]`. |
| 3 | + phase pursuer (`pursuer_green`, intangible to avatar on odd-tick parity, tangible on even) + tick-skip ACTION5 | 18×18 grid with a corridor wall structure (horizontal wall at y=8, vertical wall at x=4 from y=10..14). Avatar must traverse green's cell at (9, 9) on an odd tick to reach the bait region; ACTION5 advances pursuers without moving the avatar to align parities. Witness sketch (see spec §4 L3): 24-action sequence beginning `[ACTION1×6, ACTION5, ACTION1, ACTION3, ACTION1, ACTION3, ACTION1, ACTION4, ACTION4, ACTION1, ACTION1, ACTION3, ACTION3, ACTION1, ACTION1, ACTION1, ACTION4, ACTION1, ACTION1]`. |

## Win condition
Every sprite tagged `pursuer` has `interaction == REMOVED` (i.e.,
zero live pursuers remain on the level). Triggers `self.next_level()`.

## Lose condition
Either (a) any sprite tagged `pursuer` with
`interaction == TANGIBLE` shares a cell with the avatar (caught — note
that the phase pursuer in `INTANGIBLE` state on odd ticks does NOT
trigger this), or (b) the per-level step counter reaches zero. Both
trigger `self.lose()`.

## Internal state

- `self._step_budget: int` — current level's step budget (60 / 80 /
  100 for L1 / L2 / L3 from `level.get_data("step_budget")`).
- `self._step_units_used: int` — units consumed in this level
  (ACTION1-4 = 1 unit each; L3 ACTION5 = 2 units; L1/L2 ACTION5 = 1
  unit no-op).
- `self._tick: int` — pursuer-tick counter incremented on every
  pursuer-advancing action; used to compute green's parity in L3.
- `self._step_hud: StepCounterHud` — `RenderableUserDisplay` drawing
  a horizontal bar at row 63 (pink filled portion, grey drained
  portion).

## Notable code patterns

- **Two-pass pursuer move resolution.** All pursuer destinations are
  computed first (with wall-block and bounds checks), then applied
  simultaneously, then merge-on-collision is detected by grouping
  by `(x, y)`. Avoids the simultaneous-conflict gotcha noted in
  `code/universal-scaffold.md`.
- **Phase pursuer via `InteractionMode.TANGIBLE` ↔ `INTANGIBLE`.** A
  single `_update_phase_interaction()` helper toggles the green
  pursuer's interaction based on `self._tick % 2`. Avatar capture
  ignores INTANGIBLE pursuers; merge-on-collision still applies
  (green merges with cyan / red / yellow on any tick).
- **Tag-based dispatch for chase rules.** `pursuer_manhattan` /
  `pursuer_orthogonal` / `pursuer_phase` tags select which chase
  rule applies in `_chase_step()`. `pursuer_phase` reuses
  Manhattan-major; orth uses a minor-axis-first rule with y-first
  tie-break.
- **Camera viewport per-level resize.** `on_set_level` sets
  `self.camera.width`/`.height` from `level.grid_size` so the 14/16/18
  cell grids each render at their natural scale (4×, 4×, 3×) and
  centre in the 64×64 frame.
- **Decorative floor sprite.** `floor_<size>` sprites are
  `collidable=False, layer=-1` rectangles with a sparse palette-3
  speckle on a palette-4 ground; entities are 1×1 single-palette
  sprites that read clearly against the textured floor (per
  `negative-similarity-check.md` principle 1).
