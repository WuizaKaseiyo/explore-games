# Mechanic pick — cv5b

## ID
`cv5b` — verified non-colliding with the 25 reference IDs and with the 75
entries in `prior-games/index.md`. Not an English word.

## Mechanic family tag
`arc-launch-target`

## One-paragraph description
**Arc-Launch Target Practice.** A movable *launcher* avatar walks the
playfield (ACTION1-4). It carries an integer *power level* that the player
cycles with ACTION5 across a small set of preset values (e.g. 1..3 — short,
medium, long). At any moment a *preview-arc* of small dotted pixels is
rendered from the launcher into the playfield, showing the parabolic
trajectory a marble would follow at the current power if fired in the
launcher's facing direction. Pressing ACTION6 anywhere on the preview-arc
*fires*: the marble is animated cell-by-cell along the parabolic path over
several frames, finally landing on the arc's terminal cell. If the landing
cell is a *target ring*, the target is captured (consumed). If the path
*passes through* (overlaps) a *shield bar* — a tall vertical wall sprite
with non-zero height — the marble is absorbed mid-flight (no target hit;
counted as a miss). Some targets at L3 are *raised* (read as "high") and can
only be hit if the arc apex is above their lip; others are *low* and can
only be hit by a flat, low-power arc. Win = every target captured; lose =
step budget exhausted. The mechanic combines basic physics (parabolic
gravity-bound trajectory), geometry (apex height vs barrier height), and
objectness (launcher / marble / shield / target as persistent entities).

## Closest taxonomy entries — distinguishing rules

### vs `cd82` (orbit-fire-paint, ref)
- *Description from taxonomy:* paint-tank rides an 8-slot ring around a central
  canvas; ACTION5 fires the tank inward to splash colour into a sector of the
  canvas.
- **Distinguishing rule (concrete):** cd82's tank is *fixed to an 8-slot ring
  surrounding the canvas* (positions are constrained to one of 8 angular
  slots) and fires *inward in a straight axial slab* (rectangle or triangle)
  at the canvas; cv5b's launcher walks *freely on a 2D playfield* and emits a
  *single marble along a parabolic arc* with adjustable range and apex height.
  cd82 paints; cv5b consumes a target. cd82 has no barrier-clearance; cv5b's
  whole novelty is *clearing shields by arcing over them*.

### vs `bp35` (gravity-fall-navigation, ref)
- *Description from taxonomy:* pawn auto-falls one row per step under gravity;
  side-step to land on platforms; gravity-flippers and portals at later levels.
- **Distinguishing rule (concrete):** bp35 the *player IS the projectile*
  under continuous gravity, with side-step inputs steering the fall; cv5b the
  *player walks a launcher* that *emits* a marble — the launcher itself never
  falls. bp35 has flippers/portals re-routing the player; cv5b has a parabolic
  arc whose *apex* is set by power-cycle and whose *direction* is set by the
  launcher's facing. The control loop, the entity that follows gravity, and
  the win condition (reach gem at end of fall) are different.

### vs `r11l` (centroid-puppet-leg, ref)
- *Description:* click a footprint then a destination; drags the footprint
  across a corridor; centroid follows.
- **Distinguishing rule:** r11l has *no projectile* — it physically slides a
  leg-sprite across the grid; the head's centroid follows linearly. cv5b
  emits a marble that traces a *parabolic curve* through air; only the
  landing cell matters, not the path's grid neighbours.

## Closest prior-games entries — distinguishing rules

### vs `bx84` (beam-mirror-reflect, prior)
- *Description:* emitter shoots a coloured beam; click empty cells to drop
  mirrors; mirrors reflect at right angles; L2 filter recolours, L3 prism
  splits east+south.
- **Distinguishing rule (concrete):** bx84 has a *static emitter* and the
  player *places mirror cells* that bend the beam at *right angles only*; the
  beam's path is *linear segments* and is fully determined by mirror placements.
  cv5b has a *mobile launcher* (player walks it) and a *parabolic curve*
  (continuous, not line-segments) — there is *no mirror placement*. cv5b's
  power-level cycle changes the *length* of the arc, an axis bx84 has no
  analogue for. cv5b's shields *block* the arc mid-flight; bx84 mirrors
  *redirect*.

### vs `vt6q` (grapple-anchor-yank, prior)
- *Description:* fire a directed cardinal grapple line; heavy anchor yanks
  avatar, light anchor yanked into socket.
