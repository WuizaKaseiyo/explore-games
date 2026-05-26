# External Source Mechanic Seeds

### WEB-001 - clickmaze-key-parity

```yaml
id: WEB-001
source: Clickmazes-style path constraint
source_url: https://clickmazes.com/index-ps.htm
fetched_via: source-catalog
last_refreshed: 2026-05-09
family_tag: clickmaze-key-parity
family_class: graph-traversal
exploration_profile: rule-induction
interaction_type: arrows
state_surface: visible
implementation_risk: low
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [fz5j, directed-lineage-graph]
```

**Core mechanic:** Keys flip a visible parity state, and doors accept
entry only when the player's parity matches the door's marker.

**Interactive loop:** The player walks, tests doors under different
parity states, and learns which key order opens the path.

**Exploration hook:** L1 places two safe doors beside one key so the
player can probe parity before any irreversible choice.

**Progress signal:** Door markers glow when the current parity can pass.

**Failure or pressure:** Collecting keys greedily can flip parity away
from the door needed later.

**Novelty WRT corpus:** It is path-based but centres on discovering a
stateful parity grammar, not phase timing or ordinary key-door gating.

**Composition directions:** L1 teaches one parity flip, L2 adds a
crossroad where one key must be delayed, and L3 adds a door that must be
visited twice under different parity states.

### WEB-002 - if-object-affordance-chain

```yaml
id: WEB-002
source: Interactive fiction affordance puzzle
source_url: https://ifarchive.org/
fetched_via: source-catalog
last_refreshed: 2026-05-09
family_tag: if-object-affordance-chain
family_class: induction
exploration_profile: tool-affordance
interaction_type: click
state_surface: visible
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [affordance-border-test, pz4t]
```

**Core mechanic:** Tools visibly affect only objects with matching
affordance shapes; using a tool transforms both the object and the tool
into the next affordance state.

**Interactive loop:** The player probes tools against safe objects,
observes compatible and incompatible responses, and schedules the chain.

**Exploration hook:** Failed probes produce visible tool/object flashes
without consuming resources, while compatible probes change state.

**Progress signal:** A target chain completes when every object has been
transformed into its required affordance state.

**Failure or pressure:** Using a compatible tool too early advances it
past the state needed for a later object.

**Novelty WRT corpus:** Inspired by IF affordance puzzles, but converted
to visible sprite-state probing instead of text verbs.

**Composition directions:** L1 tests one tool/object pair, L2 adds a
tool state cycle, and L3 requires preserving an intermediate tool state.

### WEB-003 - gallery-mirror-grammar

```yaml
id: WEB-003
source: PuzzleScript gallery grammar pattern
source_url: https://www.puzzlescript.net/Gallery/index.html
fetched_via: source-catalog
last_refreshed: 2026-05-09
family_tag: gallery-mirror-grammar
family_class: symbolic-rewrite
exploration_profile: rule-induction
interaction_type: global-tick
state_surface: visible
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [cy3k, qz73]
```

**Core mechanic:** A global tick mirrors selected symbols across a local
axis, but mirrored symbols change type according to a visible grammar.

**Interactive loop:** The player places or selects an axis, ticks, and
learns how symbol types rewrite under reflection.

**Exploration hook:** L1 uses isolated symbols so the player can test
horizontal and vertical mirrors and see different rewrites.

**Progress signal:** Target cells accept only the rewritten symbol, not
the original symbol.

**Failure or pressure:** Mirroring with the wrong axis can create the
right position but the wrong rewritten type.

**Novelty WRT corpus:** Near symbolic rewrite and alignment games, but
its central discovery is reflection-dependent grammar.

**Composition directions:** L1 teaches one axis, L2 adds the second
axis, and L3 requires applying axes in a specific order.

### WEB-004 - experimental-interface-dials

```yaml
id: WEB-004
source: Experimental Gameplay interface puzzle
source_url: https://experimental-gameplay.org/
fetched_via: source-catalog
last_refreshed: 2026-05-09
family_tag: experimental-interface-dials
family_class: constraint-satisfaction
exploration_profile: state-revelation
interaction_type: modal
state_surface: visible
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [qz73, lv4k]
```

**Core mechanic:** Dials expose only aggregate field readings; adjusting
one dial changes two hidden-but-visualized channels shown as bars.

**Interactive loop:** The player turns dials, watches channel bars, and
infers which dial controls which channel combination.

**Exploration hook:** Small dial changes in L1 visibly move paired bars,
letting the player map cause to effect.

**Progress signal:** The level wins when all bars align with target
bands at the same time.

**Failure or pressure:** A dial setting that fixes one channel can push
another outside its target band.

**Novelty WRT corpus:** It is constraint-based but emphasizes learning an
interface-to-state mapping through probes.

**Composition directions:** L1 maps two dials, L2 adds a coupled dial,
and L3 adds a lock that freezes one channel while the others move.

