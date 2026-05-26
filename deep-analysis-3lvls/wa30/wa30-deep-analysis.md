# wa30 — deep analysis

> **3-LEVELS-ONLY NOTE.** This analysis was authored against the
> original full reference games (6+ levels each). Our generated
> games target only **L1, L2, L3** — so any content below that
> describes "level 4+", "L4+", "L5+", sprite rows annotated
> "(level 4+ only)" / "(level 5+ only)", action-handler branches
> for late levels, or internal-state flags gating late-level
> behaviour describe content NOT present in the truncated 3-level
> versions used by the harness. Read the L1/L2/L3 sections as
> primary; treat L4+ references as historical context only.


## Source meta
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/wa30/ee6fef47/wa30.py`
- Lines: 1237
- Class name: `Wa30`
- available_actions: `[1, 2, 3, 4, 5]` (UP / DOWN / LEFT / RIGHT, ACTION5 = lock-or-unlock)
- Number of levels in source: 9
- Number of levels documented in this analysis: 3
- Imports: `ActionInput`, `NovaBaseGame`, `Camera`, `GameAction`, `Level`, `RenderableUserDisplay`, `Sprite` from `novaengine`; `numpy as np`.

## Mechanic essence (one sentence)

A green-tipped lavender player walks the arena in four-pixel hops, and pressing the lock key when it stands beside a grey crate latches that crate to the player so the next walking step drags the crate alongside — with the level solved when every crate sits squarely inside a hollow blue-bordered goal-frame, while a purple drone in later levels chases the same crates and tries to lock onto them first.

## Sprite roster

| sprite (obfuscated) | dims | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| `aidclcbjcv` | 64x20 | 4 | (default) | (default) | YES | (default) | YES | level-7+ background panel covering bottom 20 rows of the 64x64 frame |
| `byigobxzpg` | 4x4 | 12 | kdweefinfi | 1 | YES | (default) | YES | purple AI drone (L2+, races the player to grab crates) |
| `cwefnfvjhr` | 64x16 | 4 | (default) | (default) | YES | (default) | YES | level-7+ background panel covering top 16 rows |
| `doijajrgdi` | 8x12 | 9, 2 | fsjjayjoeg | (default) | NO | (default) | YES | tall goal-frame: hollow palette-9 outline around 6x10 palette-2 interior |
| `geffskzhqq` | 4x8 | 2 | zqxwgacnue | (default) | NO | (default) | YES | small disposal-zone (level 7+) — solid palette-2 block, no outline |
| `ghklglzjuf` | 8x8 | 9, 2 | fsjjayjoeg | (default) | NO | (default) | YES | square goal-frame (level 6+) |
| `jigtxgzhwt` | 12x4 | 9, 2 | fsjjayjoeg | (default) | NO | (default) | YES | wide-rectangle goal-frame: hollow palette-9 outline around 10x2 palette-2 interior (L1) |
| `jqzhxgbmtz` | 4x4 | 15 | ysysltqlke | 1 | YES | (default) | YES | "white agent" — adversary that pushes crates into disposal zones (level 6+ — out of scope for L1-3) |
| `ktghqrydvd` | 8x16 | 9, 2 | fsjjayjoeg | (default) | NO | (default) | YES | tall goal-frame (L3, L5) |
| `ofwegeqknn` | 4x8 | 9, 2 | fsjjayjoeg | (default) | NO | (default) | YES | narrow goal-frame (L4, L7) |
| `ooaamfpvqr` | 8x8 | 2 | zqxwgacnue | (default) | NO | (default) | YES | medium disposal-zone (level 6+) |
| `peimznrlqd` | 12x12 | 9, 2 | fsjjayjoeg | (default) | NO | (default) | YES | large square goal-frame (L8, L9) |
| `pktgsotzmw` | 4x4 | 4, 9 | geezpjgiyd | 1 | YES | (default) | YES | grey crate — the puzzle pieces the player must deliver to goal-frames |
| `pmargquscu` | 4x4 | 2 (with -2 transparency holes) | bnzklblgdk | (default) | NO | (default) | YES | wall sprite — palette-2 with 4 negative-2-tagged holes (an X-pattern of impassable cells) |
| `uasmnkbzmm` | 4x4 | 5 | debyzcmtnr | (default) | YES | (default) | YES | stone wall — solid palette-5 block (level 4+) |
| `vikkhnsrzd` | 16x8 | 9, 2 | fsjjayjoeg | (default) | NO | (default) | YES | extra-wide goal-frame (L8) |
| `wkmuwhjqyo` | 8x4 | 9, 2 | fsjjayjoeg | (default) | NO | (default) | YES | thin horizontal goal-frame (L4, L7, L9) |
| `wppuejnwhl` | 4x4 | 0, 14 | wbmdvjhthc | 1 | YES | (default) | YES | player avatar — top row palette-0 (black cap), bottom 3 rows palette-14 (green body) |
| `xqaqifquaw` | 12x12 | 2 | zqxwgacnue | (default) | NO | (default) | YES | extra-large disposal-zone (L8) |
| `xxmzyqktqy` | 4x4 | 9, 2 | fsjjayjoeg | (default) | NO | (default) | YES | minimum-size goal-frame (L4) — 1x1 hollow palette-2 surrounded by palette-9 |

### `aidclcbjcv` — 64x20 background panel (level 7+)
- Pixel pattern: solid 64x20 of palette-4 (background-grey).
- Where it appears: not placed in L1-3 (only L7).
- Role: out of scope.
- Visual-vs-functional read: large flat grey background; not interactive.

### `byigobxzpg` — purple AI drone (L2, L3)
- Pixel pattern: 4x4 solid palette-12 (purple).
- Where it appears: L2 (1 copy at (24, 36)), L3 (1 copy at (48, 12)). Multiple copies in L4-9.
- Role: an autonomous "AI drone" that competes with the player for crates. Behaviour driven by `ynmgxjqkgh()` after every action: if the drone is currently locked to a crate, BFS to the nearest goal-frame cell and step one cell along that path; otherwise, look for adjacent crates to lock onto, or BFS to the nearest passive-block-adjacent cell.
- Visual-vs-functional read: at-rendered-scale a 4x4 solid purple square. Reads as a "blocking object". Tag `kdweefinfi` distinguishes it from the player's `wbmdvjhthc` tag. Nearest-other-sprite: `wppuejnwhl` (the player) — also a 4x4 layer-1 sprite, but with a black cap above its green body. The drone has no cap, so "uniformly purple square" = drone, "green block with black cap" = player. The drone has NO directional indicator, while the player's cap rotates based on direction (`pjedoipwee` chooses rotation 0/90/180/270 based on (dx, dy)).
- Visual contrast notes: purple-12 against the palette-1 (cyan) background reads boldly.

### `cwefnfvjhr` — 64x16 background panel (level 7+)
- Pixel pattern: solid 64x16 of palette-4.
- Where it appears: not placed in L1-3 (only L7).
- Role: out of scope.

### `doijajrgdi` — 8x12 goal-frame (L2)
- Pixel pattern: 8 cols × 12 rows. Outermost ring is palette-9 (1-cell thick on all sides); interior 6x10 is palette-2 (matching background to "see through"). Effectively a hollow rectangle picture-frame.
- Where it appears: L2 only (1 copy at (12, 28)).
- Role: goal-frame — a 6x10 interior region into which crates must be deposited. The win predicate `ymzfopzgbq` checks each crate's (x, y) corner is in the precomputed `wyzquhjerd` set, which contains every cell of every `fsjjayjoeg`-tagged sprite.
- Visual-vs-functional read: at-rendered-scale a hollow blue-bordered rectangle (palette-9 outline around palette-2 transparent middle). Tag `fsjjayjoeg` shared with all goal-frames. Nearest-other: `jigtxgzhwt`, `ktghqrydvd`, `ofwegeqknn`, `ghklglzjuf`, `xxmzyqktqy`, `vikkhnsrzd`, `peimznrlqd`, `wkmuwhjqyo` are all goal-frames of different shapes/sizes — same tag, same role. Player tells them apart by aspect ratio.
- Visual contrast notes: palette-9 (cyan/blue) outline against palette-1 (background) and palette-2 interior is a clear "frame" silhouette.

### `geffskzhqq` — 4x8 disposal-zone (level 7+)
- Pixel pattern: solid 4x8 palette-2.
- Where it appears: not placed in L1-3.
- Role: out of scope (level 7+).

### `ghklglzjuf` — 8x8 square goal-frame (level 6+)
- Pixel pattern: 8x8 with palette-9 outer ring and 6x6 palette-2 interior.
- Where it appears: not placed in L1-3.
- Role: goal-frame variant.

### `jigtxgzhwt` — 12x4 wide goal-frame (L1)
- Pixel pattern: 12 cols × 4 rows. Outermost ring palette-9; interior 10x2 palette-2.
- Where it appears: L1 only (1 copy at (28, 28)). Used in middle of the 64x64 grid.
- Role: the L1 goal-frame. Has interior cells (x, y) for x in 29..38, y in 29..30 (10x2 = 20 cells). However the win predicate uses every cell of the sprite (including the border), so the effective "drop zone" includes all 12x4 = 48 cells.

  Wait — re-reading `on_set_level` lines 901-905: `wyzquhjerd` is built by iterating EVERY (x, y) cell in the sprite's bounding box, regardless of whether it's the border or interior. So the "in goal" cell set for `jigtxgzhwt` placed at (28, 28) is the full 12x4 = 48 cells from (28, 28) to (39, 31).

  But each crate is 4x4 (`pktgsotzmw`), so each crate's top-left corner (x, y) must be in `wyzquhjerd`. With a 12x4 frame, valid top-left positions for a 4x4 crate within the frame are (28..36, 28). That's actually 9 horizontal slots × 1 vertical slot — but the 4-pixel grid only allows positions (28, 28), (32, 28), (36, 28). So 3 crates can fit horizontally inside the frame.
- Visual-vs-functional read: hollow rectangle 12x4. Distinct from other goal-frames by its 3:1 aspect ratio. Visually clear as a "wide drop zone".
- Visual contrast notes: against palette-1 background, the palette-9 outline is the clearest "container" visual.

### `jqzhxgbmtz` — 4x4 white-purple agent (level 6+)
- Pixel pattern: solid 4x4 palette-15 (light purple/lilac).
- Where it appears: not placed in L1-3.
- Role: out of scope (white agent — adversary that pushes crates to disposal).

### `ktghqrydvd` — 8x16 tall goal-frame (L3)
- Pixel pattern: 8 cols × 16 rows. Outermost ring palette-9; interior 6x14 palette-2.
- Where it appears: L3 only (1 copy at (52, 24)). L5 also uses it (out of scope).
- Role: tall goal-frame in L3.
- Visual-vs-functional read: tall hollow rectangle. Aspect 1:2.
- Visual contrast notes: same palette as other frames.

### `ofwegeqknn` — 4x8 narrow goal-frame (level 4+)
- Pixel pattern: 4 cols × 8 rows. Outermost ring palette-9; interior 2x6 palette-2.
- Where it appears: not placed in L1-3.
- Role: out of scope.

### `ooaamfpvqr` — 8x8 medium disposal (level 6+)
- Pixel pattern: solid 8x8 palette-2.
- Where it appears: not placed in L1-3.
- Role: out of scope.

### `peimznrlqd` — 12x12 large goal-frame (level 8+)
- Pixel pattern: 12 cols × 12 rows with palette-9 ring and 10x10 palette-2 interior.
- Where it appears: not placed in L1-3.
- Role: out of scope.

### `pktgsotzmw` — 4x4 crate (every L1-3 level)
- Pixel pattern: 4x4 with palette-4 outer ring and 2x2 palette-9 interior. Visually a small grey-bordered window with a cyan core.
- Where it appears: L1 (3 copies at (44,24), (16,28), (32,36)), L2 (5 copies), L3 (5 copies). Heavy use in later levels.
- Role: passive crate — the puzzle objects. Cannot move on its own; only moves when an agent (player, drone, or white) is locked to it via `wqwsvmhhzj`. The colour of the crate's outer ring is mutated by `uxricavavq` in `zzppkjnqgk()` based on its current state: palette 4 (default), palette 0 (locked to player), palette 3 (adjacent to player but not locked), palette 5 (locked to non-player agent). So the crate's palette tells the player whether it's "free", "ready to grab", "in hand", or "stolen by drone".
- Visual-vs-functional read: at-rendered-scale a 4x4 grey square with a 2x2 cyan dot in the centre. The grey ring's colour CHANGES based on game state — this is a critical visual cue:
  - palette-4 grey: free crate, anyone can grab.
  - palette-3 (darker grey): adjacent to player; pressing ACTION5 will lock onto it.
  - palette-0 (black): currently locked to player, will move with the player's next step.
  - palette-5 (mid-grey): locked to a non-player agent (drone or white).

  Tag `geezpjgiyd` is the universal "passive block" tag; queries via `level.get_sprites_by_tag("geezpjgiyd")` enumerate every crate. **The visual identity of the crate is consistent (always 4x4 with palette-9 core), but the outer ring colour mutates** — a player must learn this colour-coding to play. Nearest-other: `wppuejnwhl` (player) is also 4x4 with palette-14 body, but has a palette-0 cap row.
- Visual contrast notes: the central palette-9 dot is constant regardless of state; the outer ring is the state indicator. Against palette-1 background, all four colour states are distinguishable.

### `pmargquscu` — 4x4 wall with diagonal holes (L3)
- Pixel pattern: 4x4 of palette-2 with 4 cells set to palette -2 (transparent / blocking-only). The pattern is `[[2, -2, 2, 2], [-2, 2, 2, 2], [2, 2, 2, -2], [2, 2, -2, 2]]` — two diagonal stripes of palette-2 cells with -2 holes interleaved. Tag `bnzklblgdk` is registered into `qthdiggudy` set in `on_set_level` (line 911-913): every wall sprite's (x, y) is added to a "blocked-by-wall" set used in `kblzhbvysd` to reject moves. Since `pmargquscu` has `collidable=False`, the engine doesn't auto-detect collisions; the game tracks them manually via the `bnzklblgdk` tag.
- Where it appears: L3 (13 copies forming a vertical column at x=32, y=0..60 in 4-pixel steps).
- Role: impassable wall column. Crates and agents cannot cross.
- Visual-vs-functional read: at-rendered-scale a 4x4 dotted/stripey grey-with-holes pattern. The -2 cells render as the underlying background (palette-1 cyan), creating a "see-through" striped look. Tag `bnzklblgdk` shared with no other sprite. Player must learn that "stripey-grey" = wall.
- Visual contrast notes: palette-2 against palette-1 reads as a darker blue/navy stripe. Distinct from `uasmnkbzmm` (solid palette-5 stones) which appears in L4+.

### `uasmnkbzmm` — solid stone wall (level 4+)
- Pixel pattern: 4x4 solid palette-5 (mid-grey).
- Where it appears: not placed in L1-3 (L4 and beyond).
- Role: out of scope.

### `vikkhnsrzd` — 16x8 wide goal-frame (level 8+)
- Pixel pattern: 16x8 hollow palette-9.
- Where it appears: not placed in L1-3.
- Role: out of scope.

### `wkmuwhjqyo` — 8x4 thin goal-frame (level 4+)
- Pixel pattern: 8x4 hollow palette-9.
- Where it appears: not placed in L1-3.
- Role: out of scope.

### `wppuejnwhl` — player avatar (every L1-3 level)
- Pixel pattern: 4x4. Row 0 is solid palette-0 (black cap); rows 1-3 are solid palette-14 (green body). Reads as a green block with a black hat.
- Where it appears: every L1-3 level (1 copy at (32, 48), (12, 8), (16, 36) respectively for L1, L2, L3).
- Role: the player avatar. Tag `wbmdvjhthc` is queried in `yygfcvqoyx` to find "the player sprite" each tick. Movement is via `qnmfimgpwc(player, dx, dy)` which (a) sets rotation based on direction (`pjedoipwee` returns 0 for UP, 90 for RIGHT, 180 for DOWN, 270 for LEFT) so the cap visually rotates to face movement direction, and (b) calls `wqwsvmhhzj(player, x+dx, y+dy)` which respects locks (if locked, moves the locked block too; if blocked by `pkbufziase` collision set, refuses).
- Visual-vs-functional read: at-rendered-scale a 4x4 green square with a black cap on one side; the cap's side rotates to face the last movement direction. This is the player's only directional indicator — without it, the player is indistinguishable from the body of any other agent.
- Visual contrast notes: green-14 against palette-1 cyan reads strongly; the black cap is unmistakable.

### `xqaqifquaw` — 12x12 large disposal (level 8+)
- Pixel pattern: solid 12x12 palette-2.
- Where it appears: not placed in L1-3.
- Role: out of scope.

### `xxmzyqktqy` — 4x4 minimum goal-frame (level 4+)
- Pixel pattern: 4x4 with palette-9 outer ring and 2x2 palette-2 interior.
- Where it appears: not placed in L1-3.
- Role: out of scope.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (64, 64)
- Number of sprites placed: 5 (1 goal-frame + 3 crates + 1 player).
- Composition by role: 1 goal-frame (`jigtxgzhwt` at (28, 28)) + 3 crates (`pktgsotzmw` at (44, 24), (16, 28), (32, 36)) + 1 player (`wppuejnwhl` at (32, 48)). No drone, no white agent, no wall, no stones.
- Level data: `{"StepCounter": 200}` — sets `kuncbnslnm.dbdarsgrbj = 200` in `on_set_level`.
- Spawn position(s): player at (32, 48), bottom-centre of the 64x64 grid. Note all positions are 4-aligned (multiples of 4) — the `celomdfhbh = 4` constant enforces a 4-pixel movement quantum.
- Per-cell layout: 64x64 grid, but only 16x16 effective cells due to the 4-pixel quantisation. Goal-frame fills cells (28..40 cols, 28..32 rows) — 3 horizontal × 1 vertical 4x4 slots inside. Crates at cells (44, 24), (16, 28), (32, 36). Player at (32, 48).
- Mechanic introduced relative to the previous level: this is the first level — introduces the **lock-and-drag** mechanic. Pressing UP/DOWN/LEFT/RIGHT (ACTION1-4) moves the player by 4 cells in that direction, also rotating the player sprite to face the new direction. Pressing ACTION5 either (a) unlocks the player from a currently-locked crate, or (b) locks onto an adjacent crate (where adjacency is defined by `vwiozbtqgi` — checks if a crate sits exactly 4 cells in the player's facing direction). When locked, the next movement drags the locked crate one cell along the same direction (preserving the relative offset). Win when all 3 crates' (x, y) are inside `wyzquhjerd` (the cells of the goal-frame). Movement is rejected if the destination is in `pkbufziase` (the collidable-occupancy set, including borders -4 and 64).
- Specific challenge: deliver 3 crates from their scattered positions into a 12x4 horizontal goal-frame. The player must lock-walk-unlock for each crate (~6-8 actions per crate, depending on path length). Total ~20-25 actions for direct routes.
- Estimated optimal action count: ~25 (3 crates × ~7 actions per crate).

### Level 2
- `grid_size`: (64, 64)
- Number of sprites placed: 8 (1 drone + 1 goal-frame + 5 crates + 1 player).
- Composition by role: 1 purple drone (`byigobxzpg` at (24, 36)) + 1 tall goal-frame (`doijajrgdi` 8x12 at (12, 28)) + 5 crates (`pktgsotzmw` at (48, 32), (36, 28), (40, 20), (48, 24), (44, 40)) + 1 player (`wppuejnwhl` at (12, 8)).
- Level data: `{"StepCounter": 70}` — much tighter budget than L1.
- Spawn position(s): player at (12, 8), top-left.
- Per-cell layout: 64x64. Goal-frame at cells x=12..19, y=28..39 (8x12). 5 crates clustered in the right half of the grid at x=36..48, y=20..40. Drone at (24, 36) sits between the player and the crate cluster.
- Mechanic introduced relative to L1: **AI competitor** (purple drone). After every player action, the drone takes a "turn" via `ynmgxjqkgh()`. The drone's behaviour is identical to the player's strategy: BFS for the nearest passive crate, lock onto it when adjacent, BFS toward the goal-frame, drop the crate inside. The drone competes with the player for crates — only one agent can be locked to a given crate at a time (`zmqreragji[crate]` maps crate → its owner; if the drone tries to lock to a crate the player owns, the lock fails).

  Crucially, the drone CAN deliver crates to the goal-frame too — the win predicate counts ALL crates regardless of who delivered them. So the drone is actually a *helper* / *parallel worker*, not an adversary. The competition is over which player gets which crate.
- Specific challenge: 5 crates to deliver, only 70 step budget. With a drone helping, the player needs to deliver ~3 crates while the drone delivers ~2 (or vice versa). The tight budget means the player should pick crates closest to the goal-frame and let the drone pick up the rest.
- Estimated optimal action count: ~35 player actions (3-4 crates × 7-8 actions). Within 70 budget.

### Level 3
- `grid_size`: (64, 64)
- Number of sprites placed: 24 (1 drone + 1 goal-frame + 5 crates + 13 walls + 1 player + crate at (32, 12)).

  Recount: 1 drone (`byigobxzpg` at (48, 12)) + 1 tall goal-frame (`ktghqrydvd` 8x16 at (52, 24)) + 5 crates (`pktgsotzmw` at (32, 32), (20, 20), (12, 44), (8, 16), (32, 12)) + 13 wall sprites (`pmargquscu` × 13 forming a vertical wall column at x=32, y=0,4,8,…,60) + 1 player (`wppuejnwhl` at (16, 36)) = 1+1+5+13+1 = 21. With set positions of the crates at (32, 12) and walls at (32, 12), there's overlap. Actually one of the walls is at (32, 12) which is the same as a crate — so the wall sits beneath the crate? Looking at the source level 3 sprite list (lines 374-403), I count 24 entries.
- Composition by role: 1 drone, 1 goal-frame, 5 crates, 13 walls (`pmargquscu`), 1 player.
- Level data: `{"StepCounter": 100}`.
- Spawn position(s): player at (16, 36), middle-left. Drone at (48, 12), top-right.
- Per-cell layout: walls form a vertical column at x=32, y=0..60 every 4 cells = 16 wall cells (but only 13 are placed; 3 gaps allow passage). Goal-frame at right side x=52..59, y=24..39. Crates scattered with one each in the left half ((20, 20), (8, 16), (12, 44)) and one each on the right ((32, 32), (32, 12)). Note (32, 12) overlaps with a wall position — the wall is at (32, 12) too, so there's a sprite stack.

  Actually re-reading: `pmargquscu` has `collidable=False` so it's NOT added to `pkbufziase` automatically. Instead, walls are tracked via `qthdiggudy` (the `bnzklblgdk` tag set). `kblzhbvysd(v)` checks `v not in self.pkbufziase and v not in self.qthdiggudy`. So a crate CAN sit at the same world cell as a wall (the wall is in `qthdiggudy`, the crate in `pkbufziase`, but they're checked separately). The crate is reachable by the player/drone.
- Mechanic introduced relative to L2: **Walls** that block movement. The vertical column at x=32 with 4-cell gaps means agents must navigate around or through the gaps. Combined with the drone competing for crates, this adds spatial planning: which agent reaches which crate via which gap?
- Specific challenge: 5 crates split across the wall, with the goal-frame on the right side. The player starts on the left side of the wall; the drone starts on the right. Crates are distributed: 3 on left (player's side), 2 on right (drone's side). The player and drone naturally divide labour by side, but each must traverse the wall via gaps to reach crates on the other side.
- Estimated optimal action count: ~50 (5 crates total × ~10 actions including wall navigation).

Levels 4 through 9 exist but are excluded per skill scope.

## Action handlers

### ACTION1 (UP), ACTION2 (DOWN), ACTION3 (LEFT), ACTION4 (RIGHT)
- Trigger: `self.action.id == GameAction.ACTION1/2/3/4`.
- Branches inside `step()`: dispatched via `yygfcvqoyx(self.action)`. Each direction sets (dx, dy) to (0, -4), (0, 4), (-4, 0), (4, 0) respectively. Decrement step counter via `kuncbnslnm.pfakmupgbr()` (returns False if counter hits 0). Call `qnmfimgpwc(player, dx, dy)` which:
  - If player is NOT currently locked to anything: set player rotation to face the move direction (`pjedoipwee` → 0/90/180/270).
  - Call `wqwsvmhhzj(player, player.x + dx, player.y + dy)`:
    - If player IS locked: compute the offset to the locked crate (`tkrlgpoppf.x - player.x`, `tkrlgpoppf.y - player.y`); validate the move via `fuykgiiwit` which checks both the player's destination and the locked-crate's destination are clear of `pkbufziase` and `qthdiggudy`. If valid, remove both sprites from `pkbufziase`, set both to new positions, re-add to `pkbufziase`. Run `lgirylubbp()` to recompute the disposal-adjacency set.
    - If player is NOT locked: validate the move via `kblzhbvysd` (destination not in `pkbufziase` or `qthdiggudy`). If valid, remove old position from `pkbufziase`, set new position, re-add.
- Then call `dhrikuybfo()` which runs `ynmgxjqkgh()` (purple AI step), `aoeyzovteg()` (white agent step — none in L1-3), and `zzppkjnqgk()` (recolour all crates and white agents based on adjacency / lock state).
- Then check `ymzfopzgbq()` (win) → `next_level()`, or `kuncbnslnm.current_steps == 0` (lose) → `lose()`.
- State mutations: read `self.action`, `self.nsevyuople`, `self.zmqreragji`, `self.pkbufziase`, `self.qthdiggudy`, `self.kuncbnslnm`. Written: `kuncbnslnm.current_steps`, `pkbufziase`, player.position, possibly locked-crate.position, player.rotation, every crate's `pixels` (via `uxricavavq` recolouring).
- Side effects on sprites: player and locked-crate `set_position`, `set_rotation`. Every crate's `pixels[:, 0/3]` and `pixels[0/3, :]` (the outer ring) recoloured per state.
- Engine effects: `next_level()` if all crates in goal-frames; `lose()` if step counter hits 0.
- Pre-conditions / gating: if player or locked-crate destination is in `pkbufziase` or `qthdiggudy`, the move is silently rejected (no position update). The step counter still decrements.

### ACTION5 (lock-or-unlock)
- Trigger: `self.action.id == GameAction.ACTION5`.
- Branches: decrement step counter. If player is in `nsevyuople` (locked to a crate), call `kqrtstlzkg(player)` to unlock — removes the entry from both `nsevyuople[player]` and `zmqreragji[crate]`, then refreshes adjacency sets. Otherwise iterate over every `geezpjgiyd`-tagged crate; if any sits exactly 4 cells in the player's facing direction (`vwiozbtqgi(player, crate)` checks based on `player.rotation`), lock onto it via `xpcvspllwr(player, crate)`. Then iterate over every `ysysltqlke`-tagged white agent; if any is in front of the player, unlock that agent from any crate it owns AND remove the agent from the level (`current_level.remove_sprite(agent)`) — i.e. ACTION5 KILLS adjacent white agents (out of scope for L1-3 since no white agents are placed).
- Then `dhrikuybfo()` — same as movement actions.
- State mutations: `kuncbnslnm.current_steps`, `nsevyuople`, `zmqreragji`, possibly `pkbufziase` (when killing an agent).
- Side effects on sprites: lock/unlock recolours the affected crate via `zzppkjnqgk`. Killing an agent removes it from the level.
- Engine effects: `next_level()` if win predicate now holds; `lose()` if budget exhausted.
- Pre-conditions / gating: lock fails silently if no crate is in the player's facing cell. Kill-white-agent fails silently if no white agent is in the player's facing cell. The step counter still decrements regardless.

## HUD widgets

### `etuniyewsy` — bottom-row depleting step bar
- Class name (obfuscated): `etuniyewsy`.
- Render-pixel range: row 63 (very bottom row), all 64 columns.
- What value it displays: `self.current_steps / self.dbdarsgrbj` — proportion of step budget remaining. `dbdarsgrbj` is set to `level.get_data("StepCounter")` per level (200, 70, 100 for L1, L2, L3).
- Visual style: row 63 — palette-7 (pink) cells fill from the LEFT for `eagwaqduxs = round(64 * remaining/total)` cells; palette-4 (background-grey) fills the rest. As budget drains, the pink segment shrinks from the right edge toward the left.
- Update points: `pfakmupgbr` is called once per ACTION1-5 (decrements counter), `ububboesmh` is called in `xcuqvqnmiu` from `on_set_level` (resets to max).
- Where it is registered: instantiated in `__init__` as `self.kuncbnslnm = etuniyewsy(0)` and added to the camera via `interfaces=[self.kuncbnslnm]` at line 868.

## Internal state — exhaustive

| attr (obfuscated) | semantic name | type | initial value | written by | read by | role |
|---|---|---|---|---|---|---|
| `kuncbnslnm` | step_counter_HUD | `etuniyewsy` | `etuniyewsy(0)` | `__init__`, `on_set_level` (via `xcuqvqnmiu`), `yygfcvqoyx` | `step` (lose check), `_get_hidden_state`, render | the bottom-row step bar; `dbdarsgrbj` is the per-level max, `current_steps` counts down |
| `nsevyuople` | agent_to_locked_crate | `dict[Sprite, Sprite]` | `{}` | `__init__`, `on_set_level`, `xpcvspllwr`, `kqrtstlzkg` | `wqwsvmhhzj`, `qnmfimgpwc`, `cyjrduhzmz`, `egqayvffim`, `ynmgxjqkgh`, `aoeyzovteg`, `yygfcvqoyx` | maps each agent (player, drone, white) to its currently-locked crate; missing entry means agent is free |
| `zmqreragji` | crate_to_locking_agent | `dict[Sprite, Sprite]` | `{}` | `on_set_level`, `xpcvspllwr`, `kqrtstlzkg` | `vyltpasvhc`, `xpcvspllwr`, `zzppkjnqgk`, `ymzfopzgbq` | inverse of `nsevyuople`: maps each locked crate to its owning agent; used to check "is this crate already taken" |
| `pkbufziase` | occupied_cells | `set[tuple[int, int]]` | `set()` | `on_set_level` (from collidables and grid borders), `wqwsvmhhzj`, `yygfcvqoyx` (when killing white agent) | `kblzhbvysd`, `fuykgiiwit`, `czrprbohhe`, `cyjrduhzmz`, `zauouvdhta`, `egqayvffim` | every collidable sprite's (x, y) plus 64 border-sentinel positions outside the grid; gates movement |
| `wyzquhjerd` | goal_frame_cells | `set[tuple[int, int]]` | `set()` | `on_set_level` | `shbxbhnhjc`, `ynmgxjqkgh`, `cyjrduhzmz`, `ymzfopzgbq` | every cell of every `fsjjayjoeg`-tagged goal-frame sprite (including borders); the win predicate requires every crate's (x, y) to lie in this set |
| `lqctaojiby` | disposal_zone_cells | `set[tuple[int, int]]` | `set()` | `on_set_level` | `ahzqkfjpsc`, `aoeyzovteg`, `egqayvffim`, `lgirylubbp` | every cell of every `zqxwgacnue`-tagged disposal sprite; used by white-agent goal-seeking (out of scope for L1-3) |
| `qthdiggudy` | wall_cells | `set[tuple[int, int]]` | `set()` | `on_set_level` | `kblzhbvysd`, `fuykgiiwit` | every (x, y) of every `bnzklblgdk`-tagged wall sprite (`pmargquscu` in L3); gates movement |
| `lkvghqfwan` | crate_adjacency_cells | `set[tuple[int, int]]` | `set()` | `on_set_level` (via `vyltpasvhc`), `xpcvspllwr`, `kqrtstlzkg` | `czrprbohhe` (BFS goal-set for unlocked drones) | the union of cells adjacent (4-cells in any direction) to every unlocked crate; used as the BFS target for an unlocked drone seeking a crate to grab |
| `uuorgjazmj` | locked_crate_destination_set | `set[tuple[int, int]]` | `set()` | `on_set_level` (via `lgirylubbp`), `xpcvspllwr`, `kqrtstlzkg`, `wqwsvmhhzj` | `zauouvdhta` (BFS goal-set for unlocked white) | similar to `lkvghqfwan` but only for crates eligible for white-agent acquisition (excludes crates locked to white agents) |
| (inherited) `_action_count` | engine action count | int | 0 | engine | not directly read | engine-level action counter; the game uses its own `kuncbnslnm.current_steps` instead |

## Win condition

Plain English: the level wins when every crate's (x, y) corner lies inside some goal-frame, AND no crate is currently locked to any agent.

Literal condition: `self.ymzfopzgbq()` (lines 1177-1179):
```python
def ymzfopzgbq(self) -> bool:
    fyfxmnwzhp = self.current_level.get_sprites_by_tag("geezpjgiyd")
    return all([self.shbxbhnhjc((ijudbtgsll.x, ijudbtgsll.y))
                and ijudbtgsll not in self.zmqreragji
                for ijudbtgsll in fyfxmnwzhp])
