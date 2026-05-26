# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02 pick_mechanic): ID `kf42`, family `tether-pawn-cycle`, novelty justifications.
- workspace/study-notes.md (from #01 study): cross-cut frequencies for HUD/action conventions; recurring design moves (per-level layering, depleting bar, tag-based grouping, animation cursor, two-sprite swap).
- skills/code/spec-template.md: the 9 mandatory subsections.
- skills/code/universal-scaffold.md: file structure conventions for §3 and §6.
- skills/code/novaengine-api.md: API surface for HUD widgets and `_get_valid_actions`.
- skills/code/id-generation.md: confirmed `kf42` valid.
- skills/global/action-enum.md, color-legend.md, paths.md: action slot semantics + palette legend.
- skills/design-constraints/{core-knowledge-priors,forbidden-elements,composition-and-tutorial,checklist}.md: full constraints for §2, §3, §4, §7-9.
- skills/mechanic-novelty/similarity-check.md: re-applied at §9 of the spec.
- skills/mechanism-details/m0r0.md, r11l.md, sk48.md, ls20.md: re-grounded near-miss distinguishing rules.

## Deliverables Produced
- workspace/mechanic-spec.md: 9-section spec covering title, mechanic family (3 priors used), sprite roster (5 entries), level progression (EXACTLY 3 levels with composition arc), action mapping (5 of 7 slots, with `_get_valid_actions` gating before first selection), HUD widgets + per-game state + hidden-state shape, testable win/lose predicates, novelty note re-grounded against the four taxonomy near-misses + empty prior-games index.

## Notes
- Action set is `[1, 2, 3, 4, 6]` — five actions. ACTION5 and ACTION7 omitted.
- Hidden state encodes (active_pawn_index, remaining_steps, two pawn colours). Required because two frames where the *visible* pawns sit at the same coordinates but the *active* one differs are distinct in graph identity.
- The cycler is collapsed to a single-step direct cycler at L2 and a 3-colour cycle at L3, so L3's composition rests on choosing both *which* pawn cycles AND *which* corridor it traverses (rather than counting cycle steps).
- Step budgets (30/50/80) chosen so: (a) L1 random-policy solubility is non-trivial but possible (~14 actions optimal vs 5-action search space); (b) L2 random has ~zero chance of routing one pawn through the cycler and getting both onto the right pads; (c) L3 same with deeper composition. These match the reference-game pattern (most non-tutorial levels are random-policy unsolvable per the deep-analysis frequency tables).
