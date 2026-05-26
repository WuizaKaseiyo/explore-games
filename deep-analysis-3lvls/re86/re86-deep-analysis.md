# re86 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/re86/4e57566e/re86.py`
- Lines: 2141
- Class name: `Re86`
- available_actions: `[1, 2, 3, 4, 5]` (UP/DOWN/LEFT/RIGHT, ACTION5=cycle-active-shape)
- Number of levels in source: 8
- Number of levels documented in this analysis: 3
- Imports: `NovaBaseGame`, `Camera`, `GameAction`, `Level`, `RenderableUserDisplay`, `Sprite` from `novaengine`; `numpy as np`.

## Mechanic essence (one sentence)

Several hollow coloured-frame shapes float over a large hidden canvas with a target picture printed on it, and the player slides one of the frames three pixels at a time with the arrow keys (or presses cycle to switch which frame is active) so that each frame visits the right colour-zone to dye itself the matching colour and then settles over the canvas region whose target tint matches — the level is solved when every painted-tint region of the canvas is fully covered by frames of the matching colour.

## Sprite roster

(re86 has 47 sprites, mostly unique shape-frames per level. For brevity, sprites are documented by tag-group below; each sprite within a tag-group plays the same role.)

| sprite (obfuscated) | dims | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| `afywyyglcv` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L4) |
| `aschrteoyn` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L8) |
| `asmnsdxgsk` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L4) |
| `bpyckthxmf` | 64x64 | various | vzuwsebntu, yojcsdeysc | (default) | YES | (default) | YES | L3 hidden canvas template |
| `bqmgjlkmqn` | 64x64 | various | vzuwsebntu, yojcsdeysc | (default) | YES | (default) | YES | L2 canvas template |
| `cbhctuvcnt` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L5) |
| `cpvfxfphfa` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L7) |
| `dcflskgkgl` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L4) |
| `dpzvropmzo` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L5) |
| `eqeslzldkz` | 21x21 | various | vfaeucgcyr | (default) | YES | (default) | YES | shape frame (L1) |
| `etzeycqbyy` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L8) |
| `eyneohpmjj` | varies | various | vfaeucgcyr, nogegkgqgd | (default) | YES | (default) | YES | special shape (L6) |
| `fbtcowegat` | 64x64 | various | vzuwsebntu, yojcsdeysc | (default) | YES | (default) | YES | L8 canvas template |
| `fgqcnlhlgm` | varies | various | vfaeucgcyr | (default) | YES | (default) | YES | shape frame (L7) |
| `fklxqevxxp` | varies | various | vfaeucgcyr, nogegkgqgd | (default) | YES | (default) | YES | special shape (L5) |
| `frclqesaod` | varies | various | vfaeucgcyr | (default) | YES | (default) | YES | shape frame (L7) |
| `fweulealsg` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L8) |
| `gbupodwvrg` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L8) |
| `hdvyqioykf` | 12x6 | various | vfaeucgcyr | (default) | YES | (default) | YES | shape frame (L3) |
| `hjixhujtpv` | varies | various | vfaeucgcyr, nogegkgqgd | (default) | YES | (default) | YES | special shape (L8) |
| `iifvwgzbwn` | varies | various | vfaeucgcyr, nogegkgqgd | (default) | YES | (default) | YES | special shape (L7) |
| `isvtoltpsx` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L8) |
| `ivujimpeey` | varies | various | vfaeucgcyr, nogegkgqgd | (default) | YES | (default) | YES | special shape (L2) |
| `iwyyumxlbi` | varies | various | miqpqafylc | (default) | YES | (default) | YES | break-zone (L8) |
| `jvodigootl` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L7) |
| `kbzudfbtuw` | 24x24 | various | vfaeucgcyr | (default) | YES | (default) | YES | shape frame (L4) |
| `kujmqhwaes` | varies | various | vfaeucgcyr, nogegkgqgd | (default) | YES | (default) | YES | special shape (L3) |
| `ljtpmpariz` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L7) |
| `lsdbpojpqq` | varies | various | vfaeucgcyr, ldkpywfara | (default) | YES | (default) | YES | plus-shape (L5) |
| `lyvtpjfhwk` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L8) |
| `makzsprowp` | varies | various | miqpqafylc | (default) | YES | (default) | YES | break-zone (L7) |
| `nblhzkeddg` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L7) |
| `nbnfdoxidw` | 64x64 | various | vzuwsebntu, yojcsdeysc | (default) | YES | (default) | YES | L7 canvas template |
| `nkqbswtgwq` | 64x64 | various | vzuwsebntu, yojcsdeysc | (default) | YES | (default) | YES | L5 canvas template |
| `pseflysmdl` | 64x64 | various | yojcsdeysc | (default) | YES | (default) | YES | the master target template referenced for win-check |
| `pulmowhpll` | varies | various | miqpqafylc | (default) | YES | (default) | YES | break-zone (L6) |
| `qjbithskbd` | varies | various | vfaeucgcyr, ldkpywfara | (default) | YES | (default) | YES | plus-shape (L4) |
| `qjmaetmxgi` | varies | various | vfaeucgcyr | (default) | YES | (default) | YES | shape frame (L5) |
| `quydqebohi` | varies | various | vfaeucgcyr | (default) | YES | (default) | YES | shape frame (L6) |
| `rshqkcbsif` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L8) |
| `smftodnzus` | varies | various | (other) | (default) | YES | (default) | YES | (auxiliary) |
| `thfoqjoykf` | 12x12 | various | (other) | (default) | YES | (default) | YES | shape frame (L2) |
| `ubbwffhagx` | varies | various | (other) | (default) | YES | (default) | YES | shape frame (L2) |
| `uvubdhcpuz` | 64x64 | various | (canvas-related) | (default) | YES | (default) | YES | L1 canvas |
| `veoebsedym` | 64x64 | various | (canvas-related) | (default) | YES | (default) | YES | L4 canvas |
| `verxwpckie` | varies | various | (other) | (default) | YES | (default) | YES | (auxiliary) |
| `whrsffulfe` | varies | various | (other) | (default) | YES | (default) | YES | (auxiliary) |
| `wvmsvpjtki` | varies | various | (other) | (default) | YES | (default) | YES | (auxiliary) |
| `xeksskfrzc` | 64x64 | various | (canvas-related) | (default) | YES | (default) | YES | L6 canvas |
| `xgcdlptfww` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L8) |
| `xilddaovjn` | varies | various | vfaeucgcyr, nogegkgqgd | (default) | YES | (default) | YES | special shape (L8) |
| `xkpsgharmr` | varies | various | ozhohpbjxz | (default) | YES | (default) | YES | colour zone (L7) |
| `xuudmqejui` | varies | various | (other) | (default) | YES | (default) | YES | (auxiliary L1) |
| `zniyxhxlju` | varies | various | (other) | (default) | YES | (default) | YES | (auxiliary L4) |
| `ztrwteeaki` | varies | various | (other) | (default) | YES | (default) | YES | (auxiliary L5) |

