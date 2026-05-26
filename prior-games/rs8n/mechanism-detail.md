# rs8n — line-reverse-sweep

## Summary
The player walks a maroon avatar through a 16-cell-square arena scattered with four distinct coloured shape items (hollow pink ring, yellow 2-pixel checkerboard, orange filled blob, blue vertical bar). ACTION5 fires a small sweeper that travels in the avatar's facing direction, picks up every item it crosses, and on hitting a wall or anchor pillar reverses to re-deposit the carried items at their pickup cells in reversed pickup-order — a per-segment in-place reversal. Win condition: every cell with a target outline displayed in the top (and at L3, right-side) preview holds an item whose shape and colour match. Key constraint: the only mechanic that re-orders items is the sweep verb. Side-effects: anchor pillars halt sweeps mid-line and are flanked by access-blocking walls so the anchor cell is geometrically unreachable for the avatar — the anchor's stop-effect is strictly necessary for the per-segment-reversed permutation. At L3, the same sweep verb must be fired along the perpendicular axis (north or south) as well.

## Action mapping

| Action | Semantic | Gate / when valid |
|---|---|---|
| ACTION1 | Face up + walk one cell up (rotate-only if blocked) | not during sweep |
| ACTION2 | Face down + walk one cell down (rotate-only if blocked) | not during sweep |
| ACTION3 | Face left + walk one cell left (rotate-only if blocked) | not during sweep |
| ACTION4 | Face right + walk one cell right (rotate-only if blocked) | not during sweep |
| ACTION5 | Fire a sweeper in the avatar's current facing; multi-tick outgoing+return animation; reverses items along the cardinal segment between the avatar and the first blocker; consumes one step from the budget | only when `sweep_phase` is `idle` |

## Per-level mechanic progression

| Level | Mechanic introduced (or composed) | Specific challenge / constraint |
|---|---|---|
| 1 | M1 = walk + line-reverse-sweep | 4 items in a single row, in wrong order; preview at top shows the target. Witness `[4, 4, 5]` (3 actions, budget 50). |
| 2 | + M2 = anchor partitioning with access-blocking walls | Row 8 has an anchor at (5,8) flanked by walls at (5,7) and (5,9), partitioning the row into two segments that BOTH need reversal; player must execute east-from-west AND west-from-east sweeps, detouring south of the anchor between them. Witness `[4, 5, 2, 4, 4, 4, 2, 4, 4, 4, 4, 1, 1, 3, 5]` (15 actions, budget 100). Without the anchor the reachable permutation group on the row is `{e, σ_full}` (cyclic of order 2) which does NOT contain the target permutation `σ_A σ_B` (in the Klein-four group) — so the level is strictly unwinnable without M2. |
| 3 | + M3 = perpendicular-axis sweeps required by a 2D-grid target | A 3-row × 5-column grid of 14 items + 1 anchor at the centre cell (7,5). The grid's own geometry guards the anchor — every cardinal neighbour of (7,5) is an item, so the avatar can never walk onto the anchor regardless of whether the anchor sprite is present (no extra access-walls needed). The target requires four full-column reverses (cols 5, 6, 8, 9) AND both row-5 segment-reverses across the anchor; the player must rectify items along both axes via 6 sweeps from 6 distinct firing positions outside the grid edges. Witness 31 actions, budget 250. |

## Win condition
After every non-sweep action (and after each sweep completes), iterate the level's `targets` list (`[(cell_x, cell_y, shape_tag, palette), ...]`). For each target cell, verify an item-tagged sprite at the pixel position with the matching shape tag and matching dominant palette. If all match, fire `self.next_level()`. After L3's win-check passes, the engine itself fires `self.win()`.

## Lose condition
Step counter (`StepCounterHud`) drains by one per processed action input. When the current value reaches zero (checked after every non-sweep action), `self.lose()` fires. No other lose path — items are not destroyed during a sweep, there are no hazards, and the sweep is its own inverse so no soft-locks are possible.

## Internal state
- `step_counter_hud` — `StepCounterHud(RenderableUserDisplay)` with `(budget, current)`; rendered as a row-63 horizontal bar.
- `sweep_phase` — `"idle"` | `"outgoing"` | `"return"`; gates whether `step()` advances the sweep animation or processes a new action input.
- `sweep_axis` — `(dx, dy)` cardinal direction of the active sweep (multiples of CELL = 4).
- `sweep_cursor` — current pixel position of the sweeper sprite during animation.
- `sweep_pickups` — FIFO queue of `(item, original-cell)` pairs picked up during the outgoing leg.
- `sweeper_sprite` — the visible cursor sprite during the animation; created at ACTION5 and removed on sweep completion.
- `return_drop_map` — `{cell: item}` built at the start of the return leg; on each return tick, if the sweeper is at a key in this map, the corresponding item is re-placed at that cell.

## Notable code patterns
- **Multi-tick sweep animation as a phase machine.** ACTION5 transitions to `outgoing`; subsequent `step()` calls advance the cursor one cell per tick without firing `complete_action()`. When the cursor reaches a blocker the phase flips to `return`; subsequent ticks retreat the cursor and drop items as scheduled. Only when the cursor reaches the player's cell does `complete_action()` fire — so one ACTION5 input consumes exactly one step against the budget regardless of segment length. (Same idiom as cn04 / sk48 / r11l multi-frame animations.)
- **Reverse-mapping by cell-keyed dictionary.** During the outgoing leg, the `(item, cell)` pair list is appended in pickup order. At the start of the return leg, the list is converted into `{cell: item}` where each `item_k` is mapped to the cell of `item_{n+1-k}` (i.e. reversed-pair). The return leg simply drops at every visited cell that's a key in the map. Cleaner than tracking two parallel lists with on-the-fly index arithmetic.
- **`BlockingMode.BOUNDING_BOX` on items, default `PIXEL_PERFECT` elsewhere.** Items have transparent corners; default pixel-perfect collision skipped them at their cell's top-left, breaking `get_sprite_at(x, y, "item")`. `BOUNDING_BOX` on items only — leaving the perimeter walls and other sprites at PIXEL_PERFECT so the perimeter's `-1` interior lets the player walk through interior cells — restores correct cell-level item detection.
- **Anchor + access-walls combo for strict counterfactual (L2).** An anchor alone does not strictly require itself, because the avatar could position itself at the anchor cell (in the absence of the anchor) and fire from there to achieve the same partial sweep. Flanking the anchor cell with walls (at the cells immediately above and below) makes the anchor cell *geometrically unreachable* for the avatar; the anchor's sweep-stop role is then the only way to partition the line.
- **Anchor-by-grid-geometry at L3.** When the anchor sits inside a dense 3×5 grid where every cardinal neighbour is an item, the surrounding items themselves block the avatar from ever reaching the anchor cell — no extra access-walls are needed. This is the cleaner construction whenever the puzzle naturally places the anchor inside a packed grid: the items double as access blockers.
- **Single 64×64 perimeter-wall sprite with brick pattern only on the outer 4-cell ring.** Reduces sprite count vs. 60 per-cell wall instances and renders a uniform border; the `-1` interior is essential so other sprites can occupy interior cells without collision.
- **Visible facing via the avatar's white "eye-stripe" rotated by `set_rotation`.** The avatar sprite has `0` (white) at row 0 columns 1-2 and `13` (maroon) elsewhere. Engine rotation moves the eye-stripe to the appropriate side, signalling the avatar's facing direction without any external HUD or arrow glyph.
