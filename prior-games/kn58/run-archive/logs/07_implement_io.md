# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (post-revision, all 18 checklist items pass).
- skills/code/universal-scaffold.md, novaengine-api.md, id-generation.md.
- skills/global/{action-enum,color-legend,paths}.md.
- 5 reference source files re-checked for house-style: cn04, sp80, sk48 (full reads from #01); sb26 partial read.

## Deliverables Produced
- `prior-games/kn58/kn58.py` (546 lines).
- `prior-games/kn58/metadata.json`.
- workspace/implement-summary.md.

## Notes
- Implementation diverged from the spec on one detail: the "click-on-existing-anchor toggles anchor off" rule was replaced with a no-op (same-cell click leaves anchor in place). Reason: the toggle made every other identical click a no-pull step, breaking the L1 witness. The simpler rule is more agent-friendly and matches reference-game conventions (no anchor-removal verb in any of the 25).
- All three levels' witnesses run cleanly to completion in the smoke test. L3 ends at `GameState.WIN`.
- Sprites use semantic names (no obfuscation, per universal-scaffold style rules).
- House-style checks: sprite bank → levels → constants → HUD widget → game class. Confirmed.
- Tag-based dispatch via `level.get_sprites_by_tag(...)` for `pawn`, `target`, `wall`, `anti_anchor`, `anchor` groups.
- Two-pass simultaneous-conflict resolution implemented per `universal-scaffold.md` § Simultaneous-conflict — fixpoint iteration to handle vacate-and-enter chains.
