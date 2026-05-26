# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (autonomous mode — no seed)
- skills/global, skills/design-constraints, skills/mechanic-novelty, skills/mechanism-details, skills/code (registered)
- skills/mechanic-novelty/taxonomy-of-25-games.md (full)
- skills/mechanic-novelty/similarity-check.md (full)
- skills/mechanic-novelty/negative-similarity-check.md (full)
- prior-games/index.md (22 prior games)
- spot-checked prior mechanism-detail.md files for near-misses (zk9p, gv47, lv4k)

## Deliverables Produced
- mechanic-pick.md: 4-char ID `xn5p`, family `chamber-stamp-partition`. Pawn walks a chamber and stamps walls to subdivide a single connected region into per-colour subregions. L1 walk+stamp+partition; L2 adds pushable molecules; L3 adds decaying stamps. Distinguished from gv47 (grow vs partition), zk9p (stationary molecules vs autonomous pursuers), and ka59 (no stamp verb, topological-vs-positional win).

## Notes
- Initially considered herd-shepherd-flee but rejected via negative-similarity check vs zk9p (sharing 5-6 of 8 axes).
- Topology-of-connectedness is under-explored in both reference + priors; chosen as the hunting ground.
- ID `xn5p` matches the `<2 letter><digit><letter>` pattern common in priors (`bx84`, `wt39`, `kp9z`, `kn58`, `lv4k`).

