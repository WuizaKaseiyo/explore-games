# m0r0 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/m0r0/dadda488/m0r0.py`
- Lines: 908
- Class name: `M0r0`
- available_actions: `[1, 2, 3, 4, 5, 6]` (UP/DOWN/LEFT/RIGHT, ACTION5 is registered but the source never branches on it, ACTION6 = click)
- Number of levels in source: 6
- Number of levels documented in this analysis: 3
- Imports: `NovaBaseGame`, `Camera`, `GameAction`, `InteractionMode`, `Level`, `RenderableUserDisplay`, `Sprite` from `novaengine`; `numpy as np`.

## Mechanic essence (one sentence)

Two glowing pawns float through a winding maze as mirror-image siblings — pressing UP moves both up, but pressing LEFT pushes one left while pulling the other right — and the level is solved when each mirrored pair walks into the same cell and merges, while spike-tiles slap them back to where they started and clickable post-stones in the path can be selected and dragged aside one at a time to clear the route.

## Sprite roster

| sprite (obfuscated) | dims | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| `cvcer` | 1x1 | 9 | sys_click, nhiae | (default) | YES | (default) | YES | post-stone — clickable wall that the player can pick up and slide aside (L3+) |
| `dfnuk-qeazm` | 1x3 | 15 | (default) | (default) | YES | (default) | YES | white-purple coloured wall (level 5+) |
| `dfnuk-raixb` | 1x3 | 14 | (default) | (default) | YES | (default) | YES | green coloured wall (level 5+) |
| `dfnuk-ujcze` | 1x3 | 12 | (default) | (default) | YES | (default) | YES | purple coloured wall (level 5+) |
| `hnutp-qeazm` | 1x1 | 15 | (default) | (default) | YES | (default) | YES | white-purple key trigger (level 5+) |
| `hnutp-raixb` | 1x1 | 14 | (default) | (default) | YES | (default) | YES | green key trigger (level 5+) |
| `hnutp-ujcze` | 1x1 | 12 | (default) | (default) | YES | (default) | YES | purple key trigger (level 5+) |
| `jggua-Level1` | 13x13 | 0, -1 | jggua | (default) | YES | (default) | YES | maze wall sprite used by L3 |
| `jggua-Level2` | 15x15 | 0, -1 | jggua | (default) | YES | (default) | YES | maze wall sprite (level 5+) |
| `jggua-Level3` | 16x16 | 0, -1 | jggua | (default) | YES | (default) | YES | maze wall sprite (defined but never placed) |
| `jggua-Level4` | 16x16 | 0, -1 | jggua | (default) | YES | (default) | YES | maze wall sprite (defined but never placed) |
| `jggua-Level5` | 16x16 | 0, -1 | jggua | (default) | YES | (default) | YES | maze wall sprite (defined but never placed) |
| `jggua-Level6` | 11x11 | 0, -1 | jggua | (default) | YES | (default) | YES | maze wall sprite used by L1 (rotated 180°) |
| `jggua-Level7` | 11x11 | 0, -1 | jggua | (default) | YES | (default) | YES | maze wall sprite (defined but never placed) |
| `jggua-Level8` | 14x14 | 0, -1 | jggua | (default) | YES | (default) | YES | maze wall sprite (defined but never placed) |
| `jggua-Level9` | 11x11 | 0, -1 | jggua | (default) | YES | (default) | YES | maze wall sprite (level 4+) |
| `jggua-Level10` | 13x13 | 0, -1 | jggua | (default) | YES | (default) | YES | maze wall sprite (defined but never placed) |
| `jggua-Level11` | 9x10 | 0, -1 | jggua | (default) | YES | (default) | YES | maze wall sprite used by L2 |
| `qzfkx-kncqr-crkfz` | 1x1 | 10 | sys_click | 2 | YES | (default) | YES | mirror-orb (vertical-and-horizontal flip pair, level 5+) |
| `qzfkx-kncqr-idtiq` | 1x1 | 10 | sys_click | 2 | YES | (default) | YES | mirror-orb (vertical flip pair, level 5+) |
| `qzfkx-ubwff-crkfz` | 1x1 | 10 | sys_click, pxwnx | 2 | YES | (default) | YES | mirror-orb (horizontal flip — used in every L1-3 level) |
| `qzfkx-ubwff-idtiq` | 1x1 | 10 | sys_click, pxwnx | 2 | YES | (default) | YES | mirror-orb (no-flip baseline — used in every L1-3 level) |
| `wyiex` | 1x1 | 8 | wyiex | (default) | YES | (default) | YES | hazard tile (orange spike) |

### `cvcer` — clickable post-stone (L3 only in scope)
- Pixel pattern: single-cell palette-9 (blue).
- Where it appears: L3 (3 copies at (1,3), (6,2), (8,6)). Also L4 and L6 (out of scope).
- Role: in `step()`, clicking a cvcer flips `self.vmcbq = False` and binds `self.cfwgj = cvcer`, after which arrow keys move that single cvcer instead of moving the mirror-orbs. `cvcer` carries the `nhiae` tag, which is read by `bpcdxdwyxx` (orb mover) as a barrier — so until you slide the cvcer aside, the orbs cannot pass through its cell. The HUD `kyrgqgqaes` paints a 5×5 outline around each cvcer at its scaled position, drawing it as a hollow square in palette 5 (the global background colour).
- Visual-vs-functional read: at-rendered-scale, the HUD draws cvcer as a hollow 5×5 *outline* in palette 5 against whichever palette the level's `npwxa` data dyes the floor (15+8 in L3). On its own the sprite is just a single palette-9 dot — without the HUD overlay a player would see only a dot. **The functional role (movable wall) is conveyed entirely by the HUD overlay**, not by the sprite itself.
  - At-rendered-scale shape: hollow square (HUD-painted overlay).
  - Palette signature: 9 (raw sprite) + 5 (HUD outline). Shared with no other game sprite.
  - Nearest-other-sprite check: the orbs `qzfkx-*` are also single-cell sprites, but they're palette-10 and HUD-rendered as solid filled scaled squares; the cvcer is hollow.