```

Where `shbxbhnhjc(v) = v in self.wyzquhjerd` checks the cell is in the goal-frame set.

Called from `step()` at line 1233 immediately after every action. On True, `self.next_level()`.

Same predicate for L1, L2, L3.

## Lose condition

Plain English: lose if the step counter reaches 0 with crates still un-delivered.

Literal condition: at line 1235 in `step()`:
```python
elif not self.kuncbnslnm.current_steps:
    self.lose()
```

The lose check fires only if the win predicate is False. So if the player happens to win with 0 steps remaining, `next_level()` fires before `lose()`.

There is no other lose path (no hazard, no respawn cost).

## Resource economy

- Depleting resource (energy / step counter / lives): YES — `kuncbnslnm.current_steps`, displayed as the bottom-row pink-shrinking bar by `etuniyewsy`. Decremented by 1 per action (UP/DOWN/LEFT/RIGHT/lock). Initial value is per-level: 200 (L1), 70 (L2), 100 (L3); 100, 125, 75, 125, 150, 70 for L4-9.
- Accumulating resource (collected items, score, sequence progress): YES (implicit) — the count of crates inside goal-frames. Tracked indirectly via the win predicate; no explicit counter.
- Lives mechanic (respawn cost): NO. Single `lose()` ends the game.
- Resource interaction with win/lose: step counter is the sole lose trigger; goal-frame fill is the sole win trigger. Independent: running out of steps cannot win; an early win short-circuits the budget.

## Action-budget signature

- Default budget per level: per-level via `level.get_data("StepCounter")`. L1=200, L2=70, L3=100.
- Whether budget tightens or shifts across levels 1-3: YES — L1 has 200 (generous tutorial), L2 drops to 70 (much tighter, but a drone helper offsets), L3 climbs back to 100.
- Per-level vs. per-environment: per-level (reset by `xcuqvqnmiu` in `on_set_level`).
- Decrement rate per action: 1 per action (UP/DOWN/LEFT/RIGHT/lock all cost 1). Even rejected moves (move into a wall) cost 1.
- Refill mechanism: NONE.

## Notable code patterns / techniques

- **4-pixel quantum grid**: every position and offset is a multiple of `celomdfhbh = 4`. The 64x64 frame is effectively a 16x16 logical grid. All collision sets, BFS expansions, and adjacency checks use 4-cell stride. This is a clean way to render at 64x64 while operating on a coarser logical grid.
- **Per-tag occupancy sets** (`pkbufziase`, `wyzquhjerd`, `lqctaojiby`, `qthdiggudy`): instead of querying the level's sprite list every check, `on_set_level` builds set-of-cells indices keyed by tag. `kblzhbvysd` and `fuykgiiwit` then run in O(1) per check. A clean cache pattern.
- **Border-sentinel cells in `pkbufziase`** (lines 896-900): adds (`-celomdfhbh, i`), (`64, i`), (`i, -celomdfhbh`), (`i, 64`) for `i in range(0, 64, 4)` — i.e. ghost cells just outside the grid in all 4 directions. Movement bounds-checking is unified with collision-checking through this trick: a move that would step out of the grid hits a sentinel cell and is rejected by the same `kblzhbvysd` predicate as a wall hit.
- **BFS for AI movement** (`czrprbohhe`, `cyjrduhzmz`, `zauouvdhta`, `egqayvffim`): four near-identical BFS routines compute the next step toward different goal-sets (crate-adjacent, goal-frame-from-locked, disposal-adjacent, disposal-from-locked). Each AI agent advances one step per game tick by following the shortest BFS path.
- **Lock-pair as bidirectional dict** (`nsevyuople` / `zmqreragji`): forward and reverse maps for agent↔crate locks. Allows O(1) "is this agent locked?", "is this crate taken?", and "who has this crate?".
- **In-place pixel mutation for state-feedback** (`uxricavavq`): rewrites the outer ring of a 4x4 sprite in-place to encode runtime state via colour. The crate's outer ring colour reads as: 4 (free), 3 (adjacent to player), 0 (player-locked), 5 (drone-locked).
- **Direction-encoded rotation** (`pjedoipwee`): converts (dx, dy) to one of four rotation angles 0/90/180/270 by direction priority. Used to rotate the player's "cap" to face the last move direction.
- **`fuykgiiwit` validates locked-pair moves**: special collision check that allows the locked pair to "swap into each other's cells" (the source and destination of the pair). This is critical for preventing self-collisions during locked movement.
- **Recolour-pass after every action** (`zzppkjnqgk`): runs after every action to re-derive every crate and white-agent's colour from current lock/adjacency state. Keeps the visual perfectly synced to the logical state without scattered set-colour calls throughout the step logic.

## Anti-patterns / lessons

- **Four near-identical BFS functions** (`czrprbohhe`, `cyjrduhzmz`, `zauouvdhta`, `egqayvffim`) — copy-paste with different goal-checks and different validity predicates. A generated game should consolidate to one parameterised BFS.
- **Massive 64x20 / 64x16 background sprites** (`aidclcbjcv`, `cwefnfvjhr`) — defined but only used in L7+. Not relevant for a 3-level game.
- **9 different goal-frame shapes** (`doijajrgdi`, `ghklglzjuf`, `jigtxgzhwt`, `ktghqrydvd`, `ofwegeqknn`, `peimznrlqd`, `vikkhnsrzd`, `wkmuwhjqyo`, `xxmzyqktqy`) — every level uses a slightly different aspect ratio. For a 3-level generated game, one or two goal-frame shapes is plenty.
- **Two adversary types** (purple drone `kdweefinfi`, white agent `ysysltqlke`) — out of scope for L1-3 except the drone in L2-3. A generated game should pick one adversary and stick with it.
- **Wall sprite `pmargquscu` is `collidable=False`** but tracked manually via tag — the engine's collision system isn't being used. A generated game should set walls to `collidable=True` and skip the manual `qthdiggudy` set.
- **Step budget decrements on rejected moves** — pressing into a wall still costs 1. A more forgiving generated game might exempt rejected moves to reduce frustration.
- **Player rotation only applies when not locked** (line 971-973) — when locked to a crate, the player's cap stops rotating to face new directions. This is a subtle visual inconsistency.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES (bottom row, full-width depleting horizontal bar).
- Has lives mechanic: NO.
- Has click-to-select (uses ACTION6): NO.
- Has tag-based grouping (uses `level.get_sprites_by_tag`): YES — heavy reliance: `fsjjayjoeg`, `zqxwgacnue`, `bnzklblgdk`, `geezpjgiyd`, `kdweefinfi`, `ysysltqlke`, `wbmdvjhthc` are all queried via tag.
- Uses ACTION5 (modal): YES (lock-or-unlock).
- Uses ACTION6 (click): NO.
- Uses ACTION7: NO.
- Has level data dicts (uses `level.get_data` / `level.set_data`): YES (`level.get_data("StepCounter")`).
- Multi-mechanic per level (vs. single mechanic per level): NO — same lock-and-drag mechanic in all three; L2 adds a drone, L3 adds walls, but the core "push crates to goal-frame" stays.
- Tutorial level appears solvable by random play: NO. With 200 steps and 3 crates each requiring deliberate sequencing, random play would mostly burn the budget on rejected moves and unlock-without-target.
- Has a depleting resource: YES — step counter, per-level (200/70/100).
- Has an accumulating resource: YES — count of crates in goal-frames (implicit, not displayed).
- Sprite shape convention used: mixed — solid rectangles (player, drone, crates, agents), hollow rectangles (goal-frames), striped wall, transparent (-2) cells in walls.
- HUD position: bottom (single row).
- Palette size used: 8 distinct palette values appear in placed L1-3 sprites: {0, 2, 4, 9, 12, 14} from sprites + {3, 5} drawn at runtime by `uxricavavq` recolouring crates. Total = 8.
- Background colour value: 1 (`BACKGROUND_COLOR = 1`).
- Padding / letter-box colour value: 0 (`PADDING_COLOR = 0`).
- Number of distinct mechanics introduced across levels 1-3: 3 (lock-and-drag in L1, drone competitor in L2, walls in L3).
- Number of levels documented: 3.

(End of file.)
