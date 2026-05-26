# Implementation summary — `bz3k`

## Files
- `prior-games/bz3k/bz3k.py` — 598 lines.
- `prior-games/bz3k/metadata.json`.

## Plain-English rule summary
A single avatar drifts on a 64×64 grid with persistent integer
velocity that survives between turns. Each arrow press applies a
±1 impulse to the matching velocity component, then the avatar
slides per-axis (horizontal first, then vertical), one cell at a
time, with collision handling. Walls stop motion and zero the
matching velocity component. Some special tiles modify velocity
when crossed (one type clamps speed to magnitude 1, another type
negates both velocity components). The destination latches only
when the avatar arrives at it with both velocity components
exactly zero.

## Smoke validation (pre-state-transition)
- `python -c "import ast; ast.parse(...)"` → SYNTAX OK.
- Instantiation: `Bz3k()` succeeds; 3 levels.
- L1 witness (10 actions, `→×5 ←×5`): avatar reaches target,
  level advances 0 → 1.
- L2 witness (13 actions, `→×13`): avatar passes cap-band, rams
  east wall, level advances 1 → 2.
- L3 witness (10 actions, `→→→←←→→←→→`): avatar uses flipper to
  reverse, threads cap-band, lands at target with vx=vy=0, game
  state advances to `GameState.WIN`.

All three witnesses match the spec; total 33 actions to beat the
game.