- Visual contrast notes: against the L3 dyed background (palette 15 split with 8), the palette-5 hollow square stands out; the inner palette-9 dot at the centre tells the player which cell is the actual hit-target.

### `dfnuk-qeazm` — palette-15 vertical wall (level 5+)
- Pixel pattern: 1×3 column of palette-15.
- Where it appears: not placed in L1-3 (level 5).
- Role: out of scope.
- Visual-vs-functional read: simple vertical bar; palette 15. Nearest-other: `dfnuk-raixb`, `dfnuk-ujcze` — same shape, different colour.
- Visual contrast notes: out of scope.

### `dfnuk-raixb` — palette-14 vertical wall (level 5+)
- Pixel pattern: 1×3 column of palette-14.
- Where it appears: not placed in L1-3.
- Role: out of scope.
- Visual-vs-functional read: as `dfnuk-qeazm` above, different colour (green).
- Visual contrast notes: out of scope.

### `dfnuk-ujcze` — palette-12 vertical wall (level 5+)
- Pixel pattern: 1×3 column of palette-12.
- Where it appears: not placed in L1-3.
- Role: out of scope.
- Visual-vs-functional read: as `dfnuk-qeazm` above, different colour (purple).
- Visual contrast notes: out of scope.

### `hnutp-qeazm` — palette-15 single-cell key (level 5+)
- Pixel pattern: 1×1 of palette-15.
- Where it appears: not placed in L1-3.
- Role: out of scope.
- Visual-vs-functional read: single dot; palette 15. Nearest-other: `qzfkx-*` orbs are also single dots but palette-10 and HUD-painted at scale.
- Visual contrast notes: out of scope.

### `hnutp-raixb` — palette-14 single-cell key (level 5+)
- Pixel pattern: 1×1 of palette-14.
- Where it appears: not placed in L1-3.
- Role: out of scope.

### `hnutp-ujcze` — palette-12 single-cell key (level 5+)
- Pixel pattern: 1×1 of palette-12.
- Where it appears: not placed in L1-3.
- Role: out of scope.

### `jggua-Level1` — 13x13 maze with multiple corridors (L3)
- Pixel pattern: 13×13. Mostly palette-0 (black) outline forming a closed boundary at row 0, row 12, col 0, col 12; interior carved into corridor cells (palette -1 transparent) with vertical and horizontal palette-0 dividers creating 4-5 distinct rooms connected by narrow passages.
- Where it appears: L3 only (1 copy, default position (0,0)).
- Role: maze wall against which orbs collide and are blocked.
- Visual-vs-functional read: at-rendered-scale, palette-0 cells form solid black walls and palette -1 cells reveal the dyed background colour underneath; the maze reads as a black labyrinth on a coloured floor. Tag `jggua` is read by `bpcdxdwyxx` to reject orb movements that collide with any cell of the wall sprite.
- Visual contrast notes: solid black against any non-black background; the corridors take their colour from `npwxa` (palette 15+8 for L3 — purple-white split with orange).

### `jggua-Level2` — 15x15 maze (level 5+)
- Pixel pattern: 15×15 with multiple long corridors.
- Where it appears: L5 only (out of scope).

### `jggua-Level3` — 16x16 maze (defined but unused)
- Pixel pattern: 16×16, dense corridor pattern.
- Where it appears: never placed in any level.
- Role: dead sprite.

### `jggua-Level4` — 16x16 maze (defined but unused)
- Pixel pattern: 16×16 with diagonal labyrinth segments.
- Where it appears: never placed.
- Role: dead sprite.

### `jggua-Level5` — 16x16 maze (defined but unused)
- Pixel pattern: 16×16 organic-curve labyrinth.
- Where it appears: never placed.
- Role: dead sprite.

### `jggua-Level6` — 11x11 maze with central diamond (L1)
- Pixel pattern: 11×11. Closed boundary at rows 0, 10 and cols 0, 10 (palette-0). Centre forms a diamond/spiral pattern with palette-0 dividers; corridors are palette -1.
- Where it appears: L1 only (1 copy, default position, rotated 180°).
- Role: maze wall for L1.
- Visual-vs-functional read: at-rendered-scale, palette-0 against the dyed L1 background (palette 11+12 split — yellow-purple); reads as black corridors. Rotation 180° flips the asymmetric diamond.

### `jggua-Level7` — 11x11 maze (defined but unused)
- Pixel pattern: 11×11, simple grid pattern.
- Where it appears: never placed.

### `jggua-Level8` — 14x14 maze (defined but unused)
- Pixel pattern: 14×14, large central hub with branching arms.
- Where it appears: never placed.

