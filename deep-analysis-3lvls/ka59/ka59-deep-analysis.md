# ka59 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/ka59/9f096b4a/ka59.py`
- Lines: 1663
- Class name: `Ka59`
- available_actions: `[1, 2, 3, 4, 6]` (UP/DOWN/LEFT/RIGHT, ACTION6=click-to-switch-active)
- Number of levels in source: 7
- Number of levels documented in this analysis: 3
- Imports: `NovaBaseGame`, `Camera`, `GameAction`, `Level`, `RenderableUserDisplay`, `Sprite` from `novaengine`; `numpy as np`.

## Mechanic essence (one sentence)

A handful of coloured pawns sit scattered across a walled arena, and the player clicks one to make it active and presses an arrow to slide it three cells — pushing any pawns it bumps into recursively along the same line — while explode-tiles spray the eight surrounding pawns outward and a slow chaser shuffles toward the active pawn each turn; the level is solved when every coloured target square has a pawn (or an enemy on its enemy-target) sitting on it.

## Sprite roster

| sprite (obfuscated) | dims | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| `ahupezxcuy` | varies | (palette specific) | gobzaprasa | (default) | YES | (default) | YES | corner explode-tile (level 5+) |
| `awtopsutqo` | 51x51 | (palette specific) | divgcilurm | (default) | YES | (default) | YES | L1 outer level frame |
| `cisjjwiopp` | varies | (palette specific) | xlfuqjygey, sys_click | (default) | YES | (default) | YES | player pawn variant (L2, L7) |
| `cnoctyjgvb` | 60x60 | (palette specific) | divgcilurm | (default) | YES | (default) | YES | L4 outer frame |
| `crgdfmgpyr` | 60x60 | (palette specific) | divgcilurm | (default) | YES | (default) | YES | L3 outer frame |
| `ctttougcls` | 69x69 | (palette specific) | divgcilurm | (default) | YES | (default) | YES | L5 outer frame |
| `ejsiqtothk` | 65x57 | (palette specific) | divgcilurm | (default) | YES | (default) | YES | L7 outer frame |
| `explode-3-1` | 9x9 | 13 | whiknkvuty, llnhiluenw | (default) | YES | (default) | YES | explosion animation tick 1 (3-wide source) |
| `explode-3-2` | 9x9 | 13 | whiknkvuty, llnhiluenw | (default) | YES | (default) | YES | explosion animation tick 2 |
| `explode-3-3` | 9x9 | 13 | whiknkvuty, llnhiluenw | (default) | YES | (default) | YES | explosion animation tick 3 |
| `explode-6-1` | 12x12 | 13 | whiknkvuty, llnhiluenw | (default) | YES | (default) | YES | explosion animation tick 1 (6-wide source) |
| `explode-6-2` | 12x12 | 13 | whiknkvuty, llnhiluenw | (default) | YES | (default) | YES | explosion animation tick 2 |
| `explode-6-3` | 12x12 | 13 | whiknkvuty, llnhiluenw | (default) | YES | (default) | YES | explosion animation tick 3 |
| `gamgogbomz` | 69x69 | (palette specific) | divgcilurm | (default) | YES | (default) | YES | L2 outer frame |
| `guzlfxebqr` | varies | (palette specific) | nnckfubbhi | (default) | YES | (default) | YES | enemy chaser variant (L5+) |
| `gypjdeisqg` | varies | (palette specific) | vwjqkxkyxm | (default) | YES | (default) | YES | inner wall (L2) |
| `hvalrvllph` | varies | (palette specific) | gobzaprasa | (default) | YES | (default) | YES | explode-tile (L5) |
| `kdqjpjawgp` | varies | (palette specific) | vwjqkxkyxm | (default) | YES | (default) | YES | inner wall (L5) |
| `peoafdrnua` | 6x6 | (palette specific) | xlfuqjygey, sys_click | (default) | YES | (default) | YES | player pawn variant (L2) |
| `pomlugyufe` | 6x6 | (palette specific) | xlfuqjygey, sys_click | (default) | YES | (default) | YES | primary player pawn — used in every L1-3 level |
| `puozseozpy` | 69x69 | (palette specific) | divgcilurm | (default) | YES | (default) | YES | L6 outer frame |
| `pyqqacvnjx` | 6x6 | (palette specific) | rktpmjcpkt | (default) | YES | (default) | YES | player-target square (L2) |
| `roeurgaobs` | varies | (palette specific) | gobzaprasa | (default) | YES | (default) | YES | explode-tile variant (level 6+) |
| `sfcitxooao` | varies | (palette specific) | xlfuqjygey, sys_click | (default) | YES | (default) | YES | player pawn variant (L2, L7) |
| `sflczmmopv` | varies | (palette specific) | vwjqkxkyxm | (default) | YES | (default) | YES | inner wall (L6) |
| `spsfzvxpoo` | varies | (palette specific) | vwjqkxkyxm | (default) | YES | (default) | YES | inner wall (L7) |
| `sxasgylpxm` | varies | (palette specific) | rktpmjcpkt | (default) | YES | (default) | YES | player-target (L2, L7) |
| `thewpulaxq` | varies | (palette specific) | ucjzrlvfkb | (default) | YES | (default) | YES | enemy-target square — only enemies satisfy this |
| `wewoeeghkd` | 6x6 | (palette specific) | rktpmjcpkt | (default) | YES | (default) | YES | primary player-target — used in every L1-3 level |
| `wrxsaqlvhe` | varies | (palette specific) | vwjqkxkyxm | (default) | YES | (default) | YES | inner wall (L1) |
| `xozzfidseo` | 6x6 | (palette specific) | rktpmjcpkt | (default) | YES | (default) | YES | player-target (L2, L7) |
| `ynfdrywqny` | varies | (palette specific) | vwjqkxkyxm | (default) | YES | (default) | YES | inner wall (L4) |
| `yxphjztrgf` | varies | (palette specific) | nnckfubbhi | (default) | YES | (default) | YES | enemy chaser — moves toward active player each turn |

