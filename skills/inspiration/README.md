# Inspiration Seeds

This directory provides a structured inspiration pool for autonomous
mechanic selection. Its purpose is to increase variety before novelty
filtering, not to override NovaPlay constraints.

During `pick_mechanic`, when the user gives no seed, the agent must read
this README, `SCHEMA.md`, and the seed files. It then builds a candidate
pool with at least five candidates spanning at least three
`family_class` buckets and at least three `exploration_profile`
buckets when the corpus permits.

## Files

| file | count | role |
|---|---:|---|
| `extra-mechanic-seeds.md` | 12 | Initial structured seed pool |
| `exploration-mechanic-seeds.md` | 12 | Exploration-heavy seed pool |
| `external-source-seeds.md` | 12 | Seeds abstracted from external source families |

## Source Catalog

Read `SOURCE_CATALOG.md` before sampling from the web. It lists the
preferred inspiration sources, source keys, extraction template,
network budget, and Nova conversion filters. Web sampling is best-effort;
the seed files above are the offline fallback.

## Selection Rules

- Treat every seed as raw material, not as a finished game.
- Prefer underused classes before adding more physics-leaning or
  sokoban-like mechanics.
- Reject candidates whose Nova conversion would depend on text labels,
  hidden rules, real-time timing, physics precision, or non-core priors.
- For every considered candidate, record:
  - seed id or source synthesis;
  - `family_class`;
  - `exploration_profile`;
  - `interaction_type`;
  - `state_surface`;
  - closest prior-game ids;
  - why it was accepted or rejected.
- The final chosen mechanic still has to pass
  `mechanic-novelty/similarity-check.md` and
  `mechanic-novelty/negative-similarity-check.md`.
- The final chosen mechanic must also pass
  `design-constraints/exploration-pressure.md`: it needs a concrete
  discovery question, player probes, visible feedback, and a mastery
  rule that L1 teaches and L2/L3 extend.

## Maintenance

Run:

```bash
python skills/inspiration/validate_inspiration.py
```

Use stricter thresholds when expanding the corpus:

```bash
python skills/inspiration/validate_inspiration.py --min-seeds 80 --min-non-physics 0.70 --min-exploration-profiles 6
```
