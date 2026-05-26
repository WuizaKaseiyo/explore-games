# Game spec — rs8n  (revision 4 — L3 redesigned as a 3×5 grid)

> **Revision history**
> - **R3** (post initial user feedback): dropped the L3 colour-shifter; made L2's anchor strictly necessary via access-blocking walls; required east-and-west sweeps at L2; added vertical-axis sweeps at L3 via a separate column-10 segment; bumped budgets L2 70→100, L3 120→250.
> - **R4** (this revision, per second user note): rebuilt L3 as a **single 3×5 grid** with one anchor at the centre cell (7,5) — instead of two separate perpendicular line segments. The grid geometry makes the anchor cell intrinsically unreachable (every cardinal neighbour is an item), so no explicit access-walls are needed for the L3 anchor. The target is a 2D permutation that requires four full-column reverses AND both row-5 segment-reverses; the player must rectify items along both axes. L2 unchanged from R3.

## 1. Title
*Line-Reverse Sweeper.* (Working title; never visible in-game.)

## 2. Mechanic family
**`line-reverse-sweep`** with **anchor-partition** and **multi-direction-axis** composition. A walking avatar fires sweeps in its facing direction that pick up every item along a cardinal line, then re-deposit the items in reversed pickup-order — a per-segment in-place reversal. Anchor pillars partition lines so the player must fire from both sides of the anchor to reverse both segments; access-blocking walls make the anchor's stop-effect strictly necessary. At L3 the same verb is required in the vertical axis as well. Prior categories used: **objectness** (items as persistent sprites that get picked up and re-placed) + **basic geometry & topology** (sweep produces a reflection-permutation on a 1-D segment whose endpoints are the avatar position + the first blocker; segments are independent under anchor partitioning).

## 3. Sprite roster
Grid is 64×64 with cell stride 4 (a 16×16 logical grid). Every gameplay-relevant sprite is 4×4 with internal pixel structure per checklist item 20.

| Name | Pixels (4×4) | Palette | Tags | Role |
|---|---|---|---|---|
| `player` | `[[13,0,0,13],[13,13,13,13],[13,13,13,13],[13,13,13,13]]` | 13 (maroon) + 0 (white) eye-stripe | `["player"]`, layer 2, collidable | Avatar; rotation moves the eye-stripe to the facing edge. |
| `wall` | `[[3,3,3,3],[3,5,5,3],[3,5,5,3],[3,3,3,3]]` | 3 grey + 5 black | `["wall","blocker"]`, layer 0, collidable | 4×4 interior wall used for perimeter (assembled into a single 64×64 sprite) and as access-blocking sentinels next to each anchor. |
| `perimeter_walls` | 64×64 with brick pattern only on the outer 4-cell ring | 3 + 5 | `["wall","blocker"]`, layer 0, collidable | Single sprite implementing the playfield perimeter. |
| `anchor_pillar` | `[[5,3,3,5],[3,1,1,3],[3,1,1,3],[5,3,3,5]]` | 5 black corners + 3 grey + 1 off-white centre | `["anchor","blocker"]`, layer 1, collidable | Visually distinct from walls (corners + bright centre = "pillar"); halts both sweep and walk. |
| `item_pink_ring` | `[[-1,7,7,-1],[7,-1,-1,7],[7,-1,-1,7],[-1,7,7,-1]]` | 7 pink | `["item","shape_ring"]`, layer 1, collidable, BOUNDING_BOX | Movable item. |
| `item_yellow_checker` | `[[11,-1,11,-1],[-1,11,-1,11],[11,-1,11,-1],[-1,11,-1,11]]` | 11 yellow | `["item","shape_checker"]`, layer 1, BOUNDING_BOX | Movable item. |
| `item_orange_blob` | `[[-1,12,12,-1],[12,12,12,12],[12,12,12,12],[-1,12,12,-1]]` | 12 orange | `["item","shape_blob"]`, layer 1, BOUNDING_BOX | Movable item. |
| `item_blue_bar` | `[[-1,9,9,-1],[-1,9,9,-1],[-1,9,9,-1],[-1,9,9,-1]]` | 9 blue | `["item","shape_bar"]`, layer 1, BOUNDING_BOX | Movable item. |
| `sweeper` | `[[-1,2,2,-1],[2,2,2,2],[2,2,2,2],[-1,2,2,-1]]` | 2 light grey | `["sweeper"]`, layer 3, INTANGIBLE | Animation-only cursor during a sweep. |
| `preview_*` (4 variants) | same pixels as the matching item | as item | `["preview"]`, layer 0, INTANGIBLE | Cosmetic-only: top row + (L3) right column show the desired final item arrangement. |

