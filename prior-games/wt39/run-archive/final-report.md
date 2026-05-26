# Game generation final report

## Generated game

- **ID**: wt39
- **Source**: `prior-games/wt39/wt39.py`
- **Metadata**: `prior-games/wt39/metadata.json`
- **Lines of code**: 337

## Mechanic

A single red pawn rests on a tiled ice arena bordered by black
walls. Pressing a cardinal arrow launches the pawn gliding cell-by-
cell in that direction; the slide stops only when the pawn meets a
wall or a cracked thaw-tile. Scattered across the ice in later
levels are angled-bumper deflectors that turn an in-flight slide
ninety degrees, and brittle frozen thaw-tiles that crack after a
single slide passes through them and thereafter act as walls. The
level advances when, after a slide settles, the pawn comes to rest
on the goal cell; the level ends in loss when the per-level step
budget is exhausted. Difficulty composes: L1 teaches the slide rule
on an open arena, L2 forces a bumper deflection because the goal
sits in a region only reachable through one, and L3 demands the
player crack a specific thaw-tile so its newly-formed wall stops a
later slide on the goal.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | UP — pawn glides north until blocked. |
| ACTION2 | DOWN — pawn glides south until blocked. |
| ACTION3 | LEFT — pawn glides west until blocked. |
| ACTION4 | RIGHT — pawn glides east until blocked. |

ACTION5, ACTION6, and ACTION7 are NOT in `available_actions`.

## Levels

- **L1.** Base dynamic system: slide-until-wall. Pawn at (2, 2),
  goal at (8, 7), two interior wall blocks. Witness: `[RIGHT, DOWN]`
  (2 actions). Step budget 30.
- **L2.** Adds **bumper-deflect** (M2). One angled bumper at (10, 2)
  deflects east-going slides southward. The goal at (4, 10) is
  unreachable except via the bumper; column 10 rows 1-6 has no
  other slide-stop. Witness: `[RIGHT (bumper deflect), LEFT, DOWN]`
  (3 actions). Step budget 60.
- **L3.** Adds **thaw-cracking** (M3). One frozen thaw-tile at
  (4, 8) cracks after a slide passes through it; the cracked cell
  thereafter behaves as a wall. The goal at (4, 9) has no adjacent
  slide-stop until the thaw cracks. Witness: `[RIGHT, LEFT, DOWN
  (cracks thaw), UP (stops on goal)]` (4 actions). Step budget 80.

## Novelty note

- **Closest taxonomy entry.** No reference game uses unbounded
  slide-until-wall. The nearest neighbour is **ka59 sokoban-explode-
  chase**, which moves the active pawn one 3-cell push step per
  arrow press; wt39 moves the pawn UNCONDITIONALLY UNTIL collision
  — momentum-based glide rather than push-based step.
- **Closest prior-game entry.** The nearest neighbour is **vn8d
  domino-cascade-topple**, which shares the "single action triggers
  far-reaching motion" surface signature. Distinguishing rule: vn8d
  ignites a deterministic cascade across separate domino objects
  (the player chooses which chain to start); wt39's deflection
  happens to a single moving pawn during a single slide, and the
  player drives the pawn with explicit arrow presses one slide at a
  time. Different agency cardinality (chain of objects vs single
  agent).

## Index update

One row appended to `prior-games/index.md`:

```
| wt39 | glide-deflect-thaw | Glide-Deflect-Thaw — pawn glides in pressed direction until wall; angled bumpers deflect 90°; L2 adds bumpers, L3 adds brittle thaw-tiles that crack after one slide. | 2026-05-05T15:45:03Z | (autonomous) |
```
