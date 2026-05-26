# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02): chose `rk7x` / live-switch-routing.
- skills/code/spec-template.md: 9-section template.
- skills/code/universal-scaffold.md: file structure + style rules + camera-resize requirement.
- skills/code/novaengine-api.md: API signatures.
- skills/design-constraints/composition-and-tutorial.md: 3-level structure + +1-or-+2 promotion rule.
- skills/design-constraints/checklist.md: 18-item §3.4 compliance checklist.
- skills/design-constraints/difficulty-rules.md: per-level (a)-(d) bullet structure.
- skills/design-constraints/forbidden-elements.md: glyph/letter/digit ban.
- skills/global/color-legend.md, action-enum.md: palette + slot semantics.
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md: novelty re-check on the fleshed-out mechanics.

## Deliverables Produced
- workspace/mechanic-spec.md: full 9-section spec. L1 = 1 mechanic; L2 = 2 (+1); L3 = 4 (+2). Witness solutions written. Per-mechanic counterfactual sentences provided. Difficulty justifications include random-resistance estimates, human time targets, planning depth chains (with named heuristic for L3 and divergence point), step budgets (L1=24 over witness 14, L2=60 over 30, L3=96 over 50).

## Notes
- Mechanic counts: L1=1 (live switch routing), L2=2 (carry + coloured stops), L3=4 (carry both + dual couriers + conflict cells). Both promotions are +1 or +2 per the rule.
- The "switch lock-on-pass" idea was rejected during drafting in favour of "coloured stops" because lock-on-pass is a constraint, not a clean mechanic with its own witness-required behaviour.
- L3 conflict-cell rule needed concrete grounding: chose to require red and blue couriers to swap rows (red 1→14, blue 14→1) so the obvious shortest path collides at the swap junction, forcing a witness detour. Counterfactual reads cleanly.
- Coordinate scheme: 16×16 logical grid scaled 4× to 64×64 frame. Camera viewport set to (16, 16) in `on_set_level` (per universal-scaffold camera-resize requirement); display-to-grid math then works with sprite grid coords.
- Aesthetic: sprites have internal pixel patterns (courier with direction tip, junction with coloured central blade, hollow-ring stops). Palette deliberately diverges from priors per the negative-similarity-check cautionary tale.
- Action enum: pure click (`available_actions=[6]`), no arrows or ACTION5. The "freedom slot" ACTION5 is unused, which is justified because the only player verb in this game is "click a cell" — adding arrow keys would be wasted; clicking off-board cleanly maps to "wait" with no separate verb needed.
- Risk surfaced for critique_spec: the per-mechanic counterfactual at L3 for "dual couriers" is a structural one (terminal+stops require both couriers); the post-discovery planning argument hinges on a *specific* heuristic-vs-witness divergence at the swap junction, which may need tightening if critique flags it as not concrete enough.
