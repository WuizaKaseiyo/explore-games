# Mechanic pick — vp6h

## game_id
`vp6h` (4 chars, lowercase alphanumeric, not English word, not in
the 25 reference IDs, not in `prior-games/index.md`).

## mechanic_family
`shadow-cast-collect`

## Seed
None (autonomous).

## One-paragraph mechanic description

A bright "lit field" floods the playfield from a single horizontal
**lantern bar** mounted on the top edge — picture parallel rays
streaming straight downward across every column. Opaque **pillar**
obstacles cast vertical **shadow strips** behind them; cells in those
strips are dark, every other cell is bright. The avatar walks the
playfield (cardinal arrows). Scattered through the playfield are
**crystal** sprites the avatar must collect — but a crystal is only
*pickable* while standing in a shaded cell. Stepping onto a crystal
that is currently lit *destroys* it (one fewer crystal toward the
collect-all win). The player repositions the lantern by clicking any
column on the rail at the top edge: the lantern slides to that column
and the shadow strips snap to the new geometry. L2 introduces the
need to reposition: multiple crystals exist whose shaded columns are
disjoint from one another, so the player must move the lantern between
pickups. L3 introduces a **second lantern** on a parallel rail (same
top edge, distinct y-row): now lit ∪ lit is hostile (a crystal lit by
either lantern is destroyable), and only the **intersection** of
both shadow fields is safe-pickup territory, requiring deliberate
joint placement of both lanterns per crystal.

## Action mapping

| Slot | Verb |
|---|---|
| ACTION1-4 | Walk avatar one cell N/S/W/E |
| ACTION6 | Click any cell on a lantern's top-edge rail to slide that lantern to the clicked column (snap-to-x). At L3, click resolves to whichever lantern's rail row was clicked. |

`available_actions = [1, 2, 3, 4, 6]`. ACTION5 unused (and unavailable
to the agent), ACTION7 (undo) unused.

## Mechanics inventory (per the +1/+2 rule)

- **M1 — shadow-pickup:** crystals can only be picked up while
  standing in a shaded cell; lit crystals are destroyed when the
  avatar steps on them. (Active L1, L2, L3.)
- **M2 — lantern-slide:** click on the lantern rail repositions the
  lantern; shadow geometry recomputes. (Introduced L2; active L2, L3.)
- **M3 — dual-shadow-overlap:** a second lantern with independent
  rail; safe-pickup zone is the *intersection* of the two shadow
  fields. Single-shadow cells become hostile. (Introduced L3.)

L1 = M1.  L2 = M1 + M2 (+1).  L3 = M1 + M2 + M3 (+1).

## Novelty — taxonomy near-misses

### lq5x (prior) — `lantern-cone-illuminate`

Closest near-miss. A "lantern" sprite plus collection-on-light is a
shared signature. Concrete distinguishing rules:

1. **Geometry inversion.** lq5x's safe zone is the *interior of a
   directional cone* projected from a player-carried lantern; my
   safe zone is the *occlusion* — the shadow strip *behind* an
   obstacle. The player's mental model is opposite: lq5x =
   "bathe targets in light"; vp6h = "block light from reaching
   crystals so they survive."
2. **Light field topology.** lq5x emits a *cone* (3-wide directional
   wedge) that rotates around the avatar with ACTION5. vp6h emits a
   *parallel-ray field* across the entire playfield (no cone, no
   directionality — strictly downward).
3. **Lantern locus.** lq5x's lantern is *carried* by the avatar;
   the avatar's position fixes the cone's apex. vp6h's lantern is
   *stationary on a 1D top-edge rail* and is repositioned by ACTION6
   click on the rail; the avatar and lantern are decoupled controls.
4. **Win condition.** lq5x wins by tinting target rings with the
   correct cone-colour (match colour pickup → match target ring).
   vp6h wins by collecting all crystals (no colour-tinting; crystals
   are colour-uniform within a level).
