# su15 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/su15/4c352900/su15.py`
- Lines: 2153
- Class name: `Su15`
- available_actions: `[6, 7]` (ACTION6=click, ACTION7=undo)
- Number of levels in source: 8+
- Number of levels documented in this analysis: 3
- Imports: `novaengine` standard + numpy.

## Mechanic essence (one sentence)

Coloured fruit-tokens scatter across an open arena, and the player clicks them one at a time to scoop them up — picking the right number-and-flavour combination ticks off the recipe printed at the top of the screen, while patrolling enemies drift toward the player's last click and end the run on contact.

## Sprite roster

(su15 has approximately 35 sprites. Tag-grouped overview below.)

| sprite (obfuscated) | dims | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| `0`-`8` | varies | varies | fruit, N | (default) | YES | (default) | YES | numbered fruit tokens (9 distinct flavours) |
| `avvxfurrqu` | varies | varies | goal | (default) | YES | (default) | YES | goal/recipe display tile |
| `spnivuaouo` / `wovupizsya` | varies | varies | goal | (default) | YES | (default) | YES | goal-display variants |
| `eifgovhtsm`, `jpjwahlikp`, `nyvfnpgcbv`, `pzqkrtozkk`, `recfijsnol`, `tltqnwoiek` | varies | varies | key | (default) | YES | (default) | YES | key tokens (UI/HUD glyphs) |
| `enemy` | varies | 8/12 | enemy | (default) | YES | (default) | YES | patrolling enemy that chases the player's last-click position |
| `enemy2` | varies | varies | enemy2 | (default) | YES | (default) | YES | secondary enemy variant |
| `enemy3` | varies | varies | enemy3 | (default) | YES | (default) | YES | tertiary enemy variant |
| `ezepymlzep` | varies | varies | hint | (default) | YES | (default) | YES | hint glyph (clickable to reveal) |
| `zjbjphqtno` | varies | varies | hint | (default) | YES | (default) | YES | hint glyph variant |
| `tixakbqato`, `wmivicdntp`, plus various others | varies | varies | (default) | (default) | YES | (default) | YES | UI/decoration sprites |

### Tag-group: `fruit` + numerical sub-tag (fruits)
- Sprites: `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8` (9 fruit types, each with its own palette signature).
- Pixel pattern: each is a unique small fruit shape (4-6 pixels wide).
- Role: collectibles. Click on one to consume it; consumption increments the recipe's tally for that fruit-type.
- Visual-vs-functional read: at-rendered-scale, distinct fruit silhouettes (apple, lemon, grape, etc.). Player tells them apart by shape and colour. Tag `fruit` + the numerical sub-tag (`0`, `1`, etc.) identifies the type.

### Tag-group: `goal` (goal-display)
- Sprites: `avvxfurrqu`, `spnivuaouo`, `wovupizsya`.
- Role: visual indicator of the recipe at the top. Per-level data `goal: [count, type]` specifies how many of which fruit type to collect.

### Tag-group: `enemy` / `enemy2` / `enemy3` (patrolling enemies)
- Sprites: `enemy`, `enemy2`, `enemy3`.
- Role: drift toward the player's last-click position. On contact with the player, lose. Different enemy types may have different speed.

### Tag-group: `key` (keys)
- Sprites: 6 different key glyphs.
- Role: appear in the HUD area at the top; some may unlock additional level features.

### Tag-group: `hint` (hint glyphs)
- Sprites: `ezepymlzep`, `zjbjphqtno`.
- Role: clickable hint tokens that reveal extra information.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (64, 64)
- Number of sprites placed: 8.
- Composition: 1 fruit-2 (`2` at (3, 58)), 1 goal (`avvxfurrqu` at (44, 11)), 1 key (`eifgovhtsm` at (30, 4)), 1 hint (`ezepymlzep` at (8, 52)), various UI tiles (`qakdkhhaxs`, `tixakbqato`, `vjbztqdvzs`, `xjbvgededw`).
- Level data: `{"goal": [2, 1], "steps": 32}` — collect 2 fruits of type-1.
- Mechanic introduced relative to the previous level: this is the first level — introduces the **collect-by-clicking** mechanic. ACTION6 click consumes the fruit at the click position. Recipe predicate compares collected counts against `goal`. Win when recipe satisfied.
- Specific challenge: there's only 1 fruit-2 placed, but the goal asks for 2 fruits of type-1. The hint glyph (`ezepymlzep`) likely indicates how to find more or transform.
- Estimated optimal action count: ~5-10.

