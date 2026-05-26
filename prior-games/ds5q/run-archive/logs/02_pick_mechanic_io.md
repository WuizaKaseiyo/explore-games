# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (HITL not allowed; no run seed → autonomous mode).
- skills/mechanic-novelty/taxonomy-of-25-games.md (25 reference families).
- skills/mechanic-novelty/similarity-check.md (positive distinguishing-rule procedure).
- skills/mechanic-novelty/negative-similarity-check.md (8-dimension overlap test, kf42→vh68 cautionary tale).
- prior-games/index.md (41 prior generated games).
- skills/code/id-generation.md (4-char ID procedure + reserved list).
- skills/code/spec-template.md, skills/code/universal-scaffold.md (preview for write_spec & implement).
- skills/design-constraints/core-knowledge-priors.md (4 allowed priors).

## Deliverables Produced
- `workspace/mechanic-pick.md` — id `ds5q`, family `wall-erode-chain`, full description, positive + negative similarity analysis against the closest 5 priors and reference games, palette plan.

## Notes
- Trialed and rejected (overlap risk): refraction-prism (bx84), sub-grid rotation maze (lp85+tu93 overlap), shape-overlay (re86), zone-gravity (tg6w), spring-launch (kj82), wavefront-tuning (pf3w), Lights-Out (existing video game), CGoL (existing automaton), echo-chamber (bx84), waterfall-cascade (sp80), domino-fuse (vn8d), pressure-plate Sokoban (ka59 / wa30), drift-zone (tg6w), lattice-trim marbles (vd3g + kp9z).
- Action subset narrowed to `[1,2,3,4,5]` (no click) to avoid the click-to-edit-terrain surface signature shared by xn5p / vd3g / kp9z / qm4t.
- L1 = walk + erode-adjacent (single hardness, single uncoloured pickaxe). L2 = +1 (colour-matched-pickaxe via charge-pad). L3 = +1 (colour-chain-hardness — same-colour walls share a global hardness counter, forcing chain-erode of an unreachable wall).
- ID `ds5q`: prefix "ds" + suffix "5q". Not a recognisable English word; not in reserved or prior list.
