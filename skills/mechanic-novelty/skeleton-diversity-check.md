# Skeleton Diversity Check

> **DORMANT / NOT WIRED IN.** This doc describes an earlier 10-column
> diversity schema for `prior-games/index.md` (with `primary_skeleton`,
> `secondary_skeleton`, `interaction_type`, `state_model`,
> `objective_shape` columns). The live index and the authoritative
> `prior-games-index-format.md` / `finalize/index-row-format.md` use
> the **5-column** schema (`game_id | mechanic_family | description |
> timestamp | seed`), and `validate_prior_index.py` validates that.
> No FSM state references this file. The skeleton reasoning below is
> still useful as a *thinking aid* during `pick_mechanic` /
> `critique_spec`, but do NOT add skeleton columns to the index.

This gate prevents autonomous runs from producing games that are
technically novel but structurally the same kind of play experience as
recent or overused prior games.

Run this check during `pick_mechanic` for every candidate and during
`critique_spec` on the full spec. The positive similarity check asks
"can the candidate be distinguished from each prior?". This gate asks
a coarser question: "what is the player fundamentally thinking about
while playing, and have we made too many games with that skeleton?"

## Skeleton Vocabulary

Use exactly one `primary_skeleton` and zero or one
`secondary_skeleton` from this list.

| skeleton | Use when the main play thought is... | Reject near-clones that... |
|---|---|---|
| `avatar-navigation` | navigating a controlled avatar through hazards, gates, timing, or terrain | only add a new tile type to another walking maze |
| `object-placement` | moving, pushing, placing, dragging, tilting, or arranging physical board objects | are another crates-to-targets or pawns-to-targets variant |
| `signal-routing` | steering a beam, courier, wave, cone, shadow, or other signal to receivers | only recolour a beam/router/courier prior |
| `global-field-update` | applying a global tick/pulse/force/tilt that moves or transforms many things together | are another field pulse with different names |
| `cellular-propagation` | local neighbour rules, growth, frontier expansion, spreading, or automata | are another flood-fill/sandpile/wavefront with cosmetic changes |
| `recipe-composition` | selecting, combining, sequencing, or consuming ingredients / sets | are another formula matcher without a new dependency pressure |
| `classification-sorting` | assigning objects to classes, bins, signatures, or equivalence groups | only change the visual feature used for sorting |
| `topology-transform` | changing connectivity, passability interpretation, regions, wrap, portals, masks, or graph structure | reduce to ordinary walking/pushing after the topology is named |
| `multi-actor-coordination` | coordinating multiple actors, roles, agents, or independently moving entities | are another select-actor-and-move-to-target layout |
| `symbolic-rewrite` | changing symbolic state by rule, parity, grammar, face orientation, or local rewrite | are just toggles/cycles without compositional symbolic consequence |
| `spatial-constraint` | satisfying geometric, balance, alignment, quota, adjacency, or invariant constraints | are another static arrangement puzzle with only different sprites |

The skeleton is not the theme, implementation technique, or mechanic
family name. It is the dominant cognitive task. If a game has a
walking avatar but the real puzzle is balancing quotas, the primary
skeleton is `spatial-constraint`, not `avatar-navigation`.

## Extra Labels

Every candidate and finalized game must also carry:

- `interaction_type`: one of `arrows`, `click`, `click+arrows`,
  `global-tick`, or `modal`.
- `state_model`: short lowercase-hyphen tag describing how state
  changes, such as `actor-state`, `local-rule`, `global-field`,
  `topology-overlay`, `symbolic-state`, `inventory`, `orientation`,
  `periodic-field`, or `constraint-counters`.
- `objective_shape`: short lowercase-hyphen tag describing what
  winning asks for, such as `reach-goal`, `cover-targets`,
  `align-sockets`, `satisfy-constraints`, `synchronize-events`,
  `classify-objects`, `complete-recipes`, `collect-all`, or
  `route-signal`.

These labels prevent easy relabeling. A candidate that shares skeleton,
interaction type, and objective shape with a prior should be treated as
the same kind of game unless the state model is genuinely different.

## Autonomous Candidate Rules

At `pick_mechanic`, before the normal similarity checks:

1. Label every candidate with `primary_skeleton`,
   `secondary_skeleton`, `interaction_type`, `state_model`, and
   `objective_shape`.
2. The autonomous candidate pool must contain at least five candidates
   and should cover at least four distinct `primary_skeleton` values.