### Tag-group: `vfaeucgcyr` (shape frames — the player's pawns)
- Sprites: `eqeslzldkz`, `hdvyqioykf`, `kbzudfbtuw`, `qjmaetmxgi`, `quydqebohi`, `frclqesaod`, `fgqcnlhlgm`, plus subset `nogegkgqgd` (special shapes), `ldkpywfara` (plus-shapes).
- Pixel pattern: hollow rectangular or plus-shaped frames in palette-X (varies per sprite). Centre pixel is palette-0 (`gigkddryzx`) for the active shape, palette-X for inactive.
- Role: the player's draggable shape frames. Press ACTION1-4 to move the active frame 3 cells; ACTION5 to cycle which frame is active. The active frame is the one with `pixels[h//2, w//2] == 0`. Frames carry their own colour (read by `hfoimipuna`). When a frame collides with a colour zone (`ozhohpbjxz`), the frame absorbs that zone's colour.
- Visual-vs-functional read: at-rendered-scale, hollow frames with a bright-coloured outline. The active frame has a black centre dot; inactive frames have a coloured centre. Player tells active vs inactive by centre pixel. Different frame shapes (rectangle, plus, irregular) are stylistically varied but mechanically identical — the only difference is hit-area shape.

### Tag-group: `ozhohpbjxz` (colour zones)
- Sprites: many (`afywyyglcv`, `asmnsdxgsk`, `cbhctuvcnt`, `cpvfxfphfa`, `dcflskgkgl`, `dpzvropmzo`, `etzeycqbyy`, `fweulealsg`, `gbupodwvrg`, `isvtoltpsx`, `jvodigootl`, `ljtpmpariz`, `lyvtpjfhwk`, `nblhzkeddg`, `rshqkcbsif`, `xgcdlptfww`, `xkpsgharmr`).
- Pixel pattern: each is a coloured rectangular tile of palette-X (varies). The colour identifies what colour a frame absorbs upon collision.
- Role: when an active shape-frame walks over a colour zone, the frame's pixels are recoloured to the zone's colour (lines 2061-2074). This sets up a multi-step animation in `step()` (the `zrermyobpw` / `gwwpnjmvvo` state) where the frame's pixels propagate the new colour outward over multiple ticks.