(For brevity, full per-sprite subsections are aggregated by tag-group; each sprite within a tag group plays the same role.)

### Tag-group: `divgcilurm` (outer frames)
- Sprites: `awtopsutqo`, `gamgogbomz`, `crgdfmgpyr`, `cnoctyjgvb`, `ctttougcls`, `puozseozpy`, `ejsiqtothk` (one per level).
- Pixel pattern: large NxN hollow rectangle of palette-3 (or similar) outline with -1 transparent interior.
- Where they appear: one outer frame per level, placed at (-3, -3) to extend just outside the playfield.
- Role: impassable boundary; queried in `aqoyvqxpct` to detect "block can't move into the wall".
- Visual-vs-functional read: thin solid frame around the playfield. Player tells them apart only by which level they appear in — they're functionally identical.

### Tag-group: `xlfuqjygey + sys_click` (player pawns)
- Sprites: `pomlugyufe` (every level), `cisjjwiopp` (L2, L7), `peoafdrnua` (L2), `sfcitxooao` (L2, L7).
- Pixel pattern: 6x6 coloured square with palette-X centre (0/4 colour code).
- Role: a controllable pawn. Multiple pawns per level; one is "active" (`ascpmvdpwj`) at any time; click switches active. Active pawn responds to arrow keys (moves 3 cells). On collision with non-active pawns, recursive Sokoban-style push (`esglqyymck`).
- Visual-vs-functional read: at-rendered-scale, 6x6 coloured square; the active one is recoloured to palette-0 (`ikmfqdniny`) via `yrzfpsrdrm` to mark active state. Inactive pawns are palette-4 (`pjzynjktxf`).

### Tag-group: `rktpmjcpkt` (player-targets)
- Sprites: `wewoeeghkd`, `pyqqacvnjx`, `sxasgylpxm`, `xozzfidseo`.
- Role: target squares the player must position pawns over. The win predicate `cbdaoltbck` checks that every `rktpmjcpkt` sprite has a `xlfuqjygey` pawn sitting at its (x+1, y+1) position — i.e. the pawn is exactly inscribed inside the target.
- Visual-vs-functional read: 6x6 hollow target square.

### Tag-group: `ucjzrlvfkb` (enemy-targets)
- Sprites: `thewpulaxq`.
- Role: target squares for enemies (`nnckfubbhi`). Win requires every enemy-target has an enemy pawn inscribed inside.

### Tag-group: `nnckfubbhi` (enemy chasers)
- Sprites: `yxphjztrgf`, `guzlfxebqr`.
- Role: enemy that chases the active player each turn. `tmuauqrmwt` runs greedy Manhattan-distance steps toward the active player; if the enemy lands on the active player, `lose()`.

### Tag-group: `vwjqkxkyxm` (inner walls)
- Sprites: `wrxsaqlvhe`, `gypjdeisqg`, `kdqjpjawgp`, `sflczmmopv`, `spsfzvxpoo`, `ynfdrywqny`.
- Role: small interior walls. Block movement of all pawns (player + enemy + explode targets).