3. Reject a candidate if its `primary_skeleton` appears in any of the
   most recent five rows of `prior-games/index.md`, unless it earns an
   explicit override.
4. Reject a candidate if its `primary_skeleton` is high-frequency in
   the full corpus. High-frequency means count >=
   `max(ceil(20% of prior games), 5)`.
5. An override is allowed only when at least two of these three labels
   differ materially from the conflicting prior set:
   `interaction_type`, `state_model`, `objective_shape`.
   The override must explain the player-visible structural difference,
   not just a naming difference.
6. Even with an override, reject if
   `negative-similarity-check.md` finds three or more shared dimensions
   with any single prior.

If too many candidates are rejected, return to the inspiration pool and
sample from underused skeletons rather than weakening the gate.

## Critique-Time Skeleton Drift

At `critique_spec`, compare the labels declared in `mechanic-pick.md`
against the completed `mechanic-spec.md`.

Reject the spec if:

- the full spec's primary skeleton differs from the selected
  candidate's declared `primary_skeleton`;
- L2 or L3 turns into a high-frequency skeleton that was not declared
  at pick time;
- the implementation plan collapses a supposedly novel skeleton into
  ordinary object placement, signal routing, or avatar navigation;
- the spec shares primary skeleton, interaction type, and objective
  shape with any recent-five prior without a valid override.

When rejecting, name the actual skeleton the spec drifted into and the
specific spec sections that caused the drift.

## Existing Prior Labels

The table below records the current generated corpus. Future runs
should use `prior-games/index.md` as the live source of truth; this
table is a baseline audit for the games that existed when this gate was
introduced.

| game_id | primary_skeleton | secondary_skeleton | interaction_type | state_model | objective_shape |
|---|---|---|---|---|---|
| kf42 | multi-actor-coordination | object-placement | click+arrows | actor-state | cover-targets |
| qz73 | spatial-constraint | symbolic-rewrite | modal | orientation-state | align-sockets |
| kx14 | global-field-update | object-placement | modal | fluid-field | deliver-objects |
| qb84 | object-placement | symbolic-rewrite | arrows | inventory-swap | match-targets |
| lq5x | signal-routing | avatar-navigation | click+arrows | projection-field | collect-all |
| gv47 | cellular-propagation | spatial-constraint | click | region-growth | surround-targets |
| hr8q | recipe-composition | classification-sorting | click | inventory-recipe | complete-recipes |
| ng52 | classification-sorting | spatial-constraint | click | feature-signature | classify-objects |
| pj7k | symbolic-rewrite | avatar-navigation | arrows | orientation-state | paint-targets |
| pz4t | object-placement | spatial-constraint | click+arrows | anchor-transform | tile-region |
| vn8d | global-field-update | cellular-propagation | click | chain-reaction | clear-targets |
| fz5j | avatar-navigation | spatial-constraint | arrows | periodic-field | reach-goal |
| kn58 | global-field-update | object-placement | click | attraction-field | cover-targets |
| bx84 | signal-routing | spatial-constraint | click | beam-path | route-signal |
| wt39 | avatar-navigation | object-placement | arrows | glide-motion | reach-goal |
| zk9p | multi-actor-coordination | avatar-navigation | arrows | autonomous-agents | clear-actors |
| rk7x | signal-routing | topology-transform | click | switch-network | route-signal |
| gx7m | global-field-update | symbolic-rewrite | modal | rotation-network | align-state |
| vp6h | signal-routing | avatar-navigation | arrows | projection-field | collect-all |
| kp9z | cellular-propagation | global-field-update | click | local-overflow | satisfy-sinks |
| zd7m | multi-actor-coordination | topology-transform | arrows | cohort-motion | reach-goal |
| lv4k | spatial-constraint | object-placement | click | constraint-counters | satisfy-constraints |
| xn5p | topology-transform | avatar-navigation | click+arrows | region-partition | partition-region |
| mr5q | global-field-update | multi-actor-coordination | click | polarity-field | clear-pairs |
| pf3w | cellular-propagation | signal-routing | click | wavefront-field | synchronize-events |
| tg6w | global-field-update | object-placement | arrows | gravity-field | cover-targets |
| ej4t | object-placement | avatar-navigation | arrows | radius-gated-motion | cover-targets |
| vy3m | multi-actor-coordination | object-placement | modal | role-verbs | cover-targets |
| tw94 | topology-transform | object-placement | arrows | wrap-topology | cover-targets |
| cy3k | symbolic-rewrite | classification-sorting | arrows | symbolic-state | match-pattern |
