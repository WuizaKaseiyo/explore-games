# Game generation final report

## Generated game
- **ID**: qm4t
- **Source**: `prior-games/qm4t/qm4t.py`
- **Metadata**: `prior-games/qm4t/metadata.json`
- **Lines of code**: 514

## Mechanic
The player drops markers (vertex posts) on the playfield by clicking
empty cells; the engine renders the convex hull of all currently-placed
markers as an outlined fence with a faint inside-tint. Pressing the
commit verb (ACTION5) consumes every coloured creature whose centre
lies strictly inside the fence — matching-colour critters tick off
per-colour tally chips, while non-matching critters and patrollers
each rack up one strike. Three strikes (or running out of step budget)
ends the run; clearing every tally chip wins the level. The three
levels escalate from a free-shape tutorial enclosing a single colour,
through a corner-decoy band that forces tight pen sizing, into a
final composition where mobile patrollers cycle through the playfield
and the player must time the commit so that the patrollers are at
phase-cells outside the chosen pen.

## Action mapping

| Action | Effect |
|---|---|
| ACTION5 | Commit the pen — capture every critter / patroller whose centre is strictly inside the convex hull of currently-placed posts; non-matching captures cost 1 strike each; on commit, all posts are cleared. |
| ACTION6 | Click — if the click cell is empty, place a vertex_post there (capped at 8 posts); if it hits an existing post, remove that post; otherwise no-op. |

## Levels

- **L1.** 3 green critters scattered. Tutorial: place a 3-vertex
  triangle around them and commit. Tally clears, advance.
- **L2.** Adds 4 maroon critters at the playfield corners as
  forbidden decoys. Witness must place a small triangle around the
  centre cluster of greens, leaving every maroon outside.
- **L3.** Adds 2 yellow critters (also targets), 1 maroon along the
  mid-band, and 3 patrollers on a synced 8-step cycle. Patrollers
  spend phases 0..3 at centre cells (inside any reasonable pen) and
  phases 4..7 at the four corners (outside). Witness places 4
  rectangle vertices, advancing the action count to phase 4, then
  commits — capturing all 5 required critters with no strikes.

## Novelty note
- **Closest taxonomy entry**: `su15` (radial-blast-capture). Distinguishing
  rule: su15's capture region is a fixed-radius disk centred on a single
  click; qm4t's capture region is a player-defined convex polygon
  built across multiple clicks.
- **Closest prior-games entry**: `gv47` (seed-grow-surround-dissolve).
  Distinguishing rule: gv47's "surround" emerges from a cellular-
  automaton-style growth of paint regions plus contact chemistry on
  ACTION5; qm4t's "surround" is a static-geometry convex-hull
  inside-test with no time evolution between commits and no
  chemistry. The negative-similarity walk against gv47 yields 2
  shared dimensions (click+ACTION5 verb skeleton, step-counter lose
  mode), well below the 3-dimension reject threshold.

## Index update
One row appended to `prior-games/index.md`:

```
| qm4t | convex-pen-trap | Convex Pen Trap — click cells to drop vertex-posts whose convex hull defines a pen; ACTION5 commits and captures every critter strictly inside, scored against per-colour tally chips (forbidden critters and patrollers strike). | 2026-05-08T00:00:57Z | (autonomous) |
```
