# Shadow-Cast-Occlude — *Sundial-Shadow-Garden*

## Summary

A **garden viewed from above** with several tall **obelisks** rising
from a sun-warmed lawn. A small **horizon strip** at the top of the
camera shows the sun arcing left-to-right across the sky over the
course of the level. Every tick, the sun advances exactly one
position along its arc; the entire shadow geometry recomputes from
the new sun angle.

The player has **only one verb** that matters: ACTION6 click to grab
an obelisk + arrow keys to slide it. ACTION5 is **pass-the-turn**
(let the sun advance without moving anything). The level wins when
the **sun-clock chimes** — at a specific tick declared in level data,
every target tile must satisfy its `lit` / `shadow` requirement.
Crucially: the sun keeps moving, so the player has only one chance
per "noon" to align everything; missing it means waiting for the
next chime cycle.

## Visual elements (distinct from prior corpus)

- 64×64 canvas. The garden lawn is a **noisy two-tone green** (palette
  3 light/dark stipple, 1 cell = 4×4 px) that breaks the flat-tile
  uniformity of the rest of the corpus. Lit tiles render the bright
  green; shadowed tiles render the dark green. (Not pale-yellow vs.
  blue — the dual-green keeps the *garden* aesthetic.)
- A **sky strip** 4 pixels tall sits above the playable lawn. The sun
  is a small bright-yellow 2×2 sprite that visibly moves one column
  per ACTION5 tick across the strip from east → west. A pixel-thin
  arc traces the sun's projected ascent (rising on the eastern third
  → noon overhead → descending western third).
- Obelisks are **tall purple stones** rendered as 1-cell-wide,
  3-cells-tall sprites with a 2-pixel pyramidal cap. Their shadow
  on the lawn lengthens as the sun lowers (at sun-elevation high =
  short shadow of length 1; at sun-elevation low = long shadow of
  length up to 5).
- The **active obelisk** has a small white pip on its cap.
- Targets are 1×1 hollow rings on the lawn — bright-yellow ring for
  `lit`-required, indigo ring for `shadow`-required.
- L2 introduces **drifting clouds**: 1×3 wide grey-blue cloud sprites
  in the sky strip; each cloud's shadow recolours the lawn cells
  beneath its projected footprint to a third tint (`shaded-warm`,
  palette 8). Targets requiring `shadow` accept either obelisk-
  shadow or cloud-shadow; targets requiring `cloud-shadow`
  specifically need the cloud overlay.
- L3 introduces **reflective pool tiles**: a pool of pale-blue water
  on the lawn. When sunlight (a lit ray of any direction) strikes a
  pool, the pool emits a *bright spot* on the lawn cell directly
  opposite the sun's azimuth — i.e. the pool casts a virtual sun
  shaft across the lawn that itself behaves as direct light.
- A small **sun-clock chime indicator** in the top-left corner
  ticks down to the next chime; coloured **gold** at chime time.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION1 | Move the active obelisk one cell up. Sun **does not** advance on a successful obelisk move (this would be too tight on budget). Sun does advance on a *failed* move (rejected by another obelisk or wall) — a wasted turn. | obelisk selected |
| ACTION2 | Move down. | as above |
| ACTION3 | Move left. | as above |
| ACTION4 | Move right. | as above |
| ACTION5 | Pass — sun advances one column. | always |
| ACTION6 | Click on an obelisk to set it active. **Click consumes no step and the sun does not advance** (so the player can re-target without losing time). | always; clicks on lawn / obelisk-shadow / sky strip are no-ops with no step. |

## Mechanics enumeration

- **M1 — sun-arc auto-advance:** the sun's position advances by one
  column on every ACTION5 (and on every *failed* move attempt). It
  does **not** advance on successful obelisk moves or on selection
  clicks. The sun position determines:
  - light direction (azimuth from current column to noon overhead),
  - shadow length per obelisk (longer at low sun-elevation),
  - sun-clock chime ticking.
- **M2 — obelisk shadow projection:** each obelisk casts a shadow
  strip in the cardinal direction *opposite* the sun, with length
  = `floor(8 - 2 * sun_elevation_quartile)` (range 1 to 5). The
  strip terminates at lawn edge or another obelisk. The strip is
  always 1 cell wide (obelisks are 1-wide).
- **M3 — obelisk movement:** the player slides the active obelisk
  one cell at a time with arrows. Obelisks block each other.
- **M4 — sun-clock chime:** at fixed level-data tick(s), the engine
  evaluates the win predicate. Targets are checked **only** at
  chime time, not every tick. Outside chime, mismatched targets
  are not penalised — but the player must time obelisks so the
  chime tick lands on the correct geometry.
- **M5 — drifting clouds (level 2+):** clouds drift in the sky
  strip at a fixed speed (1 cell per tick, level data sets
  trajectory). Their projected shadow on the lawn moves with them.
  The cloud's shadow is a separate state from obelisk shadow:
  a lawn cell can be (a) lit, (b) obelisk-shadow, (c) cloud-shadow,
  or (d) both. Some targets require *cloud-shadow specifically*
  (rendered with an indigo+grey-blue ring).
