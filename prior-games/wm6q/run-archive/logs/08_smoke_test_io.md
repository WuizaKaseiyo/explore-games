# Step #08: smoke_test (visit 1/6)

## Inputs Consumed
- `prior-games/wm6q/wm6q.py` (from #07 implement)
- `mechanic-spec.md` (witness sequences for CHECK_WITNESS_WINS)
- `skills/code/smoke-test-checks.md` (10 universal-check definitions + custom-check template)

## Deliverables Produced
- `workspace/smoke-test-pass.md` — universal-check + custom-check tables, all PASS.
- `workspace/smoke-test-custom.py` — 4 authored custom checks.
- `workspace/smoke-frames/level_{1,2,3}.png` — rendered initial frames.

## Notes
- Initial run failed CHECK_SPRITE_CONTENT because sprite.pixels was a Python list
  but novaengine's `Camera._raw_render` requires a numpy array (`.shape`). Patched
  `_paint_tile_pixels` and `_placeholder_tile_pixels` to return `np.ndarray`
  with `dtype=np.int16`; second run passed.
- Initial `check_lose_at_budget` failed because clicking a single tile in L1
  cycled into a winning configuration (tile A at R=2 makes A.right=yellow which
  matches B.left=yellow). Switched the check to L3 where rotating one tile
  cannot satisfy the 12-internal-boundary win predicate; second run passed.
- Witness replay was successful end-to-end: L1 (2 clicks) → L2 → L3 → WIN.
- All universal checks pass; all custom checks pass. Transition to finalize.