### `jggua-Level9` — 11x11 maze (level 4+)
- Pixel pattern: 11×11.
- Where it appears: L4 only (out of scope).

### `jggua-Level10` — 13x13 maze (defined but unused)
- Pixel pattern: 13×13, comb-pattern of horizontal corridors.
- Where it appears: never placed.

### `jggua-Level11` — 9x10 maze (L2)
- Pixel pattern: 9 cols × 10 rows. The inverse of typical mazes — most cells palette-1 (transparent / corridor) with a few palette-0 dividers forming a cross pattern at col 4 and row 3-4.
- Where it appears: L2 only (1 copy at (2, 0)).
- Role: maze wall for L2.
- Visual-vs-functional read: simpler structure than the other mazes — mostly open with a single vertical wall down col 4.
- Visual contrast notes: dyed background palette 6+15 (magenta-pink + white) for L2.

### `qzfkx-kncqr-crkfz` — single palette-10 mirror-orb (level 5+)
- Pixel pattern: 1×1 palette-10.
- Where it appears: not placed in L1-3.
- Role: out of scope (vertical-AND-horizontal flip mirror partner).
- Visual-vs-functional read: identical at the sprite level to the three other `qzfkx-*` orbs; the differences are entirely encoded in the obfuscated *name*. Tag-discrimination would not help — only the substring matching in `step()` (`"kncqr-idtiq"`, `"ubwff-crkfz"`, etc.) tells these orbs apart. Player sees only "another palette-10 dot".

### `qzfkx-kncqr-idtiq` — single palette-10 mirror-orb (level 5+)
- Pixel pattern: 1×1 palette-10.
- Where it appears: not placed in L1-3.
- Role: out of scope (vertical flip mirror partner).

### `qzfkx-ubwff-crkfz` — single palette-10 mirror-orb (horizontal-flip pair) (L1, L2, L3)
- Pixel pattern: 1×1 palette-10.
- Where it appears: every L1-3 level (1 copy each, positioned at (7,9), (8,1), (8,10)).
- Role: one of the two mirror-orbs that the player controls indirectly via arrow keys. Its motion is mirrored across the vertical axis: when the player hits `(dx, dy)`, this orb moves `(-dx, dy)`. So pressing LEFT moves it RIGHT, RIGHT moves it LEFT, UP moves it UP, DOWN moves it DOWN.
- Visual-vs-functional read: at-rendered-scale, the sprite renders as a single palette-10 (cyan) dot scaled up by `kyrgqgqaes` to fill its scaled cell — but the HUD itself does not draw orbs explicitly; the engine renders palette-10 wherever it's visible. The `pxwnx` tag is checked in the HUD to *skip* drawing checkerboard hazards on top of the orb's cell. **Visually identical to its `idtiq` sibling**: only the name encodes which orb mirrors. A player must learn by trial which one mirrors how.
  - At-rendered-scale shape: single scaled-up cell of palette 10 (cyan).
  - Palette signature: 10. Shared only with the other three `qzfkx-*` orbs.
  - Nearest-other-sprite check: `qzfkx-ubwff-idtiq` — its mirror partner; visually identical except by spatial relationship.
- Visual contrast notes: cyan-10 stands out against any of the L1-3 dyed backgrounds (yellow-purple, magenta-white, purple-orange); always salient.

### `qzfkx-ubwff-idtiq` — single palette-10 mirror-orb (no-flip baseline) (L1, L2, L3)
- Pixel pattern: 1×1 palette-10.
- Where it appears: every L1-3 level (1 copy each, positioned at (3,9), (4,1), (4,10)).
- Role: the "anchor" mirror-orb. When the player hits `(dx, dy)`, this orb moves `(dx, dy)` — straight motion with no flip. Its `crkfz` partner mirrors across the vertical axis.
- Visual-vs-functional read: identical at the sprite level to `crkfz`; the role asymmetry is entirely behavioural and only revealed by playing.

### `wyiex` — palette-8 hazard spike (L2, L4, L6 in source)
- Pixel pattern: 1×1 palette-8 (orange).
- Where it appears: L2 only in scope (29 copies at various cells along the bottom rows). Heavy use in L4 (out of scope) and L6 (out of scope).
- Role: hazard. When an orb's post-move position equals a wyiex cell, the orb name is appended to `self.yvmbd` and a 7-tick blink animation runs (alternating colour palette 11/10) before all `sys_click` sprites snap back to their `myxvz` start positions.
- Visual-vs-functional read: at-rendered-scale, the HUD draws each wyiex as a palette-5 *checkerboard* pattern across its scaled cell (every other pixel where `(x+y)%2==1`), unless that cell already contains a `pxwnx`-tagged orb (in which case the wyiex is skipped). So visually, hazards look like dotted/striped patches, distinguishing them from solid orbs.
  - At-rendered-scale shape: checkerboard cell.
  - Palette signature: 8 + 5 (HUD overlay).
  - Nearest-other-sprite check: distinct — no other sprite uses checkerboard rendering. The cvcer is hollow square; the orbs are solid squares; wyiex is checkerboard.
