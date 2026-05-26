# Step #06: smoke_test

## Inputs Consumed
- `prior-games/qz73/qz73.py` (the game source).
- `workspace/mechanic-spec.md` (for visual-sanity comparison).
- `skills/code/smoke-test-checks.md` (8 universal checks + the
  custom-check template).
- `novaengine` library (live import).
- Three rendered PNGs at `workspace/smoke-frames/level_*.png`
  (produced by the smoke run itself; viewed by Read for the
  visual-sanity pass).

## Deliverables Produced
- `workspace/smoke-test-custom.py` (canonical filename per state spec).
- `workspace/smoke_test_custom.py` (importable Python sibling — same
  content, dash-replaced underscore so `import smoke_test_custom`
  works without an importlib loader).
- `workspace/smoke-test-pass.md` (results table).
- `workspace/smoke-frames/level_{1,2,3}.png` (rendered initial
  frames per level).

## Notes
- All 8 universal checks PASS.
- All 4 custom checks PASS.
- Visual sanity PASS for all 3 levels — initial frames match the
  spec's slot/colour layout.
- Authored 4 custom checks (the maximum the state allows): one per
  essential mechanic invariant (rotation, lock-toggle,
  locked-tip-immobility, L1 minimal-solve drives next_level). Each
  uses ≤ 2 setup actions and a single boolean assertion, well within
  the smoke-test-checks.md hard constraints.
- The `check_locked_tip_does_not_rotate` is the most important of
  the four: if it fails, the lock mechanic doesn't work and L2/L3
  are unsolvable. It passed with `locked-slot before=0 after=0`,
  confirming that the spec's "skip-locked-slot" rotation rule is
  correctly implemented.
- `CHECK_CAMERA_DEFAULT` returned `(needs_per_level=False, has_resize=True)`
  — every level is 64×64 so per-level resize isn't strictly needed,
  but the source mutates the camera anyway (defensive style per the
  universal scaffold).
- This is visit 1/3. No transition to fix_implementation needed.
