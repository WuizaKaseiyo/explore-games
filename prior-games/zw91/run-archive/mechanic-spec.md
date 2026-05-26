# mechanic-spec.md — `zw91`

## 1. Title
Inflate-Fit-Burst — a single avatar whose own footprint size is a verb.

## 2. Mechanic family
**Family tag:** `inflate-fit-burst`.

The player controls one mobile avatar whose footprint cycles through three sizes (small=4×4, medium=8×8, large=12×12 cells). Arrows step the avatar one tile (4 cells) cardinally; ACTION5 cycles the avatar's size up by one notch (small→medium→large; from large, the avatar enters an **overloaded** intermediate state visible as a persistent halo, and the next ACTION5 fires a one-shot **burst** that destroys nearby shove-blocks and breakaway-walls, resetting the avatar to small). When ACTION5 grows the avatar over a **shove-block**, each block whose cells lie inside the *new* footprint is rolled in the cardinal direction `sign(block.center − avatar.center)` (with the dominant axis breaking ties; if both axes tie in magnitude, east wins). The block rolls one tile at a time in the push direction and continues to roll as long as the next-tile destination is empty; it parks at its current position the moment the next tile in the push direction is a collidable wall, breakaway-wall, or another shove-block (or the perimeter). If the block's *first* attempted destination is already blocked (so it cannot move at all), the entire inflate cancels and any blocks that already moved this cycle roll back to their pre-cycle positions. The win condition for a level is that the avatar's top-left tile and current size match every **socket** placed in the level (sockets are sized hollow rings declared per-level).

Core knowledge priors used: **objectness** (avatar, blocks, sockets, walls, breakaway-walls as persistent entities); **basic geometry / topology** (footprint size matching socket size; inside / outside of a hollow ring; adjacency for inflate-push); **basic physics** (push-block radial slide that stops at obstacles; burst destruction zone). No agentness — there are no autonomous NPCs.

## 3. Sprite roster
- **`avatar_small`**: 4×4 pixels. Palette 12 (orange) outer with palette 13 (maroon) corners and a centre cross of palette 1 (off-white). Tag `["avatar"]`. Role: player; movable; cycles to medium on ACTION5.
- **`avatar_med`**: 8×8 pixels. Palette 12 outer ring (1-cell thick), palette 13 inner ring (1-cell), centre 4×4 of palette 12 with a palette-1 cross at the centre 2×2. Tag `["avatar"]`. Role: player at medium size.
- **`avatar_large`**: 12×12 pixels. Palette 12 outer ring (2-cell thick), palette 13 inner band, centre 6×6 of palette 12 with a palette-1 cross at the centre 4×4. Tag `["avatar"]`. Role: player at large size.
- **`overload_halo`**: 16×16 pixels. Hollow ring in palette 7 (pink) with palette 12 spokes — sits centred on `avatar_large` when the player has cycled past large into the **overloaded** state. Tag `["overload"]`, layer 5 (above avatar). Role: visible cue for "burst-loaded".
- **`wall_strip_h`**: 64×4 pixels. Palette 4 (off-black) base with palette 5 (black) brick-grout pattern (alternating cells per row, 2-row tall bricks). Tag `["wall"]`. Role: top / bottom border.
- **`wall_strip_v`**: 4×56 pixels. Same brick pattern, transposed. Tag `["wall"]`. Role: left / right border.
- **`wall_block`**: 4×4 pixels. Same brick pattern as the strips. Tag `["wall"]`. Role: interior wall tile (re-used to assemble L2 / L3 columns).
- **`breakaway_wall`**: 4×4 pixels. Palette 4 base with palette 7 (pink) crack lines forming a star pattern interior. Tag `["wall", "breakaway"]`. Role: collidable wall that burst destroys.
- **`socket_small`**: 4×4 pixels. Hollow square ring of palette 11 (yellow) outer (1-cell thick) with palette 12 (orange) corner accents. Inside is `-1` (transparent). Tag `["socket"]`. `interaction=INTANGIBLE`. Role: target the avatar must body-fit at small size.
- **`socket_med`**: 8×8 pixels. Hollow ring of palette 11 (2-cell thick) with palette 12 corner accents and a palette-11 cross etched at the centre. Inside transparent. Tag `["socket"]`. INTANGIBLE.
- **`socket_large`**: 12×12 pixels. Hollow ring of palette 11 (2-cell thick) with palette 12 corner accents, plus a palette-11 cross etched at the centre. Inside transparent. Tag `["socket"]`. INTANGIBLE.
- **`shove_block`**: 4×4 pixels. Palette 15 (purple) outer cells with palette 6 (magenta) interior cross. Tag `["shove_block"]`. Role: push-target during inflate.
- **`step_counter` (HUD widget)**: a `RenderableUserDisplay` painting row 0 with a 64-wide bar — palette 9 (blue) for remaining steps, palette 0 (white) for spent steps.

