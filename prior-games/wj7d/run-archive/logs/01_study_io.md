# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): scope, FSM, paths, HITL=not allowed
- states/study.md (from harness root): four required reading inputs
- skills/global/*.md: action-enum, color-legend, paths
- skills/conventions/*.md: from-tech-report, cross-cut-frequencies, reference-game-patterns
- skills/design-constraints/*.md: core-knowledge-priors, forbidden-elements, composition-and-tutorial, checklist, difficulty-rules
- skills/mechanic-novelty/*.md: taxonomy, similarity-check, negative-similarity-check, prior-games-index-format
- skills/mechanism-details/*.md: 25 quick-reference summaries
- 25 deep-analyses + screenshots from deep-analysis-3lvls/<id>/
- 5 reference-game source files in full (chosen for diversity, ≤2000 lines)
- prior-games/index.md (cumulative novelty source of truth — 36 priors)

## Deliverables Produced
- None (per state spec; cached patterns subsume per-run study notes)

## Notes
- Five source files chosen across families: cn04 (click+arrow+ACTION5 rotate/select),
  m0r0 (mirror-orb-merge, animation phase ticks, scaled-overlay
  RenderableUserDisplay), sb26 (tile-place-commit), tu93 (cardinal-only
  walkable-region pixel-tag), r11l (pure-click centroid-puppet).
- Recurring API: NovaBaseGame super().__init__ with available_actions=[...],
  Camera(background, letter_box=PADDING_COLOR), Level(sprites=[...],
  grid_size=(W,H), data={...}), level.get_sprites_by_tag,
  level.get_sprite_at(gx, gy, tag="..."), camera.display_to_grid(x, y),
  Sprite.set_position / move / set_interaction(InteractionMode.X) /
  color_remap / set_rotation, RenderableUserDisplay subclass with
  render_interface(frame), self.next_level() / self.lose() /
  self.complete_action(), animation phase via early-return-without-
  complete_action.
- Prior-games corpus is dense: 36 priors. Mechanics families used so far
  are concentrated on grid-pawn-walking (zk9p, ek73, jd4q, fz5j, kn58, wt39,
  cohort-step zd7m), painting/canvas (gv47, ft09-style), routing/cascades
  (vn8d, kp9z, gx7m, rk7x, bx84), shifting (qx7p, lp85-style), state-toggling
  (kj82, mr5q), and various place/commit (qm4t, qn7w, zw91, sb26-style).
  Less explored: tape rewrite (tr87 family), tilt-stratification (tg6w
  exists but in a different angle), structural transformations of the
  playfield itself, spatial-reasoning where the player AS A WHOLE is
  geometrically transformed (not just a stretch like nb6t).

