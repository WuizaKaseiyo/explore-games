# Exploration Pressure Gate

Every generated game must be more than a deterministic execution puzzle.
It must give the player something meaningful to discover through play:
a rule, mapping, state transformation, dependency, boundary condition,
or emergent consequence that is visible or inferable from interaction.

This is not permission to hide arbitrary rules. NovaPlay exploration
must be fair: the player can form hypotheses from visible state, test
them with actions, and observe feedback that updates their model.

## Required Exploration Contract

Every `mechanic-pick.md` and `mechanic-spec.md` must include an
exploration contract with these fields:

- `exploration_profile`: one of the profiles below.
- `discovery_question`: the concrete question the player is expected
  to answer by experimenting.
- `probe_actions`: 2-4 short action probes a reasonable player could
  try before knowing the full solution.
- `observable_feedback`: what changes on screen after each probe.
- `mastery_rule`: the rule the player should infer.
- `anti-randomness`: why random input or greedy play is unlikely to
  discover a complete solution.

## Exploration Profiles

Use exactly one primary profile:

| profile | Player discovers... | Good signals |
|---|---|---|
| `rule-induction` | a visible input-output rule, symbol mapping, or transformation grammar | repeated probes reveal a consistent rule |
| `state-revelation` | how hidden or compressed state becomes visible through actions | state markers, trail changes, counters, or overlays update |
| `tool-affordance` | what a verb/tool can and cannot affect | boundaries, invalid cases, and side effects are visible |
| `system-dynamics` | how local changes cascade through a system | propagation, chain reactions, or field updates expose causality |
| `topology-discovery` | how connectivity/passability differs from appearance | moving or toggling reveals alternate routes or region membership |
| `resource-experiment` | how spending, decay, quotas, or limited charges affect future options | counters and remaining resources make tradeoffs visible |
| `multi-agent-discovery` | how actors or roles differ and how their effects compose | same input produces role-specific outcomes |
| `constraint-probing` | which arrangements satisfy or violate an invariant | local badges, highlights, or target states update after probes |

## Minimum Bar

Reject a mechanic or spec if any of these are true:

- The only challenge is executing a known path after reading the spec.
- L1 does not teach the discovery question through safe interaction.
- L2/L3 add mechanics but do not add new information to discover.
- The player cannot tell why a probe succeeded or failed from visible
  board state, HUD, or immediate sprite changes.
- The discovery depends on text labels, memorized real-world trivia,
  arbitrary hidden rules, or timing reflexes.
- Random play can stumble into the solution as easily as a player who
  has inferred the rule.

## Per-Level Expectations

- **L1:** A safe sandbox. The player can perform at least two distinct
  probes and observe the base rule without losing.
- **L2:** The same base rule must be composed with a new affordance,
  dependency, or constraint. The player must revise their L1 model.
- **L3:** The game must require transfer: the player applies the
  learned rule under a changed context, decoy, ordering dependency, or
  boundary case. L3 should not merely add more objects.

## Critique Procedure

During `critique_spec`, read the exploration contract and walk the
player's likely learning path:

1. Can the player form the stated `discovery_question` from visible
   state?
2. Do the `probe_actions` produce distinct and informative feedback?
3. Does L1 teach the base `mastery_rule` before L2/L3 rely on it?
4. Does each later level add an exploratory revision, not just a longer
   witness?
5. Is the exploration fair under NovaPlay core priors?

If any answer is no, reject the spec and ask for a redesigned mechanic
or level layout, not just more prose.
