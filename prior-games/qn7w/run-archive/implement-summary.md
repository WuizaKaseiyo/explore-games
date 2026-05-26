# Implement summary — qn7w

## Files
- `prior-games/qn7w/qn7w.py` — 648 lines.
- `prior-games/qn7w/metadata.json` — schema-conformant.

## Smoke results
- `python -c "import ast; ast.parse(open(...))"` → parse OK.
- `Qn7w()` instantiated; 3 levels detected; `available_actions = [6]`.
- L1 witness: 1 click → terminal ball ejects → socket filled → `_check_win() == True`. ✓
- L2 witness: junction click → branch flipped to up → pusher click → up-branch terminal ejects → blue socket filled → win. ✓
- L3 witness: junctions A & B flipped → pusher A fires (1 deposit) → pusher B fires (2 deposits) → merge_pad fully filled → win. ✓
- L2 counterfactual: 8 pusher clicks without junction flip → 3 down-branch ejects consumed by wall, then 5 no-ops → socket never fills → win never reached. ✓

## Plain-English summary of the rule
Click a button to fire a single momentum pulse along a pre-placed chain of touching round pieces; the pulse passes invisibly through the chain's body and ejects only the far-end piece by exactly one piece-width along the chain's axis. The chain's body never moves; only the chain shortens by one each click. A T-shaped switch in the middle of a chain redirects the pulse along whichever branch it currently points at; clicking the switch toggles the active branch. A special two-deposit pad accepts pieces from any chain and lights up only after two distinct ejected pieces land on it.

## Notes
- Critical bug found and fixed during smoke: `level.get_sprite_at(x, y, tag=...)` requires (x, y) to land on a non-transparent (non-`-1`) pixel of the sprite. Sprite top-left corners use `-1` for rounded silhouette, so position-based lookup at sprite top-left fails. Fixed by adding `_sprite_at_position(x, y, tag)` helper that iterates `get_sprites_by_tag(tag)` and matches on `.x, .y` directly. Used in `_fire_pulse` (terminal ball lookup) and `_process_eject` (target_socket / merge_pad lookup).
- Junction state encoded entirely in instance state (`self._chains[i]["active_branch"]`); visual cue is the junction sprite's pixel-painted tab.
- Implementation includes `_get_valid_actions` enumerating only pusher and junction centres, restricting the agent's exploration space.
