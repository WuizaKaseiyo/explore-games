# Game generation final report

## Generated game
- **ID**: `bw7k`
- **Source**: `prior-games/bw7k/bw7k.py`
- **Metadata**: `prior-games/bw7k/metadata.json`
- **Lines of code**: 337

## Mechanic

A small avatar walks the grid one cell per arrow press. Scattered
on the board are coloured rune-pads paired with same-coloured
hollow rings. The first time the avatar steps onto a rune-pad, a
ghostly companion of the matching colour spawns there and is
immediately seated at the cell where the avatar's recorded
walk-history would have led it from the pad — applying each move
in order, walking through walls only when free, and skipping any
step blocked by a wall or grid edge. The level resolves when the
avatar stands on its goal-frame and every spawned companion
stands on its same-coloured ring; the step counter ends the
level on a `lose()` if it empties first. Composition: L1 is the
base system (walk + anchor + replay), L2 adds replay-walls (the
shade's tape encounters walls that cause skips, so the avatar's
path-shape matters), L3 adds multi-shade simultaneity (two
colour-pairs whose tapes are in strict-prefix relation, with a
between-anchors detour wall and a second replay-wall that
together force the witness's path-shape).

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Move actor UP one cell (4 pixels). Append `(0, -4)` to the move-tape. |
| ACTION2 | Move actor DOWN one cell. Append `(0, +4)`. |
| ACTION3 | Move actor LEFT one cell. Append `(-4, 0)`. |
| ACTION4 | Move actor RIGHT one cell. Append `(+4, 0)`. |

## Levels

- **Level 1** — base system (walking + anchor-spawn-shade + shade-replays-tape). Single column layout: actor at bottom, anchor mid-bottom, target mid-top, actor-goal at top. Witness: 13 × ACTION1.
- **Level 2** — adds replay-walls. Pre-anchor path-shape includes "decoy" RIGHT/LEFT cancel-pairs whose tail-LEFTs are skipped during the shade's replay against the wall east of `target_red`, leaving the shade at the offset target. Witness: RIGHT×6 + UP×6 + LEFT×6 + UP×7 (25 actions).
- **Level 3** — adds multi-shade simultaneity. Two colour-pairs (red, yellow); a between-anchors detour wall forces the actor through a DOWN-RIGHT-UP detour whose moves are inserted into `shade_yellow`'s tape; a second replay-wall (NE of `target_yellow`) skips a tail of RIGHTs so the trailing UP seats the shade on its target. Witness: UP×6 + DOWN + RIGHT×8 + UP + UP×8 + LEFT×4 (28 actions).

## Novelty note

- **Closest taxonomy entry**: `tn36` (program-pawn-trace). Distinguishing rule: `tn36` builds the programme via explicit click-buttons in a slot tray; `bw7k` records moves implicitly from arrow-walking. `tn36` has one programmable pawn; `bw7k` has actor + autonomous shade companion(s) whose motion is derived from a frozen snapshot of the actor's prior walking history.
- **Closest prior-game entry**: `jd4q` (echo-trail-teleport). Distinguishing rule: `jd4q`'s "echo" is a fading visual record of visited CELLS that the actor can teleport back to; `bw7k`'s "shade" is a SPAWNED moving entity whose position is derived from REPLAYING the actor's recorded directions from the anchor cell.

## Index update

One row appended to `prior-games/index.md`:

```
| bw7k | actor-replay-shade | Ghost-Playback — actor walks; stepping on coloured anchor spawns a same-coloured shade that replays the actor's recent path. | 2026-05-09T02:02:36Z | (autonomous) |
```
