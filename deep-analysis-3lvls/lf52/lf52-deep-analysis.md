# lf52 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/lf52/271a04aa/lf52.py`
- Lines: 5877
- Class name: `Lf52`
- available_actions: `[1, 2, 3, 4, 6, 7]` (UP/DOWN/LEFT/RIGHT, click, undo)
- Number of levels in source: 10
- Number of levels documented in this analysis: 3
- Imports: standard novaengine + numpy + typing.

## Mechanic essence (one sentence)

A small token sits on an 8×8 board of procedurally-generated coloured nodes; pressing an arrow key shuffles the token one step along the current track, clicking on a highlighted neighbour-node teleports it there, and undo rewinds the latest move — the level wins when the token reaches a procedurally-defined target configuration whose layout depends on the level's seed index.

## Sprite roster

lf52 follows the same procedural-content-generation pattern as bp35: every level uses only `xnpkcymhua` as a placeholder at (3, 2) on an 8×8 grid. The actual game content (graph nodes, edges, tokens, target) is built at level-start by a runtime generator keyed on `level_index + 1`.

The sprite dictionary contains hundreds of glyphs that the generator picks from. Per-sprite enumeration is omitted given the procedural nature; sprites are loaded into the runtime graph rather than placed declaratively.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (8, 8).
- Composition: 1 placeholder (`xnpkcymhua` at (3, 2)); actual content built procedurally with seed 1.
- Mechanic introduced relative to the previous level: this is the first level — introduces the procedural graph-traversal mechanic.

### Level 2
- `grid_size`: (8, 8).
- Procedural seed 2.

### Level 3
- `grid_size`: (8, 8).
- Procedural seed 3.

Levels 4-10 exist but are excluded per skill scope (and follow the same pattern, differing only by seed).

## Action handlers

### ACTION1-4 (UP/DOWN/LEFT/RIGHT)
- Each dispatches a directional move via the procedural game-state's `oreuzgjmdx` (or analogous) handler.

### ACTION5
- Special action via `uatdugrwtx` (or analogous).

### ACTION6 (click)
- Jump to the clicked node.

### ACTION7 (undo)
- Rewind the most recent move.

## HUD widgets

Step counter implicit in the procedural game-state. `BACKGROUND_COLOR = LIGHT_BLUE = 10`, `PADDING_COLOR = DARK_GRAY = 3`.

## Internal state — exhaustive

All state held in the procedural game-object instance.

## Win condition

Procedural — depends on level seed.

## Lose condition

Procedural — depends on level seed.

## Resource economy

- Depleting resource: implicit step counter.
- Accumulating resource: graph-traversal progress.
- Lives mechanic: NO.

## Action-budget signature

- Default budget per level: derived from procedural seed.
- Decrement rate: 1 per action.

## Notable code patterns / techniques

- **Procedural content generation** keyed on level index — same pattern as bp35.
- **STORES_UNDO global flag** controls whether ACTION7 is registered.
- **GRAPH_BUILDER global flag** toggles between play mode and graph-building mode.

## Anti-patterns / lessons

- **Massive procedural codebase** (5877 lines) for a 10-level 8×8 game.
- **Placeholder sprite-only level data** — opaque to static analysis.

## Cross-references

Highly similar to bp35 in structure (procedural generation, placeholder levels).

## Frequency-table contributions

- Has step-counter HUD: YES (implicit).
- Has lives mechanic: NO.
- Has click-to-select: YES.
- Has tag-based grouping: UNKNOWN (procedural).
- Uses ACTION5: YES.
- Uses ACTION6: YES.
- Uses ACTION7: YES (undo).
- Has level data dicts: NO.
- Multi-mechanic per level: NO — same procedural mechanic.
- Tutorial level appears solvable by random play: UNKNOWN.
- Has a depleting resource: YES.
- Has an accumulating resource: YES.
- Sprite shape convention used: mixed.
- HUD position: dynamic.
- Palette size used: 16 (full palette via WHITE..PURPLE constants).
- Background colour value: 10 (LIGHT_BLUE).
- Padding / letter-box colour value: 3 (DARK_GRAY).
- Number of distinct mechanics introduced across levels 1-3: 1 base mechanic; difficulty scales with level index seed.
- Number of levels documented: 3.

(End of file.)
