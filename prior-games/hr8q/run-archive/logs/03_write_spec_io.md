# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (#02)
- skills/code/spec-template.md, universal-scaffold.md
- skills/design-constraints/{checklist,composition-and-tutorial,difficulty-rules,core-knowledge-priors,forbidden-elements}.md
- skills/global/{action-enum,color-legend}.md

## Deliverables Produced
- workspace/mechanic-spec.md: full 9-section spec.

## Notes
- Mechanic count: L1 = 1 (pair-blend-and-commit); L2 = 2 (+intermediate-as-ingredient via mismatched commit); L3 = 3 (+finite-inventory-with-multi-target).
- L3 ordering: queue is FIFO and inventory is tight; trap recipe (purple+magenta=green) defeats greedy "use intermediate ASAP" heuristic; swap of witness actions 6-7 leaves yellow exhausted before chain2, breaking solvability.
- All recipes UNORDERED (frozenset key).
- Click ALWAYS deducts 1 use; at L1/L2 inventories effectively infinite (use=large) so deduction is invisible; at L3 deduction is binding.
