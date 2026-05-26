# sp80 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/sp80/0ee2d095/sp80.py`
- Lines: 874
- Class name: `Sp80`
- available_actions: `[1, 2, 3, 4, 5, 6]` (UP/DOWN/LEFT/RIGHT, ACTION5=pour, ACTION6=click)
- Number of levels in source: 6
- Number of levels documented in this analysis: 3
- Imports: `ActionInput`, `NovaBaseGame`, `Camera`, `GameAction`, `Level`, `RenderableUserDisplay`, `Sprite` from `novaengine`; `numpy as np`; `typing` items.

## Mechanic essence (one sentence)

A row of horizontal coloured shelves hangs above a row of empty U-cups, and the player clicks a shelf to grab it and slides it left or right with the arrow keys; pressing the pour key sends a drop of water plummeting from each marked spout — it splits when it lands on a shelf, falls straight when it doesn't, and the level is solved when every cup catches a drop in its open mouth, while drops that drift past every shelf and hit the bottom drain spend one of four pour attempts.

## Sprite roster

| sprite (obfuscated) | dims | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| `adbrqflmwi` | 7x1 | 4, 8 | ksmzdcblcz, syaipsfndp | (default) | YES | (default) | YES | 7-wide horizontal shelf with central palette-4 spout pixel (level 4+) |
| `jgfvrvnkaz` | 5x1 | 8 | ksmzdcblcz, sys_click | (default) | YES | (default) | YES | 5-wide horizontal shelf without a spout |
| `mdhkebfsmg` | 1x4 | 8 | ksmzdcblcz, sys_click | (default) | YES | (default) | YES | 4-tall vertical shelf (level 6+) |
| `nadtnzkesz` | 34x34 | 1, -1 | (default) | (default) | YES | (default) | YES | hollow palette-1 large boundary frame (defined but never placed) |
| `nkrtlkykwe` | 1x1 | 6 | nkrtlkykwe | (default) | YES | (default) | YES | water droplet — the falling water particle |
| `nvzozwqarf` | 8x1 | 8 | ksmzdcblcz, sys_click | (default) | YES | (default) | YES | 8-wide shelf (defined but never placed) |
| `odioorqnkn` | 6x1 | 8 | ksmzdcblcz, sys_click | (default) | YES | (default) | YES | 6-wide shelf (L3) |
| `qwsmjdrvqj` | 2x2 | 15, -1 | hfjpeygkxy, sys_click | (default) | YES | (default) | YES | corner deflector (level 5+) |
| `syaipsfndp` | 1x1 | 4 | syaipsfndp | (default) | YES | (default) | YES | spout marker — palette-4 pixel placed at the top edge to mark a drop source |
| `trurgcakbj` | 4x1 | 8 | ksmzdcblcz, sys_click | (default) | YES | (default) | YES | 4-wide shelf (L3) |
| `ttkatugvbk` | 22x22 | 1, -1 | (default) | (default) | YES | (default) | YES | hollow 22x22 boundary frame (level 4+) |
| `uihgaxtzkm` | 7x1 | 8 | ksmzdcblcz | (default) | YES | (default) | YES | 7-wide shelf without sys_click tag (defined but never placed) |
| `untfxhpddv` | 3x1 | 8 | ksmzdcblcz, sys_click | (default) | YES | (default) | YES | 3-wide shelf (L2) |
| `uzunfxpwmd` | 32x1 | 1 | uzunfxpwmd | (default) | YES | (default) | YES | floor/drain — catches missed drops and triggers spill-counter |
| `uzvelihpxo` | 18x18 | 1, -1 | (default) | (default) | YES | (default) | YES | 18x18 boundary frame around the 16x16 playfield |
| `vkwijvqdla` | 2x2 | 15, -1 | hfjpeygkxy, sys_click | (default) | YES | (default) | YES | mirror corner deflector (level 5+) |
| `xsrqllccpx` | 3x2 | 11, -1 | xsrqllccpx | (default) | YES | (default) | YES | U-cup catch target — top row `[11, -1, 11]` (open mouth), bottom row `[11, 11, 11]` (cup floor) |
| `zgsbadjnjn` | 5x1 | 4, 8 | ksmzdcblcz, syaipsfndp, sys_click | (default) | YES | (default) | YES | 5-wide shelf with central spout (level 6+) |

