# Step #01: study

## Inputs Consumed
- task-overview.md (from harness): workflow framing, FSM, HITL=not-allowed
- states/study.md (from harness): study instructions
- skills/global/{action-enum,color-legend,paths}.md
- skills/conventions/{from-tech-report,cross-cut-frequencies,reference-game-patterns}.md
- skills/design-constraints/{core-knowledge-priors,forbidden-elements,composition-and-tutorial,checklist,difficulty-rules}.md
- skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check,prior-games-index-format}.md
- skills/mechanism-details/<id>.md for all 25 reference games (ar25, bp35, cd82, cn04, dc22, ft09, g50t, ka59, lf52, lp85, ls20, m0r0, r11l, re86, s5i5, sb26, sc25, sk48, sp80, su15, tn36, tr87, tu93, vc33, wa30)
- prior-games/index.md (27 priors: kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, ng52, pj7k, pz4t, vn8d, fz5j, kn58, bx84, wt39, zk9p, rk7x, gx7m, vp6h, kp9z, zd7m, lv4k, xn5p, mr5q, pf3w, tg6w; latest tg6w 2026-05-07T15:33:50Z)
- 5 reference source files (different action-family slots):
  - game_sources_3_lvls/cn04/65d47d14/cn04.py — full (620 lines, click+arrow+ACTION5 rotate-jigsaw)
  - game_sources_3_lvls/cd82/fb555c5d/cd82.py — full (677 lines, full keyboard+click stencil-paint)
  - game_sources_3_lvls/wa30/ee6fef47/wa30.py — full (839 lines, arrow+ACTION5 carry-pickup)
  - game_sources_3_lvls/tr87/cd924810/tr87.py — class+step+rule-engine (lines 400-696, arrow-only cycle)
  - game_sources_3_lvls/sb26/7fbdac44/sb26.py — class+step+phase-engine (lines 400-827, click+ACTION5+undo mastermind)

## Notes

Key patterns absorbed:
- `Sprite(pixels=[[..]], name=..., tags=[..], collidable=, visible=, layer=)`; `-1` is transparent.
- Levels declared as `Level(sprites=[s.clone().set_position(x,y).color_remap(...).set_rotation(...)], grid_size=(W,H), data={...})`.
- `RenderableUserDisplay` subclass with `render_interface(frame)` paints a row/col bar; passed via `Camera(interfaces=[...])` (cd82, wa30, tr87) or `camera.replace_interface([...])` (cn04).
- `NovaBaseGame.__init__(game_id, levels, camera, available_actions=[1..7])`.
- `step()` reads `self.action.id` (GameAction.ACTION1..7); ACTION6 carries `data["x"], data["y"]` in display coords; convert via `self.camera.display_to_grid(int(x), int(y)) → (gx, gy) | None`.
- Always call `self.complete_action()` exactly once per step unless animating (phase counters short-circuit it; `next_level()` and `lose()` followed by `complete_action()` are common).
- Multi-phase animations: hold integer phase counters (`-1` idle, `>=0` ticking), check at top of step(), advance counter, return without `complete_action()` until phase ends.
- Tag queries: `level.get_sprites_by_tag("foo")`, `level.get_sprite_at(gx, gy, "tag")`, `level.get_sprites_by_name(...)`.
- `_get_valid_actions()` override to gate which actions appear; for ACTION6 must enumerate ActionInputs with display-pixel `(x,y)`.
- `_get_hidden_state()` returns small np.int16 array — engine hashes `(frame, hidden_state)` for graph identity.
- `on_set_level(level)` re-initialises per-level state, reads `level.get_data("Key")` for tunables (StepCounter, BackgroundColour, etc.).
- Color legend: 0=white, 1=off-white, 2=light-grey, 3=grey, 4=off-black, 5=black, 6=magenta, 7=pink, 8=red, 9=blue, 10=light-blue, 11=yellow, 12=orange, 13=maroon, 14=green, 15=purple. -1 transparent.
- BFS pathfinding in cell strides (wa30); permutation tables (lp85, sp80 tilt); rotation/cycle by sprite-name suffix (tr87); phase-tagged animation counters (sb26).

Universal must-haves: 64×64 grid, integer palette 0..15, step-counter HUD with `lose()` on zero, tag-based sprite queries, `available_actions` minimal subset.

Anti-patterns to avoid for novelty: `{4,8,9}` palette, sparse 1×1 pawns on empty field, single-mechanic scaling, low-resolution upscaled grids, hidden state without persistent visual cue.

## Deliverables Produced
- None (terminal of this state has no deliverables; cached patterns file replaces per-run study-notes.md).
