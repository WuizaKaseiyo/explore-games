# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md: no seed provided → autonomous mode.
- skills/mechanic-novelty/taxonomy-of-25-games.md: 25 reference mechanics.
- prior-games/index.md: 27 prior generated mechanics.
- skills/design-constraints/core-knowledge-priors.md: 4 allowed prior categories.
- skills/mechanic-novelty/similarity-check.md: positive novelty test.
- skills/mechanic-novelty/negative-similarity-check.md: 8-dimension overlap test.
- skills/code/id-generation.md: 4-char ID rules.

## Brainstorming
Surveyed unused territories; rejected:
- liquid-flow / pipe routing (overlaps sp80 pour-shelf-route).
- grow-tendril (overlaps sk48 paired-snake-trail, gv47 seed-grow).
- beam/prism (overlaps bx84 beam-mirror-reflect).
- pawn-chain tether (overlaps kf42 tether-pawn-cycle, r11l centroid-puppet).
- gravity-tilt-settle (overlaps tg6w settle-pile-tilt, bp35 gravity-fall).
- patrolling-NPC chase (overlaps zk9p pursuer-merge, ka59).
- weave / stamp-cycle (overlaps ft09 stamp-3x3-paint).
- color-region merge (overlaps gv47 seed-grow, hr8q pair-blend).

Selected territory: **player edits the playfield TERRAIN STATE; pawns flow downhill across that mutable terrain.** No prior game has cell-local height-state with adjacency-lowest-neighbor rolling. Closest priors:
- tg6w (settle-pile-tilt): one global tilt direction sliding all blocks to rim. My mechanic: per-cell binary terrain, pawns step at most one cell per click toward an adjacent low cell. Different operating principle (local gradient vs global tilt; one-cell-step vs slide-to-rim).
- kn58 (anchor-pull-magnet): single anchor pulls every pawn one cell along its dominant Manhattan axis. My mechanic: terrain CELLS are the state; pawns react to their immediate 4-neighbourhood, not to a global attractor.
- kp9z (grain-accumulate-topple): cells accumulate counts, overflow at capacity 4. My mechanic: cell binary state set by the player, no accumulation, no overflow.

## Deliverables Produced
- mechanic-pick.md: game ID `vd3g`, family `valley-dig-roll`, full one-paragraph mechanic description, similarity-check + negative-similarity-check tables vs 5 closest priors with concrete distinguishing rules.

## Notes
- Decision: clicking a cell toggles its binary HIGH↔LOW state. Marbles on HIGH cells roll one cell into the priority-N→E→S→W lowest neighbour each click; marbles on LOW cells stay. Two marbles can't share a cell — yields stay put. Win = each marble on its matching-colour target low-cell.
- L1 mechanic = terrain-toggle + roll-to-low.
- L2 +1 mechanic = immutable WALL cells (not toggleable, marbles never enter).
- L3 +1 mechanic = LINKED ANCHOR pairs — toggling one cell auto-toggles its paired cell at a remote location.
- All within physics + objectness + topology priors.