Palette in use: `{0,1,3,4,5,7,9,11,12,13}`. Ten values — distinct from the cautionary `{4,8,9}` cluster called out in `negative-similarity-check.md`.

## 4. Level progression, mechanic enumeration, and witness solutions

All three levels share `grid_size = (64,64)`, the perimeter wall ring, and `BACKGROUND_COLOR = PADDING_COLOR = 4`. **CELL = 4** — every gameplay sprite sits at pixel positions that are multiples of 4. Preview sprites render at logical row y=1 (and at logical column x=13 for L3).

### Level 1 — base dynamic system

**Setup:**
- Perimeter walls.
- Row y=8 items: (5,8)=`item_pink_ring`, (6,8)=`item_yellow_checker`, (7,8)=`item_orange_blob`, (8,8)=`item_blue_bar`.
- Avatar at (2,8) facing east (rotation 90).
- Preview at y=1: `blue_bar`@(5,1), `orange_blob`@(6,1), `yellow_checker`@(7,1), `pink_ring`@(8,1) — the desired *reversed* arrangement.
- `step_budget = 50`.
- Targets: `[(5,8,"shape_bar",9), (6,8,"shape_blob",12), (7,8,"shape_checker",11), (8,8,"shape_ring",7)]`.

**Mechanics required by the witness (N = 1):**
- **M1 — line-reverse sweep.** ACTION5 fires a sweep from the cell adjacent to the avatar in the avatar's facing direction; sweeper advances until it hits a wall/anchor/edge; items along the path are picked up in order then reassigned by reverse index `(item_k → cell_{n+1-k})` on the return leg.

**Necessity per mechanic:**
- *L1 cannot be solved without triggering M1 because* every target cell `(5..8, 8)` requires an item whose shape+colour differs from the item that starts there. Walking does not move items (items are collidable; the avatar rotates without moving when blocked). The sweep is the only verb that re-assigns items between cells; without firing it, every cell stays at its initial item.

**Witness solution:** `[ACTION4, ACTION4, ACTION5]` (3 actions, budget 50).

**Difficulty justification:**
- (a) **Random-resistance.** A random agent can occasionally stumble in (the witness is 3 actions); allowed per L1 = tutorial.
- (b) **Human-tractable.** ~30 seconds. Player sees four items + preview, presses keys, discovers ACTION5 reverses, solves.
- (c) **Planning depth.** *No strict planning requirement* — L1 is the discovery gate.
- (d) **Step budget.** 50 (≈17× witness); generous.

### Level 2 — base system + 1 new mechanic

**Setup:**
- Perimeter walls.
- Row y=8 items + anchor: (3,8)=`item_pink_ring`, (4,8)=`item_yellow_checker`, anchor at (5,8), (6,8)=`item_orange_blob`, (7,8)=`item_blue_bar`.
- **Access-blocking walls** at (5,7) and (5,9) — these flank the anchor cell so that the cell at (5,8) is unreachable for the avatar. Without these walls the avatar could detour around the anchor (via row 7 or row 9) and stand at (5,8) — which would let the avatar produce partial sweeps without using the anchor. With them, the anchor's stop-effect is the only way to partition row 8.
- Avatar at (1,8) facing east.
- Preview at y=1: `yellow_checker`@(3,1), `pink_ring`@(4,1), gap at (5,1), `blue_bar`@(6,1), `orange_blob`@(7,1) — the *both-segments-reversed* target.
- `step_budget = 100`.
- Targets: `[(3,8,"shape_checker",11), (4,8,"shape_ring",7), (6,8,"shape_bar",9), (7,8,"shape_blob",12)]`.

