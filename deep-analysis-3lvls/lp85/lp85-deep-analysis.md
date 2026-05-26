# lp85 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/lp85/305b61c3/lp85.py`
- Lines: 21429
- Class name: `Lp85`
- available_actions: `[6]` (click only)
- Number of levels in source: ~30+ (the level list is very long)
- Number of levels documented in this analysis: 3
- Imports: standard novaengine + numpy.

## Mechanic essence (one sentence)

A grid of coloured tokens sits inside a Rubik's-cube-like board with a pair of L/R arrow-buttons stuck to every row and every column on the outside, and the player clicks one of those buttons to shift the entire matching row or column one cell in that direction — the level is solved when each token has slid onto a target-tile of its matching style.

## Sprite roster

lp85 has 105 sprites. Key tag-groups:

| tag-group | role |
|---|---|
| `sys_click` + `button_<N>_<L\|R>` | clickable row/column shift buttons (direction encoded in tag suffix) |
| `bghvgbtwcb` | player tokens of type-1 (must overlap `goal`) |
| `fdgmtkfrxl` | player tokens of type-2 (must overlap `goal-o`) |
| `goal` | target squares for `bghvgbtwcb` |
| `goal-o` | target squares for `fdgmtkfrxl` |

The huge file size comes from a comprehensive lookup table (`chmfaflqhy` and `qfvvosdkqr(izutyjcpih)`) precomputing all row/column shifts for every level layout — essentially a giant transition-table for the puzzle's group-theoretic permutations.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (32, 19)
- Level data: `{"StepCounter": 13, ...}` — extremely tight 13-step budget.
- Mechanic introduced relative to the previous level: this is the first level — introduces the **row/column shift** mechanic. Click ACTION6 on a button (tag `button_<row>_<L|R>`) to shift that row or column. Win when every token overlaps its matching goal.

### Level 2
- `grid_size`: (41, 41)
- Level data: `{"StepCounter": 60}`.
- Mechanic: same; larger grid, more tokens, more buttons.

### Level 3
- `grid_size`: (39, 31)
- Level data: `{"StepCounter": 80}`.
- Mechanic: same; non-square grid.

Levels 4+ exist but are excluded per skill scope.

## Action handlers

### ACTION6 (click)
- Trigger: click on a button-tagged sprite.
- Branches: parse tag `button_<row>_<L|R>` to determine row/column index and direction; look up the precomputed shift via `chmfaflqhy`; apply the position swaps to all affected sprites.

## HUD widgets

`fonypcnqmf` — depleting bar HUD.

## Internal state — exhaustive

`uopmnplcnv` (precomputed transition table), `afhycvvjg` (clickable buttons), `kshrbnrfkopq`/`papamfmeoa` (grid dimensions).

## Win condition

`khartslnwa()`: for every `bghvgbtwcb` token, the cell at (token.x+1, token.y+1) must contain a `goal`-tagged sprite. Similarly for `fdgmtkfrxl` and `goal-o`. All match → win.

## Lose condition

Step counter hits 0 (`toxpunyqe.xsfawdkqoi()` returns False).

## Resource economy

- Depleting resource: YES — step counter (13, 60, 80 for L1-3).
- Accumulating resource: tokens-on-goal count.
- Lives mechanic: NO.

## Action-budget signature

- Default budget per level: per-level via `level.get_data("StepCounter")`. L1=13, L2=60, L3=80.
- Whether budget tightens or shifts across levels 1-3: variable.
- Decrement rate: 1 per click.
- Refill mechanism: NONE.

## Notable code patterns / techniques

- **Precomputed transition table** for row/column shifts — encoded as ~20,000 lines of static data. Eliminates runtime computation but dramatically inflates source size.
- **Tag-encoded button metadata** (`button_<row>_<L|R>`): row index and direction parsed from tag string.
- **Two-token-class win predicate**: separate goals for two different token types.

## Anti-patterns / lessons

- **Massive source file** (21k+ lines) due to precomputed tables — a generated game should compute shifts at runtime.
- **Tag string parsing** for behavioural metadata is fragile.
- **Tight L1 budget (13 steps)** — very unforgiving tutorial.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES.
- Has lives mechanic: NO.
- Has click-to-select: YES.
- Has tag-based grouping: YES (`sys_click`, `button_*`, `bghvgbtwcb`, `fdgmtkfrxl`, `goal`, `goal-o`).
- Uses ACTION5: NO.
- Uses ACTION6: YES.
- Uses ACTION7: NO.
- Has level data dicts: YES (`StepCounter`, `level_name`).
- Multi-mechanic per level: NO — same row/column shift mechanic.
- Tutorial level appears solvable by random play: NO (tight 13-step budget rules this out).
- Has a depleting resource: YES.
- Has an accumulating resource: YES.
- Sprite shape convention used: mixed.
- HUD position: bottom (camera 16x16 viewport scrolls over larger grid).
- Palette size used: ~12.
- Background colour value: 4.
- Padding / letter-box colour value: 3.
- Number of distinct mechanics introduced across levels 1-3: 1 (row/column shift).
- Number of levels documented: 3.

(End of file.)