### `adbrqflmwi` — 7-wide spout-shelf (level 4+)
- Pixel pattern: 7x1, `[8, 8, 8, 4, 8, 8, 8]`. Six palette-8 pixels with a single palette-4 hole at column 3.
- Where it appears: not placed in L1-3.
- Role: out of scope.

### `jgfvrvnkaz` — 5-wide shelf (every L1-3 level)
- Pixel pattern: 5x1, all palette-8.
- Where it appears: L1 (1 copy at (3, 4)), L2 (1 at (6, 6)), L3 (1 at (1, 8)). Also L4-5.
- Role: a single movable shelf the player clicks and slides. When a falling drop hits this shelf, the drop splits into two new drops at the cells immediately left and right of the impact, both continuing to fall.
- Visual-vs-functional read: at-rendered-scale, a 5-pixel-wide horizontal palette-8 (orange) bar. Tag `ksmzdcblcz` distinguishes it as a "shelf" (drop-deflector); `sys_click` makes it clickable. Nearest-other: `untfxhpddv` (3-wide), `trurgcakbj` (4-wide), `odioorqnkn` (6-wide), `nvzozwqarf` (8-wide), `uihgaxtzkm` (7-wide) — same palette, different lengths. Player tells them apart by length — wider shelves cover more cells.

### `mdhkebfsmg` — vertical shelf (level 6+)
- Pixel pattern: 1x4 palette-8.
- Where it appears: not placed in L1-3.

### `nadtnzkesz` — large boundary (defined but never placed)
- Pixel pattern: 34x34 hollow.
- Where it appears: never placed.

### `nkrtlkykwe` — water droplet
- Pixel pattern: 1x1 palette-6 (magenta).
- Where it appears: every L1-3 level — pre-placed at the spout position (e.g. L1 at (9, 1)). Also dynamically spawned in `tadqvfdobr` whenever ACTION5 fires.
- Role: the falling water particle. Each "spill" tick advances every drop by its (worqgwkuyx, patlrtoom) direction. On collision with various sprite types: shelf → split into 2 side-drops; cup → fill cup if both adjacent cells are cup-cells; drain → die and increment spill counter.
- Visual-vs-functional read: single magenta dot. Reads as a water drop. Distinct from anything else by colour and tag.

### `nvzozwqarf` — 8-wide shelf (defined but never placed)
- Pixel pattern: 8x1 palette-8.
- Where it appears: never placed.

### `odioorqnkn` — 6-wide shelf (L3)
- Pixel pattern: 6x1 palette-8.
- Where it appears: L3 (2 copies at (8, 7) and (1, 5)).

### `qwsmjdrvqj` — upper-right hollow corner deflector (level 5+)
- Pixel pattern: 2x2, three palette-15 pixels with hollow upper-right.
- Where it appears: not placed in L1-3.

### `syaipsfndp` — top-edge spout marker
- Pixel pattern: 1x1 palette-4.
- Where it appears: every L1-3 level — placed at the top edge (y=0). L1 has 1 copy at (9, 0); L2 has 1 at (5, 0); L3 has 3 copies at (1, 0), (14, 0), (6, 0).
- Role: marks where a water drop spawns when ACTION5 (pour) fires. The `tadqvfdobr` spawn loop iterates every `syaipsfndp`-tagged sprite and spawns a `nkrtlkykwe` drop one cell BELOW each palette-4 pixel. Multiple sources mean multiple drops per pour.
- Visual-vs-functional read: single palette-4 (off-grey) cell at the top of the playfield. Reads as a tap/spout indicator.

### `trurgcakbj` — 4-wide shelf
- Pixel pattern: 4x1 palette-8.
- Where it appears: L3 (1 copy at (10, 10)). Also L4, L5.

### `ttkatugvbk` — 22x22 boundary (level 4+)
- Pixel pattern: hollow 22x22.
- Where it appears: not placed in L1-3.

### `uihgaxtzkm` — 7-wide shelf without sys_click (defined but never placed)
- Pixel pattern: 7x1 palette-8.
- Where it appears: never placed.

### `untfxhpddv` — 3-wide shelf (L2)
- Pixel pattern: 3x1 palette-8.
- Where it appears: L2 (2 copies at (6, 9) and (11, 11)).

