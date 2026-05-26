# Game generation final report

## Generated game
- **ID**: `pf3w`
- **Source**: `prior-games/pf3w/pf3w.py`
- **Metadata**: `prior-games/pf3w/metadata.json`
- **Lines of code**: 534

## Mechanic

The player has only two verbs: a click that activates a pre-placed pulse-emitter slot in the chamber, and an `ACTION5` keypress that advances a global tick counter. Each activated emitter pushes a colored 1-cell-thick halo outward by one BFS-distance unit per global tick, curving around walls and any obstacles in its path. Target receivers — small hollow colored rings scattered in the chamber — light up on the single tick when a same-colored halo's frontier cell coincides with the target's center; the next tick the frontier has moved past and the target unlits. The level wins on the one tick when every target is simultaneously lit. Across the three levels, the player learns the place + tick verb (L1), then learns to *stagger* placements across multiple emitters so multiple halos converge at multiple receivers on the same tick (L2), and finally must factor in wall-routed BFS distance and color-keyed receivers when planning the placement-and-timing combination (L3).

## Action mapping

| Action | Effect |
|---|---|
| ACTION5 | Advance the global tick counter by 1; every active emitter's wavefront radius increments and the rendered halo trail moves outward by one cell. |
| ACTION6 | Click at (x, y) to activate the inactive slot whose 3×3 footprint covers the click — the slot's color (blue or magenta) is determined by its pre-placed color tag. |

## Levels

- **Level 1** — M1 (place emitter + tick to deliver wavefront). Single emitter, single same-colored target. Witness 9 actions. Step budget 30.
- **Level 2** — M1 + M2 (inter-emitter timing offset for simultaneous arrival). Two emitters (same color) and two targets at distinct BFS distances; player must stagger placements. Witness 10 actions. Step budget 35.
- **Level 3** — M1 + M2 + M3a (wall-routed BFS) + M3b (color-keyed targets). Two differently-colored emitters, two color-keyed targets, and a wall column with a single-row gap forcing BFS-routing. Witness 23 actions. Step budget 70.

(Witness lengths reflect the `VISIBLE_RADIUS_OFFSET=1` UX choice: clicking a slot lights only the slot's yellow center; the first `ACTION5` produces the first visible Manhattan-2 ring outside the slot's arms. Radius 1 lives under the slot's own arm cells and is intentionally hidden — the click is a clean "this thing is now active" signal without showing wavefront yet, and each `ACTION5` then visibly grows the ring outward.)

## Novelty note

- **Closest taxonomy entry**: `cd82` (orbit-fire-paint) and `sp80` (pour-shelf-route). Distinguishing rule: cd82's basket travels on a single 8-cell ring orbit and stamps a fixed half-canvas region in one shot; sp80 commits a one-shot fluid simulation that resets between commits. `pf3w`'s `ACTION5` is the only time-advancement verb, applied repeatedly to a *persistent* world state — emitters never reset, and the puzzle is precisely about how many ticks elapse between placements. No reference game has an inter-emitter timing-offset axis at all.
- **Closest prior-game entry**: `bx84` (beam-mirror-reflect). Distinguishing rule: bx84's emitter shoots a 1D directed beam that the player redirects via clickable mirrors; `pf3w`'s emitter radiates a 2D BFS-distance level-set that automatically curves around walls without mirrors, and the puzzle is the temporal stagger of multi-source convergence rather than spatial routing of a single beam. Negative-similarity walk: `pf3w` shares 2 of 8 dimensions with bx84 (both have emitters + walls; both use a step-counter HUD), well below the 3-of-8 reject threshold; the heavy-weighted dimensions (visual signature, pixel grain, core dynamic) all DIFFERENT.

## Index update

One row appended to `prior-games/index.md`:

```
| pf3w | wavefront-converge-timing | Wavefront Synchronization — click pre-placed slots to activate colored emitters; ACTION5 globally ticks each emitter's BFS-radius wavefront outward; level wins on the single tick when every same-colored target receiver coincides with a frontier cell. | 2026-05-07T15:25:50Z | (autonomous) |
```
