# Game generation final report

## Generated game
- **ID**: `nb6t`
- **Source**: `prior-games/nb6t/nb6t.py`
- **Metadata**: `prior-games/nb6t/metadata.json`
- **Lines of code**: 579

## Mechanic
A chain of three rectangular rod-segments is anchored at a fixed cell of the playfield. Each segment has an independent absolute heading (E / N / W / S) and an integer length (1..14); the chain's hinges and tip are computed by walking the chain from the base. The player selects one of three hinges as the active hinge and rotates its segment 90° (CCW or CW), extends or retracts it (L2+), or sets the active hinge directly by clicking on a hinge cell. The active hinge is highlighted with a yellow halo so its identity is always visible. L1 establishes the base system (cycle + rotate); L2 layers length-adjust on top, requiring the player to retract one segment to reach a non-12-multiple x-coordinate; L3 layers carry-and-drop, where the chain's tip auto-picks-up a coloured object and a click on the tip drops it. Goal: place the tip on the level's target (L1, L2) or deliver the object to its colour-matched drop-zone (L3).

## Action mapping
| Action | Effect |
|---|---|
| ACTION1 | Extend the active segment by +1 cell (max 14). L2+ only. |
| ACTION2 | Retract the active segment by -1 cell (min 1). L2+ only. |
| ACTION3 | Rotate the active segment 90° CCW (E→N→W→S→E). |
| ACTION4 | Rotate the active segment 90° CW (E→S→W→N→E). |
| ACTION5 | Cycle the active hinge index forward (mod 3). |
| ACTION6 | Click at (x, y). On a hinge → set active. On the tip while carrying → drop the carried object. |

## Levels
- **L1**: cycle + rotate. Tutorial; tip must reach (4, 8). Witness length 6.
- **L2**: cycle + rotate + length-adjust. Tip must reach (8, 8); requires retracting seg 0 to length 8 plus rotating segs 1, 2 to N. Witness length 10.
- **L3**: cycle + rotate + length-adjust + carry-and-drop. Tip picks up red object at (8, 8); player must reconfigure the chain (extend seg 0 from 4 back to a target length, rotate seg 2 from N back to E, retract seg 0 to 4) to reach drop-zone at (32, 20), then click the tip to drop. Witness length 19.

## Novelty note
- **Closest taxonomy entry**: `s5i5` (rod-stretch-retract). Distinguishing rule: s5i5 has multiple **independent** rods on fixed axes that **stretch axially** via colour-swatch clicks; nb6t has **one connected** chain whose segments **rotate** about hinges (and additionally stretch via length-adjust). Visual signatures diverge — multiple separate sticks vs one polyline chain.
- **Closest prior-game entry**: `qz73` (radial-cycle-lock). Distinguishing rule: qz73 is a **single rigid rotor** whose tips move together as a rigid body; nb6t is **N independent hinges** whose segments rotate individually. qz73 has a tip-lock mode; nb6t has none.

## Index update
Appended one row to `prior-games/index.md`:

```
| nb6t | hinge-chain-reach | Articulated Reach — three rod-segments at independent hinges; rotate / extend / cycle active; carry-and-drop at L3 to deliver an item to a drop-zone. | 2026-05-07T22:11:11Z | (autonomous) |
```
