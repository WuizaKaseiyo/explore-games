# Stack-Pillar-Lift

## Summary

The grid has a row of vertical **pillar slots** along the bottom.
Each pillar slot can hold a stack of coloured **block sprites**,
stacked from the bottom up. The player has a single-block
**holder buffer** above the pillars (visible as a 1×1 sprite at
the top centre); at most one block can be held at a time. Verbs:
ACTION6 click a pillar to **lift** the topmost block from that
pillar into the holder; ACTION6 click a pillar with the holder
already full to **drop** the held block onto the top of that
pillar. ACTION5 returns the held block to its original pillar
(pure undo of the most recent lift, only valid if no drop has
happened since).

Each level shows a static **target stack arrangement** (one
target per pillar). The level wins when every pillar's current
stack of block colours from bottom to top exactly equals the
target's bottom-to-top sequence AND the holder is empty. The
only failure mode is exhausting the per-level step counter.

## Visual elements

- 12×12 grid; 5 pillars rendered as 1-cell-wide vertical strips
  along the bottom 8 rows.
- Each block is a 1×1 saturated-colour cell; stacks render as a
  vertical column of blocks rising from the pillar's base.
- The **holder buffer** is a single 1×1 cell at top centre; when
  empty, it shows a hollow grey square; when full, it shows the
  held block's colour.
- A **target panel** above each pillar shows the required
  bottom-to-top sequence as a small vertical strip (1-pixel-wide
  cells at scale).
- A **locked block** (level 2+) carries a 1-pixel dark-grey
  border — it cannot be lifted (clicking the pillar lifts the
  next-down block above it, OR if it's the topmost, the click
  is a no-op).

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION5 | Return the most-recently-lifted block to the pillar it came from. Only valid if the holder is full AND the block in the holder was lifted (not yet dropped) most-recently. | holder full AND has a "lift origin" |
| ACTION6 | Click pixel `(x, y)`; engine resolves to nearest pillar (column-aligned). If holder is empty, lift the topmost block from that pillar (if any AND not locked); update holder. If holder is full, drop the held block on top of that pillar's stack. Click off-pillar is a no-op. | always |

`available_actions = [5, 6]`. No avatar.

## Mechanics enumeration

- **M1 — lift-block:** ACTION6 click a pillar with the holder
  empty; topmost block is moved to the holder.
- **M2 — drop-block:** ACTION6 click a pillar with the holder
  full; held block is placed on top of that pillar's stack.
- **M3 — undo-lift:** ACTION5 returns the held block to its
  original pillar (only valid if the block is in the holder
  from a recent lift and has not been replaced/dropped).
- **M4 — match-target-stacks:** the win predicate compares
  every pillar's current bottom-to-top stack to the target
  stack AND requires the holder to be empty.
- **M5 — locked-block (level 2+):** specific blocks are tagged
  `locked` and cannot be lifted. If a pillar's topmost block is
  locked, ACTION6 click on that pillar is a no-op (no step
  consumed). The player cannot lift past a locked block (stack
  LIFO discipline), so locked blocks must already be in their
  target stack position at level start; the player builds the
  remaining stacks around them.
- **M6 — capacity-limit-pillar (level 3+):** specific pillars
  have a maximum stack height (e.g. 3 blocks). Dropping a block
  on a pillar that's at capacity is rejected (no-op, no step
  consumed; the holder remains full). This forces the player
  to plan WHERE to temporarily park blocks while assembling
  another pillar's target stack.

## Per-level progression

### Level 1 — base system (M1 + M2 + M4)
- 3 pillars; 6 blocks total. Target: Specific stack arrangements on two pillars.
- **Witness:** 15 actions. Towers of Hanoi style gameplay but with block colors. The player must shuffle blocks around to extract the required colors and stack them in the correct sequence.
- **Mechanics required:** M1 (lift), M2 (drop), M4 (target match).

### Level 2 — + M3 (undo) + M5 (locked block)
- 4 pillars; 10 blocks; 3 locked blocks. 
- **Witness:** 35 actions. The locked blocks act as obstacles that prevent accessing the blocks beneath them. The player must find ways to route their desired blocks around the locked ones, treating the locked blocks as permanent walls in the vertical axis.
- **Mechanics required:** M1, M2, M3, M4, M5.

### Level 3 — + M6 (capacity limit) + composition
- 5 pillars; 15 blocks; 4 locked blocks; 2 capacity-limited pillars (max 2 blocks each).
- **Witness:** 60+ actions. The capacity-limited pillars are the only free spaces, making them extreme bottlenecks. The player must perform a highly specific sequence of lifts and drops to shuffle blocks without overflowing the limited pillars. A single misplaced block will deadlock the puzzle.
- **Mechanics required:** M1, M2, M3, M4, M5, M6.

## Win condition
After every ACTION6 that resolves to a lift or drop, walk every pillar; compare its bottom-to-top stack of block colours to the pillar's target stack. AND check the holder is empty. If both conditions hold, fire `self.next_level()`.

## Lose condition
`steps_used >= max_steps` → `self.lose()`.

## Internal state
- `self.pillars: list[list[Block]]` — pillar index → bottom-up stack of blocks.
- `self.holder: Block | None` — single held block.
- `self.lift_origin_index: int | None` — pillar index from which the held block was lifted (used for ACTION5 undo).
- `self.locked: set[Block]` — blocks that cannot be lifted.
- `self.pillar_capacities: list[int | None]` — per-pillar max height (None = unlimited).
- `self.targets: list[list[int]]` — per-pillar target colour sequence (bottom-up).
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus
- **vs `sb26 — tile-place-commit`**: stack-pillar-lift uses *vertical* stacks where order matters bottom-to-top, and there's no commit phase — every action immediately rearranges state.

## Step budget
- L1: 40.
- L2: 80.
- L3: 150.

## Random-resistance
Random pillar clicks lift and drop blocks at random; the chance of every pillar's stack matching the exact target sequence is small. L3's capacity limits + locked blocks make random play essentially unable to solve.

## Planning depth
- **L1:** moderate — recognise which blocks need to move where.
- **L2:** deep — locked blocks force routing through other pillars, requiring intermediate sorting steps.
- **L3:** very deep — capacity limits force ordering: blocks must be parked in the right pillar at the right time. The extremely constrained workspace requires calculating 10+ moves ahead to avoid deadlocks.