### Tag-group: `vzuwsebntu + yojcsdeysc` (canvas templates) and `pseflysmdl`
- Sprites: `bqmgjlkmqn`, `bpyckthxmf`, `nbnfdoxidw`, `nkqbswtgwq`, `fbtcowegat` per-level canvases. Plus the master `pseflysmdl`.
- Role: the canvas behind everything. The win predicate `cdjxpfqest` (lines 1877-1901) renders all `vfaeucgcyr` shapes onto a clean copy of `pseflysmdl.pixels`, then for each `vzuwsebntu`-tagged canvas checks: are all of the canvas's non-(-1, ≠4) pixels in agreement with the rendered composite? If yes for every canvas → win.

### Tag-group: `miqpqafylc` (break-zones)
- Sprites: `iwyyumxlbi`, `pulmowhpll`, `makzsprowp`.
- Role: when a frame collides with a break-zone, the frame either reshapes (grows or shrinks dimensions) or has its pixels cut. Special handling for `nogegkgqgd`-tagged shapes vs others.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (64, 64)
- Number of sprites placed: 3 — `eqeslzldkz` (shape frame at (23, 32)), `uvubdhcpuz` (canvas, default position), `xuudmqejui` (auxiliary at (10, 16)).
- Composition: 1 shape frame + 1 canvas template + 1 auxiliary.
- Level data: `{"StepCounter": 100}`.
- Spawn position(s): the only shape frame is the active one by default (its centre pixel is palette-0).
- Mechanic introduced relative to the previous level: this is the first level — introduces the **shape-overlay-on-canvas** mechanic. Move the shape frame (3-cell stride) over the canvas; the win predicate `cdjxpfqest` checks that the rendered composite of all `vfaeucgcyr` shapes (overlaid on the master template) matches every `vzuwsebntu`-tagged canvas's non-background pixels.
- Specific challenge: align the single shape frame at the correct canvas position to satisfy the predicate.
- Estimated optimal action count: ~5-10.

### Level 2
- `grid_size`: (64, 64)
- Number of sprites placed: 4 — `bqmgjlkmqn` (canvas), `ivujimpeey` (special shape at (30, 21)), `thfoqjoykf` (shape at (35, 29)), `ubbwffhagx` (shape at (16, 7)).
- Composition: 1 canvas + 2 normal shape frames + 1 special (`nogegkgqgd`) shape.
- Level data: `{"StepCounter": 100}`.
- Mechanic introduced relative to L1: **Multiple shape frames + ACTION5 cycle**. Press ACTION5 to cycle which frame is active. Special-tag shapes (`nogegkgqgd`) have a different behaviour — their centre is always palette-0 (transparent) regardless of cycle state.
- Specific challenge: position 3 frames to overlay correctly on the canvas, cycling between them with ACTION5.
- Estimated optimal action count: ~15-20.

