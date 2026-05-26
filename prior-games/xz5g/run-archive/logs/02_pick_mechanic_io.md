# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (for seed policy: no seed → autonomous)
- skills/global/* (action enum, palette, paths)
- skills/design-constraints/* (priors, forbidden, composition, checklist, difficulty)
- skills/mechanic-novelty/{taxonomy-of-25-games, similarity-check, negative-similarity-check, prior-games-index-format}.md
- skills/code/id-generation.md (4-char opaque ID rules)
- prior-games/index.md (45 entries) — checked for ID + family collisions
- prior-games/{hp9c,vy3k,pv5q}/mechanism-detail.md (closest-mechanic deep dives)
- skills/mechanism-details/{cn04,sb26,m0r0}.md (sampled in study)

## Deliverables Produced
- mechanic-pick.md: game ID `xz5g`, mechanic family `arena-pivot-rotate`,
  one-paragraph description, distinguishing rules vs vy3k / hp9c / cn04 /
  qj4r-rj5w-wj7d / pv5q / qz73, negative-similarity-check walkthrough.

## Notes
- ID xz5g passes collision check against 25 reference + 45 indexed prior +
  9 untracked prior-games dirs.
- Closest novelty risk is vy3k (region-swap-arrange): both use click +
  ACTION5-commit-rotate. Distinguishing rule rests on
  *continuous-pivot vs 4-quadrant-choice* (negative-similarity Principle 3
  core-dynamic divergence) plus committed visual-signature distinctions
  (no quadrant frames, distinct pivot-halo, denser pixel grain).
- Will re-run negative-similarity-check in critique_spec against fleshed-
  out L2/L3 — if drift toward discrete-choice feel, revise.
- Considered and rejected during pick: stamp-clone-cohort (m0r0 overlap),
  echo-stamp parallel ghosts (m0r0 overlap), cellular-step (Conway
  novelty axis 1 risk), wind-drift-anchor (g50t/kn58 partial overlap),
  ballistics arc launcher (cd82 + bx84 partial overlap), pipe-rotate
  routing (bx84 close), guards' sight-cone evasion (lq5x cone-rendering
  inverse, axis-1 risk).
