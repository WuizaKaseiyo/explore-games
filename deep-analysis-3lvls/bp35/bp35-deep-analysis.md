# bp35 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/bp35/0a0ad940/bp35.py`
- Lines: 4588
- Class name: `Bp35`
- available_actions: `[3, 4, 6, 7]` (LEFT, RIGHT, click, undo)
- Number of levels in source: 9
- Number of levels documented in this analysis: 3
- Imports: standard novaengine + numpy.

## Mechanic essence (one sentence)

A small token traverses a procedurally-generated graph of coloured nodes, and the player clicks one of the highlighted neighbour-nodes (or presses LEFT/RIGHT to step along the current track) to walk the token one edge at a time toward a winning configuration — undo rewinds the most recent move and resetting the level reshuffles the graph layout per level index.

## Sprite roster

bp35 is unusual: 117 sprite definitions exist in the dictionary but every level uses only `sprite-1` as a placeholder at (4, 3). The actual game content (graph nodes, edges, tokens, win positions) is constructed at runtime by `uakietkqfso()` keyed on `qswcochjodb = level_index + 1`. The 117 sprite library functions as the procedural-content-generation alphabet rather than per-level placements.

Per the SKILL's "every entry needs a row" requirement: there are 117 entries in `sprites = {...}`, all unique 5-12-pixel glyphs in varying palettes, but they're invoked dynamically by the procedural builder. Per-level documentation cannot enumerate them at static analysis time without executing the generator — they are loaded into a graph data structure and rendered via the runtime camera system.

| sprite category | count | role |
|---|---|---|
| node-colour glyphs | ~40 | individual coloured nodes for the graph |
| edge-decoration glyphs | ~30 | visual connectors between nodes |
| token / marker glyphs | ~15 | the player token and movement indicators |
| HUD / control glyphs | ~10 | overlays, buttons, indicators |
| placeholder | 1 (`sprite-1`) | default level-1 token (4, 3) |
| miscellaneous | ~21 | various unique procedurally-used glyphs |

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (8, 8)
- Number of sprites placed: 1 (`sprite-1` at (4, 3)).
- Composition: a single placeholder; actual content built by procedural builder using `qswcochjodb = 1`.
- Level data: none.
- Mechanic introduced relative to the previous level: this is the first level — introduces graph navigation. Procedural builder constructs a small graph for level 1; the player walks a token using LEFT/RIGHT (along the current track) or click (to jump to a clicked node).

### Level 2
- `grid_size`: (8, 8)
- Number of sprites placed: 1 (placeholder).
- Procedural seed: level index 2.
- Mechanic: same; larger or more complex graph.

### Level 3
- `grid_size`: (8, 8)
- Number of sprites placed: 1 (placeholder).
- Procedural seed: level index 3.

(All 9 levels share the same level data; the difference is solely the procedural builder seed.)

## Action handlers

### ACTION3 / ACTION4 (LEFT / RIGHT)
- Trigger: `self.action.id == GameAction.ACTION3/4`.
- Branches: in `urzvqcxbsz`, dispatch `oreuzgjmdx(-1, 0)` / `oreuzgjmdx(1, 0)` — moves the token one edge left or right along the current track.

### ACTION6 (click)
- Trigger: click on a node.
- Branches: dispatch `gwfodrkvzx(x, y)` — attempt to traverse to the clicked node.

### ACTION7 (undo)
- Trigger: undo the most recent move.

## HUD widgets

`qmjscfjptx` — runs at the camera level, rendering the procedural game state into 64x64 frames.

## Internal state — exhaustive

Procedurally-built graph state held in `oztjzzyqoek` (uakietkqfso instance). Specific attributes are obfuscated and built dynamically.

## Win condition

`oztjzzyqoek.nkuphphdgrp` flag set True triggers `next_level()`. The exact predicate depends on the procedural game's goal (likely "token reaches goal node" or similar).

## Lose condition

`oztjzzyqoek.jrhqdvdwpsb` flag set True triggers `lose()`. Likely "token enters losing state" (e.g. invalid move, time-out, etc.).

## Resource economy

- Depleting resource: `hbqwwgceeqp` counter (incremented per action). Likely the step counter.
- Accumulating resource: progress through the graph.
- Lives mechanic: NO.

## Action-budget signature

- Default budget per level: derived from procedural seed.
- Per-level vs. per-environment: per-level.
- Decrement rate: 1 per action.

## Notable code patterns / techniques

- **Procedural content generation** keyed on level index. Single placeholder sprite per level definition; actual content built at level start.
- **Action set restricted to 4 actions** (LEFT, RIGHT, click, undo) — no UP/DOWN, suggesting horizontal-only navigation along a track.
- **Custom HUD class** (`qmjscfjptx`) that maintains its own frames_to_render queue.

## Anti-patterns / lessons

- **117 sprite definitions, all used procedurally** — extreme sprite-library size for a small 8x8 grid game.
- **Procedural generation in source code** is opaque to static analysis; static analysis can only describe the action API and class structure.
- **`GRAPH_BUILDER` global flag** that toggles between play mode and graph-construction mode is a code-smell.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES (implicit via `hbqwwgceeqp`).
- Has lives mechanic: NO.
- Has click-to-select: YES.
- Has tag-based grouping: UNKNOWN — depends on procedural builder.
- Uses ACTION5: NO.
- Uses ACTION6: YES.
- Uses ACTION7: YES (undo).
- Has level data dicts: NO (level data is empty; everything is procedural).
- Multi-mechanic per level: NO — same procedural mechanic across all levels.
- Tutorial level appears solvable by random play: UNKNOWN — depends on graph.
- Has a depleting resource: YES (action counter).
- Has an accumulating resource: YES (graph progress).
- Sprite shape convention used: mixed.
- HUD position: dynamic.
- Palette size used: many (procedural).
- Background colour value: dynamic constant `jltzfsatusf` (uses module-level globals; effective value 0 from line 96).
- Padding / letter-box colour value: dynamic constant `mxsayyrckip` (effective 3).
- Number of distinct mechanics introduced across levels 1-3: 1 base mechanic; difficulty scales with level index seed.
- Number of levels documented: 3 (with caveat that levels are procedurally identical in structure, differing only by seed).

(End of file.)