### `uzunfxpwmd` — floor/drain
- Pixel pattern: 32x1 palette-1 (cyan).
- Where it appears: every L1-3 level (1 copy at (0, 15) — bottom row).
- Role: catches drops that miss every cup. When a drop lands on the drain, the drain pixel turns palette-14 (yellow flash), the drop is added to `szbmtoxgbd`, and `enlvswjeov` is set True (signals "spill happened"). After the win animation, if `enlvswjeov`, increment `zzocrmvox` (spill counter); after 4 spills, `lose()`.
- Visual-vs-functional read: at-rendered-scale, a 32-cell horizontal palette-1 line at the bottom of the playfield. Reads as a "ground" or "drain" line. Tag `uzunfxpwmd`. Distinct role.

### `uzvelihpxo` — 18x18 boundary frame
- Pixel pattern: 18x18 with palette-1 outer ring and -1 transparent interior.
- Where it appears: every L1-3 level (1 copy at (-1, -1) — placed offset so the 18-cell ring sits 1 cell outside the 16x16 playfield boundary).
- Role: cosmetic frame around the playfield. Doesn't affect collisions.
- Visual-vs-functional read: hollow palette-1 rectangle.

### `vkwijvqdla` — upper-left hollow corner deflector (level 5+)
- Pixel pattern: 2x2 mirror of `qwsmjdrvqj`.
- Where it appears: not placed in L1-3.

### `xsrqllccpx` — U-cup catch target
- Pixel pattern: 3x2; top row `[11, -1, 11]` (palette-11 corners with transparent middle); bottom row `[11, 11, 11]` (solid bottom).
- Where it appears: every L1-3 level. L1 has 2 cups at (4, 13) and (10, 13); L2 has 3 at (2, 13), (6, 13), (10, 13); L3 has 3 at (1, 13), (12, 13), (7, 13).
- Role: catch-target. When a drop currently sitting in the cup's mouth (col = position.x + 1, row = position.y) attempts to move further down and the cells to its left and right are both palette-11 (cup arms), the cup is "filled" — pixels recoloured to palette-13 (red) and the cup is added to `srwrqoodsc`. Win when all cups are in `srwrqoodsc`.
- Visual-vs-functional read: at-rendered-scale, a yellow U-shape with a hollow centre. Reads as a small chalice / catch cup. Distinct role and palette.

### `zgsbadjnjn` — 5-wide spout shelf (level 6+)
- Pixel pattern: 5x1, `[8, 8, 4, 8, 8]`. Central palette-4 spout in middle of palette-8 strip.
- Where it appears: not placed in L1-3.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (16, 16)
- Number of sprites placed: 7.
- Composition: 1 shelf (`jgfvrvnkaz` 5x1 at (3, 4)), 1 spout marker (`syaipsfndp` at (9, 0)), 1 pre-placed droplet (`nkrtlkykwe` at (9, 1)), 1 floor (`uzunfxpwmd` at (0, 15)), 1 boundary frame (`uzvelihpxo` at (-1, -1)), 2 cups (`xsrqllccpx` at (4, 13) and (10, 13)).
- Level data: `{"steps": 30, "rotation": 0}`.
- Spawn position(s): no avatar; the player's "selected sprite" defaults to the closest movable shelf to the origin (set via `ckahxkcgfi` → `gchfqtwjap` in `on_set_level`).
- Per-cell layout: 16x16. Spout marker at (9, 0). Shelf at (3, 4) spans columns 3-7 row 4. Floor at row 15. Cups at row 13 spanning columns 4-6 and 10-12.
- Mechanic introduced relative to the previous level: this is the first level — introduces the **shelf-arrange + pour** mechanic. The player has 30 steps and 4 pour attempts. Each step (UP/DOWN/LEFT/RIGHT/click/pour) decrements the step counter via `rpnnowtzay`. The player can click a shelf to select it (`gchfqtwjap`), arrow-keys slide it (`try_move_sprite`), and ACTION5 fires `tadqvfdobr` which spawns drops below every spout marker. Drops fall, splitting when they hit shelves and possibly filling cups. After all drops have settled (either filled a cup or spilled), the win-animation flash runs; if any drops spilled, `zzocrmvox += 1`; if 4 spills → `lose()`.
- Specific challenge: with 1 shelf and 2 cups, the player must perform multiple pour attempts with the shelf in different positions to fill each cup. The shelf at (3, 4) starts left of the spout (col 9); the player must slide it under the spout column to direct drops into the cups. Approximate: 1st pour with shelf at column 5-9 → drop splits to (4, 4) and (10, 4) → (10, 4) drop falls through (10, 12), (10, 13) — cup-2's left edge — but the cup-fill check requires the drop to be at the mouth (col 11). So the player needs to set shelf to columns 7-11 → drop at col 9 splits to (8, 4) and (10, 4)... still neither is col 5 or col 11. Likely the player needs 2 pours: first pour to fill cup-1 (slide shelf so split lands at col 5), second to fill cup-2 (slide shelf so split lands at col 11).
- Estimated optimal action count: ~10-15 (slide ~3-4 cells + 1 pour, repeat for second cup).