**Mechanics required by the witness (N+1 = 2; +1 new):**
- **M1 — line-reverse sweep** (carried from L1).
- **M2 — anchor partitioning with strict counterfactual access.** The anchor pillar halts the sweep mid-line; combined with the access-blocking walls at (5,7)/(5,9) the anchor cell is geometrically unreachable for the avatar, so the only way to partition the row 8 line is via the anchor.

**Necessity per mechanic:**
- *L2 cannot be solved without triggering M1 because* the targets at (3..7, 8) require both segment-A and segment-B reversed from their initial configurations. Walking does not move items. Without ACTION5 ever firing, the row stays in its initial state and no target is satisfied.
- *L2 cannot be solved without triggering M2 because* without the anchor at (5,8) the row-8 line is unblocked between the perimeter walls at x=0 and x=15, so the only reachable permutations of the four items via sweeps are `{identity, full-row-reverse}` (the cyclic group of order 2 generated by the full-line involution). The target permutation is the product of two transpositions `(ring↔checker, blob↔bar)`, which lies in the *Klein four-group* `{e, σ_A, σ_B, σ_A σ_B}` — NOT in `{identity, full-reverse}`. So the target is unreachable without anchor-partitioning. The access-blocking walls at (5,7) and (5,9) ensure the avatar cannot bypass the missing anchor by detouring to cell (5,8) and using its own position as a partition point: with those walls the avatar geometrically cannot stand at (5,8). Concretely: remove the anchor + leave the walls, and target permutation is unreachable; remove the anchor + remove the walls, the avatar can still reach (5,8) but at L2's puzzle constraints this only matters as an EQUIVALENT replacement of the anchor's role — what matters is that with the level as-designed, neither anchor nor avatar-at-(5,8) is available without the anchor sprite.

**Witness solution:**
```
[ACTION4, ACTION5,                               # walk east to (2,8), sweep east → segment A reversed
 ACTION2, ACTION4, ACTION4, ACTION4,             # south to (2,9), east to (4,9), east-blocked at (5,9) wall (rotate-only)
 ACTION2, ACTION4, ACTION4, ACTION4, ACTION4,    # south to (4,10), east 4× to (8,10)
 ACTION1, ACTION1,                               # north 2× to (8,8)
 ACTION3, ACTION5]                               # face west (blocked by item, rotate-only), sweep west → segment B reversed
```
**15 actions**, budget 100.

**Difficulty justification:**
- (a) **Random-resistance.** Near-zero within budget 100. The witness requires the avatar to pre-position on BOTH sides of the row, separated by a multi-cell detour around the access walls.
- (b) **Human-tractable.** ~3 minutes. The player learns from L1 that ACTION5 reverses; here they discover that (i) the row has two segments separated by an anchor, (ii) the anchor cannot be reached or walked-around at row level, and (iii) they need to detour south to swap sides.
- (c) **Planning depth.** Moderate post-discovery planning. Post-discovery decision space at level start: at least 4 plausible first actions — ① walk east + sweep east first; ② walk south + east + north then sweep west first; ③ sweep east immediately from (1,8); ④ walk south first. Plausible-but-wrong path: option ③ (sweep east from (1,8) facing east) — sweeper enters (2,8) → empty floor, then (3,8) → pickup ring, (4,8) → pickup checker, anchor stops, reverses segment A. *This actually works for segment A*, but the player then realises they've used one ACTION5 with avatar still at (1,8), needs to detour ~12 more actions to reach (8,8), then face west, sweep west. Net same; not a wrong path so much as a slightly different one. The genuinely-wrong path is option ② (going east first via south detour, then sweep west, then return to sweep east from west) — this works too but doubles the detour cost. The witness's reasoning chain: minimise detour by reversing segment A first (avatar is already west of A) before walking to the east side.
- (d) **Step budget.** 100 (≈7× witness); generous, plenty of cushion for exploratory sweeps + walks.

### Level 3 — system + 1 new mechanic  (revision 4: 3×5 grid with central anchor)

