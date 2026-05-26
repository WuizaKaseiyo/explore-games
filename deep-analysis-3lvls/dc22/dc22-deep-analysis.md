# dc22 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/dc22/4c9bff3e/dc22.py`
- Lines: 2917
- Class name: `Dc22`
- available_actions: `[1, 2, 3, 4, 6]` (UP/DOWN/LEFT/RIGHT, click)
- Number of levels in source: 6+
- Number of levels documented in this analysis: 3
- Imports: standard novaengine + numpy + typing.

## Mechanic essence (one sentence)

A small pawn walks across a board scattered with coloured wedge-blocks and one or more spinning colour-wheel triggers, and stepping on a trigger cycles every wedge of the same colour to its next colour-state in a fixed sequence — the level is solved when the wedges' colours line up to match a target ring shown alongside the puzzle.

## Sprite roster

dc22 has approximately 60 sprites. Key tag-groups:

| tag-group | count | role |
|---|---|---|
| `pcxjvnmybet` | 1 per level | player avatar |
| `wbze` | many | colour-cycling wedges (sprites named with numeric suffix like `wbze-efzv1`, `wbze-efzv2`) — the suffix encodes the current colour-state |
| `itki` | several | colour-cycle triggers (also numeric-suffixed) |
| `vgiqmhpyxb` ("itki-color-cycle") | dynamic | triggers that cycle wedges of a colour |
| `bpnwmawiuv` ("itki-color-jpug") | dynamic | special trigger variant |
| `zgkdpiyghze` | varies | targets / goal markers |
| `bqxa` | 1 per level | level-name banner / status display |
| `jpug-*` | varies | jpug-tagged status indicators (intangible) |
| `kbqq-efzv` | varies | static decoration tiles |
| `merged-sprite`, `qeqe-bg` | 1 per level | level-frame backgrounds |
| `hhxv*`, `vckz-*`, `qgdz-*`, `bgeg-*`, `rpygrnbjhwj*` | varies | level-specific decoration / extra mechanics |

(Per-sprite per-bullet documentation is omitted for brevity given the sprite count and analysis context budget; sprites within a tag group share role.)

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (64, 44)
- Number of sprites placed: 14.
- Composition: 1 player (`bqxa` at (24, 10) — actually `bqxa` may be HUD; player is `pcxjvnmybet`-tagged; check on_set_level), various `wbze` colour wedges, `itki` triggers, decoration.
- Level data: `{"StepCounter": 128}`.
- Mechanic introduced relative to the previous level: this is the first level — introduces the **walk + trigger + cycle** mechanic. Arrow keys move the pawn 1 cell; walking onto an `itki` trigger cycles all `wbze`-tagged sprites of the matching prefix through their colour-numbered states (e.g. `wbze-efzv1` → `wbze-efzv2`). Win when colour configuration matches target.
- Specific challenge: figure out which trigger cycles which wedges and reach the goal configuration.

### Level 2
- `grid_size`: (64, 48)
- Number of sprites placed: 19.
- Level data: `{"StepCounter": 192}`.
- Mechanic introduced relative to L1: **More wedges and triggers**; possibly compound triggers (`itki-color-cycle` and `itki-color-jpug` interact differently).

### Level 3
- `grid_size`: (64, 48)
- Number of sprites placed: 24.
- Level data: `{"StepCounter": 192}`.
- Mechanic introduced relative to L2: **More complex wedge graph** with `itki1`/`itki2` triggers and `wbze-efzv-p-1`/`wbze-efzv_vucz_1` wedge variants.

Levels 4-6 exist but are excluded per skill scope.

## Action handlers

### ACTION1-4 (UP/DOWN/LEFT/RIGHT)
- Trigger: arrow keys move the player 1 cell.
- Side effects: if the new cell hits an `itki` trigger, dispatch colour-cycle on the matching `wbze` group.

### ACTION6 (click)
- Trigger: click-to-interact (specific to certain `jpug` sprites).

## HUD widgets

`khximaydsc` — bottom-row depleting bar at row 63, plus a "fade-out vignette" effect when `pxicvzkjuui >= 0` (approaching lose).

## Internal state — exhaustive

Many: `lvnwxszdcv` (cycling state), `qmxenejanqe` (per-prefix wedge count), `wbzes` (all colour wedges), etc.

## Win condition

When the configuration of `wbze` colour-states matches the level's target.

## Lose condition

Step counter hits 0.

## Resource economy

- Depleting resource: YES — step counter (per-level: 128, 192, 192).
- Accumulating resource: YES (implicit) — wedges in target state.
- Lives mechanic: NO.

## Action-budget signature

- Default budget per level: per-level via `level.get_data("StepCounter")`. L1=128, L2=192, L3=192.
- Decrement rate: 1 per movement; possibly 20 per "deduction event" via `yepbymuune`.
- Refill mechanism: NONE.

## Notable code patterns / techniques

- **Numeric-suffix sprite naming** (`wbze-efzv1`, `wbze-efzv2`): the suffix encodes the colour state; cycling increments the suffix.
- **Per-prefix wedge count cache** (`qmxenejanqe`): pre-computes how many states each wedge group has.
- **Vignette fade-out HUD effect** when approaching loss state.

## Anti-patterns / lessons

- **Heavy sprite library** (60+) for L1-3; many never used in scope.
- **Complex name-based dispatch** (suffix parsing of sprite names).

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
- Has level data dicts: YES (StepCounter).
- Multi-mechanic per level: NO — same colour-cycle mechanic across L1-3.
- Tutorial level appears solvable by random play: NO.
- Has a depleting resource: YES.
- Has an accumulating resource: YES (implicit).
- Sprite shape convention used: mixed.
- HUD position: bottom (with optional full-frame vignette).
- Palette size used: ~12 distinct values.
- Background colour value: 4.
- Padding / letter-box colour value: 3.
- Number of distinct mechanics introduced across levels 1-3: 1 (colour-cycle).
- Number of levels documented: 3.

(End of file.)