### Level 2
- `grid_size`: (16, 16)
- Number of sprites placed: 10.
- Composition: 1 jgfvrvnkaz shelf at (6, 6), 2 untfxhpddv shelves at (6, 9) and (11, 11), 1 nkrtlkykwe at (5, 1), 1 syaipsfndp at (5, 0), 1 floor, 1 frame, 3 cups at (2, 13), (6, 13), (10, 13).
- Level data: `{"steps": 45, "rotation": 180}`.
- Spawn position(s): selected shelf = closest to origin = `jgfvrvnkaz` at (6, 6).
- Per-cell layout: 16x16. Spout at (5, 0). Shelves at (6, 6), (6, 9), (11, 11). 3 cups at (2-4, 13), (6-8, 13), (10-12, 13). Cup mouths at columns 3, 7, 11.
- Mechanic introduced relative to L1: **Multiple shelves** (3 instead of 1) and **rotation** of the rendered view. `level.data["rotation"] = 180` flips the entire frame upside-down on render via `hbwuwfezbg`, and the action-direction map (`wdxitozphu[2]`) remaps UP↔DOWN and LEFT↔RIGHT so the player's controls feel correct from the rotated viewpoint. Also more cups (3) and tighter step budget (45 vs L1's 30 — actually MORE in L2... wait L1 has 30, L2 has 45). 45 is more than 30 so the budget is looser.
- Specific challenge: with 3 cups and 3 shelves, the player must position shelves so a single pour attempt routes drops into all 3 cups (or fills them in 2-3 attempts within the 4-attempt budget). The 180° rotation adds a perceptual challenge — the player sees the world flipped.
- Estimated optimal action count: ~20-30.

### Level 3
- `grid_size`: (16, 16)
- Number of sprites placed: 15.
- Composition: 1 jgfvrvnkaz at (1, 8), 3 nkrtlkykwe drops at (1, 1), (14, 1), (6, 1), 2 odioorqnkn shelves at (8, 7) and (1, 5), 3 syaipsfndp markers at (1, 0), (14, 0), (6, 0), 1 trurgcakbj at (10, 10), 1 floor, 1 frame, 3 cups at (1, 13), (12, 13), (7, 13).
- Level data: `{"steps": 100, "rotation": 180}`.
- Spawn position(s): closest shelf = `odioorqnkn` at (1, 5) or similar.
- Per-cell layout: 16x16. 3 spouts (col 1, 6, 14). 4 shelves (lengths 6, 6, 5, 4). 3 cups at columns 1, 7, 12 (mouths at 2, 8, 13).
- Mechanic introduced relative to L2: **Multiple spouts** (3 instead of 1). Each pour attempt now spawns 3 drops simultaneously. Player must coordinate shelf positions to route ALL 3 drops to cups in fewer pour attempts. Continued 180° rotation. Larger step budget (100).
- Specific challenge: with 3 spouts and 3 cups arranged in different columns, ideally a single pour routes each drop to its own cup via shelf placement. Requires careful pre-pour shelf positioning.
- Estimated optimal action count: ~30-50.

Levels 4, 5, 6 exist but are excluded per skill scope.

## Action handlers

