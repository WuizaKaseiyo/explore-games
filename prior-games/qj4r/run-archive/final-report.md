# Game generation final report

## Generated game
- **ID**: qj4r
- **Source**: `prior-games/qj4r/qj4r.py`
- **Metadata**: `prior-games/qj4r/metadata.json`
- **Lines of code**: 435

## Mechanic
The active playfield is a coloured rectangular sheet, initially 8×8 logical cells centred in the 64×64 frame, holding orange/purple "dot" pieces and same-coloured "ring" targets. A cardinal arrow folds the sheet along its central horizontal or vertical axis over a 4-frame animation: pieces on the pressed half visibly travel toward their reflected cells while the folded-out half tints maroon ("lifting"); on the snap frame, the active region halves and the lifted half retires into the dim grey padding. **Targets are anchored** — they don't reflect with folds. If a fold retires a target's cell into padding, the target is destroyed and the level loses immediately (the only failure path beyond step-budget exhaustion). Two same-colour pieces that meet at one cell *merge* into a single maroon-rimmed piece. The level wins when every coloured piece sits on its same-coloured target with per-colour counts matching. Levels: L1 trains the fold + lose-on-retired-target; L2 adds same-colour merge; L3 adds a second colour group with its own anchored target.

## Action mapping
| Action | Effect |
|---|---|
| ACTION1 | Fold top half onto bottom (kept = bottom; pieces in top y reflect across central horizontal axis) |
| ACTION2 | Fold bottom half onto top (kept = top) |
| ACTION3 | Fold left half onto right (kept = right; pieces in left x reflect across central vertical axis) |
| ACTION4 | Fold right half onto left (kept = left) |

## Levels
- **Level 1** (M1 fold-mirror-translate, anchored target): single orange piece at logical (1, 1) + anchored orange target at (6, 6). The player must do one x-fold and one y-fold (witness `[ACTION3, ACTION1]` or symmetric `[ACTION1, ACTION3]`); ACTION2 or ACTION4 as a first action retires the target's row/column → instant lose. Step budget 10.
- **Level 2** (M1 + M2 same-colour-piece-merge, anchored target): two orange pieces at (1,4) and (6,4) + anchored target at (5,4). Witness `[ACTION3, ACTION4]` merges the oranges then lands the merged piece on the target. Step budget 14.
- **Level 3** (M1 + M2, second colour added): two oranges + anchored target_O at (5,4); purple at (2,1) + anchored target_P at (5,1). Witness `[ACTION3, ACTION4]` is unique among 2-step paths — every other 2-step sequence retires at least one of the two anchored targets. Step 1 merges oranges and lands purple on target_P; step 2 lands the merged orange on target_O. Step budget 22.

## Novelty note
- **Closest taxonomy entry**: `ar25 (shape-mirror-cover)`. Distinguishing rule: ar25 has a permanent floating mirror line and a continuously-projected ghost; the playfield never shrinks. qj4r's central-axis fold IS the mechanic, the playfield contracts irreversibly per fold, and pieces transform (merge / cleanup) under additional rules layered on the reflection.
- **Closest prior-game entries**: `bx84` (beam-mirror-reflect), `wt39` (glide-deflect-thaw), `tg6w` (settle-pile-tilt), `pz4t` (anchor-pivot-place), `qm4t` (convex-pen-trap). None contracts the playfield via central-axis reflection; none uses cardinal-arrow folds as the sole verb; none combines reflection with same-colour piece-merge and decoy cleanup.

## Index update
One row appended to `prior-games/index.md`:

```
| qj4r | fold-mirror-pair | Fold-Mirror Pairing — cardinal arrows fold the active sheet across its central axis; same-colour pieces merge on coincidence; grey decoy is removed when overlapped. | 2026-05-08T01:18:17Z | (autonomous) |
```