- **M6 — reflective pool (level 3+):** pool tiles reflect direct
  sunlight as a *virtual emitter*. The reflected ray travels from
  the pool one cell at a time in the azimuth direction (away from
  the sun) until it hits an obelisk or wall, casting "lit" on
  every cell it crosses **even those that obelisks were
  shadowing**. Pools are static; their reflections move with the
  sun.

## Per-level progression

### Level 1 — base sun + obelisks (M1 + M2 + M3 + M4)
- 12×10 lawn. 2 obelisks. 4 targets (mix of lit / shadow).
  Sun crosses the sky in 14 ticks; chime at tick 7 (noon).
- The player must arrange both obelisks before the chime so the
  shadows land on the shadow targets and avoid the lit targets.
- **Witness:** 13 actions including obelisk repositioning and 4
  pass-turns. Step budget 18.
- **Mechanics required:** M1 (sun moves), M2 (shadow), M3 (move),
  M4 (chime).

### Level 2 — + M5 (clouds add a moving variable)
- 14×12 lawn. 3 obelisks. 5 targets, two of them require
  cloud-shadow specifically. Two clouds drift left→right.
  Sun crosses in 22 ticks; chime at tick 11.
- The player must coordinate obelisk shadow + cloud arrival so
  both obelisk-shadow targets and cloud-shadow targets are
  satisfied AT THE SAME tick. Clouds can't be moved — the player
  must move obelisks to match where the cloud will be.
- **Witness:** 28 actions.
- **Mechanics required:** M1, M2, M3, M4, M5.

### Level 3 — + M6 (reflective pool turns shadow into multi-source)
- 16×14 lawn. 4 obelisks, 2 reflective pools, 1 cloud.
  6 targets. Sun crosses in 30 ticks; chime at tick 15.
- The pools convert the puzzle into a *multi-source illumination*
  problem: a target behind an obelisk's shadow may still be lit
  by a pool reflection. The player must use the obelisks to
  occlude pool reflections from one direction while leaving them
  open from another, AND time it so the cloud passes over the
  cell at chime tick.
- **Witness:** ~50 actions. Step budget 70.
- **Mechanics required:** M1, M2, M3, M4, M5, M6.

## Win condition

At a sun-clock chime tick, walk every target. For each, the
target's required state (`lit` / `shadow` / `cloud-shadow`) must
equal the current lighting state of its cell. If all match, fire
`self.next_level()`. If any mismatches, the chime passes and the
player must wait for the next chime (or run out of budget — see
Lose).

## Lose condition

- `steps_used >= max_steps` → `self.lose()`.
- L1 has only **one** chime; L2 has **one**; L3 has **two** —
  missing the second chime is a direct lose.

## Internal state

- `self.sun_col: int` — current sun column on the sky strip
  (advances each tick).
- `self.sun_elevation_quartile: int` — derived from sun_col.
- `self.obelisks: list[Sprite]` — obelisk sprites with `.pos`.
- `self.active_obelisk: int | None`.
- `self.clouds: list[Cloud]` — `pos`, `velocity`, `shape`.
- `self.pools: set[(int, int)]` — fixed pool cells.
- `self.targets: list[(Sprite, str)]` — `("lit"|"shadow"|"cloud")`.
- `self.chime_ticks: list[int]`.
- `self.tick: int`.

## Novelty vs reference + prior corpus

- **vs `gg04 — mirror-beam-bounce`**: mirror-beam is a *click to
  rotate one mirror at a time* puzzle where beams travel across
  the board through static filters. Sundial has no rotatable
  beams — the *light source itself moves automatically* and
  shadow strips are projected occlusions, not reflected beams.
- **vs `lq5x — lantern-cone-illuminate`**: lantern-cone is a
  player-walked light source illuminating cells in a cone.
  Sundial has the inverse: light fills the lawn by default and
  obelisks *carve out* shadow strips, with the sun moving
  autonomously.
- **vs `gg11 — tide-current-drift`**: tide-current sets a global
  drift direction on the player's command. Sundial's analogous
  global state (sun position) is **automatic and irreversible**,
  giving the puzzle a stopwatch quality the rest of the corpus
  lacks.
- **vs original spec**: the original `shadow-cast-occlude` had
  the player toggle the light direction with ACTION5. The
  revised version makes the sun advance automatically — turning
  a static light-rotation puzzle into a moving-target tracking
  puzzle.

## Step budget

- L1: 18.
- L2: 35.
- L3: 70.

## Random-resistance

Random clicks select random obelisks; random arrows move them
randomly; the sun is on a fixed schedule. Hitting all targets at
the chime tick by random arrow noise is exponentially small once
the level has 4+ targets. Cloud-shadow targets on L2 in particular
require the obelisk to be in *exactly* one column at the chime
tick.

## Planning depth

- **L1:** moderate — backward reasoning from the chime tick about
  where each obelisk must stand.
- **L2:** deep — coordination between obelisk positions and cloud
  arrival; the player must compute where the cloud will be at
  chime and pre-position obelisks.
- **L3:** very deep — pool reflections turn each obelisk into a
  multi-axis blocker (it must occlude *both* the direct sun and
  one or more pool-reflected rays at the chime tick).
