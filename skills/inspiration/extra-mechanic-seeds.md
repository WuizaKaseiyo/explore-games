# Extra Mechanic Seeds

### PS-001 - rule-rewrite-frontier

```yaml
id: PS-001
source: PuzzleScript-style rule rewriting
source_url: https://github.com/increpare/PuzzleScript
fetched_via: synthetic-from-demo-family
last_refreshed: 2026-05-08
family_tag: rule-rewrite-frontier
family_class: symbolic-rewrite
exploration_profile: rule-induction
interaction_type: global-tick
state_surface: visible
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [kp9z, pf3w]
```

**Core mechanic:** A global tick rewrites every marked frontier cell
according to its local neighbourhood, turning frontier cells into walls,
bridges, or blockers.

**Interactive loop:** The player places or toggles a small number of
rewrite markers, then advances the tick and observes how the frontier
materializes.

**Exploration hook:** Early probes reveal which neighbour patterns make
frontier cells become walls, bridges, or blockers.

**Progress signal:** Targets become reachable only after the rewrite
frontier forms a continuous, colour-compatible structure.

**Failure or pressure:** A marker placed one cell too early creates a
permanent blocker or consumes the only bridge path.

**Novelty WRT corpus:** Close to `kp9z` only in global propagation and
to `pf3w` only in wave timing; the distinguishing rule is local symbol
rewrite into terrain, not accumulating grains or synchronizing waves.

**Composition directions:** L1 teaches one marker rule, L2 adds a
second marker type, and L3 requires ordering two rewrites so the first
creates support for the second.

### PS-002 - actor-role-grammar

```yaml
id: PS-002
source: PuzzleScript multi-actor grammar
source_url: https://github.com/Auroriax/PuzzleScriptPlus
fetched_via: synthetic-from-demo-family
last_refreshed: 2026-05-08
family_tag: actor-role-grammar
family_class: multi-actor
exploration_profile: multi-agent-discovery
interaction_type: modal
state_surface: visible
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [vy3m, zd7m]
```

**Core mechanic:** Multiple controllable actors share a board but each
actor interprets the same action vocabulary with a distinct grammar.

**Interactive loop:** The player cycles the active actor, uses the same
directional or modal action, and exploits the selected actor's rule
translation.

**Exploration hook:** The same input produces different visible effects
for each role, inviting the player to map role grammar by trying it.

**Progress signal:** A target arrangement is possible only when each
role performs the transformation that the others cannot.

**Failure or pressure:** Activating the wrong role first moves a shared
object into a region where the necessary role can no longer reach it.

**Novelty WRT corpus:** Near `vy3m` because of class roles, but the
distinguishing rule is action reinterpretation by role rather than fixed
push/pull/stomp verbs.

**Composition directions:** L1 uses two roles with one shared action,
L2 adds a role whose action has an inverse effect, and L3 requires a
role order that defeats greedy nearest-target play.

### PS-003 - wraparound-window

```yaml
id: PS-003
source: PuzzleScript topology patterns
source_url: https://github.com/increpare/PuzzleScript
fetched_via: synthetic-from-demo-family
last_refreshed: 2026-05-08
family_tag: wraparound-window
family_class: topology-transform
exploration_profile: topology-discovery
interaction_type: arrows
state_surface: inferred-rule
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [cohort-step-route, phase-step-tile]
```

**Core mechanic:** Movement wraps through selected board edges, but only
inside a movable or toggled window of rows and columns.

**Interactive loop:** The player shifts the active wrap window and then
walks through what appears to be a disconnected edge.

**Exploration hook:** Safe edge-crossing probes reveal which rows or
columns currently wrap and which ones behave normally.

**Progress signal:** Objects or the avatar reach targets by crossing an
edge whose topology is currently active.

**Failure or pressure:** A wrong window shift sends the avatar or object
to the wrong edge basin and wastes the step budget.

**Novelty WRT corpus:** Similar to routing games only at the surface;
the distinguishing rule is dynamic topology of the board boundary, not
portals, phase tiles, or static graph edges.

