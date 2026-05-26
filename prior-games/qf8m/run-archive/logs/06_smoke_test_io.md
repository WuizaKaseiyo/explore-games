# Step #06: smoke_test

## Inputs Consumed
- prior-games/qf8m/qf8m.py (the implementation)
- prior-games/qf8m/metadata.json
- mechanic-spec.md (witness sequences)
- skills/code/smoke-test-checks.md (10 universal checks + custom-check template)
- workspace/logs/state_log.md (visit count = 1)

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom check functions, all passing
- workspace/smoke-test-pass.md: full check matrix
- workspace/smoke-frames/level_{1,2,3}.png: 512×512 rendered frames

## Notes
- All 10 universal checks pass on first attempt. CHECK_WITNESS_WINS
  was the most discriminating: L1 (2 clicks), L2 (3 clicks), L3 (4
  clicks) witnesses each advanced the engine `_score`, and L3's run
  reached `_state == WIN`.
- All 4 custom checks pass:
    1. rook click flips 9 cells (row+col-corner).
    2. bishop click at (1,1) in L2 flips 7 cells (main+anti-1).
    3. tri-state cycles 0→1→2 mod 3 across 2 flips.
    4. L1 witness advances level score.
- Visual sanity: PNGs render the playfield + target display + HUD as
  the spec described. The +-cross / X-cross / ring motifs read clearly
  even at 64-px native resolution, satisfying checklist 21.
- No fix_implementation loop needed.
