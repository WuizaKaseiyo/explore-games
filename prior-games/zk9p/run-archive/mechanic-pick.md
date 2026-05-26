# Mechanic pick — zk9p

## Game ID
`zk9p`

Verified non-colliding:
- Not in the 25 reference IDs (ar25 bp35 cd82 cn04 dc22 ft09 g50t ka59 lf52 lp85 ls20 m0r0 r11l re86 s5i5 sb26 sc25 sk48 sp80 su15 tn36 tr87 tu93 vc33 wa30).
- Not in `prior-games/index.md` (kf42 qz73 kx14 qb84 lq5x gv47 hr8q ng52 pj7k pz4t vn8d fz5j kn58 bx84 wt39).
- 4 lowercase alphanumeric chars; not an English word.

## Mechanic family
`pursuer-merge-walk`

## One-paragraph description

The player walks a single avatar around a small wall-bounded arena
inhabited by 2-4 deterministic AI "pursuer" pawns of distinct colours.
Each pursuer moves one cell per turn under its own per-type chase rule
(e.g. step toward the player along the larger Manhattan axis; step
toward the player on whichever axis the player just moved). When two
or more pursuers land on the same cell on the same tick, they all
merge and disappear. A pursuer landing on the avatar's cell ends the
level (lose). The level is won when every pursuer has been eliminated
through induced collisions before the step counter expires. The
player's tactical lever is timing: walking such that two pursuers'
deterministic next-tick targets are the same cell, then stepping away
so the pursuers overshoot into one another. Core priors used:
**agentness** (pursuers are NPCs that act with intent toward the
player), **objectness** (pursuers and avatar are persistent
positionable entities), **basic geometry** (Manhattan-axis
discrimination determines which pursuer moves which way).

## Per-level outline

- **L1** (tutorial, base dynamic system): one avatar + 2 pursuers with
  one shared chase rule (Manhattan-axis-major step-toward), no walls,
  small grid (12×12). Witness exercises avatar-walk + pursuer-chase +
  merge-on-collision.
- **L2**: introduces walls (block both avatar and pursuer chase paths
  via BFS) AND a second pursuer type (orthogonal-axis chaser). 3
  pursuers total. Witness exercises L1 mechanics + wall-routing +
  second-chase-type discrimination.
- **L3**: introduces a "phase pursuer" that's intangible to the avatar
  on alternate ticks (so the avatar can pass through it on every
  second tick) AND ACTION5 "tick-skip" — a free no-move action that
  costs 2 step-counter units but advances every pursuer by one tick
  while the avatar holds position. 4 pursuers total. Witness exercises
  every L1+L2 mechanic plus phase-timing plus tick-skip composition.

## Action subset
`[1, 2, 3, 4, 5]` — UDLR for avatar walk; ACTION5 for tick-skip
(introduced in L3 but declared from L1, gated to no-op when not L3).

(Per `action-enum.md`: ACTION5 carries the distinctive verb. Tick-skip
makes the verb genuinely free-slot rather than no-op.)

## Similarity check (against 25-game taxonomy)

Family-level match: the candidate's `pursuer-merge-walk` tag shares
the "merge" suffix with **m0r0** (`mirror-orb-merge`) and shares
"chase" / pursuit theme with **ka59** (`sokoban-explode-chase`),
**g50t** (`walk-vs-scroll`), **m0r0**, **su15**
(`recipe-fruit-collect`), **tu93** (`maze-pickup-train`), **wa30**
(`lock-drag-crate`). Description-level checks for each:

- **m0r0** — merges *player avatars* (4 of them) via axis-flipped
  lockstep movement; my candidate merges *enemies* induced by player
  bait. The verb (lockstep multi-avatar drive vs single-avatar walk),
  the merge subject (player vs NPC), and the win condition (all four
  player avatars paired vs all enemies eliminated) all differ.
  **Distinguishing rule:** in m0r0 the player physically embodies the
  things being merged; in zk9p the player is the bait luring others to
  merge.
- **ka59** — has one chaser as a hazard, but the core mechanic is
  click-select-then-slide blocks + explode-tiles + cover targets. The
  chaser ends the game on contact but is not the win condition. My
  candidate's chasers ARE the win condition (eliminate them).
  **Distinguishing rule:** ka59's chaser is a hazard; zk9p's pursuers
  are the puzzle pieces.
