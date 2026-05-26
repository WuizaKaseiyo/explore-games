# Mechanic pick

## Game ID
**pq5w**

(4 chars, lowercase alphanumeric; not in the 25 reference IDs; not in
`prior-games/index.md`; not an English word.)

## Mechanic family
`portal-pair-relocate`

## Run input
(autonomous — no user seed)

## One-paragraph description
The playfield contains exactly TWO portal sprites that are linked as a
pair. The avatar walks the grid with arrow keys; stepping into a portal
cell teleports the avatar to the paired portal cell. ACTION5 RE-ANCHORS
the portal the avatar most-recently-emerged-from to the avatar's current
empty cell (only valid when the avatar stands on a non-portal floor cell
AND the most-recent-emerged-portal is set). The OTHER portal stays
fixed. So the player drags ONE portal at a time across the level by a
walk-through-then-relocate pattern. The goal is to reach a fixed goal
cell that is otherwise unreachable (separated by walls). Composition
across L2/L3 layers in: forbidden cells that fail the level if the
avatar steps on them after a teleport (so picking when to teleport
matters), and a second portal pair colour-coded so each pair only
links to its own match (so the player must reason about which pair to
relocate when).

Core-knowledge priors used: **objectness** (avatar, portals, walls,
goal as persistent entities) and **basic geometry & topology**
(portal pairs establish a non-spatial connectivity that bypasses
wall-defined connectivity). No physics, no agentness — there are no
autonomous NPCs in this game.

## Near-miss similarity check (and concrete distinguishing rules)

### vs prior-games corpus

**jd4q — echo-trail-teleport.** jd4q has a fading-echo trail behind
the avatar; ACTION6 click teleports back to a chosen echo, CONSUMING
the trail. The teleport endpoints are dynamic (the avatar's recent
path) and the use is one-shot per teleport.
**Distinguishing rule for pq5w**: the portal pair is *fixed* (until
deliberately relocated via ACTION5) and *persistent* — repeated
walk-throughs traverse the same pair without consuming anything. The
relocate verb is what gives the player puzzle leverage; trail-based
teleport is fundamentally different.

**ek73 — wake-trail-evade.** ek73 has warp pads as a SECONDARY
mechanic; the primary verb is the avatar leaving a decaying-hazard
trail behind itself. Warp pads in ek73 are pre-placed and not
relocated.
**Distinguishing rule for pq5w**: pq5w's portal pair is the *primary*
verb, and the player MOVES it during play. There is no decaying-hazard
trail, and stepping on a previously-vacated cell is harmless.

**bx84 — beam-mirror-reflect.** bx84 is a click-to-place mirror puzzle
where a beam is the active entity; no walking avatar.
**Distinguishing rule for pq5w**: the active entity is a walking avatar
that traverses point-to-point via portals. There is no beam, no
projectile, and no click-to-place sub-game.

**vy3k — region-swap-arrange.** vy3k swaps entire quadrants of the
playfield. Avatar walks within a quadrant.
**Distinguishing rule for pq5w**: pq5w teleports the AVATAR's point
position via the portal pair — the playfield itself is unchanged.
Walls / goals / pickups stay where they are.

**kn58 — anchor-pull-magnet.** kn58 has click-to-place a single anchor
that pulls every pawn one cell along its dominant Manhattan axis.
**Distinguishing rule for pq5w**: kn58's interaction is sliding via
attraction; pq5w's is point-teleport via a paired link. The player in
kn58 places an anchor that affects MANY pawns; pq5w places a portal
that the avatar later walks INTO.

**xz5g — arena-pivot-rotate.** xz5g rotates sprites 90° around a
chosen pivot.
**Distinguishing rule for pq5w**: no rotation in pq5w; portals are
endpoints of a teleport edge, not pivots of a transform.

### vs the 25 reference taxonomy

No reference game has a portal-pair teleport mechanic. The closest is
`g50t` (walk-vs-scroll) where the world scrolls; that's a coordinate-
shift mechanic, not a teleport-pair, and its primary tension is
chase-the-edge, not connectivity-via-paired-cells.

## Negative similarity (per `negative-similarity-check.md`)
Walked the seven dimensions for jd4q (the closest prior). Universal
axes (walls, goal, step counter, walking-avatar) are shared as
expected; load-bearing axes (visual signature, pixel grain, core
dynamic) all diverge — pq5w has 2 distinctive paired ring-sprites,
no fading-echo cells, and a "drag-the-pair" core dynamic absent in
jd4q's "lay-then-consume". PASS.
