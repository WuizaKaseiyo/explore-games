# Game generation final report

## Generated game
- **ID**: qz73
- **Source**: `prior-games/qz73/qz73.py`
- **Metadata**: `prior-games/qz73/metadata.json`
- **Lines of code**: 394

## Mechanic
A central hub anchors a ring of eight angular slots; some slots
hold small coloured tip-pieces and others hold matching coloured
hollow rings ("sockets"). The player has two verbs: ACTION5
advances every unlocked tip-piece one slot clockwise, with locked
tips holding their position; ACTION6 click toggles whether a tip is
locked. The level is solved when every socket-slot contains a tip
of the matching colour. Level 1 introduces rotation alone (two
ACTION5 presses align three tips with three sockets). Level 2
introduces the lock mechanic — one tip is already at its socket
and must be locked before any rotation, otherwise the rotation
moves it away. Level 3 composes both: no all-rotate-no-lock witness
exists; the player must alternate between locking aligned tips and
rotating the rest, building the solution piece-by-piece.

## Action mapping
| Action | Effect |
|---|---|
| ACTION5 | advance the rotor: every unlocked tip moves to the next slot clockwise, skipping slots held by locked tips |
| ACTION6 | click a tip's display centre to toggle its lock flag (a black-corner overlay appears when locked) |

## Levels
| Level | Mechanic introduced (or composed) | Specific challenge |
|---|---|---|
| 1 | rotation only (no locks needed) | 3 tips at slots {0, 2, 4}, 3 sockets at {2, 4, 6}, same colours; 2× ACTION5 wins |
| 2 | rotation + lock | 3 tips at {0, 3, 6}, 3 sockets at {1, 4, 6}; one tip already at its socket — must lock it first to prevent rotation away |
| 3 | composition (interleave lock + rotate) | 5 tips at {0, 1, 2, 5, 7}, 5 sockets at {0, 2, 3, 5, 6}; no single rotation aligns all sockets — solution requires alternating lock-toggles with rotations |

## Novelty note
- **Closest taxonomy entry**: ar25 (`shape-mirror-cover`) and cn04 (`nub-pair-glyph`) both use ACTION5 to rotate, but rotation acts on a *selected piece* in those games (player picks a sprite, then rotates only that one). qz73's ACTION5 rotates the WHOLE rotor as a single rigid object; the player never selects a piece to rotate. The lock mechanic — a per-tip exemption from the global rotation — has no analogue in either reference game.
- **Closest prior-game entry**: kf42 (`tether-pawn-cycle`). Distinguishing rule: kf42's verbs are click-to-select + arrow-walk + walk-on-pad-to-set-colour, with two single-cell pawns navigating a small walled arena under a Chebyshev-distance tether. qz73 has no avatar, no walking, no tether; its verbs are ACTION5-rotate-the-rotor and ACTION6-toggle-a-spoke-lock. The visual signature, palette, pixel grain, and core dynamic all diverge — the only shared dimension is the universal step-counter HUD.

## Index update
One row appended to `prior-games/index.md`:

```
| qz73 | radial-cycle-lock | Radial Tip-Lock Alignment — rotate a central rotor of coloured tips and lock individual tips to align each tip with its same-coloured socket. | 2026-04-28T22:04:02Z | (autonomous) |
```
