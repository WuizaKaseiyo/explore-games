# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02 pick_mechanic): the chosen mechanic, ID, and similarity-check.
- skills/code/spec-template.md: the 9-section structure.
- skills/code/universal-scaffold.md: file structure, naming rules, viewport-resize requirement.
- skills/code/novaengine-api.md: API cheatsheet (Sprite, Level, Camera, NovaBaseGame, InteractionMode).
- skills/design-constraints/composition-and-tutorial.md: 3-level rule + per-level mechanics rule (+1 or +2 per promotion, no drop-out).
- skills/design-constraints/checklist.md: 22 items.
- skills/design-constraints/difficulty-rules.md: per-level (a/b/c/d) bullets.
- skills/design-constraints/forbidden-elements.md: no letters/digits/clipart.
- skills/design-constraints/core-knowledge-priors.md: §3.4 prior categories.

## Deliverables Produced
- mechanic-spec.md: the full 9-section spec for tj4n.
  - Section 4 fully enumerates per-level mechanics (L1: 2; L2: 4; L3: 6) — each promotion adds exactly 2 new mechanics. Every prior-level mechanic remains required.
  - Witness solutions are written out action by action for L1 and L2; L3 is described at outline level (would be ~72 actions of similar texture).
  - Per-mechanic counterfactual necessity is given for every level.
  - Difficulty justifications cover (a)/(b)/(c)/(d) per level.

## Notes
- L3's witness is given as a 3-loop sketch rather than full action enumeration to keep the spec readable; the implementation will follow the same shape.
- The pursuer mechanic (M5) plus closure-leaves-walls (M6) are the two L3 additions. M5+M6 compose: walls from earlier closures bottleneck the pursuer's BFS path, forcing the witness to order closures carefully. This is the L3 composition in the §3.4 sense.
- ACTION7 (undo) is included to soften the "every step is permanent" feel of the trail mechanic; ACTION7 is strict-undo per global/action-enum.md.
- The 16×16 logical grid scaled to 64×64 with 4×4 sprite cells avoids the chunky-block anti-pattern (checklist item 20) by ensuring every primary sprite has internal pixel detail (avatar has eye-dot, trail has ring, target has central dot, forbidden has X, pursuer has eye-dots, wall has cross-hatch).
- Aesthetic direction: blue-pink-yellow-red palette with off-white background and black accents. No symbol/letter/digit shapes; all sprites are abstract topology (rings, crosses, diamonds).
