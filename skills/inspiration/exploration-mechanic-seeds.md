# Exploration-Heavy Mechanic Seeds

### EXP-001 - echo-probe-materials

```yaml
id: EXP-001
source: Synthetic exploration pattern
source_url: local:synthetic
fetched_via: synthetic
last_refreshed: 2026-05-09
family_tag: echo-probe-materials
family_class: induction
exploration_profile: rule-induction
interaction_type: click
state_surface: inferred-rule
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [bx84, pf3w]
```

**Core mechanic:** Clicking a probe sends an echo through adjacent
materials; each material transforms the echo by a visible rule such as
split, delay, absorb, or invert.

**Interactive loop:** The player probes materials, observes the echo
shape, and arranges or activates probes in an order that reaches target
receivers.

**Exploration hook:** L1 lets the player fire echoes into isolated
materials so each material's transformation can be inferred before
composition is required.

**Progress signal:** Receivers light when they receive the required echo
shape or phase.

**Failure or pressure:** A greedy probe order can consume a one-shot
material or produce the wrong phase for the final receiver.

**Novelty WRT corpus:** Related to signal-routing games, but the core is
discovering material response rules, not steering a known beam path.

**Composition directions:** L1 teaches two materials, L2 composes them
in series, and L3 includes a decoy material whose local success blocks a
later receiver.

### EXP-002 - reversible-cause-lab

```yaml
id: EXP-002
source: Synthetic exploration pattern
source_url: local:synthetic
fetched_via: synthetic
last_refreshed: 2026-05-09
family_tag: reversible-cause-lab
family_class: symbolic-rewrite
exploration_profile: system-dynamics
interaction_type: modal
state_surface: visible
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [gx7m, qz73]
```

**Core mechanic:** ACTION5 toggles between forward and reverse causality
for a small rule network; activating one node either pushes effects
outward or pulls prerequisites inward.

**Interactive loop:** The player flips direction, activates nodes, and
learns when a dependency should be solved forward or backward.

**Exploration hook:** Probing the same node in both causality modes
shows opposite but consistent state changes.

**Progress signal:** Required nodes become satisfied when their visible
dependency arrows are all in the correct state.

**Failure or pressure:** Solving forward too early can satisfy a local
node while making a later prerequisite unreachable.

**Novelty WRT corpus:** It touches rotation/network priors but asks the
player to explore direction of causality rather than propagate rotation.

**Composition directions:** L1 compares one forward/reverse pair, L2
adds a forked dependency, and L3 requires alternating causality modes.

### EXP-003 - sample-and-freeze-field

```yaml
id: EXP-003
source: Synthetic exploration pattern
source_url: local:synthetic
fetched_via: synthetic
last_refreshed: 2026-05-09
family_tag: sample-and-freeze-field
family_class: hidden-state
exploration_profile: state-revelation
interaction_type: click+arrows
state_surface: partially-hidden
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [fz5j, one-bit-memory-trail]
```

**Core mechanic:** The board has a visible scanner that samples a small
region and freezes the sampled state as temporary terrain.

**Interactive loop:** The player moves the scanner, samples a region,
and uses the frozen copy before it melts or is overwritten.

**Exploration hook:** Sampling different regions reveals which state is
copied and how long the frozen copy persists.

**Progress signal:** Temporary bridges or blockers appear where the
sampled pattern is projected.

**Failure or pressure:** Sampling the wrong source copies a blocker or
melts a needed bridge before the route is complete.

**Novelty WRT corpus:** Near periodic and memory-state games, but the
state is discovered through spatial sampling and temporary projection.

**Composition directions:** L1 samples one bridge, L2 reuses a sample as
a blocker, and L3 requires choosing which of two possible source states
to freeze first.

### EXP-004 - affordance-border-test

```yaml
id: EXP-004
source: Synthetic exploration pattern
source_url: local:synthetic
fetched_via: synthetic
last_refreshed: 2026-05-09
family_tag: affordance-border-test
family_class: constraint-satisfaction
exploration_profile: tool-affordance
interaction_type: click+arrows
state_surface: visible
implementation_risk: low
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [xn5p, pz4t]
```

**Core mechanic:** A tool affects only cells on the border between two
visible regions, transforming border membership without changing region
interiors.

**Interactive loop:** The player tests the tool on interior, border,
and corner cells, then uses the learned affordance to reshape regions.

**Exploration hook:** Invalid interior probes do nothing while border
probes visibly swap membership, making the tool's boundary condition
discoverable.

**Progress signal:** Region badges update as border cells are reassigned
to satisfy target quotas.

**Failure or pressure:** Changing the wrong border can disconnect a
region or make a quota impossible within the step budget.

**Novelty WRT corpus:** Related to partitioning, but the core discovery
is the exact affordance boundary of a tool, not free wall stamping.

