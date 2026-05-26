# ft09 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/ft09/0d8bbf25/ft09.py`
- Lines: 2517
- Class name: `Ft09`
- available_actions: `[6]` (click only)
- Number of levels in source: 6
- Number of levels documented in this analysis: 3
- Imports: standard novaengine + numpy.

## Mechanic essence (one sentence)

A 32×32 canvas of empty cells extends past the camera's 16×16 viewport, and the player taps a cell with a stamp-glyph hovering over it; each tap stamps a small 3×3 colour-pattern around the clicked cell — the level is solved when the canvas's stamped pattern matches the target pattern printed in the corner.

## Sprite roster

ft09 has 100+ sprites, mostly `bsT`-tagged cell tiles (the canvas cells themselves), plus `Hkx` (click-stamps), `NTi` (alternative click-stamps), `gOi` (glyph), `Ycb` (level-1 demo helper). Per-sprite enumeration is omitted for brevity given the extreme count.

| tag-group | count | role |
|---|---|---|
| `bsT` | many | canvas cell tiles (the 32×32 grid) |
| `Hkx` | varies | clickable stamp source — 3x3 mask used to apply colour at click |
| `NTi` | varies | alternate clickable stamp (uses `gOi` glyph mask instead of fixed 3x3) |
| `Ycb` | 1 (L1) | tutorial demo highlight (level 1 only) |
| `gOi` | varies | glyph for stamp pattern |

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (32, 32)
- Composition: many `bsT` canvas tiles + 1 demo `Ycb` highlight + a few `Hkx` stamp tools.
- Level data: `{"kCv": ..., "cwU": ..., "elp": ...}` — initial step counter, target colours, stamp pattern.
- Mechanic introduced relative to the previous level: this is the first level — introduces the **click-to-stamp** mechanic. ACTION6 click on a `bsT` cell stamps a 3×3 pattern centred there. Win when the canvas matches the target.

### Level 2
- `grid_size`: (32, 32)
- Mechanic: same; more cells.

### Level 3
- `grid_size`: (32, 32)
- Mechanic: same; possibly larger target.

Levels 4-6 exist but are excluded per skill scope.

## Action handlers

### ACTION6 (click)
- Trigger: click on a `Hkx` or `NTi`-tagged sprite.
- Branches: dispatch the 3×3 stamp `irw` (or per-sprite `eHl` for `NTi`) at the click position. Each cell of the 3×3 mask applies a colour to the corresponding canvas cell.

## HUD widgets

`sve` HUD class — depleting bar at the bottom of the 16x16 viewport.

## Internal state — exhaustive

`zth` (level-1 demo highlight), `our` (animation tick), `gqb` (target colours `[9, 8]` default), `irw` (default 3x3 stamp pattern `[[0,0,0],[0,1,0],[0,0,0]]`).

## Win condition

When the stamped canvas matches the target pattern.

## Lose condition

Step counter hits 0.

## Resource economy

- Depleting resource: YES (step counter from `level.get_data("kCv")`).
- Accumulating resource: YES (canvas cells stamped).
- Lives mechanic: NO.

## Action-budget signature

- Default budget per level: per-level via `level.get_data("kCv")`.
- Decrement rate: 1 per click.
- Refill mechanism: NONE.

## Notable code patterns / techniques

- **Camera viewport smaller than grid** (16×16 viewport over 32×32 grid) — implies scrolling or partial visibility.
- **Stamp pattern in level data** (`elp`) — flexibly configurable per-level.
- **Demo highlight on L1** (`Ycb`) — the first level shows a tutorial pulse animation.

## Anti-patterns / lessons

- **Many sprite definitions** (100+) for what is essentially a stamp-pattern puzzle.
- **Camera/grid dimension mismatch** complicates click-to-grid mapping.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES.
- Has lives mechanic: NO.
- Has click-to-select: YES.
- Has tag-based grouping: YES.
- Uses ACTION5: NO.
- Uses ACTION6: YES.
- Uses ACTION7: NO.
- Has level data dicts: YES (`kCv`, `cwU`, `elp`).
- Multi-mechanic per level: NO — same stamp mechanic across levels.
- Tutorial level appears solvable by random play: NO.
- Has a depleting resource: YES.
- Has an accumulating resource: YES.
- Sprite shape convention used: mixed.
- HUD position: bottom (within 16x16 viewport).
- Palette size used: ~10.
- Background colour value: 4.
- Padding / letter-box colour value: 4.
- Number of distinct mechanics introduced across levels 1-3: 1 (stamp).
- Number of levels documented: 3.

(End of file.)
