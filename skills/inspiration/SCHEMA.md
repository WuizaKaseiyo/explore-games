# Inspiration Seed Schema

Each inspiration seed is a compact mechanic source for autonomous
mechanic selection. Seeds are not game specs. They describe reusable
mechanic pressure that must be converted into an NovaPlay-compatible,
turn-based, core-prior-only game family before use.

## Seed Format

Each seed lives in a markdown file under this directory and starts with
a stable heading:

```markdown
### PS-001 - rule-rewrite-frontier
```

Immediately below the heading, include one fenced `yaml` block with the
fields below, followed by the required prose sections.

```yaml
id: PS-001
source: PuzzleScript demo
source_url: https://example.com/source.txt
fetched_via: manual
last_refreshed: 2026-05-08
family_tag: rule-rewrite-frontier
family_class: symbolic-rewrite
exploration_profile: rule-induction
interaction_type: global-tick
state_surface: visible
implementation_risk: medium
classic_overlap: none
usable_as: abstract-inspiration
closest_prior_ids: [kp9z, wavefront-converge-timing]
```

## Required Fields

- `id`: Stable seed id. Prefix should indicate source family, such as
  `PS`, `PSP`, `GEN`, or `Nova`.
- `source`: Human-readable source name.
- `source_url`: Source URL when available. Use `local:` only for local
  notes that cannot be traced to a web source.
- `fetched_via`: How the seed was obtained, for example `manual`,
  `gh api`, `raw-github`, or `synthetic`.
- `last_refreshed`: ISO date when the seed was last checked.
- `family_tag`: Lowercase hyphenated mechanic tag.
- `family_class`: One of `symbolic-rewrite`, `multi-actor`,
  `topology-transform`, `constraint-satisfaction`, `hidden-state`,
  `induction`, `cellular-automaton`, `set-or-recipe`,
  `graph-traversal`, `physics-leaning`, or `other`.
- `exploration_profile`: One of `rule-induction`,
  `state-revelation`, `tool-affordance`, `system-dynamics`,
  `topology-discovery`, `resource-experiment`,
  `multi-agent-discovery`, or `constraint-probing`. See
  `../design-constraints/exploration-pressure.md`.
- `interaction_type`: One of `arrows`, `click`, `click+arrows`,
  `global-tick`, or `modal`.
- `state_surface`: One of `visible`, `partially-hidden`,
  `inferred-rule`, or `memory-required`.
- `implementation_risk`: One of `low`, `medium`, or `high`.
- `classic_overlap`: One of `none`, `sokoban-like`,
  `sliding-block-like`, `pipe-routing-like`, `baba-like`, or `other`.
- `usable_as`: One of `direct`, `abstract-inspiration`, or `reject`.
- `closest_prior_ids`: Inline list of closest existing prior-game ids
  or reference-family tags. Empty list is allowed only when genuinely
  no close prior exists.

## Required Prose Sections

Every seed must include these section labels exactly:

- `**Core mechanic:**`
- `**Interactive loop:**`
- `**Exploration hook:**`
- `**Progress signal:**`
- `**Failure or pressure:**`
- `**Novelty WRT corpus:**`
- `**Composition directions:**`

## Use During `pick_mechanic`

When the user seed is empty, the agent samples across this corpus before
choosing a mechanic. The seed may be used directly only if it passes the
novelty checks; otherwise it should be recombined or abstracted into a
new family. Seeds marked `reject` are kept as cautionary examples and
must not be selected.
