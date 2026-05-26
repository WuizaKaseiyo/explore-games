# fix_implementation

## Description
Surgical fix-pass on `prior-games/<game_id>/<game_id>.py` driven by
`workspace/smoke-test-failures.md`. Read the failure list, address
each one, and re-run smoke_test.

This state does NOT regenerate the source from scratch — it edits
the existing file. If a single failure requires a broader rewrite
than surgical edits can deliver (e.g. the win predicate is missing
because the spec itself is wrong), write
`workspace/error.md` and halt the run instead of attempting a full
rewrite. Spec-level problems are caught earlier by `critique_spec`;
arriving here with one usually means the spec drifted during
`implement` and a re-run is cleaner than patching downstream.

Steps in order:

1. Read `workspace/smoke-test-failures.md` end-to-end. Each entry
   has `observed`, `threshold`, `diagnosis`, `fix-direction`.
2. For each failure, inspect the relevant section of the source
   (`prior-games/<game_id>/<game_id>.py`) and apply the smallest
   edit that resolves the diagnosis. Common patterns:

   - **CHECK_CAMERA_VIEWPORT**: add the per-level camera resize at
     the top of `on_set_level`:
     ```python
     gw, gh = level.grid_size or (64, 64)
     self.camera.width = gw
     self.camera.height = gh
     ```
   - **CHECK_SPRITE_CONTENT**: usually a sprite-placement bug —
     check `_levelN_sprites()` (or wherever sprites are placed) for
     missing entries or wrong coordinates.
   - **CHECK_ACTION_BRANCHES**: either remove the unused action ID
     from `available_actions=[...]` in `__init__`, or add the
     missing `elif self.action.id == GameAction.ACTION<N>: ...`
     branch in `step()`.
   - **CHECK_ACTION_RUNTIME**: read the offending handler in
     `step()`; the diagnosis includes the exception class. Common
     causes: unguarded attribute access on `None` (e.g. moving when
     `active_pawn is None`), index errors, missing
     `self.complete_action()`.
   - **CHECK_PALETTE_RANGE**: a sprite's pixel array contains a
     value outside [0, 15] (often `-2` from a `color_remap` target
     that should be `-1`). Locate the offending pixel array and fix.
   - **CHECK_WIN_PATH_EXISTS**: the win predicate helper is defined
     but never called from `step()`. Wire the helper into a
     `if self._check_win(): self.next_level()` branch.
   - **CHECK_LOSE_PATH_EXISTS**: typically the energy-bar exhaustion
     path is missing. Add the standard pattern, using a PRIVATE
     `_steps_used` counter incremented only inside handled-action
     branches (NOT the engine's `self._action_count`, which counts
     the implicit RESET as a step and produces a "first-frame energy
     already lost" bug — see qz73 / lq5x for the canonical pattern):
     ```python
     # in __init__ / on_set_level:
     self._steps_used = 0
     # at the end of each handled action's branch in step():
     self._steps_used += 1
     # in step() after action handling:
     if self._steps_used >= self.max_steps:
         self.lose()
         self.complete_action()
         return
     ```
   - **CHECK_CAMERA_DEFAULT**: same as CHECK_CAMERA_VIEWPORT.

3. After all edits, re-run the runtime smoke from `implement` step
   5 (`g = <PascalClass>()`) to confirm the source still
   instantiates and `__init__` raises no exception.
4. Clean up any `__pycache__` directories created during the
   smoke-test or the post-edit instantiation:
   ```bash
   find prior-games/<id> -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
   ```

## Skills
- skills/global
- skills/code

## Next States

### smoke_test
**Condition:** All entries in `workspace/smoke-test-failures.md`
have been addressed by edits to
`prior-games/<game_id>/<game_id>.py`, AND the source still parses
and instantiates.
**Deliverables:**
- workspace/fix-revisions.md: numbered list, one entry per failure
  in `smoke-test-failures.md`. For each entry: which check, what
  edit was applied (a short description plus the function/line
  range touched).
