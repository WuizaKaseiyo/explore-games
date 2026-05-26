# Game generation final report

## Generated game
- **ID**: zw91
- **Source**: `prior-games/zw91/zw91.py`
- **Metadata**: `prior-games/zw91/metadata.json`
- **Lines of code**: 594

## Mechanic
The player controls one mobile avatar whose footprint cycles through three sizes (small, medium, large). Arrows step the avatar one tile cardinally; ACTION5 grows the avatar by one notch. Growing the avatar over a `shove_block` rolls the block in the cardinal direction away from the avatar's centre until it hits a wall or another block. From size 3, ACTION5 enters a one-shot **overloaded** state visible as a halo, and a further ACTION5 fires a **burst** that destroys nearby `shove_block` and `breakaway_wall` sprites within Chebyshev-12 cells of the footprint, resetting the avatar to size 1. The level is won when the avatar's body fits a same-shape `socket` ring at matching size; the level is lost when the per-level step counter expires. L1 establishes movement + size-cycle; L2 adds inflate-push; L3 adds overload-burst, with the witness requiring all four mechanics to fire in concert (push blocks east, then burst destroys both rolled blocks AND breakaway-walls in one shot).

## Action mapping
| Action | Effect |
|---|---|
| ACTION1 | UP — move avatar 4 cells north (no-op if footprint overlaps wall or shove_block) |
| ACTION2 | DOWN — move avatar 4 cells south |
| ACTION3 | LEFT — move avatar 4 cells west |
| ACTION4 | RIGHT — move avatar 4 cells east |
| ACTION5 | size-cycle / enter-overload / fire-burst — branch on `(self.size, self.overloaded)` |

## Levels
- **L1** (base dynamic system): M1 move + M2 size-cycle. Open chamber; one socket-large at the opposite corner; navigate + cycle to match. Witness 22 actions, step budget 50.
- **L2** (+M3 inflate-push): vertical wall column with a 2-tile gap plugged by 2 shove-blocks blocks the only east passage; align in the gap row, inflate to size 2 to push blocks aside, walk to socket-med. Witness 12 actions, step budget 60.
- **L3** (+M4 overload-burst): two wall columns each with a 3-tile gap — first plugged by 3 shove-blocks, second by 3 breakaway-walls — sealing off the inner room with socket-large; navigate to a position whose Cheby-12 burst zone covers both target sets, push blocks east during the 2→3 cycle, overload, burst (destroys blocks AND breakaways simultaneously), then re-navigate east at size 1 and re-cycle to size 3 at the socket. Witness 17 actions, step budget 100.

## Novelty note
- **Closest taxonomy entry**: `s5i5` (rod-stretch-retract). Distinguishing rule: in s5i5 the player operates remote click-control swatches to stretch *stationary* rods whose tips must reach targets — the player is not on the playfield. In zw91 the player IS the avatar — a single mobile pawn whose footprint cycles through 3 *radial* sizes via a modal verb (ACTION5), and the win condition is the avatar's body fitting a same-shape socket at matching size. Different agency (player-embodied vs remote operator), different verb axis (radial vs axial), different goal (body-in-socket vs tip-on-target).
- **Closest prior-game entry**: `nb6t` (hinge-chain-reach). Distinguishing rule: nb6t has multiple jointed rod-segments with independent hinges that the player articulates by selecting and rotating each segment; zw91 has a single self-contained avatar whose entire footprint resizes radially in place — no hinges, no segments, no kinematic chain. nb6t plays as "operate an articulated arm"; zw91 plays as "be a self-resizing pawn." (`gv47` seed-grow-surround-dissolve was also flagged but is more distant — gv47 grows *regions on a canvas*, not a player avatar.)

## Index update
One row appended to `prior-games/index.md`:

```
| zw91 | inflate-fit-burst | Inflate-Fit-Burst — single avatar whose footprint cycles 3 sizes; arrows move, ACTION5 grows-pushes-or-bursts; body must fit same-size socket. | 2026-05-08T00:19:13Z | (autonomous) |
```