Roles are author-side labels; tags are runtime-only. The 4-character ID `zw91` is opaque per §3.4.

## 4. Level progression, mechanic enumeration, and witness solutions

All three levels use `grid_size=(64, 64)`. The internal "tile" convention (1 tile = 4×4 cells) is used only for layout; movement is `set_position(±4, ±4)` per arrow press regardless of avatar size. The avatar's `top-left` cell is its anchor; growing extends the footprint asymmetrically right + down, so a player who grows at tile (X, Y) has the new cells appear in the rightward and downward expansion. Walls form the playfield perimeter at tile rows/cols 0 and 15 (cells y∈{0..3, 60..63} and x∈{0..3, 60..63}).

**Win predicate (all levels):** for every sprite tagged `socket`, the avatar's current size matches the socket's size AND the avatar's `top-left` cell equals the socket's `top-left` cell.

### Level 1 — base dynamic system
**Layout:**
- Perimeter walls only.
- Avatar starts at top-left tile (2, 2), size small. Top-left cell (8, 8).
- One `socket_large` at top-left tile (12, 12). Top-left cell (48, 48). Socket footprint: cells (48..59, 48..59).

**Mechanics required by the witness (N = 2):**
1. **M1 — move** (arrow press steps the avatar one tile).
2. **M2 — size-cycle** (ACTION5 cycles the avatar's size 1 → 2 → 3, advancing the rendered sprite, the occupied cells, and the socket-fit predicate).

Both mechanics are exercised by the witness below; neither is hidden.

**Necessity per mechanic (counterfactual, per checklist item 12):**
- **M1**: L1 cannot be solved without triggering M1 because the avatar starts at top-left cell (8, 8) and the only socket has top-left cell (48, 48); without arrow movement the avatar stays at (8, 8) and never satisfies the win predicate's position clause.
- **M2**: L1 cannot be solved without triggering M2 because the only socket is `socket_large` (size 3) and the avatar's initial size is small (size 1); without ACTION5 cycling, `avatar.size != socket.size` for the entire run and the win predicate is unreachable.

**Witness solution** (22 actions):
```
[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4,
 ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2, ACTION2,
 ACTION5, ACTION5]
```
After 10 RIGHT (ACTION4) presses the avatar's top-left is at cell (48, 8). After 10 DOWN (ACTION2) presses the top-left is at cell (48, 48). The first ACTION5 cycles to medium (footprint (48..55, 48..55), all open). The second ACTION5 cycles to large (footprint (48..59, 48..59), all open, equals socket footprint). Win predicate fires.

**Difficulty justification:**
- **(a) Random-resistance.** A vision-blind / random-policy agent has only a small chance of producing the precise navigation+cycle sequence within the 50-step budget, but L1 is the tutorial — by NovaPlay §3.4 random-policy stumble-through is acceptable here. The probability of solving by uniform random over 5 actions in 50 steps is small but not vanishing, which is the tutorial's design intent (low score weight 1/6).
- **(b) Human-tractable.** A first-time human reads the rendered frame: orange avatar small at top-left, larger yellow ring at bottom-right. Inferring "navigate and grow to fit" takes a handful of exploratory actions — solvable in well under 1 minute.
- **(c) Planning depth.** No strict planning requirement at L1. Once the player has discovered M1 (arrows move) and M2 (ACTION5 grows), the path is direct: walk to the socket, cycle until size matches.
- **(d) Step budget.** `step_budget = 50`. Generous over the 22-action witness (~2.3×) so a first-time player has comfortable room to explore (e.g., spam ACTION5 a few times, walk past the socket, retrace).

### Level 2 — base system + 1 new mechanic
**Layout:**
- Perimeter walls.
- Vertical wall column at tile_x=8: `wall_block` at tiles (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14). The gap at tiles (8, 6) and (8, 7) is the only passage.
- Two `shove_block` instances at tiles (8, 6) and (8, 7), wedged in the gap. Top-left cells (32, 24) and (32, 28).
- Avatar starts at top-left tile (2, 7). Top-left cell (8, 28).
- One `socket_med` at top-left tile (12, 6). Top-left cell (48, 24). Socket footprint: cells (48..55, 24..31) = tiles (12-13, 6-7).

**Mechanics required by the witness (M = 3 = N+1):**
1. **M1 — move** (carried forward from L1; required by witness).
2. **M2 — size-cycle** (carried forward from L1; required by witness).
3. **M3 — inflate-push (NEW).** When ACTION5 cycles the avatar from size N to size N+1, every shove-block whose cell is within the *new* footprint is rolled in the cardinal direction away from the avatar's centre, one tile per cell of growth; the rolling stops on contact with a wall or another block. If a block cannot move at all (because the immediately-adjacent cell in the push direction is wall-bound), the entire inflate is canceled.

**Necessity per mechanic (counterfactual, per checklist item 12):**
- **M1**: L2 cannot be solved without triggering M1 because the avatar starts at cell (8, 28) and the socket's top-left is at (48, 24); without arrow movement the avatar's top-left never equals the socket's top-left.
- **M2**: L2 cannot be solved without triggering M2 because the only socket is `socket_med` (size 2) and the avatar starts at size 1; without ACTION5 cycling, `avatar.size != socket.size` and the win predicate is unreachable.
- **M3**: L2 cannot be solved without triggering M3 because the vertical wall column at tile_x=8 has wall blocks at every (8, y) for y∈{1..5, 8..14} — the only opening is tiles (8, 6) and (8, 7), and both opening tiles are occupied by `shove_block` instances. The avatar at size 1 cannot move into tile (8, 6) or (8, 7) (block collides); the avatar at size 2 cannot pass the gap at tile_y=7 because growing at top-left tile (7, 7) places footprint cells in tile (8, 8), which is wall (inflate cancels); the avatar at size 3 cannot pass at any tile_y because its 12-cell-tall footprint always overlaps a wall block in the column. The only path east of tile_x=8 is (i) align the avatar at top-left tile (7, 6), where size-2 footprint covers tiles (7-8, 6-7) — both gap tiles — and (ii) inflate, which triggers M3 to roll both blocks east through the open inner area. Without M3, both blocks remain in tiles (8, 6) and (8, 7) and avatar size 2 cannot enter the gap.

**Witness solution** (12 actions):
```
[ACTION4, ACTION4, ACTION4, ACTION4, ACTION4,
 ACTION1,
 ACTION5,
 ACTION4, ACTION4, ACTION4, ACTION4, ACTION4]
```
- 5×ACTION4 (RIGHT): top-left moves cell (8, 28) → (28, 28) — tile (7, 7), size 1.
- 1×ACTION1 (UP): top-left cell (28, 24) — tile (7, 6), size 1.
- 1×ACTION5 (cycle 1→2): footprint becomes cells (28..35, 24..31) = tiles (7-8, 6-7). Both shove-blocks at (8, 6), (8, 7) are inside the new footprint. Push direction: east (`sign(block.x − avatar.x) = +1`, `sign(block.y − avatar.y) = 0`). Each block rolls east tile-by-tile through empty tiles (9, *), (10, *), …, (14, *) and stops when the next tile is the perimeter wall at tile (15, *). Each block parks at tile (14, 6) and (14, 7) respectively — well outside the avatar's required path.
- 5×ACTION4 (RIGHT) at size 2: top-left advances tile (7, 6) → (12, 6). Footprint cells (48..55, 24..31). Equal to socket_med's footprint. Win predicate fires.

**Difficulty justification:**
- **(a) Random-resistance.** A random / small-LLM policy is extremely unlikely to (i) reach top-left tile (7, 6) AND (ii) press ACTION5 from there AND (iii) navigate at size 2 without fumbling — within the 60-step budget. Any inflate at the wrong cell either fails (tile (8, 8) wall) or leaves the blocks unmoved. Probability of solving by uniform-random over 5 actions ≪ 1/10⁴.
- **(b) Human-tractable.** A human reads: orange avatar (small) at left, yellow medium-socket at right, vertical wall column with two purple shove-blocks plugging the only gap. They infer that growing while adjacent to a block must somehow move it. Total time ~2 minutes (including 30 sec to discover M3 by trying ACTION5 next to a block).
- **(c) Planning depth — moderate post-discovery.** Once the player has fully understood M1, M2, M3, the post-discovery decision space at level start (avatar size 1 at tile (2, 7), open space east to tile (7, *)) is at least 3 valid first actions (ACTION1 up, ACTION4 right, ACTION5 cycle). The plausible-but-wrong path is "stay at tile_y=7 and try to inflate-push at tile (7, 7)" — this fails because size-2 footprint at tile (7, 7) overlaps wall at tile (8, 8). The witness chain reasons: "I must align at tile_y=6 before inflating because the gap is 2 tiles tall; size-2 footprint must fit entirely in the gap; the gap occupies tiles (8, 6-7), so my size-2 anchor must be at tile_y=6."
- **(d) Step budget.** `step_budget = 60`. Generous over the 12-action witness (5×) so the player has room to discover the alignment requirement.

### Level 3 — system + 1 more new mechanic
**Layout (revised after critique-revisions.md issue 1):**
- Perimeter walls.
- First vertical wall column at tile_x=8: `wall_block` at tiles (8, 1..5) and (8, 9..14); **3-tile gap** at (8, 6), (8, 7), (8, 8). Three `shove_block` instances plug the gap at (8, 6), (8, 7), (8, 8). Top-left cells (32, 24), (32, 28), (32, 32).
- Second vertical wall column at tile_x=11: `wall_block` at tiles (11, 1..5) and (11, 9..14); **3-tile gap** at (11, 6), (11, 7), (11, 8) replaced by three `breakaway_wall` instances. Top-left cells (44, 24), (44, 28), (44, 32).
- Avatar starts at top-left tile (2, 7). Top-left cell (8, 28).
- One `socket_large` at top-left tile (12, 6). Top-left cell (48, 24). Socket footprint: cells (48..59, 24..35) = tiles (12-14, 6-8).

**Mechanics required by the witness (M = 4 = previous-level + 1):**
1. **M1 — move** (carried forward).
2. **M2 — size-cycle** (carried forward).
3. **M3 — inflate-push** (carried forward).
4. **M4 — overload-burst (NEW).** When the avatar at size 3 is sent ACTION5, it does NOT wrap to size 1; instead it enters an **overloaded** state with `overload_halo` rendered around its footprint at layer 5. From overloaded, the next ACTION5 fires a one-shot **burst**: every `shove_block` and `breakaway_wall` whose cells lie within Chebyshev-distance 8 (i.e., 2 tiles) of the avatar's current footprint cells is removed (`set_interaction(InteractionMode.REMOVED)`). The avatar then resets to size 1 at the same top-left position; the overload_halo is hidden. The burst is single-use per level: after firing, ACTION5 resumes its size-cycle role (1→2→3→overloaded→burst→1→…) but breakaway-walls already destroyed remain destroyed.

**Necessity per mechanic (counterfactual, per checklist item 12):**
- **M1**: L3 cannot be solved without triggering M1 because the avatar starts at cell (8, 28) and the socket's top-left is at (48, 24); without movement the avatar's top-left never equals the socket's top-left.
- **M2**: L3 cannot be solved without triggering M2 because the only socket is `socket_large` (size 3) and the avatar starts at size 1; without ACTION5 cycling, sizes never match.
- **M3**: L3 cannot be solved without triggering M3 because the wall column at tile_x=8 has walls at every tile_y∈{1..5, 9..14} and three `shove_block` instances at the only gap-cells (8, 6), (8, 7), (8, 8). Size-1 avatar cannot pass any of (8, 6-8) (block collides). Size-2 avatar cannot align with the gap at all (its 2-tile-tall footprint always either includes a wall row or one of the block-occupied gap rows). Size-3 avatar at top-left tile (7, 6) has footprint tiles (7-9, 6-8) — exactly the 3-tile gap — but tiles (8, 6), (8, 7), (8, 8) all hold shove_blocks, so size-3 inflate at (7, 6) requires the inflate-push rule to fire on all three of them. The only avatar position from which size-3 inflate succeeds (with blocks initially in place) is (7, 6), and that inflate triggers M3 by definition.

  **Alt-path enumeration (per critique-revisions.md issue 2):** The only conceivable M3-skip is "burst at a size-3 position whose Cheby-12 burst zone covers all three blocks AND all three breakaway-walls in one shot, AND have reached that position with the size-3 inflate succeeding without M3 ever firing." Burst zone Cheby-12 from a size-3 footprint is a 36-cell-wide window. To cover the block-cells (x=32..35 at tile_x=8) AND the breakaway-cells (x=44..47 at tile_x=11), the avatar's size-3 footprint x-range [tx, tx+11] must satisfy `tx-12 ≤ 32` AND `tx+23 ≥ 47` → `tx ∈ [24, 44]`. Tile-aligned tx values in that range: 24 (tile 6), 28 (tile 7), 32 (tile 8), 36 (tile 9), 40 (tile 10), 44 (tile 11). For avatar size 3 to be feasible at tx, footprint tiles must be free of walls/blocks at the moment of the size-3 inflate. Tx=24 (tile 6) ty=24 (tile 6): footprint tiles (6-8, 6-8); shove-blocks initially at (8, 6-8) all lie in the footprint — inflate-push fires on all three blocks (each pushed east into open tiles (9-10, *)), and the inflate succeeds — but **M3 fires** on this very cycle. Tx=28 (tile 7): footprint tiles (7-9, 6-8); same blocks (8, 6-8) all lie in footprint; M3 fires identically. Tx=32 (tile 8): footprint tiles (8-10, 6-8); blocks (8, 6-8) in footprint; M3 fires. Tx=36 (tile 9): footprint tiles (9-11, 6-8); breakaway-walls at (11, 6-8) lie in footprint and inflate-push does *not* move breakaways — inflate cancels. Tx=40 (tile 10): footprint tiles (10-12, 6-8); breakaway-walls at (11, 6-8) in footprint — cancels. Tx=44 (tile 11): footprint tiles (11-13, 6-8); breakaway-walls in footprint — cancels. **No size-3 position in [24, 44] reaches both target sets without M3 firing**; the three feasible burst positions (tx ∈ {24, 28, 32}) all require M3 push during the 2→3 cycle that placed the avatar there. M3 is unavoidable.

- **M4**: L3 cannot be solved without triggering M4 because the second wall column at tile_x=11 has wall_blocks at every tile_y∈{1..5, 9..14} and `breakaway_wall` instances at the only gap-cells (11, 6), (11, 7), (11, 8). A `breakaway_wall` is collidable like a normal wall; arrow movement treats it as solid, and inflate-push does not move it (the push-roll rule only moves `shove_block`). The only mechanism that destroys breakaway-walls is the burst portion of M4. Without firing burst, the three breakaway-walls remain intact and the inner room (tiles 12..14) is unreachable: avatar size 1 at (10, 6) cannot enter tile (11, 6) (breakaway collides); size 2 at (9, 6) footprint (9-10, 6-7) cannot grow to size 3 at (9, 6) because the size-3 footprint (9-11, 6-8) overlaps three breakaway-walls at (11, 6-8) which inflate-push cannot move (cancels inflate); size 3 at (10, 6) cannot exist (breakaway in footprint). M4 must fire.

**Witness solution** (17 actions):
```
[ACTION1,
 ACTION4, ACTION4, ACTION4, ACTION4,
 ACTION5, ACTION5, ACTION5, ACTION5,
 ACTION4, ACTION4, ACTION4, ACTION4, ACTION4, ACTION4,
 ACTION5, ACTION5]
```
Step-by-step (revised after critique-revisions.md issue 1; 3-block / 3-breakaway layout; burst-radius Chebyshev-12):
1. ACTION1 (UP): top-left cell (8, 28) → (8, 24); avatar at tile (2, 6) size 1.
2-5. 4×ACTION4 (RIGHT): top-left (8, 24) → (24, 24); avatar at tile (6, 6) size 1.
6. ACTION5 (cycle 1→2): new footprint cells (24..31, 24..31) = tiles (6-7, 6-7). No shove-blocks lie inside this footprint (the three shove-blocks are at tiles (8, 6), (8, 7), (8, 8), all of which have tile_x=8 — outside (6-7, 6-7)). Inflate succeeds with no push needed; avatar reaches size 2 at tile (6, 6).
7. ACTION5 (cycle 2→3 + push): new footprint cells (24..35, 24..35) = tiles (6-8, 6-8). All three shove-blocks lie inside this footprint. Push direction is east for each (block centres at (34, 26), (34, 30), (34, 34); avatar size-3 centre at (24+6, 24+6) = (30, 30); ddx ≥ |ddy| with ddx > 0 for blocks at y=6 and y=7, and ddx > 0 with |ddx|=|ddy| for the (8, 8) block, so all push east per the dominant-axis-with-east-tiebreak rule). Each block rolls east tile-by-tile through (9, *), (10, *); the next tile (11, *) is a `breakaway_wall` — blocks park at (10, 6), (10, 7), (10, 8). Avatar reaches size 3 at tile (6, 6).
8. ACTION5 (overload entered): `overload_halo` is set TANGIBLE at layer 5 surrounding the size-3 avatar's footprint and remains so until burst fires (per checklist item 19's persistent-cue requirement); size remains 3.
9. ACTION5 (burst fires): burst zone = footprint cells (24..35, 24..35) padded by Chebyshev-distance 12 = cells (12..47, 12..47). The blocks at tiles (10, 6), (10, 7), (10, 8) — cells (40..43, 24..35) — are inside the zone (max-x 43 ≤ 47, max-y 35 ≤ 47). The breakaway-walls at tiles (11, 6), (11, 7), (11, 8) — cells (44..47, 24..35) — are also inside (max-x 47 ≤ 47). All six sprites have `set_interaction(InteractionMode.REMOVED)` applied. Avatar resets to size 1 at top-left cell (24, 24) = tile (6, 6); `overload_halo` is set REMOVED.
10-15. 6×ACTION4: top-left (24, 24) → (48, 24); avatar at tile (12, 6) size 1. Path tiles (7, 6) → (8, 6) → (9, 6) → (10, 6) → (11, 6) → (12, 6) — all open after burst (blocks REMOVED, breakaway-walls REMOVED).
16. ACTION5 (cycle 1→2): footprint cells (48..55, 24..31). No blocks remain anywhere; inflate succeeds. Avatar size 2 at (48, 24).
17. ACTION5 (cycle 2→3): footprint cells (48..59, 24..35) = tiles (12-14, 6-8). Open. Equal to `socket_large`'s footprint. Win predicate fires.

