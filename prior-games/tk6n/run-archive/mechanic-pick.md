# mechanic-pick.md

## Game ID
**tk6n** — 4-character lowercase, opaque (not an English word), not in
the 25-reference list, not in `prior-games/index.md` (verified by
inspection).

## Mechanic family
`boomerang-arc-catch`

## One-paragraph description

Avatar walks one cell per arrow press and carries a single boomerang.
Pressing ACTION5 throws the boomerang in the avatar's last-faced
cardinal direction. The boomerang flies as an animated sprite, advancing
ONE cell per subsequent player action: outbound for `K = level_data
"throw_range"` cells in the throw direction, then it switches to a
HOMING return phase — each tick of the return phase, the boomerang
takes one cell in the cardinal direction whose Manhattan-distance
component to the AVATAR's CURRENT cell is largest (ties broken: x then
y). The boomerang lights coloured TARGET sprites it overlaps on either
the outbound OR return path; once a target is lit it stays lit. While
the boomerang is in flight the avatar can still walk freely — and the
RETURN PATH BENDS to chase wherever the avatar walks. The boomerang is
caught (returns to "held") when its cell coincides with the avatar's
cell on a return-phase tick. If the boomerang is currently flying it
cannot be re-thrown; ACTION5 is gated to no-op while in-flight.

Action subset: `[1, 2, 3, 4, 5]` (no click; ACTION7 OMITTED per
`action-enum.md` strict-undo rule because the game has no undo).

Core-knowledge priors used:
- **Objectness** — boomerang is a coherent persistent object that
  occupies a cell and can be in different states (held / outbound /
  returning).
- **Basic physics** — straight-line projection, then return-toward-
  avatar; the player learns the trajectory rule from a single L1
  throw.
- **Basic geometry & topology** — at L2, walls of two heights gate
  the projectile's outbound path; the player must aim through gaps.

The win condition is a small target-cover predicate: every TARGET
sprite in the level has been lit by the boomerang AND the boomerang
is currently held by the avatar. Lose: step budget exhausted.

## Closest taxonomy entries — concrete distinguishing rules

(Walked the 25-row taxonomy. Closest five named below.)

1. **vt6q (prior-game) — grapple-anchor-yank.** vt6q's ACTION5 fires
   a directed cardinal grapple line that resolves *INSTANTLY* on its
   first non-fence hit and either yanks the avatar to the anchor or
   slides the anchor to the avatar's adjacent socket; the line is a
   single-tick effect with no flight phase, no return, no target-
   lighting. tk6n's ACTION5 launches a *MULTI-TICK* projectile that
   travels OUTBOUND-then-RETURNS, lighting targets along the path
   on both legs, with the return path RE-AIMED EACH TICK at the
   avatar's CURRENT cell — a dynamic the avatar's continued walking
   actively reshapes. The verbs (instant pull vs delayed catch),
   the dynamic (one-tick yank vs multi-tick path-painting), and the
   win condition (avatar+sockets vs targets-cover-by-flight-path)
   are all distinct.

2. **bx84 (prior-game) — beam-mirror-reflect.** bx84 has a
   *CONTINUOUSLY EMITTING* coloured beam, and the player verb is
   PLACING and CYCLING mirrors so the beam's instantaneous endpoint
   sits on a target. The beam is steady-state — at any frame the
   beam's full path is rendered. tk6n's projectile is a *DISCRETE
   POINT* travelling cell-by-cell over many ticks; there is no
   beam, no mirrors, no place-mirror verb, and the player cannot
   "see" the future trajectory because the return leg DEPENDS ON
   FUTURE AVATAR MOVEMENT. The novelty axis is steady-state-spatial
   (bx84) vs transient-temporal-with-feedback (tk6n).

3. **wt39 (prior-game) — glide-deflect-thaw.** wt39's *AVATAR*
   glides until a wall and bounces off bumpers — the avatar is the
   moving entity, the puzzle is routing the avatar. tk6n's avatar
   walks one cell per arrow (no glide); the entity that glides is
   a *SECOND* object, the boomerang, which the avatar throws and
   catches. The two-body dynamic (avatar walks while boomerang
   flies) is structurally different from a single-body glide.