- Visual contrast notes: checkerboard pattern conveys "danger/caution" stripe convention well; against the dyed background it reads as a noisy/textured cell.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (11, 11)
- Number of sprites placed: 3
- Composition by role: 1 maze (`jggua-Level6` rotated 180°), 2 mirror-orbs (`qzfkx-ubwff-idtiq` at (3,9), `qzfkx-ubwff-crkfz` at (7,9)).
- Level data: `{"npwxa": [11, 12]}` — the HUD `kyrgqgqaes` reads this and dyes every palette-0 cell of the rendered frame as a 32-px split: left half palette 11 (yellow), right half palette 12 (purple). (When all 4 orbs are unpaired, the dyer uses a 4-quadrant split instead, but L1 has only 2 orbs total, so always 2-strip.)
- Spawn position(s): no avatar; both orbs start at row 9 — `idtiq` at col 3, `crkfz` at col 7. The maze pillar is at column 4-5 between them.
- Per-cell layout: 11×11 grid. Maze occupies (0,0)..(10,10) with row 0 / row 10 / col 0 / col 10 forming the closed border, and interior dividers carving rooms; orbs are at (3, 9) and (7, 9), both in the bottom corridor.
- Mechanic introduced relative to the previous level: this is the first level — introduces the **mirror-orb** mechanic. Two orbs move in vertical lock-step (same `dy`) but opposite horizontally (`crkfz` flips `dx` sign). Pressing LEFT pulls them apart, RIGHT brings them together; UP and DOWN move both the same direction. Walls (`jggua` tag) block individual orb moves — collision is resolved per-orb. When two orbs end up on the same cell, both are added to `self.fqunj` and set INTANGIBLE; when no unpaired orb remains, `next_level()` fires.
- Specific challenge: the maze pillar between the two orbs forces the player to navigate the orbs around it before they can meet in the middle. Because both orbs move in the same direction simultaneously, the player must find a position where pressing LEFT or RIGHT (which pushes them together horizontally) doesn't immediately push one orb into a wall. Likely solution path: move both UP first, threading them through the maze's central diamond, then meet in the middle row.
- Estimated optimal action count: ~6-10.

### Level 2
- `grid_size`: (13, 13)
- Number of sprites placed: 32
- Composition by role: 1 maze (`jggua-Level11` at (2, 0)), 2 mirror-orbs, 29 hazards (`wyiex` at scattered cells along the bottom rows: (5,5), (5,6), (5,7), (5,8), (12,8), (11,8), (10,8), (9,8), (8,8), (4,8), (2,8), (1,8), (0,8), (4,12), (3,12), (2,12), (1,12), (0,12), (9,12), (8,12), (7,12), (6,12), (5,12), (12,12), (11,12), (10,12)).
- Level data: `{"npwxa": [6, 15]}` — palette 6 (magenta) split with 15 (white-purple). Dyer paints the left 32 columns palette-6, right 32 cols palette-15.
- Spawn position(s): both orbs at row 1 — `idtiq` at col 4, `crkfz` at col 8. Maze pillar at col 4 between them.
- Per-cell layout: 13×13 grid. Maze occupies cols 2-10, rows 0-9 (sized 9×10). Hazards form two horizontal bands across rows 8 and 12.
- Mechanic introduced relative to L1: **Hazards** — `wyiex` tiles. If an orb's post-move position lands on a wyiex tile, the orb is added to `self.yvmbd` and the entire `sys_click` set is reset to its level-start positions (via `myxvz` snapshot) after a 7-tick blink animation that re-colours the hazard-hit orb(s) palette-11 then palette-10 alternately. New tag `wyiex` checked in `step()` for hazard detection.
- Specific challenge: the orbs must avoid the two hazard rows while navigating to a common cell. The lower hazard band is densely packed; only narrow safe corridors exist. Player must route both orbs through the hazard-free cells.
- Estimated optimal action count: ~10-16.

### Level 3
- `grid_size`: (13, 13)
- Number of sprites placed: 6
- Composition by role: 1 maze (`jggua-Level1`), 3 movable post-stones (`cvcer` at (1,3), (6,2), (8,6)), 2 mirror-orbs (`ubwff-idtiq` at (4,10), `ubwff-crkfz` at (8,10)).
- Level data: `{"npwxa": [15, 8]}` — palette 15 split with 8.
- Spawn position(s): both orbs at row 10 — `idtiq` at col 4, `crkfz` at col 8. Three cvcer post-stones scattered at (1,3), (6,2), (8,6).
- Per-cell layout: 13×13. Maze (`jggua-Level1`) occupies cols 0-12 rows 0-12 with multiple chambers connected by narrow passages.
- Mechanic introduced relative to L2: **Movable click-walls** (`cvcer` with `nhiae` tag). cvcer cells block orb movement (`bpcdxdwyxx` rejects any orb move that would collide with a cvcer). The player can click a cvcer to flip `vmcbq=False` and bind `cfwgj` to that cvcer; arrow keys then move *just the cvcer* (using `try_move_sprite`) instead of the orbs. Re-clicking the cvcer or clicking outside any cvcer flips `vmcbq=True` and restores normal orb-mirror motion. So in L3, the player alternates between "drag a wall aside" and "advance the orbs".
- Specific challenge: 3 walls scattered through the maze block the orb routes; the player must select each wall in turn, slide it out of the way, then return to orb-mode and advance. Requires planning the order of wall removals to avoid dead-ends.
- Estimated optimal action count: ~20-30 (3 walls × ~3 clicks-and-moves + ~10 orb-moves).

Levels 4, 5, 6 exist but are excluded per skill scope.

