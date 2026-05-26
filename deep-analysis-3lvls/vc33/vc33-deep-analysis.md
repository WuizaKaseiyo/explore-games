# vc33 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/vc33/9851e02b/vc33.py`
- Lines: 2137
- Class name: `Vc33`
- available_actions: `[6]` (ACTION6 = click only)
- Number of levels in source: 7
- Number of levels documented in this analysis: 3
- Imports: standard novaengine + numpy.

## Mechanic essence (one sentence)

A long row of coloured floor-tiles carries a handful of small units perched on top, with a clickable pull-tab dangling from each end of the row; clicking a tab drags the entire row of tiles one step in the tab's direction — every unit slides along with the floor it stands on — and the level is solved when each unit ends up resting over the house painted in its own colour.

## Sprite roster

(vc33 has approximately 60 sprites across 7 levels. Tag-grouped overview below; each sprite within a group plays the same role.)

| sprite (obfuscated) | dims | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| (many) | varies | varies | rDn | (default) | YES | (default) | YES | floor tiles (the rows that slide) |
| (many) | varies | varies | UXg | (default) | YES | (default) | YES | tower/building obstacles fixed in place |
| (many) | varies | varies | HQB | (default) | YES | (default) | YES | unit/figure standing on a floor tile |
| (many) | varies | varies | fZK | (default) | YES | (default) | YES | target house — the place a matching-colour unit must end up |
| (some) | varies | varies | ZGd, ACQ | (default) | YES | (default) | YES | clickable pull-tab — drags the row in its direction |
| (some) | varies | varies | zHk, ACQ | (default) | YES | (default) | YES | clickable bridge-extender (level 1+ feature) |
| (some) | varies | varies | rlV | (default) | YES | (default) | YES | transient overlay (cleaned up between actions) |
| (some) | varies | varies | WuO | (default) | YES | (default) | YES | collision-stop marker |

