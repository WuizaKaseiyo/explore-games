# Step #05: write_spec (round 2 — revising after critique)

## Inputs Consumed
- workspace/critique-revisions.md (from #04): 5 issues with concrete fixes.
- workspace/mechanic-spec.md (round 1 from #03): the spec to revise.
- skills/code/spec-template.md, universal-scaffold.md, novaengine-api.md.
- skills/design-constraints/checklist.md, difficulty-rules.md, forbidden-elements.md.

## Deliverables Produced
- `workspace/mechanic-spec.md` (round 2) — revised:
  - § 3 avatar redesigned to a rim+inner-block+corner-indicator pattern with no tool/humanoid imagery.
  - § 4 L1 layout: full stone rows at row 3 and row 5 sealing the corridor.
  - § 4 L2 layout: col 7 stones except at exit; (5, 1), (6, 3), (6, 5) stones to make (6, 4) reachable only from the blue wall.
  - § 4 L3 layout: same right-half sealing as L2; col 3 has TWO openings — `wall_red_h2` at (3, 1) and `wall_red_h3` at (3, 4) — flanked by stones, creating a row-1/row-4 route choice.
  - § 4 L3 (c) rewritten: post-discovery decision-space named the row-1 vs row-4 branch, the failing heuristic is "monotone-progress along the goal-row" (row-4) with concrete divergence trace and 5-action / ~23% delay vs the witness.
  - § 2, § 3, § 5, § 6, § 9 — every "pickaxe" reference replaced with "charge state / charge indicator".
  - Witness counts: L1 = 9, L2 = 25, L3 = 22. Step budgets 30 / 80 / 90.

## Notes
- Round-2 changes are localised; § 1 (title), § 2 (mechanic family core text), § 5 (action mapping), § 7 (win), § 8 (lose) are unchanged in substance. § 9 distinguishing rules unchanged (geometry tweaks don't alter family identity).
- L3's witness now goes via row 1 (the shorter route through `wall_red_h2`); the row-4 route stays valid as a slower alternative which is the point of (c) — it's the heuristic-failure path.
- Layered-hardness mechanic is exercised by both routes (both col-3 openings are hardness > 1).
- Critique-round 2 needs to verify each item again from scratch.
