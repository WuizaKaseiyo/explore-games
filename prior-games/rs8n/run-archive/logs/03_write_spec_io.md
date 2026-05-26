# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02 pick_mechanic): ID `rs8n`, family `line-reverse-sweep`, novelty argued.
- skills/code/spec-template.md, universal-scaffold.md, novaengine-api.md
- skills/design-constraints/* (all in study)
- skills/global/action-enum.md, color-legend.md, paths.md
- skills/mechanic-novelty/* (similarity & negative-similarity)

## Deliverables Produced
- mechanic-spec.md: Full 9-section spec. § 4 has 3 levels (L1: 1 mech, L2: 2 mech, L3: 3 mech, +1 per level), per-level witness solutions (3 / 2 / 9 actions), per-mechanic counterfactual lines for every (mechanic, level), 4-bullet difficulty justification per level (random-resistance, human-tractable, planning depth, step budget). § 5 action mapping concrete. § 7/§ 8 win/lose are testable predicates. § 9 novelty cross-references against 3 taxonomy near-misses + 3 prior-games near-misses.

## Notes
- Concrete numerical positions for each level were chosen so that (a) the per-mechanic counterfactual is *strict unsolvability* (anchor removal makes L2/L3 unwinnable; shifter removal makes L3 unwinnable), not just inconvenience, and (b) witnesses are 3-9 actions (well below 1/13× of budget) per the generous-budget rule.
- Sweep state machine designed to count ACTION5 as exactly one budget-step regardless of sweep length, matching the multi-tick animation conventions in sk48 / cn04 / r11l / sb26.
- Item visual signature: 4 distinct shapes × deliberate palette (pink/yellow/orange/blue + green via shifter) — palette diversity and pixel-detail richness named in negative-similarity-check.md.

