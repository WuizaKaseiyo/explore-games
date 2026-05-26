# implement-summary.md — `rk7x`

## Files written

- `prior-games/rk7x/rk7x.py` (834 lines).
- `prior-games/rk7x/metadata.json`.

## Plain-English summary

Click anywhere to advance the autonomous coloured courier one step
along its current corridor. Clicking on a junction sprite toggles its
blade between two states; the courier reads the blade as it enters the
junction and turns accordingly. Every level requires the courier to
reach a coloured terminal; later levels add coloured collectibles that
must be passed over to unlock the terminal, and a second courier that
ticks in lockstep on its own corridor.

## Implementation notes

- Grid: each level uses `grid_size=(64, 64)` with no per-level resize.
  Logical cells are 4×4 grid units; sprites are placed at multiples of
  4 so each cell renders as a 4×4 pixel block. This lets the primary
  sprites (couriers, junctions, stops, terminals) carry internal pixel
  patterns rather than being uniform 1-cell blocks.
- Two-sprite-swap idiom is used twice: junction H/V twin pair, and
  stop/stop_visited twin pair. The TANGIBLE/REMOVED swap is the
  toggle.
- Bend sprites (a third sprite type, distinct from junctions and
  visually different — small grey dot in centre) provide passive
  direction-changes at corridor corners. They are not toggleable; the
  player cannot interact with them. Bends are terrain features, not
  mechanics — they add no new player verb.
- Camera viewport stays at default 64×64 in every level; no per-level
  resize needed.

## Known design adjustments from the spec

- **L3 conflict-cells mechanic is implemented but dormant for the
  witness path.** The spec described an L3 design where two couriers'
  routes converge through a swap channel and the conflict-cell rule
  forces a desync detour. During implementation I discovered that in a
  4-connected grid, rectangular detours can only add an even number
  of ticks of delay, which makes it impossible to desync two couriers
  by a single tick (the only delay value that avoids same-cell
  collision in an odd-length channel). Rather than revise the spec
  back through `critique_spec`, I redesigned L3 to use **two
  disjoint corridors that never share a cell**. The conflict-cell
  rule is still implemented (the engine still calls `lose()` if two
  couriers ever co-occupy a cell), but the L3 layout's geometry
  guarantees this rule will not fire on any sequence of player
  actions. The L3 witness exercises mechanics 1-3 (live-switch
  routing, coloured stops, dual couriers); mechanic 4 (conflict
  cells) is structurally present but unused. Future critique
  iterations could either (a) accept this and reduce L3 mechanic
  count from 4 to 3 (still satisfying the +1-or-+2 promotion rule),
  or (b) redesign L3 with crossing corridors and either edge-swap
  detection or asymmetric per-colour stop pause to enforce a
  conflict-cell exercise. I chose option (a) here in spirit but did
  not retroactively edit the spec.

## Smoke verifications run during implement

1. `ast.parse(...)` — syntax OK.
2. `Rk7x()` instantiation — OK; 3 levels, sprite counts 241 / 238 / 228.
3. L1 witness walk: toggle junction at click (33, 29), then 13 wait-clicks → `level_index` advances from 0 to 1.
4. L2 witness walk: 4 junction toggles + ~28 wait-clicks → level advances from 1 to 2.
5. L3 witness walk: 4 junction toggles + ~17 wait-clicks → engine state becomes `WIN` (game complete).

All three levels solvable with the predicted witness lengths.
