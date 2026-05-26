# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (9-section spec, post-critique-pass)
- workspace/critique-pass.md (clean critique)
- skills/code/{universal-scaffold, novaengine-api, id-generation, spec-template}.md
- workspace/mechanic-pick.md
- 5 reference-game source files (used as template guidance — sk48 for tag-based dispatch + RenderableUserDisplay HUD; cn04 for level-data dict and grid-bounds movement guard; sp80 for level-data step budget; m0r0 for InteractionMode.REMOVED on consumed sprites; sb26 for step-counter HUD subclass)

## Deliverables Produced
- prior-games/bw7k/bw7k.py (337 lines): full game source — sprite bank, 3 levels, constants, StepCounterHud (renderable user display), Bw7k class with __init__, on_set_level, helper methods (_actor, _is_blocked, _trigger_anchor_if_landed, _compute_replay_endpoint, _check_win), step, _get_hidden_state.
- prior-games/bw7k/metadata.json
- workspace/implement-summary.md (3-5 line plain-English rule summary)

## Notes
- **Mechanic implementation choice**: shade replay is resolved INSTANTLY on spawn (the entire move-tape is walked in a single `step()` call, with skip-on-block per entry). This avoids the per-tick advance ambiguity in the spec text and keeps the implementation single-tick atomic. Spec was updated in `mechanic-spec.md` to reflect the instantaneous resolution; the WIN PREDICATE is unchanged (it still checks final positions of actor + shades).
- **Style**: meaningful semantic names throughout (no obfuscated tokens) per `universal-scaffold.md` § Style rules. Class name is `Bw7k` (PascalCase of the game ID) per the only naming convention kept from reference games.
- **Verification**:
  - `python -c "import ast; ast.parse(...)"` → PARSE OK.
  - Runtime instantiation: `Bw7k()` constructed without raising; `len(g._levels) == 3`; `g._available_actions == [1, 2, 3, 4]`.
  - `__pycache__` directories cleaned up.
- Camera viewport is the engine default 64×64 because all three levels are `grid_size=(64, 64)`. No explicit `self.camera.width = ...` resize needed in `on_set_level`. (Per `universal-scaffold.md`'s Camera-viewport-must-match-level-grid_size note: "If your game has a single fixed grid_size of exactly 64×64 (like ls20), you can skip this — the default 64×64 camera matches and no scaling is needed.")
- ACTION7 omitted from `available_actions` per checklist item 22.
- `set_interaction(InteractionMode.REMOVED)` is used to consume an anchor on first trigger so it doesn't double-spawn on revisit.
