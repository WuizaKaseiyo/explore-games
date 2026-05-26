# tu93 — deep analysis

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
- File: `/Users/nickhe/Programming/NovaPlay-Agents/game_sources/tu93/2b534c15/tu93.py`
- Lines: 1251
- Class name: `Tu93`
- available_actions: `[1, 2, 3, 4]` (UP / DOWN / LEFT / RIGHT)
- Number of levels in source: 9
- Number of levels documented in this analysis: 3
- Imports: `NovaBaseGame`, `Camera`, `GameAction`, `Level`, `RenderableUserDisplay`, `Sprite` from `novaengine`; `numpy as np`.

## Mechanic essence (one sentence)

A 3-cell-tall pawn hops three pixels at a time along the value-2 corridors carved into a single maze-shaped tile, and as it walks past a coloured-arrow tile the arrow either falls into step behind the pawn like a duckling, advances one corridor-cell every turn on its own purple-clockwork march, or waits dormant until the pawn brushes it red and joins the procession — the level is solved when the pawn and every duckling stand on the goal-marker tile together.

## Sprite roster

| sprite (obfuscated) | dims | palette values used | tags | layer | collidable | blocking | visible | role inferred |
|---|---|---|---|---|---|---|---|---|
| `advckbbctt` | 33x33 | 0, 2, -1 | vhlesexlqd | -1 | YES | (default) | YES | maze tile (L1) — value-2 cells = walkable corridors, value-0 = corner-nodes, -1 = transparent |
| `aspakzyitl` | 3x3 | 12, 15 | zzuxulcort | (default) | YES | (default) | YES | purple chaser-arrow (defined but not placed in L1-3) |
| `ayinstebts` | 39x39 | 0, 2, -1 | vhlesexlqd | -1 | YES | (default) | YES | maze tile (L6) — out of scope |
| `bddyedlpub` | 3x3 | 8, 15 | vllvfeggte | (default) | YES | (default) | YES | orange follower-arrow (level 4+) |
| `brszdbeosn` | 39x15 | 0, 2, -1 | vhlesexlqd | -1 | YES | (default) | YES | maze tile (L2) |
| `cgxpypzvev` | 3x3 | 8, 15 | vllvfeggte | (default) | YES | (default) | YES | orange follower-arrow (L3) |
| `cjplklyfag` | 3x3 | 13, 15 | natiyqayts | (default) | YES | (default) | YES | red conditional-follower (level 9+) |
| `cvcykawwvn` | 3x3 | 8, 15 | vllvfeggte | (default) | YES | (default) | YES | orange follower (level 6+) |
| `ejqdrxvqko` | 3x3 | 12, 15 | zzuxulcort | (default) | YES | (default) | YES | purple chaser (defined but not placed in L1-3) |
| `fifgqtcmkj` | 3x3 | 12, 15 | zzuxulcort | (default) | YES | (default) | YES | purple chaser (level 6+) |
| `gtklxebphp` | 39x27 | 0, 2, -1 | vhlesexlqd | -1 | YES | (default) | YES | maze tile (L3) |
| `hfobzpnztv` | 3x3 | 12, 15 | zzuxulcort | (default) | YES | (default) | YES | purple chaser (level 9+) |
| `hgvhiprods` | 3x3 | 8, 15 | vllvfeggte | (default) | YES | (default) | YES | orange follower (level 9+) |
| `imoxtwqezq` | 3x3 | 12, 15 | zzuxulcort | (default) | YES | (default) | YES | purple chaser (level 9+) |
| `iwawirbnxl` | 3x3 | 9, 4 | vllvfeggte | (default) | YES | (default) | YES | blue follower (level 5+) |
| `iyplkijgol` | 3x3 | 13, 15 | natiyqayts | (default) | YES | (default) | YES | red conditional-follower (level 7+) |
| `kndyleqrkw` | 3x3 | 12, 15 | zzuxulcort | (default) | YES | (default) | YES | purple chaser (level 5+) |
| `kxiutgppmt` | 3x3 | 8, 15 | vllvfeggte | (default) | YES | (default) | YES | orange follower (L2) |
| `kxuptismsp` | 33x39 | 0, 2, -1 | vhlesexlqd | -1 | YES | (default) | YES | maze tile (level 8+) |
| `makkrfiwqg` | 45x45 | 0, 2, -1 | vhlesexlqd | -1 | YES | (default) | YES | maze tile (level 9+) |
| `mcrwthchct` | 3x3 | 1, 15 | albwnmiahg | (default) | YES | (default) | YES | the pawn / player avatar — palette-1 (cyan) body with palette-15 cap pixel that toggles to palette-11 when "active" |
| `mivgxwpflv` | 3x3 | 8, 15 | vllvfeggte | (default) | YES | (default) | YES | orange follower (level 4+) |
| `nittvfnhzg` | 3x3 | 12, 15 | zzuxulcort | (default) | YES | (default) | YES | purple chaser (level 5+) |
| `ntmztjafro` | 3x3 | 12, 15 | zzuxulcort | (default) | YES | (default) | YES | purple chaser (L3) |
| `pbdsotvhqq` | 39x9 | 0, 2, -1 | vhlesexlqd | -1 | YES | (default) | YES | maze tile (level 5+) |
| `psrdkitxxm` | 3x3 | 12, 15 | zzuxulcort | (default) | YES | (default) | YES | purple chaser (L3) |
| `ptunqyictb` | 3x3 | 8, 15 | vllvfeggte | (default) | YES | (default) | YES | orange follower (level 9+) |
| `qfbnkdxpdo` | 3x3 | 12, 15 | zzuxulcort | (default) | YES | (default) | YES | purple chaser (level 9+) |
| `qfgklunikd` | 5x5 | (any) | (default) | (default) | YES | (default) | YES | "expanded" sprite shape — used as visual target swap when an arrow expires |
| `qgamkwcgto` | 3x3 | 8, 15 | vllvfeggte | (default) | YES | (default) | YES | orange follower (level 7+) |
| `rlkxuujqdr` | 3x3 | (any) | (default) | (default) | YES | (default) | YES | small "expanded" sprite shape — visual swap target |
| `rtyncmnohe` | 3x3 | 12, 15 | zzuxulcort | (default) | YES | (default) | YES | purple chaser (defined but not placed) |
| `sbarnmpjpm` | 3x3 | 13, 15 | natiyqayts | (default) | YES | (default) | YES | red conditional-follower (level 6+) |
| `sjwurrpact` | 3x3 | 13, 15 | natiyqayts | (default) | YES | (default) | YES | red conditional-follower (level 6+) |
| `tciltoqihp` | 3x3 | 13, 15 | natiyqayts | (default) | YES | (default) | YES | red conditional-follower (level 6+) |
| `udqmltazlr` | 3x3 | 8, 15 | vllvfeggte | (default) | YES | (default) | YES | orange follower (level 4+) |
| `uqxhtswcue` | 3x3 | 12, 15 | zzuxulcort | (default) | YES | (default) | YES | purple chaser (level 8+) |
| `uusnwexoqh` | 33x33 | 0, 2, -1 | vhlesexlqd | -1 | YES | (default) | YES | maze tile (level 7+) |
| `vxqrqqcnyf` | 3x3 | 8, 15 | vllvfeggte | (default) | YES | (default) | YES | orange follower (level 8+) |
| `woawzicyis` | 3x3 | 8, 15 | vllvfeggte | (default) | YES | (default) | YES | orange follower (level 5+) |
| `wsaxbozuoh` | 3x3 | 8, 15 | vllvfeggte | (default) | YES | (default) | YES | orange follower (level 6+) |
| `xtivqldqva` | 3x3 | 14, 15 | xboyuzuyxv | (default) | YES | (default) | YES | green goal-marker — exit cell |
| `zdorjsnggl` | 3x3 | 13, 15 | natiyqayts | (default) | YES | (default) | YES | red conditional-follower (level 6+) |

