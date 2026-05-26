# Game generation final report

## Generated game
- **ID**: kx14
- **Source**: `prior-games/kx14/kx14.py`
- **Metadata**: `prior-games/kx14/metadata.json`
- **Lines of code**: 512

## Mechanic
The playfield is a vertical cross-section of a fluid tank. Light-blue
water fills cells from a movable surface line down to the bottom; the
upper part is air. One or more buoyant balls float on the water
surface, and a few solid horizontal platforms hang inside the tank at
fixed rows. The player's verbs are: raise/lower the water surface
(ACTION1/2), tilt all floating balls one cell left or right (ACTION3/4),
and click a ball to anchor or unanchor it (ACTION6). Anchored balls
ignore both surface changes and tilts and act as obstacles for other
balls. Each level resolves when every coloured ball sits inside its
same-coloured target ring; the only failure mode is exhausting the
per-level step counter. Level 1 introduces the base tide+tilt system
on an empty tank; level 2 adds platforms that block vertical paths in
specific columns; level 3 adds the anchor toggle and demands a
two-ball swap that tilt alone cannot resolve.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Raise the water surface by 1 row (towards the top of the grid). Re-projects every un-anchored ball: balls below the new surface rise buoyantly unless blocked by a platform in their column. |
| ACTION2 | Lower the water surface by 1 row (towards the bottom). Re-projects every un-anchored ball: balls above the new surface fall to the surface unless a platform stops them. |
| ACTION3 | Tilt every un-anchored ball one cell left, in column-ascending order; each ball blocked by a wall, a platform-cell, or another ball stays put. |
| ACTION4 | Tilt every un-anchored ball one cell right, in column-descending order; same blocking rules. |
| ACTION6 | Click at display-pixel `(x, y)`. If the click maps to a cell holding a ball and anchoring is enabled for the current level, toggle that ball's anchor state. Misclicks do not consume a step. |

## Levels

- **Level 1 — base dynamic system.** One orange ball, one orange target ring, no platforms, no anchor (clicks are no-ops). Water-control + tilt are the two required mechanics. Witness: 9 actions (4 ACTION1 + 5 ACTION4).
- **Level 2 — adds platform-block.** One orange ball, one orange target ring, plus a 3-cell-wide platform on the left at row 6 that blocks the direct vertical rise. Witness: 15 actions, threading right past the platform's right edge before continuing the rise.
- **Level 3 — adds anchor toggle.** Two balls (orange + green) on the water surface that must SWAP horizontal sides while landing at row 5; one platform in the middle (row 6 cols 4–6) blocks the upper tilt corridor, forcing a descend-tilt-rise loop for the second ball. Witness: 21 actions, anchoring the orange ball before raising water, tilting the green ball to its target, anchoring it, then unanchoring the orange ball and routing it via row 7 (below the platform) before raising back to the target row.

## Novelty note

- **Closest taxonomy entry: `sp80` (pour-shelf-route).** Distinguishing rule: sp80's water is an instantaneous cascade fired by ACTION5 against a 4-pour-per-level budget; the player primary verb is shelf-arrangement. kx14's water is a continuous bidirectionally-controlled persistent surface that rises/lowers each turn under direct player control; there is no pour event and no pour budget. Verb cardinality and water-event model both differ.
- **Closest prior-game entry: `qz73` (radial-cycle-lock).** Distinguishing rule: qz73's lock pins individual tips against a global ACTION5 ring rotation; the lock removes a tip from a single rotational cycle. kx14's anchor pins balls against BOTH water-level changes AND tilts (immunity from two distinct classes of player-environment-action); additionally, an anchored ball can be left in mid-air by a receding tide (an outcome qz73's lock has no analogue for). Topology differs entirely (radial dial vs vertical cross-section); visual signature differs entirely (small coloured tips on grey field vs water/air horizontal-band cross-section with internally-patterned 5×5 ball sprites).

## Index update

One row appended to `prior-games/index.md`:

```
| kx14 | tide-tilt-buoyant | Tide-Tilt Buoyant — vertical fluid tank where ACTION1/2 raise/lower the water surface, ACTION3/4 tilt floating balls, ACTION6 anchors. | 2026-04-29T01:42:31Z | (autonomous) |
```
