# smoke_test

## Description
A deterministic post-implement battery of programmatic checks. Run
each check defined in `code/smoke-test-checks.md` (Tier 1) against
the just-generated `prior-games/<game_id>/<game_id>.py`. Each check
produces a numeric or boolean result that can be compared to a fixed
threshold; no LLM judgement is required.

The agent loads the game via:

```python
import importlib.util, sys
from pathlib import Path
src = Path(f"prior-games/{game_id}/{game_id}.py")
spec = importlib.util.spec_from_file_location(f"smoke_{game_id}", src)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GameClass = getattr(mod, PascalClassName)
g = GameClass()
```

Then runs the ten universal checks listed in
`code/smoke-test-checks.md`:

1. `CHECK_CAMERA_VIEWPORT` (camera viewport == level.grid_size per level)
2. `CHECK_SPRITE_CONTENT` (non-empty playfield per level)
3. `CHECK_ACTION_BRANCHES` (every declared action has a `step()` branch)
4. `CHECK_ACTION_RUNTIME` (each action runs without exception)
5. `CHECK_PALETTE_RANGE` (rendered pixels in [0, 15])
6. `CHECK_WIN_PATH_EXISTS` (`self.next_level()` or `self.win()` reachable)
7. `CHECK_WITNESS_WINS` (each level's named witness, replayed against
   the loaded game, advances past that level — L1's witness reaches
   L2, L2's witness reaches L3, L3's witness reaches WIN)
8. `CHECK_LOSE_PATH_EXISTS` (`self.lose()` reachable)
9. `CHECK_CAMERA_DEFAULT` (per-level camera resize when grid sizes differ)
10. `CHECK_VISUAL_SANITY` (vision pass: rendered initial frames per
    level match what the spec's `## 2. Mechanic family` and
    `## 4. Level progression …` describe — sprite count, coarse placement,
    HUD presence, no catastrophic rendering bug)

PLUS the agent authors **2-4 custom checks** specific to this
game's mechanic, following the strict template and constraints in
`code/smoke-test-checks.md` § *Custom checks (agent-authored)*. Each
custom check tests ONE essential invariant of the mechanic with ≤ 5
setup actions, ONE action under test, and ONE boolean assertion.
Common patterns (direction-press moves avatar, click-selects-sprite,
modal-action-toggles-state, action-counter-increments, lose-at-
budget, minimal-solve-wins) are documented in the same skill file.

The custom checks are written inline as Python functions in
`workspace/smoke-test-custom.py` and run alongside the universal
checks. Failures are reported under a `## Custom checks` section in
`workspace/smoke-test-failures.md` with the same four-field schema
as universal-check failures.

The full procedure for each universal check, plus the custom-check
template and constraints, is in `code/smoke-test-checks.md`.

**Maximum revision cap.** This state may be entered at most 6 times
per run. Track the visit count by reading `workspace/logs/state_log.md`
(count rows where state == `smoke_test`). On the 6th entry that
still surfaces failures, write a brief `workspace/error.md` and halt
the run instead of looping back to `fix_implementation`.

## Skills
- skills/global
- skills/code

## Next States

### finalize
**Condition:** Every universal check AND every authored custom
check returns a `PASS`-equivalent result (per the thresholds in
`code/smoke-test-checks.md`).
**Deliverables:**
- workspace/smoke-test-custom.py: 2-4 custom-check functions, one
  per essential mechanic invariant, each conforming to the template
  and constraints in `code/smoke-test-checks.md` § Custom checks.
- workspace/smoke-test-pass.md: per the schema in
  `code/smoke-test-checks.md` (one row per universal check, one row
  per custom check, one column per level where applicable).

### fix_implementation
**Condition:** At least one universal or custom check failed AND
this is at most the 5th visit to `smoke_test` (so a transition
back gives `fix_implementation` a 6th attempt before the cap fires).
**Deliverables:**
- workspace/smoke-test-failures.md: per the schema in
  `code/smoke-test-checks.md`. Each failing check has the four
  fields `observed`, `threshold`, `diagnosis`, `fix-direction`.
  Universal checks go under `## Universal checks`; custom checks
  go under `## Custom checks`.
