# Game generation final report

## Generated game
- **ID**: kp9z
- **Source**: `prior-games/kp9z/kp9z.py`
- **Metadata**: `prior-games/kp9z/metadata.json`
- **Lines of code**: 354

## Mechanic
The player drops grains onto designated source cells with click. Each cell
holds a non-negative integer count visualised as up to four sub-cell pips
inside a bordered tile. When a cell exceeds capacity it topples — its
count resets to zero and one grain is delivered to each of its four
cardinal neighbours, which can in turn topple in a deterministic cascade.
Two further cell types modulate the cascade: sinks absorb every grain
delivered to them and never re-emit, and redirectors topple at capacity
one and forward their single grain to a fixed cardinal exit. The strict
win predicate requires every cell to end at exactly its declared target
count, so over-shooting is a real failure mode. Level 1 introduces the
drop+topple base system with one source and four cardinal targets; level
2 adds sinks (two sources, two cascade footprints, four targets); level 3
adds redirectors (two sources, two redirect chains, two targets two cells
beyond their sources).

## Action mapping
| Action | Effect |
|---|---|
| ACTION6 | Click cell at `(x, y)`. If the cell is a source, drops one grain on it (and runs the cascade). Clicks on non-source cells are no-ops, but consume one step of the budget. |

## Levels
- **L1** (4×4 board, budget 8) — base dynamic system: drop + topple-on-cap-4. Witness: 4 clicks on the single source.
- **L2** (5×5 board, budget 16) — adds sink. Witness: 4 clicks each on two sources.
- **L3** (5×5 board, budget 16) — adds redirector. Witness: 4 clicks each on two sources, each topple chained through a redirector to a target two cells away.

## Novelty note
- **Closest taxonomy entry**: `dc22` (colour-cycle-walk). Distinguishing rule: dc22 cycles a global tag-group state on step; kp9z increments a per-cell counter and topples by overflow, with cascade emerging from threshold-overflow rather than from a deliberate trigger.
- **Closest prior-game entry**: `vn8d` (domino-cascade-topple). Distinguishing rules: (1) state cardinality — vn8d binary, kp9z integer 0..3; (2) trigger — vn8d one-click chain, kp9z accumulates over many drops; (3) direction — vn8d directional pillars, kp9z 4-way symmetric topple (with redirectors as a separate explicit mechanic); (4) verb cardinality — vn8d single click, kp9z many sequenced drops; (5) failure mode — kp9z has overshoot via strict win predicate, vn8d has none (toppling is monotone).

## Index update
One row appended to `prior-games/index.md` (verified by `tail -1`):

```
| kp9z | grain-accumulate-topple | Grain Accumulate Topple Cascade — click sources to drop grains; cells overflow at capacity 4 to 4 cardinals; sinks absorb, redirectors forward. | 2026-05-06T23:03:52Z | (autonomous) |
```