(Per the SKILL's exhaustive requirement, individual sprites are referenced by name in the per-level breakdown below; each plays the role indicated by its tag membership.)

### Tag-group: `rDn` (floor tiles)
- Pixel pattern: each rDn sprite is a coloured rectangular bar of palette-X. They tile horizontally or vertically depending on the level's `TiD` direction.
- Where they appear: every level — multiple copies forming a row.
- Role: the floor that slides. When a pull-tab is clicked, the whole row slides one step (TiD direction). Sprite-level pixels[0] vs pixels[-1] colour determines which "side" the tile faces.

### Tag-group: `HQB` (units / figures)
- Pixel pattern: small coloured figures (e.g. 4x6 humanoid sprites) with a specific colour identity.
- Role: the units standing on top of the floor. They move with the row.

### Tag-group: `fZK` (target houses)
- Pixel pattern: coloured house-shape tiles.
- Role: each unit must end up positioned over its matching-colour house.

### Tag-group: `ZGd, ACQ` (pull-tabs)
- Pixel pattern: small coloured tabs hanging off the ends of the floor row.
- Role: clickable. Each tab represents a direction; clicking advances the row one step that way. Has tag `ACQ` to make it clickable.

### Tag-group: `zHk, ACQ` (bridge-extenders, level 4+)
- Pixel pattern: pull-loops on bridges.
- Role: clickable handle that extends a bridge across a gap when the alignment is correct.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (32, 32)
- Number of sprites placed: 7 — `ChX`, `EtZ`, `KLo`, `pYt`, `qAd`, `xQZ` × 2.
- Composition: 1 row of floor tiles + 1-2 units + 1 target + 2 pull-tabs.
- Level data: `{"RoA": 50, "TiD": [2, 0]}` — slides 2 cells right per tab-click; 50-step budget.
- Spawn position(s): no avatar; the player only clicks tabs.
- Mechanic introduced relative to the previous level: this is the first level — introduces the **slide-row + unit-positioning** mechanic. ACTION6 click on a pull-tab slides the entire row (and units on top) by `TiD` cells in that tab's direction. Win when each unit sits on the matching-colour house.
- Specific challenge: figure out which tab to click how many times to align unit and house.
- Estimated optimal action count: ~5-10.

### Level 2
- `grid_size`: (32, 32)
- Number of sprites placed: 11.
- Level data: `{"RoA": 50, "TiD": [-2, 0]}` — slides 2 cells LEFT (negative direction). Uses different rotation (90).
- Mechanic introduced relative to L1: **Mirror direction** (negative TiD). Same mechanic, opposite slide direction; rotation 90 reorients the row to vertical.
- Specific challenge: navigate units to their matching houses with leftward slides.
- Estimated optimal action count: ~10-20.

### Level 3
- `grid_size`: (52, 52)
- Number of sprites placed: 23.
- Level data: `{"RoA": 75, "TiD": [0, 2]}` — slides 2 cells DOWN (vertical direction).
- Mechanic introduced relative to L2: **Vertical slides** (TiD on y-axis). More units (4+ figures), more houses, more floor tiles. Larger 52x52 grid.
- Specific challenge: align multiple units to their houses simultaneously while the slides only move the entire row.
- Estimated optimal action count: ~25-40.

Levels 4-7 exist but are excluded per skill scope.

## Action handlers

### ACTION6 (click)
- Trigger: `self.action.id.value == 6`.
- Branches: in `step()`, decrement step counter via `self.vrr.czh()`. Read (x, y); convert via `display_to_grid`; find the sprite at that grid position. If the sprite has tag `ZGd` → call `ccl(sprite)` which drags the row using `gel`. If sprite has tag `zHk` → if `krt` predicate passes, build an animation queue via `teu(sprite)` and assign to `self.vai`.
- Subsequent ticks (when `self.vai` is set) advance the bridge animation; when complete, run `jcy` (cleanup transient sprites).
- State mutations: every floor tile and unit's position; pull-tabs may relocate; `self.vai` animation queue.
- Engine effects: `next_level()` if `gug()` returns True (all units on matching houses); `lose()` if step counter at 0.

## HUD widgets

### `ehv` — depleting step bar (referenced as `self.vrr`)
- Class: `ehv` (RenderableUserDisplay).
- Render-pixel range: presumably row 63 or similar (standard pattern).
- What value it displays: `olv / lpw` (current/max). Reset per-level via `kbn`.

## Internal state — exhaustive

| attr (obfuscated) | semantic name | type | initial value | written by | read by | role |
|---|---|---|---|---|---|---|
| `vrr` | step_counter_HUD | `ehv` | `ehv(0)` | `__init__`, `kbn`, `step` | render | step counter |
| `oro` | slide_direction | `tuple[int, int]` | (0, 0) | `on_set_level` | many | `TiD` from level data |
| `dzy` | tab_to_pair_map | `dict[Sprite, tuple[Sprite, Sprite]]` | `{}` | `on_set_level` | `ccl` | maps each pull-tab to its (master_floor_tile, slave_floor_tile) pair |
| `vai` | bridge_animation | `ysn \| None` | None | `step`, `teu` | `step` | animation queue for bridge-extension sequences |

## Win condition

Plain English: every `HQB` unit must sit on top of an `fZK` target house whose pattern includes the unit's identifying colour, AND the unit's parent tower (`UXg`) must be properly attached via the row.

Literal condition: `gug()` (lines 1908-1927). For each `HQB` unit (`dds`):
- Read its colour `AkL` (the bottom-right pixel).
- Find the floor tile beneath it.
- Find the tower-tile attached to that floor.
- Check at least one `fZK` target's pixel-set contains `AkL` AND aligns with the unit's column AND the corresponding tower-tile is in the chain.

If True for every unit → win.

## Lose condition

Plain English: lose if step counter hits 0.

Literal condition: at line 2120, `elif not self.vrr.olv: self.lose()`.

## Resource economy

- Depleting resource: YES — step counter (per-level via `level.get_data("RoA")`: 50, 50, 75 for L1-3).
- Accumulating resource: YES (implicit) — count of units on matching houses.
- Lives mechanic: NO.
- Resource interaction: budget is sole lose; unit-position match is sole win.

## Action-budget signature

- Default budget per level: per-level via `level.get_data("RoA")`. L1=50, L2=50, L3=75.
- Whether budget tightens or shifts across levels 1-3: YES — L3 increases to 75.
- Decrement rate per action: 1 per click.
- Refill mechanism: NONE.

## Notable code patterns / techniques

- **`TiD` slide-direction in level data**: a 2-element list `[dx, dy]` specifies how far the row slides per click and in which axis.
- **Pair-mapping via geometric alignment** (`on_set_level` lines 1885-1906): for each pull-tab `pdw`, find its companion floor tiles by matching alignment along the slide axis.
- **Slide animation with carry-over** (`gel`): when the floor slides, units (`pth`) on top move with it; the floor tile's pixel array is also extended/trimmed to maintain visual continuity.
- **Bridge-extension via `teu` animation queue**: builds a list of `diu` move-instruction objects.

## Anti-patterns / lessons

- **3-character obfuscated names** (`ChX`, `EtZ`, etc.) — much shorter than typical (most Nova games use 10-character names). Tighter but still unreadable.
- **Heavy use of geometric alignment in `on_set_level`** to discover pairs at runtime — fragile if level layouts have edge cases.
- **Multi-tag dispatch** (`zHk + ACQ`, `ZGd + ACQ`) — clickable behaviours differ by primary tag.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES.
- Has lives mechanic: NO.
- Has click-to-select (uses ACTION6): YES.
- Has tag-based grouping: YES (`rDn`, `UXg`, `HQB`, `fZK`, `ZGd`, `zHk`, `ACQ`, `rlV`, `WuO`).
- Uses ACTION5 (modal): NO.
- Uses ACTION6 (click): YES.
- Uses ACTION7: NO.
- Has level data dicts: YES (`level.get_data("RoA")`, `level.get_data("TiD")`).
- Multi-mechanic per level: NO — same slide-row mechanic across L1-3 with axis variation.
- Tutorial level appears solvable by random play: UNKNOWN — small grid, few clicks; possibly yes.
- Has a depleting resource: YES — step counter.
- Has an accumulating resource: YES (implicit).
- Sprite shape convention used: mixed — coloured floor bars, small humanoid figures, house-shape targets.
- HUD position: bottom (typical).
- Palette size used: ~10 distinct values across L1-3.
- Background colour value: 3 (`BACKGROUND_COLOR = 3`).
- Padding / letter-box colour value: 4 (`PADDING_COLOR = 4`).
- Number of distinct mechanics introduced across levels 1-3: 1 (slide-row); L2 adds direction reversal, L3 adds vertical axis.
- Number of levels documented: 3.

(End of file.)