### WEB-005 - ifdb-reversible-rooms

```yaml
id: WEB-005
source: IFDB spatial puzzle abstraction
source_url: https://ifdb.org/
fetched_via: source-catalog
last_refreshed: 2026-05-09
family_tag: ifdb-reversible-rooms
family_class: topology-transform
exploration_profile: topology-discovery
interaction_type: arrows
state_surface: inferred-rule
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [tw94, foldout-map-memory]
```

**Core mechanic:** Entering a room through one edge reverses selected
exits inside that room; the visible exit arrows update after entry.

**Interactive loop:** The player enters rooms from different edges,
observes exit reversal, and plans a route through changing connectivity.

**Exploration hook:** L1 has a safe two-room loop where entering from
north versus west visibly flips different exits.

**Progress signal:** Target rooms become reachable only after the exit
orientation graph is configured.

**Failure or pressure:** Entering a room from the wrong side can reverse
the exit needed to leave the region.

**Novelty WRT corpus:** It abstracts IF room-navigation puzzles into
visible topology, not text commands.

**Composition directions:** L1 teaches one reversible room, L2 adds a
choice of entry side, and L3 requires preserving an exit while flipping
another room.

### WEB-006 - itch-anomaly-sorter

```yaml
id: WEB-006
source: itch.io experimental sorting pattern
source_url: https://itch.io/games/tag-experimental
fetched_via: source-catalog
last_refreshed: 2026-05-09
family_tag: itch-anomaly-sorter
family_class: induction
exploration_profile: constraint-probing
interaction_type: click
state_surface: inferred-rule
implementation_risk: low
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [ng52, counterexample-glyphs]
```

**Core mechanic:** One object in each set violates a hidden visible-rule
pattern; clicking a candidate reveals whether the inferred anomaly rule
was correct.

**Interactive loop:** The player compares object features, selects a
suspected anomaly, and uses feedback to infer the next set's rule.

**Exploration hook:** Early sets give reversible feedback that marks
which feature was wrong without ending the level.

**Progress signal:** Each correctly identified anomaly locks into a
collection rail.

**Failure or pressure:** Choosing by colour alone works on the first set
but fails when shape or adjacency becomes the relevant feature.

**Novelty WRT corpus:** It extends classification into active anomaly
hypothesis testing.

**Composition directions:** L1 teaches one feature, L2 changes the
relevant feature, and L3 requires identifying a relational anomaly.

### WEB-007 - pattern-library-role-inversion

```yaml
id: WEB-007
source: Gameplay design pattern abstraction
source_url: https://gameplaydesignpatterns.org/
fetched_via: source-catalog
last_refreshed: 2026-05-09
family_tag: pattern-library-role-inversion
family_class: multi-actor
exploration_profile: multi-agent-discovery
interaction_type: modal
state_surface: visible
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [vy3m, role-memory-handshake]
```

**Core mechanic:** Two actors invert each other's affordances when they
swap roles: the mover becomes a blocker and the blocker becomes a mover.

**Interactive loop:** The player toggles role inversion, tests actor
effects, and stages swaps to make temporary blockers and movers.

**Exploration hook:** L1 lets the player invert roles beside a harmless
target to observe the exact affordance swap.

**Progress signal:** Targets require actors to arrive while holding the
correct inverted role.

**Failure or pressure:** Inverting too early can strand the only actor
that can later move through a gate.

**Novelty WRT corpus:** Multi-actor, but its discovery is reciprocal
role inversion rather than fixed actor classes.

**Composition directions:** L1 teaches one inversion, L2 adds a gate that
requires delayed inversion, and L3 requires two actors to exchange roles
twice.

### WEB-008 - indiepocalypse-conversation-objects

```yaml
id: WEB-008
source: Indiepocalypse experimental interaction abstraction
source_url: https://pizzapranks.itch.io/indiepocalypse
fetched_via: source-catalog
last_refreshed: 2026-05-09
family_tag: indiepocalypse-conversation-objects
family_class: set-or-recipe
exploration_profile: state-revelation
interaction_type: click
state_surface: visible
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [hr8q, sample-and-freeze-field]
```

**Core mechanic:** Selecting one symbol reveals a temporary set of
related objects; combining two revealed objects creates a persistent
tool.

**Interactive loop:** The player reveals related objects, experiments
with pairings, and chooses which temporary object to preserve.

**Exploration hook:** L1 shows that each selected symbol exposes a
different temporary object cloud with visible expiry.

**Progress signal:** Persistent tools fill target sockets.

**Failure or pressure:** Preserving the first useful-looking object can
consume the reveal needed for a later pairing.

**Novelty WRT corpus:** Inspired by idea-object interaction, but reduced
to visible symbol sets and recipe persistence.

**Composition directions:** L1 preserves one object, L2 combines objects
from two reveals, and L3 adds an expiring reveal order dependency.

