# Game generation final report

## Generated game
- **ID**: dj5h
- **Source**: `prior-games/dj5h/dj5h.py`
- **Metadata**: `prior-games/dj5h/metadata.json`
- **Lines of code**: 1043

## Mechanic

The avatar walks a chain of floor islands separated by pits. Above the playfield runs a horizontal beam from which one or more pulley wheels suspend pairs of coloured platforms — one platform on each side of the wheel. The two platforms on a single wheel are coupled by rope-length conservation: when one is HIGH the other is LOW, never both at once. Clicking a wheel makes it the active pulley; the freedom action then toggles that pulley, instantly inverting both platforms (carrying the avatar with whichever platform they happen to be standing on). Level 2 introduces a small carryable peg and a recessed socket: walking onto the peg picks it up, walking onto the matching socket while carrying drops it, which removes a wall blocking the goal corridor. Level 3 introduces an overhead orange cable that couples two of the three pulleys in opposite phase, so a single toggle action acts on both at once and the player must sequence the peg-drop *before* the cable-toggle.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Walk avatar 4 px in -y |
| ACTION2 | Walk avatar 4 px in +y |
| ACTION3 | Walk avatar 4 px in -x |
| ACTION4 | Walk avatar 4 px in +x |
| ACTION5 | Toggle the **active pulley** (and any cable-coupled partner) — both of its platforms swap HIGH ↔ LOW. Excluded from `_get_valid_actions()` when no pulley is active. |
| ACTION6 | Click at (x, y); if the click cell is inside any wheel's 5×5 footprint, that wheel becomes the active pulley (orange halo lights, all other halos clear). |

ACTION7 is not declared (no meaningful undo — binary toggles are self-inverse).

## Levels

- **L1** (base dynamic system): 1 pulley. Avatar boards the LOW platform, toggles, rides up to a goal at HIGH. Witness: `[ACTION6@(30,7), ACTION5, ACTION4×4, ACTION5]` (6 actions). Step budget 30.
- **L2** (+1 mechanic — peg/socket/wall): 1 pulley. Initial state requires a toggle to bridge A→B. Avatar walks across, picks up the red peg on B, drops it on a socket further along B; the wall blocking C removes; avatar continues to the goal. Witness: `[ACTION6@(10,7), ACTION5, ACTION4×14]` (16 actions). Step budget 80.
- **L3** (+1 mechanic — opposite-phase cable coupling): 3 pulleys. PA and PC are cable-coupled in opposite phase. Avatar walks across PA-blue (initial bridge), picks up the blue peg on B, returns and drops it on the PA-blue socket (wall removes), continues forward across PB-blue-clone and C, walks past the removed wall onto PC-red at LOW, then a single click+toggle on PC simultaneously raises PC-red (carrying the avatar to the goal at HIGH) and inverts PA's state. Witness: `[ACTION4×4, ACTION3×2, ACTION4×13, ACTION6@(58,7), ACTION5]` (20 actions). Step budget 150.

## Novelty note

- **Closest taxonomy entry**: `m0r0` (mirror-orb-merge). Distinguishing rule: m0r0 couples two *pawns* by mirroring arrow-input across both axes (the avatar IS the moving pair); dj5h couples two pieces of *scenery* (paired platforms) on a single vertical axis via rope-length conservation, while the avatar is a single walker who interacts with the scenery by riding it.
- **Closest prior-game entry**: `m0r0` (taxonomy) and `pn5d` / `xv2b` (vessel-equalize-flow). For pn5d/xv2b, distinguishing rule: hydrostatic equalisation across N connected vessels vs. binary-discrete rope-length conservation between exactly 2 platforms per pulley. Other near-misses (kj82, pv5q, kn58, mr5q, vt6q, wb6n, gx7m) addressed in `mechanic-pick.md` § Novelty.

## Index update

One row appended to `prior-games/index.md`:

```
| dj5h | pulley-pair-platform | Pulley-Pair Platform Walk — overhead pulleys couple paired hanging platforms; click selects, ACTION5 toggles state, peg unlocks walls, cable couples pairs at L3. | 2026-05-09T02:27:55Z | (autonomous) |
```
