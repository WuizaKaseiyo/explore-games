# tn36 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/tn36/ab4f63cc/tn36.py`
- Lines: 2624
- Class name: `Tn36`
- available_actions: `[6]` (click only)
- Number of levels in source: 7
- Number of levels documented in this analysis: 3
- Imports: standard novaengine + numpy.

## Mechanic essence (one sentence)

A small programmable pawn sits at one end of a coloured runway with a row of slot-buttons spread across the bottom of the screen, and the player clicks buttons in sequence to choose a programme of move-and-rotate instructions; running the programme makes the pawn step through the runway one tick at a time, and the level wins when the pawn's traced path lights up exactly the cells of the target pattern.

## Sprite roster

(tn36 has approximately 50 sprites. Key tag-groups summarised below.)

| sprite (obfuscated) | dims | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| `ajoyntzwka` | varies | varies | ccjcukzyce | (default) | YES | (default) | YES | runway tile (palette base) |
| `ccjcukzyce` | varies | varies | ccjcukzyce | (default) | YES | (default) | YES | runway tile variant |
| `baxznkbwix` | varies | varies | baxznkbwix, sys_click | (default) | YES | (default) | YES | clickable instruction-button |
| `clnkuqefvl` | varies | varies | clnkuqefvl | (default) | YES | (default) | YES | runway pattern marker |
| `cohggajxpz` | 64x64 | varies | (default) | (default) | YES | (default) | YES | full-frame background |
| `egshileqmu` | varies | varies | qgqvgxjtau, sys_click | (default) | YES | (default) | YES | clickable run-button (commit) |
| `etitgfbxdb` | varies | varies | zdzgatsoyb, ilkhmcqzxr | (default) | YES | (default) | YES | level-target marker |
| `gntlsxcsje` | varies | varies | trvxlvpbdv | (default) | YES | (default) | YES | (auxiliary) |
| `iggxhsyqne` | varies | varies | (default) | (default) | YES | (default) | YES | empty slot indicator |
| `kbopcuwwcp` | varies | varies | baxznkbwix, sys_click | (default) | YES | (default) | YES | clickable button variant |
| `kjhqtlszdp` | varies | varies | rlqfpkqktk, sys_click | (default) | YES | (default) | YES | clickable rotation/scale button |
| `mgmykqfuye` | varies | varies | mgmykqfuye | (default) | YES | (default) | YES | (auxiliary) |
| `nptbwdzzvs` | varies | varies | annjcsdtyc | (default) | YES | (default) | YES | shape sprite |
| `pstzpoiwdb` | varies | varies | yssamcbruq | (default) | YES | (default) | YES | (auxiliary) |
| `qzgehddpew` | varies | varies | egcefpppze | (default) | YES | (default) | YES | (auxiliary) |
| `rnftwykgro` | varies | varies | (default) | (default) | YES | (default) | YES | runway colour cell |
| `rrvflvsand` | varies | varies | udwswsnybp | (default) | YES | (default) | YES | (auxiliary) |
| `sduonucejh` | varies | varies | tkgkshggjr | (default) | YES | (default) | YES | (auxiliary) |
| `trvxlvpbdv` | varies | varies | trvxlvpbdv | (default) | YES | (default) | YES | (auxiliary) |
| `veaxnfieni` | varies | varies | ylbysintoa | (default) | YES | (default) | YES | shape variant |
| `xaxbhjndqw` | varies | varies | yikencmwll | (default) | YES | (default) | YES | (auxiliary) |
| `znhdjhhoai` | varies | varies | (default) | (default) | YES | (default) | YES | (auxiliary) |
| `zdzgatsoyb` | varies | varies | zdzgatsoyb | (default) | YES | (default) | YES | target marker variant |
| (others) | varies | varies | various | (default) | YES | (default) | YES | runway cells, frames, marker variants |

### Tag-group: `ccjcukzyce` and `clnkuqefvl` (runway / pattern tiles)
- Sprites: many.
- Role: form the runway grid against which the pawn steps. The colour pattern of these cells is the target pattern.

### Tag-group: `baxznkbwix + sys_click` (programme buttons)
- Sprites: `baxznkbwix`, `kbopcuwwcp`.
- Role: clickable buttons. Each click adds an instruction to the programme.

### Tag-group: `qgqvgxjtau + sys_click` (run-buttons)
- Sprites: `egshileqmu`.
- Role: clickable. Click executes the programme.