**Setup:**
- Perimeter walls.
- A 3-row × 5-column **grid of items** at rows 4..6 (3 rows) and columns 5..9 (5 columns); 14 items + 1 anchor at the centre cell (7,5). Concretely:
  - Row 4: `(5,4)=pink_ring`, `(6,4)=blue_bar`, `(7,4)=yellow_checker`, `(8,4)=orange_blob`, `(9,4)=pink_ring`.
  - Row 5: `(5,5)=orange_blob`, `(6,5)=pink_ring`, **anchor at (7,5)**, `(8,5)=blue_bar`, `(9,5)=yellow_checker`.
  - Row 6: `(5,6)=yellow_checker`, `(6,6)=orange_blob`, `(7,6)=blue_bar`, `(8,6)=pink_ring`, `(9,6)=orange_blob`.
- **No explicit access-blocking walls at the anchor** — every cell cardinally adjacent to (7,5) is itself an item (collidable), so the avatar can never walk onto the anchor cell regardless of whether the anchor sprite is present. The grid geometry itself guarantees the anchor's strict counterfactual.
- A matching **3×5 target-preview grid** rendered three rows below at rows 11..13, columns 5..9, with a gap at (7,12) corresponding to the anchor position — so the player can compare cell-by-cell.
- Avatar starts at (1,5) facing east.
- `step_budget = 250`.
- 14 target tuples in `level.get_data("targets")` covering every non-anchor cell of the 3×5 grid (see `rs8n.py` for the literal list).

**Mechanics required by the witness (N+1 = 3; +1 new at L3):**
- **M1 — line-reverse sweep** (carried from L1).
- **M2 — anchor partitioning** (carried from L2). At L3 the anchor sits at the centre of a 3×5 grid; its row-5 partition splits row 5 into two 2-cell segments. The anchor cell is geometrically unreachable because all four cardinal neighbours are item cells (collidable).
- **M3 — perpendicular-axis (vertical) sweeps required by the 2D-grid target.** The 3×5 target permutation rearranges items both *horizontally* (the anchor row needs both 2-cell segments reversed) and *vertically* (columns 5, 6, 8, 9 each need a full-column reverse swapping `(col,4)↔(col,6)` with the row-5 middle cell as the reversal fixed point). Per user authorisation, the *requirement to use the perpendicular axis* counts as the new mechanic for L3 even though the underlying verb is the same `ACTION5 → sweep in facing direction`.

**Necessity per mechanic:**
- *L3 cannot be solved without triggering M1 because* 11 of the 14 target cells require an item shape+colour that differs from the cell's initial occupant. Walking does not move items. Without ACTION5 ever firing, the grid stays in its initial state and the win predicate cannot fire.
- *L3 cannot be solved without triggering M2 because* the row-5 target permutation requires reversing both 2-cell segments `(5,5)↔(6,5)` and `(8,5)↔(9,5)` while leaving the segments un-mixed across the anchor. Without the anchor at (7,5), row 5 has four items at columns 5,6,8,9 with cell (7,5) empty; the reachable permutation group on these four cells under any horizontal sweep is only `{e, full-row-reverse}` (cyclic order 2), and a full-row reverse would swap `(5,5)↔(9,5)` and `(6,5)↔(8,5)` — NOT the target's `(5,5)↔(6,5), (8,5)↔(9,5)` pairing. The target's row-5 permutation lies in the *Klein four-group* `{e, σ_left, σ_right, σ_left σ_right}` reachable only with anchor-partitioning, and not in the cyclic-2 group reachable without.
- *L3 cannot be solved without triggering M3 because* the column targets require items to move between row 4 and row 6 (e.g. target (5,4) requires `shape_checker/11` whose only initial instance on column 5 is at (5,6); similarly for columns 6, 8, 9). Horizontal sweeps only permute items along the row they are fired on — they never move an item between row 4 and row 6. The only verb that can swap `(col,4)↔(col,6)` for any column is a sweep along that column (north-from-above or south-from-below). The 3×5 target requires this swap on four separate columns (5, 6, 8, 9); without those four vertical sweeps the target is unreachable.

