# Step #02: pick_mechanic

## Inputs Consumed
- Run input (from harness invocation): no user seed → autonomous mode.
- skills/mechanic-novelty/taxonomy-of-25-games.md (from #01 study).
- skills/mechanic-novelty/similarity-check.md and negative-similarity-check.md (from #01 study).
- skills/mechanic-novelty/prior-games-index-format.md (from #01 study).
- prior-games/index.md (60 prior entries).
- skills/design-constraints/core-knowledge-priors.md (from #01 study).
- skills/code/id-generation.md (from #01 study).
- Selected prior screenshots: prior-games/kj82, pv5q L1; reference m0r0 L1 (negative-similarity grounding).

## Deliverables Produced
- `mechanic-pick.md`: 4-char ID `dj5h`; mechanic family `pulley-pair-platform`; one-paragraph description ("Pulley-Pair Platform Walk" — coupled binary platform-pair toggling via overhead pulley + avatar walking); concrete distinguishing rules vs near-misses (m0r0, pv5q, kj82, pn5d, xv2b, kn58, mr5q, vt6q, wb6n); negative-similarity table walking the 8 dimensions across priors; verdict NOVEL.

## Notes
- The mechanic uses three priors: physics (length-conservation), objectness (platforms/weights/pins), geometry/topology (graph reachability through walkable cells).
- Action mapping: arrows = walk, ACTION6 click = select pulley, ACTION5 = toggle active pulley. ACTION7 omitted (no meaningful undo for binary toggles — "toggle again" is the natural inverse).
- ID generation procedure: picked random 2-letter prefix `dj`, 2-char suffix `5h`; verified non-collision against 25 reference + 60 priors; not an English word.

