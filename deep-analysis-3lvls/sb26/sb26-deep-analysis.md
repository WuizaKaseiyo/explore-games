# sb26 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/sb26/7fbdac44/sb26.py`
- Lines: 1152
- Class name: `Sb26`
- available_actions: `[5, 6, 7]` (ACTION5 = commit/play, ACTION6 = click, ACTION7 = undo)
- Number of levels in source: 8
- Number of levels documented in this analysis: 3
- Imports: `NovaBaseGame`, `Camera`, `GameAction`, `Level`, `RenderableUserDisplay`, `Sprite` from `novaengine`; `ActionInput` from `novaengine.enums`; `numpy as np`; `math`.

## Mechanic essence (one sentence)

A row of coloured square tiles sits in a tray at the bottom, a row of target-colour boxes hangs at the top, and one or more numbered frames stretch between them — the player clicks a tray tile and clicks a frame-slot to drop it in (or clicks two tray tiles to swap them), then presses commit to send a marker walking left-to-right across the top boxes that ticks each one off only if the colour sat in the corresponding frame-slot matches; the level is solved when every target is ticked.

## Sprite roster

| sprite (obfuscated) | dims | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| `jkxncpvknr` | 8x8 | 0, -1 | (default) | 1 | YES | (default) | YES | hollow black frame — moving cursor that walks across the top targets during commit |
| `jvkvqzheok1` | 10x10 | 8, -2 | pkpgflvjel | (default) | YES | (default) | YES | size-1 frame slot (level 6+) |
| `jvkvqzheok2` | 16x10 | 8, -2 | pkpgflvjel | (default) | YES | (default) | YES | size-2 frame (L3) |
| `jwaufhyryn` | 43x14 | 8, -1 | (default) | 12 | YES | (default) | YES | giant L-shaped overlay frame (level 8) |
| `lngftsryyw` | 6x6 | 8, -2 | lngftsryyw, sys_click | 1 | YES | (default) | YES | coloured tray tile — palette-8 outer ring with recoloured interior; the puzzle's draggable pieces |
| `lnzhvcagos` | 48x12 | 0, -1 | (default) | 10 | YES | (default) | YES | wide expanding overlay rectangle drawn behind the cursor during commit-animation |
| `nyqgqtujsa5` | 34x10 | 8, -2 | pkpgflvjel | (default) | YES | (default) | YES | size-5 frame (L3, L4, L5) |
| `oflgslmuku` | 64x8 | 8, -1 | (default) | 12 | YES | (default) | YES | giant horizontal frame overlay (level 7+) |
| `pcrvmjfjzg3` | 22x10 | 8, -2 | pkpgflvjel | (default) | YES | (default) | YES | size-3 frame (L4+) |
| `pqezjimbse` | 2x8 | 14 | (default) | 1 | NO | (default) | YES | small green divider tile (L2) |
| `qdmvvkvhaz4` | 28x10 | 8, -2 | pkpgflvjel | (default) | YES | (default) | YES | size-4 frame (L1, L2, L8) |
| `quhhhthrri` | 6x6 | 8, -1 | (default) | 1 | YES | (default) | YES | top-row target colour-box — palette-8 outer ring with recoloured interior; the puzzle's "answer key" |
| `susublrply` | 6x6 | 2, -2 | susublrply, sys_click | (default) | YES | (default) | YES | empty frame-slot — palette-2 centre dot indicating "tile can go here" |
| `upbhqnvnyx` | 6x6 | 3, -1 | (default) | (default) | YES | (default) | YES | hollow grey frame — used as a "fill marker" overlay when a vgszefyyyp expansion is collected |
| `uzxwqmkrmk` | 8x8 | 5 | (default) | (default) | YES | (default) | YES | grey shelf/divider rectangle at the top of the playfield |
| `vgszefyyyp` | 6x6 | 8, -2 | lngftsryyw, sys_click | 1 | YES | (default) | YES | "expansion" tile — palette-8 outer + inner rings; clicking adds a fillmarker to the chain |
| `wbkmnqvtxh6` | 34x9 | 8, -2 | pkpgflvjel | (default) | YES | (default) | YES | size-6 frame (level 7+) |
| `wrqpmmfhup` | 6x6 | (any) | (default) | (default) | YES | (default) | YES | tile-cursor overlay — recoloured at runtime to highlight the tile under the cursor |
| `zpwrpmkvsv` | 64x1 | (any) | (default) | (default) | YES | (default) | YES | placeholder line at y=53 — placed at level start, removed in `on_set_level` |
| `zzssdzqbbr7` | 49x10 | 8, -2 | pkpgflvjel | (default) | YES | (default) | YES | size-7 frame (level 8+) |