**Difficulty justification:**
- **(a) Random-resistance.** A random / small-LLM policy must (i) reach tile (7, 6); (ii) sequence FOUR ACTION5s in a row at that exact cell; (iii) re-navigate post-burst; (iv) re-cycle precisely twice at the destination. Probability ≪ 1/10⁴ within the 100-step budget; spamming ACTION5 anywhere else yields cancelled inflates or wasted bursts.
- **(b) Human-tractable.** A human reads the L3 frame: starting orange avatar small, two block-plugged gaps, two crack-textured (breakaway) wall cells in a second column, and a large yellow socket in the inner room. They infer (over ~30 sec of play) that grow-to-push works (carry-forward from L2) and that something special must clear the cracked walls. Discovering overload+burst takes another minute. Solve time ~3 minutes.
- **(c) Planning depth — challenging post-discovery.** A fully informed player faces ≥ 3 valid first actions (ACTION1 up, ACTION4 right, ACTION5 cycle). The trivial heuristic "burst as soon as size 3 is reachable" fails because the burst zone is centred on the avatar at the moment of firing — bursting at any far-from-targets position (e.g., size-3 avatar at tile (3, 6) or (4, 6)) covers neither block-cells nor breakaway-cells, wasting the single-use burst. The trivial heuristic "press ACTION5 four times in a row from the start cell" fails because cycling 1→2 at (2, 6) inflates harmlessly but cycling 2→3 from there — footprint tiles (2-4, 6-8) — has no blocks or breakaways to interact with, and bursting at that position covers nothing useful. The witness chain — "first navigate to tile (6, 6), then cycle 1→2 (no push needed), then cycle 2→3 (which fires M3 push on all three blocks east into tiles (10, 6-8)), then overload, then burst (which destroys the rolled blocks AND the breakaway-walls because tile (6, 6)'s Cheby-12 burst zone reaches cells x=12..47, covering both target sets), then re-navigate east at size 1 through the cleared corridor, then re-cycle to size 3 at the socket" — is the unique winning sequence with this position choice. A heuristic player who positions east-of-(6, 6) (e.g., tile (7, 6)) finds that the (8, 8) shove-block's push direction is south (because its centre is straight south of the size-3 avatar centre when avatar is at (7, 6)), and south is wall — inflate cancels and the player cannot reach size 3 at (7, 6). The planning depth is the realisation that the avatar's *position relative to the blocks* determines the push directions and therefore which inflate positions are even feasible.
- **(d) Step budget.** `step_budget = 100`. Generous over the 17-action witness (~6×). Larger than L2's budget per `difficulty-rules.md` § d's "L3 budget must NOT shrink relative to L2" rule.

