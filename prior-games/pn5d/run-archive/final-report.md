# Game generation final report

## Generated game
- **ID**: pn5d
- **Source**: `prior-games/pn5d/pn5d.py`
- **Metadata**: `prior-games/pn5d/metadata.json`
- **Lines of code**: 432

## Mechanic
A horizontal row of open-top vessels sits on the playfield, joined at their bases by toggleable valves rendered as small green-or-grey blocks in the gaps between them. The player slides a yellow ring-cursor between vessels with arrow keys, presses the pour key to add one liquid unit to every vessel in the cursor's currently-connected group, and clicks valves to flip their open/closed state and re-partition the group. Each vessel carries a red inward target pip on its right wall at the desired surface row; a vessel may also carry an outward orange overflow lip on its left wall, capping its surface to that row regardless of how high the rest of the group rises. The level wins when every vessel's surface matches its target; the level loses when the bottom step bar runs out. Levels compose: L1 introduces pour-and-equalize across a single fixed-open valve; L2 adds the valve-toggle verb (different targets force the player to disconnect); L3 adds the overflow cap (the budget-fitting strategy is the merged-group pour, where the cap absorbs C's excess while A, B, D rise to their high targets).

## Action mapping
| Action | Effect |
|---|---|
| ACTION3 | Move pour-cursor LEFT one vessel (clamped at the leftmost). |
| ACTION4 | Move pour-cursor RIGHT one vessel (clamped at the rightmost). |
| ACTION5 | Pour 1 height-unit into every vessel of the cursor's connected group; overflow-capped vessels clip their surface afterwards. |
| ACTION6 | Click `(x, y)`. If the click hits a valve sprite, toggle its open/closed state; otherwise no-op. |

## Levels
- **L1** (2 vessels A, B; one fixed-open valve A-B; targets A=B=4; budget 12): introduces M1 pour-and-equalize. Witness = 4 pours.
- **L2** (3 vessels A, B, C; valves A-B and B-C, both initially open; targets A=3, B=2, C=5; budget 18): adds M2 valve-toggle. Witness = 10 actions: 2 group pours, then 2 toggles to disconnect, then per-vessel pours.
- **L3** (4 vessels A, B, C, D; 3 valves all initially closed; C with overflow cap at 2; targets A=B=D=9, C=2; budget 20): adds M3 overflow-cap. Witness = 12 actions: 3 toggles to merge all, then 9 pours; C clips at 2 from pour 3 onward while A, B, D rise to 9.

## Novelty note
- Closest taxonomy entry: **sp80** (`pour-shelf-route`). Distinguishing rule: sp80 routes discrete falling drops via player-positioned shelves into target cups (aiming task with a 4-attempt counter); pn5d distributes continuous liquid volume across a connected-vessel graph (no drops, no aiming, no attempt counter).
- Closest prior-games entry: **kx14** (`tide-tilt-buoyant`). Distinguishing rule: kx14 has one tank with a player-controlled global water surface and buoyant balls that re-project; the win is balls landing on rings. pn5d has multiple vessels with player-toggleable connectivity; the player pours rather than raising the surface; the win is the surfaces themselves at marked rows. Different cast, verb, goal axis.

## Index update
One row appended to `prior-games/index.md`:

```
| pn5d | vessel-equalize-flow | Connected-Vessel Filling — pour into one vessel raises every connected vessel; toggleable valves split groups; overflow caps clip surfaces. | 2026-05-08T22:01:32Z | (autonomous) |
```
