# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (autonomous mode, no seed).
- states/pick_mechanic.md.
- skills/global, design-constraints, mechanic-novelty (full re-read of similarity-check, negative-similarity-check, taxonomy-of-25-games, prior-games-index-format).
- skills/code/id-generation.md.
- skills/code/spec-template.md (peeked to confirm what mechanic-pick must enable for write_spec).
- mechanism-details (already in memory from study).
- prior-games/index.md (60 entries, just re-confirmed).

## Deliverables Produced
- `mechanic-pick.md`: ID `hl4n`, family `row-col-tint-cross`, one-paragraph description, similarity-check vs taxonomy + 60-game prior index, negative-similarity table vs 5 closest priors, action palette + camera + resources answers.

## Notes
- Decision rationale: the prior corpus is dense (60 games) and motion / magnet / mirror / fold / flow mechanics are heavily-occupied. Picked a non-motion, pure-click mechanic in the row+column space, distinct from the four prior row+column entries (lp85 shifts cells, vc33 swaps stones, qx7p slides bands, qf8m flips a fixed row+col cross) by recoloring stationary cells via row/column tint markers with override-then-blend composition.
- Considered and rejected: gravity-well/tractor-pull (too close to kn58, mr5q, nf3z on the negative-similarity test); sonar/echo (too close to lf52 fog-of-war); prism/refraction (covered by bx84); voronoi region claim (visually too close to xn5p partition); freeze/melt phase change (too close to pk4m duotone-flip-walk).
- Open question that defers to write_spec: how to make the L3 "bright-wins" blend rule discoverable without instructions. Plan: when both row + column have been set away from background, the cell shows the brighter (higher-palette-index) of the two; player learns this by clicking and seeing colors collapse. The brightness rule is also visually obvious (the higher-index color is always "stronger" — yellow > red > blue, in terms of the palette ordering's perceptual brightness).
- The chosen action palette `[6]` matches 5/25 reference games (lp85, r11l, vc33, sc25, ft09) so the player has soft-norm support for "pure click means look for clickable sprites".