**Composition directions:** L1 contrasts interior and border cells, L2
adds corners with two possible regions, and L3 requires preserving one
border while changing another.

### EXP-005 - latent-channel-mixer

```yaml
id: EXP-005
source: Synthetic exploration pattern
source_url: local:synthetic
fetched_via: synthetic
last_refreshed: 2026-05-09
family_tag: latent-channel-mixer
family_class: hidden-state
exploration_profile: state-revelation
interaction_type: modal
state_surface: partially-hidden
implementation_risk: high
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [hr8q, mr5q]
```

**Core mechanic:** Objects carry a visible colour and a latent channel
shown only by temporary scanner pulses; mixing depends on both.

**Interactive loop:** The player pulses the scanner, infers latent
channels, and chooses pairings that produce target outputs.

**Exploration hook:** Scanner probes reveal latent channels for one turn,
allowing the player to compare visible colour against hidden channel.

**Progress signal:** Correctly mixed objects display stable output marks.

**Failure or pressure:** Pairing by visible colour alone creates a wrong
output and consumes one of the needed objects.

**Novelty WRT corpus:** Similar to recipe games only in combining; the
distinctive pressure is discovering transient latent state before mixing.

**Composition directions:** L1 scans before one mix, L2 adds a decoy
same-colour object, and L3 requires remembering a channel after it is no
longer displayed.

### EXP-006 - living-constraint-badges

```yaml
id: EXP-006
source: Synthetic exploration pattern
source_url: local:synthetic
fetched_via: synthetic
last_refreshed: 2026-05-09
family_tag: living-constraint-badges
family_class: constraint-satisfaction
exploration_profile: constraint-probing
interaction_type: click
state_surface: visible
implementation_risk: low
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [lv4k, local-invariant-balance]
```

**Core mechanic:** Local badges expose only whether a constraint is
under, exact, or over; the player must infer which cells contribute.

**Interactive loop:** The player toggles cells, watches adjacent badges,
and infers the footprint of each constraint.

**Exploration hook:** Single-cell probes cause multiple badges to change,
letting the player discover overlapping constraint footprints.

**Progress signal:** All badges reach exact status simultaneously.

**Failure or pressure:** Fixing one badge greedily can push a hidden
overlap into overfull status elsewhere.

**Novelty WRT corpus:** It resembles balance and invariant puzzles but
centres on discovering constraint footprints through feedback.

**Composition directions:** L1 has two badges with one overlap, L2 adds a
badge with asymmetric footprint, and L3 includes a decoy cell that
affects no badge.

### EXP-007 - role-memory-handshake

```yaml
id: EXP-007
source: Synthetic exploration pattern
source_url: local:synthetic
fetched_via: synthetic
last_refreshed: 2026-05-09
family_tag: role-memory-handshake
family_class: multi-actor
exploration_profile: multi-agent-discovery
interaction_type: modal
state_surface: visible
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [vy3m, kf42]
```

**Core mechanic:** Actors transfer a one-bit memory mark when they touch;
each role interprets the mark differently on its next action.

**Interactive loop:** The player cycles roles, creates handshakes, and
observes how a marked actor's next action changes.

**Exploration hook:** Safe L1 handshakes reveal each role's response to
receiving or giving the memory mark.

**Progress signal:** Targets accept actors only after the correct mark
has passed through the required role sequence.

**Failure or pressure:** Handshaking in the wrong order gives the mark to
an actor that consumes it without producing the needed effect.

**Novelty WRT corpus:** It is multi-actor but not another fixed verb
roster; the discovery is a transferable state protocol.

**Composition directions:** L1 teaches one transfer, L2 requires a
three-actor chain, and L3 includes a role that erases marks unless used
last.

### EXP-008 - foldout-map-memory

```yaml
id: EXP-008
source: Synthetic exploration pattern
source_url: local:synthetic
fetched_via: synthetic
last_refreshed: 2026-05-09
family_tag: foldout-map-memory
family_class: topology-transform
exploration_profile: topology-discovery
interaction_type: arrows
state_surface: inferred-rule
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [tw94, wraparound-window]
```

**Core mechanic:** Crossing a fold edge unfolds a hidden adjacent panel
and refolds the panel behind the player, changing the active map.

**Interactive loop:** The player tests fold edges, memorizes which panel
appears, and plans a route through temporary map configurations.

**Exploration hook:** Early fold crossings reveal panel adjacency through
visible unfold/refold animation.

**Progress signal:** Needed target panels become active only after the
correct fold sequence.

**Failure or pressure:** A wrong fold can hide the panel containing the
return path or required target.

**Novelty WRT corpus:** It is topology-based, but unlike toroidal wrap it
requires discovering a dynamic map adjacency graph.

