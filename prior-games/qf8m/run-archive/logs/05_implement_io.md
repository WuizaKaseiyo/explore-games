# Step #05: implement

## Inputs Consumed
- mechanic-spec.md (from #03 / #04)
- skills/code/{universal-scaffold, novaengine-api}.md
- game_sources_3_lvls/cn04/65d47d14/cn04.py (style reference; full source)
- skills/global/action-enum.md (action subset = [6])

## Deliverables Produced
- prior-games/qf8m/qf8m.py (545 lines)
- prior-games/qf8m/metadata.json
- workspace/implement-summary.md

## Notes
- `_levels` is the engine attribute, not `levels` (small drift from the
  state's example check; substantive smoke tests below worked fine).
- All 3 witnesses verified via direct step() simulation: L1 (2 clicks),
  L2 (3 clicks), L3 (4 clicks) each produce the exact target pattern
  and `_check_win()` returns True.
- Sprite naming is fully semantic — no obfuscation: `rook_template`,
  `bishop_template`, `tristate_template`, `target_template`,
  `StepCounterHud`, `_flip_rook`, `_flip_bishop`, `_cycle_one`,
  `_check_win`, `_handle_click`, `_update_cell_visual`,
  `_update_target_visual`. Class name is Pascal-case of game id (`Qf8m`).
- HUD uses the universal "depleting bar on row 63" idiom (StepCounterHud
  subclass of RenderableUserDisplay).
- Tag-based grouping: cells tagged `cell` + sub-tag (`rook`, `bishop`,
  `tristate`); target mini-tiles tagged `target_cell`. Used in
  `on_set_level` for O(N) per-level setup.
- Click rule dispatch: cell kind read from sprite tags at level-build
  time, cached in `_cell_kind`, used by `_handle_click` to pick
  `_flip_rook` / `_flip_bishop` / no-op (tri-state click).
- `_get_valid_actions` enumerates 25 ACTION6 candidates at cell
  centres so an external agent has a tabular click vocabulary.