### Tag-group: `gobzaprasa` (explode-tiles)
- Sprites: `ahupezxcuy`, `hvalrvllph`, `roeurgaobs`.
- Role: when an active player ends up overlapping (or near) an explode-tile, the tile sprays the 8 surrounding cells outward by 3 in their respective compass directions over a 3-tick animation. The animation uses the `explode-X-N` sprites as visual overlays. Out of scope for L1-3 except in level 5+ but the code path exists.

### Tag-group: `whiknkvuty + llnhiluenw` (explosion animation overlays)
- Sprites: `explode-3-1` through `explode-6-3` (3 sizes × 3 ticks each = 6 sprites).
- Role: visual overlays added during explosion animation; cleared after 3 ticks.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (45, 45)
- Number of sprites placed: 6.
- Composition: 1 outer frame (`awtopsutqo` at (-3, -3)), 2 player pawns (`pomlugyufe` at (9, 21) and (18, 21)), 2 player-targets (`wewoeeghkd` at (2, 23) and (35, 17)), 1 inner wall (`wrxsaqlvhe` at (24, 12)).
- Level data: `{"StepCounter": 100}`.
- Spawn position(s): no avatar; the active pawn defaults to the first `xlfuqjygey`-tagged sprite (the leftmost `pomlugyufe`).
- Per-cell layout: 45x45. 2 pawns side-by-side at row 21; 2 targets at row 23 (left) and row 17 (right). One wall in the middle.
- Mechanic introduced relative to the previous level: this is the first level — introduces the **multi-pawn Sokoban** mechanic. Click switches active pawn; arrows move active pawn 3 cells; if a non-active pawn is in the way, it gets pushed (recursive). Walls block movement. Win when both targets contain a pawn.
- Specific challenge: route 2 pawns to 2 targets. The wall at (24, 12) blocks direct paths.
- Estimated optimal action count: ~10-15.

### Level 2
- `grid_size`: (63, 63)
- Number of sprites placed: 10.
- Composition: 1 outer frame (`gamgogbomz`), 1 player-target (`pyqqacvnjx`), 1 enemy-target (`thewpulaxq`)... wait actually let me re-check L2: 1 cisjjwiopp (player), 1 gamgogbomz (frame), 1 gypjdeisqg (wall), 1 peoafdrnua (player), 1 pomlugyufe (player), 1 pyqqacvnjx (target), 1 sfcitxooao (player), 1 sxasgylpxm (target), 1 wewoeeghkd (target), 1 xozzfidseo (target). So 4 players, 4 targets, 1 wall, 1 frame.
- Level data: `{"StepCounter": 127}`.
- Composition refined: 4 player pawns + 4 player-targets + 1 wall + 1 frame.
- Mechanic introduced relative to L1: **Multi-pawn (4 instead of 2)** with click-to-switch becoming critical. More targets to fill.
- Specific challenge: route 4 pawns to 4 targets while pushing through the wall.
- Estimated optimal action count: ~25-40.

