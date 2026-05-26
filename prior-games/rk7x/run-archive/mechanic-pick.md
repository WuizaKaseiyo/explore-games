# mechanic-pick.md

## Run input
- Seed: (autonomous) — no user-supplied seed.

## Chosen 4-character ID
- **`rk7x`**
- Verification: not in the 25-game reserved list; not in `prior-games/index.md` (16 priors). Lowercase alphanumeric, opaque, not an English word.

## Mechanic family tag
`live-switch-routing`

## One-paragraph description
A small coloured **courier** sprite walks the board autonomously along a fixed
cardinal direction at exactly one cell per player action; the courier never
takes input. The board is a network of one-cell-wide corridors carved into a
solid wall block; corridors meet at **junction cells** that hold a clickable
**switch** sprite. A switch has a small visible "blade" pointing one of two
directions (the two cardinal exits other than the one the courier is arriving
on). When the courier enters a junction, the switch's current blade direction
decides which exit it takes; the switch never blocks the courier (every
junction has exactly two outgoing exits). The player's verb is to **click any
switch on the board** during the gap between courier ticks: that toggles the
clicked switch's blade between its two valid orientations. The courier must
visit every coloured **stop** (a 1-cell coloured marker) along the corridor
network and reach the **terminal** (a target cell whose colour matches the
courier's hue) before the per-level action budget runs out. The interesting
puzzle is that the player and the courier alternate: each player click ticks
the courier one cell, so the player has only N actions to reposition all
upcoming switches before the courier reaches them, AND every click counts as
a tick (no free clicks).

## Per-level mechanic plan (informational; finalised in `write_spec`)
- **L1 — base dynamic system.** Courier auto-walks; clicking a switch toggles
  it; clicking on empty space ticks the courier without changing routing
  (this is the "wait" verb). Witness must (a) tick at least once and
  (b) toggle at least one switch — a corridor that is solvable without ever
  toggling a switch is rejected. A single stop and the terminal share a
  colour; the player must route the courier across one switched fork to
  visit both.
- **L2 — adds two mechanics.** (i) **Coloured stops** that must be visited
  in colour order — out-of-order visit consumes the stop without scoring it;
  (ii) **One-shot dead-end branches** that the courier enters but cannot
  exit (the switch at the dead-end mouth shuts behind it after entry) — so
  the player must time switch-toggles so the courier never enters a
  dead-end while a stop is still required.
- **L3 — adds two mechanics.** (iii) **Two simultaneous couriers** of
  different colour, walking in different starting directions, ticked
  together by every player action — the player must interleave switch
  toggles for both. (iv) **Conflict cells**: two couriers may not occupy
  the same cell on the same tick (collision = lose), so the routing must
  also respect a temporal-disjointness constraint.

L1 mechanics required by witness = 1 (live switch routing).
L2 = L1 + 2 = 3 (live switch routing + colour-order stops + dead-end branches).
L3 = L2 + 2 = 5 (above + dual couriers + conflict cells).

This satisfies the +1-or-+2 rule across L1→L2 and L2→L3.

## Core-knowledge prior categories used
- **Objectness**: courier, switches, stops, walls, terminals are persistent
  entities.
- **Basic geometry & topology**: corridor network = graph; switch = local
  topology editor (which edge is "active" at a junction); the player is
  steering the courier through the graph by editing edges.
- **Agentness**: the courier acts with intent (it walks deterministically).
  In L3, two agents act independently in lockstep.

No use of physics or symbolic glyphs.

## Positive similarity check (per `mechanic-novelty/similarity-check.md`)

Walked the candidate against every entry in `taxonomy-of-25-games.md` and
every entry in `prior-games/index.md`. Family-level matches escalated to
description-level; for taxonomy near-misses I re-read the corresponding
`mechanism-details/<id>.md`.

### Near-misses identified

| Source | Entry | Family-level match? | Description-level match? | Distinguishing rule |
|---|---|---|---|---|
| taxonomy | `tn36` (program-pawn-trace) | yes (program/route) | partial | tn36's loop is **compose program first, then run**: ACTION6 clicks build a tape of move/rotate/resize ops; the pawn reacts only after the player has committed the program. `rk7x`'s loop is **edit-during-execution**: every player click ticks the courier one cell, so the player is reading the courier's *current* graph position and adjusting the very next switch. There is no commit verb; the program is the trajectory of the live courier as it traverses the network. |
| taxonomy | `bp35` (gravity-fall-navigation) | yes (auto-mover with player input each tick) | partial | bp35 player **is** the auto-mover (player IS the falling pawn; side-step lets them move it left/right). `rk7x`'s player is NOT the courier — they edit the environment from a distance. The verb cardinality differs: bp35 acts on the avatar's column; `rk7x` acts on a global-position switch sprite. Also bp35 is single-axis (gravity); `rk7x`'s courier turns at every junction. |
| taxonomy | `sp80` (pour-shelf-route) | partial (route a flow through a board) | no | sp80 is a placement phase (move pipe pieces) followed by a commit phase (ACTION5 spawns liquid that runs to completion). `rk7x` has no placement/commit phases; the courier walks every action and the player edits each tick. sp80's mover is a fluid (multi-cell broadcast); `rk7x`'s mover is a single 1-cell agent at known position. |
| taxonomy | `vn8d` (domino-cascade-topple) | partial (single edit kicks off automatic propagation) | no | vn8d kicks off **a single chain reaction with one click** that propagates without further input until completion. `rk7x` has no chain reaction; one tick = one cell of courier travel, one player click. The player must intervene every tick. |
| taxonomy | `bx84` (beam-mirror-reflect, prior) | partial (route a thing through reflectors) | no | bx84 fires a beam from a fixed emitter; mirrors are placed on empty cells (not toggled in place). `rk7x`'s courier is a persistent moving agent that occupies a cell, not a beam. Switches are pre-placed at fixed junction positions and only their orientation is edited. |
| prior | `vn8d` (already addressed above) | — | — | — |
| prior | `bx84` (already addressed above) | — | — | — |
| prior | `pj7k` (rolling-cube-face-paint) | partial (an auto-mover deposits something each cell) | no | pj7k's cube rolls only when the player presses an arrow; the rolling permutes its faces and stamps the bottom face's colour. `rk7x`'s courier walks every action regardless of click target (clicking switches OR empty space both tick the courier), and there is no face-permutation — the courier's identity is fixed. |
| prior | `kn58` (anchor-pull-magnet) | partial (click → environment moves passive object) | no | kn58 has *one* anchor at a time and pawns step toward it along the dominant Manhattan axis. `rk7x` has many fixed switches; clicking a switch does not move the courier directly — it only changes which exit the courier will take when it next enters that switch. The "movement causation" is decoupled (and delayed) from the click. |
| prior | `wt39` (glide-deflect-thaw) | partial (auto-mover bounces off bumpers) | no | wt39's player presses a direction → the pawn glides in that direction until a wall (one launch = many cells in a single action). `rk7x`'s courier moves exactly one cell per action and does not respond to direction keys at all. Also wt39's bumpers always deflect the *same* way; `rk7x`'s switches are toggled per-junction and are the only routing primitive. |
| prior | `kf42`, `qz73`, `kx14`, `qb84`, `lq5x`, `gv47`, `hr8q`, `ng52`, `pz4t`, `fz5j`, `zk9p` | no family-level match | — | None of these involve an autonomous agent traversing a corridor network whose junctions are edited mid-traversal. |

No flagged row produced a "yes/yes/none" verdict. The candidate's
distinguishing rule against each near-miss is concrete, naming the rule (no
commit phase, no avatar-input, single-cell-per-tick, junction-edge-edit
verb). Verdict: **NOVEL** under the positive check.

## Negative similarity check (per `mechanic-novelty/negative-similarity-check.md`)

I mentally rendered L1 — small (12×12) walled grid with corridors carved
through a solid wall block; one courier (a 2-pixel coloured arrow), one
switch sprite at the single junction (with a visible "blade" indicator),
one coloured stop, one terminal in matching colour, plus the universal
step-counter HUD — and walked the eight dimensions in
`negative-similarity-check.md` against every relevant prior and taxonomy
near-miss whose `level_1.png` I opened during `study`.

For each prior/taxonomy entry, I count shared dimensions:

| Prior / ref | Shared dimensions (1-8) | Count | Verdict |
|---|---|---|---|
| `bp35` (gravity-fall-navigation) | 4 (kill-by-step-budget) — and arguably 8 partial (auto-mover with player tick) | 1.5 | clean |
| `tn36` (program-pawn-trace) | 4 (kill-by-budget), 1 (a board with auto-mover sprite) | 2 | clean |
| `bx84` (prior, beam-mirror-reflect) | 1 (board has a propagating thing), 4 (kill-by-budget) | 2 | clean |
| `vn8d` (prior, domino-cascade-topple) | 1 (board with chain-thing), 4 (kill-by-budget) | 2 | clean |
| `kn58` (prior, anchor-pull-magnet) | 1 (board with passive entities affected by clicks), 4 (kill-by-budget) | 2 | clean |
| `wt39` (prior, glide-deflect-thaw) | 1 (board with bouncing entity), 4 (kill-by-budget) | 2 | clean |
| `pj7k` (prior, rolling-cube-face-paint) | 4 (kill-by-budget), 2 (player-presses-direction-on-mover, partial) | 1.5 | clean |
| `tu93` (lockstep-multi-maze) | 1 (multi-agent grid), 4 (kill-by-budget) | 2 | clean (matters for L3 with dual couriers, see below) |

No prior shares 3+ dimensions with the L1 mental render. Visual signature
(dimension 6) is distinct from every prior — `rk7x`'s L1 is a corridor maze
carved into a solid block with a single visible junction blade, which none
of the priors render. Pixel grain (dimension 7) of the courier (a 2-pixel
arrow with internal direction-tip) and the switch (a junction box with a
visible blade-direction "tongue") have internal pixel structure rather
than being plain n×n rectangles. Core dynamic (dimension 8) — "edit a
junction's outgoing-edge while an autonomous agent walks it" — does not
appear in any prior.

**L3 dual-courier check vs. tu93.** With two couriers in L3, the visual
signature could drift toward tu93's multi-agent grid. Difference: tu93's
agents move *together in response to player arrows* (lockstep arrow
input); `rk7x`'s couriers move *autonomously every action regardless of
what the player does*. The verb is fundamentally different (no
multi-agent input); the resemblance is at the visual-cast level only and
both games rendered side-by-side would not feel like the same game.

**Palette plan to ensure dimension-6 divergence.** The chosen palette
will avoid the `{4 wall, 8 red, 9 blue}` trap. Primary roles: walls = 5
(black) framing solid corridors, courier = 11 (yellow) with a 12 (orange)
tip, switches = 14 (green) with a 6 (magenta) blade, stops = 10 (light
blue), terminal = 15 (purple). HUD step-counter = 3 (grey) on row 63.
This palette signature is not used by any of the 16 priors per their
mechanism descriptions or the level_1.png I opened.

Verdict: **NOVEL** under the negative check. No prior shares 3+ surface
dimensions; visual signature, pixel grain, and core dynamic all diverge.

## Final verdict

`rk7x` (live-switch-routing) is novel against the 25-game reference
taxonomy and the 16-game prior corpus by both positive and negative
similarity tests. Proceed to `write_spec`.
