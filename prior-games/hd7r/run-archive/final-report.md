# Game generation final report

## Generated game
- **ID**: hd7r
- **Source**: `prior-games/hd7r/hd7r.py`
- **Metadata**: `prior-games/hd7r/metadata.json`
- **Lines of code**: 452

## Mechanic
The player walks a single shepherd one cell per arrow press on a 16×16
board. Timid creatures react to the shepherd's proximity: after each
move, every creature within a fixed scare-radius takes one deterministic
step *away* — orange creatures back straight away, magenta creatures
veer one cell perpendicular — unless a wall, a shut gate, the edge, or
another creature blocks that step. The player never touches a creature;
control is purely a question of which side to stand on so the flee
points the creature toward its goal. The win is spatial: drive every
creature onto a pen of its own colour. Difficulty composes across the
three levels: L1 teaches the flee law with one creature funneled into a
corner; L2 adds a click-togglable gate in a dividing wall (one creature
must be herded through the opened gate while another is parked on a wall
backstop); L3 adds the perpendicular-flee temperament, so the player
must sidestep-herd a magenta creature to a wall pen, open the gate, and
straight-herd an orange creature across — all three mechanics fired
together. The only failure is a generous depleting energy bar.

## Action mapping
| Action | Effect |
|---|---|
| ACTION1 | Move shepherd UP; in-radius creatures then flee |
| ACTION2 | Move shepherd DOWN; in-radius creatures then flee |
| ACTION3 | Move shepherd LEFT; in-radius creatures then flee |
| ACTION4 | Move shepherd RIGHT; in-radius creatures then flee |
| ACTION6 | Click a gate post to toggle it open/shut (no flee step) |

## Levels
- **L1** — base dynamic (flee-step): one orange creature funneled into a
  corner pen using walls as backstops. Witness 11 actions.
- **L2** — adds gate-toggle: two creatures, a dividing wall with one shut
  gate; one creature must be herded through the opened gate, the other
  parked on a wall-backstop pen. Witness 11 actions.
- **L3** — adds the perpendicular (skittish) temperament: a magenta
  creature sidestep-herded to a west wall pen plus an orange creature
  driven through the gate to an east pen — all three mechanics composed.
  Witness 16 actions.

## Novelty note
- **Closest taxonomy entry**: ka59 (sokoban-explode-chase). Distinguishing
  rule: ka59's NPC chases the player and the player *pushes* pawns onto
  targets; hd7r's NPCs *flee* and are never pushed or contacted — control
  is a repulsion field at a distance, and the win cell is one the shepherd
  can never stand on. (The whole agentness reference set — g50t, tu93,
  m0r0, su15, wa30 — uses chasing/patrolling/competing NPCs, never a
  flee-from-the-player policy.)
- **Closest prior-game entry**: zk9p (pursuer-merge-walk). Distinguishing
  rule: zk9p's pursuers move TOWARD the avatar and win = mutual
  collision/merge; hd7r inverts the policy (creatures flee) and the win
  is positional (each creature on its own pen), with no merge and no
  lure. Also distinct from mw8p (chase-web escape), gg26 (static sheep +
  fence-placement + flood-fill-area), and rk7x/gg25 (path-following
  actors that ignore the player). The negative-similarity seven-dimension
  walk found no single prior sharing ≥3 dimensions, with divergence on
  the heavy axes (core dynamic, visual signature, pixel grain).

## Index update
One row appended to `prior-games/index.md`:

`| hd7r | repulsion-herd-funnel | Shepherd's Repulsion Funnel — walk a shepherd whose proximity makes timid creatures flee; herd each onto its matching pen, using a togglable gate and a perpendicular-flee temperament. | 2026-05-26T13:34:43Z | (autonomous) |`

## Smoke test
All 10 universal checks PASS (incl. CHECK_WITNESS_WINS for all 3 levels
and a dynamic lose-fires check) and all 4 custom checks PASS, on the
first smoke_test visit (1/6). critique_spec visits used: 1/10.
