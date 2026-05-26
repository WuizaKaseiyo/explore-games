# Step #06: smoke_test

## Inputs Consumed
- prior-games/qb84/qb84.py (from #05 implement).
- workspace/mechanic-spec.md (from #03): for visual-sanity comparison.
- skills/code/smoke-test-checks.md: 9 universal checks + custom-check
  template.
- workspace/logs/state_log.md: visit count = 1/3.

## Deliverables Produced
- workspace/smoke-test-custom.py: 4 custom-check functions
  (check_lift_swaps_colors, check_sticky_locks_bead,
  check_pair_propagation_sets_neighbour, check_lose_at_budget).
- workspace/smoke-test-pass.md: all 9 universal + 4 custom checks PASS.
- workspace/smoke-frames/level_{1,2,3}.png: rendered initial frames.

## Notes
- File naming hyphen vs underscore: workspace/smoke-test-custom.py
  has hyphens (per state spec). Standard Python `import` doesn't
  load hyphenated filenames; `importlib.util.spec_from_file_location`
  is required to load it. Documented in module docstring.
- All 4 custom checks pass on first run.
- Visual sanity: pair-peg corner markers (palette 0 white) visible
  at sub-pixel scale in the rendered PNG; sticky-peg central hole
  (palette 4 matches background) creates a visible "donut" shape;
  target reference strip in bottom-right corner reads as a small
  horizontal sequence of bead colours.
- pycache cleaned.