## 5. Action mapping
`available_actions = [1, 2, 3, 4, 5]`.

- `ACTION_1` (UP): move avatar by `(0, -4)` cells if the new top-left + size footprint contains no `wall` and no `shove_block`. Else no-op.
- `ACTION_2` (DOWN): `(0, +4)`.
- `ACTION_3` (LEFT): `(-4, 0)`.
- `ACTION_4` (RIGHT): `(+4, 0)`.
- `ACTION_5` (size-cycle / overload / burst): branched by current `state` (revised to use the rule from §2):
  - **If size ∈ {1, 2}** (try to grow to size+1):
    1. Compute candidate footprint at new size at the avatar's current top-left.
    2. If any cell of the candidate footprint overlaps a `wall` or `breakaway_wall` sprite, cancel — avatar size unchanged.
    3. Otherwise, identify every `shove_block` whose cells lie inside the candidate footprint. For each such block: push direction = `(sign(block.center.x − avatar.center.x), sign(block.center.y − avatar.center.y))` projected to the dominant cardinal axis (ties → east). Roll the block one tile at a time in the push direction; the block continues rolling as long as the next-tile destination is empty and stops the moment the next-tile destination is a `wall`, `breakaway_wall`, another `shove_block`, or the grid perimeter. If a block's first attempted destination is already blocked (it cannot move at all), cancel the entire inflate and roll back any blocks already moved this cycle.
    4. If no cancel fired, commit: swap `avatar_small`/`avatar_med`/`avatar_large` TANGIBLE↔REMOVED to advance size.
  - **If size == 3 and not overloaded:** set `self.overloaded = True`, set `overload_halo` to TANGIBLE at the avatar's centred position (layer 5), and reposition the halo each subsequent step so it tracks the avatar (the halo is the persistent visual cue that the next ACTION5 will fire burst rather than continue size-cycling).
  - **If size == 3 and overloaded:** fire burst. For every sprite tagged `shove_block` or `breakaway`, if any of its cells lies within Chebyshev-distance 12 (3 tiles) of any avatar-footprint cell, call `sprite.set_interaction(InteractionMode.REMOVED)`. Then reset avatar size to 1 (swap variants), set `self.overloaded = False`, and set `overload_halo` to REMOVED.
