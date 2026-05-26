# Game generation final report

## Generated game
- **ID**: ek73
- **Source**: `prior-games/ek73/ek73.py`
- **Metadata**: `prior-games/ek73/metadata.json`
- **Lines of code**: 594

## Mechanic
A single yellow-cross avatar walks one cell per arrow-press around a walled grid to collect every orange-star target. Each cell the avatar **vacates** is left behind as a glowing magenta wake mark for K=3 turns then fades; stepping onto an active wake cell loses the level. Level 1 establishes this base dynamic — the player must plan paths whose immediate backtracks would step on their own recent footprints. Level 2 adds **clearer pads** (green-asterisk floor tiles): stepping on one instantly erases every active wake cell, letting the avatar back out of self-trapped corridors. Level 3 adds **paired warp pads** (blue-ringed tiles): stepping on a warp pad teleports the avatar to its pair-partner, with both pads then consumed; this is the only way to escape a dead-end corridor whose return is wake-blocked.

## Action mapping
| Action | Effect |
|---|---|
| ACTION1 | Move avatar one logical cell up. |
| ACTION2 | Move avatar one logical cell down. |
| ACTION3 | Move avatar one logical cell left. |
| ACTION4 | Move avatar one logical cell right. |

After every successful move, the vacated cell becomes a wake mark of age 1; existing wake ages by 1; wake of age > 3 disappears. Stepping into a wall is a no-op (step counter still ticks). Stepping into an active wake cell triggers `self.lose()`. Pad effects fire on stepping onto a pad cell.

## Levels
- **L1** — base wake-trail mechanic; T-shape playfield (2-wide horizontal corridor + 1-wide vertical arm); two collectibles forcing a row-3 → row-4 detour around fresh wake.
- **L2** — adds wake-clearer pad on a 1-cell branch off a 2-wide corridor; one collectible is reachable only by exit-via-clearer + west on row 5.
- **L3** — adds paired warp pads on side cells; T-junction with three collectibles at branch ends; clearer co-located with the top collectible to escape the chimney; warp pair is the only escape from the west-corridor dead-end.

## Novelty note
- **Closest taxonomy entries**: g50t (ghost-replay), sk48 (paired-snake-trail), with concrete distinguishing rules in `workspace/mechanic-pick.md` § Similarity check (g50t = commit-then-replay-ghost vs ek73's continuous decay; sk48 = permanent symmetric-trail-match vs ek73's single-avatar self-evading temporary trail).
- **Closest prior-games entries**: fz5j (phase-step-tile), wt39 (glide-deflect-thaw), zd7m (cohort-step-route). Distinguishing rule for fz5j: bad cells are externally-clocked (per-tile period set by level layout) vs ek73's player-created wake. wt39 is glide-until-wall with permanent thaw-cracks vs ek73 step-one-cell with temporary decay. zd7m moves every pawn lockstep vs ek73's single-avatar.

## Index update
Appended one row to `prior-games/index.md`:

```
| ek73 | wake-trail-evade | Wake-Trail Evade — avatar walks one cell per arrow-press; vacated cells become decaying hazards behind the player; clearer pads erase wake; warp pads teleport in pairs. | 2026-05-07T20:59:16Z | (autonomous) |
```
