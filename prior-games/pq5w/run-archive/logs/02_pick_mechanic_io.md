# Step #02: pick_mechanic

## Inputs Consumed
- mechanic-novelty/taxonomy-of-25-games.md (full table)
- mechanic-novelty/similarity-check.md, negative-similarity-check.md
- prior-games/index.md (67 priors)
- code/id-generation.md
- skills/mechanism-details/* (selectively for near-miss disambiguation)

## Candidate
- Family tag: portal-pair-relocate
- 4-char ID: pq5w (lowercase alphanumeric, not in reserved 25, not in prior-games index, not an English word)
- Run input seed: (autonomous; no seed)

## Near-miss survey
- jd4q echo-trail-teleport: trail-based, consume-on-teleport (different).
- ek73 wake-trail-evade: warp pads as auxiliary, primary verb is wake-decay (different primary verb).
- vy3k region-swap-arrange: regional 4-quadrant rotation/swap (different — point-to-point vs region).
- bx84 beam-mirror-reflect: beam-and-mirrors (no avatar walk; click-to-place).
- xz5g arena-pivot-rotate: rotate sprites around clicked pivot (no teleport).
- kn58 anchor-pull-magnet: magnet pulls pawns one cell toward click (no teleport, slide motion).

## Negative-similarity check
Compared mental render of candidate L1 against jd4q (the closest):
- (1) board: walking avatar + walls + goal + 2 portals (vs jd4q: walking avatar + walls + goal + trail of fading echoes). Common ≈ universal walls/goal.
- (2) verb: walk + ACTION5 = relocate-portal (vs jd4q: walk + ACTION6 click = teleport-back-consuming-trail). Different.
- (3) goal: reach a goal cell. SAME (universal).
- (4) lose: step counter. SAME (universal).
- (5) supporting: portal pair, relocate verb. Different.
- (6) palette: my plan uses 2 portal-tone colors + avatar color + walls + goal-cross. jd4q's palette has fading echoes. Different visual signature.
- (7) pixel grain: portals can be 4×4 paired rings. Different.
- (8) core dynamic: "drag-and-drop one portal at a time to bypass walls" vs "lay-then-collapse a path". Different.
Shared on universal axes only (walls, goal, step counter, walking). 1 + 3 + 4 are universal-shared; the load-bearing axes (6, 7, 8) all diverge. PASS.

## Distinguishing rules
1. vs jd4q (echo-trail-teleport): jd4q uses a path-history of fading echoes consumed when teleporting. pq5w has 2 PERSISTENT portal endpoints whose pairing is stable across turns; ACTION5 RE-ANCHORS the most-recently-used portal at the avatar's current cell, leaving the other unchanged. No trail; no consumption.
2. vs ek73 (wake-trail-evade): ek73's warp pads are AUXILIARY pieces (pre-placed pairs that move into place once); pq5w's portal pair is the PRIMARY verb, and the player RE-POSITIONS them mid-level via ACTION5. ek73's primary verb is wake-decay-evade; pq5w has no decaying floor.
3. vs bx84 (beam-mirror-reflect): bx84 places mirrors and shoots beams; click-driven projectile mechanic. pq5w has a walking avatar (no beam, no projectile). The connecting line in pq5w is the avatar's TELEPORT, not a propagated beam.
4. vs vy3k (region-swap-arrange): vy3k swaps full quadrants; pq5w swaps avatar's POINT-position via portal pair. Quadrant != endpoint.

## Mechanic family description
The playfield contains exactly TWO PORTAL sprites linked as a pair. The avatar walks the grid via arrow keys; stepping into a portal cell teleports the avatar to the paired portal cell (paired-pixel matching their visible pairing colours). ACTION5 RE-ANCHORS the portal that was MOST RECENTLY entered to the avatar's current cell (only valid when the avatar stands on an empty floor cell, not on a portal). The OTHER portal stays in place. So the player drags one portal at a time across the level by walking-through-then-relocating, opening fresh teleport pairs that bypass walls. Goal: reach a fixed goal cell.

Core knowledge priors used:
- objectness (avatar, portals, walls, goal — persistent and movable),
- topology (the portal pair establishes a "connection" between two cells that bypasses spatial connectivity defined by walls).

## Deliverable
Wrote workspace/mechanic-pick.md with mechanic-family tag, 4-char ID, the description, and the per-near-miss distinguishing rules.