### ACTION1 / ACTION2 / ACTION3 / ACTION4 (UP / DOWN / LEFT / RIGHT)
- Trigger: `self.action.id in [GameAction.ACTION1, ACTION2, ACTION3, ACTION4]` after `lnqtlqefzv` remaps for rotation.
- Branches inside `step()`:
  - First call `lnqtlqefzv()` to get the (action_id, data) remapped for the current rotation. The remap uses `wdxitozphu[k]` where `k = rotation // 90 % 4`.
  - If `mlgebkvsmt == "change"` (idle/edit mode): decrement step counter via `rpnnowtzay(1)`. If `dpkgglmdup` is set (a shelf is selected), compute (worqgwkuyx, patlrtoom): UP→(0,-1), DOWN→(0,+1), LEFT→(-1,0), RIGHT→(+1,0). Compute new position; check `aqltiyljgy` (would the move violate boundaries — y < 3 forbidden, no overlap with cups allowed). If valid, attempt `try_move_sprite`; if collisions are all `ksmzdcblcz` or `hfjpeygkxy` tagged (other shelves), force `move(worqgwkuyx, patlrtoom)` anyway (shelves can pass through each other). Set `hypjnwsut = False`.
  - If `mlgebkvsmt == "spill"`: arrow-key actions are silently ignored during the spill animation.
- State mutations: read `self.dpkgglmdup`, `self.tunzhnhfa`, `self.action`. Written: `self.dpkgglmdup.position`, `self.tunzhnhfa`, possibly `self.hypjnwsut`, `self.awpmaspsfp`.
- Side effects on sprites: selected shelf `move()` if validated.
- Engine effects: `lose()` if step counter hits 0.
- Pre-conditions / gating: only effective when a shelf is selected; rejected if move would violate boundaries.

### ACTION5 (pour)
- Trigger: `self.action.id == GameAction.ACTION5`.
- Branches: only fires in `mlgebkvsmt == "change"` mode. If `zzocrmvox >= 4` (already 4 spills used), `lose()`. Otherwise call `tadqvfdobr()`:
  - Set `mlgebkvsmt = "spill"` to enter animation mode.
  - Deselect any selected shelf.
  - Initialise drop list `pksbqruoge` from all `nkrtlkykwe` already in the level (each tagged with motion (0, 1)).
  - Iterate every `syaipsfndp`-tagged sprite; for each palette-4 pixel in the sprite's bounding box, spawn a new `nkrtlkykwe` drop at the cell directly below.
  - Subsequent ticks (handled by the spill branch in `step()`) advance every drop by its (worqgwkuyx, patlrtoom). Collisions with shelves split drops; collisions with cups fill them; collisions with floor mark spilled.
- State mutations: `self.mlgebkvsmt`, `self.dpkgglmdup`, `self.pksbqruoge`, `self.shpilcvwbs`, `self.enlvswjeov`, `self.epilwznfbr`, `self.srwrqoodsc`, `self.szbmtoxgbd`.
- Side effects on sprites: many drops added; cups recoloured palette-13 on fill; drain cells recoloured palette-14 on spill.
- Engine effects: at end of animation, `next_level()` if all cups filled and no spill; `lose()` if step counter exhausted; otherwise reset to `mlgebkvsmt = "change"`.
- Pre-conditions / gating: rejected if `zzocrmvox >= 4`.

### ACTION6 (click — select shelf)
- Trigger: `self.action.id == GameAction.ACTION6`.
- Branches: only fires in `mlgebkvsmt == "change"` mode. Read (x, y) from `action.data` (already remapped for rotation by `lnqtlqefzv`); convert to grid via `camera.display_to_grid`. Iterate every `ksmzdcblcz` or `hfjpeygkxy`-tagged sprite; if click is within sprite bounding box, call `gchfqtwjap(sprite)` to select it (recolour to palette-9, `set_layer(1)`). Set `hypjnwsut = True` (gates `_get_valid_actions` to disallow clicks for the next action).
- State mutations: `self.dpkgglmdup`, `self.hypjnwsut`, the clicked sprite's pixels (recolour) and layer.
- Side effects on sprites: previously-selected shelf restored to original palette and layer; new shelf recoloured to palette-9.
- Engine effects: none.
- Pre-conditions / gating: silent no-op if click misses every shelf.

## HUD widgets

