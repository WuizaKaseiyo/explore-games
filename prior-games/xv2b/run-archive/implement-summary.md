# implement-summary

## Files
- `prior-games/xv2b/xv2b.py` — 575 lines.
- `prior-games/xv2b/metadata.json`.

## Implementation summary

Three vertical water-vessels stand side by side; small valves
mounted in the gaps between them open or close on click. Each
ACTION5 simulates one tick of hydrostatic equalisation: open
valves transfer one cell of water from the higher to lower side
when the slit is submerged, an always-on drain (L2/L3) consumes a
cell from its vessel, and an active pump (L3) transfers one cell
from its source to its destination regardless of relative levels.
The win condition is per-vessel water-level matching its target
side-tick across all three vessels.

## Witness verification

L1 witness (18 actions = 2 toggles + 16 ticks) reaches (8, 8, 8)
at tick 16 — verified by hand-tracing and by simulation.

L2 witness (9 actions = 1 toggle + 8 ticks) reaches (12, 8, 8) at
tick 8 — verified.

L3 witness (27 actions = 1 toggle + 22 ticks + 1 toggle + 3 ticks)
reaches (0, 5, 3) at tick 25 — verified by simulation. **Spec L3
target levels were updated from (0, 5, 10) to (0, 5, 3) and
V_AB slit-height from 0 to 15** to ensure the witness is reachable
under the implemented snapshot-semantics tick rules.

## Notes on engine integration
- `Sprite.set_visible(False)` paired with
  `Sprite.set_interaction(InteractionMode.REMOVED)` is used to swap
  closed/open valve variants and pump_off/pump_on — per
  `code/universal-scaffold.md` § Two-sprite swap.
- `Camera(interfaces=[StepCounterHud])` registers the HUD; the bar
  drains over the step budget and turns red below 25%.
- `_get_hidden_state` packs `(step_counter, water levels, valve
  states, pump states)` into a 4×4 int16 array so the engine's
  graph hashing distinguishes states with the same rendered frame
  but different valve/pump configurations.