- ACTION 6, 7 not in `available_actions` (no click, no undo).

Context-dependent gating: none required at the engine level — the size-cycle branch handles all four ACTION5 sub-states internally.

## 6. HUD and per-game state
**HUD widgets (passed to `Camera(interfaces=[...])`):**
- `StepCounterHud`: a `RenderableUserDisplay` painting frame-row 0 with `(remaining/max) × 64` cells of palette 9 (blue) followed by spent cells of palette 0 (white). Updated each step via `step_counter_ui.set_remaining(self._step_counter_remaining)`.

**Internal state (instance attributes on the `Zw91` game class):**
- `self.size: int` — current avatar size, ∈ {1, 2, 3}. Visible cue: which of the three avatar sprite variants is TANGIBLE (others REMOVED). Per checklist item 19: visible cue is the rendered footprint size itself.
- `self.overloaded: bool` — True when size==3 and a further ACTION5 has been fired without yet bursting. Visible cue: `overload_halo` sprite is set to `interaction=TANGIBLE` at layer 5 surrounding the avatar at the moment of overload-entry and remains so until burst fires; it is repositioned to track the avatar's centre every step. Per checklist item 19, the halo is the persistent visible cue (not a one-frame flash) that the next ACTION5 will fire burst rather than continue size-cycling.
- `self.burst_used: bool` per level — True after burst has fired this level (used to prevent double-burst within a level; the breakaway-walls being one-shot destroyed already enforces this naturally, but the flag also prevents accidental halo flicker).
- `self.step_counter_remaining: int` — drains by 1 per action; HUD reflects this.
- `self._top_left: tuple[int, int]` — the avatar's anchor cell; same as `self.active_avatar_sprite.x`, `.y` but tracked for size-swap convenience.