### `gxetqmbwgi` — top-row depleting step bar
- Class name (obfuscated): `gxetqmbwgi`.
- Render-pixel range: row 0 (top row), all 64 columns.
- What value it displays: `current_steps / pxfqncpydm` — proportion of step budget remaining (per-level via `level.get_data("steps")`: 30, 45, 100 for L1, L2, L3).
- Visual style: row 0 — palette-14 (yellow) for the leading `imathbgwdx = round(64 * remaining/total)` cells; palette-0 (black) for the rest. Yellow shrinks from the right edge.
- Update points: every tick via `rpnnowtzay(1)`; reset in `on_set_level` via `mmboppqpvb`.
- Where it is registered: `interfaces=[self.jvjkymhjfc, self.nmcpyttlk]` in `Camera`.

### `hbwuwfezbg` — frame rotator
- Class name (obfuscated): `hbwuwfezbg`.
- Render-pixel range: ALL pixels — applies a numpy `rot90` to the entire frame.
- What value it displays: rotation factor `_k` (0/1/2/3) read from `level.data["rotation"] // 90 % 4`.
- Visual style: rotates the frame 90/180/270 degrees if `_k != 0`. The action mapping in `lnqtlqefzv` and `_get_valid_actions` reciprocally remaps directional actions so the player's input feels correct from the rotated viewpoint.
- Update points: `set_rotation` is called in `on_set_level`.
- Where it is registered: same `interfaces=[]` list as the step-bar.

## Internal state — exhaustive

| attr (obfuscated) | semantic name | type | initial value | written by | read by | role |
|---|---|---|---|---|---|---|
| `mlgebkvsmt` | game_mode | str | "change" | `__init__`, `on_set_level`, `tadqvfdobr`, `yxidiymutj` | `step` | game state machine: "change" = edit mode (player moves shelves); "spill" = animation mode (drops fall) |
| `dpkgglmdup` | selected_shelf | `Sprite \| None` | None | `__init__`, `on_set_level`, `gchfqtwjap`, `dgtqqipvxj` | `step`, `gchfqtwjap`, `dgtqqipvxj`, `tadqvfdobr` | currently-selected shelf (or None) |
| `pksbqruoge` | active_drops | `list[tuple[Sprite, int, int]]` | `[]` | `__init__`, `on_set_level`, `tadqvfdobr`, `step` (spill) | `step` (spill) | (drop_sprite, dx, dy) tuples for every active falling drop |
| `shpilcvwbs` | spawned_drops | `list[Sprite]` | `[]` | `__init__`, `on_set_level`, `tadqvfdobr`, `step` (spill), `yxidiymutj` | `yxidiymutj` | drops added during a spill (cleaned up at end of animation) |
| `enlvswjeov` | spill_happened | bool | False | `__init__`, `on_set_level`, `tadqvfdobr`, `step` (spill) | `step` (spill) | True if any drop hit the drain during the current spill |
| `epilwznfbr` | spill_complete | bool | False | `__init__`, `on_set_level`, `tadqvfdobr`, `step` (spill) | `step` (spill) | True when all drops have either filled a cup or spilled |
| `srwrqoodsc` | filled_cups | `set[Sprite]` | `set()` | `__init__`, `on_set_level`, `tadqvfdobr`, `step` (spill), `yxidiymutj` | `step` (win check) | the set of cup sprites that have been filled |
| `szbmtoxgbd` | spilled_drain_cells | `set[Sprite]` | `set()` | `__init__`, `on_set_level`, `tadqvfdobr`, `step` (spill), `yxidiymutj` | `step` (animation flash) | drain sprites that spilled during this pour |
| `jmbhqnxkkc` | flash_tick | int | 0 | `__init__`, `step` | `step` | win-animation tick counter |
| `jvjkymhjfc` | step_counter_HUD | `gxetqmbwgi` | `gxetqmbwgi(0)` | `__init__`, `on_set_level`, `rpnnowtzay` | render | the top-row depleting bar |
| `awpmaspsfp` | shelf_just_selected | bool | False | `__init__`, `on_set_level`, `gchfqtwjap`, `step` | `step` | flag for "did we just select a shelf?" — gates valid actions |
| `hypjnwsut` | post_click_lock | bool | False | `__init__`, `on_set_level`, `step` | `_get_valid_actions` | True after a click; gates next action to non-click |
| `tunzhnhfa` | remaining_steps | int | 0 | `__init__`, `on_set_level`, `rpnnowtzay` | `step`, `rpnnowtzay` | step counter |
| `zzocrmvox` | spill_count | int | 0 | `__init__`, `on_set_level`, `yxidiymutj` | `step`, `tadqvfdobr` | number of pour attempts that ended with a spill; `lose()` at 4 |
| `sywpxxgfq` | rotation_quarter | int | 0 | `__init__`, `on_set_level` | `lnqtlqefzv`, `_get_valid_actions`, `udeubouzyp`, `fewyrfijcb` | rotation factor (0/1/2/3) for view rotation and action remap |
| `nmcpyttlk` | rotation_HUD | `hbwuwfezbg` | `hbwuwfezbg(0)` | `__init__`, `on_set_level` | render | rotates the entire frame |

