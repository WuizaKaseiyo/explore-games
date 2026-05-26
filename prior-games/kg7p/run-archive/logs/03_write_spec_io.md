# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02): ID kg7p, mechanic family beam-tether-haul, L1/L2/L3 sketch.
- skills/code/spec-template.md (from harness): 9-section spec structure.
- skills/code/universal-scaffold.md (from harness): scaffold layout, item 20 cell-grain rules, semantic-name rule.
- skills/code/novaengine-api.md (from harness): Sprite/Level/Camera/NovaBaseGame signatures.
- skills/design-constraints/* (from #01): checklist (items 11, 12, 19, 20, 22), composition-and-tutorial, difficulty-rules, forbidden-elements.
- skills/conventions/* (from #01): reference-game-patterns, cross-cut-frequencies.

## Deliverables Produced
- mechanic-spec.md: 9 sections — Title, Mechanic family, Sprite roster, Level progression with per-level mechanics + counterfactual necessity + witness + four-bullet difficulty justification (per level), Action mapping, HUD and state, Win condition, Lose condition, Novelty note (taxonomy + prior-games + re-run of negative similarity check).

## Notes
- Action subset `[1, 2, 3, 4, 5]`. No ACTION6, no ACTION7. ACTION5 = distinctive verb (beam toggle).
- Mechanic count per level: L1=2, L2=3, L3=4. Strict +1 per level (composition-and-tutorial.md compliance).
- Counterfactual for L3-M4 uses geometric argument: `block_D`'s east-haul path passes through `(5, 5)` where `block_C` sits, forcing delivery order. This catches the "deliver nearest first" trivial heuristic.
- Step budgets: L1=40 (witness 9), L2=70 (witness 35), L3=80 (witness 25). All ≥ 2× witness, non-shrinking.
- Win predicate: every block on tag-matching target by exact (x, y) pixel coords (stride-4 snapped). Lose predicate: step_count ≥ budget.
- "No hidden state" cues (item 19): beam_indicator sprite (visible green ring) marks beam-on AND highlights coupled block; avatar's green emitter row marks facing direction.
- "Low-resolution" guard (item 20): 4×4 sprites with internal pattern (hollow centers, chevrons, hatch, checker). Logical grid is 16×16 at stride 4 inside 64×64 frame.
- "ACTION7 strict-undo" (item 22): satisfied trivially — ACTION7 not in `available_actions`.
- L1 has no strict planning; L2 moderate post-discovery (4 plausible first actions named); L3 challenging (5 plausible first actions; greedy heuristic named and its failure point geometrically located).
- Aesthetics: palette deliberately diverges from wa30 / kn58 / vt6q (the closest priors). Light-blue avatar, yellow blocks, blue-orange/red targets, grey walls, pink-checker barriers, green beam.
- Open question for critique: per checklist item 12, the L3 counterfactual argument for M4 should be re-derived per alternate strategy — current spec walks one alternative (deliver-D-first); the critique state should enumerate any other plausible alternates.
