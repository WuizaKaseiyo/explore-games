# Step #05: write_spec (round 2)

## Inputs Consumed
- workspace/mechanic-spec.md (revision 0 from #03, edited in place)
- workspace/critique-revisions.md (from #04, 7 issues)
- skills/code/spec-template.md, universal-scaffold.md, novaengine-api.md
- skills/design-constraints/*

## Deliverables Produced
- workspace/mechanic-spec.md (revision 1): added "Revision history" section; applied all 7 critique fixes:
  - Issue 1 (BLOCKING): L3 phase 4 witness re-routed via col 11 (avoiding the col-13 bot-pillar at rows 8..10). Path: (7,9) → 4 rights to (11,9) → 5 ups to (11,4) → 2 rights to (13,4). Total phase 4: 11 actions. Total L3: 25 actions.
  - Issue 2 (MINOR): L2 phase 1 corrected to 2 actions (was 3). Total L2: 25 actions.
  - Issue 3 (MINOR): L1 witness corrected to 6 actions (was 7).
  - Issue 4 (MINOR): Crystal palette `[[10, 14], [14, 10]]` → `[[10, 15], [15, 10]]` (light-blue + purple, avoiding green=safe cultural overtone).
  - Issue 5 (BLOCKING): col-2 pillar removed from L2 layout. M2 necessity now grounded in ordering: collect A before sliding leftward.
  - Issue 6 (CLARIFY): blocking modes specified — pillars `BlockingMode.PIXEL_PERFECT` (default), crystals `InteractionMode.INTANGIBLE`, lanterns `InteractionMode.INTANGIBLE`.
  - Issue 7: resolved by Issue 5 fix.
- L2 difficulty justification (c) rewritten to use the corrected layout (no col-2 pillar) and the corrected ordering chain.
- L3 §(d) step-budget ratio updated for the new witness count (25 actions / 120 budget = 4.8× headroom; ratio 0.21).

## Notes
- Internal walk-through confirmed every avatar position in the L1, L2, L3 witnesses is walkable (avatar 2×2 footprint does not overlap any pillar at any step). Pickup conditions verified per cell (top-shadow + bot-shadow checks).
- L2 witness end-state spare is now 70 - 25 = 45 actions.
- L3 witness phase 2 unchanged (2 actions for A); phase 3 unchanged (10 actions for C); phase 4 rewritten (11 actions for B).
- Visit count for write_spec: 2.