### Level 3
- `grid_size`: (54, 54)
- Number of sprites placed: 7.
- Composition: 1 outer frame (`crgdfmgpyr`), 1 player (`pomlugyufe`), 2 enemy-targets (`thewpulaxq` × 2), 1 player-target (`wewoeeghkd`), 2 enemies (`yxphjztrgf` × 2).
- Level data: `{"StepCounter": 100}`.
- Mechanic introduced relative to L2: **Enemies + enemy-targets**. Each turn after the player moves, every enemy steps 1 cell toward the active player (via `tmuauqrmwt`'s greedy chase). Enemies block movement. Win requires the player on the player-target AND each enemy on an enemy-target.
- Specific challenge: lure 2 enemies onto 2 enemy-target squares while the player simultaneously reaches the player-target. The chase mechanic means enemies follow the player, so positioning must direct them precisely.
- Estimated optimal action count: ~25-35.

Levels 4-7 exist but are excluded per skill scope.

## Action handlers

### ACTION1 / ACTION2 / ACTION3 / ACTION4 (UP / DOWN / LEFT / RIGHT)
- Trigger: `self.action.id in [GameAction.ACTION1..4]`.
- Branches: animation guards first (`osqsnogokn` and `zglbibxjth` queues). Otherwise:
  - Decrement step counter via `rciyayewnv.euooiuweso()`.
  - Call `aqoyvqxpct(active_pawn, dx, dy)` with (0, -3), (0, 3), (-3, 0), (3, 0) respectively. This attempts to move the active pawn; if it collides with a wall (`vwjqkxkyxm` or `divgcilurm`), reject; if it collides with another pawn or enemy, return the list of collisions for further processing.
  - If collisions returned, set `osqsnogokn = collisions`, store directions in `zhcrzgpwcp`, queue Sokoban push animation. Add `npkgknfkdf`/`gluqysfhzt`/`naomqrerji`/`auzmgazqte` collider sprite (a side-of-the-active-pawn sentinel) to the level so the chain push knows which side to push from. Mark the active pawn's edge palette-14 to indicate motion direction.
  - Otherwise (move succeeded with no collisions), call `zniafiymcd()` to advance enemies, then check `wzfqyavgic()` for any new explode-tiles to fire, queue them in `zglbibxjth`.
- After all motion & animation, call `obrnalfvlv()` to update the active pawn's edge palettes based on neighbour adjacency, then check `cbdaoltbck()` (win predicate) → `next_level()`. If step counter is 0, `lose()`. Else `complete_action()`.
- State mutations: `rciyayewnv.current_steps`, every pawn's position, `osqsnogokn`, `zglbibxjth`, `zhcrzgpwcp`, `msbtawvatm`, `ascpmvdpwj.pixels` (edge palettes).
- Engine effects: `next_level()` on win; `lose()` on enemy-catches-player or step counter 0.
- Pre-conditions / gating: rejected if the active pawn would hit a wall (silent no-op).

### ACTION6 (click — switch active pawn)
- Trigger: `self.action.id == GameAction.ACTION6`.
- Branches: read (x, y); convert via `display_to_grid`; find `xlfuqjygey`-tagged sprite at (game_x, game_y); call `ufbbcjjuxx(sprite)` which recolours old active pawn to palette-4 and new active pawn to palette-0.
- State mutations: `ascpmvdpwj`, both pawns' centre pixel.
- Engine effects: none direct.

## HUD widgets

### `inajiwvkvh` — bottom-row depleting step bar
- Class name: `inajiwvkvh`.
- Render-pixel range: row 63, all 64 columns.
- What value it displays: `current_steps / xetzkqhcfq` (per-level via `level.get_data("StepCounter")`: 100, 127, 100).
- Visual style: row 63 — palette-4 (aceihsjyjn) for remaining cells; palette-0 (zhstiyenwh) for depleted.

## Internal state — exhaustive

| attr (obfuscated) | semantic name | type | initial value | written by | read by | role |
|---|---|---|---|---|---|---|
| `rciyayewnv` | step_counter_HUD | `inajiwvkvh` | `inajiwvkvh(0)` | `__init__`, `on_set_level`, `step` | `step`, `_get_hidden_state` | step counter |
| `ascpmvdpwj` | active_pawn | `Sprite` | first `xlfuqjygey` | `on_set_level`, `ufbbcjjuxx` | `step` (movement), `obrnalfvlv` | the currently-controlled pawn |
| `osqsnogokn` | push_animation_queue | `list[Sprite]` | `[]` | `step` | `step` (animation guard) | sprites currently being pushed via Sokoban chain |
| `zhcrzgpwcp` | push_directions | `dict[Sprite, tuple[int, int]]` | `{}` | `step` | `tesoceiypr`, `step` | per-sprite (dx, dy) for the current push |
| `msbtawvatm` | animation_tick | int | 0 | `on_set_level`, `step` | `step` | sub-step counter for push and explode animations |
| `zglbibxjth` | exploding_tiles | `list[Sprite]` | `[]` | `on_set_level`, `step` (after move) | `step` (explosion animation) | explode-tiles activated by the current move |

## Win condition

Plain English: every player-target (`rktpmjcpkt`) has a player pawn inscribed inside it AND every enemy-target (`ucjzrlvfkb`) has an enemy inscribed inside it.

Literal condition: `cbdaoltbck()` (lines 1462-1473):
```python
for target in get_sprites_by_tag("rktpmjcpkt"):
    if not vbolnamxei(target, players):
        return False
for target in get_sprites_by_tag("ucjzrlvfkb"):
    if not vbolnamxei(target, enemies):
        return False
return True
```

Where `vbolnamxei(target, candidates)` returns True if any candidate is exactly inscribed in target (i.e. positioned at (target.x+1, target.y+1) with dimensions 2 less than target).

Same predicate for L1, L2, L3.

## Lose condition

Plain English: lose if (a) an enemy catches the active pawn, or (b) the step counter hits 0.

Literal condition: 
- Enemy catch: in `tmuauqrmwt` (line 1418-1420), if enemy's position equals active pawn's position after greedy chase, `self.lose()`.
- Step exhaustion: at line 1661, `elif not self.rciyayewnv.current_steps: self.lose()`.

## Resource economy

- Depleting resource: YES — `rciyayewnv.current_steps` (per-level: 100, 127, 100). Decremented by 1 per ACTION1-4 and ACTION6.
- Accumulating resource: YES — count of targets satisfied (implicit).
- Lives mechanic: NO. Single `lose()` ends game.
- Resource interaction: step counter is one lose trigger; enemy-collision is another; full-target-fill is the win.

## Action-budget signature

- Default budget per level: per-level via `level.get_data("StepCounter")`. L1=100, L2=127, L3=100.
- Whether budget tightens or shifts across levels 1-3: NO consistent direction.
- Per-level vs. per-environment: per-level (reset in `on_set_level`).
- Decrement rate per action: 1 per directional action and 1 per click.
- Refill mechanism: NONE.

## Notable code patterns / techniques

- **3-cell stride** (`jesnwclftg = 3`): all movement is in 3-pixel quanta.
- **Recursive Sokoban push** (`esglqyymck`): if pushing a pawn would collide with another pawn, recursively push that one too. If push fails, revert.
- **Active-pawn edge highlighting** (`obrnalfvlv`): the active pawn's outer ring is recoloured palette-14 (`annkmrfrcw`) on sides facing other blocks, palette-0 elsewhere — visual feedback about adjacency.
- **Enemy greedy chase** (`tmuauqrmwt`): up to 6 single-cell steps per turn toward the active pawn, choosing the dominant axis.
- **Explode-tile cascade** (`wzfqyavgic`, `egsdqzlidg`): when a player's edge touches an explode-tile, the tile fires; the cascade can chain.
- **Tag-based collision filter** (`fymskljcbk`): combined query for "is this any of the moveable types" (xlfuqjygey, nnckfubbhi, gobzaprasa).
- **Sentinel collider sprites** (`npkgknfkdf`, `gluqysfhzt`, etc.): added to the level temporarily during Sokoban push to indicate which side of the active pawn pushed.

## Anti-patterns / lessons

- **6 different outer-frame sprites** (one per level) — they're all just hollow rectangles of different sizes. A generated game should parameterise.
- **6 different inner-wall sprites** — same role, slight variations.
- **Active state encoded in pixel-mutation** (`yrzfpsrdrm` rewrites the centre pixels of pawns to palette-0/4). Fragile; a generated game should use `color_remap` or layer.
- **Enemy chase logic** uses Manhattan distance with axis preference — can deadlock if walls block. Generated games should validate solvability.
- **Multi-phase animation state** scattered across `osqsnogokn`, `zglbibxjth`, `zhcrzgpwcp`, `msbtawvatm` — error-prone. Generated games should consolidate.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES (bottom row).
- Has lives mechanic: NO.
- Has click-to-select (uses ACTION6): YES.
- Has tag-based grouping: YES (`xlfuqjygey`, `divgcilurm`, `vwjqkxkyxm`, `rktpmjcpkt`, `ucjzrlvfkb`, `nnckfubbhi`, `gobzaprasa`, `whiknkvuty`, `llnhiluenw`).
- Uses ACTION5 (modal): NO.
- Uses ACTION6 (click): YES.
- Uses ACTION7: NO.
- Has level data dicts: YES (`level.get_data("StepCounter")`).
- Multi-mechanic per level: NO — L1=push, L2=more pawns, L3=enemies.
- Tutorial level appears solvable by random play: NO. Sokoban requires planning.
- Has a depleting resource: YES — step counter.
- Has an accumulating resource: YES — targets satisfied.
- Sprite shape convention used: mixed — large hollow frames, small filled pawns, hollow target rings.
- HUD position: bottom.
- Palette size used: roughly 8 distinct values across L1-3 sprites.
- Background colour value: 1 (`BACKGROUND_COLOR = 1`).
- Padding / letter-box colour value: 2 (`PADDING_COLOR = 2`).
- Number of distinct mechanics introduced across levels 1-3: 3 (push in L1, more pawns in L2, enemies in L3).
- Number of levels documented: 3.

(End of file.)
