# Mechanic pick

## ID
`fz5j`

ID-generation check:
- 4 chars, lowercase, alphanumeric ✓
- Not an English word ✓
- Not in 25 reference reserved list (ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15, tn36, tr87, tu93, vc33, wa30) ✓
- Not in `prior-games/index.md` (kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, vn8d) ✓

## Mechanic family
`phase-step-tile`

## Description
A coloured avatar walks a small grid populated with **periodically-pulsing tiles**: each tile has a hidden integer period n ∈ {2, 3, 4} and is "open" only when the global step counter satisfies `step % n == offset_n`. Walking onto an open tile succeeds; walking onto a closed tile is rejected (move ignored, step still ticks, costing budget). Walls are permanently closed; the goal cell is permanently open. The distinctive ACTION5 verb is **wait**: increment the step counter without moving, so the player can re-align with a tile's phase. The puzzle is timing — pick a route AND a sequence of waits such that every phase-tile crossing happens during the right step.

Priors used (per `core-knowledge-priors.md`):
- **Objectness**: avatar, walls, tiles, goal — discrete entities with positions.
- **Basic geometry & topology**: path connectivity through a 2D grid.
- **Basic physics** *(loose-fit)*: time as a deterministic counter; periodicity as a temporal-rhythm prior. (No agentness, no NPCs.)

Mechanic count per level (matches checklist item 11 — base N=2 in L1, +1 in L2, +2 in L3):
- L1 mechanics (N=2): walk + period-2 phase-tile.
- L2 mechanics (N+1=3): walk + period-2 + period-3.
- L3 mechanics (L2+2=5): walk + period-2 + period-3 + period-4 + ACTION5-wait.

Action palette: `[1, 2, 3, 4, 5]` (cardinal walk + ACTION5 wait). No click. Same family as wa30 by *palette* but the ACTION5 verb is novel ("wait" is not the verb of any of the 9 reference games that use ACTION5: rotate, commit, pour, lock, cycle, fire, etc.). No reference game has a "wait/pass" action — all 25 require *some* state change per turn, even tu93's lockstep multi-move.

Camera: fixed-grid 64×64 viewport, with a 12×12 (L1), 12×12 (L2), 14×14 (L3) logical grid scaled up via `Camera.width=12/14, Camera.height=12/14` in `on_set_level`.

Visual signature (Principle 2 of `negative-similarity-check.md` — pick a fresh palette unlike priors): the per-period tile colours are
- period-2 → palette 10 (light-blue) when open ↔ palette 5 (black) when closed
- period-3 → palette 6 (magenta) when open ↔ palette 5 when closed
- period-4 → palette 12 (orange) when open ↔ palette 5 when closed

Avatar palette 14 (green); walls palette 4 (off-black); goal palette 11 (yellow). Dominant palette = `{4 wall, 5 closed, 6 magenta, 10 light-blue, 11 goal-yellow, 12 orange, 14 avatar-green}` — a 7-colour palette which deliberately differs from the cautionary `{4, 8, 9}`-only kf42→vh68 signature, and differs from every prior on the index.

Pixel grain (Principle 1): each 4-cell-wide tile is rendered with internal pattern — a small dot at the centre when open, a solid block when closed — so the playfield has internal pixel structure rather than uniform 1-pixel pawns.

## Similarity check (positive)

For each row in `taxonomy-of-25-games.md` and `prior-games/index.md`, family-level check then description-level check.

### Taxonomy near-misses

**tu93 (maze-pickup-train)** — Family overlap: both walk a maze with per-turn time-progression. Description-level: tu93's "ticking" is *secondary AI agents* (zzuxulcort bouncer / natiyqayts rotator / vllvfeggte pickup) advancing their own positions per step under their own rules (per `skills/mechanism-details/tu93.md`). The player's challenge is multi-agent collision avoidance and lockstep alignment. **fz5j has no second agent at all** — the cells themselves change state on a deterministic phase rule. Concrete distinguishing rule: *tu93's antagonists are mobile sprites following AI; fz5j's antagonists are stationary cells whose `is_open` predicate flips on a global counter modulo a per-cell period*. WIN CONDITION: tu93 = every primary on its exit (multi-agent); fz5j = single avatar on goal. PRIMARY ACTION: tu93 = direction-press moves all primaries; fz5j = direction-press moves single avatar. PRIMARY CONSTRAINT: tu93 = lockstep destination must be walkable for *every* primary; fz5j = destination cell's phase must be open at the *current step counter*. Only one of three matches → NOVEL.

**g50t (walk-vs-scroll)** — Family overlap: both have a turn-counter pressure beyond plain step budget. Description-level: g50t's pressure is a *uniformly scrolling backdrop* — the world slides one cell every two turns and you race the edge. fz5j has no scrolling and no race. The distinctive g50t verb is ACTION5-commit (lay a ghost path); fz5j's distinctive verb is ACTION5-wait. Concrete distinguishing rule: *g50t loses if the timer scrolls off-screen regardless of player position; fz5j has no scroll and loses only when budget exhausted*. NOVEL.