### Level 3
- `grid_size`: (64, 64)
- Number of sprites placed: 4 — `bpyckthxmf` (canvas), `hdvyqioykf` (shape at (9, 45)), `kujmqhwaes` (special shape at (33, 36)), `whrsffulfe` (shape at (7, 37)).
- Composition: 1 canvas + 3 shape frames (one special).
- Level data: `{"StepCounter": 200}`.
- Mechanic introduced relative to L2: **Step budget doubles** (200 vs 100). More overlay positions; more cycling needed.
- Specific challenge: 3 shapes to position; the higher budget allows for trial and error.
- Estimated optimal action count: ~25-35.

Levels 4-8 exist but are excluded per skill scope.

## Action handlers

### ACTION1 / ACTION2 / ACTION3 / ACTION4 (UP / DOWN / LEFT / RIGHT)
- Trigger: `self.action.id in [GameAction.ACTION1..4]`.
- Branches: animation guard (if `zrermyobpw` and `gwwpnjmvvo` are both set, advance the colour-flood-fill animation). Otherwise decrement step counter, call `ngvfkggdii(dx, dy)` which finds the active shape (whose centre pixel is palette-0) and calls `ufgmbvuqnv` to move it 3 cells. The `ufgmbvuqnv` handles boundary checks, break-zone collisions (reshape the sprite), and colour-zone collisions (initiate flood-fill animation).
- After move: check `cdjxpfqest` (win) → `next_level()`. If step counter 0 → `lose()`.
- State mutations: many — every frame's position and pixels, `zrermyobpw`, `gwwpnjmvvo`, step counter.

### ACTION5 (cycle active shape)
- Trigger: `self.action.id == GameAction.ACTION5`.
- Branches: decrement step counter. Find current active frame (centre pixel == palette-0); compute next frame in `vfaeucgcyr` list; set its centre to palette-0; reset old active's centre via `tgawbgxjra`.
- State mutations: every frame's centre pixel.

## HUD widgets

### `nkrjkaokaj` — bottom-row depleting step bar
- Class name (obfuscated): `nkrjkaokaj`.
- Render-pixel range: row 63, all 64 columns.
- What value it displays: `current_steps / miqcxmgtji`.
- Visual style: row 63 — palette-15 for remaining; palette-1 for depleted.

## Internal state — exhaustive

| attr (obfuscated) | semantic name | type | initial value | written by | read by | role |
|---|---|---|---|---|---|---|
| `gimylktpny` | step_counter_HUD | `nkrjkaokaj` | `nkrjkaokaj(0)` | `__init__`, `on_set_level`, `step` | `step`, `_get_hidden_state`, render | step counter |
| `zrermyobpw` | colour_zone_in_progress | `Sprite \| None` | None | `step`, `ufgmbvuqnv` | `step` | the colour-zone currently flooding into a frame |
| `gwwpnjmvvo` | shape_being_painted | `Sprite \| None` | None | `step`, `ufgmbvuqnv` | `step` | the shape frame being recoloured |

## Win condition

Plain English: every `vzuwsebntu`-tagged canvas's pixel pattern must be reproducible by the union of all `vfaeucgcyr` frames overlaid on the master `pseflysmdl` template, ignoring transparent and palette-4 cells.

Literal condition: `cdjxpfqest` (lines 1877-1901). Build a 64x64 composite by rendering every `vfaeucgcyr` sprite onto a copy of `pseflysmdl.pixels` (skipping -1 transparent cells). Then for every `vzuwsebntu`-tagged canvas: check `np.any((canvas.pixels != -1) & (canvas.pixels != 4) & (canvas.pixels != composite))` — if any non-transparent non-palette-4 pixel disagrees, return False.