### Level 2
- `grid_size`: (64, 64)
- Number of sprites placed: 13.
- Composition: 8 fruit-0 sprites scattered, 1 goal, 1 key (`pkqaggtppt`), 1 key (`recfijsnol`), 1 UI (`tixakbqato`), 1 large background (`wmivicdntp` scaled 2x).
- Level data: `{"goal": [3, 1], "steps": 32}` — collect 3 fruits of type-1.
- Mechanic introduced relative to L1: more fruits, but they're all type-0 while the goal asks for type-1; transformation via key needed.
- Specific challenge: figure out how to convert type-0 fruits to type-1 (likely via key interaction).
- Estimated optimal action count: ~15-20.

### Level 3
- `grid_size`: (64, 64)
- Number of sprites placed: 16.
- Composition: 6 fruit-0 + 3 fruit-1, 2 goals, 1 key, 1 UI tile.
- Level data: `{"goal": [[3, 1], [2, 1]], "steps": 48}` — multi-goal recipe.
- Mechanic introduced relative to L2: **Multi-goal** — must satisfy a list of recipe entries.
- Specific challenge: collect counts of multiple fruit types.
- Estimated optimal action count: ~20-30.

Levels 4-8 exist but are excluded per skill scope.

## Action handlers

### ACTION6 (click)
- Trigger: click on a fruit, hint, key, or other clickable.
- Branches: dispatch to interaction routines that decrement step counter, increment collected-count, possibly trigger enemy advance.

### ACTION7 (undo)
- Trigger: undo the most recent action; restore previous state from snapshot.

## HUD widgets

### `musowtfgnt` — depleting step bar
- Pattern: standard depleting bar at top or bottom of the frame.

## Internal state — exhaustive

| attr | semantic name | type | role |
|---|---|---|---|
| `reqbygadvzmjired` | goal_recipe | various | the recipe from `level.get_data("goal")` |
| `koprtgesg` | keys_collection | list[Sprite] | all key-tagged sprites |
| `citbwsczl` | (collected fruits state) | dict | per-fruit-type counters |

## Win condition

Plain English: every entry in the level's `goal` recipe is satisfied (i.e. the right count of each required fruit type has been collected).

Literal condition: in the step handler, after a fruit collection, check `len(get_sprites_by_tag("fruit"))` against the recipe.

## Lose condition

Plain English: lose if the step counter hits 0 OR an enemy reaches the player.

## Resource economy

- Depleting resource: YES — step counter (per-level: 32, 32, 48).
- Accumulating resource: YES — collected-fruit count (the "score" toward the recipe).
- Lives mechanic: NO.

## Action-budget signature

- Default budget per level: per-level via `level.get_data("steps")`. L1=32, L2=32, L3=48.
- Whether budget tightens or shifts across levels 1-3: YES — L3 increases to 48.
- Decrement rate: 1 per click.
- Refill mechanism: NONE.

## Notable code patterns / techniques

- **Numerical sub-tag on fruits** (`fruit + "0".."8"`): tag combinations identify fruit type without separate name dispatch.
- **Multi-goal recipes** in level data (a list of `[count, type]` entries).
- **Enemy chase via last-click target**: enemies drift toward the player's last click position rather than a player avatar (no avatar in this game).

## Anti-patterns / lessons

- **Numeric string sprite names** (`"0"`, `"1"`, ..., `"8"`) — the names ARE the type identifiers. Mixed convention with the obfuscated long names.
- **Many UI sprites** — the top portion of the frame is dense with key/goal/hint indicators.
- **Multiple enemy variants** with subtle behaviour differences encoded in tag.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES.
- Has lives mechanic: NO.
- Has click-to-select: YES.
- Has tag-based grouping: YES (`fruit`, `goal`, `enemy`, `key`, `hint`, plus numerical sub-tags).
- Uses ACTION5: NO.
- Uses ACTION6: YES.
- Uses ACTION7: YES (undo).
- Has level data dicts: YES (`level.get_data("goal")`, `level.get_data("steps")`).
- Multi-mechanic per level: NO — same recipe-collection mechanic; L3 adds multi-goal complexity.
- Tutorial level appears solvable by random play: UNKNOWN.
- Has a depleting resource: YES — step counter.
- Has an accumulating resource: YES — collected counts per fruit type.
- Sprite shape convention used: mixed — small fruit glyphs (4-6 cells), enemy patrols (varies), HUD keys/hints.
- HUD position: top.
- Palette size used: ~10 distinct values across L1-3.
- Background colour value: 5.
- Padding / letter-box colour value: 3.
- Number of distinct mechanics introduced across levels 1-3: 1-2 (recipe collection in L1, multi-goal in L3).
- Number of levels documented: 3.

(End of file.)