- **g50t** — NPCs are ghost replays of the player's prior commits,
  not autonomous pursuers; win is achieved by covering targets via
  union of ghost paths. **Distinguishing rule:** g50t has no live AI
  pursuit — its "agents" are deterministic playback of past actions;
  zk9p has live agents that compute a fresh chase target each tick
  based on the avatar's current cell.
- **su15** — click-detonates a radial blast that sucks fruits in;
  enemies engulfed in the blast cost a strike. The verb is click-blast
  not walk; the agents are passive fruits not active pursuers; the
  enemies are a fail condition not the win. **Distinguishing rule:**
  su15's agency is click-blast-vacuum; zk9p's is walk-bait.
- **tu93** — multiple primary avatars move in lockstep on a walkable
  underlay to exit cells; secondary species (vllvfeggte / zzuxulcort /
  natiyqayts) are hazards or blockers, not merge-targets. **Distin-
  guishing rule:** tu93's win is route-all-primaries-to-exits; zk9p's
  win is induce-pursuers-to-merge.
- **wa30** — single carrier walks and uses ACTION5 to pick up /
  deliver passengers. NPCs are passengers that auto-walk via BFS
  toward destinations, cooperating with the player. **Distinguishing
  rule:** wa30's NPCs cooperate (they want to reach destinations);
  zk9p's NPCs antagonise (they pursue the avatar); the verb in wa30 is
  carry-and-deliver while zk9p's is bait-and-collide.

No reference game uses pursuer-into-pursuer-collision-merge as a
primary mechanic. NOVEL.

## Similarity check (against `prior-games/index.md`)

Walking each prior:

- **kf42** (tether-pawn-cycle) — two-pawn max-distance tether; click
  selects, arrows step. No pursuit, no merge. Distinguishing: my
  candidate's enemies move autonomously per-tick; kf42's pawns are
  player-controlled.
- **qz73** (radial-cycle-lock) — central rotor of coloured tips +
  per-tip click-locks. No pursuit, no NPCs.
- **kx14** (tide-tilt-buoyant) — water surface raise/lower + ball tilt
  + anchor click. No pursuit.
- **qb84** (bead-lift-swap) — pure-arrow chain navigation; lift/drop
  swaps active bead's colour. No pursuit.
- **lq5x** (lantern-cone-illuminate) — single lantern projects
  directional cone. No pursuit.
- **gv47** (seed-grow-surround-dissolve) — click coloured seeds to
  grow regions; ACTION5 mixes contacting region pairs. No pursuit.
- **hr8q** (pair-blend-recipe) — click two ingredients to fill formula
  widget; commit consumes / distils. No pursuit.
- **ng52** (multiset-signature-classify) — partition objects into bins
  whose stick signatures define multiset. No NPCs.
- **pj7k** (rolling-cube-face-paint) — single cube rolls; faces
  permute and deposit colour. No pursuit.
- **pz4t** (anchor-pivot-place) — tile a connected region with
  components; clicked-pixel sets anchor; arrows reflect; ACTION5
  rotates. No pursuit.
- **vn8d** (domino-cascade-topple) — single click triggers chain
  reaction through pillars. No pursuit (cascade is deterministic
  one-shot, not per-tick AI).
- **fz5j** (phase-step-tile) — avatar walks tiles that pulse open /
  closed on per-cell periods; entering a closed tile costs a life. No
  pursuit (tiles are passive obstacles).
- **kn58** (anchor-pull-magnet) — click any cell to place a magnetic
  anchor; every coloured pawn slides one cell toward it.
  **Closest comparison.** Both have "multi-agent slide per signal",
  but kn58's pawns are passive (they only move when clicked) and slide
  toward the click, not toward the avatar; there is no avatar in kn58.
  My candidate's pursuers are active each tick and chase the avatar.
  Distinguishing rule: kn58 is signal-driven simultaneous slide of
  passive objects toward a click point; zk9p is autonomous per-tick
  pursuit of the avatar by AI agents.
- **bx84** (beam-mirror-reflect) — beam + mirrors + filters. No
  pursuit.
- **wt39** (glide-deflect-thaw) — pawn glides until wall; bumpers
  deflect 90°. Glide ≠ pursuit; the pawn is the player.

NOVEL on every prior; no flagged near-misses requiring concrete
distinguishing rules beyond kn58 (covered above).

## Negative similarity check (against close priors and references)

Walking the eight dimensions of `negative-similarity-check.md`. The
two priors most likely to share dimensions are **kn58** (multi-agent
slide on click) and **kf42** (multi-pawn click-and-arrow). The two
references most likely to share are **ka59** (chaser hazard) and
**tu93** (multi-NPC species).