## Action handlers

### ACTION1 / ACTION2 / ACTION3 / ACTION4 (UP/DOWN/LEFT/RIGHT)
- Trigger: `self.action.id == GameAction.ACTION1/2/3/4`.
- Branches inside `step()`:
  - First the global guards: if `self.zgdmc >= 0` (a hazard-blink animation is in progress), advance the animation tick — re-colour all `self.yvmbd` orbs to palette 11 (even ticks `< 5`) or palette 10 otherwise, increment `zgdmc`; when `zgdmc > 6`, snap every `myxvz`-recorded sprite back to its start (x, y), reset state, and `complete_action()`. Return without processing the click direction.
  - Otherwise update step-counter HUD (`self.tmbjb.ekyafbirsw(150 - self._action_count)`); if `_action_count > 150`, call `lose()` and return.
  - Compute (dx, dy) from action ID (UP→(0,-1), DOWN→(0,1), LEFT→(-1,0), RIGHT→(1,0)). Call `self.set_placeable_sprite(None)` to release any cvcer drag-bind.
  - **Branch A (cvcer-drag mode)**: if `self.cfwgj` is set AND `self.vmcbq` is False, attempt a single move on the bound cvcer: bound-check against grid, then `try_move_sprite(self.cfwgj, dx, dy)` (engine method, presumably checks collisions against other sprites). Then `dssyxgdgjg()` (out-of-scope side effect; does nothing in L3 because no `dfnuk-*`/`hnutp-*` sprites are present). `complete_action()` and return.
  - **Branch B (mirror-orb mode)**: `self.vmcbq` is True. Build the list of unpaired orbs (`dawfcldxmo`); snapshot their current positions into `self.bwyvb`. For each orb, compute its mirrored direction (`ubwff-idtiq`→(dx,dy), `ubwff-crkfz`→(-dx,dy), `kncqr-idtiq`→(dx,-dy), `kncqr-crkfz`→(-dx,-dy)). Call `bpcdxdwyxx(sprite, mirrored_dx, mirrored_dy)` per orb — moves it one cell in the mirrored direction unless any of these collide: bounds, `jggua`-tagged maze wall, `nhiae`-tagged cvcer post-stone, any collidable `dfnuk-*` coloured wall.
  - After all orbs have attempted their mirrored move, check each moved orb against `wyiex`-tagged hazards at its new cell; any hit is appended to `self.yvmbd`. If `yvmbd` is non-empty, set `zgdmc = 0` (start blink animation) and return without `complete_action()` — the next tick continues the animation.
  - Otherwise check for **swap-merging**: if two orbs that started 1 cell apart on the same row/col now occupy each other's previous cell (i.e. they passed through each other during the move), set both to the midpoint cell — modelled as integer-divide of the sum of their post-move coords.
  - Then check for **co-location**: build a dict of (x, y) → list of orbs at that cell; for any cell with 2 orbs, add both names to `self.fqunj` and `set_interaction(InteractionMode.INTANGIBLE)`. For 3+ orbs in one cell, only the first 2 pair; the rest are reverted to their `bwyvb` start position.
  - Call `dssyxgdgjg()` (recomputes wall removability based on key-cell coverage; no-op in L1-3).
  - Count remaining unpaired orbs `tttipukmnd`; if zero, `next_level()`. Then `complete_action()`.
- State mutations: read `self.cfwgj`, `self.vmcbq`, `self.fqunj`, `self.zgdmc`, `self.action.id`, `self.action.data`, `self._action_count`, `self.current_level`. Written: `self.bwyvb`, `self.fqunj`, `self.yvmbd`, `self.zgdmc`, every orb's position, every orb's interaction mode, `self.tmbjb.current_steps`.
- Side effects on sprites: orbs `move()`, `set_position()`, `set_interaction(REMOVED|INTANGIBLE|TANGIBLE)`, `color_remap(None, 11)` / `color_remap(None, 10)` during blink animation.
- Engine effects: `next_level()` when all orbs paired; `lose()` if action count exceeds 150.
- Pre-conditions / gating: rejected silently if movement would push the orb out of grid (`bpcdxdwyxx` returns early); rejected silently if collision with maze wall, post-stone, or coloured wall.

### ACTION5
- Trigger: `self.action.id == GameAction.ACTION5`.
- Branches: ACTION5 is registered in `available_actions=[1,2,3,4,5,6]` but `step()` has no `if self.action.id == GameAction.ACTION5` branch. The (dx, dy) computation only matches actions 1-4, so for ACTION5 both `ujqjq` and `bpjkc` remain 0. Then the cvcer-drag path is taken if `cfwgj` is set, and `bpcdxdwyxx(self.cfwgj, 0, 0)` does nothing meaningful (no movement). The orb-branch enters with (0, 0) and likewise does nothing. Net effect: ACTION5 is a no-op except for incrementing `_action_count`.
- State mutations: `_action_count` (engine) is incremented; `tmbjb.current_steps` updated next tick.
- Engine effects: none direct.
- Pre-conditions / gating: none — but the action is effectively wasted budget.