State persistence on level set: `on_set_level` resets `self.size = 1`, `self.overloaded = False`, `self.burst_used = False`, `self.step_counter_remaining = level.get_data("step_budget")`, all three avatar variants placed at the level's start cell with `avatar_small` TANGIBLE and the others REMOVED, halo hidden.

## 7. Win condition
Triggered after every successful action: enumerate every sprite tagged `socket` and check `(socket.x, socket.y) == (self.active_avatar.x, self.active_avatar.y)` AND `socket_size_for(socket) == self.size`. If every socket matches, call `self.next_level()`. A level with N sockets requires N matches; in the spec's three levels, N=1 always.

## 8. Lose condition
Triggered when `self.step_counter_remaining` hits 0. Call `self.lose()`. No other lose path; the avatar can always retreat / cycle / re-attempt, and the burst is single-use but never traps the player into an unsolvable state on its own (a misfired burst on L3 makes the level unsolvable, but the budget is generous enough that a player can burn through it diagnosing the failure rather than waiting in a no-win state — and the engine still fires `lose()` on counter exhaustion).

## 9. Novelty note

### Closest taxonomy entries (per `mechanic-novelty/similarity-check.md`)

- **s5i5 — `rod-stretch-retract`** (reference). *Distinguishing rule:* in s5i5 the player operates remote click-control swatches to stretch/retract *stationary* rods whose tips must reach targets — the player is not embodied. The win condition is "every rod's tip reaches its target cell." In `zw91` the player IS the avatar — a single mobile pawn whose footprint cycles through 3 *radial* sizes via a modal verb (ACTION5), and the win condition is "the avatar's body fits the socket at matching size." Different agency (player-embodied vs remote operator), different verb axis (radial vs axial), different goal (body-in-socket vs tip-on-target).
- **ka59 — `sokoban-explode-chase`** (reference). *Distinguishing rule:* ka59's explode-tiles are environmental fixtures triggered by walking over them; explosion is a *consequence of position*. ka59 also has chasers (autonomous AI). `zw91` has *no environmental triggers and no AI*: the burst is an on-demand resource the player loads by cycling to max-size, and fires by pressing ACTION5 once more — single-shot per level, conditional on the size mechanic. ka59's destruction is a consequence of position; `zw91`'s burst is a consequence of state-loading via the size verb.
- **ft09 — `stamp-3x3-paint`** (reference). *Distinguishing rule:* ft09's footprint is a 3×3 paint stamp triggered by a click at any cell; the canvas accumulates stamps to match a target image. The player is a click-cursor, not a body. In `zw91`, the avatar's footprint is *the avatar itself* — a body that occupies cells, blocks paths, fits sockets — not a paint area; there is no canvas, no painting, no stamp accumulation.

