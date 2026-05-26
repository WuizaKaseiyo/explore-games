# Game generation final report

## Generated game
- **ID**: rt9k
- **Source**: `prior-games/rt9k/rt9k.py`
- **Metadata**: `prior-games/rt9k/metadata.json`
- **Lines of code**: 454

## Mechanic

The player walks a single avatar across a small playfield with the
four arrow keys. The playfield's outer boundary is a torus —
walking off any edge re-enters from the opposite edge — and every
wrap-cross nudges the avatar's visible tone-state by one step in a
three-hue cycle (right or down wraps advance the tone; left or up
wraps regress it). Some walls are tone-coded and only let the
avatar pass when its tone matches their tone, and the third level
adds a goal cell that only completes the level when the avatar
arrives in the right tone. Reaching the goal therefore becomes a
problem of composing wrap-crosses to land in the right cell with
the right tone at the right moment, with one new mechanic introduced
per level (wrap; then tone-cycle and tone-coded filter walls; then a
tone-keyed goal in the third level).

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Move avatar one cell up; if the move would leave the playfield, wrap to the opposite (bottom) edge AND decrement tone by one (mod 3). |
| ACTION2 | Move avatar one cell down; if the move would leave the playfield, wrap to the opposite (top) edge AND increment tone by one (mod 3). |
| ACTION3 | Move avatar one cell left; left-edge wrap → right edge AND tone −1 (mod 3). |
| ACTION4 | Move avatar one cell right; right-edge wrap → left edge AND tone +1 (mod 3). |

(No ACTION5, no ACTION6, no ACTION7. Pure-arrow control.)

## Levels

- **L1.** Tutorial. Avatar at left, plain goal at right, single full-height solid wall splitting the playfield. The only path is a wrap. Witness = 9 LEFT presses; budget 30.
- **L2.** Adds tone-cycle on wrap-cross + tone-coded filter walls. A green filter column on the right half blocks any avatar that hasn't gained green tone via a left-wrap. Witness = 4 LEFT + 12 DOWN; budget 50.
- **L3.** Adds a goal-tone gate (the goal cell only triggers the level transition when the avatar arrives with yellow tone) and a yellow filter strip across the right half's bottom row. Reaching the goal in yellow tone forces a second wrap (UP-wrap from the goal column) that converts green back to yellow, threading the avatar through the yellow filter strip on the way. Witness = 4 LEFT + 15 UP = 19 actions; budget 70.

## Novelty note

- **Closest taxonomy entry**: `m0r0` (mirrored-quad-control). Distinguishing rule: m0r0 controls four avatars whose move axes are mirrored per-quadrant; rt9k controls one avatar on a wrapping torus surface where inputs are never mirrored — the only input-to-state coupling is the topological wrap, not an axis flip.
- **Closest prior-game entry**: `pk4m` (duotone-flip-walk). Distinguishing rule: pk4m exposes an explicit ACTION5 colour-flip verb plus auto-flip pads inside the playfield (free in-place colour change); rt9k ties tone change *only* to topological wrap-edge crossings, has no ACTION5 toggle and no flip-pads, and uses a three-tone cycle instead of pk4m's binary toggle. The mental model diverges: pk4m's player asks "when do I flip?"; rt9k's player asks "which edges do I cross, in what order, to land at the goal in the right tone?".

## Index update

One row appended to `prior-games/index.md`:

```
| rt9k | torus-wrap-tone-cycle | Torus Wrap with Tone-Cycle — arrows walk an avatar on a torus playfield; each wrap-cross cycles tone through 3 hues; tone-coded filter walls and L3 goal-tone gate. | 2026-05-10T07:10:49Z | (autonomous) |
```