### ACTION6 (click)
- Trigger: `self.action.id == GameAction.ACTION6`.
- Branches: read (x, y) from `action.data`, convert via `camera.display_to_grid`. If conversion fails, fall through. Call `current_level.get_sprite_at(grid_x, grid_y, tag="sys_click")` to find the topmost sys_click sprite under the click. If the hit is a `cvcer`: set `vmcbq = False`, recolour every unpaired orb to palette-1 (dim them visually), recolour any previously-bound cvcer back to palette-9, bind the new one to `self.cfwgj`, call `set_placeable_sprite(self.cfwgj)`, recolour the new cvcer to palette-11 (highlight). If the hit is anything else (or nothing): set `vmcbq = True`, recolour orbs back to palette-10, recolour any previously-bound cvcer back to palette-9, clear `self.cfwgj`. Always `complete_action()` and return.
- State mutations: read `self.action.data`, `self.cfwgj`, `self.fqunj`, `self.current_level`. Written: `self.cfwgj`, `self.vmcbq`, every orb's `color_remap`, possibly cvcer's `color_remap`. Calls engine `set_placeable_sprite`.
- Side effects on sprites: cvcer recoloured to palette 11 on selection / palette 9 on deselect; orbs recoloured to palette 1 on cvcer-drag-mode entry / palette 10 on exit.
- Engine effects: none direct.
- Pre-conditions / gating: clicks off-frame are silent no-ops. Clicks on already-paired orbs are ignored (since `fqunj`-listed orbs return their sprites with `interaction=INTANGIBLE` and would not be returned by `get_sprite_at(..., tag="sys_click")`).

## HUD widgets

### `lradlpwbhu` — top-and-bottom step bars
- Class name (obfuscated): `lradlpwbhu`.
- Render-pixel range: row 0 (entire 64-wide width) and row 63 (entire width). Two thin horizontal strips at the very top and bottom of the frame.
- What value it displays: `self.current_steps / self.fehzjtpngn` — proportion of step budget remaining (numerator counts down; denominator is 150).
- Visual style: row 0 is a depleting bar — palette-5 (background) cells fill from the **left** for `dilxnftulx` cells, and palette-0 (black) cells fill the **right**. Row 63 is the mirror — palette-5 fills from the **right** (`63 - x < dilxnftulx`) and palette-0 from the left. So as time passes, the palette-5 region shrinks from both ends inward toward the centre, while palette-0 expands.
- Update points: `ekyafbirsw` is called from (a) `M0r0.on_set_level` (line 679) and (b) the very first executable line of `step()` (line 709) on every action that's not within a blink animation.
- Where it is registered: instantiated in `__init__` and added via `self._camera.replace_interface([self.erwkb, self.tmbjb])` at line 673 (after `super().__init__`).

### `kyrgqgqaes` — background-dyer + cvcer-outline + wyiex-checkerboard overlay
- Class name (obfuscated): `kyrgqgqaes`.
- Render-pixel range: every cell of the 64×64 frame that contains palette-0 (the black mask), plus scaled-up cells corresponding to cvcer and wyiex sprite positions.
- What value it displays: composite. Three overlays:
  1. The pair of palette colours from `level.data["npwxa"]` (e.g. `[11, 12]`) is split across the 64×64 frame: when 4 orbs are unpaired (only happens at L5+) it's a 4-quadrant split (`color1` top-left and bottom-right, `color2` top-right and bottom-left); otherwise it's a vertical 2-strip split (`color1` left half cols 0-31, `color2` right half cols 32-63). Every palette-0 (background-mask) cell of the frame is replaced with the corresponding split cell.
  2. For every visible cvcer, a 5x5 (or `scale` × `scale`) hollow square outline is drawn in palette-5 around the cvcer's grid cell after rescaling.
  3. For every wyiex *not* covered by an orb (`pxwnx`-tagged), a checkerboard pattern (palette-5 at every cell where `(x+y) % 2 == 1`) is drawn over the scaled cell.
- Visual style: the dyer is a flat 2- or 4-quadrant fill; cvcer outlines are 1-px-wide hollow squares; wyiex is checkerboard.
- Update points: every render — runs every frame regardless of action. The dyer reacts to `level.data["npwxa"]` (which only changes at level transitions) and to `len(unpaired orbs)` (which decreases as orbs pair up — the dyer flips from 2-strip to 4-quadrant or vice versa).
- Where it is registered: instantiated in `__init__` as `self.erwkb = kyrgqgqaes(self)` and added via `self._camera.replace_interface([self.erwkb, self.tmbjb])`. Note: this is the FIRST interface in the list, so it renders before the step-counter; the step-counter at row 0/63 paints over the corner pixels of the dyer.

## Internal state — exhaustive