### Closest prior-games entries

- **nb6t — `hinge-chain-reach`**. *Distinguishing rule:* nb6t has multiple jointed rod-segments with independent hinges that the player articulates by selecting and rotating each segment; the segments form a reaching arm. `zw91` has a single self-contained avatar whose entire footprint resizes radially in place — no hinges, no segments, no kinematic chain. nb6t plays as "operate an articulated arm"; `zw91` plays as "be a self-resizing pawn."
- **gv47 — `seed-grow-surround-dissolve`**. *Distinguishing rule:* gv47's growth is *region-on-canvas*: clicked seeds expand outward into adjacent paint cells; the player is not embodied. In `zw91`, growth is *avatar-self*: the player's own pawn changes radial size, navigates, and body-fits sockets. No painting, no region merging, no canvas.
- **kn58 — `anchor-pull-magnet`**. *Distinguishing rule:* kn58 uses a click to place an anchor that magnetically pulls all coloured pawns; the verb is *external object emission* operating on multiple pawns. `zw91` uses no anchors, no magnetic field, and operates only on the player's own footprint. The "pushing" in `zw91` is the side-effect of the avatar's own growth; the "pulling" in kn58 is a separate object's effect.
- **kp9z — `grain-accumulate-topple`**. *Distinguishing rule:* kp9z has discrete grains overflowing cardinal neighbours when capacity is exceeded — a sandpile cellular-automaton dynamic. `zw91` has no grains, no per-cell capacity, no cascade. The player's avatar size changes once per ACTION5, not as a propagating wave.

### Negative similarity check (8 dimensions)
Walked in `mechanic-pick.md`. No prior shares 3+ dimensions with `zw91`'s L1 mental rendering. Strongest divergence on dimensions 5 (cast: avatar+walls+socket-rings+shove-blocks+breakaway-walls — distinct), 6 (visual signature: orange/maroon avatar + yellow rings + purple blocks + cracked-pink breakaways — no overlap with `{4,8,9}` priors), 7 (pixel grain: every primary sprite has internal pattern), 8 (core dynamic: avatar's own footprint size as the verb — no prior).

If `prior-games/index.md` already contains `zw91` from a separate run: it does not — verified at pick_mechanic time.