### `advckbbctt` — maze tile (L1)
- Pixel pattern: 33x33 mosaic of palette-0 (corner nodes) and palette-2 (corridor cells) with -1 transparent gaps. The maze cells are arranged on a 3-cell stride: every (3i, 3j) cell is a "node" (palette-0); cells between nodes can be palette-2 (walkable) or -1 (impassable wall).
- Where it appears: L1 only (1 copy at (3, 3)).
- Role: the maze itself. Tag `vhlesexlqd` makes it the singleton "maze sprite" — the rest of the game references it via `get_sprites_by_tag("vhlesexlqd")[0]`. Walkability is checked by reading `maze.pixels[i, j]` at the candidate cell.
- Visual-vs-functional read: at-rendered-scale, a complex grid of palette-0 dots (3x3 cells) connected by palette-2 strips. Reads as a maze diagram. Distinct.

### `aspakzyitl` — purple chaser (defined but not placed in L1-3)
- Pixel pattern: 3x3 `[[12, 15, 12], [12, 12, 12], [12, 12, 12]]`. Purple body with palette-15 cap.
- Role: out of scope.

### `ayinstebts` — maze tile (L6)
- Pixel pattern: 39x39.
- Where it appears: L6 only.
- Role: out of scope.

### `bddyedlpub` — orange follower (L4+)
- Pixel pattern: 3x3 `[[8, 15, 8], [8, 8, 8], [8, 8, 8]]`.
- Where it appears: not placed in L1-3.

