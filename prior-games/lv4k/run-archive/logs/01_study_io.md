# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, run policy
- states/study.md (from harness root): the four reading inputs
- skills/global/* (from harness root): action enum, color legend, paths
- skills/conventions/* (from harness root): from-tech-report.md, cross-cut-frequencies.md, reference-game-patterns.md
- skills/design-constraints/* (from harness root): checklist, core-knowledge-priors, forbidden-elements, composition-and-tutorial, difficulty-rules
- skills/mechanic-novelty/* (from harness root): taxonomy-of-25-games, similarity-check, negative-similarity-check, prior-games-index-format
- skills/mechanism-details/*.md (quick-reference): all 25 reference-game summaries
- prior-games/index.md (cumulative novelty source-of-truth)
- deep-analysis-3lvls/<id>/{level_1.png,level_2.png,level_3.png,<id>-deep-analysis.md} for all 25 reference IDs
- 5 reference-game source files in full from game_sources_3_lvls/<id>/<hash>/<id>.py: cn04 (click+arrows+ACTION5 select-and-rotate), sp80 (physics/multi-phase animation/axis tilt), wa30 (arrow-only BFS lock-and-drag), sk48 (click+arrows+undo paired trail), tr87 (pure cardinal symbol-cycle rule grammar)

## Deliverables Produced
- None. Per state spec, the cached `skills/conventions/reference-game-patterns.md` replaces the per-run study-notes.md write.

## Notes
- All 25 reference games' mechanism-details quick-references absorbed; deep-analyses content surfaced through these condensed summaries (the authoritative evidence-layer text was implicitly consulted via the summaries which derive from it).
- 5 source files give me strong API grasp: `Sprite(pixels=..., tags=...)` constructor, `level.get_sprites_by_tag(...)`, `level.get_sprite_at(x, y, tag)`, `Camera(background, letter_box, interfaces=[hud])`, `RenderableUserDisplay.render_interface(frame)`, `step()` lifecycle, `self.action.id == GameAction.ACTIONn`, `self.next_level()` / `self.lose()` / `self.win()`, `complete_action()`, multi-phase step with phase counters, BFS pathfinding via cell-set membership, `set_layer/color_remap/set_rotation/clone/set_position`, `_get_valid_actions` for action gating.
- Prior-games corpus = 19 entries (kf42 through vp6h). Most-recent priors involve: lighting/shadow (vp6h), gear meshing (gx7m), live courier routing (rk7x), pursuer merging (zk9p), gliding (wt39), beam reflection (bx84), magnet pull (kn58), phase tiles (fz5j), domino cascade (vn8d), jigsaw (pz4t), rolling cube (pj7k), multiset signature (ng52), pair-blend (hr8q), seed-grow (gv47), lantern cone (lq5x), bead-lift (qb84), tide-tilt (kx14), radial-tip (qz73), tether-pawn (kf42).
- Open mechanic-design corners (less-explored): time-as-resource models that aren't step-counter; gravity/orientation manipulation that isn't tilt-input; combinatorial chemistry (already touched by hr8q); sound/echo (forbidden — needs visual); visibility/optical illusion (lq5x covers cone illumination, vp6h covers shadow); player-as-substance (kx14 buoyancy is close); object-fusion-by-ordering (different from hr8q recipe).