## Win condition

Plain English: the level wins when every cup has been filled AND no drops spilled during the most recent pour attempt.

Literal condition: in the `step()` spill branch (lines 706-726), once `epilwznfbr` is True (all drops settled), check:
- `inszeuniyy = all(r in self.srwrqoodsc for r in dojowtxhlx)` — every cup is in the filled set.
- `if self.enlvswjeov or not inszeuniyy:` — if any drop spilled OR not all cups filled, run the failure-animation (flash drain palette-14/1 for 6 ticks; flash unfilled cups palette-0/11 for 5 ticks; then call `yxidiymutj` to clean up and increment spill counter).
- `else:` — both conditions met → `complete_action()` and `next_level()`.

Same predicate for L1, L2, L3.

## Lose condition

Plain English: lose if (a) step counter reaches 0 mid-action, or (b) the player has used up all 4 pour attempts (spill counter ≥ 4) and presses pour again.

Literal condition: 
- Step exhaustion (`rpnnowtzay` line 843-846): `if self.tunzhnhfa <= 0: self.lose()`. Also at line 720: `if self.tunzhnhfa <= 0: self.lose()` after a failed-attempt animation.
- Pour attempt exhaustion (line 695-697): `if self.zzocrmvox >= 4: self.lose()` BEFORE starting `tadqvfdobr`.

## Resource economy

- Depleting resource (energy / step counter / lives): YES — `tunzhnhfa` step counter (initial per-level 30/45/100/120/100/120). Decremented by 1 per action. Threshold 0 triggers `lose()`.
- Accumulating resource: YES — filled-cup count (`len(srwrqoodsc)`); progress is binary per cup.
- Lives mechanic: YES (sort of) — 4 pour attempts (`zzocrmvox`) act as lives. Each failed attempt (cup not filled or spill) increments the counter; 4 failures = lose.
- Resource interaction: step counter and pour-attempt counter are both lose triggers; cup-fill count is the win trigger. All three independent.

## Action-budget signature

- Default budget per level: per-level via `level.get_data("steps")`. L1=30, L2=45, L3=100.
- Whether budget tightens or shifts across levels 1-3: NO consistent direction — L1 (30) → L2 (45) → L3 (100). Generally loosening.
- Per-level vs. per-environment: per-level (reset in `on_set_level`).
- Decrement rate per action: 1 per action (UP/DOWN/LEFT/RIGHT/click/pour all cost 1).
- Refill mechanism: NONE.

## Notable code patterns / techniques

- **Two-mode state machine** (`mlgebkvsmt`): "change" mode for player editing, "spill" mode for falling-drop animation. Clean separation between input handling and animation.
- **Drop-collision branches** (lines 727-794): a dict-style enumeration over the cell-in-front sprite's tag — each tag handled by a different code path: empty (continue falling), drop (merge), shelf (split), cup (try fill, else split), corner (deflect), drain (spill).
- **Rotation-aware action remap** (`wdxitozphu`, `qxlcnqsvsf`, `lnqtlqefzv`): the entire game can be rendered at 0/90/180/270 rotation, and player input is remapped so directional actions feel intuitive from the rotated viewpoint. `_get_valid_actions` also remaps so the action-chooser sees correct directions.
- **Per-level rotation via `level.data["rotation"]`**: a single integer flag drives both the view rotation and the action remap.
- **Spawn at palette-4 pixels** (`tadqvfdobr` lines 618-631): drops are spawned by scanning every `syaipsfndp`-tagged sprite for palette-4 cells; this lets shelves with internal spout markers (e.g. `adbrqflmwi`) act as spouts without needing a separate sprite.
- **Selection highlighting via `pixels` mutation** (`gchfqtwjap`, `dgtqqipvxj`): on select, replace all non-special pixels with palette-9; on deselect, replace with the original palette (8 for `ksmzdcblcz` shelves, 15 for `hfjpeygkxy` corners).
- **`try_move_sprite` with collision relaxation** (line 687-689): moves a shelf even if it collides with other shelves; only respects boundary collisions.
- **`_get_valid_actions` returns rotation-remapped actions**: ensures the LLM sees actions in the player's reference frame, not the engine's.