### `brszdbeosn` — maze tile (L2)
- Pixel pattern: 39x15 (less wide than L1's maze).
- Where it appears: L2 only (1 copy at (3, 12)).
- Role: maze for L2. Smaller corridor count.

### `cgxpypzvev` — orange follower (L3)
- Pixel pattern: 3x3 standard orange-arrow.
- Where it appears: L3 (1 copy at (15, 15) rotated 90).
- Role: a follower the player must pick up. Tag `vllvfeggte`. When the player walks within (twsfmzbqkg=6) cells of this follower, `kqpvpzoaim` activates it via `ijipdchkji` (sets pixels[0,1] = 11). Activated followers then move with the player.

### `cjplklyfag` — red conditional-follower (level 9+)
- Pixel pattern: 3x3 `[[13, 15, 13], [13, 13, 13], [13, 13, 13]]`. Maroon body.
- Where it appears: not placed in L1-3.

### `cvcykawwvn` — orange follower (level 6+)
- Pixel pattern: 3x3 standard orange-arrow.
- Where it appears: not placed in L1-3.

### `ejqdrxvqko` — purple chaser (defined but not placed)
- Pixel pattern: 3x3 standard purple.
- Where it appears: never placed in any level.

### `fifgqtcmkj` — purple chaser (level 6+)
- Pixel pattern: 3x3 standard purple.
- Where it appears: not placed in L1-3.

### `gtklxebphp` — maze tile (L3)
- Pixel pattern: 39x27.
- Where it appears: L3 only (1 copy at (3, 9)).

### `hfobzpnztv` — purple chaser (level 9+)
- Pixel pattern: 3x3 standard purple.
- Where it appears: not placed in L1-3.

### `hgvhiprods` — orange follower (level 9+)
- Pixel pattern: 3x3 standard orange.
- Where it appears: not placed in L1-3.

### `imoxtwqezq` — purple chaser (level 9+)
- Pixel pattern: 3x3 standard purple.
- Where it appears: not placed in L1-3.

### `iwawirbnxl` — blue follower (level 5+)
- Pixel pattern: 3x3 `[[9, 4, 9], [9, 9, 9], [9, 9, 9]]`. Blue body, palette-4 cap.
- Where it appears: not placed in L1-3.

### `iyplkijgol` — red conditional-follower (level 7+)
- Pixel pattern: 3x3 standard red.
- Where it appears: not placed in L1-3.

### `kndyleqrkw` — purple chaser (level 5+)
- Pixel pattern: 3x3 standard purple.
- Where it appears: not placed in L1-3.

### `kxiutgppmt` — orange follower (L2)
- Pixel pattern: 3x3 standard orange.
- Where it appears: L2 (1 copy at (27, 18) rotated 270).
- Role: follower for L2.

### `kxuptismsp` — maze tile (level 8+)
- Pixel pattern: 33x39.
- Where it appears: not placed in L1-3.

### `makkrfiwqg` — maze tile (level 9+)
- Pixel pattern: 45x45.
- Where it appears: not placed in L1-3.

### `mcrwthchct` — pawn / player avatar
- Pixel pattern: 3x3 `[[1, 15, 1], [1, 1, 1], [1, 1, 1]]`. Cyan body with white cap pixel that toggles palette to indicate active state.
- Where it appears: every L1-3 level (1 copy each).
- Role: the player. Tag `albwnmiahg`. Direction encoded by rotation (0=up, 90=right, 180=down, 270=left). Each ACTION1-4 attempts to step bsfndluqyd=3 cells in the corresponding direction, validated by checking the maze cell at that offset has pixel-value 2. Player position is offset from maze position.
- Visual-vs-functional read: at-rendered-scale, a 3x3 cyan square with a white cap that points the direction of last move. Tag is unique. Nearest-other: every other 3x3 sprite uses similar cap-pattern — distinguished only by body palette.

### `mivgxwpflv` — orange follower (level 4+)
- Pixel pattern: 3x3 standard orange.
- Where it appears: not placed in L1-3.

### `nittvfnhzg` — purple chaser (level 5+)
- Pixel pattern: 3x3 standard purple.
- Where it appears: not placed in L1-3.

### `ntmztjafro` — purple chaser (L3)
- Pixel pattern: 3x3 standard purple.
- Where it appears: L3 (1 copy at (3, 27) rotated 90).
- Role: chaser. Tag `zzuxulcort`. Each turn, after the player moves, the chaser steps 1 cell in its current rotation direction (`yacjieihbk`). When it reaches a node-cell, it tries to "consume" any followers (`vllvfeggte`/`zzuxulcort`/`natiyqayts`) at the same position via `ojcejjkbwt` — converts them to expanded `rlkxuujqdr` 3x3 or `qfgklunikd` 5x5 sprites then removes. The chaser direction is updated by `irydcdcqyd` based on the maze's pixel pattern at offset (chooses to continue if the cell ahead is walkable, otherwise reverses).

### `pbdsotvhqq` — maze tile (level 5+)
- Pixel pattern: 39x9.
- Where it appears: not placed in L1-3.

### `psrdkitxxm` — purple chaser (L3)
- Pixel pattern: 3x3 standard purple.
- Where it appears: L3 (1 copy at (21, 15) rotated 180).

### `ptunqyictb` — orange follower (level 9+)
- Pixel pattern: 3x3 standard orange.
- Where it appears: not placed in L1-3.

### `qfbnkdxpdo` — purple chaser (level 9+)
- Pixel pattern: 3x3 standard purple.
- Where it appears: not placed in L1-3.

### `qfgklunikd` — expanded 5x5 visual swap target
- Pixel pattern: 5x5 (recoloured at runtime).
- Where it appears: spawned by `ojcejjkbwt` when a 5x5 follower expires (consumed by chaser). The follower's pixels are replaced with `qfgklunikd.pixels`, recoloured to its original colour, position offset (-1, -1).
- Role: visual death animation overlay; replaced once then removed on next iteration.

### `qgamkwcgto` — orange follower (level 7+)
- Pixel pattern: 3x3 standard orange.
- Where it appears: not placed in L1-3.

### `rlkxuujqdr` — expanded 3x3 visual swap target
- Pixel pattern: 3x3 (recoloured at runtime).
- Where it appears: spawned by `ojcejjkbwt` when a 3x3 follower expires.
- Role: visual death animation overlay.

### `rtyncmnohe` — purple chaser (defined but not placed)
- Pixel pattern: 3x3 standard purple.
- Where it appears: never placed.

### `sbarnmpjpm` — red conditional-follower (level 6+)
- Pixel pattern: 3x3 standard red.
- Where it appears: not placed in L1-3.

### `sjwurrpact` — red conditional-follower (level 6+)
- Pixel pattern: 3x3 standard red.
- Where it appears: not placed in L1-3.

### `tciltoqihp` — red conditional-follower (level 6+)
- Pixel pattern: 3x3 standard red.
- Where it appears: not placed in L1-3.

### `udqmltazlr` — orange follower (level 4+)
- Pixel pattern: 3x3 standard orange.
- Where it appears: not placed in L1-3.

### `uqxhtswcue` — purple chaser (level 8+)
- Pixel pattern: 3x3 standard purple.
- Where it appears: not placed in L1-3.

### `uusnwexoqh` — maze tile (level 7+)
- Pixel pattern: 33x33.
- Where it appears: not placed in L1-3.

### `vxqrqqcnyf` — orange follower (level 8+)
- Pixel pattern: 3x3 standard orange.
- Where it appears: not placed in L1-3.

### `woawzicyis` — orange follower (level 5+)
- Pixel pattern: 3x3 standard orange.
- Where it appears: not placed in L1-3.

### `wsaxbozuoh` — orange follower (level 6+)
- Pixel pattern: 3x3 standard orange.
- Where it appears: not placed in L1-3.

### `xtivqldqva` — green goal-marker
- Pixel pattern: 3x3 `[[14, 15, 14], [14, 14, 14], [14, 14, 14]]`. Green body with palette-15 cap.
- Where it appears: every L1-3 level (1 copy each at distinct positions per level).
- Role: exit cell. Tag `xboyuzuyxv`. Win predicate requires every `albwnmiahg`-tagged sprite (player + activated followers) to be at the exit's position.
- Visual-vs-functional read: at-rendered-scale, a 3x3 green square with white cap. Distinct from purple/orange/red arrows by colour.

### `zdorjsnggl` — red conditional-follower (level 6+)
- Pixel pattern: 3x3 standard red.
- Where it appears: not placed in L1-3.

## Levels 1, 2, and 3 only

### Level 1
- `grid_size`: (39, 38)
- Number of sprites placed: 3
- Composition: 1 maze tile (`advckbbctt` 33x33 at (3, 3)), 1 player (`mcrwthchct` at (3, 3) rotation 90 — facing right), 1 exit (`xtivqldqva` at (33, 33)).
- Level data: `{"StepCounter": 50}`.
- Spawn position(s): player at (3, 3), facing right (rotation 90). Exit at far corner (33, 33).
- Per-cell layout: 39x38 grid. Maze tile occupies (3, 3) to (35, 35) — 33x33 maze inside the grid. Player at top-left of maze; exit at bottom-right.
- Mechanic introduced relative to the previous level: this is the first level — introduces the **maze-step navigation** mechanic. Each ACTION1-4 attempts to step the player 3 cells in the corresponding direction; the move is allowed only if the maze tile's pixel at the offset is value-2 (walkable). The player's rotation updates to face the move direction. After the player moves, all chasers (`zzuxulcort`) advance 1 cell, conditional-followers (`natiyqayts`) advance if "active". Win when player at exit position.
- Specific challenge: simple navigation through the L1 maze. No followers, no chasers. Just find the route from (3, 3) to (33, 33).
- Estimated optimal action count: ~10-15 (depending on maze geometry).

### Level 2
- `grid_size`: (45, 45)
- Number of sprites placed: 4
- Composition: 1 maze tile (`brszdbeosn` 39x15 at (3, 12)), 1 follower (`kxiutgppmt` at (27, 18) rot 270), 1 player (`mcrwthchct` at (3, 24)), 1 exit (`xtivqldqva` at (39, 12)).
- Level data: `{"StepCounter": 50}`.
- Spawn position(s): player at (3, 24).
- Per-cell layout: 45x45. Maze 39x15 sits in middle band rows 12-26. Player at (3, 24); follower at (27, 18); exit at (39, 12).
- Mechanic introduced relative to L1: **Followers** (`vllvfeggte`). When the player moves close enough (within 6 cells via `lzfoxdhqxu`), the follower's pixels[0, 1] flips to palette-11 (active) via `ijipdchkji`, and the follower then mirrors the player's moves. Win condition extends: ALL followers must reach the exit, not just the player.
- Specific challenge: navigate the wider 39x15 maze, pick up the follower, lead both to exit.
- Estimated optimal action count: ~20-30.

### Level 3
- `grid_size`: (45, 45)
- Number of sprites placed: 6
- Composition: 1 maze tile (`gtklxebphp` 39x27 at (3, 9)), 1 follower (`cgxpypzvev` at (15, 15) rot 90), 2 chasers (`ntmztjafro` at (3, 27) rot 90; `psrdkitxxm` at (21, 15) rot 180), 1 player (`mcrwthchct` at (33, 33)), 1 exit (`xtivqldqva` at (15, 33)).
- Level data: `{"StepCounter": 35}` — tighter budget than L1/L2.
- Spawn position(s): player at (33, 33).
- Per-cell layout: 45x45. Maze 39x27 covers most of the playfield. Two chasers patrol along the maze; one follower needs collection.
- Mechanic introduced relative to L2: **Chasers** (`zzuxulcort`). After every player move, each chaser advances 1 cell in its current rotation direction. When a chaser reaches a node-cell, it consumes any same-cell followers (player or activated follower) — the consumed sprite is replaced with `rlkxuujqdr`/`qfgklunikd` expansion sprites then removed (i.e. lose). The chasers' direction reverses when their next cell is not walkable.
- Specific challenge: navigate maze, collect follower, avoid 2 patrolling chasers, reach exit before chasers consume the train. Tight 35-step budget.
- Estimated optimal action count: ~25-30.

Levels 4-9 exist but are excluded per skill scope.

## Action handlers

### ACTION1 / ACTION2 / ACTION3 / ACTION4 (UP / DOWN / LEFT / RIGHT)
- Trigger: `self.action.id in [GameAction.ACTION1, ACTION2, ACTION3, ACTION4]`.
- Branches inside `step()`: state machine with `iuubfszcoi` (0/1/2):
  - **State 0 (player turn)**: read player position relative to maze; compute candidate cell offset (i.e. (lmvmotdds, spxwaggxt - bsfndluqyd) for UP); check if that cell in the maze pixels is value-2; if so, set player rotation, advance player by `wkagrzgfwd`, set `iuubfszcoi = 1`. Decrement step counter via `tsoqrmroqn.zdxmrkxivd()`.
  - **State 1 (follower turn)**: if `vpaafwwtxk()` returns True (all followers have completed their move), call `kqpvpzoaim()` (activate any new followers within range), `yacjieihbk()` (advance all chasers), `jjqtojitqv()` (advance active conditional-followers). Set `iuubfszcoi = 2`.
  - **State 2 (settle)**: if `rodqliwlhy()` returns True (all sprites have stable positions), run `irydcdcqyd()` (update chaser directions), `sdjbufarus()` (activate conditional-followers near the player), check win predicate (all followers at exit → `next_level()`), check lose (no followers left or step counter exhausted → `lose()`). Reset `iuubfszcoi = 0`. Call `complete_action()`.
- State mutations: read `self.action`, `self.iuubfszcoi`, `self.tsoqrmroqn`. Written: every sprite's position, every sprite's rotation (chasers reverse), `pixels[0, 1]` (active flag) of activated followers, `self.tsoqrmroqn.current_steps`, `self.iuubfszcoi`, `self.sdiguidlbg` (rotation history for delayed conditional-followers).
- Side effects on sprites: player + activated followers move; chasers advance; conditional-followers may activate or advance; consumed sprites replaced with expansion overlays then removed.
- Engine effects: `next_level()` when all followers at exit; `lose()` when no followers remain or step counter at 0.
- Pre-conditions / gating: directional move rejected if maze cell is not value-2.

## HUD widgets

### `klmvbszflr` — bottom-row depleting step bar
- Class name (obfuscated): `klmvbszflr`.
- Render-pixel range: row 63 (very bottom), all 64 columns.
- What value it displays: `current_steps / mspafmzsoi` ratio.
- Visual style: row 63 — palette-6 (cvtecbuzje) for the leading remaining-budget cells; palette-0 for the rest.
- Update points: every action via `zdxmrkxivd`; reset in `on_set_level` via `fkcoriciwn`.
- Where it is registered: `interfaces=[self.tsoqrmroqn]` in Camera constructor.

## Internal state — exhaustive

| attr (obfuscated) | semantic name | type | initial value | written by | read by | role |
|---|---|---|---|---|---|---|
| `tsoqrmroqn` | step_counter_HUD | `klmvbszflr` | `klmvbszflr(0)` | `__init__`, `on_set_level`, `step` | `step`, render | step bar |
| `iuubfszcoi` | game_phase | int | 0 | `__init__`, `on_set_level`, `step` | `step` | state machine: 0 = player turn, 1 = follower advance, 2 = settle |
| `sdiguidlbg` | rotation_history | `dict[Sprite, list[int]]` | `{}` | `__init__`, `on_set_level`, `step`, `sdjbufarus` | `step`, `sdjbufarus` | per-sprite rotation queue for delayed conditional-followers (red `natiyqayts` follow with a 1-tick delay) |

## Win condition

Plain English: the level wins when every player-tagged sprite (the original player + every activated follower) sits at the exit position.

Literal condition: in `step()` state-2 branch:
```python
hyedoggckq = self.current_level.get_sprites_by_tag("albwnmiahg")
ahvmhmsmxp = self.current_level.get_sprites_by_tag("xboyuzuyxv")
if hyedoggckq and all([any([s.x == e.x and s.y == e.y for e in ahvmhmsmxp]) for s in hyedoggckq]):
    self.next_level()
```

Same predicate for L1, L2, L3.

## Lose condition

Plain English: lose if no `albwnmiahg`-tagged sprites remain (player or all followers consumed by chasers) OR step counter hits 0.

Literal condition:
```python
elif not hyedoggckq or not self.tsoqrmroqn.current_steps:
    self.lose()
```

## Resource economy

- Depleting resource: YES — `tsoqrmroqn.current_steps` (initial per-level: 50/50/35). Decremented by 1 per ACTION1-4. Threshold 0 triggers `lose()`.
- Accumulating resource: YES (implicit) — count of activated followers (`vllvfeggte`-tagged sprites with pixels[0, 1] == 11). Followers contribute to the win-predicate sprite count.
- Lives mechanic: NO. Single `lose()` ends game.
- Resource interaction: step counter and chaser-consumption are both lose triggers; reach-exit-with-all-followers is the win trigger.

## Action-budget signature

- Default budget per level: per-level via `level.get_data("StepCounter")`. L1=50, L2=50, L3=35.
- Whether budget tightens or shifts across levels 1-3: YES — L3 drops to 35 (tighter as chasers introduced).
- Per-level vs. per-environment: per-level (reset in `on_set_level`).
- Decrement rate per action: 1 per directional action.
- Refill mechanism: NONE.

## Notable code patterns / techniques

- **Maze as a single tile sprite** with palette-2 walkable cells and palette-0 nodes; walkability is checked by reading the sprite's pixel array directly. Compact representation.
- **3-cell stride** (`bsfndluqyd = 3`): all positions are multiples of 3; the maze is a 3-cell-grid graph carved into a flat sprite.
- **Three-phase step state machine** (`iuubfszcoi`): 0=player input, 1=follower advance, 2=settle. Allows clean separation of player action, AI step, and predicate checks.
- **Rotation as direction-indicator**: chasers and the player both encode direction via rotation; the cap pixel (`pixels[0, 1]`) makes it visually obvious.
- **Delayed conditional-follower queue** (`sdiguidlbg`): each red follower's rotation history is stored so it follows the player's path with a 1-tick lag.
- **Adjacency-test via Manhattan distance and rotation-aware offset** (`lzfoxdhqxu`).
- **Expansion-on-death** (`ojcejjkbwt`): consumed sprites are replaced with bigger overlay sprites for one frame, providing visual "explosion" feedback.

## Anti-patterns / lessons

- **Many duplicate sprites** (multiple `vllvfeggte`-tagged orange followers with identical pixel data, multiple `zzuxulcort` purple chasers — same shape across `aspakzyitl`, `ejqdrxvqko`, `fifgqtcmkj`, `hfobzpnztv`, `imoxtwqezq`, `kndyleqrkw`, `nittvfnhzg`, `ntmztjafro`, `psrdkitxxm`, `qfbnkdxpdo`, `rtyncmnohe`, `uqxhtswcue`). All are identical 3x3 templates differing only by name. A generated game should consolidate.
- **Many maze sprites** (one per level: `advckbbctt`, `ayinstebts`, `brszdbeosn`, `gtklxebphp`, `kxuptismsp`, `makkrfiwqg`, `pbdsotvhqq`, `uusnwexoqh`) — 8 mazes for 9 levels. Acceptable but clutters the sprite library.
- **`pixels[0, 1]` as state flag**: sprites carry their "active" state in their first-row second-pixel — fragile. A generated game should use `color_remap` or a separate state dict.
- **State machine via integer counter** (`iuubfszcoi 0/1/2`) instead of explicit enum — readable but error-prone.
- **Helper methods named with random tokens** (`pbknvgksfm`, `vpvzjytxsq`, `fybihpkboq`, `hktynliktc` — all do similar things but with subtle differences). Hard to maintain.

## Cross-references

No cross-references — analysis isolated.

## Frequency-table contributions

- Has step-counter HUD: YES (bottom row).
- Has lives mechanic: NO.
- Has click-to-select (uses ACTION6): NO.
- Has tag-based grouping (uses `level.get_sprites_by_tag`): YES (`vhlesexlqd`, `albwnmiahg`, `vllvfeggte`, `zzuxulcort`, `natiyqayts`, `xboyuzuyxv`).
- Uses ACTION5 (modal): NO.
- Uses ACTION6 (click): NO.
- Uses ACTION7: NO.
- Has level data dicts (uses `level.get_data` / `level.set_data`): YES (`level.get_data("StepCounter")`).
- Multi-mechanic per level: NO — L1 = base, L2 adds followers, L3 adds chasers.
- Tutorial level appears solvable by random play: NO. Random arrow keys mostly hit walls.
- Has a depleting resource: YES — step counter.
- Has an accumulating resource: YES — activated-follower count.
- Sprite shape convention used: mixed — large maze tiles (mosaic), 3x3 unit pawns (cap-glyph).
- HUD position: bottom.
- Palette size used: 7 distinct palette values in placed L1-3 sprites: {0, 1, 2, 8, 12, 14, 15}. Plus {6} for HUD = 8.
- Background colour value: 5 (`BACKGROUND_COLOR = 5`).
- Padding / letter-box colour value: 5 (`PADDING_COLOR = 5`).
- Number of distinct mechanics introduced across levels 1-3: 3 (maze-step in L1, followers in L2, chasers in L3).
- Number of levels documented: 3.

(End of file.)