| attr (obfuscated) | semantic name | type | initial value | written by | read by | role |
|---|---|---|---|---|---|---|
| `bwyvb` | pre_move_orb_positions | `dict[str, tuple[int, int]]` | `{}` | `__init__`, `on_set_level`, `step` (orb branch) | `step` (swap-merge check, revert-on-overcrowd) | snapshot of every unpaired orb's (x, y) just before the current arrow-key dispatch; used by the swap-merge logic to detect the case where two orbs passed through each other in opposite mirrored directions, and by the overcrowd path to revert orbs that stack 3+ deep |
| `fqunj` | paired_orb_names | `set[str]` | `set()` | `__init__`, `on_set_level`, `step` (orb branch) | `step` (orb branch and HUD), `dssyxgdgjg`, `kyrgqgqaes.render_interface` | the set of orb names that have already been paired (and made INTANGIBLE); used to filter "remaining unpaired" orbs in every iteration |
| `erwkb` | background_dyer_HUD | `kyrgqgqaes` | `kyrgqgqaes(self)` | `__init__` | camera interface render | renders the dual-colour background dye + cvcer outlines + wyiex checkerboard |
| `tmbjb` | step_counter_HUD | `lradlpwbhu` | `lradlpwbhu(150)` | `__init__`, `on_set_level`, `step` | camera interface render | renders the top+bottom step bar |
| `cfwgj` | dragged_cvcer | `Sprite \| None` | None | `__init__`, `on_set_level`, `step` (click branch) | `step` (cvcer-drag branch and click branch) | the currently-bound cvcer (post-stone) being dragged; non-None ⇒ `vmcbq` must be False |
| `vmcbq` | mirror_orb_mode | bool | True | `__init__`, `on_set_level`, `step` (click branch) | `step` (cvcer-drag and orb branches) | True ⇒ arrow keys move all unpaired orbs in mirrored fashion; False ⇒ arrow keys move just `self.cfwgj` |
| `yvmbd` | hazard_hit_orbs | `list[Sprite]` | `[]` | `on_set_level`, `step` (orb branch) | `step` (blink animation branch) | orbs that landed on a wyiex this tick — kept until the blink animation finishes |
| `zgdmc` | hazard_blink_tick | int | -1 | `on_set_level`, `step` (orb branch + blink branch) | `step` (every entry — gates all other logic) | -1 ⇒ idle; 0..6 ⇒ blink animation tick; >6 ⇒ snap-back-and-reset |
| `myxvz` | sys_click_initial_positions | `list[tuple[Sprite, int, int]]` | `[]` | `on_set_level` | `step` (blink-end branch) | snapshot of every sys_click sprite's (sprite, x, y) at level start — used by the hazard reset to restore positions |
| (inherited) `_action_count` | step count | int | 0 | engine | `step` (every entry) | counts up; compared against 150 for lose check |

## Win condition

Plain English: the level wins when every mirror-orb has been "paired" with another orb at the same cell. Specifically: every name from the four `qzfkx-*` candidates that was actually placed in the level must end up in `self.fqunj` (the set of orbs successfully merged with a partner).

Literal condition: at the bottom of the orb-branch in `step()` (line 847-849):
```python
tttipukmnd = sum(1 for name, sprite in dawfcldxmo
                 if name not in self.fqunj
                 and sprite.interaction != InteractionMode.INTANGIBLE)
if tttipukmnd == 0:
    self.next_level()
```

The same predicate applies to L1, L2, L3 (only `ubwff-crkfz` and `ubwff-idtiq` are placed in each, so the predicate reduces to "both ubwff orbs paired").

## Lose condition

Plain English: lose if the action count exceeds 150 without solving the level.

Literal condition: at line 710-713, after step-counter HUD update:
```python
if self._action_count > 150:
    self.lose()
    self.complete_action()
    return
```

There is no other lose path. Hazards (wyiex) only reset orb positions; they don't directly trigger `lose()`. The action budget plus repeated hazard hits is the lose-flow.

## Resource economy

- Depleting resource (energy / step counter / lives): YES — 150-step budget per level, displayed as the dual top+bottom bar (`lradlpwbhu`), decremented 1 per action by the engine, threshold 150 triggers `lose()`. Hazard hits do NOT deplete extra steps beyond the action that caused the hit.
- Accumulating resource (collected items, score, sequence progress): YES — the `self.fqunj` set accumulates paired-orb names. As orbs pair, the set grows; when it equals the placed-orb count, `next_level()` fires. There is no numeric score; progress is binary per orb.
- Lives mechanic (respawn cost): NO. Hazard hits reset orbs to start positions but do not consume any "life" counter. The same level can be re-attempted within the same 150-step budget.
- Resource interaction with win/lose: step-counter is the sole lose trigger; pair-set completeness is the sole win trigger. They are independent: running out of steps cannot win the level, and pairing all orbs ends the level immediately regardless of remaining steps.

## Action-budget signature

- Default budget per level: 150 (`lradlpwbhu(fehzjtpngn=150)` in `__init__`).
- Whether budget tightens or shifts across levels 1-3: NO. `tmbjb.ekyafbirsw(150)` is called in `on_set_level` for every level.
- Per-level vs. per-environment: per-level (engine resets `_action_count` per level).
- Decrement rate per action: 1 per action. Even no-op actions (clicks that miss any sprite, ACTION5) consume 1 step. Hazard-blink animation ticks do NOT increment `_action_count` — they're handled by the early-return branch (`if self.zgdmc >= 0`) before `complete_action()`.
- Refill mechanism: NONE.

## Notable code patterns / techniques

