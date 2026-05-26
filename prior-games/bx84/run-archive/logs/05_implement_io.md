# Step #05: implement

## Inputs Consumed
- workspace/mechanic-spec.md (the 9-section spec)
- workspace/critique-pass.md (verdict: PASS on all gates)
- skills/code/{universal-scaffold,novaengine-api,id-generation,spec-template}.md
- skills/global (recall from #01)
- novaengine package source at .venv/lib/python3.12/site-packages/novaengine/ (consulted Sprite + Camera + NovaBaseGame signatures + how `perform_action` dispatches `_set_action` then `step`)

## Deliverables Produced
- prior-games/bx84/bx84.py (384 lines).
- prior-games/bx84/metadata.json.
- workspace/implement-summary.md.

## Notes
- AST-parse OK and runtime smoke-test OK on instantiation + the spec's witnesses for all 3 levels (L1, L2, L3 each won by their respective witnesses).
- L3 adjacent-swap breakage verified at runtime: the 2-click witness (place mirror, then toggle prism) wins; the swapped sequence (toggle prism, then place mirror) leaves target_yellow_south unlit and requires a 3rd click to recover. This confirms the spec's planning-depth claim (item 18 / commute test) is genuine, not just hypothetical.
- Layer ordering: beam_overlay runs at layer 10 so it renders above 1×1 mirror/filter/prism cells but only paints non-(-1) pixels (`Camera._raw_render` skips transparent), so underlying sprites remain visible at their cells.
- Used a custom `_sprite_at` helper that does bounding-box hit-testing across all sprites (excluding beam_overlay). This sidesteps the engine's PIXEL_PERFECT default for 3×3 hollow-ring targets, ensuring beam paths through the transparent centre cell are recognised as "visiting the target" and clicks anywhere in the ring's bounding box no-op (rather than placing a mirror inside the ring).
- Naming convention: meaningful semantic names throughout (per universal-scaffold.md § Style rules) — sprite keys (`emitter`, `mirror_bs`, `mirror_sl`, `filter`, `prism_es`, `prism_en`, `target_*`), helper class (`StepCounterHud`), helper methods (`_handle_click`, `_trace_beam`, `_sprite_at`).
- No surface comments revealing the mechanic intent. The module docstring is `"""bx84."""`. Internal comments explain algorithmic decisions but not "what the player must do".
