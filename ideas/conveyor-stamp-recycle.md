# Conveyor-Stamp-Recycle

*(NEW idea filling the **continuous-feed processing-pipeline
blindspot**. Real-world inspiration: factory conveyor belts,
postal sorting offices, bottling lines, simple ICs — where items
move along a track and pass through fixed transformation stages.
Top-down U-shaped track view.)*

## Summary

A **U-shaped conveyor belt** loops around the playfield: items
enter at the top-left **inlet**, ride the belt clockwise around
the U, and exit at the top-right **outlet bin**. Every tick, every
item on the belt advances one cell along the loop direction.
Cells along the belt are slots into which the player can drop
**stamp tiles** that transform any item passing over them.

The player's verbs: ACTION6 click a stamp in the side tray to
select it, then click a slot to drop it. Stamps placed on the
belt are static; once placed they persist for the rest of the
level. ACTION5 advances the belt by one tick (releases another
input item from the inlet, every passing item advances one cell,
items in the outlet are scored).

The level wins when every input item has been processed and
delivered to the outlet bin matching its required output
signature.

## Visual elements (distinct from prior corpus)

- 64×64 canvas. The belt is rendered as a dotted dark-grey
  pathway (a U bent around three sides of the playfield). Belt
  motion is visualised as **moving 1-pixel hash marks** that
  shift one pixel per tick — this is the most dynamic visual cue
  in the corpus, telegraphing "things are moving" even before
  any item is in flight.
- An **inlet hopper** at the top-left has a queue of pending
  items rendered as a vertical stack (next item at top, second
  in queue below it, …).
- **Items** are 2×2 sprites in palette colours. They may carry
  a 1-pixel **stripe** (added by stripe-stamps) or have a
  **shape mark** (a small dot, square, or triangle inside)
  added by shape-stamps. The full colour-stripe-shape state is
  the item's *signature*.
- **Stamps** are 3×3 sprites with iconic glyphs:
  - colour-paint stamp: a coloured paint blob.
  - stripe-stamp: 3 horizontal lines.
  - shape-stamp: a small square / triangle / circle.
  - L2 branch-switch: a Y-junction icon.
  - L3 recycle-gate: a curved-arrow icon.
  - L3 timer-stamp: a clock-face icon.
- The **outlet bin** at top-right is a 3-cell-wide receptacle
  with a target signature pinned above it (icons of the
  required colour-stripe-shape combinations).
- A **stamp tray** runs along the bottom of the canvas: one slot
  per available stamp, with selection pip on the active stamp.
- A **reading rule strip** appears on the right rim above the
  outlet showing the win signature pictographically (colour
  swatch + stripe pattern + shape icon, one row per required
  output).

## Action mapping

| Action | Semantic | Gate |
|---|---|---|
| ACTION5 | Advance the belt one tick. Each in-flight item moves one cell along the loop. The next pending input item enters the inlet (if the inlet cell is empty). All stamps trigger on every item that landed on them this tick. Items that reach the outlet bin are scored (they remain in the bin, painted with their final signature). | always |
| ACTION6 | Click cell `(x, y)`. Resolves to one of: (a) stamp in tray → select; (b) belt slot when a stamp is selected → drop the stamp there (consumes that stamp from the tray); (c) on L3 a placed timer-stamp → tick its phase by 1; (d) anywhere else → no-op. | always |

`available_actions = [5, 6]`.

## Mechanics enumeration

- **M1 — belt-tick:** ACTION5 advances belt by one cell in the
  loop direction (clockwise around the U). Every item moves
  exactly one cell.
- **M2 — inlet-feed:** at each tick, the next item in the inlet
  queue is placed at the inlet cell (if empty). The queue is
  fixed by level data (a deterministic order of items).
- **M3 — stamp-transform:** when an item lands on a cell holding
  a stamp, the stamp's transform is applied to the item's
  signature: colour-paint stamp overrides colour; stripe-stamp
  adds a stripe (cumulative — a stripe-stamp passed twice gives
  a double stripe); shape-stamp sets the shape mark.
- **M4 — outlet-score:** when an item reaches the outlet cell,
  it lands in the outlet bin (final state). The win predicate
  compares the multiset of bin contents to the level's target
  signature multiset.
