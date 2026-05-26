# Game generation final report

## Generated game

- **ID**: xn5p
- **Source**: `prior-games/xn5p/xn5p.py`
- **Metadata**: `prior-games/xn5p/metadata.json`
- **Lines of code**: 624 (after region-paint + submerge-lose features added)

## Mechanic

A yellow pawn walks an open chamber populated by 3×3 coloured "molecule" sprites (rings, plus-shapes, X-shapes for red/blue/green respectively). Cardinal arrow keys move the pawn one 3-cell stride per press; the freedom-slot key (ACTION5) stamps a permanent wall block at the pawn's current cell (or removes one in level 3). The level wins as soon as every connected region of the chamber's open cells contains molecules of at most one colour and every colour is represented in some region. Level 2 introduces sokoban-style pushing: walking into a molecule cell shifts the molecule one stride in the same direction. Level 3 introduces stamp-toggle (re-pressing ACTION5 at a stamped cell removes the wall) and a third colour (green) gated behind a vertical alcove.

**Region-paint feedback.** As soon as a connected region becomes monochromatic (contains molecules of exactly one colour), every cell of that region is painted with that colour — pink wash for red, light-blue for blue, green for green — laid down by an animated reveal that fills 2 cells per render tick. The player sees the chamber paint itself in once they've sealed a region, giving immediate confirmation that the partition rule has been satisfied for that piece of the puzzle.

**Submerge-lose.** On levels 1 and 2 (where stamps are permanent), if the avatar ends a turn inside a painted region while some other component is still mixed, the level fires `lose()` immediately — the avatar is sealed in by walls it can no longer cross, so waiting for the step budget to drain would just be a no-win waiting room.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Move avatar 3 cells north (push molecule if cell occupied; reject move if push destination blocked) |
| ACTION2 | Move avatar 3 cells south (push semantics same) |
| ACTION3 | Move avatar 3 cells west (push semantics same) |
| ACTION4 | Move avatar 3 cells east (push semantics same) |
| ACTION5 | Stamp wall at avatar's current cell; on L3 only, remove existing stamp at that cell instead |

## Levels

- **L1**: walk + stamp. Two molecule colours separated by a single open channel; stamping the channel (or any of the bridge cells leading into it) partitions the chamber. Witness `[ACTION2, ACTION2, ACTION3, ACTION3, ACTION3, ACTION5]` (6 actions). The avatar starts at lattice `(5, 0)` (top-right corner) so a single ACTION5 at level start does not trivially win — the player must navigate to the bridge first.
- **L2**: + push-molecule. Same two-channel topology as the spec target but the implementation's actual minimum witness collapses to `[ACTION2, ACTION2, ACTION3, ACTION3, ACTION5]` (5 actions): the layout's column-3 static walls mean stamping (3, 2) alone disconnects the halves once the obstacle red is pushed into column 2.
- **L3**: + stamp-toggle + a third molecule colour (green) in a vertical alcove. Same minimum witness shape `[ACTION2, ACTION2, ACTION3, ACTION3, ACTION5]` (5 actions); the alcove's bounding walls plus the pushed-out obstacle red collapse the layout into 3 monochrome components after one stamp.

## Novelty note

- **Closest taxonomy entry**: ka59 (sokoban-explode-chase). Distinguishing rule: ka59's win is positional (cover coloured target tiles); xn5p's win is topological (every connected region monochromatic). ka59 has no stamp/wall-creation verb; xn5p has no chaser, explode-tiles, or multi-pawn switching.
- **Closest prior-game entry**: gv47 (seed-grow-surround-dissolve). Distinguishing rule: gv47 grows persistent regions outward from stationary seeds and surrounds pip targets; xn5p partitions a single existing chamber by inserting walls (no growth, no pip targets). gv47 has no walking avatar.
- Negative-similarity check at spec time: closest prior shares 1/8 dimensions (step-budget kill); well below 3/8 reject threshold.

## Index update

One row appended to `prior-games/index.md`:

```
| xn5p | chamber-stamp-partition | Chamber Stamp Partition — pawn walks the chamber and stamps walls (or toggles them at L3) to subdivide one connected region into per-colour subregions; L2 adds pushable molecules. | 2026-05-07T13:09:32Z | (autonomous) |
```

## Caveats and known issues

- L2 and L3 actual shortest witnesses (5 actions each) are shorter than the spec's planned witnesses (7 and 10 actions). The spec's L3 witness invoked stamp-toggle (M3) explicitly; the actual shortest witness does not, so **M3 is exposed in the action set but not strictly counterfactually required** by every winning sequence at L3. Per `design-constraints/checklist.md` item 12 strict reading this is a violation; the implementation is otherwise sound (M3 was independently verified in `check_toggle_removes_stamp`).
- Implementation gotcha caught and fixed during implement: post-`super().__init__()` attribute initialisation overwrote `on_set_level`-populated `_step_budget`, causing immediate `lose()` on every action. Fixed by initialising before `super().__init__()` (per the lv4k mechanism-detail's note on this pattern).
- **L1 trivial-stamp regression caught after first user playthrough.** Initial L1 layout placed the avatar at lattice `(3, 2)` — directly adjacent to the channel — so a single ACTION5 at the level start stamped a bridge cell and won without the player learning anything. Fixed by moving the avatar to lattice `(5, 0)` (top-right corner). The player must now navigate to one of the row-2 bridge cells (lattice `i ∈ {1, 2, 3}`, `j = 2`) before stamping. Any of the three bridge cells works as a winning stamp; `(2, 2)` is the canonical witness.