### `jkxncpvknr` — moving cursor frame
- Pixel pattern: 8x8 hollow palette-0 ring with -1 transparent interior.
- Where it appears: spawned at level start (`mjeqtdqvm = sprites["lnzhvcagos"].clone()` ... actually wait, this is the `lnzhvcagos`. Re-reading: `mjeqtdqvm` is `lnzhvcagos` — the wide overlay. `jkxncpvknr` is referenced via `self.ohvavdnio = sprites["jkxncpvknr"].clone().color_remap(None, llttrdekba).set_layer(10)`).
- Role: the moving cursor that walks across the top-row targets during the commit-animation. Recoloured to palette `llttrdekba` (a constant) at level start.
- Visual-vs-functional read: hollow black frame; tracks animation progress.

### `jvkvqzheok1` — size-1 frame slot (level 6+)
- Pixel pattern: 10x10 hollow palette-8.
- Where it appears: not placed in L1-3.
- Role: out of scope (level 6+ frame).

### `jvkvqzheok2` — size-2 frame (L3)
- Pixel pattern: 16x10 hollow palette-8 with `-2` interior. Width 16 = 2 slots × 7 cells + 2 ring cells.
- Where it appears: L3 (2 copies at (15, 31) and (33, 31), recoloured to palette-14 and palette-9 respectively).
- Role: holds 2 tray tiles in a row; each "size-N" frame's name encodes its slot count via the trailing digit (`int(frame.name[-1])`).
- Visual-vs-functional read: hollow rectangle; tag `pkpgflvjel`. The numerical suffix in the name (e.g. `2`, `3`, `4`, `5`) is parsed at runtime to determine slot count.

### `jwaufhyryn` — giant L-shaped overlay (L8)
- Pixel pattern: 43x14 with palette-8 forming an L-shape.
- Where it appears: not placed in L1-3.
- Role: out of scope.

### `lngftsryyw` — coloured tray tile
- Pixel pattern: 6x6, `[[-2, -2, -2, -2, -2, -2], [-2, 8, 8, 8, 8, -2], [-2, 8, 8, 8, 8, -2], [-2, 8, 8, 8, 8, -2], [-2, 8, 8, 8, 8, -2], [-2, -2, -2, -2, -2, -2]]`. 4x4 inner block of palette-8 surrounded by transparent border, recoloured per placement.
- Where it appears: every L1-3 level — many copies in the bottom tray (y=56) and some in mid-field. Recoloured per placement to one of palettes 6, 8, 9, 11, 12, 14, 15.
- Role: draggable coloured tile. The player clicks one to "pick up" (raises the tile-cursor `wrqpmmfhup` overlay), then clicks a frame-slot (`susublrply`-tagged) to drop it in.
- Visual-vs-functional read: at-rendered-scale, a 6x6 filled square with palette-X center colour (the colour determines its identity). Tag `lngftsryyw + sys_click` makes it clickable.
- Visual contrast notes: each tile's centre colour is its identity; outer ring is always palette-8 (shared with all tiles).

### `lnzhvcagos` — wide expanding overlay
- Pixel pattern: 48x12 with palette-0 corner brackets and -1 transparent middle.
- Where it appears: every L1-3 level (1 copy added at level start as `self.mjeqtdqvm`).
- Role: an overlay that "stretches" between the source frame-slot and the target box during commit-animation. The `dagvovvbpp` and `fkyoqwmrzb` helpers grow/shrink its width to span between two coordinates.
- Visual-vs-functional read: hollow black bracket-rectangle that visually traces the connection.

### `nyqgqtujsa5` — size-5 frame (L3+)
- Pixel pattern: 34x10 hollow palette-8 with -2 interior. Width 34 = 5 slots × 6 cells + 4 dividers.
- Where it appears: L3 (1 at (15, 19)).

### `oflgslmuku` — giant 64x8 frame (level 7+)
- Where it appears: not placed in L1-3.

### `pcrvmjfjzg3` — size-3 frame (L4+)
- Pixel pattern: 22x10 hollow palette-8.
- Where it appears: not placed in L1-3.

### `pqezjimbse` — small green divider (L2)
- Pixel pattern: 2x8 solid palette-14.
- Where it appears: L2 (1 copy at (34, 24)).
- Role: cosmetic divider.

