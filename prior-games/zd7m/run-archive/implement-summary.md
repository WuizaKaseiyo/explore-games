# Implement summary — `zd7m`

## Files written

- `prior-games/zd7m/zd7m.py` — 413 lines.
- `prior-games/zd7m/metadata.json`.

## Plain-English summary of the implemented rule

A pure-arrow puzzle: every press of an arrow attempts to step
every movable pawn one cell in that direction simultaneously.
Pawns can be selectively held in place by static obstacle
sprites or by paired teleporter sprites that swap a pawn's
position with its partner. A run advances when every pawn
sits on a target sprite of its own colour; it ends when the
shared step counter runs out.

## Runtime checks performed

- `ast.parse` confirms valid Python syntax.
- Game class instantiates without exception.
- L1 witness (DOWN × 10) advances the engine to level 1 (L2).
- L2 witness (RIGHT × 10 + DOWN × 4) advances to level 2 (L3),
  with the anchor at (7, 10) blocking yellow's RIGHT presses
  and the anchor at (14, 7) blocking pink's DOWN presses.
- L3 witness (RIGHT × 10 + DOWN × 4) finishes with
  `GameState.WIN` — yellow teleports through portal_a at
  (4, 14) to portal_b at (17, 17) (= target_yellow); pink
  remains pinned at (14, 4) on target_pink.
