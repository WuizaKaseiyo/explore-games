# Game generation final report

## Generated game
- **ID**: tj4n
- **Source**: `prior-games/tj4n/tj4n.py`
- **Metadata**: `prior-games/tj4n/metadata.json`
- **Lines of code**: 460

## Mechanic
A single avatar walks a 16-cell-wide arena leaving a coloured pink trail behind on each step. When the avatar steps back onto its own existing trail, the loop closes — every yellow target sprite whose centre lies strictly inside the closed polygon (Jordan-curve interior, ray-cast point-in-polygon) is captured, while any red forbidden sprite caught inside costs a strike. Three strikes lose the level; capturing every required sprite without exceeding the step budget wins. Level 1 introduces the base walk-trail-and-close mechanic. Level 2 adds a vertical column of three forbiddens that turns one big rectangular loop into a losing path (3 strikes), forcing the player to plan two smaller closures around the left and right target pairs separately. Level 3 keeps every L1 / L2 mechanic and adds three small pink 2×2 waypoints — the avatar's trail-head has to walk through every pink cell in addition to closing the loops, so the player must extend or detour their natural witness path to absorb each one before the level can be won.

## Action mapping
| Action | Effect |
|---|---|
| ACTION1 | Move avatar up one cell |
| ACTION2 | Move avatar down one cell |
| ACTION3 | Move avatar left one cell |
| ACTION4 | Move avatar right one cell |

ACTION5/6/7 are intentionally not declared — closure is automatic (no commit verb needed), there are no clickable sprites, and the game does not need undo.

## Levels
- **L1**: Base dynamic system — walk-deposits-trail (M1) + closing-loop-captures-interior (M2). 3 yellow targets in a horizontal cluster centre-stage; tutorial-friendly any-rectangle-around-targets wins.
- **L2**: Adds forbidden-strike (M3) + multi-closure-sequencing (M4). 4 corner targets + 3 forbiddens in central column. One big loop strikes 3 → lose; two small loops on either side of the forbidden column win.
- **L3**: Adds pink-marker-waypoints (M5). Same 4 corner targets + 3 forbidden column + 3 small pink 2×2 waypoints at cells `(2, 7)`, `(14, 7)`, `(8, 14)`. The avatar's trail-head must walk through every pink cell in addition to closing the two loops. The L2 witness naturally walks through two of the three pinks; the third (bottom-centre) requires a short 3-step detour after the second closure. Witness 57 actions.

## Novelty note
- Closest taxonomy entry: `sk48 paired-snake-trail` (also has trail-deposit-during-walk). **Distinguishing rule**: sk48 uses two mirrored snake heads with axis-flipped controls; the win is per-cell colour-match between the two trails. tj4n uses one avatar; the win is Jordan-curve interior membership (point-in-polygon) — a topology test rather than a per-cell parity test — combined with a must-walk-over waypoint constraint at L3.
- Closest prior-game entry: `qm4t convex-pen-trap` (also encloses target sprites for capture). **Distinguishing rule**: qm4t builds the pen as the *convex hull* of click-dropped vertex posts (always convex). tj4n builds the polygon as the avatar's literal walked path (can be arbitrarily non-convex); the polygon's edge length is bounded by walk cost; and there is no commit verb. tj4n's L3 also overlays a must-visit waypoint mechanic that qm4t doesn't have.

## Index update

Appended one row to `prior-games/index.md`:

```
| tj4n | walk-trail-loop-enclose | Boundary Trace — walk a loop; closed loop captures interior targets, strikes on enclosed forbiddens, plus must-visit pink waypoints at L3. | 2026-05-08T19:30:57Z | (autonomous) |
```