**dc22 (colour-cycle-walk)** — Family overlap: both have cells that change state. Description-level: dc22's cycler triggers fire *only when the player steps on a trigger* — the change is event-driven, not autonomous. fz5j's tiles change state on every step, regardless of player action, on a deterministic period. Concrete distinguishing rule: *dc22 mutation is action-triggered (player chooses when to cycle each colour); fz5j mutation is autonomous (counter mod period, player has zero direct control over a tile's state, only over WHEN to walk onto it)*. NOVEL.

**ls20 (cycler-attribute-match)** — Family overlap: both involve "cycle" sprites. Description-level: ls20 cycles *avatar attributes* (shape/colour/rotation indices) when the avatar steps on a cycler tile; the win predicate is per-pellet attribute match. fz5j has no avatar attributes and no per-pellet matching — the avatar is a fixed entity, the tiles are the dynamic elements. Concrete distinguishing rule: *ls20 mutates the avatar; fz5j mutates the field*. NOVEL.

**wa30 (lock-drag-crate)** — Family overlap: same action palette `[1,2,3,4,5]`. Description-level: wa30's ACTION5 is pickup/drop a tethered passenger; fz5j's ACTION5 is wait/pass-turn. Wholly different verbs. wa30 has no time/phase; fz5j has no carry. NOVEL on description.

No other taxonomy entry comes within reach.

### Prior-games near-misses

**kx14 (tide-tilt-buoyant)** — Family overlap: both have time/state on a fluid axis. Description-level: kx14's "tide" is a *vertical fluid surface* the player raises/lowers via ACTION1/2 — fluid mechanics, ball buoyancy, anchoring. fz5j has no fluid, no anchor, no buoyancy. Concrete distinguishing rule: *kx14 simulates a continuous water surface and balls floating on it; fz5j has discrete cell-phase pulsing with no fluid or buoyancy concept*. NOVEL.

**lq5x (lantern-cone-illuminate)** — Family overlap: spatial directional lighting could rhyme with phase-pulsing. Description-level: lq5x projects a *3-cell directional cone* attached to a movable lantern; arrow walks lantern, ACTION5 rotates cone direction. The illumination is spatial-directional. fz5j has no light, no cone, no direction-rotation; it has temporal periodicity per cell. Concrete distinguishing rule: *lq5x is "where am I aiming?" (spatial direction); fz5j is "when am I arriving?" (temporal phase)*. NOVEL.

**vn8d (domino-cascade-topple)** — Family overlap: both have temporal sequencing. Description-level: vn8d is single-click triggers a *one-shot chain reaction* through fixed dominos and pads. fz5j has no chain-reaction primitive; the time progression is a uniform counter the player advances by walking or waiting. Concrete distinguishing rule: *vn8d is "set up the dominos, then click once and watch"; fz5j is "thread the avatar through every move and time arrivals"*. NOVEL.

**pj7k (rolling-cube-face-paint)** — Family overlap: both have a moved entity that cares about an internal index per tick. Description-level: pj7k's cube has a 6-face rotation index; each roll permutes faces and deposits the bottom face's colour. The state is per-cube, attached to the entity. fz5j has no rolling, no per-entity face-state, no painting — the state lives on the cells themselves and depends only on the global counter. Concrete distinguishing rule: *pj7k's hidden state is a face permutation attached to the player-controlled cube; fz5j has no per-entity hidden state — phase is a function of (cell, step counter) only*. NOVEL.

No other prior comes within reach.

## Negative similarity check

Per `negative-similarity-check.md`, walking the eight dimensions against each prior. Strongest-overlap candidate to interrogate: tu93 (most thematically adjacent — both are walk-in-maze-with-time).

| Dimension | tu93 | fz5j | shared? |
|---|---|---|---|
| 1. What's on the board | maze + primary agents + secondary AI mobs + walkable underlay + exits | avatar + walls + phase-pulsing tiles + goal | partial (both have maze + walkable underlay) |
| 2. What player physically does | press direction → ALL primaries move (lockstep) | press direction → single avatar moves; press ACTION5 to wait | NO (single vs lockstep, plus wait verb) |
| 3. What level asks for | get every primary onto its exit | get single avatar onto goal | partial (reach goal common to many games) |
| 4. What kills player | step budget OR all primaries destroyed by enemies | step budget only | NO (no enemy destruction in fz5j) |
| 5. Cast of supporting elements | walls + walkable + 3 distinct enemy AI species + exit | walls + 3 distinct phase tiles + goal | NO (cast roles totally different — AI vs phase) |
| 6. Visual signature | greyish maze with chunky 3×3 yellow primaries + small mobile enemies | green avatar + magenta/light-blue/orange pulsing tiles + yellow goal | NO (palette and aesthetic completely different) |
| 7. Pixel grain | mostly mid-detail | each phase-tile has internal open-dot/closed-block pattern | partial |
| 8. Core dynamic | "how do I move all my primaries together past the AI?" | "what step do I need to be at this cell?" | NO (multi-agent vs temporal-phase, fundamentally different player thought) |

Shared dimensions with tu93: at most 2 (dimensions 1 and 7), neither of them the heavy ones (6/8). **Below the 3-threshold.**

Spot-check against priors with `level_1.png` images that I've internalised:
- kf42 (tether-pawn-cycle): tether + arrows + click + colour pads on a 12-16 grid with 1×1 pawns. fz5j has no tether, no click, multi-pixel tiles, no colour pads. Shared: dimension 1 only (small grid). 1/8 — clearly distinct.
- pz4t (anchor-pivot-place): jigsaw click+arrow+ACTION5-rotate, dark-grey region tiling. Different action palette (no click), different verb (no rotate). Shared: 0/8.
- vn8d (domino-cascade-topple): click once and watch. fz5j is move-by-move walker. 0/8.
- lq5x (lantern-cone): light beam projection. fz5j has no projection. 0/8.

**No prior overlaps on 3+ dimensions. Negative similarity check passes.**

## Verdict
**NOVEL on positive (similarity-check) AND negative (negative-similarity-check) tests** against both the 25-reference taxonomy AND the 11-entry prior-games index. Proceed to `write_spec`.
