# Mechanic Spec

## 1. Title
Counterweight Shaft Puzzle

## 2. Mechanic family
counterweight-latch-bridge

## 3. Mechanic essence
Move an avatar with arrows across scaffold tiles and ladders. `ACTION5` actuates the paired lift system when the avatar is standing on one of the platforms. Before the latch is engaged, the two lifts move in opposite vertical directions. After the left lift is latched high, the right lift can be toggled on its own. In level 3, stepping onto the bridge pad while the right lift is high permanently fills the bridge slot.

## 4. Levels 1-3

| Level | New composition | Witness |
|---|---|---|
| 1 | Walk to the ladder, ride the left lift upward, then cross the upper scaffold to the goal. | `[4, 4, 1, 1, 4, 5, 4, 4, 4, 4, 4]` |
| 2 | Latch the left lift high, climb down from the upper spine to the right lift, then raise it to reach the goal shelf. | `[4, 4, 1, 1, 4, 5, 4, 4, 4, 2, 2, 2, 4, 5, 4, 4, 4, 4, 4]` |
| 3 | Repeat the latch pattern, then use the raised right lift to trigger a permanent bridge before the final walk. | `[4, 4, 1, 1, 4, 5, 4, 4, 4, 2, 2, 2, 4, 5, 4, 4, 4, 4, 4, 4]` |

## 5. Action mapping

| Action | Meaning |
|---|---|
| `ACTION1` | move up on a ladder |
| `ACTION2` | move down on a ladder |
| `ACTION3` | move left one traversable cell |
| `ACTION4` | move right one traversable cell |
| `ACTION5` | actuate the lift under the avatar |

## 6. Win condition
Reach the goal pad on the current level.

## 7. Lose condition
Exhaust the step budget.

## 8. Internal state
- avatar cell
- left platform height
- right platform height
- left platform latch state
- bridge deployment state
- step count / step budget

## 9. Novelty note
The mechanic is not a color-routing, fluid-level, or slide-until-wall system. Its distinct core rule is that the avatar directly rides a paired lift, then permanently changes the coupling by latching one side before using the other to unlock a final traversal surface.
