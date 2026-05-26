# Step #07: implement

## Inputs Consumed
- states/implement.md (from harness root): the 6-step procedure.
- workspace/mechanic-spec.md (v2, from #05): spec to translate.
- workspace/critique-pass.md (from #06): green-light to implement.
- skills/code/{universal-scaffold,novaengine-api,id-generation}.md (from prior steps): scaffold + API + ID rules.
- game_sources_3_lvls/cn04/65d47d14/cn04.py (from #01 study): house-style template (sprite bank → levels → constants → HUD class → game class with on_set_level/step/_get_hidden_state).

## Deliverables Produced
- `prior-games/ek73/ek73.py` (594 lines): full game source. Sprite bank with 9 sprite kinds (player, collectible, wall, wake_age1/2/3, clearer_pad, warp_pad_a/b). Three levels assembled by `_build_level_*` helpers using walkable-cell sets (`_l1_walkable`, etc.) and a `_build_walls` helper that places wall sprites at every non-walkable logical cell. `StepCounterHud` widget. `Ek73(NovaBaseGame)` class with `on_set_level` per-level state init, `step()` dispatching ACTION1-4 with: (i) wall/off-grid check (no-op), (ii) wake check (lose), (iii) move + pad effect (clearer/collectible/warp), (iv) age-then-add wake, (v) win check, (vi) soft-lock check.
- `prior-games/ek73/metadata.json`: schema-conforming.
- `workspace/implement-summary.md`: 3-5 line plain-English rule summary + line counts.

## Notes
- Parse check: PASS (`ast.parse` succeeds).
- Runtime smoke (instantiation only): PASS — `Ek73()` instantiated; `current_level` of type `Level`; `grid_size=(64, 64)`.
- step() smoke test via direct attribute setting failed because `self.action` is an engine property (not a writable attribute) — actions are injected by the engine's outer loop, not callable directly. The smoke_test state will run the game through the engine's normal action dispatch.
- Implementation deviations from spec:
  - Wake sprite spawning uses `level.add_sprite(...)` if available, else a fallback to `level._sprites.append(...)`. This may need adjustment based on the actual novaengine `Level` API; smoke_test will reveal if dynamic sprite spawning fails.
  - Co-located clearer + collectible at L3 `(8, 1)`: implemented by triggering BOTH at the same cell on overlap (clearer fires first to clear wake, then collectible is consumed).
  - Soft-lock detector treats lethal-only-wake-neighbours as soft-locked (the lose-on-wake fires before the soft-lock fires; the soft-lock branch covers the case of all-walls neighbours specifically).
- __pycache__ cleaned up.
- Transitioning to smoke_test.
