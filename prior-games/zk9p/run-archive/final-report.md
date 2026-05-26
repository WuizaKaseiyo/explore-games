# Game generation final report

## Generated game
- **ID**: zk9p
- **Source**: `prior-games/zk9p/zk9p.py`
- **Metadata**: `prior-games/zk9p/metadata.json`
- **Lines of code**: 434

## Mechanic
The player walks a single magenta avatar around a small wall-bounded
arena that is also inhabited by 2-4 autonomous AI "pursuer" pawns of
distinct colours. Each pursuer follows a deterministic per-type chase
rule and steps one cell toward the avatar after every avatar action.
When two or more pursuers land on the same cell on the same tick they
all merge and disappear. A pursuer landing on the avatar's cell ends
the level. The level is won when no pursuers remain. The player's
tactical lever is timing — walking such that two pursuers'
deterministic next-tick destinations are the same cell, then stepping
away so the pursuers overshoot into one another. Levels add walls and
new pursuer types (orthogonal-axis chaser, then a phase pursuer
intangible on alternate ticks plus an ACTION5 tick-skip) so that L3
forces the player to engineer two distinct merges in concert.

## Action mapping
| Action | Effect |
|---|---|
| ACTION1 | Move avatar one cell up; advance pursuers |
| ACTION2 | Move avatar one cell down; advance pursuers |
| ACTION3 | Move avatar one cell left; advance pursuers |
| ACTION4 | Move avatar one cell right; advance pursuers |
| ACTION5 | L3: tick-skip (avatar holds, pursuers advance, 2-unit cost). L1/L2: no-op (1-unit cost) |

## Levels
- **L1** (14×14, 60-step budget) — base dynamic system: avatar walk,
  Manhattan-major chase rule on `pursuer_red` + `pursuer_yellow`,
  merge-on-collision. No walls. Witness: `[UP, UP, UP, UP]` triggers
  a 2-pursuer merge at cell (7, 5).
- **L2** (16×16, 80-step budget) — adds walls (block both avatar and
  pursuer chase) and a `pursuer_cyan` with the orthogonal-major
  chase rule (prefers minor axis). Walls force cyan to stall until
  the avatar shifts off-column, releasing it via the orth rule. Win
  requires a 3-pursuer merge.
- **L3** (18×18, 100-step budget) — adds `pursuer_green` (intangible
  to the avatar on every odd tick) and ACTION5 tick-skip. The
  corridor wall structure forces the avatar to traverse green's cell
  on an odd tick to set up two distinct merges; ACTION5 is required
  to align pursuer parities at the bait cell.

## Novelty note
- **Closest taxonomy entry**: m0r0 (`mirror-orb-merge`) shares the
  word "merge". Distinguishing rule: m0r0 merges the player's *own*
  avatars (4 of them, axis-flipped lockstep); zk9p merges *enemies*
  (autonomous AI) induced to collide by the player's bait walking.
  Subjects of merge differ; verb differs; win condition differs.
- **Closest prior-game entry**: kn58 (`anchor-pull-magnet`).
  Distinguishing rule: kn58 has no avatar — the player clicks an
  anchor and every passive pawn slides one cell toward the click.
  zk9p has an avatar (the player embodies the bait); pursuers
  compute their step toward the avatar's *current* cell every tick;
  pursuit is autonomous, not click-triggered.

## Index update
Row appended to `prior-games/index.md`:

```
| zk9p | pursuer-merge-walk | Pursuer-Merge Walk — walk an avatar to lure autonomous AI pursuers into self-collisions; merged pursuers vanish; level wins when none remain. | 2026-05-05T19:35:19Z | (autonomous) |
```
