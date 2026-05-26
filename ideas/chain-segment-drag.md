# Chain-Segment-Drag

## Summary

The player controls a **chain head sprite** trailed by a fixed
number of **body segments**. Arrow keys move the head 1 cell in
that direction. Each body segment maintains the rule **"stay 1
cell away (Manhattan = 1) from its successor in the chain
order"**: when the head moves, the first segment moves to the
head's old cell if its current Manhattan distance to the new
head position would be > 1; the second segment moves similarly
if the first segment's old position is > 1 cell away; and so on
down the chain. (This is the classic "Snake follow" rule.)

Each level shows **target rings** painted on the floor at fixed
cells. Levels can require the chain HEAD to reach a goal cell
AND/OR the BODY to cover a target zone (a set of cells, all of
which must be occupied by some chain cell at the same instant).
The level wins when the level-specific predicate holds at end of
turn. The only failure mode is exhausting the per-level step
counter.

## Visual elements

- 12×12 grid; pale-grey background.
- The **chain head** is a 1×1 saturated-colour cell (orange).
- **Body segments** are 1×1 cells in a slightly desaturated
  shade of the head's colour, with a small dark-grey 1-pixel
  marker showing chain order.
- **Target rings** are 1×1 hollow rings; goal-flag rings are
  saturated orange (head goal) and dark-grey (body-zone target).
- **Walls** are solid black 1×1 cells; the chain head is blocked;
  body segments cannot occupy walls (their follow-update is
  rejected if it would land them on a wall — see clarification
  in mechanics).

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION1 | Move chain head 1 cell up; trigger the body follow-update. Move is rejected if it would put the head on a wall or off-grid (no step consumed in that case to avoid easy-loss). | always |
| ACTION2 | Head down. | always |
| ACTION3 | Head left. | always |
| ACTION4 | Head right. | always |
| ACTION5 | Reverse the chain — what was the head becomes the tail and vice versa. After reversal, ACTION1-4 move the new head and body follows. The body cells stay in the same physical positions; only the chain ORDER reverses. | always |
| ACTION6 | Click on a body segment to "anchor" it — it stops following the chain head until the player clicks it again to release. Anchored segments still BLOCK head movement (act as walls for collision). | always |

`available_actions = [1, 2, 3, 4, 5, 6]`.

## Mechanics enumeration

- **M1 — head-walk-and-body-follow:** ACTION1-4 moves head 1
  cell. Each body segment then "follow-updates": if its
  Manhattan distance to its preceding-in-chain segment is > 1,
  it moves to the old position of its predecessor. Updates
  happen sequentially down the chain.
- **M2 — wall-block-head:** the head cannot enter a wall; if
  the move would go into a wall or off-grid, the entire
  move is cancelled (head stays put; no follow-update; no
  step consumed — to avoid bricking the player into wasted
  steps).
- **M3 — head-on-target win:** the chain head must reach the
  level's goal-flag cell.
- **M4 — body-zone-target (level 2+):** specific levels also
  require every cell in a target zone to be occupied by some
  chain cell (head or any body segment) at the end of the
  same turn the head is on its goal flag.
- **M5 — chain-reverse (level 3+):** ACTION5 reverses the chain
  order. This is a no-cost-spatial-rearrangement: the cells
  occupied by the chain do not change, but the *new head* is
  what was the tail. Subsequent ACTION1-4 moves the new head.
- **M6 — anchor-segment (level 3+):** ACTION6 click on a body
  segment toggles its anchor state. An anchored segment does
  NOT follow when the chain moves; it stays in place. Other
  segments still follow chain order, but the anchored segment
  acts like a wall for the head's collision check (so the head
  can't push through it). Anchor toggling lets the player pin
  parts of the body to cover specific target-zone cells while
  the head moves elsewhere.

## Per-level progression

### Level 1 — base system (M1 + M2 + M3)
- 8×8 region; chain length = 4. Goal flag at the far end. Walls form a simple maze.
- **Witness:** 15 actions. Head walks through the maze to reach the goal.
- **Mechanics required:** M1, M2, M3.

### Level 2 — + M4 (body-zone target)
- 10×10 region; chain length = 6. Complex walls.
- **Witness:** 35 actions. The player must choose a path so that when the head reaches the goal, the trailing body segments exactly cover the body-zone target. The body-zone target is shaped like a winding snake, forcing the player to take a highly specific, non-shortest path to the goal so the tail aligns perfectly.
- **Mechanics required:** M1, M2, M3, M4.

### Level 3 — + M5 (chain reverse) + M6 (anchor segment)
- 12×12 region; chain length = 8. Tight corridors.
- **Witness:** 60+ actions. The player must use anchors to pin parts of the body to cover target zones, then drag the rest of the chain elsewhere. Eventually, they must reverse the chain so the tail becomes the new head, allowing them to extract the chain from a dead-end without un-pinning the anchored segments. Extremely complex spatial reasoning required.
- **Mechanics required:** M1, M2, M3, M4, M5, M6.

## Win condition
After every action, check the head is on its goal-flag cell AND (level 2+) the body-zone target's required cells are all occupied by some chain cell. If predicate holds, fire `self.next_level()`.

## Lose condition
`steps_used >= max_steps` → `self.lose()`.

## Internal state
- `self.chain: list[Sprite]` — head at index 0, body segments in order toward tail.
- `self.positions: list[(int, int)]` — current cell per chain index.
- `self.anchored: set[Sprite]` — segments whose follow rule is suspended.
- `self.walls: set[(int, int)]`.
- `self.goal_pos: (int, int)`.
- `self.body_zone_target: set[(int, int)]` — required cells.
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `sk48 — paired-snake-trail`**: chain-segment-drag has ONE head and a chain that always FOLLOWS (the body position is determined by the head's history).

## Step budget
- L1: 40.
- L2: 80.
- L3: 150.

## Random-resistance
Random arrow presses produce a random walk; the chance of the head ending on the goal-flag AND the body simultaneously covering the target zone is exponentially small in chain length and target-zone size.

## Planning depth
- **L1:** moderate — trace a valid path through the maze.
- **L2:** deep — backward deduction required. Player must figure out the last N steps of the path to ensure the body aligns with the zone.
- **L3:** very deep — anchors act as temporary save points for body segments. Player must orchestrate the stretching and reversing of the chain to satisfy all constraints simultaneously.
