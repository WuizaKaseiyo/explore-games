# Step #08: smoke_test (visit #1)

## Inputs Consumed
- prior-games/wj7d/wj7d.py
- prior-games/wj7d/metadata.json
- skills/code/smoke-test-checks.md (Tier 1 + custom-check templates)
- mechanic-spec.md (for witness sequences and per-level descriptions)

## Work
- Wrote `smoke_test_custom.py` with 4 custom checks:
  arrow-moves-selected-stamp, click-selects-stamp-at-l2,
  fold-consumes-stamp, collision-blocks-stamp-into-other.
- Wrote `_smoke_runner.py` to drive all 10 universal checks +
  the 4 custom checks.
- All 30 reported checks PASS (29 PASS + 1 RENDERED for vision).
- Rendered the 3 initial-state PNGs to
  `workspace/smoke-frames/level_*.png`.
- Visually inspected all 3 PNGs:
  - All show a green HUD bar at row 0 (step counter).
  - All show a white horizontal crease bisecting the playfield.
  - L1 shows 1 stamp + 1 shadow + halo (auto-selected).
  - L2 shows 2 stamps above crease + 2 shadows below + no halo.
  - L3 shows the deliberately-asymmetric layout that requires
    crease re-orientation to V to solve red.
  - No symbols, letters, digits, or culturally-loaded clipart.
  - No catastrophic rendering bugs.

## Deliverables Produced
- workspace/smoke-test-custom.py (and identical
  smoke_test_custom.py for import)
- workspace/_smoke_runner.py
- workspace/smoke-test-pass.md
- workspace/smoke-frames/level_1.png, level_2.png, level_3.png

## Notes
- The implementation passed every check on the first visit; no
  loop back to fix_implementation needed.
- The CHECK_WITNESS_WINS check translated all three witnesses
  from the spec verbatim and confirmed they each advance the
  game state correctly.