### Tag-group: `rlqfpkqktk + sys_click` (rotation/scale buttons)
- Sprites: `kjhqtlszdp`.
- Role: clickable instruction modifier (rotation or scale).

### Tag-group: `zdzgatsoyb`, `ilkhmcqzxr` (target markers)
- Sprites: `etitgfbxdb`, `zdzgatsoyb`.
- Role: indicate the desired final pattern.

### Tag-group: `annjcsdtyc`, `mjbdqbhcpj` (programmable pawn)
- Sprites: shape sprites that execute the programme.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (64, 64)
- Number of sprites placed: 30.
- Composition: Many runway tiles, programme buttons, target markers, 1 pawn shape (`ylbysintoa`).
- Level data: (none in source, defaults).
- Mechanic introduced relative to the previous level: this is the first level — introduces the **programme-the-pawn** mechanic. The player clicks programme-buttons to add instructions; clicks the run-button to execute. The pawn walks the runway following the instructions; win when the pawn's path matches the target pattern.
- Specific challenge: figure out the right sequence of moves to lay down the target pattern.
- Estimated optimal action count: ~10-15.

### Level 2
- `grid_size`: (64, 64)
- Number of sprites placed: many (60+).
- Level data: `{"Programs": [[1,1,1,1], [33,33,33,33]], "Positions": [[2,0], [0,2]], "Rotations": [90, 180], "Scales": [1, 1], "Reset": [False, False]}` — multi-pawn programme.
- Mechanic introduced relative to L1: **Multiple pawns** with separate programmes. Each pawn has its own initial position, rotation, and scale. The data dict spells out a default programme that the player can modify.
- Specific challenge: program multiple pawns simultaneously to draw overlapping patterns.

### Level 3
- `grid_size`: (64, 64)
- Number of sprites placed: many (90+).
- Level data: `{"Programs": [[3,3,3,3], [33,33,33,33], [34,34,34,34], [2,2,2,2]], "Positions": [[0,-2], [0,2], [2,0], [-2,0]], "Rotations": [...], "Scales": [...]}` — 4 pawns.
- Mechanic introduced relative to L2: **4 pawns** with 4 different programmes.
- Specific challenge: orchestrate 4 pawns to draw a complex pattern.

Levels 4-7 exist but are excluded per skill scope.

## Action handlers

### ACTION6 (click)
- Trigger: click on a sys_click-tagged sprite.
- Branches: dispatch by sprite tag — `baxznkbwix` adds instruction; `qgqvgxjtau` runs programme; `rlqfpkqktk` cycles rotation/scale.

## HUD widgets

Standard depleting bar at row 63 (BACKGROUND_COLOR=5, PADDING_COLOR=3).

## Internal state — exhaustive

Multiple animation tick variables and programme storage; complex state machine.

## Win condition

Plain English: after running the programme, the runway colour pattern matches the target pattern.

## Lose condition

Plain English: lose if step counter (clicks budget) hits 0 without solving.

## Resource economy

- Depleting resource: YES (step counter).
- Accumulating resource: YES (programme instructions).
- Lives mechanic: NO.

## Action-budget signature

- Default budget per level: per-level data.
- Per-level vs. per-environment: per-level.
- Decrement rate: 1 per click.

## Notable code patterns / techniques

- **Programme as level data** (`Programs`, `Positions`, `Rotations`, `Scales`, `Reset`): the level dict spells out the initial programme parameters.
- **Multi-pawn execution**: each pawn has its own programme list.

## Anti-patterns / lessons

- **Heavy sprite library**: 50+ sprites for the programme-runway puzzle.
- **Complex level data structure** with nested arrays.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES.
- Has lives mechanic: NO.
- Has click-to-select: YES.
- Has tag-based grouping: YES (many tags).
- Uses ACTION5: NO.
- Uses ACTION6: YES.
- Uses ACTION7: NO.
- Has level data dicts: YES (Programs, Positions, Rotations, Scales, Reset).
- Multi-mechanic per level: NO — single mechanic with parameter variation.
- Tutorial level appears solvable by random play: NO.
- Has a depleting resource: YES.
- Has an accumulating resource: YES.
- Sprite shape convention used: mixed.
- HUD position: bottom.
- Palette size used: ~10.
- Background colour value: 5.
- Padding / letter-box colour value: 3.
- Number of distinct mechanics introduced across levels 1-3: 1 (programme-execute) + multi-pawn variation.
- Number of levels documented: 3.

(End of file.)