## Anti-patterns / lessons

- **Five dead/never-placed sprites** (`mdhkebfsmg`, `nadtnzkesz`, `nvzozwqarf`, `qwsmjdrvqj`, `vkwijvqdla`, `ttkatugvbk`, `uihgaxtzkm`, `zgsbadjnjn`, `adbrqflmwi` in L1-3) — many sprite definitions for L4+ features. A 3-level generated game should ship only what's used.
- **Two flag attributes for similar concepts** (`hypjnwsut` and `awpmaspsfp`) — both gate "post-click" valid actions but do slightly different things. Consolidate.
- **180° view rotation and action remap** at L2-3 — adds cognitive load; arguably extraneous to the core mechanic. Generated 3-level games should not introduce view rotation as a sub-mechanic.
- **Silent action consumption** during spill animation — actions submitted while drops are falling are ignored but still consume the step counter. Could be confusing.
- **Spill counter resets only on level-change** — a partial fill isn't preserved across pour attempts. Players who fill cup-1 in attempt 1 and cup-2 in attempt 2 must complete BOTH cups in a SINGLE attempt to win (since `srwrqoodsc` is reset at the start of each `tadqvfdobr`).

  Actually re-reading `tadqvfdobr` line 616-617: `self.srwrqoodsc = set()`, `self.szbmtoxgbd = set()`. So yes, EVERY pour resets the filled-cups set. The player must fill ALL cups in a SINGLE pour to win. This is harder than I thought.

  This is a major mechanic constraint — the player has 4 attempts but each attempt must independently fill ALL cups. Alternatively, an attempt that only partially fills cups is treated as a spill+restart — `srwrqoodsc` resets next time. So the puzzle is more like "find the configuration that fills all cups in one go".

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES (top row, depleting bar).
- Has lives mechanic: YES (4 pour attempts).
- Has click-to-select (uses ACTION6): YES.
- Has tag-based grouping (uses `level.get_sprites_by_tag`): YES (`ksmzdcblcz`, `hfjpeygkxy`, `nkrtlkykwe`, `xsrqllccpx`, `uzunfxpwmd`, `syaipsfndp`).
- Uses ACTION5 (modal): YES (pour).
- Uses ACTION6 (click): YES.
- Uses ACTION7: NO.
- Has level data dicts (uses `level.get_data` / `level.set_data`): YES (`level.get_data("steps")`, `level.get_data("rotation")`).
- Multi-mechanic per level: NO — same shelf-arrange + pour mechanic across L1-3; L2 adds rotation; L3 adds multiple spouts.
- Tutorial level appears solvable by random play: NO. Random shelf-position + random pour has near-zero chance of routing all drops to all cups in a single attempt.
- Has a depleting resource: YES — step counter + pour attempts.
- Has an accumulating resource: YES (within a single pour) — filled-cup set.
- Sprite shape convention used: mixed — horizontal bars (shelves), single-cell (drops, spouts), U-shape (cups), hollow rectangles (frame, drain).
- HUD position: top.
- Palette size used: 7 distinct palette values appear in placed L1-3 sprites: {1, 4, 6, 8, 11} from sprites + {9, 13, 14} from runtime recolours. Total = 8.
- Background colour value: 12 (`BACKGROUND_COLOR = 12`).
- Padding / letter-box colour value: 1 (`PADDING_COLOR = 1`).
- Number of distinct mechanics introduced across levels 1-3: 1 (water-pouring); L2 adds view rotation, L3 adds multiple spouts — both extensions of the base mechanic.
- Number of levels documented: 3.

(End of file.)
