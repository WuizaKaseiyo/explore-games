# sc25 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/sc25/f9b21a2f/sc25.py`
- Lines: 2716
- Class name: `Sc25`
- available_actions: `[1, 2, 3, 4, 6]` (UP/DOWN/LEFT/RIGHT, click)
- Number of levels in source: 6
- Number of levels documented in this analysis: 3
- Imports: standard novaengine + numpy.

## Mechanic essence (one sentence)

A small explorer-avatar wanders an illustrated scene while a 3×3 directional touch-pad sits in the bottom-right corner and the four arrow keys are also active; tapping a pad-cell or pressing an arrow nudges the avatar one step toward any of the nine compass directions, and the level is solved when the avatar finds and reaches the specific scenery item named in the level's hidden goal-string.

## Sprite roster

sc25 has many sprites with frequently-used groups:

| sprite (obfuscated) | role |
|---|---|
| `bbyayvbjq` | 3x3 grid of pad-buttons (always 9 copies at fixed positions in the bottom-right) |
| `jqwvpaczd-1/2/3/4` | direction-pad icons overlaying the pad buttons |
| `dtfljwuit-1/2/3/4/5` | per-level scene backdrop |
| `lppppobad-*` (suffixes: `ewsjvovai`, `fpokrvgln`, `jzukcpajs`, `aprnrzeyj`, `ui`) | scenery item with named identifier (the named one is the goal per `wdsxxkugj`) |
| `nwxssyzit` | recurring scene element (large, scaled) |
| `pcohqadae` | recurring icon |
| `sjzzsedwu` | corner UI element |
| `edusagitv`, `eeneuskrx`, `fxxlxszkp`, `hldxbucrr`, `ltwvrfpfp`, `miouvjsug`, `xhjhqjlxm` | level-specific decorations |
| (others) | various |

Tags: `jqwvpaczd` (the pad), `sys_click`.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (64, 64).
- Composition: 9 pad buttons (`bbyayvbjq`), 9 pad-direction icons (`jqwvpaczd-*`), `dtfljwuit-2` backdrop, `lppppobad-fpokrvgln` (goal target), `lppppobad-ewsjvovai` (decoy), `lppppobad-ui` (UI element), `nwxssyzit` (avatar?) at (39, 19), `pcohqadae` at (12, 17), `sjzzsedwu` corner UI.
- Level data: `{"sykpecmoq": 50, "wdsxxkugj": "fpokrvgln", "ozhskarnd": True}` — 50-step budget; goal is `lppppobad-fpokrvgln`.
- Mechanic introduced relative to the previous level: this is the first level — introduces the **pad-and-arrows navigation** mechanic. Click a pad cell (ACTION6) or press an arrow key (ACTION1-4) to move the avatar. Win when the avatar reaches the specific goal sprite named in `wdsxxkugj`.

### Level 2
- `grid_size`: (64, 64).
- Composition: same pad + new backdrop `dtfljwuit-1`, new decorations.
- Level data: `{"sykpecmoq": 25, "wdsxxkugj": "jzukcpajs", "ozhskarnd": True}` — tighter 25-step budget; different goal.

### Level 3
- `grid_size`: (64, 64).
- Composition: same pad + backdrop `dtfljwuit-4`, new decorations + `aprnrzeyj` goal.
- Level data: `{"sykpecmoq": 50, "wdsxxkugj": "aprnrzeyj", "ozhskarnd": True}`.

Levels 4-6 exist but are excluded per skill scope.

## Action handlers

### ACTION1-4 (UP/DOWN/LEFT/RIGHT)
- Trigger: arrow keys.
- Branches: move the avatar 1 cell.

### ACTION6 (click)
- Trigger: click on the 3x3 pad.
- Branches: dispatch direction based on which pad cell was clicked. The pad-cell positions in `_get_valid_actions` (line 1691-1699) are 9 (x, y) pairs at columns 25, 30, 35 and rows 50, 55, 60.

## HUD widgets

Step counter implicit. Bottom-right pad doubles as visible UI.

## Internal state — exhaustive

`sykpecmoq` (step budget), `wdsxxkugj` (goal-name string).

## Win condition

The avatar reaches the sprite whose name matches `level.get_data("wdsxxkugj")` (the suffix of an `lppppobad-*` sprite).

## Lose condition

Step counter hits 0.

## Resource economy

- Depleting resource: YES — step counter (50, 25, 50 for L1-3).
- Accumulating resource: avatar progress.
- Lives mechanic: NO.

## Action-budget signature

- Default budget per level: per-level via `level.get_data("sykpecmoq")`.
- Decrement rate: 1 per move.
- Refill mechanism: NONE.

## Notable code patterns / techniques

- **Goal name in level data** (`wdsxxkugj`): a string identifies which sprite is the win target.
- **3x3 directional pad with click-coords pre-defined** in `_get_valid_actions`.
- **Both arrow keys AND pad-clicks** dispatch the same movement logic — UI flexibility.

## Anti-patterns / lessons

- **Goal target identified by name suffix matching** — fragile.
- **Same 9 pad-position list duplicated in `_get_valid_actions`** — could be parameterised.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES (implicit).
- Has lives mechanic: NO.
- Has click-to-select: YES.
- Has tag-based grouping: YES (`jqwvpaczd`, `sys_click`).
- Uses ACTION5: NO.
- Uses ACTION6: YES.
- Uses ACTION7: NO.
- Has level data dicts: YES (`sykpecmoq`, `wdsxxkugj`, `ozhskarnd`).
- Multi-mechanic per level: NO — same navigation mechanic.
- Tutorial level appears solvable by random play: UNKNOWN — depends on goal proximity.
- Has a depleting resource: YES.
- Has an accumulating resource: YES (avatar position toward goal).
- Sprite shape convention used: mixed.
- HUD position: bottom-right (the pad).
- Palette size used: ~12.
- Background colour value: 2.
- Padding / letter-box colour value: 3.
- Number of distinct mechanics introduced across levels 1-3: 1 (navigation).
- Number of levels documented: 3.

(End of file.)
