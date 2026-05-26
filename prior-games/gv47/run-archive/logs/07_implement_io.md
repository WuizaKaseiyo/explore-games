# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (post-revision).
- skills/code/{universal-scaffold, novaengine-api, smoke-test-checks}.md.
- Reference reads from #01 study (sp80, tu93, r11l) for HUD widget and step() patterns.

## Deliverables Produced
- prior-games/gv47/gv47.py (564 lines): full game class Gv47 with sprite bank, 3 levels, StepCounterHud widget, region-based growth/mix logic, _check_win, _get_valid_actions overriding to enumerate per-cell click positions.
- prior-games/gv47/metadata.json: id, title "Seed Bloom & Mix", default_fps 30, baseline_actions [5, 6].
- workspace/implement-summary.md: paths, line count, plain-English rule, runtime smoke verification log.

## Notes
- Camera resized per-level (all three are 12×12).
- Used `level.add_sprite` + `level.remove_sprite` to manage runtime paint sprites; cleared on `on_set_level` to make replays clean.
- `_get_valid_actions` enumerates ACTION5 + ACTION6 at every grid cell center to guarantee the runner can supply valid clicks at scale=5.
- Self-smoke runtime tests passed: instantiation, L1 win transition, L2 mix-to-green, L3 wind-bias growth measured at 17 cells/click vs ~12 unbiased.