**Composition directions:** L1 teaches one wrap pair, L2 adds movable
window alignment, and L3 combines object movement with avatar wrapping.

### PS-004 - local-invariant-balance

```yaml
id: PS-004
source: PuzzleScript constraint demos
source_url: https://github.com/increpare/PuzzleScript
fetched_via: synthetic-from-demo-family
last_refreshed: 2026-05-08
family_tag: local-invariant-balance
family_class: constraint-satisfaction
exploration_profile: constraint-probing
interaction_type: click
state_surface: visible
implementation_risk: low
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [lv4k, ng52]
```

**Core mechanic:** Clicks assign small symbols to cells, and each local
region must satisfy a visible invariant such as balanced counts or
paired colours.

**Interactive loop:** The player toggles symbols while watching local
constraint badges update.

**Exploration hook:** Toggling one shared cell shows how overlapping
regions can be fixed or broken by the same action.

**Progress signal:** Regions light up when their local invariant is
satisfied, and the level wins when all regions are simultaneously valid.

**Failure or pressure:** A choice that satisfies one region can break a
neighbouring region because cells participate in overlapping checks.

**Novelty WRT corpus:** Near `lv4k` and `ng52` in explicit reasoning,
but it uses overlapping local invariants rather than torque arithmetic
or object classification.

**Composition directions:** L1 has disjoint regions, L2 overlaps one
cell between two constraints, and L3 requires solving an ordering where
one toggle fixes two regions but breaks a third.

### PS-005 - inferred-switch-language

```yaml
id: PS-005
source: PuzzleScript induction patterns
source_url: https://github.com/increpare/PuzzleScript
fetched_via: synthetic-from-demo-family
last_refreshed: 2026-05-08
family_tag: inferred-switch-language
family_class: induction
exploration_profile: rule-induction
interaction_type: click+arrows
state_surface: inferred-rule
implementation_risk: high
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [rk7x, bx84]
```

**Core mechanic:** Switches have visible symbols, and the player must
infer the symbol-to-effect mapping from immediate board changes.

**Interactive loop:** The player probes a switch, observes which gates
or paths changed, and then uses the inferred mapping to plan a route.

**Exploration hook:** Each switch press gives immediate visual feedback
that lets the player infer the symbol-to-effect language.

**Progress signal:** Correctly inferred switch effects open a route or
align a path to a target.

**Failure or pressure:** Pressing switches in the wrong inferred order
locks the route into a state that requires reset or exceeds budget.

**Novelty WRT corpus:** Similar to `rk7x` and `bx84` in routing, but
the core is learning a visible symbol language, not toggling known
junctions or placing mirrors.

**Composition directions:** L1 gives one obvious mapping, L2 requires
using two learned mappings, and L3 includes a decoy mapping that looks
locally helpful but blocks the final path.

### PS-006 - one-bit-memory-trail

```yaml
id: PS-006
source: PuzzleScript memory-state patterns
source_url: https://github.com/Auroriax/PuzzleScriptPlus
fetched_via: synthetic-from-demo-family
last_refreshed: 2026-05-08
family_tag: one-bit-memory-trail
family_class: hidden-state
exploration_profile: state-revelation
interaction_type: arrows
state_surface: partially-hidden
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [phase-step-tile, shadow-cast-collect]
```

**Core mechanic:** A visible trail records only the last state bit of
visited cells, and future movement depends on whether a cell was last
entered in mode A or mode B.

**Interactive loop:** The player walks to write a trail state, toggles
mode through a visible pad, and reuses the trail as passable or blocked.

**Exploration hook:** Re-entering cells in different modes reveals that
the trail records the last written state and changes future movement.

**Progress signal:** A route becomes available only after the correct
trail states have been written.

**Failure or pressure:** Walking through cells in the wrong mode writes
the wrong memory and blocks the later return path.

**Novelty WRT corpus:** It shares timed-state flavour with `fz5j`, but
state is written by the player and persists as local memory rather than
cycling by period.

