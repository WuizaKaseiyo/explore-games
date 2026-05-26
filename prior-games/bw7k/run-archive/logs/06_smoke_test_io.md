# Step #08: smoke_test

## Inputs Consumed
- prior-games/bw7k/bw7k.py (the implemented game)
- workspace/mechanic-spec.md (witness sequences for CHECK_WITNESS_WINS)
- skills/code/smoke-test-checks.md (the 10-check Tier 1 battery + custom-check templates)
- novaengine API (perform_action, ActionInput, GameAction, render)

## Deliverables Produced
- workspace/smoke-test-runner.py: orchestrator script that runs the 10 universal checks plus 4 custom checks against the loaded game.
- workspace/smoke-test-custom.py: 4 custom-check functions using Patterns A, C, F from `smoke-test-checks.md`.
- workspace/smoke-test-pass.md: every check PASS.
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames for visual sanity check.

## Notes
- All 10 universal checks pass.
- All 4 custom checks pass.
- Visual sanity per level confirms sprite count, sprite placement, HUD presence, no catastrophic rendering bug. The renders at workspace/smoke-frames/ match the spec's Level 1/2/3 descriptions.
- CHECK_CAMERA_DEFAULT: levels share grid_size (64, 64), so per-level camera resize is not required (default 64×64 camera matches the engine's default). Per `code/universal-scaffold.md` § Camera viewport must match level grid_size: "If your game has a single fixed grid_size of exactly 64×64 (like ls20), you can skip this — the default 64×64 camera matches and no scaling is needed."
- CHECK_WITNESS_WINS confirms each spec witness actually wins:
  - L1 (13 ACTION1): score 0→1, state NOT_FINISHED (advanced to L2).
  - L2 (RIGHT×6+UP×6+LEFT×6+UP×7 = 25 actions): score 1→2, state NOT_FINISHED (advanced to L3).
  - L3 (UP×6+DOWN+RIGHT×8+UP+UP×8+LEFT×4 = 28 actions): score 2→3, state WIN (the engine fired `self.win()` after the last `self.next_level()`).
