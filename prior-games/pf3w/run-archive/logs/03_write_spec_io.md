# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02 pick_mechanic): ID `pf3w`, family tag `wavefront-converge-timing`, novelty argument.
- skills/code/spec-template.md, universal-scaffold.md, novaengine-api.md, id-generation.md.
- skills/design-constraints/composition-and-tutorial.md, difficulty-rules.md, checklist.md.
- skills/global/action-enum.md, color-legend.md.
- All design philosophy and cached-pattern files from #01 study.

## Deliverables Produced
- mechanic-spec.md: full 9-section spec — title, mechanic family, sprite roster (10 sprites with cell-array dimensions and palette values), level progression with EXACTLY 3 levels each carrying mechanics + necessity counterfactuals + witness solutions + 4-bullet difficulty justifications, action mapping (ACTION5 + ACTION6 only), HUD (single step-counter HUD widget; wavefront rendering via in-world sprites at layer 1), win condition, lose condition, novelty note.

## Notes
- L1 introduces M1 (click-place + tick-deliver) — count 1.
- L2 carries M1 + introduces M2 (inter-emitter timing offset) — count 2 (= N+1).
- L3 carries M1, M2 + introduces M3a (wall-routed BFS) and M3b (color-keyed targets) — count 4 (= L2-count + 2). Both per-level promotions are within the +1-or-+2 rule.
- BFS distances re-checked carefully:
  - L1: slot_blue (3, 8) → target_blue (12, 8) = 9 cells. Witness 10 actions, budget 30.
  - L2: slot_A (3, 4)→target_A (12, 4) = 9; slot_B (3, 12)→target_B (10, 12) = 7. Stagger 2, witness 11 actions, budget 35.
  - L3 wall-routed: slot_blue (1, 1)→target_blue (13, 14) = 25; slot_magenta (3, 13)→target_magenta (13, 1) = 22. Stagger 3 (slot_blue first), witness 27 actions, budget 70.
- Step budgets monotonically increase L1 → L2 → L3 (30 → 35 → 70), satisfying `difficulty-rules.md` § 2(d) for L3.
- M3b's necessity argument: with M3b enforced, only same-color routing wins (witness 27 actions); without M3b, a cross-color routing of 26 actions is also valid. So M3b's distinguishing behavior (target only lights via same-color wavefront) IS exercised by the witness — the witness uses slot_blue→target_blue and slot_magenta→target_magenta, both color-matched.
- All 21 checklist items are anticipated to pass (will be verified in #04 critique_spec). Item 18 (per-level (a) random-resistance, (b) human-tractable, (c) planning depth, (d) step budget) is filled per `difficulty-rules.md` § 2; item 12 (per-mechanic counterfactual) is filled per-mechanic per-level; item 19 (no-hidden-state) is satisfied because every emitter's tick-offset is surfaced by its visible wavefront radius (the wavefront sprite IS the state cue); item 20 (no-info-loss-at-32×32) is satisfied because all gameplay sprites are 3×3 cells with multi-color internal patterns, walls are 2×2 cells with checker pattern, and target lit/unlit is a center-pixel swap that survives downsampling; item 21 (UI teaches role) — emitters render as colored "+" cross with yellow center (clearly an active source), targets render as hollow ring → filled ring (clearly a receiver waiting for input).
- Ready for critique_spec.