**Witness solution (31 actions, budget 250):**
```
# Phase 1 — Walk (1,5) → (5,3), north of the grid.
[ACTION1, ACTION1, ACTION4, ACTION4, ACTION4, ACTION4,
 # Rotate to face south (item at (5,4) blocks the walk; ACTION2 still rotates), sweep south through column 5.
 ACTION2, ACTION5,

 # Phase 2 — Walk (5,3) → (4,5), west of the grid.
 ACTION3, ACTION2, ACTION2,
 # Rotate to face east (item at (5,5) blocks the walk), sweep east through row 5's west segment.
 ACTION4, ACTION5,

 # Phase 3 — Walk (4,5) → (6,3), back north for column 6.
 ACTION1, ACTION1, ACTION4, ACTION4,
 ACTION2, ACTION5,

 # Phase 4 — Walk (6,3) → (8,3), continue east for column 8.
 ACTION4, ACTION4,
 ACTION2, ACTION5,

 # Phase 5 — Walk (8,3) → (9,3), one cell east for column 9.
 ACTION4,
 ACTION2, ACTION5,

 # Phase 6 — Walk (9,3) → (10,5), east then south for row 5's east segment.
 ACTION4, ACTION2, ACTION2,
 # Rotate to face west (item at (9,5) blocks the walk), sweep west.
 ACTION3, ACTION5]
```

Sweep order (6 sweeps): col 5 south → row 5 east → col 6 south → col 8 south → col 9 south → row 5 west. Column 7 is intentionally never swept — it has the anchor at (7,5) splitting it into single-cell segments where reversal is a no-op, and the target leaves (7,4) and (7,6) at their initial values.

