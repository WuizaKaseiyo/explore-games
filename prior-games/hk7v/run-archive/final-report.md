# Game generation final report

## Generated game
- **ID**: `hk7v`
- **Source**: `prior-games/hk7v/hk7v.py`
- **Metadata**: `prior-games/hk7v/metadata.json`
- **Lines of code**: 449

## Mechanic
The player operates a Cartesian gantry from above the playfield —
there is no walking avatar. A horizontal beam at the top carries a
small movable trolley; a vertical rope of variable length hangs from
the trolley, ending in a U-claw hook. ACTION3/4 slide the trolley
left/right one cell; ACTION1/2 raise/lower the hook one cell; ACTION5
toggles grab/release on whatever block sits directly below the hook.
A released block falls under gravity until it rests on floor or atop
another block. Each level wins when every coloured block sits on its
same-coloured horizontal target stripe on the floor. Composition adds
two constraints across the three levels: a wall the rope and any
carried block must clear by hook-raising before horizontal traversal
(L2), and a stacked supply column whose blocks must be removed
top-down because only the topmost block is grabbable (L3).

## Action mapping
| Action | Effect |
|---|---|
| ACTION1 (UP) | Raise hook one cell (rope shortens). Carried block rises with it. |
| ACTION2 (DOWN) | Lower hook one cell (rope lengthens). Carried block lowers with it. |
| ACTION3 (LEFT) | Slide trolley one cell left. Hook + rope + any carried block follow. |
| ACTION4 (RIGHT) | Slide trolley one cell right. |
| ACTION5 | Toggle grab/release. Grab a block whose top is directly below the hook bottom; release the carried block to fall under gravity. |

ACTION6 (click) and ACTION7 (undo) are not declared.

## Levels
- **L1** — Tutorial: one red block, one red target, no wall.
  Introduces the overhead manipulator (M1).
- **L2** — Adds **+2 mechanics**: colour-pairing (M2, two distinct
  block/target pairs) and rope-clearance-above-wall (M3, a wall in
  the middle that forces hook-raising before horizontal traversal).
- **L3** — Adds **+1 mechanic**: gravity-stacking-disassembly (M4)
  — the supply column starts as a stack of three blocks, and only
  the topmost is grabbable. Composes with the L2 wall and three
  coloured target/block pairs.

## Novelty note
- **Closest taxonomy entry**: `wa30` (lock-drag-crate) — shared at
  the abstract goal level (deliver coloured objects to coloured
  drop-zones). Distinguishing rule: in `wa30` the player IS the
  walking actor latched to a crate; in `hk7v` there is no walking
  avatar — every input drives an overhead trolley/rope/hook system,
  and the rope-clearance + gravity-stacking constraints have no
  analogue in `wa30`.
- **Closest prior-game entry**: `dj5h` (pulley-pair-platform) — the
  only other prior with an "overhead" element. Distinguishing rule:
  `dj5h` couples paired hanging platforms (raising one drops the
  other) and the player rides a platform; `hk7v` has a single rope
  with one hook, no coupling, and the player is not on the
  playfield at all. Other near-misses (`vt6q` grapple-anchor-yank,
  `nb6t` hinge-chain-reach, `pv5q` pivot-rod-swing, `wb6n`
  tether-pin-wrap) each diverge on at least 5 of the 8
  negative-similarity dimensions; the radial-vs-Cartesian
  manipulator-geometry distinction is the load-bearing axis against
  most of them.

## Index update
One row appended to `prior-games/index.md`:

```
| hk7v | overhead-trolley-hook | Overhead Trolley + Hook Pick-and-Place — gantry trolley + variable-rope hook delivers coloured blocks to coloured floor markers; rope clears walls and stack disassembly. | 2026-05-10T07:10:19Z | (autonomous) |
```

`mechanism-detail.md` written to
`prior-games/hk7v/mechanism-detail.md`.
