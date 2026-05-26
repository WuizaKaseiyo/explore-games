# implement-summary

## Files

- `prior-games/tm5x/tm5x.py` (516 lines)
- `prior-games/tm5x/metadata.json`

## Plain-English summary of the implemented rule

A single avatar walks the playfield with arrow keys and toggles its
own polarity (hot ↔ cold) with the freedom-slot key. Each step, the
avatar's current cell and its four cardinal neighbours imprint a
polarity-driven value onto a 16×16 integer field; the field is
recomputed from scratch every step (positional, not accumulating).
Goal markers latch permanently the moment their underlying cell
shows the marker's required value. Levels add a polarity-toggle and
then movement-blocking obstacles to force routing decisions.

## Implementation notes

- `class Tm5x(NovaBaseGame)` — game class with semantic helper methods
  (`_active_pawn`, `_toggle_polarity`, `_try_move`, `_recompute_temperature`,
  `_update_field_pixels`, `_check_targets`).
- `class StepCounterHud(RenderableUserDisplay)` — depleting bar at
  display row 0.
- Sprites bank uses semantic names (`pawn_hot`, `pawn_cold`,
  `target_hot`, `target_cold`, `target_hot_satisfied`,
  `target_cold_satisfied`, `wall_insulator`, `temperature_field`),
  per `code/universal-scaffold.md` § Style rules — not the
  reference games' obfuscated tokens.
- Two-sprite swap idiom for polarity toggle (both pawn variants
  pre-placed in each level, one TANGIBLE and one REMOVED, swapped
  on toggle), per `novaengine-api.md` "Two-sprite swap" pattern.
- Three levels with grid_size (64, 64); thermal cells at 4-pixel
  stride (16×16 thermal grid); pawn / targets / walls are 4×4
  multi-pixel sprites with internal patterns satisfying
  checklist item 20.
- `available_actions=[1,2,3,4,5]` — pure cardinal + ACTION5 polarity
  toggle. No click, no undo.
- Step budgets per spec: L1=30, L2=60, L3=100.

## Smoke verifications

- AST parse: PASS (`python -c "import ast; ast.parse(open(...).read())"` clean).
- Instantiation: PASS — `Tm5x()` constructs without raising; level
  count = 3; available_actions = [1, 2, 3, 4, 5]; initial polarity = 1
  (hot); _temperature shape (16, 16); initial _temperature[8, 8] = 2
  (pawn-cell imprint correct at L1 start); _initial_target_names =
  {'target_hot'}; current_level grid_size = (64, 64).
- __pycache__ cleaned.