**Difficulty justification:**
- (a) **Random-resistance.** Near-zero within budget 250. The witness requires 6 ACTION5 sweeps from 6 geometrically-distinct firing positions (one north of each non-anchor column, one west and one east of the anchor row); each firing position is one cell outside the 3×5 grid edge, and reaching each requires several walks (the avatar must walk *around* the grid because items block direct passage through). Joint probability of stumbling into all six firing positions in any valid order under random play is well below 1/10,000.
- (b) **Human-tractable.** ~5–7 minutes total. After L2 the player has internalised that the sweep reverses a line segment between the avatar and the first blocker; L3 generalises this to a 2D grid where (i) the central anchor partitions the anchor row into two reversible segments, and (ii) the perpendicular axis is now mandatory because items need to move between row 4 and row 6. The challenge is route planning around the grid (the firing positions are scattered along the grid's top edge and along its left/right sides; the avatar must walk a loop that visits them all).
- (c) **Planning depth — Challenging.** The post-discovery decision space at level start contains roughly 6 mandatory sweeps × (orderings) × (firing-side choice for each full-column reverse: from north or from south) = many candidate witnesses. The order of sweeps is **almost** order-independent in its effect on the target (the row-5 middle cells (5,5),(6,5),(8,5),(9,5) are the fixed points of their column reversals, so column sweeps don't disturb row-5 cells; row-5 sweeps don't disturb non-row-5 cells in their columns) — but the total walk cost depends strongly on the order. A trivial heuristic that fails: *"execute all four column sweeps first, then both row sweeps."* — this heuristic produces a witness around 35–40 actions because the avatar has to traverse the entire top edge of the grid for the four column sweeps and then walk all the way down and around to the row firing positions. A more efficient ordering interleaves a row sweep next to a column sweep when their firing positions are nearby (e.g., col 5 north → row 5 west; col 9 north → row 5 east). The witness above uses one such interleaving and lands at ~31 actions. The post-discovery player who notices *"the row-5 west firing position is right under the col-5/6 firing positions"* finds the shorter route; the player who treats horizontal and vertical sweeps as two monolithic phases doesn't. This is genuine planning beyond pattern-matching.
- (d) **Step budget.** 250 (≈8× witness); generous, exploration-friendly. Even a player who walks an extra loop around the grid and re-fires one or two sweeps in the wrong direction (which is an involution and self-undoes on a second fire) has plenty of cushion.

## 5. Action mapping
`available_actions = [1, 2, 3, 4, 5]`. ACTION6 (click) and ACTION7 (undo) omitted.

| Slot | Semantic | Notes |
|---|---|---|
| ACTION1 | Face up + walk 1 (rotate-only if blocked) | |
| ACTION2 | Face down + walk 1 (rotate-only if blocked) | |
| ACTION3 | Face left + walk 1 (rotate-only if blocked) | |
| ACTION4 | Face right + walk 1 (rotate-only if blocked) | |
| ACTION5 | Fire sweep in current facing direction (multi-tick animation) | Distinctive verb; only valid when `sweep_phase == idle`. |

## 6. HUD and per-game state
### HUD
`StepCounterHud(RenderableUserDisplay)` — single row-63 horizontal bar; pink (palette 7) shrinking left-to-right over off-black (4). Reset to `level.get_data("step_budget")` on `on_set_level`; decremented by 1 per processed action input.

### Per-game state
- `step_counter_hud: StepCounterHud`.
- `sweep_phase: str` in `{"idle","outgoing","return"}`.
- `sweep_axis: tuple[int,int]` cardinal direction of the active sweep (multiples of CELL).
- `sweep_cursor: tuple[int,int]` current sweeper pixel position.
- `sweep_pickups: list[tuple[Sprite, tuple[int,int]]]` FIFO queue of `(item, original-cell)` pairs.
- `sweeper_sprite: Sprite | None`.
- `return_drop_map: dict[tuple[int,int], Sprite]` built at start of return leg.

### Sweep state machine
On ACTION5 from `idle`: capture facing direction, spawn sweeper, transition to `outgoing`, decrement budget by 1, return without `complete_action()`. Each `outgoing` tick: check the cursor cell for off-grid / blocker (if so, step back and transition to `return`); otherwise pick up any item, advance the cursor one cell. Each `return` tick: drop the scheduled item if the cursor cell is a key in `return_drop_map`; if the cursor would step onto the player's cell, finalise (remove sweeper, check win/lose, `complete_action()`); otherwise advance the cursor one cell backward.

Determinism preserved (no `random.random()` in `step()`).

## 7. Win condition
After every action (and at the end of every sweep animation), iterate `level.get_data("targets")` — a list of `(cell_x, cell_y, shape_tag, palette)` tuples. For each target cell, check that an `item`-tagged sprite is at the cell's pixel position, has the named shape tag, and has the named dominant palette. If all hold, fire `self.next_level()`; after L3's win-check returns True, the engine fires `self.win()`.

## 8. Lose condition
`self.step_counter_hud.current <= 0` checked after every non-sweep action. If True, fire `self.lose()`. No other lose path.

## 9. Novelty note
Closest taxonomy entries:
- **vc33 row-column-swap-stripe** — distinguishing rule: vc33 cyclically slides whole rows/columns by one position per click; `rs8n` reverses an arbitrary cardinal segment (involutive, not cyclic), chosen at fire-time by avatar position + facing + anchor placement, on a 2D arena where items are scattered.
- **lp85 button-permutation-puzzle** — distinguishing rule: lp85 applies fixed pre-coded permutations whose pattern the player must memorise per-button; `rs8n` applies a single geometry-derived permutation rule (segment-reversal) whose *locus* depends on player choice.
- **r11l tethered-throw-placement** — distinguishing rule: r11l throws a single piece toward a click target; `rs8n` reverses an entire cardinal segment in place.

Closest prior-game entries (`prior-games/index.md`, 46 entries):
- **qx7p column-shift-row-align** — distinguishing rule: qx7p slides columns past a scan line (cyclic translation); `rs8n` reverses arbitrary segments (involutive permutation) chosen at fire-time, in both axes (L3).
- **vt6q grapple-anchor-yank** — distinguishing rule: vt6q's grapple is a single-piece translation toward an anchor; `rs8n`'s sweep is an n-item segment-reversal.
- **qn7w pulse-chain-eject** — distinguishing rule: qn7w fires momentum through a pre-arranged chain ejecting only the terminal ball; `rs8n` moves every item in the swept segment and reverses their order.

The negative-similarity check (per `mechanic-novelty/negative-similarity-check.md`) was performed against r11l, su15, and vt6q L1 frames. No prior overlaps `rs8n`'s L1/L2/L3 visuals on three or more of the eight surface dimensions; the core dynamic — segment-reversal as the primary verb, in either axis — is implemented by no prior.
