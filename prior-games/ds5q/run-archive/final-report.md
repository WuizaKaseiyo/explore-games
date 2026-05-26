# Game generation final report

## Generated game
- **ID**: ds5q
- **Source**: `prior-games/ds5q/ds5q.py`
- **Metadata**: `prior-games/ds5q/metadata.json`
- **Lines of code**: 566

## Mechanic
The avatar is a small framed token with a corner indicator. It walks one logical tile (8 pixels) per arrow press through a stone-bordered chamber. ACTION5 swings a coloured strike: every wall in the avatar's 4-cardinal neighbourhood whose colour matches the indicator loses one hardness layer and is removed when its hardness reaches zero. The indicator's colour is set by stepping onto a same-coloured charge-pad on the floor; un-coloured strikes do nothing. Stone barriers are un-erodable and channel the avatar's path. Each level adds a rule on top of the previous level's vocabulary: L1 introduces walking and erosion on a single neutral wall colour, L2 introduces colour-matched charging via two pads, and L3 introduces multi-strike layered hardness, where walls are visibly stripe-banded by their remaining strike count and the player must commit to the right erode-position for several consecutive turns. The win condition for every level is to reach the exit cell within a generous step budget.

## Action mapping
| Action | Effect |
|---|---|
| ACTION1 | Move avatar 8 pixels north (one tile up); blocked by walls and stones. |
| ACTION2 | Move avatar 8 pixels south. Same blocking rules. |
| ACTION3 | Move avatar 8 pixels west. |
| ACTION4 | Move avatar 8 pixels east. |
| ACTION5 | Strike: decrement hardness of every same-colour adjacent wall by 1; remove if hardness reaches 0. No-op when uncharged. |

## Levels
- **Level 1** — establishes walk + erode on a one-tile-wide stone-bordered corridor with two grey hardness-1 walls between the avatar and the exit.
- **Level 2** — introduces the colour-pickaxe-match mechanic: the avatar starts uncharged and must visit a red pad before eroding the red wall, then visit a blue pad before eroding the blue wall that gates the exit.
- **Level 3** — introduces layered hardness: stripe-counted walls require multiple strikes. The col-3 corridor has TWO openings (a hardness-2 red wall on row 1 and a hardness-3 red wall on row 4), giving the post-discovery player a real route choice; the goal-row monotone-progress heuristic loses ~5 actions vs the optimal row-1 route.

## Novelty note
- **Closest taxonomy entry** — `xn5p` (chamber-stamp-partition). Distinguishing rule: xn5p ADDS walls to subdivide a chamber (additive); ds5q REMOVES wall layers to traverse one (subtractive). Goal is opposite-shape (partition vs reach-exit).
- **Closest prior-game entry** — `xn5p` (same as taxonomy match — it appears in both). The same distinguishing rule holds. Other near-misses (vd3g, fz5j, kn58, ek73, jd4q) share at most surface dimensions with ds5q; their core dynamics, routed entities, and player inputs differ concretely (see `mechanic-spec.md` § 9).

## Index update
Confirmed: one row appended to `prior-games/index.md`:
```
| ds5q | wall-erode-chain | Pickaxe Chamber — avatar walks 8-pixel hops in a stone-bordered chamber, charging a colour at coloured pads to chip same-colour walls down through visible hardness layers. | 2026-05-08T10:06:38Z | (autonomous) |
```
