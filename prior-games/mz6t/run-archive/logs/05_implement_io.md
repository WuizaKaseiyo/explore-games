# Step #05: implement

## Inputs Consumed
- mechanic-spec.md (from #03 write_spec): 9-section spec.
- critique-pass.md (from #04 critique_spec).
- skills/code/{universal-scaffold, novaengine-api}.md (in memory).
- prior-games/qf8m/qf8m.py (read in #01 for house-style anchoring).

## Deliverables Produced
- prior-games/mz6t/mz6t.py (573 lines).
- prior-games/mz6t/metadata.json.
- implement-summary.md.

## Notes
- Followed qf8m's style: meaningful semantic sprite names (`vote_cell`, `wall_cell`, `anchor_cell`), `_build_level_sprites` helper, per-level Level construction with `data={...}` carrying initial/target/walls/anchors/step_budget, `StepCounterHud` subclass on row 62, single `step()` dispatch.
- Added `TargetPanelHud` (RenderableUserDisplay) to render the target panel without needing per-cell sprites — cleaner than placing 25 mini-sprites per level.
- `_apply_tick` reads from `old_state` snapshot, writes to `new_state`, then commits — synchronous update.
- Anchor lock is checked after every cell-state change (click + post-tick) to catch initial-state matches and tick-induced matches.
- Win check is gated on `self.action.id == GameAction.ACTION5` — clicks don't trigger win check, satisfying the spec's M2-required-by-engine design.
- Verified all 3 witnesses replay deterministically: L1 → score 1, L2 → score 2, L3 → state WIN.
- Cleaned up __pycache__ post-test.
