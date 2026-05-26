# Mechanic Pick

## Game ID
`lv4k`

Verified non-colliding:
- not in the 25 reference IDs (ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15, tn36, tr87, tu93, vc33, wa30)
- not in `prior-games/index.md` (kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, vn8d, fz5j, kn58, bx84, wt39, zk9p, rk7x, gx7m, vp6h)
- lowercase alphanumeric, 4 chars, doesn't spell a word

## Mechanic family
`lever-balance-torque`

## One-paragraph description

A horizontal beam pivots on a fulcrum mounted at one of several discrete positions. The beam has 2N+1 evenly-spaced *slots* (a slot is a fixed 4-cell region along the beam). A *tray* below the beam holds a small set of *weight sprites*: each weight has integer mass (visualised as the sprite's footprint size — a 1-mass weight is a 4×4 ring; a 2-mass weight is a 4×8 doubled ring). The player clicks a tray weight to select it (ACTION6), then clicks a beam slot to place it there. Once placed, the beam computes its **net torque** = Σ (mass × signed-distance-from-fulcrum) and renders the beam at the corresponding *tilt level* (−2 ≤ tilt ≤ +2). The level wins when every tray weight has been placed AND the beam's tilt level is exactly 0 (balanced). The game is **turn-based** and **deterministic** (no `random` in `step()`); animation between turns is a 3-frame tilt-level interpolation rendered into the beam sprite's pixels. ACTION5 picks up a previously-placed weight back into the tray (so the player can revise). A step-counter HUD bar drains 1/action and fires `lose()` at zero.

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION5 | Lift the highlighted beam-slot's weight back to the tray | a placed weight is highlighted (most-recently-placed) |
| ACTION6 | Click a weight in tray (selects it) OR click a beam slot (places selected weight there) | always |

(`available_actions=[5, 6]`. Pure click + modal-lift. No directional motion — slot positions are absolute, no avatar.)

## Per-level mechanic progression

| Level | Mechanics required by the witness | What the L*N* witness exercises | Step budget |
|---|---|---|---|
| L1 | M1: **place-balance** — place weights from tray onto symmetric slots about the fulcrum to zero net torque | Two equal-mass weights, central fulcrum, 5 slots. Witness: place one weight on slot −1, the other on slot +1. Beam shows tilt-level 0. | 12 |
| L2 | M1 + M2: **mass-arm-asymmetry** — weights of differing mass at differing distances must satisfy Σ(mass × arm) = 0; equal-distance placement no longer balances | One mass-2 weight + two mass-1 weights, off-center fulcrum (slot +1), 7 slots. Witness: place mass-2 at slot −2 (arm = −3 from fulcrum at +1; contribution −6), then both mass-1s at slot +4 (arm = +3 each; contribution +3+3 = +6). Tilt = 0. | 24 |
| L3 | M1 + M2 + M3: **tilt-passenger-slide** — a passenger sprite sits on the beam at a fixed start-slot; on every commit, if `|tilt| ≥ 2` the passenger shifts toward the lower end by 1 slot; if it falls off the beam, level loses immediately | Mass-2 weight + mass-1 weight + (3) mass-1 weights, asymmetric fulcrum (slot +1), 7 slots, passenger initially at slot +3. Witness: a placement order that keeps `|tilt| ≤ 1` after each commit, ending at tilt 0 with the passenger still on the beam (e.g. mass-2 at slot 0 first → tilt −1; then mass-1 at slot +3 → tilt 0; then alternating placements that maintain `|tilt|≤1`). The naive "place-all-mass-2-first" fails because intermediate tilt = −2 displaces the passenger off the beam. | 36 |

(For mechanic counting per checklist item 11: L1 has 1, L2 has 2, L3 has 3. Each level inherits all prior mechanics. +1 per level.)

## Win / Lose

- **Win (per level)**: all tray weights placed AND beam tilt = 0 → `next_level()`.
- **Lose**: step counter reaches 0 OR (L3 only) passenger displaced off the beam end (slot index out of range).

## Novelty: similarity-check (positive)

For every taxonomy entry and prior, I compared family-tag and mechanic-description.

### No family-name overlap with any taxonomy entry
None of the 25 reference families share even the first hyphen-token with `lever-balance-torque`:
- closest tokens: `tilt` (none), `balance` (none), `torque` (none), `lever` (none).

### No family-name overlap with prior-games
- `kx14` (`tide-tilt-buoyant`): "tilt" appears, escalate to description-level check.
- All others: no token overlap.

### Description-level check vs `kx14` (the only taxonomy/prior near-miss)

`kx14` per `prior-games/index.md`: *"vertical fluid tank where ACTION1/2 raise/lower the water surface, ACTION3/4 tilt floating balls, ACTION6 anchors."*

Concrete distinguishing rule: kx14's "tilt" is a **fluid surface inclination** mechanic — tilting changes which cells contain water, and floating balls move by buoyancy. `lv4k`'s "tilt" is a **rigid-body torque** mechanic — the beam is a single rigid object whose angular displacement is a pure function of placed-weight positions; there is no fluid, no buoyancy, no surface, no anchor verb. The win predicate is also distinct: kx14 = balls reach target cells via buoyancy; lv4k = tilt = 0 after all weights placed. The win-state is *configurational*, not *positional*.

### Description-level check vs other plausible "physics" priors

- `bp35` (`gravity-fall-navigation`): the **player itself** falls under gravity; lv4k's beam pivots, but the player never falls and the beam's tilt is computed not animated under continuous gravity. Different agent (avatar vs. inanimate beam) and different action paradigm (side-step while falling vs. click-place weights).
- `pj7k` (`rolling-cube-face-paint`): face-painting on a rolling cube traversal. lv4k has no walking, no painting, no traversal — only weight placement.
- `vn8d` (`domino-cascade-topple`): chain-reaction topple from a single click. lv4k has no chains; placements are independent and net-additive.
- `gx7m` (`gear-mesh-cascade`): gear rotation transmission. Different concept (rotation vs. equilibrium).
- `pz4t` (`anchor-pivot-place`): jigsaw-style tiling, where "pivot" is a sprite-rotation hint for placement; nothing physical pivots. lv4k's pivot is a rigid-body fulcrum that determines torque arms.
- `kn58` (`anchor-pull-magnet`): pieces slide toward a clicked anchor. Different mechanic — there's pull, here there's torque.

### Decision matrix verdict
| Family match | Description match | Distinguishing rule? | Verdict |
|---|---|---|---|
| `kx14`: partial-token "tilt" | no | n/a | NOVEL (cosmetic family-name overlap) |
| all other entries | no | n/a | NOVEL |

## Novelty: negative-similarity-check (looking for too much in common)

Walked the 8 dimensions of `negative-similarity-check.md` against every prior whose visual or mechanical signature could plausibly resemble a beam-with-weights game.

Reviewed the L1 rendered initial frames of: `kx14`, `pz4t`, `vp6h`, `gx7m`, `pj7k`, `kn58` (read directly from each prior's `run-archive/smoke-frames/level_1.png`). Read `vc33` and `lp85` by deep-analysis text.

| Prior | (1) Board | (2) Player verb | (3) Goal | (4) Lose | (5) Cast | (6) Visual signature | (7) Pixel grain | (8) Core dynamic | Shared dims |
|---|---|---|---|---|---|---|---|---|---|
| `kx14` | tank/water vs. beam/tray | tilt + anchor vs. click-place | balls reach cells vs. tilt-zero | step counter (both) | balls/water vs. weights/beam | cyan-water-half vs. mid-grey-with-beam | 4×4 ring vs. multi-pixel weight | buoyancy-routing vs. equilibrium | 1 (lose mode) |
| `pj7k` | open arena + cube row vs. beam/tray | walk/roll vs. click-place | face-paint match vs. tilt-zero | step counter | colored cubes vs. weights | 3 cubes line at top vs. horizontal beam mid | similar 4×4 cubes/rings | rolling-permute vs. equilibrium | 1 |
| `vc33` | striped row of stones vs. beam | click marker vs. click-place | colour-pair vs. tilt-zero | step counter | stones/rails vs. weights/beam | striped vs. beam | 4-pixel stones vs. weights | swap-stripe vs. equilibrium | 1 |
| `pz4t` | jigsaw region vs. beam | click+arrows+rotate vs. click | tile fill vs. tilt-zero | step counter | jigsaw bits vs. weights | colored rectangles vs. beam | similar pixel rects | rotation-place vs. equilibrium | 1 (kill) |
| `kn58` | scattered pawns vs. beam/tray | click anywhere vs. click-place | pawns-to-targets vs. tilt-zero | step counter | pawns/anchor vs. weights/beam | small pawns on grid vs. beam | small pixels both | one-shot pull vs. equilibrium | 1 |
| `lp85` | small grid + buttons vs. beam | click button vs. click slot | piece-on-goal vs. tilt-zero | step counter | grid pieces vs. weights | grid + buttons vs. beam | similar pixels | row/col permutation vs. torque | 1 |

No prior shares 3 or more dimensions. The dominant differences:
- **Visual signature (dim 6)**: a single horizontal beam dominating the centre with a fulcrum + tray below and a weight-tray vocabulary is *not* shared with any prior. Most priors render scattered pieces on a grid; lv4k's anchor is a rigid linear element.
- **Core dynamic (dim 8)**: torque equilibrium is genuinely absent from the 44 priors. Even the "tilt" priors (`kx14`, `sp80`'s rotation tilt) tilt for input-axis or fluid-surface reasons, not for rigid-body equilibrium.
- **Player verb (dim 2)**: `lv4k` is *click-only* with a modal lift (ACTION5), no walking. About 6/44 priors are pure click but those (`vc33`, `lp85`, `r11l`, `ft09`, `sb26`, `su15`) all use click on grid cells for placement/cycling/swap, not for placing weights on a discretised beam slot.

### Verdict: NOVEL on both positive and negative checks.

## Implementation feasibility

- Beam: a fat horizontal sprite (e.g. 56×4 cells) whose pixels are recomputed per `step()` from the current tilt level. Each tilt level pre-computes a row-shifted version of the beam pattern (one end raised, other lowered) — done in pure numpy on the sprite's `pixels` array.
- Fulcrum: a small triangle sprite (4×4) at fixed beam-x.
- Slots: invisible "click-target" sprites along the beam (used by `level.get_sprite_at(x, y, "slot_tag")` for click hit-detection).
- Weights: 4×4 (mass 1) or 4×8 (mass 2) sprites with internal pixel structure (rings) — passes the 32×32-info-loss check.
- Tray: a row of weight slots below the beam, also 4×4 click-targets.
- Passenger (L3): a 4×4 sprite that occupies a beam slot. Slides one slot per turn when `|tilt| ≥ 2`.
- Tilt computation: pure integer arithmetic — `Σ mass[i] * (slot_idx[i] − fulcrum_idx)`, then map to discrete tilt-level via signum thresholds.
- Step counter HUD: standard `RenderableUserDisplay` bar at row 0 or 63.

No randomness in `step()`; full determinism preserved for replay.
