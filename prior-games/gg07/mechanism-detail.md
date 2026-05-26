# gg07 — stack-pillar-lift

## Summary

The player controls a small overhead crane that moves along a rail above
vertical pillar stacks. ACTION3 and ACTION4 move the crane exactly one pillar
left or right. ACTION6 operates only at the current crane column: with an
empty claw it lifts the top block, and with a full claw it drops that block
onto the current pillar. ACTION5 immediately returns a just-lifted block to
the same pillar, but only before the crane has moved away.

The side panel shows compact vertical target mini-stacks: one separated
three-slot mini-stack per pillar, ordered from top to bottom in the same order
as the pillars. Within each mini-stack, lower dots are lower stack positions
and upper dots are higher stack positions. Neutral dots mark empty target
slots, so empty pillars are explicit. The target panel is separated from the
live piles by a dark divider, and every coloured block visible in the live
pile area is movable. Later levels add capacity-limited temporary pillars.
The energy bar is drawn vertically on the right edge for visual variety.

## Action mapping

| Action | Semantic | Gate / when valid |
|---|---|---|
| ACTION3 | Move crane one pillar left. | rejected at the left edge |
| ACTION4 | Move crane one pillar right. | rejected at the right edge |
| ACTION5 | Return the currently held block to the pillar it was lifted from. | holder full and crane has not moved since the lift |
| ACTION6 | Lift the top block from the current pillar, or drop the held block onto it. | rejected for empty stacks or full capacity-limited pillars |

## Per-level mechanic progression

| Level | Mechanic introduced | Specific challenge / constraint |
|---|---|---|
| 1 | One-step crane movement, lift/drop, stack target matching. | Swap the two exposed top blocks while moving the crane through the middle pillar as a temporary buffer. Witness: lift P0, move to P1, drop; move to P2, lift, move to P0, drop; return to P1, lift, move to P2, drop. |
| 2 | Three-block target stack. | P0 starts with red under yellow, P1 starts with green, and P3 starts with purple. The target requires P1 to become green-yellow-purple and P2 to hold red, so moving only yellow and purple cannot win. |
| 3 | Capacity-limited temporary pillars. | P2 and P3 can hold only one block. The player must park yellow in a one-block temporary pillar, carry purple left onto P0, then bring yellow back to P1 without overflowing a capped pillar. |

## Win condition

After every effective action, compare each pillar's current coloured block
sequence from bottom to top against the side-panel target mini-stacks. The
claw must be empty. The win predicate is purely positional; it no longer
requires any particular action sequence or undo marker activation. When all
predicates hold, `self.next_level()` fires.

## Lose condition

Effective crane moves, lifts, drops, and undo actions decrement the step bar.
If it reaches zero before the win predicate holds, `self.lose()` fires.
Rejected edge moves and impossible lift/drop attempts are free no-ops.

## Internal state

- `self.crane_index`: current pillar under the crane.
- `self.pillars`: per-pillar bottom-up colour-key stacks.
- `self.holder`: held colour key or `None`.
- `self.lift_origin`: immediate undo origin, cleared as soon as the crane moves.
- `self.targets`: bottom-up target colour keys per pillar.
- `self.capacities`: optional maximum stack height per pillar.
- `self.undo_required` / `self.undo_used`: visual marker state only.
- `self.steps_left` / `self.max_steps`: visible step budget.

## Notable code patterns

- The crane makes block transport spatial: blocks move one pillar step at a
  time because the held block rides with the crane.
- Target indicators are compact vertical side-panel mini-stacks, separate
  from live blocks; empty target pillars are shown with neutral dots.
- The renderer avoids under-block base sprites, so lifting a block reveals the
  normal pillar/floor cell rather than a misleading block-like background.
- ACTION3 and ACTION4 route the crane left and right, ACTION5 can undo a
  just-lifted block before the crane moves, and ACTION6 is the lift/drop
  operation.
