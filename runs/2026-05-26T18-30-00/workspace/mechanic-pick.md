# Mechanic pick

## 4-character ID
`hd7r` — verified non-colliding against the 25 reserved reference IDs,
against every row of `prior-games/index.md`, AND against every actual
`prior-games/*/` directory (the index is known-incomplete). Opaque,
not an English word.

## Mechanic-family tag
`repulsion-herd-funnel`

## Seed
(autonomous) — no seed provided; family chosen by the agent.

## One-paragraph description
The player controls a single **shepherd** avatar that walks one cell per
arrow press. Scattered on the field are autonomous **timid creatures**
that, after every shepherd move, take exactly one deterministic step
**directly away** from the shepherd along their dominant Manhattan axis
(a flee rule), but only when the shepherd is within a fixed "scare
radius"; outside that radius a creature stays put. Creatures cannot
walk through walls or off the field — a creature pinned against a wall
with the shepherd bearing down simply cannot move that tick. The win
condition is **spatial**: drive every creature onto (or into) its
matching **pen** cell. Because the shepherd repels rather than carries,
the player must think about *where to stand so the flee-vector points
the creature where it needs to go* — approaching from the far side,
using walls and corners as backstops, and funnelling creatures through
gaps. Core knowledge priors used: **agentness** (creatures act with
intent — they flee), **objectness** (shepherd, creatures, walls, pens
are persistent collidable entities), and **basic geometry/topology**
(funnels, corners, gaps as the levers of control).

## Core-knowledge-prior compliance
Draws ONLY from the four allowed categories: agentness (flee rule),
objectness (entities), basic geometry/topology (funnel geometry). No
acquired/symbolic/cultural knowledge. No digits, letters, clipart, or
cultural colour conventions in any sprite (creatures are abstract
round-bodied sprites with two eye pixels; pens are hollow bordered
frames; the shepherd is a distinct chunky avatar).

## Multi-mechanic plan (preview; full detail in spec §4)
- **M1 (L1, base):** flee-step — after every shepherd move each creature
  within scare radius steps one cell directly away; win = every creature
  on its pen.
- **M2 (L2, +1):** **gate posts** the shepherd can toggle (a click verb)
  open/closed to change which gaps a creature can be funnelled through —
  a creature cannot flee through a closed gate.
- **M3 (L3, +1):** **two creature temperaments** — a second creature
  type that flees *perpendicular* (it sidesteps clockwise away rather
  than straight back), so the player must steer two different flee-laws
  through the same gated geometry simultaneously.

## Novelty analysis

### Positive similarity check (similarity-check.md)
Closest taxonomy near-misses and the concrete distinguishing rule:

- **ka59 (sokoban-explode-chase):** ka59 has a *chaser that moves toward*
  the active pawn and pawns the player *pushes*. hd7r's creatures move
  *away* from the player and are never pushed/carried — the player never
  occupies or shoves a creature's cell; control is purely by repulsion
  field. Win in ka59 is "cover target squares with pawns you push";
  hd7r is "creatures flee onto pens you can never push them onto."
  Different primary verb (repel-at-distance vs push-on-contact),
  different agent intent (flee vs chase).
- **g50t / tu93 / m0r0 / su15 / wa30 (the agentness reference set):**
  every one of these has NPCs that either chase the player, patrol
  fixed waypoints, or compete for objects. None has an NPC whose policy
  is "flee from the player," and none makes the player's *body position*
  the control surface for steering an autonomous agent's destination.

Closest prior-games near-misses (scanned ALL `prior-games/*/`
mechanism-detail.md, not just index.md) and the distinguishing rule:

- **zk9p (pursuer-merge-walk):** pursuers move TOWARD the avatar and the
  win is self-collision/merge. hd7r creatures move AWAY and the win is
  positional (creature on pen); there is no merge and no lure. Inverted
  agent policy + inverted goal.
- **mw8p (predator-prey-triangle):** a rock-paper-scissors of chasing
  species; the player's creature is prey/predator in a chase web and
  the win is "reach the exit." hd7r has no chase web — creatures only
  react to the shepherd's proximity, and the player's win is to place
  the creatures, not to escape.