- **Distinguishing rule (concrete):** vt6q's grapple line is *cardinal only*
  (up/down/left/right) and *yanks an entity*; cv5b's arc is a *2D parabolic
  curve* with a free-angle clicked landing cell and *no yanking* — the
  marble is consumed at landing and the launcher does not move. vt6q has no
  power-cycle and no arc-clearance over barriers.

### vs `qn7w` (pulse-chain-eject, prior)
- *Description:* click pushers to fire momentum pulses through stationary
  ball-chains; only the terminal ball ejects per pulse.
- **Distinguishing rule (concrete):** qn7w's pulses propagate through
  *pre-placed chains of balls*; the trajectory is determined by chain
  topology (linear segments through pre-placed entities). cv5b has *free-air
  parabolic flight* with no pre-placed chain — the arc is determined by
  power and direction, not by entity topology. qn7w ejects from chain end;
  cv5b lands on a clicked cell.

### vs `pf3w` (wavefront-converge-timing, prior)
- *Description:* click slots to activate emitters; ACTION5 ticks each
  emitter's BFS-radius wavefront outward; win when target receivers
  coincide with a frontier cell.
- **Distinguishing rule (concrete):** pf3w's wavefront is *radially-symmetric
  BFS* (expanding ring); cv5b's arc is *directional + parabolic* (single curve
  in 2D). pf3w's win is *temporal coincidence* across multiple wavefronts;
  cv5b's win is *spatial landing on a ring*. No overlap on the visualisation
  (ring expansion vs single arc) or on the player verb (multi-emitter
  activation vs walk+power+aim).

### vs `lq5x` (lantern-cone-illuminate, prior)
- *Description:* single lantern projects a 3-wide directional cone; arrows
  walk, ACTION5 rotates; wax pickups extend cone range; coloured filters.
- **Distinguishing rule (concrete):** lq5x's cone is a *static projection*
  from the lantern that *fills* a wedge of cells until the lantern moves;
  cv5b's arc is a *single-shot trajectory* that fires on click, animates,
  and resolves at one landing cell. lq5x's "range" is wax-pickup-bounded;
  cv5b's power is cycled by an action — no pickup in the loop. The cone is a
  filled region; the arc is a curved line.

### vs `kn58` (anchor-pull-magnet, prior)
- *Description:* click any cell to place a magnetic anchor; coloured pawns
  slide one cell along Manhattan toward it.
- **Distinguishing rule (concrete):** kn58 is *attraction* — every coloured
  pawn drifts toward the anchor cell. cv5b is *projection* — a single marble
  flies on a parabola from the launcher to a clicked landing cell, with no
  attraction field. Different verbs, different geometry.

## Negative-similarity check — vs the closest prior (bx84)
Walking the 8 dimensions of `negative-similarity-check.md`:

1. **What is on the board.** bx84: emitter + mirrors (placed cells) + filters
   + prism + targets. cv5b: launcher (mobile) + shields (vertical bars) +
   targets (rings) + arc-preview-dots. Distinct casts; no shared entity kind
   beyond "target".
2. **What the player physically does.** bx84: click empty cells to drop
   mirrors; click mirrors to cycle. cv5b: walk launcher (arrows) + cycle
   power (ACTION5) + click landing cell (ACTION6) to fire. The walking-the-
   launcher dimension is fundamentally absent in bx84.
3. **What the level is asking for.** Both: hit all targets. Shared.
4. **What kills the player.** Both: step budget. Shared.
5. **The cast of supporting elements.** Different supports (mirrors+filters
   vs shields+arc-preview).
6. **Visible visual signature.** bx84 dominates with linear coloured-beam
   line + scattered mirror cells. cv5b dominates with a curved dotted
   pre-trajectory + tall vertical shield bars. Visually distinct at a
   glance.
7. **Pixel grain of primary sprites.** bx84 mirrors are simple
   diagonal tiles. cv5b launcher has a richer internal pattern (charge
   indicator + facing wedge). Different grain.
8. **The core dynamic.** bx84: place mirrors so a static beam reaches a
   target — a *spatial layout* puzzle. cv5b: walk + power-cycle + click
   so a parabolic arc *clears* a shield to land on the target — a
   *trajectory-vs-barrier* puzzle. Different mental model.

Shared dimensions: 3 (level goal), 4 (lose). Score: **2 / 8.** Well below
the 3-of-8 reject threshold. **PASS.**

## Verdict
NOVEL. Proceeding to write_spec with id=`cv5b`,
mechanic_family=`arc-launch-target`.
