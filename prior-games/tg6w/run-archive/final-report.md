# Game generation final report

## Generated game
- **ID**: tg6w
- **Source**: `prior-games/tg6w/tg6w.py`
- **Metadata**: `prior-games/tg6w/metadata.json`
- **Lines of code**: 597

## Mechanic

Settle-Pile Tilt is a 4-direction gravity-rotation puzzle: each arrow press sets the playfield's "down" direction, and every loose coloured block slides simultaneously and multi-cell in that direction (animated one cell per engine tick) until obstructed by a wall, another block, or the playfield border. Coloured-rim walls are passable to blocks of the matching colour and full-blocking to all others, so the same arrow press can route different-coloured blocks down different lanes. Sticky-pads catch the first block to slide ACROSS them and fix that block at the pad's cell for the rest of the level. The level wins when every coloured block sits on its same-coloured target, and loses on step-counter exhaustion or when a soft-lock is detected (the L3 sticky-pad's classic trap is orange landing on yellow's target — fired immediately, not waited out). Level progression composes the three mechanics in concert: L1 introduces the slide rule alone, L2 adds the colour-permeable rim, and L3 adds the one-shot sticky-pad whose presence fundamentally changes the planning depth — greedy-toward-target loses by trapping orange, while the witness sequence positions yellow to consume the sticky FIRST.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | UP — gravity vector (0, -1); every loose block slides upward until obstructed |
| ACTION2 | DOWN — gravity (0, +1); slides downward |
| ACTION3 | LEFT — gravity (-1, 0); slides leftward |
| ACTION4 | RIGHT — gravity (+1, 0); slides rightward |

`available_actions = [1, 2, 3, 4]` (pure cardinal motion; no click, no ACTION5, no undo).

## Levels

- **L1** introduces M1 (slide-to-end). 2 yellow blocks at lattice (1, 1) and (5, 1); 2 yellow targets at (1, 5) and (5, 5); witness `[ACTION2]`. Step budget 12.
- **L2** introduces M2 (colour-permeable rim walls). Row-3 divider with yellow-rim at (3, 3), orange-rim at (5, 3), full-block elsewhere; stop-wall at (4, 5); yellow at (3, 1), orange at (5, 1); yellow target at (1, 5), orange at (5, 5); witness `[ACTION2, ACTION3]`. Step budget 25.
- **L3** introduces M3 (one-shot sticky-pad). Row-3 divider with yellow-rim at (1, 3), orange-rim at (5, 3), full-block elsewhere; sticky-pad overlaying yellow target at (3, 5); yellow at (3, 1), orange at (5, 1), orange target at (5, 5); witness `[ACTION3, ACTION2, ACTION4, ACTION2]`. Step budget 30.

## Novelty note

- **Closest taxonomy entry**: `g50t walk-vs-scroll`. Distinguishing rule: g50t has a single avatar with one-cell-step on a scrolling board with autonomous time pressure; tg6w has multiple loose blocks with no avatar, no autonomous scroll, and a slide-to-end (multi-cell) displacement per press. Different cognitive primitives — goal-cell-reach-against-deadline vs settle-population-via-gravity-tilt.
- **Closest prior-game entry**: `zd7m cohort-step-route`. Distinguishing rule: zd7m's arrows step every pawn EXACTLY ONE cell in Manhattan-routing planning (anchors are colour-keyed step-blockers, portals teleport); tg6w's arrows slide every block ALL THE WAY UNTIL OBSTRUCTED in Sokoban-style settle dynamics, with colour-permeable rim walls (not step-blockers) and one-shot sticky-pads (not reversible portals). Different planning task: per-step coordination vs trajectory prediction with pile-up.

## Index update

One row appended to `prior-games/index.md`:

```
| tg6w | settle-pile-tilt | Settle-Pile Tilt — arrow press tilts the playfield's down direction; loose blocks slide multi-cell to settle, with colour-permeable rim walls and one-shot sticky-pads. | 2026-05-07T15:33:50Z | (autonomous) |
```

(Note: a concurrent harness run added entry `pf3w` between this run's start and finalize. Quick novelty re-check: pf3w's family is `wavefront-converge-timing` — click-driven emitters whose BFS frontiers tick on ACTION5; tg6w is pure-arrow simultaneous-slide. Different verb, different dynamic, different action subset; no novelty conflict.)