**Composition directions:** L1 writes one bridge, L2 requires revisiting
with the opposite mode, and L3 forces choosing which cells to preserve
for the final route.

### PS-007 - cellular-vote-garden

```yaml
id: PS-007
source: Cellular automata demos
source_url: https://github.com/increpare/PuzzleScript
fetched_via: synthetic-from-demo-family
last_refreshed: 2026-05-08
family_tag: cellular-vote-garden
family_class: cellular-automaton
exploration_profile: system-dynamics
interaction_type: global-tick
state_surface: visible
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [gv47, kp9z]
```

**Core mechanic:** Cells update by a visible neighbour-vote rule, turning
into the majority colour around them after each tick.

**Interactive loop:** The player plants a few coloured seeds, ticks the
board, and steers the automaton toward target colour regions.

**Exploration hook:** Small seed placements show how local majorities
win, tie, or stabilize after each tick.

**Progress signal:** Target cells become the requested colours after a
bounded number of ticks.

**Failure or pressure:** A seed in the wrong neighbourhood makes the
vote cascade stabilize into the wrong colour basin.

**Novelty WRT corpus:** Near `gv47` in colour growth and `kp9z` in
global ticks, but the distinguishing rule is simultaneous neighbour
voting rather than flood region growth or sandpile overflow.

**Composition directions:** L1 uses one colour majority, L2 adds a
tie-breaker symbol, and L3 requires staging two ticks so an intermediate
colour supports the final vote.

### PS-008 - recipe-decay-chain

```yaml
id: PS-008
source: PuzzleScript transformation chains
source_url: https://github.com/increpare/PuzzleScript
fetched_via: synthetic-from-demo-family
last_refreshed: 2026-05-08
family_tag: recipe-decay-chain
family_class: set-or-recipe
exploration_profile: resource-experiment
interaction_type: click
state_surface: visible
implementation_risk: low
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [hr8q, ng52]
```

**Core mechanic:** Chosen items combine into a product, but unused items
decay into lower-tier ingredients after each commit.

**Interactive loop:** The player selects ingredients, commits a recipe,
and manages what remains after decay.

**Exploration hook:** Trying a valid recipe early reveals which unused
ingredients decay and why order matters.

**Progress signal:** Target products are completed in order while enough
ingredients survive for later recipes.

**Failure or pressure:** Making a locally valid recipe too early decays
an ingredient needed for the final product.

**Novelty WRT corpus:** Close to `hr8q`, but the distinguishing rule is
time/order pressure from decay rather than pure formula matching.

**Composition directions:** L1 has one recipe with no decay conflict,
L2 adds a delayed dependency, and L3 requires intentionally preserving
a non-obvious ingredient.

### PS-009 - directed-lineage-graph

```yaml
id: PS-009
source: Graph traversal puzzle patterns
source_url: https://github.com/increpare/PuzzleScript
fetched_via: synthetic-from-demo-family
last_refreshed: 2026-05-08
family_tag: directed-lineage-graph
family_class: graph-traversal
exploration_profile: topology-discovery
interaction_type: click+arrows
state_surface: visible
implementation_risk: low
classic_overlap: pipe-routing-like
usable_as: abstract-inspiration
closest_prior_ids: [rk7x, zd7m]
```

**Core mechanic:** Nodes have visible parent-child arrows; visiting a
node enables only its children unless the player spends a click to
reverse one local lineage.

**Interactive loop:** The player walks through the graph, reverses a
small number of directed edges, and reaches targets in dependency order.

**Exploration hook:** Reversing one local lineage exposes how reachability
changes across the directed graph.

**Progress signal:** Required nodes are visited when their incoming
lineage becomes valid.

**Failure or pressure:** Reversing a tempting edge may disconnect a
later target because reversals are limited.

**Novelty WRT corpus:** It shares routing language with `rk7x` and
`zd7m`, but operates on explicit directed dependency reversals rather
than couriers, anchors, or portals.

**Composition directions:** L1 reverses one edge, L2 adds a fork where
only one reversal order works, and L3 uses a shared ancestor that must
remain reachable for two target branches.

