# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02 pick_mechanic)
- skills/code/spec-template.md (full)
- skills/code/universal-scaffold.md (full)
- skills/code/novaengine-api.md (full)
- skills/code/id-generation.md (cached from #02)
- skills/design-constraints/* (cached)
- skills/global/* (cached)

## Deliverables Produced
- workspace/mechanic-spec.md — full 9-section spec.

## Notes
- All 9 sections present per `code/spec-template.md`.
- Action subset `[3, 4, 5, 6]` — ACTION3/4 cursor-move, ACTION5 pour, ACTION6 valve-toggle. No undo (slot 7 omitted per strict rule).
- Three mechanics with strict counterfactual necessity:
  - L1: M1 alone (pour-and-equalize). N=1.
  - L2: M1 + M2 (valve-toggle). +1 from L1. ✓
  - L3: M1 + M2 + M3 (overflow-cap). +1 from L2. ✓
- Each mechanic's necessity at each level is restated with a concrete blocking argument (no hand-waving).
- Step budgets: 12 / 18 / 19. Buffer (budget − witness) = 8 / 8 / 8 — stable across levels (no shrink).
- Closed-valve cost at L3 is 22 actions, exceeding L3's 19-budget — forces M2 (valve toggle) at L3.
- Witness at L3 (open-all-valves + pour 9) exercises M3 (overflow cap clips C past row 2 starting from pour 3) — without M3 the merge strategy would overshoot C's target.
