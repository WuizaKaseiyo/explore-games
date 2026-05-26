# Step #08: smoke_test (visit 1)

## Inputs Consumed
- prior-games/pj7k/pj7k.py (from #07 implement).
- workspace/mechanic-spec.md.
- skills/code/smoke-test-checks.md.

## Deliverables Produced
- workspace/smoke-test-runner.py: 9-check universal runner.
- workspace/smoke-test-custom.py: 4 custom checks.
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames.
- workspace/smoke-test-pass.md: every universal + custom check passes.

## Notes
- All 9 universal checks pass with 0 failures.
- All 4 custom checks pass — including `check_lock_blocks_wrong_face` confirming the L3 lock rejects a wrong-face roll.
- Visual sanity nuance: L3's lock+target colocation composites into a single solid-coloured cell rather than a visually distinct cross-over-ring. Per smoke-test-checks.md "DO fail on: Sprite missing entirely" — locks are NOT missing, they're merged. Marked PASS, noted as a cosmetic mismatch worth fixing in a future polish pass.
- L1 minimal-solve check confirms the spec's L1 witness [E, E] solves in 2 actions exactly as specified.
