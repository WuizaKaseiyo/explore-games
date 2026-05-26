# Step #09: implement

## Inputs Consumed
- `workspace/mechanic-spec.md` (final from #07): the canonical 9-section spec including the corrected re-projection algorithm and the L1/L2/L3 witnesses.
- `workspace/critique-pass.md` (from #08): PASS verdict; no further revisions needed.
- `skills/code/{universal-scaffold.md, novaengine-api.md, id-generation.md, spec-template.md}`: file structure, API surface, style rules.
- `.venv/lib/python3.12/site-packages/novaengine/{sprites.py, level.py, camera.py, base_game.py}`: verified the actual signatures of `Sprite.color_remap(old, new)`, `Sprite.set_interaction(InteractionMode)`, `Level.get_data(key)`, `Camera.display_to_grid`, `Camera._calculate_scale_and_offset`, `NovaBaseGame.perform_action(ActionInput)`.
- `game_sources/cn04/65d47d14/cn04.py` and `prior-games/qz73/qz73.py`: source-code style reference for HUD widget pattern, sprite-bank layout, `_steps_used` private counter (qz73's pattern, used here so misclicks don't consume).

## Deliverables Produced
- `prior-games/kx14/kx14.py` (512 lines): full game implementation.
- `prior-games/kx14/metadata.json`: matches the harness schema (game_id, title, default_fps, tags, baseline_actions, local_dir, date_generated).
- `workspace/implement-summary.md`: paths + line count + plain-English mechanic summary + smoke-test verification log.

## Notes
- **Coordinate system resolved.** The spec's "12-cell grid" maps to a 60×60 sprite-coord camera viewport (camera.width=60, camera.height=60). At scale=1 the rendered 60×60 area sits centred in the 64×64 frame with a 2-pixel letterbox each side. Each "cell" of the spec is 5 pixels of the sprite-coord space; sprite positions and dimensions in the file are in pixels (e.g. ball at cell (3, 8) = `set_position(15, 40)`). Click-coord conversion: `display_to_grid(dx, dy) → (gx, gy)` then `cell_col = gx // 5; cell_row = gy // 5`.
- **Sprite roster.** Five sprites: `dmzpvavhuh` (float ball, default orange), `vqfwzbpxir` (anchored variant of ball), `obgtbrhmfd` (15×5 platform), `wkkqxbjzye` (60×60 water bulk; pixels mutated each frame), `xqgntpsmcy` (target ring, default green). Per-instance recolour via `clone().color_remap(old, new)`. Float/anchor pairs share a position with `InteractionMode.TANGIBLE`/`REMOVED` swap, per universal-scaffold's "Two-sprite swap" pattern.
- **Step-counter private counter.** Following qz73's pattern: `self._steps_used` is incremented only when an action did something (ACTION1/2/3/4 always; ACTION6 only on a click that lands on a ball when anchor is enabled). Misclicks and anchor-disabled L1 clicks do not consume a step. Lose check is `self._steps_used >= self._max_steps`. The HUD bar reads `max_steps - steps_used`.
- **Re-projection runs after every effective action.** Including tilts — this matches the spec's §6 algorithm. A side-effect: a ball that has been tilted into a column with no overhead platform will buoyantly rise to the new water surface. The L2 witness's intermediate position comments in the spec (e.g. "(3, 7) after the tilts") slightly mis-describe the ball's exact intermediate row (the actual sim puts it at (3, 6) due to immediate buoyancy), but the total action count and the final win state remain correct — verified by hand-simulation.
- **Witness verification end-to-end.** Ran the L1+L2+L3 witnesses (9 + 15 + 21 = 45 actions) sequentially in one Python session: `state=GameState.WIN` after action 45.
- **Cleanup.** `__pycache__` directories under `prior-games/kx14/` removed after the smoke test.
- **Style adherence.** Pascal-case class name `Kx14`, opaque sprite/HUD-class names (10-character random tokens), single-line `"""."""` docstrings, semantic helper-method names (allowed; obfuscation is a release-time pass), tag-based dispatch via `level.get_sprites_by_tag`, level-data-driven configuration via `level.get_data("WaterLevel")`, etc.