### PS-010 - elastic-quota-field

```yaml
id: PS-010
source: Abstract board mechanic
source_url: local:synthetic
fetched_via: synthetic
last_refreshed: 2026-05-08
family_tag: elastic-quota-field
family_class: constraint-satisfaction
exploration_profile: resource-experiment
interaction_type: global-tick
state_surface: visible
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [lv4k, mr5q]
```

**Core mechanic:** Each region has a visible quota, and a global pulse
redistributes movable tokens from overfull regions to adjacent underfull
regions along marked boundaries.

**Interactive loop:** The player toggles boundaries, pulses the field,
and steers redistribution until all quotas match.

**Exploration hook:** Opening a boundary and pulsing shows surplus tokens
flowing toward deficits, making quotas experimentally legible.

**Progress signal:** Region counters reach zero surplus or deficit.

**Failure or pressure:** Opening a boundary at the wrong time drains a
needed token into a region that cannot send it back.

**Novelty WRT corpus:** Near `lv4k` in balancing and `mr5q` in global
movement, but the distinguishing rule is quota redistribution through
player-selected boundaries.

**Composition directions:** L1 has two regions, L2 adds a third region
as a buffer, and L3 requires using a buffer temporarily before sealing
it to prevent backflow.

### PS-011 - lens-parity-routing

```yaml
id: PS-011
source: Abstract optics pattern
source_url: local:synthetic
fetched_via: synthetic
last_refreshed: 2026-05-08
family_tag: lens-parity-routing
family_class: symbolic-rewrite
exploration_profile: rule-induction
interaction_type: click
state_surface: visible
implementation_risk: medium
classic_overlap: pipe-routing-like
usable_as: abstract-inspiration
closest_prior_ids: [bx84, pf3w]
```

**Core mechanic:** Placed lenses rewrite a beam's parity state rather
than its colour or direction; parity determines which receivers accept
the beam.

**Interactive loop:** The player places or toggles lenses, fires a beam,
and observes parity markers along the path.

**Exploration hook:** Firing through one lens shows a visible parity flip,
then later probes expose how parity history accumulates.

**Progress signal:** Receivers light only when the beam reaches them
with the required parity.

**Failure or pressure:** A lens that makes one receiver valid can flip
the parity needed by a later receiver.

**Novelty WRT corpus:** Close to `bx84` in beam path and `pf3w` in
receiver timing, but the distinguishing rule is symbolic parity rewrite
instead of mirror geometry or wavefront coincidence.

**Composition directions:** L1 teaches one parity flip, L2 requires two
receivers with conflicting parity, and L3 adds a splitter where each
branch needs a different parity history.

### PS-012 - reversible-mask-overlay

```yaml
id: PS-012
source: Abstract overlay mechanic
source_url: local:synthetic
fetched_via: synthetic
last_refreshed: 2026-05-08
family_tag: reversible-mask-overlay
family_class: topology-transform
exploration_profile: topology-discovery
interaction_type: modal
state_surface: visible
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [xn5p, lq5x]
```

**Core mechanic:** A movable mask overlays the board; cells under the
mask invert passability or colour membership until the mask moves.

**Interactive loop:** The player shifts or rotates the mask, walks or
acts under the temporary overlay, then moves it again to expose a new
board interpretation.

**Exploration hook:** Moving the mask over familiar cells reveals that
passability or colour membership is conditional on overlay position.

**Progress signal:** Targets become reachable or colour-valid only when
the mask covers a planned subset of cells.

**Failure or pressure:** Moving the mask too early removes the temporary
condition needed to escape or complete a target.

**Novelty WRT corpus:** Near `xn5p` in region manipulation and `lq5x` in
projected area, but the distinguishing rule is a reversible overlay mask
that changes cell interpretation, not stamped walls or light cones.

**Composition directions:** L1 uses one fixed mask translation, L2 adds
rotation, and L3 requires preserving an exit before moving the mask to
solve a second region.
