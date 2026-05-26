# hk7v — overhead-trolley-hook

## Summary
The player operates a Cartesian gantry from above the playfield: a
horizontal beam runs across the top, a small trolley slides along it,
a vertical rope of variable length hangs from the trolley, and a U-claw
hook sits at the rope's end. ACTION3/4 slide the trolley
horizontally, ACTION1/2 raise/lower the hook, and ACTION5 toggles
grab/release on whatever block sits directly below the hook. Each
level wins when every coloured block rests on its same-coloured
horizontal target stripe on the floor. Composition layers two
constraints across L2 and L3: a wall the rope and any carried block
must clear by hook-raising before horizontal traversal, and a stacked
supply column whose blocks must be removed top-down because only the
topmost block is grabbable.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION1 | Raise hook by 1 cell (rope shortens). If carrying, the carried block also rises. | `hook.y > trolley.y + trolley.height` and the new hook footprint (and carried-block footprint, if any) does not overlap walls or non-carried blocks. |
| ACTION2 | Lower hook by 1 cell (rope lengthens). If carrying, the carried block also lowers. | `hook.y + hook.height < floor_y`; the new hook footprint and any carried-block footprint clear of walls, blocks (not carried), and floor. |
| ACTION3 | Move trolley left by 1 cell. Hook + rope + any carried block follow. | `trolley.x > 0`; rope column at `trolley.x + 2 - 1` clear of walls between trolley bottom and hook top; hook and any carried block at the new x clear of walls and non-carried blocks. |
| ACTION4 | Move trolley right by 1 cell. Symmetric to ACTION3. | Symmetric. |
| ACTION5 | Toggle grab/release. If carrying: detach block; the block then snap-falls under gravity until it rests on floor or atop another block. Otherwise: if a block exists with its top row directly below the hook bottom and matching x-range, grab it. | Always callable; effect depends on game state. |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | Overhead-manipulator (M1) — base dynamic system: trolley H + hook V + grab/release. | Single red block delivered to single red target. No wall, no stack. Witness (87 actions): `[ACTION4×14, ACTION2×41, ACTION5, ACTION4×30, ACTION5]`. |
| 2 | + Colour-pairing (M2) and rope-clearance-above-wall (M3). | Two colours coexist; one wall in the middle. The longer-distance delivery requires raising hook (and carried block) above row 20 before traversing the wall. Witness (179 actions): `[ACTION4×4, ACTION2×41, ACTION5, ACTION1×38, ACTION4×40, ACTION5, ACTION4×8, ACTION2×38, ACTION5, ACTION4×6, ACTION5]`. |
| 3 | + Gravity-stacking-disassembly (M4). | Three blocks stacked at the supply column; only the topmost is grabbable. Player must remove them in stack order, deliver each across the wall as appropriate, with two of three deliveries crossing the wall. Witness (319 actions): `[ACTION4×4, ACTION2×31, ACTION5, ACTION1×28, ACTION4×40, ACTION5, ACTION3×40, ACTION2×33, ACTION5, ACTION4×20, ACTION2×5, ACTION5, ACTION3×20, ACTION5, ACTION1×38, ACTION4×54, ACTION5]`. |

## Win condition
For every target sprite in the level, find the unique block sprite
sharing its colour tag. The win predicate is true iff each such block
is at `(target.x + 1, FLOOR_Y - block.height)` — i.e. positioned one
cell right of the target's left edge and resting on the floor with
its bottom row at row 57.

## Lose condition
`_action_count >= step_budget` for the current level (`step_budget`
is read from `level.get_data("step_budget")`: 150 / 250 / 500 for
L1 / L2 / L3). No other lose state — there is no hazard and a
mis-delivered block can be re-grabbed and moved within the budget.

## Internal state
- `self.trolley` — the trolley sprite reference.
- `self.hook` — the hook sprite reference.
- `self.rope` — the rope sprite; pixels regenerated each action,
  set to `InteractionMode.REMOVED` when length is 0.
- `self.carrying` — the block sprite currently held by the hook,
  or `None` when no block is carried. Visual cue: a carried block
  renders directly below the hook.
- `self.walls`, `self.blocks`, `self.targets` — per-level lists
  populated in `on_set_level` via tag-based queries.
- `self._step_counter_ui` — the HUD bar showing remaining steps.

## Notable code patterns
- **Dynamic-length rope sprite**. The rope sprite's `pixels`
  array is regenerated each action with shape `(rope_length, 1)`
  filled with palette `4`. When length is 0, the rope is set to
  `InteractionMode.REMOVED`. Reusable any time a game needs a
  variable-extent line connecting two movable parent sprites.
- **Cartesian-gantry collision check**. `_move_trolley`
  separately validates rope cells, hook footprint, and carried-block
  footprint against walls and other blocks at the new position.
  This generalises to any "manipulator with multiple connected
  parts" — each part's new footprint must clear obstacles
  independently.
- **Snap-fall on release**. `_fall(block)` increments `block.y` one
  cell at a time until the block bottom reaches floor or collides
  with another block (or wall). Cheaper than a phase-tick
  animation; reasonable for short falls.
- **Per-mechanic tag layers**. Sprites carry both a role tag
  (`block`, `target`, `wall`, `trolley`, `hook`, `rope`, `floor`,
  `beam`) and a colour tag (`red`, `blue`, `yellow`) where
  applicable. The win predicate iterates targets and matches on
  colour tag; a single helper would generalise to any
  pair-by-colour win condition.
- **Layered render order**. Floor and targets at layer 0 (back),
  beam at 1, walls at 2, blocks at 3, trolley/rope/hook at 4
  (front). When a block is delivered onto a target, the target
  remains visible at its protruding edges so the player can verify
  colour match without having to lift the block.
