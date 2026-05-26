# Game generation final report

## Generated game

- **ID**: nz3v
- **Source**: `prior-games/nz3v/nz3v.py`
- **Metadata**: `prior-games/nz3v/metadata.json`
- **Lines of code**: 415

## Mechanic

A central rotor pillar at the centre of a 12×12 playfield projects
a 90° lit angular sector that **auto-rotates one quadrant per
agent action** (clockwise by default). The avatar walks the
playfield with cardinal arrows; cells outside the current lit
sector are unwalkable, and stepping into a free dark cell ends
the level. The puzzle is to time arrow presses so each step's
destination is in the lit sector at that moment — riding the
rotating sector to the target. Level 2 introduces stop-tiles
that freeze rotor rotation for 4 actions (the lit-cell tint
shifts yellow → pink while frozen). Level 3 introduces a
counter-rotation switch that permanently reverses the rotor's
direction. L3's step budget is set strictly below the no-switch
clockwise-traversal path so the switch is essential — composing
M1 (sweep) + M2 (freeze) + M3 (reverse) is the only way to
reach the target.

## Action mapping

| Action | Effect |
|---|---|
| ACTION1 | Move avatar one cell up; lit-sector check at destination. |
| ACTION2 | Move avatar one cell down. |
| ACTION3 | Move avatar one cell left. |
| ACTION4 | Move avatar one cell right. |

ACTION5/6/7 deliberately omitted (the distinctive verb is the
*environmental* sweep, not a player action; ACTION7 absent per
the strict-undo rule since the game has no meaningful undo).

## Levels

- **L1**: M1 alone — rotor-sweep-walkability. Avatar (1, 1) NW → target (10, 10) SE; 18-action witness; budget 22.
- **L2**: + M2 — stop-tile freezes rotation for K'=4 actions. Walls at (4, 1)–(4, 3) force a NW detour that requires the freeze. 15-action witness; budget 26.
- **L3**: + M3 — counter-rotation switch reverses rotation direction. Walls at (3, 1)/(3, 2)/(3, 4); stop-tile at (2, 3); switch at (4, 5). The switch is essential because the no-switch clockwise traversal takes 27 actions, exceeding the 26-action budget. 15-action witness.

## Novelty note

- **Closest taxonomy entry**: `g50t (walk-vs-scroll)` — a timer-driven walking puzzle. Distinguishing rule: g50t's pressure is a unidirectional linear scroll; nz3v's is a cyclic angular sector that returns every 4 phases. Different mental model (one-shot race vs cyclical timing).
- **Closest prior-game entry**: `fz5j (phase-step-tile)`. Distinguishing rule: fz5j has independent per-cell pulse periods (the player computes `t mod period` per tile); nz3v has a single global angular phase that gates a contiguous quadrant (the player reasons about the rotor's angular position). Negative-similarity 8-dimension test: only 3 light dimensions shared (verb=walk, win=reach-target, kill=timing-fail); heavy dimensions (cast, visual signature, pixel grain, core-dynamic flavour) all diverge.

## Index update

One row appended to `prior-games/index.md`:

```
| nz3v | rotor-sweep-walk | Rotor-Sweep Walk — central rotor's auto-rotating 90° lit wedge gates walkability; stop-tile freezes rotation, switch reverses direction. | 2026-05-09T00:37:32Z | (autonomous) |
```