vs **kn58**:
1. Board: kn58 = orange pawns + targets on grey field; zk9p = avatar +
   enemies + walls on slate. **Different** (avatar is unique to zk9p;
   walls absent from kn58 L1).
2. Input: kn58 = click only; zk9p = walk + tick-skip. **Different.**
3. Level ask: kn58 = cover targets; zk9p = eliminate pursuers.
   **Different.**
4. What kills: kn58 = step counter only; zk9p = step counter +
   pursuer-on-avatar. **Different.**
5. Supporting cast: kn58 = pawns + targets; zk9p = avatar + pursuers +
   walls + (L3) phase-pursuer. **Different.**
6. Visible signature: kn58 = orange + grey; zk9p will use a slate
   floor (palette 4) + magenta avatar (palette 6) + distinct enemy
   hues (yellow 11, green 14, blue 9, red 8). **Different.**
7. Pixel grain: kn58 pawns are flat 2×2 with a single nub; zk9p
   pursuers will be 3×3 with internal-centre detail and avatar will be
   3×3 with two-tone pattern. **Different.**
8. Core dynamic: kn58 = anchor-pull passive sliding; zk9p = autonomous
   pursuit lured into self-collision. **Different.**

Shared dimensions: 0. Safe.

vs **ka59**:
1. Board: ka59 = movable blocks + chaser + walls + targets; zk9p =
   avatar + pursuers + walls. **Partially overlap (walls).**
2. Input: ka59 = click+arrow; zk9p = arrow+ACTION5. **Different.**
3. Level ask: ka59 = cover targets; zk9p = eliminate pursuers.
   **Different.**
4. Kills: ka59 = step counter + chaser-catch; zk9p = step counter +
   pursuer-catch. **Shared.**
5. Supporting cast: ka59 = blocks + targets + chaser + explode-tiles;
   zk9p = avatar + pursuers + walls. **Different.**
6. Visible signature: ka59 = grey field with red/blue blocks + black
   chaser; zk9p = slate field with magenta avatar + multi-coloured
   pursuers. Different palette signature.
7. Pixel grain: ka59 blocks are 2×2-flat-with-stripe; pursuers will be
   3×3 with centre detail. **Different.**
8. Core dynamic: ka59 = sokoban + explode + dodge; zk9p = bait-and-
   collide. **Different.**

Shared dimensions: 2 (walls, "caught = lose"). Below the 3-dim
threshold. Safe.

vs **tu93**:
1. Board: tu93 = walkable underlay + multiple primary avatars +
   exit cells + secondary species; zk9p = arena + single avatar +
   pursuers + walls. **Different.**
2. Input: both arrow-only at L1, but zk9p adds ACTION5 in L3.
   **Partially shared.**
3. Level ask: tu93 = route-all-to-exits; zk9p = eliminate-all-pursuers.
   **Different.**
4. Kills: both step counter + collision-with-enemy. **Shared.**
5. Supporting cast: tu93 has 3 secondary species + walkable underlay
   tile sprite; zk9p has wall sprites + (L3) phase-pursuer.
   **Different.**
6. Visible signature: tu93 uses grey value-2 walkable corridors with
   black non-walkable; zk9p uses solid slate floor with no underlay
   structure (walls are obstacle sprites placed on top). **Different.**
7. Pixel grain: tu93's avatars are 3×3 with a top notch; pursuers will
   be 3×3 with centre detail. **Borderline shared form (3×3 grain).**
8. Core dynamic: tu93 = lockstep route + species-tick; zk9p = lure-
   pursuit-merge. **Different.**

Shared dimensions: 2 (input partial, kills, possibly grain). Below the
3-dim threshold. Safe.

vs **g50t**:
1-8. g50t's "agents" are ghost replays of the player's past commits,
not autonomous AI; the visual signature uses a scrolling timer
sprite that has no analogue in zk9p; goal differs (cover targets vs
eliminate pursuers); palette differs. Shared: 0-1 dimensions. Safe.

## Verdict

NOVEL on both axes (taxonomy and prior corpus). The mechanic family
introduces a substantively new core dynamic — **lure autonomous
pursuers into self-collision** — that does not appear anywhere in the
25 reference games or the 15 prior generated games. Pursuit-with-merge
opens an under-explored corner of the agentness prior. Proceed to
`write_spec`.
