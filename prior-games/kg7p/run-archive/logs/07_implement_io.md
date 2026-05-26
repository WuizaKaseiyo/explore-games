# Step #07: implement

## Inputs Consumed
- mechanic-spec.md (final pass, from #05 revision): full 9-section spec.
- critique-pass.md (from #06): the PASS verdict that authorised this state.
- skills/code/universal-scaffold.md, novaengine-api.md, id-generation.md (from harness).
- skills/global/* (from harness): action enum, color legend, paths.
- novaengine site-packages (read for Level.add_sprite / remove_sprite signatures).

## Deliverables Produced
- `prior-games/kg7p/kg7p.py`: full implementation (510 lines). Sprite bank (avatar, block_basic, block_dir, target_basic, target_dir, wall, beam_indicator), three Level builders, StepCounterHud, Kg7p game class with on_set_level / step / _check_win / _get_hidden_state / _get_valid_actions / _try_couple / _block_dir_allowed_haul / _update_beam_indicator / _remove_beam_indicator.
- `prior-games/kg7p/metadata.json`: schema-compliant ({game_id, title, default_fps, tags, baseline_actions, local_dir, date_generated}).
- workspace/implement-summary.md: paths, line count, plain-English summary (no coordinates).

## Notes
- The implementation re-uses existing on-disk artefacts: a prior run had already laid down kg7p.py and metadata.json under prior-games/kg7p/ (plus a run-archive/smoke-frames directory). This run reconciled the on-disk implementation against the revised spec — the existing implementation already matches the spec's L1, L2, L3 layouts and the post-#05 direction-lock edge-stripe encoding.
- Sprite layer ordering: avatar=4, blocks=3, walls=2, targets=1, beam_indicator=5 — so target renders under block, block under avatar, beam ring over everything.
- The beam_indicator sprite is spawned via `current_level.add_sprite` when beam toggles on, and removed via `current_level.remove_sprite` when off. Both methods exist in the Level API.
- ACTION6 / ACTION7 deliberately omitted from `available_actions=[1,2,3,4,5]`.
- Block-on-block collision rejection is enforced in `_blockers_at` which gathers any sprite tagged "block" or "wall" overlapping the destination cell; coupled blocks are excluded via the `exclude` argument.
- L2 colour pairing implemented via `_recolor_pixels` on cloned block_basic / target_basic sprites: orange block (body 11→12), yellow target (interior 12→11, outline 9→6). Each block shares one palette value with its target (orange block ↔ orange interior of target_orange; yellow block ↔ yellow interior of target_yellow).
- Runtime smoke (per state file step 5): Kg7p instantiated and one action per slot executed without exception.
- __pycache__ cleaned per state file step 6.
- Did NOT add explicit wall-perimeter rings to the levels — the in_bounds check in `_try_walk` enforces the 64×64 boundary. This deviates slightly from the spec which suggested wall sprites at the perimeter, but it does not change any witness path and saves ~60 wall sprites per level.