4. **bw7k (prior-game) — actor-replay-shade.** bw7k's stepping on a
   coloured anchor SPAWNS a same-coloured shade that REPLAYS the
   actor's recent path. tk6n has no recording of avatar moves, no
   shade or replay; the projectile follows a forward-projected
   geometric rule, not a recorded action history.

5. **vn8d (prior-game) — domino-cascade-topple.** vn8d's click
   triggers a single-tick CHAIN REACTION through pillars in
   topology-determined order. tk6n has no chain reaction — a single
   ACTION5 launches a single boomerang along a *spatial* trajectory,
   not a topological cascade. There are no chained activations and
   no transitive triggers.

(Other taxonomy near-misses considered and ruled out without
deeper write-up: pf3w wavefront-converge-timing — pf3w's BFS-
radius wavefronts spread concentrically from STATIC emitters
clicked at level start; tk6n's projectile is a single point on
a 1D linear track that returns. qn7w pulse-chain-eject — qn7w
ejects only the terminal ball of a static chain; tk6n's
boomerang is a single moving object with no chain. kn58 anchor-
pull-magnet — kn58 magnetically slides every coloured pawn one
cell toward an anchor each click; tk6n moves one boomerang
along a path, not many pawns toward a point.)

## Negative similarity check (per `negative-similarity-check.md`)

Walked the 8 dimensions against vt6q (the closest prior in
verb shape):

1. **What's on the board.** vt6q: avatar + walls + anchors +
   sockets + fences + goal pad. tk6n: avatar + walls + targets
   + boomerang. **Distinct rosters.**
2. **What the player physically does on input.** vt6q: walk,
   fire grapple line, yank-resolution single-tick. tk6n: walk,
   throw boomerang, then continue walking *while it flies*.
   **Distinct verb timing** (single-tick resolution vs multi-tick
   coexistence).
3. **What the level is asking for.** vt6q: avatar on goal pad
   AND every socket holds a light anchor. tk6n: every target
   lit AND boomerang held. **Distinct win predicates.**
4. **What kills the player.** Step budget for both. **Shared.**
5. **The cast of supporting elements.** vt6q has fences (line-
   permeable but walk-blocking) and redirector-bend cells — both
   absent from tk6n. tk6n has TARGETS-along-path and walls of
   two heights — absent from vt6q. **Distinct.**
6. **Visible visual signature.** vt6q palette is dominated by
   anchor colours, fences, sockets. tk6n picks a different
   dominant palette (avatar = palettes 9 blue + 11 yellow +
   12 orange head; targets = palette 6 magenta; walls = palette 5
   black + palette 4 off-black). **Distinct dominant palette.**
7. **Pixel grain of primary sprites.** Both at full 64×64 grid_size.
   tk6n primary sprites have rich internal pixel pattern (avatar
   has eye-dot for facing, boomerang has bent-blade silhouette,
   target has starburst pattern). **Comparable richness; different
   silhouettes.**
8. **The core dynamic.** vt6q: spatial yank-pull problem.
   tk6n: temporal projectile-trajectory + path-cover problem
   where the player's continued walking REDIRECTS the return.
   **Distinct core dynamic.**

Shared dimensions (out of 8): only #4 (step counter — universal
across all 25 reference and 70 prior games). 1 shared. Threshold
for rejection is 3+. **PASS.**

Spot-checks against bx84, wt39, bw7k, vn8d: all share at most
1-2 dimensions (universal step counter; for bx84 also the
"object-shooting-projection" board element overlap on dim 1).
None reaches 3+. **PASS.**

## Outcome
Mechanic family `boomerang-arc-catch` is novel against the 25-
reference taxonomy and against `prior-games/index.md` (70 entries).
Game ID `tk6n` reserved. Proceed to `write_spec`.