### `qdmvvkvhaz4` — size-4 frame (L1, L2, L8)
- Pixel pattern: 28x10 hollow palette-8.
- Where it appears: L1 (1 at (18, 25)), L2 (2 copies at (18, 18) and (18, 32) recoloured palette-14).

### `quhhhthrri` — top-row target colour-box
- Pixel pattern: 6x6 hollow palette-8 ring with -1 interior; recoloured per placement.
- Where it appears: every L1-3 level — 4 copies in L1, 7 in L2, 7 in L3 — placed in a row at y=1 (the top of the play area).
- Role: target colour-box. During commit-animation, the cursor walks across these boxes one by one; each box becomes "ticked" if the corresponding frame-slot's tile colour matches the box's colour.
- Visual-vs-functional read: at-rendered-scale, a 6x6 hollow square with a coloured interior. Distinct from `lngftsryyw` by being hollow (lngftsryyw is filled). Player tells them apart by fill state.
- Visual contrast notes: coloured against black-bordered top.

### `susublrply` — empty frame-slot
- Pixel pattern: 6x6 with -2 transparent border and 2x2 palette-2 centre dot.
- Where it appears: every L1-3 level — multiple copies inside the frames.
- Role: an empty slot indicator. Tag `susublrply + sys_click`. When the player clicks a frame-slot, the held tile is placed there (and the slot's `set_visible(False)`); the tile takes the slot's position.
- Visual-vs-functional read: at-rendered-scale, a small palette-2 dot centred in a transparent area. Reads as a "drop target" or "empty slot".

### `upbhqnvnyx` — fill-marker overlay
- Pixel pattern: 6x6 hollow palette-3.
- Where it appears: spawned at runtime when a `vgszefyyyp` expansion is collected — added to `jyuoktbrc` list.
- Role: visual indicator that a fill-marker has been chained.

### `uzxwqmkrmk` — top-row grey shelf
- Pixel pattern: 8x8 solid palette-5.
- Where it appears: every L1-3 level — multiple copies along the top y=0 row.
- Role: cosmetic shelf above the target colour-boxes; the cursor passes over them during commit.

### `vgszefyyyp` — expansion tile
- Pixel pattern: 6x6 with palette-8 double-ring (outer + inner). Recoloured per placement.
- Where it appears: L2 (1 at (32, 20) recoloured palette-14), L3 (2 at (23, 21), (35, 21) recoloured palette-14 and palette-9).
- Role: a tile that, when clicked into a frame-slot, branches the chain — adds a `upbhqnvnyx` fill-marker and pushes a new sub-frame onto the placement stack (`buvfjfmpp`). Allows recursive sub-puzzles.

### `wbkmnqvtxh6` — size-6 frame (level 7+)
- Where it appears: not placed in L1-3.

### `wrqpmmfhup` — tile-cursor overlay
- Pixel pattern: 6x6 (recoloured at runtime).
- Where it appears: 2 copies spawned at level start as `self.mrokwhyjs`.
- Role: tile-cursor — when the player picks up a tile, this overlay is recoloured to the picked tile's colour and positioned at the picked tile's location to show selection.

### `zpwrpmkvsv` — placeholder line (removed at level start)
- Pixel pattern: 64x1.
- Where it appears: every L1-3 level (1 copy at (0, 53)) — but `on_set_level` removes it immediately.
- Role: placeholder; only present at design time.

### `zzssdzqbbr7` — size-7 frame (level 8+)
- Where it appears: not placed in L1-3.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (64, 64)
- Number of sprites placed: 18 (4 lngftsryyw tray tiles, 1 qdmvvkvhaz4 size-4 frame, 4 quhhhthrri targets, 4 susublrply slots, 4 uzxwqmkrmk shelves, 1 zpwrpmkvsv placeholder).
- Composition: 4 colours: 14, 15, 9, 11. Tray tiles at y=56 (cols 17, 25, 33, 41 — palettes 14, 15, 9, 11). Target boxes at y=1 (cols 18, 25, 32, 39 — palettes 9, 14, 11, 15). One size-4 frame at (18, 25) holding 4 slots at y=27.
- Level data: `{}` (no level data — uses defaults).
- Spawn position(s): no avatar; the cursor is initially placed at the size-4 frame's first slot.
- Per-cell layout: 64x64. Top row (y=0..6) has 4 grey shelves and 4 coloured target boxes; middle (y=25..35) has the size-4 frame with 4 empty slots; bottom (y=56) has 4 tray tiles.
- Mechanic introduced relative to the previous level: this is the first level — introduces the **tile-into-slot + commit** mechanic. The player has 64 step budget. Click ACTION6 on a tray tile to pick it up; click ACTION6 on an empty slot (`susublrply`-tagged) to drop it in (slot disappears; tile takes its position). Click ACTION5 to commit — runs an animation where the cursor walks from slot 0 to slot N-1, comparing each slot's tile colour to the corresponding target box's colour; if they match, the target box is ticked; if all match, win. Click ACTION7 to undo.
- Specific challenge: 4 tray tiles with colours 14, 15, 9, 11 must be placed in 4 slots so each slot's tile matches the corresponding target colour (target order: 9, 14, 11, 15). The player must figure out the correct permutation (4! = 24 possibilities) by reading the colours.
- Estimated optimal action count: 4 picks + 4 drops + 1 commit = 9 actions. Comfortable within 64 budget.

### Level 2
- `grid_size`: (64, 64)
- Number of sprites placed: 33 (7 tray tiles, 1 divider, 2 size-4 frames, 7 targets, 7 slots, 7 shelves, 1 expansion, 1 placeholder).
- Composition: 7 colours (8, 15, 14, 12, 6, 9, 11). Two size-4 frames stacked vertically at (18, 18) and (18, 32). One expansion (`vgszefyyyp` at (32, 20) recoloured palette-14).
- Level data: `{}`.
- Per-cell layout: 64x64. 7 target boxes at y=1, 7 tray tiles at y=56. Two frames split the middle.
- Mechanic introduced relative to L1: **Multiple frames** (2 size-4 frames stacked) and **expansion tile** (vgszefyyyp). The expansion tile, when placed, adds a fill-marker `upbhqnvnyx` and pushes a new sub-frame onto the placement stack — so committing recursively expands one frame's slot into another sub-frame's chain.
- Specific challenge: 7 tiles to place across 2 frames (8 slots total), with the expansion tile creating a branching path. The player must figure out the recursive ordering.
- Estimated optimal action count: 7 picks + 7 drops + 1 commit = 15 actions.

### Level 3
- `grid_size`: (64, 64)
- Number of sprites placed: 34.
- Composition: 7 tiles, 2 size-2 frames (`jvkvqzheok2`), 1 size-5 frame (`nyqgqtujsa5`), 7 targets, 7 slots, 7 shelves, 2 expansions.
- Level data: `{}`.
- Mechanic introduced relative to L2: **Mixed frame sizes** (2x2 frames + 1x5 frame) and **multiple expansions** (2). More complex placement graph.
- Specific challenge: figure out which tiles go in which size-2 vs size-5 vs expansion-triggered slots.
- Estimated optimal action count: ~15-20.

Levels 4, 5, 6, 7, 8 exist but are excluded per skill scope.

## Action handlers

### ACTION5 (commit / play)
- Trigger: `self.action.id == GameAction.ACTION5`.
- Branches: animation guard (if any animation tick variable >= 0, skip). Otherwise decrement `sjcuorclg` (step counter). Hide cursor sprites; capture entire current frame into `lvctpsmff.pixels`; restore cursor sprites. Call `rfdjlhefnd` to set up the commit-animation: build `rzbeqaiky[frame]` mapping (each frame to its placed tiles), set `buvfjfmpp = [(frame_0, 0)]` (placement-stack starts at frame 0), position cursor at frame 0's first slot, set `modqnpqfi = 15` (animation tick countdown).
- Subsequent ticks (driven by `dbfxrigdqx`) walk the cursor through the frames: for each slot, compare slot tile colour to the corresponding target box colour. Match → tick (animate target box recolour). All match → `next_level()`. First mismatch → animation flash (`sibihgzarf`).
- State mutations: `sjcuorclg`, `rzbeqaiky`, `buvfjfmpp`, every overlay sprite's position and colour, animation tick counters.
- Engine effects: `next_level()` on full match; `lose()` if step counter hits 0.

### ACTION6 (click)
- Trigger: `self.action.id == GameAction.ACTION6`.
- Branches: read (x, y) from `action.data`. Find the `sys_click`-tagged sprite at that grid position. Call `hjewbkcejq(sprite)`:
  - If no tile is currently picked up:
    - If sprite is a tray tile (`lngftsryyw`-tagged), pick it up (set `lqcskynzr = sprite`, recolour cursor `mrokwhyjs[0]` to tile's colour and move to tile's position).
  - If a tile IS picked up:
    - Click on same tile → drop (`lqcskynzr = None`, hide cursor).
    - Click on different tray tile → swap their positions; decrement step counter.
    - Click on empty slot (`susublrply`-tagged) → place the picked tile at slot's position; hide the slot; decrement step counter.
- Snapshot state via `rhhcxovxow` for undo.
- State mutations: `lqcskynzr`, every clicked sprite's visibility/position, `mrokwhyjs[0]` cursor, `sjcuorclg`, `uvawsoycr` undo stack.

### ACTION7 (undo)
- Trigger: `self.action.id == GameAction.ACTION7`.
- Branches: dispatch to `kxrrueustb()` which pops the most recent snapshot from `uvawsoycr`. Restores positions and visibility of all `dkouqqads` (lngftsryyw) and `dewwplfix` (susublrply) sprites.
- State mutations: snapshot pop and full restore.
- Engine effects: none.

## HUD widgets

### `khmhhfucux` — depleting step bar at y=evrmzyfopo (a constant ~53)
- Render-pixel range: row 53 (the y-divider line).
- What value it displays: `sjcuorclg / incrguxqwfjtial_energy` (initial 64).
- Visual style: row 53 — palette `horxeupwra` for remaining cells, palette `orbfpczobx` for depleted.
- Update points: every render.

## Internal state — exhaustive

| attr (obfuscated) | semantic name | type | initial value | written by | read by | role |
|---|---|---|---|---|---|---|
| `incrguxqwfjtial_energy` | max_steps | int | 64 | `on_set_level` | render | denominator |
| `sjcuorclg` | remaining_steps | int | 64 | `on_set_level`, `step` | `step`, render | step counter |
| `qaagahahj` | frames_sorted | `list[Sprite]` | (all `pkpgflvjel`-tagged) | `on_set_level` | many | the placement frames in (y, x) order |
| `rzbeqaiky` | frame_to_placed_tiles | `dict[Sprite, list[Sprite]]` | `{}` | `rfdjlhefnd` | `dbfxrigdqx`, `step` | each frame's placed tile sequence |
| `wcfyiodrx` | targets | `list[Sprite]` | (all `quhhhthrri` sprites) | `on_set_level` | `step` (commit anim) | top-row target boxes |
| `dkouqqads` | tray_tiles | `list[Sprite]` | (all `lngftsryyw`-tagged) | `on_set_level` | many | the colour tiles |
| `dewwplfix` | slots | `list[Sprite]` | (all `susublrply`-tagged) | `on_set_level` | `vjvsrcbftu`, undo | the empty frame-slots |
| `lqcskynzr` | picked_up_tile | `Sprite \| None` | None | `step`, `hjewbkcejq` | `_get_valid_actions`, `step` | currently-held tile |
| `mrokwhyjs` | cursor_sprites | `list[Sprite]` (length 2) | spawned in `on_set_level` | `step`, `hjewbkcejq` | render | tile-pickup cursor overlays |
| `mjeqtdqvm` | wide_overlay | `Sprite` (lnzhvcagos clone) | spawned | `step`, `dagvovvbpp` | render | the moving "stretch" overlay |
| `ayaigjtxp` | placement_overlay | `Sprite` (wrqpmmfhup clone) | spawned | `step` | render | overlay that traces from source slot to target box |
| `ohvavdnio` | cursor_overlay | `Sprite` (jkxncpvknr clone) | spawned | `step` | render | the moving frame cursor |
| `buvfjfmpp` | placement_stack | `list[tuple[Sprite, int]]` | `[]` | `rfdjlhefnd`, `dbfxrigdqx` | `step` | LIFO stack of (frame, slot_index) for recursive expansion |
| `jyuoktbrc` | fill_markers | `list[Sprite]` | `[]` | `dbfxrigdqx` | `step` | `upbhqnvnyx` overlays added per expansion |
| Animation ticks | various | int | -1 | `step` | `step` | various sub-step counters: `xjxrqgaqw`, `bbiavyren`, `lmvwmlqtw`, `ftyhvmeft`, `japgbruyb`, `artsfnufc`, `jlcrtmkes`, `modqnpqfi`. Each runs a multi-tick animation phase. |
| `uvawsoycr` | undo_stack | `list[list[tuple[Sprite, int, int, bool]]]` | `[]` | `rhhcxovxow`, `kxrrueustb` | `kxrrueustb` | snapshot stack |

## Win condition

Plain English: the level wins when every top-row target box has its colour matched by the tile placed in the corresponding sequential slot during commit.

Literal condition: in `dbfxrigdqx`, when the cursor reaches `pmygakdvy == len(wcfyiodrx) - 1` AND `wrudcanmwy` is True (the current slot's tile centre colour is non-empty AND matches the target), set `lmvwmlqtw = 0` to start the win-flash animation; at tick 16, call `next_level()`.

Same predicate for L1, L2, L3.

## Lose condition

Plain English: lose if step counter hits 0.

Literal condition: at line 814-815 (after a failed-commit animation completes) and line 864-865 (after a swap animation), check `if self.sjcuorclg == 0: self.lose()`.

## Resource economy

- Depleting resource: YES — `sjcuorclg` step counter (initial 64). Decremented by 1 per ACTION5 (commit), per swap, per tile-placement.
- Accumulating resource: YES — placed-tile count toward win predicate (implicit).
- Lives mechanic: NO.
- Resource interaction: step counter is sole lose trigger; full-match commit is sole win trigger.

## Action-budget signature

- Default budget per level: 64 (hardcoded `incrguxqwfjtial_energy = 64`).
- Whether budget tightens or shifts across levels 1-3: NO — same 64 each level.
- Per-level vs. per-environment: per-level (reset in `on_set_level`).
- Decrement rate per action: 1 per ACTION5, per swap, per tile-into-slot drop. Click on a tray tile (pickup) does NOT decrement.
- Refill mechanism: NONE.

## Notable code patterns / techniques

- **Frame size encoded in name suffix** (`int(frame.name[-1])`): clean way to tag capacity without an extra attribute.
- **Recursive placement-stack** (`buvfjfmpp`): supports nested frames via a LIFO of (frame, slot) tuples.
- **Snapshot-based undo** (`rhhcxovxow` / `kxrrueustb`): captures all draggable sprite states for ACTION7 reversal.
- **Multi-phase animation tick counters**: ~8 separate animation states each with their own tick variable, gated at the top of `step()`.
- **`color_remap(None, palette)` for runtime recolouring** of tile interiors: lets a single sprite template represent any colour.
- **`_get_valid_actions` returns explicit click coordinates** for each clickable sprite: helps an LLM agent pick valid actions.

## Anti-patterns / lessons

- **8 different size-N frame sprites** (`jvkvqzheok1/2`, `pcrvmjfjzg3`, `qdmvvkvhaz4`, `nyqgqtujsa5`, `wbkmnqvtxh6`, `zzssdzqbbr7`) — same template, different sizes. Could be parameterised.
- **Heavy animation state machine** with 8 mutually-exclusive tick variables — error-prone. Single state-machine enum would be cleaner.
- **`zpwrpmkvsv` placed and immediately removed** — placeholder pollution.
- **Many overlay sprites** (jkxncpvknr, lnzhvcagos, wrqpmmfhup, oflgslmuku, jwaufhyryn, ayaigjtxp, ohvavdnio, mrokwhyjs[0/1], lvctpsmff) — heavy per-frame rendering.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES (row 53).
- Has lives mechanic: NO.
- Has click-to-select (uses ACTION6): YES.
- Has tag-based grouping: YES (`pkpgflvjel`, `lngftsryyw`, `susublrply`, `sys_click`).
- Uses ACTION5 (modal): YES (commit).
- Uses ACTION6 (click): YES.
- Uses ACTION7: YES (undo).
- Has level data dicts: NO (level.data is empty).
- Multi-mechanic per level: NO — same place-tiles-then-commit mechanic across L1-3; expansions added in L2.
- Tutorial level appears solvable by random play: NO (4 tiles × 4 slots = 24 permutations; random has low chance within 64 steps).
- Has a depleting resource: YES — step counter.
- Has an accumulating resource: YES — placed-tile count.
- Sprite shape convention used: mixed — filled small squares (tiles), hollow rings (frames, targets, cursors), thin grey shelves.
- HUD position: middle (row 53).
- Palette size used: 9 distinct palette values: {0, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15} = 11.
- Background colour value: 4 (`BACKGROUND_COLOR = 4`).
- Padding / letter-box colour value: 3 (`PADDING_COLOR = 3`).
- Number of distinct mechanics introduced across levels 1-3: 2 (place-and-commit in L1, expansion-recursion in L2; L3 just adds frame variety).
- Number of levels documented: 3.

(End of file.)
