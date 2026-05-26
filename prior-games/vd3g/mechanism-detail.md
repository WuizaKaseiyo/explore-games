# vd3g — valley-dig-roll

## Summary

The player edits a binary heightmap of 16×16 cells by clicking cells
to toggle them HIGH↔LOW; coloured marble pawns flow downhill across
the terrain, stepping one cell per click into an adjacent LOW
neighbour using the cardinal priority N→E→S→W, and settling on LOW
cells (until the player toggles them back). Each level wins when
every marble is on its matching-coloured target cell. The only
input is ACTION6. Walls (immutable HIGH cells) at L2 force detours;
linked-anchor pairs (toggleable cells whose flip propagates to a
remote partner) at L3 require coordinating both marbles through
two cells in a single settling pass.

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION6 | Click at display (x, y); engine converts via `camera.display_to_grid` to a logical (col, row) cell. Toggles the cell's terrain state if it is a NORMAL or ANCHOR cell; ANCHOR clicks also flip the linked-partner cell. Walls and target cells are no-ops (still consume one step). After the toggle, the marble settling pass runs. | always |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | dig-toggle + roll-to-low | Single marble red at (5, 5); single target red at (5, 9). All non-target inner cells start HIGH. Witness `[click(5,6), click(5,6), click(5,7), click(5,7), click(5,8), click(5,8)]` — six clicks alternating dig and raise along column 5 to channel the marble four cells south to its target. Step budget 16. |
| 2 | + walls | Marble red at (3, 4); target red at (12, 4). A vertical wall column at col 7 (rows 1-14) with a single gap at (7, 8) forces the marble through an L-shaped detour. Witness 32 clicks: dig+raise pairs along (3,5..3,8)→(4,8..7,8)→(8,8..12,8)→(12,7..12,5), the final raise rolling the marble onto the target. Step budget 50. |
| 3 | + anchor-link pairs | Marble red at (3, 6) → target (12, 6); marble blue at (12, 9) → target (3, 9). Wall column at col 8 (rows 1-14) with the only crossings being two anchor cells at (8, 6) and (8, 9), linked by shared magenta corner-caps. Witness 30 clicks: walk RED to (7, 6) HIGH (8 clicks), walk BLUE to (9, 9) HIGH (6 clicks), click anchor (8, 6) [both anchors flip H→L; RED rolls to (8,6), BLUE rolls to (8,9)], click anchor (8, 6) again [both flip L→H], walk RED east to target (6 clicks), walk BLUE west to target (8 clicks). Step budget 80. |

## Win condition

After the marble settling pass following each click, every marble's
logical cell `(col, row)` equals the cell stored in
`self.marble_targets[marble.name]`. When true, `self.next_level()`
fires. After level 3, the engine's default flow advances past the
last level and calls `self.win()`.

## Lose condition

`self._action_count >= self.max_steps` at the top of `step()`
triggers `self.lose()`. There is no instant-fail collision —
walking into a wall is a no-op (marbles never enter walls); only
step exhaustion ends the run.

## Internal state

- `self.heights` — 16×16 int8 ndarray; per-cell binary height (0 = LOW,
  1 = HIGH). Repainted into the terrain canvas after every click.
- `self.cell_kind` — 16×16 int8 ndarray; per-cell type tag (NORMAL,
  WALL, TARGET_RED, TARGET_BLUE, ANCHOR_MAGENTA). Determines what
  pixel pattern the cell renders to and whether the cell is
  toggleable.
- `self.anchor_pairs` — symmetric `dict[(col, row), (col, row)]`
  mapping each anchor cell to its linked partner.
- `self.marble_targets` — `dict[marble_name, (col, row)]` mapping
  each marble sprite name to the cell it must settle on to win.
- `self.max_steps` — per-level step budget read from
  `level.get_data("max_steps")`.
- `self._step_counter_ui` — `StepCounterHud` (subclass of
  `RenderableUserDisplay`) painting a depleting horizontal bar at
  frame row 0.
- The terrain canvas itself is a 64×64 `Sprite` (tag `terrain`) whose
  `pixels` array is recomputed on every settling pass by
  `_repaint_terrain()`.

## Notable code patterns

- **Single-canvas terrain**. The whole 16×16 logical heightmap is
  rendered into a single 64×64 `Sprite` whose pixels are
  re-stamped from per-cell-kind 4×4 patterns (`PATTERN_LOW`,
  `PATTERN_HIGH`, `PATTERN_WALL`, `PATTERN_TARGET_*`,
  `PATTERN_ANCHOR_*`) every turn. Marbles ride above as separate
  4×4 sprites at multiples of 4. Avoids the 256-cell-sprite
  alternative and keeps mutation cheap.
- **Anchor link propagation**. `_toggle_cell` flips the clicked
  cell, and if it is an anchor, looks up the partner in
  `self.anchor_pairs` and flips that cell too — symmetric dict so
  either anchor click works. The propagation is a single-step,
  non-recursive lookup.
- **Priority-ordered settling pass**. `_settling_pass` sorts
  marbles by name (alphabetical: blue < red lexicographically;
  red < blue if you reverse the sort key — here red wins by name
  ordering) and steps each in turn; an `occupied` set is updated
  in-place so the second marble sees the first's new cell. The
  cardinal direction list is fixed at N→E→S→W to make movement
  fully deterministic.
- **Init-attribute-before-super**. Per-level-state attributes
  (`self.heights`, `self.cell_kind`, `self.anchor_pairs`,
  `self.marble_targets`, `self.max_steps`) are initialised
  BEFORE `super().__init__()` because the engine's
  `NovaBaseGame.__init__` calls `set_level(0)` internally, which
  triggers `on_set_level`, which writes to those attributes.
  Initialising them after `super().__init__()` would clobber
  `on_set_level`'s writes back to zeros and the game would lose
  on every action.
- **Witness 1-click-per-cell economy**. Because marbles on LOW
  cells stay settled, advancing a marble one extra cell costs 2
  clicks (dig the next cell + raise the current one), but the
  final transition into the target cell is free — the raise of
  the cell BEFORE target double-duties as the move-onto-target
  click, since target cells are immutable LOW. So a path of N
  intermediate cells expands to 2 × (N − 1) + 2 = 2N clicks total,
  not 2N + 1.
