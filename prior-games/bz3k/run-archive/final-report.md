# Game generation final report

## Generated game
- **ID**: bz3k
- **Source**: `prior-games/bz3k/bz3k.py`
- **Metadata**: `prior-games/bz3k/metadata.json`
- **Lines of code**: 605

## Mechanic
A single orange avatar carries persistent integer cardinal velocity
`(vx, vy)` that survives between turns. Each arrow press applies a
±1 impulse to the matching velocity component, then the avatar slides
per-axis (horizontal first, then vertical), one cell at a time, with
collision: walls stop motion and zero the matching velocity component;
the destination latches only on **speed-zero arrival** (vx == vy == 0
in the target cell). L1 is an open arena where the player learns the
impulse-and-slide rule and discovers that the target requires zero
velocity. L2 introduces a **velocity cap-band** in a wall-column
passage that clamps speed to magnitude 1 on traversal; the avatar
starts off-axis from the passage so the player must first turn
vertically to line up before drifting east through the cap. L3 keeps
the same toolset (drift-impulse + cap-band, no new tile mechanic) and
sets it inside an open arena with sparse scattered obstacle blocks
plus one central 8×8 blocker that splits the direct east path; the
player drifts east through the cap, then detours vertically around
the blocker and re-aligns onto the target row with vx=vy=0.

## Action mapping
| Action | Effect |
|---|---|
| ACTION1 (UP) | `vy -= 1`, then per-axis slide |
| ACTION2 (DOWN) | `vy += 1`, then per-axis slide |
| ACTION3 (LEFT) | `vx -= 1`, then per-axis slide |
| ACTION4 (RIGHT) | `vx += 1`, then per-axis slide |

## Levels
- **L1** — base mechanic: drift-impulse with speed-zero target in an open arena. 10-action witness; step budget 30.
- **L2** — adds **velocity cap-band** in a wall-column passage; avatar starts off-axis (south of the gap) so the player must build vy first to line up before drifting east through the cap. 21-action witness; step budget 60.
- **L3** — same mechanic set as L2 (no new tile type) reused inside an **open arena with sparse scattered obstacle blocks** plus one central 8×8 blocker that forces a vertical detour past the cap. 33-action witness; step budget 60.

## Novelty note
- Closest taxonomy entry: **m0r0 (mirror-orb-merge)**. Distinguishing rule: m0r0 has 2-4 paired orbs that move single-cell-per-action with mirror-axis transformations and reset to rest between actions; bz3k has one avatar with cumulative multi-cell-per-action persistent velocity.
- Closest prior-game entry: **wt39 (glide-deflect-thaw)**. Distinguishing rule: wt39 fires a one-shot glide per arrow press whose velocity resets to zero between actions; bz3k accumulates persistent two-axis velocity across actions, so successive arrows compound into faster motion rather than firing separate slides.

## Index update
One row appended to `prior-games/index.md`:

```
| bz3k | drift-impulse-cardinal | Drift-Impulse Cardinal — single avatar with persistent integer cardinal velocity that arrows ±1 impulse; cap-bands clamp speed; flipper-plates negate. | 2026-05-09T02:18:02Z | (autonomous) |
```
