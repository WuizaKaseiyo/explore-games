# Step #05: implement

## Inputs Consumed
- mechanic-spec.md (full): 9 sections, sprite roster, level layouts, witness sequences
- skills/code/universal-scaffold.md (full): file structure, naming convention, `on_set_level` camera-resize, two-sprite-swap idiom, simultaneous-conflict resolution gotcha
- skills/code/novaengine-api.md (full): Sprite/Level/Camera/NovaBaseGame/RenderableUserDisplay signatures, GameAction enum, ACTION6 click → display_to_grid pattern (not used here)
- skills/code/spec-template.md (already digested in write_spec)
- skills/code/id-generation.md (re-read): metadata.json schema
- skills/global/paths.md (re-read): output path under prior-games/<id>/
- prior-games/xn5p/xn5p.py (skim): lattice-helpers, _border_walls, sprites dict, on_set_level idiom, _action_count handling
- prior-games/wt39/wt39.py (skim, lines 370-430): single-pawn slide-animation pattern (`_anim_queue`, mid-step return without complete_action) — adapted for multi-block lockstep slide

## Deliverables Produced
- prior-games/tg6w/tg6w.py (597 lines): full NovaBaseGame subclass `Tg6w`. Universal-scaffold ordering: imports → sprite bank (8 sprite kinds + 8 named pixel-matrix constants) → lattice helpers + 3 levels with explicit sprite lists → constants (palette, stride bounds, action deltas) → `StepCounterHud` → `Tg6w` class.
- prior-games/tg6w/metadata.json: schema-conformant.
- implement-summary.md: paths + LOC + witness verification.

## Notes
- All per-level state attributes initialised BEFORE `super().__init__()` to avoid the post-super-overwrite bug noted in lv4k / xn5p mechanism-details.
- Step counter uses a private `self._steps_used` (not `self._action_count`) per the canonical fix-implementation guidance — avoids the "first-frame energy already lost" RESET-counts-as-step bug.
- Slide animation: simulation precomputed via `_compute_slide_animation`; result is a list of frames, each a list of `(block, new_x, new_y, sticky_cell_or_None)` tuples. `step()` plays one frame per engine tick without calling `complete_action`; final tick triggers `_finalise_action` which checks win/dead-end/budget then completes.
- Slide ordering: blocks furthest in the slide direction go first within each frame's per-block iteration (rightmost-first for RIGHT, etc.), avoiding the simultaneous-conflict gotcha for multi-block slides.
- Soft-lock detection (`_check_dead_end`): two failure modes — (1) a fixed block is off its same-colour target; (2) every same-colour target is occupied by a wrong-colour fixed block. Either fires `self.lose()` immediately on the turn detected, satisfying `difficulty-rules.md` § 1's "no waiting room" rule.
- Witness verification: all three levels solved on their planned sequences. Final game state after L3 witness = `GameState.WIN`.
- `__pycache__` cleaned post-test.