Same predicate for L1, L2, L3.

## Lose condition

Plain English: lose if step counter hits 0.

Literal condition: at line 2139, `elif not self.gimylktpny.current_steps: self.lose()`.

## Resource economy

- Depleting resource: YES — step counter (per-level: 100, 100, 200).
- Accumulating resource: YES (implicit) — each correctly-placed frame contributes to the win predicate.
- Lives mechanic: NO.
- Resource interaction: step counter is sole lose trigger; canvas-match is sole win trigger.

## Action-budget signature

- Default budget per level: per-level via `level.get_data("StepCounter")`. L1=100, L2=100, L3=200.
- Whether budget tightens or shifts across levels 1-3: YES — L3 doubles to 200.
- Per-level vs. per-environment: per-level (reset in `on_set_level`).
- Decrement rate per action: 1 per ACTION1-5.
- Refill mechanism: NONE.

## Notable code patterns / techniques

- **Multi-tag composition** (`vfaeucgcyr + nogegkgqgd`, `vfaeucgcyr + ldkpywfara`): tag combinations dispatch to specialised behaviour (e.g. always-transparent centre for nogegkgqgd, plus-shape mechanics for ldkpywfara).
- **Centre-pixel as active flag** (`gigkddryzx = 0`): the active shape is identified by its centre pixel == palette-0; cycling moves the flag.
- **Flood-fill animation** in `step()` (lines 2086-2106): when a frame collides with a colour zone, the frame's pixels propagate the new colour outward over multiple ticks until all non-transparent pixels match.
- **Shape resize via break-zone collision** (`ufgmbvuqnv` lines 1939-1986): collision with a `miqpqafylc`-tagged sprite reshapes the moving frame (grow or shrink dimensions). Complex pixel-array manipulation.
- **Canvas as render-target template** (`cdjxpfqest`): the win predicate composes a "what would the canvas look like if frames were rendered onto it" image and compares against expected canvas patterns.
- **`hfoimipuna(sprite)`**: extracts the dominant non-(0, -1) pixel value as the sprite's "primary colour".

## Anti-patterns / lessons

- **47 sprites, mostly unique per level** — heavy per-level sprite library. Generated games should reuse.
- **Level-specific shape templates** (`bpyckthxmf`, `nbnfdoxidw`, etc.) — each level has its own canvas and shape set. Overhead for a 3-level generated game.
- **Complex multi-phase animation state** in `step()` — error-prone.
- **Many sprites with identical role but unique names** — should be tag-based collections.
- **Implicit "active = centre-pixel-zero" convention** — fragile.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES (bottom row).
- Has lives mechanic: NO.
- Has click-to-select (uses ACTION6): NO.
- Has tag-based grouping: YES (`vfaeucgcyr`, `ozhohpbjxz`, `vzuwsebntu`, `yojcsdeysc`, `miqpqafylc`, `nogegkgqgd`, `ldkpywfara`).
- Uses ACTION5 (modal): YES (cycle active shape).
- Uses ACTION6 (click): NO.
- Uses ACTION7: NO.
- Has level data dicts: YES (`level.get_data("StepCounter")`).
- Multi-mechanic per level: NO — same template-matching mechanic across L1-3.
- Tutorial level appears solvable by random play: NO. Position-precise overlay needed.
- Has a depleting resource: YES — step counter.
- Has an accumulating resource: YES (implicit).
- Sprite shape convention used: mixed — large canvases, hollow shape frames, coloured rectangular zones.
- HUD position: bottom.
- Palette size used: many (varies by level); typically 8-12 distinct values.
- Background colour value: 5 (`BACKGROUND_COLOR = 5`).
- Padding / letter-box colour value: 3 (`PADDING_COLOR = 3`).
- Number of distinct mechanics introduced across levels 1-3: 1 (template-matching with shape frames); L2 adds cycling; L3 just adds more frames.
- Number of levels documented: 3.

(End of file.)
