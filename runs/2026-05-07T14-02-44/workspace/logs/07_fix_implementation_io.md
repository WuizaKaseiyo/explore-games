# Step #07: fix_implementation (visit 1)

## Inputs Consumed
- workspace/smoke-test-failures.md (from #06): 7 visual-sanity failures on L3 (overlaps, OOB) + 1 custom check failure (phase-delay-tile click).
- prior-games/yf3h/yf3h.py: the implementation to edit.

## Deliverables Produced
- workspace/fix-revisions.md: numbered list of edits (L3 layout redesigned to 16×16 grid; phase_delay_tile changed from INTANGIBLE to TANGIBLE; ring_overlay sized from level grid_size instead of module constant).
- Edits to `prior-games/yf3h/yf3h.py`.

## Notes
- L3 layout fully redesigned with new Manhattan distances. The mechanic still requires M3 (without the tile, red→multi=6 and blue→multi=5 are mismatched and the multi-resonator never activates), and the tile only delays blue (its decision-tick path), not red or green.
- The ring_overlay sprite bank's initial pixels are still 12×12; `on_set_level` calls `_clear_ring_overlay` which now computes the right shape from `level.grid_size` and overwrites `ov.pixels`.
- Verified via `import ast` parse and `uv run python` instantiation; all 3 levels load cleanly.
- Visit count for fix_implementation: 1/6 (this is the first visit).