5. **L3 mechanic.** lq5x L3 (per the prior's index entry) is "wax
   pickups extend cone range, filters re-tint cone colour" — a
   single-cone modification. vp6h L3 introduces a *second
   independent lantern* and the **shadow-intersection rule** — a
   compositional change in how safe zones are computed, not a
   single-cone modification.

Negative-similarity walk vs lq5x's level_1.png:
- (1) On board — both have lantern + avatar + walls + collectibles. **Shared.**
- (2) Verb — lq5x walks-and-rotates; vp6h walks-and-clicks-rail. Different.
- (3) Goal — lq5x match-by-tint; vp6h collect-all-by-occlusion. Different.
- (4) Loss — both step-counter. Shared.
- (5) Supporting cast — universal (walls + targets). Shared.
- (6) Visual signature — lq5x is *mostly dark with a bright cone*;
  vp6h is *mostly bright with vertical dark shadow strips*. Inverse.
- (7) Pixel grain — vp6h crystals are multi-cell internally-patterned
  sprites (irregular crystalline shape); avatar is a 3×3 with
  visible internal structure. lq5x sprites in level_1.png are
  uniform-coloured square frames (less grain). Different.
- (8) Core dynamic — opposite (light=hostile vs light=safe).
  Different.

Shared on 1, 4, 5 (universal-ish), differing on 2, 3, 6, 7, 8.
Below the 3+ threshold; clear divergence on the heavy axes (6, 8).

### bx84 (prior) — `beam-mirror-reflect`

Both involve "directed light geometry." Distinguishing rules:

1. **Light topology.** bx84 routes a *single coloured beam* that
   travels in a straight line and *reflects* at 90° off mirrors
   (line-of-sight). vp6h has no beam: parallel rays from an entire
   horizontal bar light a 2-D field, and there are no mirrors.
2. **Player verb.** bx84 places mirrors and cycles their orientation
   via ACTION6 click. vp6h has no mirrors and no orientation;
   ACTION6 only slides the lantern along its rail.
3. **Win condition.** bx84 wins when the beam reaches a target.
   vp6h wins by walking the avatar onto every crystal while in
   shadow.

### lf52 (reference) — `fog-of-war-sokoban`

Both involve "darkness on the playfield." Distinguishing rules:

1. **Visibility model.** lf52 has *avatar-centred fog of war*: cells
   far from the avatar are hidden (visibility = function of avatar
   position). vp6h has no fog — every cell is always visible; the
   *light/shadow* state is a function of *lantern + obstacle*
   geometry, independent of avatar position.
2. **Verb.** lf52 = walk + push-block (sokoban) + reveal-flash
   (ACTION6 click bottom-left corner). vp6h = walk + click-on-rail.
   No push-block, no flash.
3. **Win condition.** lf52 = push the block onto the target.
   vp6h = collect all crystals.

### ar25 (reference) — `reflection-rotation-fit`

Cosmetic surface overlap (both involve "reflection" idea). But ar25
is about *reflector lines* mirroring sprites for tile-fitting; it
has nothing to do with light or shadow. No descriptive overlap.

### kn58 (prior) — `anchor-pull-magnet`

Both involve "click on the playfield to influence the field." But
kn58 produces a *force vector* sliding pawns; vp6h produces a
*shadow geometry* affecting pickup-safety. Different physics
domain entirely.

### gv47 (prior) — `seed-grow-surround-dissolve`

Both have "regions" on the playfield. gv47 = paint regions grow by
clicking seeds (region growing); vp6h = shadow strips computed from
lantern + obstacles (geometric occlusion, not growth). No
mechanical overlap.

## Novelty — `prior-games/index.md` near-misses

Index has 17 priors. Closest in flavour:
- **lq5x** — addressed above (most rigorous distinguishing rules).
- **bx84** — addressed above.
- **kn58** — addressed above.
- **gv47** — addressed above.
- **fz5j (phase-step-tile)** — fz5j has tiles auto-pulse open/closed
  on per-cell periods; vp6h has no per-cell schedule, no auto-tick;
  shadow state is purely a geometric function of lantern position.
  Different temporal model (player-driven vs deterministic schedule)
  and different cause-of-state (occlusion vs schedule).

Every other prior (kf42 tether, qz73 radial-tip-lock, kx14 tide-tilt,
qb84 bead-lift-swap, hr8q pair-blend-recipe, ng52 multiset-classify,
pj7k rolling-cube, pz4t anchor-pivot-place, vn8d domino-cascade,
wt39 glide-deflect-thaw, zk9p pursuer-merge, rk7x live-switch-routing)
is mechanically far enough that family-level overlap fails — no
distinguishing-rule paragraph required.

## Negative-similarity-check verdict

For every flagged near-miss above, the candidate shares fewer than
three of the eight dimensions in
`mechanic-novelty/negative-similarity-check.md`. The heavy axes
(visual signature, pixel grain, core dynamic) diverge cleanly
against lq5x — the closest prior. The candidate passes.