**Composition directions:** L1 has one fold pair, L2 adds a three-panel
cycle, and L3 requires entering a panel only after preserving an exit.

### EXP-009 - decaying-toolbox

```yaml
id: EXP-009
source: Synthetic exploration pattern
source_url: local:synthetic
fetched_via: synthetic
last_refreshed: 2026-05-09
family_tag: decaying-toolbox
family_class: set-or-recipe
exploration_profile: resource-experiment
interaction_type: click
state_surface: visible
implementation_risk: low
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [recipe-decay-chain, hr8q]
```

**Core mechanic:** Tools have charges that decay into weaker tools after
use; weak tools can solve different constraints than strong ones.

**Interactive loop:** The player tries tools on test cells, observes
decay, and schedules strong versus weak uses.

**Exploration hook:** L1 includes safe targets where using a tool reveals
both its immediate effect and its decayed follow-up form.

**Progress signal:** Each target accepts only the tool state that matches
its visible constraint.

**Failure or pressure:** Spending a strong tool on an easy target leaves
only weak tools for a later strong constraint.

**Novelty WRT corpus:** It has recipe/order flavour but emphasizes
exploring tool affordances over selecting ingredients.

**Composition directions:** L1 decays one tool, L2 has mutually exclusive
tool order, and L3 requires intentionally creating a weak tool first.

### EXP-010 - observer-dependent-grid

```yaml
id: EXP-010
source: Synthetic exploration pattern
source_url: local:synthetic
fetched_via: synthetic
last_refreshed: 2026-05-09
family_tag: observer-dependent-grid
family_class: topology-transform
exploration_profile: tool-affordance
interaction_type: modal
state_surface: visible
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [reversible-mask-overlay, lq5x]
```

**Core mechanic:** A movable observer changes which cells are considered
adjacent; adjacency is defined relative to the observer's row or column.

**Interactive loop:** The player moves the observer, tests movement or
transfer across cells, and learns observer-relative connectivity.

**Exploration hook:** Moving the observer one step visibly rewires a
small highlighted adjacency set.

**Progress signal:** Objects or signals can cross only when the observer
creates the required adjacency.

**Failure or pressure:** Placing the observer for a local crossing can
break a previously needed connection elsewhere.

**Novelty WRT corpus:** Related to light cones and masks, but the
discovery is observer-relative adjacency rather than projected coverage.

**Composition directions:** L1 uses row adjacency, L2 adds column
adjacency, and L3 requires preserving one connection while creating
another.

### EXP-011 - counterexample-glyphs

```yaml
id: EXP-011
source: Synthetic exploration pattern
source_url: local:synthetic
fetched_via: synthetic
last_refreshed: 2026-05-09
family_tag: counterexample-glyphs
family_class: induction
exploration_profile: rule-induction
interaction_type: click
state_surface: inferred-rule
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [ng52, living-constraint-badges]
```

**Core mechanic:** The player sorts glyphs by an unknown visible feature;
after each placement, the board highlights one counterexample if the
current inferred rule is wrong.

**Interactive loop:** The player places a glyph, reads the counterexample
highlight, revises the rule, and completes the classification.

**Exploration hook:** Early wrong placements are safe and deliberately
show why a naive feature hypothesis fails.

**Progress signal:** Bins stabilize when every glyph satisfies the
inferred feature rule.

**Failure or pressure:** A greedy rule based on colour alone passes early
examples but fails on later shape-colour counterexamples.

**Novelty WRT corpus:** It extends classification by making hypothesis
revision the central interaction, not just matching known signatures.

**Composition directions:** L1 contrasts one feature, L2 adds a
counterexample requiring conjunction, and L3 requires ignoring a decoy
feature.

### EXP-012 - phase-locked-instruments

```yaml
id: EXP-012
source: Synthetic exploration pattern
source_url: local:synthetic
fetched_via: synthetic
last_refreshed: 2026-05-09
family_tag: phase-locked-instruments
family_class: graph-traversal
exploration_profile: system-dynamics
interaction_type: global-tick
state_surface: visible
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [pf3w, gx7m]
```

**Core mechanic:** Instruments on a graph pulse on visible phases; a
pulse can lock neighbouring instruments into or out of phase.

**Interactive loop:** The player ticks the system, activates a few
instruments, and observes phase locks propagating through the graph.

**Exploration hook:** L1 isolates two instruments so the player can see
exactly how one pulse changes the neighbour's phase.

**Progress signal:** The level wins when target instruments lock to the
same displayed phase on the same tick.

**Failure or pressure:** Activating the wrong hub creates a stable but
incorrect phase cluster.

**Novelty WRT corpus:** It is not another wavefront coincidence puzzle;
the player explores lock dynamics on a visible graph.

**Composition directions:** L1 teaches one lock, L2 adds a branching
graph, and L3 requires delaying a lock so two branches converge later.