- **Mirror-action lookup-by-name-substring** (lines 793-801): instead of using a tag taxonomy, the source matches orb names by substring (`"ubwff-idtiq"`, `"ubwff-crkfz"`, `"kncqr-idtiq"`, `"kncqr-crkfz"`) and uses each match to choose `(dx, dy)`, `(-dx, dy)`, `(dx, -dy)`, `(-dx, -dy)` respectively. This generalises mirror-orb pairings: a `ubwff-*` pair mirrors across the vertical axis, a `kncqr-*` pair mirrors across both axes (point-symmetric).
- **Pre-move snapshot for swap-merging** (lines 791, 818-826): every orb's pre-move position is cached in `bwyvb`. After all orbs have moved, the source checks for the special case where two orbs that started 1 cell apart now occupy each other's start cell (i.e. they passed through each other). When detected, both orbs are set to the midpoint cell.
- **Co-location pairing via dict-grouping** (lines 827-845): build a dict of (x, y) → list of orbs at that cell; cells with exactly 2 entries pair both orbs; cells with 3+ entries pair the first 2 and revert the rest to their `bwyvb` snapshots.
- **Background-dyer overlay HUD** (`kyrgqgqaes`): rather than baking dyed background colours into the camera or sprite palette, the HUD class scans the frame for palette-0 cells and replaces them per its 2- or 4-quadrant split derived from `level.data["npwxa"]`. The split mode flips when fewer than 4 orbs are unpaired, providing a visual "progress" cue.
- **Click-mode-toggle via single boolean** (`vmcbq`): the entire arrow-key behaviour is gated by one bool. True ⇒ orbs move; False ⇒ the `cfwgj`-bound cvcer moves. Click toggles it.
- **Per-sprite-name initial-position snapshot** (`myxvz`): captured at level start; used to deterministically reset all `sys_click` sprites after a hazard hit. This is a clean reset pattern — no need to clone-and-cache the entire level state.
- **`set_placeable_sprite` engine API**: hands the engine a "currently dragged" sprite; the engine uses it for position-sync-with-mouse rendering. Cleared by passing `None`.
- **`color_remap(None, palette)`**: colour-remap-all method on Sprite; used here to recolour entire sprites in one call (selection highlight, dim-during-cvcer-mode, blink animation).

## Anti-patterns / lessons

- **Behavioural identity encoded in obfuscated *names*** (orbs differ only by name substrings — `kncqr` vs `ubwff`, `crkfz` vs `idtiq`). A generated game should use tags (`mirror-vert`, `mirror-horiz`, etc.) so the discrimination is structural, not lexical.
- **ACTION5 is registered but unused** — wastes a 6th action slot on a no-op. A generated game should not register actions it has no branch for.
- **9 of 11 `jggua-Level*` maze sprites are dead-or-out-of-scope in L1-3** (only Level1, Level6, Level11 used; the rest are L4+ or never placed). A generated 3-level game should ship exactly 3 maze sprites, one per level.
- **`dssyxgdgjg` is called from L1-3 paths but does nothing in scope** — it scans for `hnutp-*`/`dfnuk-*` pairs which only exist at L5+. Cluttered code path. A generated game should not retain dead-call helpers.
- **The HUD overlay does heavy per-frame work** (full 64×64 dyer scan + cvcer outline rasterisation + wyiex checkerboard rasterisation). Acceptable for L1-3 with small grids but would not scale.
- **Mixed-system collision**: orb collision against `jggua` walls uses the engine's `collides_with`; against `nhiae`-tagged cvcer uses tag lookup; against `dfnuk-*` walls uses name iteration. Three different idioms for "is the destination cell blocked". A generated game should pick one (tag-based).

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES (top row + bottom row dual depleting bars).
- Has lives mechanic: NO.
- Has click-to-select (uses ACTION6): YES (clicks select cvcer post-stones in L3).
- Has tag-based grouping (uses `level.get_sprites_by_tag`): YES (`level.get_sprites_by_tag("sys_click")` in `on_set_level`; `level.get_sprites_by_tag("jggua")` and `level.get_sprites_by_tag("nhiae")` in `bpcdxdwyxx`).
- Uses ACTION5 (modal): YES — registered in `available_actions`, but no behavioural branch (effectively a no-op that costs a step).
- Uses ACTION6 (click): YES.
- Uses ACTION7: NO.
- Has level data dicts (uses `level.get_data` / `level.set_data`): YES (every level has a `data={"npwxa": [...]}`; `kyrgqgqaes` calls `level.get_data("npwxa")`).
- Multi-mechanic per level (vs. single mechanic per level): NO — each level introduces exactly one new mechanic on top of the previous (L1 = orbs, L2 = +hazards, L3 = +movable walls).
- Tutorial level appears solvable by random play: UNKNOWN — L1's 2-orb + 11×11 maze is small enough that random arrow-key spam might succeed within 150 steps, but the central pillar makes most random sequences fail. Empirically uncertain.
- Has a depleting resource: YES — step counter, 150 per level.
- Has an accumulating resource: YES — paired-orb count (`fqunj`).
- Sprite shape convention used: mixed — single-cell glyphs (orbs, hazards, keys, post-stones), filled small bars (coloured walls), large mosaics (mazes).
- HUD position: multiple — step counter at top + bottom; background dyer fills the entire frame's palette-0 cells.
- Palette size used: 9 distinct palette values — {0, 8, 9, 10, 12, 14, 15} from sprite bodies, plus {1, 5, 11} drawn at runtime by HUD overlays and `color_remap` highlights.
- Background colour value: 5 (`BACKGROUND_COLOR = 5`); but the visible colour of any palette-0 cell is overridden by the `kyrgqgqaes` HUD using `level.data["npwxa"]` colours.
- Padding / letter-box colour value: 0 (`PADDING_COLOR = 0`).
- Number of distinct mechanics introduced across levels 1-3: 3 (mirror-orb motion in L1, hazards in L2, movable post-stones in L3).
- Number of levels documented: 3.

(End of file.)
