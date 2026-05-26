# Game generation final report

## Generated game
- **ID**: cv5b
- **Source**: `prior-games/cv5b/cv5b.py`
- **Metadata**: `prior-games/cv5b/metadata.json`
- **Lines of code**: 428

## Mechanic
A movable launcher walks a sky-blue playfield while carrying a charge
level cycled through three settings via the freedom slot. Clicking a
landing cell fires a marble along a parabolic arc from the launcher
to the click cell; charge level chooses between flat-low, medium, and
steep-high arc shapes (each with a corresponding maximum reach). The
player must direct arcs to land on every coloured target ring before
the step counter exhausts. Solid bars block both walking and arcs
travelling through them, forcing either a walk-around or a higher
arc to clear; a stippled vertical column deflects any arc that
passes through it by one cell. Level progression composes walking +
charge-cycling + barrier clearance + deflection-aware aiming, with
each level adding one or two new constraints rather than scaling a
single mechanic.

## Action mapping
| Action | Effect |
|---|---|
| ACTION1 | Move launcher up by 1 cell |
| ACTION2 | Move launcher down by 1 cell |
| ACTION3 | Move launcher left by 1 cell |
| ACTION4 | Move launcher right by 1 cell |
| ACTION5 | Cycle charge level 1 → 2 → 3 → 1 |
| ACTION6 | Click `(x, y)` to fire a parabolic-arc marble to that cell |

## Levels
- **L1 — tutorial.** Single launcher + single ground target. Witness:
  click target. Teaches arc-fire.
- **L2 — adds walk + charge-cycle.** Two ground targets at different
  distances; far target reachable only at max charge AND only after
  walking closer.
- **L3 — adds shield + wind.** Single far target; static shield
  blocks the ground walk corridor (forces walk-around through upper
  rows); wind column between launcher and target shifts arc landing
  +1 cell, requiring aim-correction.

## Novelty note
- **Closest taxonomy entry**: cd82 (orbit-fire-paint). Distinguishing
  rule: cd82's tank rides a fixed 8-slot ring around a central canvas
  and fires axial slabs; cv5b's launcher walks freely on a 2D
  playfield and fires a parabolic-arc marble at a clicked cell with
  charge-cycle controlling arc shape. cd82 paints; cv5b consumes
  targets. cd82 has no apex/range cycle and no barrier clearance.
- **Closest prior-game entry**: bx84 (beam-mirror-reflect).
  Distinguishing rule: bx84 has a static emitter and player-placed
  mirrors that reflect a straight beam at right angles; cv5b has a
  mobile launcher and a parabolic curve with no mirrors, charge-cycle
  setting apex/range, and a wind column that deflects mid-flight.

## Index update
One row appended to `prior-games/index.md`:
`| cv5b | arc-launch-target | Arc-Launch Target Practice — walking launcher fires marbles along power-cycled parabolic arcs at target rings; shields block, wind deflects. | 2026-05-10T13:51:22Z | (autonomous) |`
