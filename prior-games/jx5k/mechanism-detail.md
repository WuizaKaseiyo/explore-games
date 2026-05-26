# jx5k — constellation-edge-link

## Summary
The player constructs a small multigraph by pair-clicking coloured node sprites at fixed positions on a 32×32 playfield. ACTION6 selects a node (a halo lights it) and a second ACTION6 on a different node cycles the edge state for that pair through `[no edge → single edge → no edge]` at L1/L2 or `[no edge → single edge → double edge → no edge]` at L3. Each node carries a small ring of pip markers showing its target degree; pips fill as edges attach. Win = every node's filled-pip count equals its target. ACTION5 (active at L2 and L3) cycles the selected node's colour through the level's palette, and edges only connect same-colour endpoints — so the L2 / L3 witness must recolour mismatched starting nodes before required edges become legal. The lose condition is step-counter exhaustion (the universal energy-bar pattern).

## Action mapping

| Action | Semantic (game-specific) | Gate / when valid |
|---|---|---|
| ACTION5 | Cycle the selected node's colour through the level palette (`[blue, red]` at L2/L3); auto-deselect after cycling | A node must currently be selected; gated out at L1 by `_get_valid_actions` |
| ACTION6 | Click at display `(x, y)`. Select-with-no-current-selection / advance-edge-cycle-on-pair / remove-edge-on-edge-sprite-click (L3) / deselect-on-empty. Edge-cycle advances are **rejected** if they would push either endpoint past its target degree (a node already at target cannot accept more incoming edges) | Always valid |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 (edge-link with degree target) — base dynamic system | 4 corner nodes (target degree 2 each); witness builds the perimeter 4-cycle. Witness `[click(16,16), click(48,16), click(48,16), click(48,48), click(48,48), click(16,48), click(16,48), click(16,16)]` (8 ACTION6s using display coordinates). |
| 2 | + M2 (node-colour-cycle + same-colour-edge constraint) — recolour mismatched nodes before edges become legal | 5 nodes (cross + centre) starting `[red, blue, red, blue, red]`; target degrees `[3, 3, 3, 3, 4]` require connecting every adjacent pair across colour boundaries. Witness `[click(32,10), action5, click(32,54), action5, then 8 edges as 16 paired ACTION6s]` (20 actions). |
| 3 | + M3 (multi-edge / 3-state cycle) — pair-click on existing edge advances `single → double` instead of removing | 4 diamond nodes, target degrees `[4, 2, 4, 2]`. Target degree 4 on n0 (and on n2) is unsatisfiable with single edges only on a 4-node graph (max degree 3 to 3 distinct neighbours), forcing a parallel edge. Witness recolours n1 and n3 (4 actions), builds 4 single edges (8 actions), then doubles n0–n2 (4 actions = 2 click pairs advancing the cycle). Witness `[click(32,16), action5, click(32,48), action5, then n0-n1, n0-n3, n1-n2, n2-n3, n0-n2 single, n0-n2 double]` (16 actions). |

## Win condition

After every successful action, `_check_win()` walks every node and computes its degree (sum of edge multiplicities incident on it). Win predicate is `all(self._compute_node_degree(name) == self._target_degrees[name] for name in self._target_degrees)`. When True, fire `self.next_level()` (or `self.win()` on the last level via the engine's `next_level` → `win` chain).

## Lose condition

`self.lose()` fires when `self._step_remaining <= 0`. The energy bar drains 1 per action; reaching 0 fires lose. No other lose path — the multi-edge cycle is fully reversible at L3 (a pair-click on `double` advances to `no edge`), so the player can always recover from a wrong edge.

## Internal state

- `self._selected_node: str | None` — name of the currently selected node; cleared on every successful action and on rejected edge attempts. Visible cue: `node_halo` sprite is TANGIBLE (orange ring) and repositioned around the selected node.
- `self._reject_flash_phase: int` — counts down from 6 to 0 for the frames following a rejected edge attempt (cross-colour or invalid line); decrements at the top of every step.
- `self._step_remaining: int` — actions remaining; per-level budget initialised in `on_set_level` from `level.get_data("step_budget")`. Surfaced via the bottom-row `StepCounterHud` widget.
- `self._level_palette: list[int]` — palette of legal colour values for the current level (`[NODE_BLUE]` at L1; `[NODE_BLUE, NODE_RED]` at L2 and L3).
- `self._max_edge_multiplicity: int` — max parallel edges per pair at the current level (1 at L1/L2, 2 at L3).
- `self._edge_state: dict[tuple[str, str], int]` — current multiplicity per node-pair (`(name_i, name_j)` with `name_i < name_j`).
- `self._node_color: dict[str, int]` — current palette value per node.
- `self._node_positions: dict[str, tuple[int, int]]` — fixed grid coordinates per node, copied from level data.

## Notable code patterns

- **Two-sprite-swap idiom for node colour**: every level pre-places all three node-colour variants (`<name>__colour_blue`, `<name>__colour_red`, `<name>__colour_yellow`) at the same cell; `_set_node_color` swaps `InteractionMode.TANGIBLE` ↔ `REMOVED` between the old and new variants. Cleaner than rewriting pixels.
- **Pre-built edge sprite pool with multiplicity**: for each pair `(i, j)` and each multiplicity index `k ∈ {0, ..., max_multiplicity-1}`, a Bresenham-rasterised line sprite (`edge__<i>__<j>__<k>`) is pre-built at level construction with palette-15 line pixels and palette `-1` transparency elsewhere. Toggling an edge swaps strand TANGIBLE / REMOVED. The k=1 variant is shifted 1 cell perpendicular to the edge axis so a double-edge renders as two visibly parallel strands.
- **Pip slot two-sprite-swap**: each pip slot has both an `pip_empty__<name>_<idx>` (palette 3 grey) and `pip_filled__<name>_<idx>` (palette 12 orange) at the same cell; `_refresh_pips` walks the slots and TANGIBLE-swaps based on the node's current degree.
- **Edge-line legality check via Bresenham + sprite-bbox overlap**: `_line_passes_through_other_node` rasterises the proposed line and checks whether any interior cell is inside any other node's rendered bounding box. This catches the canonical "chord through the centre" case at L2 without needing an explicit wall sprite.
- **Click hit-test that respects sprite transparency**: `_find_edge_at` checks both the sprite's bounding box AND the actual pixel value at the clicked cell — clicks on the transparent area of a diagonal edge sprite are not counted as edge clicks. Lets the player click *between* edges of a multi-edge bundle without ambiguity.
- **`_get_valid_actions` per-level gating**: at `_current_level_index == 0` returns `[ACTION6]` only; at L2/L3 returns `[ACTION5, ACTION6]`. Keeps L1 truly minimal so the player learns M1 alone first.
