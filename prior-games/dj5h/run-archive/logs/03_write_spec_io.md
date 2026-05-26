# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02 pick_mechanic): ID `dj5h`, mechanic family `pulley-pair-platform`, novelty argument.
- skills/code/spec-template.md, universal-scaffold.md, novaengine-api.md (from #01 study).
- skills/design-constraints/checklist.md, composition-and-tutorial.md, difficulty-rules.md, core-knowledge-priors.md, forbidden-elements.md (from #01 study).
- skills/conventions/from-tech-report.md, reference-game-patterns.md, cross-cut-frequencies.md (from #01 study).
- skills/global/action-enum.md, color-legend.md, paths.md (from #01 study).
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md (from #01 study).

## Deliverables Produced
- `mechanic-spec.md`: full 9-section spec for dj5h (pulley-pair-platform). 3 levels with explicit per-level mechanic counts (L1=3, L2=4, L3=5; +1 per promotion), counterfactual necessity per mechanic per level, witness solutions, difficulty justifications including post-discovery decision-space enumerations and named trivial heuristics, action mapping with `_get_valid_actions()` semantics, HUD/state inventory with persistent visual cues for every internal state, win/lose predicates, novelty cross-check.

## Notes
- The L3 design required iteration: an initial same-phase cable-link made M5 redundant. Resolved by switching PA/PC to **opposite-phase coupling**, which makes the cable-toggle witness-required (the pre-toggle initial state provides bridges 1-2 but blocks bridge 3; the cable-toggle is the unique mechanism that flips bridge 3 into existence, while peg-pickup is already done by then so PA's blue going HIGH is harmless).
- The witness for L2 has a tricky "step-off-platform-before-toggle" requirement to avoid carrying the avatar away from the post-drop position; spec describes this explicitly and the implementation must respect it.
- Geometric details (column ranges, exact island boundaries, exact display-pixel click coords) are intentionally left as "implementation tunes geometry"; the spec's intent is conveyed via cell-level layout while implementation finalises pixel-precise placement to make the witness lengths land.
- The 5-mechanic count for L3 was confirmed against the +1-or-+2 rule. L1 = 3 (walk + select + toggle); L2 = 4 (+ peg/socket); L3 = 5 (+ cable-linkage).

