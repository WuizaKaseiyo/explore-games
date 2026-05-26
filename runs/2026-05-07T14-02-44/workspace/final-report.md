# Game generation final report

## Generated game
- **ID**: yf3h
- **Source**: `prior-games/yf3h/yf3h.py`
- **Metadata**: `prior-games/yf3h/metadata.json`
- **Lines of code**: 631

## Mechanic
The player faces stationary "emitter" sprites (red/blue/green filled-square shapes; each has a small centre indicator dot whose colour shows whether the emitter is armed) and "resonator" sprites (hollow square frames whose outline colour communicates the colour-multiset they require to activate). Clicking an emitter (`ACTION6`) toggles its armed state — armed emitters glow yellow at the centre. Pressing `ACTION5` simultaneously fires every armed emitter as one transient concentric pulse-ring, expanding outward at one cell per animation tick along Manhattan distance. When a ring of a colour required by a resonator passes over it, the resonator records that colour as a flash for that tick; when a single tick's flash-set covers the resonator's full required-multiset, the resonator activates permanently (centre fills white). Level 1 is a one-emitter, one-resonator base. Level 2 adds colour-keyed activation: red rings activate red resonators, blue rings activate blue resonators, mismatches are ignored. Level 3 adds phase-delay tiles: clicking a tile toggles its active state, and an active tile delays any ring passing through it by one tick — letting the player align unequal Manhattan distances when a multi-colour resonator needs simultaneous arrival of two colours. Each ACTION costs one step from the level's budget; running out of budget triggers `lose()`.

## Action mapping
| Action | Effect |
|---|---|
| ACTION5 | BURST — simultaneously fire every currently-armed emitter; each fires a transient pulse-ring that expands 1 cell per tick. After firing, all emitters disarm. |
| ACTION6 | CLICK at `(x, y)` — toggles arm state of the clicked emitter, OR (from L3) toggles active state of the clicked phase-delay tile. Click on empty cell, resonator, or pip is a no-op (still consumes 1 step). |

## Levels
- **L1 (12×12 grid, step budget 12, witness 2 actions)** — Base mechanic M1 (`arm-fire-ring-strike-resonator`). One red emitter at grid (3, 6), one red resonator at (8, 6), Manhattan distance 5. Witness: arm red emitter + ACTION5.
- **L2 (12×12 grid, step budget 16, witness 3 actions)** — Adds M2 (`colour-keyed resonator`). Red and blue emitters at (2, 3) and (2, 8); same-coloured resonators at (9, 3) and (9, 8). Both colours must be armed and fired (cross-colour rings are ignored). Witness: arm red, arm blue, ACTION5.
- **L3 (16×16 grid, step budget 18, witness 5 actions)** — Adds M3 (`phase-delay tile`). Three emitters (red top-left at (1, 5), blue top-right at (11, 6), green bottom-left at (1, 11)), one multi-colour resonator at (6, 6) with `{red, blue}` requirement, one green-only resonator at (11, 11), one phase-delay tile at (12, 3). Centre-to-centre distances: red→multi = 6, blue→multi = 5, blue→tile = 4. Without the tile active, red and blue arrive at the multi-resonator at different ticks (6 and 5) and it never activates. With the tile active, blue is delayed at radius 4, aligning blue's multi-resonator arrival to tick 6 = red's arrival. Witness: `[toggle delay tile, arm red, arm blue, arm green, ACTION5]`. **Verified end-to-end** by running the witness through the engine (state → WIN; activated_resonators = 2/2) AND counterfactually (every no-delay-tile strategy fails — multi-resonator stays inactive when M3 is skipped).

## Novelty note
- Closest taxonomy entry: **bx84 (`beam-mirror-reflect`)** — both have an emitter→target topology with optional path-modifying tiles. **Distinguishing rule**: bx84 fires a single linear beam that the player routes through static reflectors / filters / prisms (spatial routing); yf3h fires concentric rings expanding omnidirectionally and uses MULTISET-SAME-TICK simultaneity for activation (a temporal-coordination puzzle). bx84 has no notion of "target needs N concurrent inputs"; yf3h's central puzzle IS that simultaneity requirement.
- Closest prior-game entry: **gv47 (`seed-grow-surround-dissolve`)** — both have outward expansion from clicked sources. **Distinguishing rule**: gv47's expansion is PERSISTENT region-fill; yf3h's rings are TRANSIENT (each ring exists only at radius R on tick R, then moves on). gv47 player thinks "what cells get covered"; yf3h player thinks "what tick each cell is touched and by which colours".

## Index update
One row appended to `prior-games/index.md`:

```
| yf3h | pulse-arm-burst-resonate | Pulse-Arm-Burst Resonate — click emitters to arm them; ACTION5 fires every armed emitter as a concentric ring; resonators activate when their colour-multiset arrives same-tick. | 2026-05-07T15:04:58Z | (autonomous) |
```
