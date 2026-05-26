# Step #03: write_spec

## Inputs Consumed
- states/write_spec.md
- skills/code/spec-template.md (the 9-section structure)
- skills/code/universal-scaffold.md (file structure + style rules)
- skills/code/novaengine-api.md (will read for API references during write)
- skills/design-constraints/{composition-and-tutorial.md, difficulty-rules.md, checklist.md, core-knowledge-priors.md, forbidden-elements.md}
- skills/global/{action-enum.md, color-legend.md, paths.md}
- skills/mechanic-novelty/* (similarity-checks, taxonomy, prior format)
- skills/mechanism-details/* (cached summaries; deeper evidence at deep-analysis-3lvls/<id>/<id>-deep-analysis.md as needed)
- workspace/mechanic-pick.md (#02 deliverable: id zk9p, family pursuer-merge-walk)

## Deliverables Produced
- workspace/mechanic-spec.md — full 9-section spec. L1 = 3 mechanics (avatar walk, Manhattan-major chase, merge-on-collision). L2 = 5 mechanics (+wall-block, +orthogonal-major chase). L3 = 7 mechanics (+phase pursuer, +tick-skip ACTION5). Per-level witness solutions, counterfactual necessity per mechanic, and four-bullet difficulty justifications.

## Notes
- Inheritance pattern: 3 → 5 → 7 (+2 each level). All carried-forward mechanics required by every later witness.
- Action subset `[1,2,3,4,5]` declared from L1, with ACTION5 gated to a single-step no-op in L1/L2 and full tick-skip in L3.
- Step budgets: 60 / 80 / 100. Witness lengths: 5 / 15 / ~24.
- L2 and L3 witnesses are sketched at the strategic level rather than tick-perfect; the critique can re-verify with the rule definitions but the implementation will need to be the source of ground truth for exact tick counts.
- Visual richness comes from the floor sprite's speckle pattern (per negative-similarity-check principle 1); entity sprites are 1×1 logical for clean cell semantics.
