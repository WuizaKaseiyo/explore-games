# g50t — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/g50t/5849a774/g50t.py`
- Lines: 2839
- Class name: `G50t`
- available_actions: `[1, 2, 3, 4, 5]` (UP/DOWN/LEFT/RIGHT, ACTION5=special-ability)
- Number of levels in source: 7
- Number of levels documented in this analysis: 3
- Imports: standard novaengine + numpy + enum.

## Mechanic essence (one sentence)

A small avatar walks across a scrolling board where the entire backdrop slides one cell to the left every two turns, and pressing the four arrow keys nudges the avatar a single cell while ACTION5 fires a context-dependent special ability — the level is solved when the avatar reaches its scrolling-goal flag before the relentlessly-advancing left edge of the world overtakes it.

## Sprite roster

g50t has many sprites with an enum-based tag system (`evgpfjbmvf`). Class hierarchy (`icnqnelege`, `wqqfxozcab`, `evnxdjdwok`, `vyvrqeukpy`, `lqtxaumfed`, `alyzsfkumg`, `yyzqramdhd`, `crfcpstubm`, `ulhhdeoyok`, `pxucxprzhn`, `lapadqkemy`, `jpyajytnzr`, `fdukwsxcoo`, `umziwqcvfy`, `utmhrglxzq`) defines 14 different game-object types beyond the visual sprites.

| tag-group | role |
|---|---|
| `ofihnvwckg` (enum-named) | the scrolling backdrop / world frame |
| various | player avatar, NPCs, hazards, collectibles, walls |

Per-sprite enumeration omitted for brevity; sprites map to the typed game-object hierarchy.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (64, 64).
- Mechanic introduced relative to the previous level: this is the first level — introduces the **walk + scroll** mechanic. The player walks 1 cell per arrow key; the world (`twyixucrqi`) slides 1 cell left every other turn (when `ucorwtereb % 2 == 0`). ACTION5 invokes a context-specific special action via `pmlawcgvcp()`.
- Win: reach the goal flag (`mrzduxdbbk` returns `safkknjslo` flag).
- Lose: the world scrolls past the avatar (`abjneovbvx` checks `-twyixucrqi.x > twyixucrqi.width`) OR the avatar's `zvuxrhnlcb` flag is set (e.g. caught by a hazard).

### Level 2
- `grid_size`: (64, 64). Same mechanic; more obstacles.

### Level 3
- `grid_size`: (64, 64). Same mechanic; further complexity (multiple lanes/hazards).

Levels 4-7 exist but are excluded per skill scope.

## Action handlers

### ACTION1-4 (UP/DOWN/LEFT/RIGHT)
- Trigger: arrow keys.
- Branches: dispatch to `vgwycxsxjz.move(dx, dy)`. Increment `ucorwtereb` (turn counter). Every-other-turn (`tmwgfkaqxj`), the backdrop slides left.

### ACTION5 (special)
- Trigger: ACTION5.
- Branches: dispatch to `vgwycxsxjz.pmlawcgvcp()` — context-specific (e.g. attack, jump, interact).

## HUD widgets

No explicit HUD — `Camera` is initialised with `background=BACKGROUND_COLOR, letter_box=PADDING_COLOR` and no interfaces. Step counter not registered.

## Internal state — exhaustive

| attr | role |
|---|---|
| `vgwycxsxjz` | the player game-object (`qxlodtievc` instance) |
| `ucorwtereb` | turn counter |
| `twyixucrqi` | the scrolling backdrop sprite |
| `qgzorkgosv` | win flag |
| `hctlyapjnq` | lose flag |

## Win condition

Plain English: the player reaches the goal flag, set via `vgwycxsxjz.safkknjslo`.

## Lose condition

Plain English: lose if (a) the backdrop scrolls past the avatar's position, or (b) the avatar's `zvuxrhnlcb` flag is set (hit a hazard).

## Resource economy

- Depleting resource: implicit — the scrolling backdrop's position counts as a "remaining time" indicator.
- Accumulating resource: avatar's progress along the scroll direction.
- Lives mechanic: NO.

## Action-budget signature

- Default budget per level: implicit (the scrolling backdrop's width determines effective budget).
- Decrement rate: 1 backdrop-step per 2 actions.

## Notable code patterns / techniques

- **Class-hierarchy-based game-object system** (`icnqnelege` base, `wqqfxozcab` etc.) — typed entities rather than tag-based dispatch.
- **Enum-based tag system** (`evgpfjbmvf`) — type-safe tag references.
- **Time-based scrolling** — backdrop advances every 2 actions, creating a soft time pressure.
- **No explicit HUD** — game state is conveyed via the scrolling visual itself.

## Anti-patterns / lessons

- **Heavy class hierarchy** — 14+ game-object subclasses. Hard to track behaviour at a glance.
- **Implicit time budget** via scroll position — players must intuit pacing.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: NO (implicit via scroll).
- Has lives mechanic: NO.
- Has click-to-select: NO.
- Has tag-based grouping: YES (enum-based).
- Uses ACTION5: YES.
- Uses ACTION6: NO.
- Uses ACTION7: NO.
- Has level data dicts: UNKNOWN.
- Multi-mechanic per level: NO.
- Tutorial level appears solvable by random play: NO.
- Has a depleting resource: YES (scroll-based time pressure).
- Has an accumulating resource: YES (avatar progress).
- Sprite shape convention used: mixed.
- HUD position: none (no HUD widget registered).
- Palette size used: ~10.
- Background colour value: 0.
- Padding / letter-box colour value: 2.
- Number of distinct mechanics introduced across levels 1-3: 1 (walk+scroll); special abilities vary per level.
- Number of levels documented: 3.

(End of file.)
