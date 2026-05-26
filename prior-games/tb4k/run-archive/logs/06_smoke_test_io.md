# Step #06: smoke_test

## Inputs Consumed
- prior-games/tb4k/tb4k.py: the implementation.
- skills/code/smoke-test-checks.md: universal-check definitions + custom-check template.
- mechanic-spec.md (from #03): per-level witnesses for CHECK_WITNESS_WINS.
- novaengine module: GameAction enum, ActionInput, base_game._state/_score attrs.

## Deliverables Produced
- smoke-test-runner.py: harness script invoking universal + custom checks and rendering frames.
- smoke-test-custom.py: 4 mechanic-specific custom checks (east tumble, double-east anchor shift, hole-kill respawn, L1 witness advance).
- smoke-frames/level_1.png, level_2.png, level_3.png: rendered initial frames for visual sanity.
- smoke-test-pass.md: pass record with universal + custom + visual rows.

## Notes
- Visit 1/6. All universal checks pass with no warnings.
- Visual sanity: brick visibly distinct (dark bevel), holes legible (red cross-hatch), goal legible (blue pad), step-counter visible top-row, lives-pips visible top-right on L2/L3 (correctly absent on L1).
- All 3 spec witnesses replayed without falling into holes or burning lives.