- **gg26 (sheep-pasture-fence):** the "sheep" is STATIC and the player
  builds fences (clicks) to enclose grass region area; flood-fill of a
  region is the predicate. hd7r creatures MOVE (flee) every tick and the
  win is each creature on a discrete pen cell, not a region-area
  flood-fill; the shepherd's body, not placed fences, is the lever.
- **rk7x / gg25 (live courier / docking patrols):** autonomous actors
  walk authored paths and the player toggles routing/holds; the actor
  ignores the player's position. hd7r's creatures have no path — their
  motion is *defined by* the shepherd's relative position every tick.

### Negative similarity check (negative-similarity-check.md) — seven dimensions
Walked against the closest priors (zk9p, mw8p, gg26, ka59). Counting a
dimension shared only when "essentially the same":

| Dim | hd7r | zk9p | mw8p | gg26 | ka59 |
|---|---|---|---|---|---|
| 1 board | shepherd + fleeing creatures + pens + walls | avatar + pursuers + walls | creature + chasers + exit | static sheep + fences + grass | pawns + targets + chaser + explode-tiles |
| 2 input | walk avatar (arrows) [+click gate L2] | walk avatar | walk creature | click to place fence | click-switch-active + walk |
| 3 asking | each creature on its pen | no pursuers remain | reach exit | enclose grass region of target area | cover target squares |
| 4 kills | step budget (+ no hard death) | pursuer touches you | chaser touches you | retry/fence budget | step budget |
| 5 cast | timid fleeing creatures + pens | merging pursuers | predator/prey species | sheep + water/stone | explode-tiles + chaser |
| 6 palette | shepherd teal, creature warm + eyes, pen ring, wall slate — distinct signature | magenta avatar set | A/B/C tri-species | green grass set | grey pawns set |
| 7 grain | round-body creatures w/ eyes, hollow pen rings, patterned walls | small blocks | spiky/leafy sprites | sheep + tiles | plain blocks |
| 8 core dynamic | **repel-at-distance to STEER an autonomous flee-vector onto a goal cell** | lure pursuers into mutual collision | survive a chase web | flood-fill enclosure | push-Sokoban + dodge |

Shared-dimension count with each prior:
- vs **zk9p**: dim 2 (walk an avatar) only → 1. (Goal, agent-policy,
  cast, core dynamic all differ.) Below threshold.
- vs **mw8p**: dim 2 (walk an avatar) only → 1. Below threshold.
- vs **gg26**: dim 1-partial (some shared "creature + pen-ish goal")
  but input (walk vs click), motion (flee vs static), and predicate
  (cell-occupancy vs region-flood-fill) all differ → ≤ 1 strong. Below
  threshold.
- vs **ka59**: dim 4 (step budget) only → 1. Push vs repel, chase vs
  flee, cover-square vs pen-placement all differ. Below threshold.

No single prior reaches 3 shared dimensions, and the two heavy named
principles — dim 8 (core dynamic) and dim 6/7 (visual signature/grain)
— diverge from every prior. The candidate passes the negative test.

## Exploration contract (exploration-pressure.md)
- **exploration_profile:** `multi-agent-discovery` (the player discovers
  how the autonomous creatures react to the shepherd's relative
  position).
- **discovery_question:** "When I move, what makes the creature move, and
  in which direction?"
- **probe_actions:** (1) step toward a creature from below → it flees up;
  (2) step toward it from the left → it flees right; (3) step far away
  → it does not move (scare-radius boundary); (4) [L2] click a gate post
  → it visibly opens/closes.
- **observable_feedback:** the creature translates one cell directly away
  on probes 1-2, stays put on probe 3, and the gate sprite swaps
  open/closed on probe 4 — all visible in the next frame.
- **mastery_rule:** "A creature within the scare radius steps one cell
  directly away from me along its larger Manhattan axis; outside the
  radius it is still; closed gates block the flee step."
- **anti-randomness:** random walking scatters creatures arbitrarily and
  cannot reliably pin each onto its specific pen; the win demands the
  shepherd be positioned on the *opposite* side of each creature from
  its pen at the right moment — a planned approach, not stumbled into.
