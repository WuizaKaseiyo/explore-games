# Mechanic pick

## Game ID
`bw7k`

ID-generation check: 4 lowercase chars (b, w, 7, k); not in the 25
reserved reference IDs; not in `prior-games/index.md`'s game_id
column (closest b-prefix entry is `bx84`); does not match any
`prior-games/<id>/` folder on disk (verified against `ls
prior-games/`); does not spell an English word.

## Mechanic family
`actor-replay-shade`

## One-paragraph description

A single coloured **actor** pawn walks the grid one cell per arrow
press. The actor's last N steps live in a small **move-tape**
rendered along one edge of the screen as an N-cell row of
direction-glyphs (a tape of recent input directions, decaying off
the left edge as new entries arrive on the right). Scattered on
the playfield are **shade-anchors** — small coloured rune-pads,
each paired with a same-coloured **shade-target** elsewhere on the
grid. When the actor walks onto a shade-anchor, a same-coloured
**shade pawn** spawns at the anchor cell and immediately begins
replaying the actor's current N-move-tape, one cell per game
turn — walking the recorded directions ghost-pawn-style. A shade
that runs out of recorded moves stops where it lands; a shade
blocked by a wall stops short. The actor continues to walk during
the shade's replay; further actor moves DO NOT update an already-
walking shade's tape (each shade carries the snapshot it was born
with). The level wins when the actor stands on its same-coloured
goal AND every spawned shade stands on its same-coloured shade-
target — all simultaneously satisfied. Step budget per level
provides the lose trigger; running out of budget calls `lose()`.

The mechanic combines **objectness** (actor + shades + walls), 
**basic geometry/topology** (paths through corridors, the actor's
path-shape determines the shade's path-shape from a different 
start), and **agentness** (shades behave with apparent intent — 
they walk autonomously, traceable to a recent player decision but
not directly steerable once spawned).

## Action mapping (preview for spec §5)

- ACTION1/2/3/4 — walk the actor one cell up/down/left/right.
- (No ACTION5, ACTION6, ACTION7 needed for L1-3; the mechanic is
  arrow-only. Subset = `[1, 2, 3, 4]`.)

## Per-level mechanic introduction (preview for spec §6)

- **L1**: actor + walls + actor-goal + ONE shade-anchor + paired
  shade-target. The witness walks a route that, by passing through
  the shade-anchor, spawns a shade whose replay-tape lands the
  shade on its target while the actor continues to its goal. Both
  delivered; level won.
- **L2**: adds a SECOND shade-anchor of a different colour with
  its own paired target. Both shades' replay-tapes are snapshots
  taken at their respective spawn times — so the actor's path
  before each anchor must encode a path that, replayed from that
  anchor's position, lands the corresponding shade on its target.
- **L3**: adds shade-permeable / shade-blocking walls (walls that
  block the ACTOR but NOT the shades, OR walls that block the
  SHADES but not the actor — visually distinguishable by palette).
  Composition: the actor must thread through actor-blocking walls
  while leaving a tape that, once replayed by a shade from the
  spawn anchor, navigates THROUGH a different wall geometry to
  reach its target. Every L1 mechanic and every L2 mechanic still
  required by L3's witness.

## Similarity check — taxonomy of the 25 reference games

For every taxonomy entry, the family-level check fails (no shared
mechanic_family tag matches `actor-replay-shade` or shares the
first two hyphen-words). Description-level check flags the
following near-misses, each with the deeper deep-analysis read:

1. **tn36 — program-pawn-trace**. Both involve a sprite executing
   a sequence of moves. But tn36 builds the programme via
   click-buttons in a slot-tray UI; the pawn waits passively while
   the player programmes, then a run-button executes. **bw7k has
   no programme buttons**: the move-tape is implicit and continuous,
   recorded as the actor walks; shades are autonomous companions
   that replay the actor's RECENT walking, not a buttonned-up
   programme. Different control surface (arrow walk vs click-on-
   buttons), different sprite roles (one programmable pawn vs
   actor + shade duo), different action subset (`[1,2,3,4]` vs
   `[6]`).

2. **zk9p — pursuer-merge-walk**. zk9p has autonomous AI pursuers
   that path toward the avatar each turn and merge on collision.
   bw7k's shades are autonomous but their motion is **literal
   replay of the actor's recent path**, not pursuit. zk9p's win
   is "all pursuers gone"; bw7k's win is "actor on its goal AND
   shades on their targets" — friendly companions, not foes.
   Distinguishing rule: the shade's per-turn direction is the
   k-th element of the recorded tape, never a pursuit step.

