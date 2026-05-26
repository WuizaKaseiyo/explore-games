# Step #09: implement

## Inputs Consumed
- mechanic-spec.md (final, after critique-pass): full 9-section spec.
- critique-pass.md (from #08): all 21 checklist items PASS, NOVEL on both axes.
- skills/code/universal-scaffold.md, novaengine-api.md, id-generation.md.
- Live novaengine source at `.venv/lib/python3.12/site-packages/novaengine/{base_game,sprites,level,camera}.py` for API-signature verification.

## Deliverables Produced
- prior-games/jx5k/jx5k.py: 644 lines, semantic naming throughout, follows universal scaffold (constants → sprite templates → helpers → layouts → level builder → HUD → game class).
- prior-games/jx5k/metadata.json: schema-compliant.
- workspace/implement-summary.md: paths, line count, 3-witness verification.

## Notes
- All 3 spec witnesses verified end-to-end (L1 8 actions → next_level; L2 20 actions → next_level; L3 16 actions → WIN). The implementation matches the spec faithfully.
- Used `Sprite(x=, y=, ...)` constructor kwarg for placement (cleaner than calling `set_position` after construction).
- `_get_valid_actions` gates ACTION5 hidden at L1 by checking `self._current_level_index == 0`.
- Two-sprite-swap idiom used throughout: node colour variants (3 per node, 1 TANGIBLE), pip slots (2 per slot — empty + filled), edge strands (per-pair, per-multiplicity-index).
- Edge sprite hit-test in `_find_edge_at` checks the actual line pixel (not just the bbox) so clicking inside the bbox of a diagonal edge but on a transparent cell does NOT match — only clicks on the line itself match.
- `_line_passes_through_other_node` uses the node sprites' rendered bounding boxes (via `sprite.x/y/width/height`) to determine obstruction; verified at L2 that the n0–n2 chord through n4 is correctly rejected by Bresenham overlap with n4's body.