### WEB-009 - database-query-tiles

```yaml
id: WEB-009
source: Interactive fiction / database puzzle abstraction
source_url: https://ifarchive.org/
fetched_via: source-catalog
last_refreshed: 2026-05-09
family_tag: database-query-tiles
family_class: constraint-satisfaction
exploration_profile: rule-induction
interaction_type: click
state_surface: visible
implementation_risk: low
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [ng52, WEB-006]
```

**Core mechanic:** Query tiles filter a set of records by visible
features; the player must compose filters to isolate the target record.

**Interactive loop:** The player clicks filters, observes which records
remain highlighted, and infers the filter logic.

**Exploration hook:** L1 includes filters with overlapping effects so
the player can probe AND versus OR behaviour.

**Progress signal:** The correct target remains as the only highlighted
record.

**Failure or pressure:** Applying a broad filter first can hide the only
record needed to infer a later narrow filter.

**Novelty WRT corpus:** It resembles classification but focuses on
discovering filter logic through visible set reduction.

**Composition directions:** L1 teaches one filter, L2 composes two
filters, and L3 includes a filter whose effect must be inferred from
what disappears rather than what remains.

### WEB-010 - gallery-one-way-transform

```yaml
id: WEB-010
source: PuzzleScript one-way rule abstraction
source_url: https://www.puzzlescript.net/Gallery/index.html
fetched_via: source-catalog
last_refreshed: 2026-05-09
family_tag: gallery-one-way-transform
family_class: symbolic-rewrite
exploration_profile: resource-experiment
interaction_type: arrows
state_surface: visible
implementation_risk: low
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [pj7k, cy3k]
```

**Core mechanic:** Moving through transform gates permanently rewrites
the actor's symbol, and only some symbols can pass later gates.

**Interactive loop:** The player tests transform gates, observes the
actor symbol change, and chooses an irreversible route.

**Exploration hook:** Safe L1 branches let the player try both transform
directions before the level asks for commitment.

**Progress signal:** Later gates visibly accept or reject the current
actor symbol.

**Failure or pressure:** Taking the locally short route can rewrite the
actor into a symbol that cannot pass the final gate.

**Novelty WRT corpus:** It uses symbolic state but adds irreversible
route planning and exploration of transform consequences.

**Composition directions:** L1 teaches one rewrite, L2 adds mutually
exclusive rewrites, and L3 requires visiting a gate only after a decoy
rewrite has been avoided.

### WEB-011 - experimental-sensor-shadow

```yaml
id: WEB-011
source: Experimental sensor mechanic abstraction
source_url: https://experimental-gameplay.org/
fetched_via: source-catalog
last_refreshed: 2026-05-09
family_tag: experimental-sensor-shadow
family_class: hidden-state
exploration_profile: state-revelation
interaction_type: click+arrows
state_surface: partially-hidden
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [vp6h, latent-channel-mixer]
```

**Core mechanic:** A sensor casts a shadow that reveals only one layer of
cell state; moving the sensor changes which layer is visible.

**Interactive loop:** The player moves the sensor, compares revealed
layers, and acts only when the needed layer is exposed.

**Exploration hook:** L1 exposes two nearby cells whose visible layer
changes as the sensor moves, teaching layer-dependent state.

**Progress signal:** Correctly revealed targets flash and become
collectible or transformable.

**Failure or pressure:** Acting on a cell under the wrong revealed layer
changes it into a blocker.

**Novelty WRT corpus:** It is related to projection and hidden-state
games, but exploration is about layer-specific sensing.

**Composition directions:** L1 reveals one layer, L2 adds a second layer
with different affordance, and L3 requires acting after moving the
sensor away from a tempting layer.

### WEB-012 - archive-commandless-inventory

```yaml
id: WEB-012
source: Interactive fiction inventory abstraction
source_url: https://ifarchive.org/
fetched_via: source-catalog
last_refreshed: 2026-05-09
family_tag: archive-commandless-inventory
family_class: set-or-recipe
exploration_profile: tool-affordance
interaction_type: modal
state_surface: visible
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [hr8q, decaying-toolbox]
```

**Core mechanic:** Inventory slots are visible board positions; moving
an item into a slot changes which board verb ACTION5 performs.

**Interactive loop:** The player loads an item, tests the changed verb,
and rearranges inventory slots to create the required action sequence.

**Exploration hook:** L1 provides two safe slot/item combinations whose
ACTION5 effects visibly differ.

**Progress signal:** Correct verb outputs mark targets or open gates.

**Failure or pressure:** Loading the wrong item before a one-shot gate
uses the action opportunity without producing the needed effect.

**Novelty WRT corpus:** It converts IF inventory affordances into visible
board-state verbs without text commands.

**Composition directions:** L1 maps item to verb, L2 adds slot-specific
verb differences, and L3 requires preserving one item for a later verb.