3. **ek73 — wake-trail-evade**. ek73 leaves decaying-hazard cells
   behind the avatar (vacated cells become hazards). bw7k's recent
   moves are kept as a *tape* (a list of directions, not cells).
   The tape only matters when a shade is spawned and replays it —
   walked cells are not hazards in bw7k. Distinguishing: in ek73
   the trail kills you; in bw7k the trail is a pattern your
   companion will retrace.

4. **jd4q — echo-trail-teleport**. jd4q's "echo" is a fading
   visual ECHO of visited cells that the player can teleport BACK
   to (consuming the trail). It is a static visual record, not a
   moving entity. bw7k's "shade" is a SPAWNED MOVING pawn that
   replays a recorded direction-tape. The names share the
   "echo/shade" lexical family but the mechanics are distinct:
   jd4q stores a CELL-trail (positions you've been); bw7k stores a
   MOVE-tape (directions you pressed) and uses it to drive an
   autonomous companion. Distinguishing rule: jd4q's trail is read
   by the actor (teleport); bw7k's tape is read by the shade
   (replay).

5. **m0r0 — mirror-orb-merge**. m0r0 has TWO orbs that move in
   mirrored fashion (UP moves both up; LEFT moves one left and
   the other right). bw7k has ONE actor that the player controls
   and a shade that REPLAYS ALREADY-WALKED moves. Distinguishing
   rule: in m0r0 the second orb's move on tick T is an algebraic
   transform of the player's tick-T input (mirror); in bw7k the
   shade's move on tick T is the player's tick-(T-K) input
   (delayed playback) where K is "ticks since the shade was
   spawned." The functional dependency is on the actor's *past*,
   not its *present*. Different mathematical relationship.

6. **lf52 / bp35 — procedural-graph-walk(-undo)**. Token traverses
   procedurally-built graph; click + undo. No move-tape, no
   shades. Different game shape entirely (graph nodes vs free-grid
   walking). Cosmetic surface overlap (a token moves on a board)
   but no mechanic-family kinship.

No other taxonomy entries flag for description-level overlap.

## Similarity check — `prior-games/index.md` (60 prior generated games)

Family-level scan: no `*-replay-*` or `*-shade-*` or `*-shadow-*`
or `*-echo-*` family except:

- `jd4q — echo-trail-teleport` (also in taxonomy near-misses,
  handled above; no further argument needed).
- `vp6h — shadow-cast-collect`. The "shadow" here is the
  illuminated/shaded region on the floor cast by overhead
  lanterns. Distinguishing rule: vp6h's shadows are STATIC
  illumination-region cues for collection; bw7k's shades are
  AUTONOMOUS REPLAY companions. No shared mechanic verb.
- `zk9p — pursuer-merge-walk` (handled above).
- `ek73 — wake-trail-evade` (handled above).

Additional prior near-misses checked at description level:

- `tn36-style "program-and-execute"` is not in the prior corpus
  (the closest scripts are `pf3w wavefront-converge-timing` —
  click-pre-placed-slots-then-tick — which is closer to a
  global-clock mechanic than an action-tape mechanic, and `kp9z
  grain-accumulate-topple` which is purely a chain-reaction with
  no recorded-history component).
- `kw8t — totem-los-link` (auto-emit beams between same-colour
  totems): superficial colour-matched-pair similarity but no
  recording or replay.
- `wb6n — tether-pin-wrap` (pawn on fixed-length leash): static
  rope geometry, no replay.
- `pj7k — rolling-cube-face-paint`: cube rolls and deposits face
  colour; faces permute as the cube rolls. The "deposit colour as
  you walk" surface is similar to "drop a tape entry as you walk",
  but pj7k deposits ONTO CELLS (colouring the floor), and the
  cube's NEXT face is determined by ROTATION mechanics. bw7k
  records DIRECTIONS to a TAPE (not cell-colour) and never
  modifies the floor. Distinguishing rule: pj7k mutates floor
  pixels via a cube's roll; bw7k mutates an off-grid tape via
  player input.

No prior matches all three criteria (win condition + primary
action + primary constraint) at the description level. The
positive similarity-check therefore returns **NOVEL**.

## Negative similarity check — `negative-similarity-check.md`

Walking the eight dimensions of the negative test against each
flagged near-miss (taxonomy + priors above):

Comparison vs **tn36** (closest in role-to-role mapping —
"sprite executing a recorded list of moves"):
1. *On the board*: tn36 = runway tiles + slot-buttons + 1 pawn;
   bw7k = open grid + actor + shades + anchor-pads + targets +
   walls. Different.
2. *Player input*: tn36 = clicks (buttons + run-button); bw7k =
   arrow walks. Different.
3. *Level asks*: tn36 = "make pawn's traced path light up the
   target pattern"; bw7k = "deliver actor + shades to colour-
   matched goals". Different (path-painting vs entity-routing).
4. *Kills*: step budget for both. Shared.
5. *Supporting cast*: tn36 = programme-buttons, target-pattern
   tiles; bw7k = shade-anchor pads, paired shade-targets, walls.
   Different.
6. *Visual signature*: tn36 = densely-decorated bottom-region
   programme tray + central runway; bw7k = open arena + small
   tape strip on the edge. Different.
7. *Pixel grain*: comparable richness, both have rich glyph
   sprites. Borderline shared.
8. *Core dynamic*: tn36 = "explicitly programme then run"; bw7k =
   "walk live, your past trajectory drives a companion". 
   Different.
Score: 1-2 dims shared (kills, possibly pixel grain). PASS.

Comparison vs **m0r0** (closest in "two-pawn coupled motion"):
1. *On board*: m0r0 = orbs + mazes + spike hazards + post-stones;
   bw7k = actor + shades + anchors + targets + walls. Different
   roster.
2. *Input*: arrows + click in m0r0; arrows-only in bw7k.
   Slightly different.
3. *Asks*: m0r0 = pair-orbs-into-same-cell; bw7k = each-pawn-on-
   its-own-target. Different.
4. *Kills*: step counter both. Shared.
5. *Cast*: m0r0 spike hazards + post-stones; bw7k anchors +
   targets + walls. Different.
6. *Visual*: m0r0 = dyed background overlay with 2-strip palette;
   bw7k = neutral background + tape-strip widget. Different.
7. *Pixel grain*: comparable.
8. *Core dynamic*: m0r0 = "control two orbs simultaneously by
   reflection"; bw7k = "control one actor; companion replays
   recent input from a different start". Different.
Score: 1-2 dims shared. PASS.

Comparison vs **zk9p** (autonomous-NPC walk):
1-3 differ; 4 shared (kills); 5 differs (zk9p has pursuers, bw7k
shades); 6-7 comparable; 8 *very* different ("avoid pursuers" vs
"route companion via replay"). 1-2 dims shared. PASS.

Comparison vs **jd4q** (named "echo"):
1. *On board*: jd4q = avatar + maze + echo-trail-cells + closing-
   doors + eraser-cell; bw7k = actor + shades (moving entities) +
   anchors + targets + walls. Different rosters.
2. *Input*: jd4q arrows + click (teleport-back); bw7k arrows-only.
   Different.
3. *Asks*: jd4q = navigate maze with branch ordering shaped by
   doors; bw7k = deliver actor + shades to targets. Different.
4. *Kills*: step counter both. Shared.
5. *Cast*: jd4q = echo-trail + doors + eraser-cell; bw7k =
   anchors + targets + walls. Different.
6. *Visual*: jd4q = trail of fading cells in the wake; bw7k =
   tape strip on edge + actor + shade pawns. Different.
7. *Pixel grain*: comparable.
8. *Core dynamic*: jd4q = "maze with breadcrumbs you can teleport
   onto"; bw7k = "your past walking drives an autonomous twin".
   Different.
Score: 1-2 dims shared. PASS.

Comparison vs **vp6h** (named "shadow"):
The "shadow" lexical overlap is incidental — vp6h's shadows are
illumination-zones, bw7k's shades are moving entities. All eight
dimensions differ. Score: 1 dim shared (kills). PASS.

Comparison vs **ek73** (named "wake"):
1. *On board*: ek73 = avatar + walked-trail-becoming-hazard +
   clearer-pads + warp-pads; bw7k = actor + shades + anchors +
   targets + walls. Different.
2. *Input*: arrow-walk both. Shared.
3. *Asks*: ek73 = navigate without entering own wake; bw7k =
   deliver companions to targets. Different.
4. *Kills*: ek73 = step-into-wake hazard + step counter; bw7k =
   step counter only. Slightly different.
5. *Cast*: ek73 wake hazards + clearer-pads + warp-pads; bw7k
   anchors + targets. Different.
6. *Visual*: ek73 = decaying wake cells in distinctive palette;
   bw7k = small tape widget + ghost-shade pawns. Different.
7. *Pixel grain*: comparable.
8. *Core dynamic*: ek73 = "your past path is a hazard for you";
   bw7k = "your past path is a companion's instructions". Sign-
   inverted dynamic. Different.
Score: 2 dims shared (input, pixel grain). PASS.

No single prior shares 3+ dimensions. The negative similarity
check passes — bw7k is sufficiently divergent in surface
signature from every close-named prior.

## Verdict

**NOVEL.** Mechanic family `actor-replay-shade` does not appear in
the taxonomy of the 25 reference games or in the 60-entry
`prior-games/index.md`. Closest near-misses (tn36, m0r0, zk9p,
jd4q, vp6h, ek73) each have concrete distinguishing rules
articulated above and pass the negative-similarity surface-
overlap test.

Proceed to `write_spec` with `bw7k` and family
`actor-replay-shade`.