- **M5 — branch-switch (level 2+):** a Y-junction stamp at a
  belt corner directs the item *based on its current colour*
  (the branch's rule is shown by colour-coded arrows on the
  stamp's icon). One belt becomes two belts on L2: a primary
  outer loop and a smaller inner shortcut. Items on the wrong
  branch reach the outlet faster but skip a downstream stamp;
  items on the right branch take the longer path.
- **M6 — recycle-gate (level 3+):** a recycle-gate stamp loops
  the item back to the inlet cell instead of advancing. Items
  passing through a recycle-gate re-enter the queue (without
  re-rendering the original colour — the item retains the
  state it had at recycle).
- **M7 — timer-stamp (level 3+):** a timer-stamp has a phase ∈
  {0, 1, 2}. It transforms an item only when phase = 0 (else
  pass-through). Each ACTION5 tick advances the phase by 1
  mod 3. ACTION6 click on the timer-stamp manually advances it
  by 1 mod 3 at a step cost. This couples item arrival timing
  to stamp phase — the player must align them.

## Per-level progression

### Level 1 — base belt + stamps (M1 + M2 + M3 + M4)
- A simple U-shape belt of total length 12 cells. 3 input items
  in the queue: red, blue, gold. The outlet target multiset
  requires `{red+stripe, blue+circle, gold+square}`. Stamp tray
  has 3 stamps: stripe, circle, square.
- The player must place each stamp on the right belt cell so
  each item picks up the correct mark. Random placement fails
  because stamps act on every item passing over them — placing
  the stripe-stamp on a cell where the blue item passes also
  stripes the blue item.
- **Witness:** ~9 actions (3 selects + 3 drops + 3 ticks).
  Step budget 14.
- **Mechanics required:** M1, M2, M3, M4.

### Level 2 — + M5 (branch-switch)
- Belt has a fork: an outer loop of 14 cells and an inner
  shortcut of 6 cells. 5 input items mixed colours. Output
  target multiset requires distinct treatment for some items
  (some need 3 stamps; others need only 1). The branch-switch
  stamp routes based on item colour: red goes outer, blue goes
  inner.
- The player must (a) place colour-paint stamps that pre-
  colour items so they take the *correct* branch, and (b)
  place transform stamps on each branch so items emerge with
  the right signature. Items mis-routed on the inner shortcut
  reach the outlet without enough transforms.
- **Witness:** ~16 actions. Step budget 26.
- **Mechanics required:** M1, M2, M3, M4, M5.

### Level 3 — + M6 (recycle) + M7 (timer-stamp)
- Belt with two branches and a recycle gate. 6 input items
  with very specific multi-stamp targets, e.g. `red + stripe +
  stripe + circle` requires the item to pass through
  stripe-stamp **twice** plus circle-stamp once.
- Timer-stamps with phase 0/1/2 mean the item must arrive at
  the right tick. The recycle-gate is the strategic resource:
  routing an item through it lengthens its journey by enough
  ticks to align with a timer-stamp's phase 0 window. Some
  items must NOT be recycled (they would over-stamp).
- The player has 2 recycle-gates and 1 timer-stamp in the
  tray. Choosing where to place them is the L3 puzzle.
- **Witness:** ~28 actions. Step budget 50.
- **Mechanics required:** M1, M2, M3, M4, M5, M6, M7.

## Win condition

After every ACTION5 tick, count items in the outlet bin. If the
multiset of bin contents (including signature) equals the level's
target multiset AND the inlet queue is empty AND the belt is
empty, fire `self.next_level()`.

## Lose condition

- `steps_used >= max_steps` triggers `self.lose()`.
- An item arriving at the outlet with a signature that does not
  match any unfilled target slot triggers `self.lose()`
  immediately (the bin colours red and the level ends). This
  prevents brute-force placement.

## Internal state

- `self.belt: list[(int, int)]` — ordered loop of belt cells.
- `self.belt_dir: int` — index advance per tick.
- `self.items_in_flight: list[Item]` — `belt_index, signature`.
- `self.inlet_queue: list[Item]` — pending input.
- `self.outlet_bin: list[Item]` — scored items.
- `self.stamps_placed: dict[(int, int), Stamp]` — `kind`,
  `phase` (timer only), `branch_rule` (branch only).
- `self.tray: list[Stamp]` — pending stamps.
- `self.target_signature: list[Signature]` — required outlet
  signatures (multiset).
- `self.tick: int`.
- `self.steps_used: int` / `self.max_steps: int`.

## Novelty vs reference + prior corpus

- **vs `vc33 — row-slide-pull-tab`**: vc33 has units perched on
  a single sliding row that the player drags entirely. Conveyor
  has the *belt* moving items autonomously each tick; player
  places **transforms** on the path, doesn't drag the belt.
- **vs `gg14 — kiln-mosaic-stamp`**: gg14 is stamp-on-canvas:
  the player places stamps directly on the playfield, items
  don't move. Conveyor has *moving items* under static stamps —
  the player composes a static processing pipeline.
- **vs `gg17 — fuse-burn-ignite`**: fuse-burn propagates fire
  through a graph. Conveyor moves discrete items one cell per
  tick along a fixed loop; transforms happen at fixed cells,
  not by edge-propagation.
- **vs `sb26 — tile-place-commit`** (reference): sb26 places
  tiles into target slots and commits. Conveyor's items
  *flow*; the player places stamps to transform them mid-flow,
  not place items into target slots.

## Step budget

- L1: 14.
- L2: 26.
- L3: 50.

## Random-resistance

Random stamp placement is very unlikely to satisfy the target
multiset on L3: items pass over every stamp on their path, so a
mis-placed stamp ruins multiple items at once. The
recycle/timer/branch combinations on L3 form a small but tight
constraint problem; random play essentially never satisfies all
of them.

## Planning depth

- **L1:** shallow — assign one stamp per cell and let the belt
  do the work.
- **L2:** moderate — branch routing forces the player to
  decompose the path into two parallel transform pipelines;
  must use colour-paint to control branching.
- **L3:** deep — recycle gates and timer-stamps couple item
  *timing* to stamp activation, requiring backward arithmetic
  on tick counts to align item arrival with phase 0 windows.
