# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, HITL=not allowed, paths convention.
- skills/global/paths.md, action-enum.md, color-legend.md: API and palette anchors.
- skills/conventions/from-tech-report.md: design philosophy distilled from §3.4 tech report.
- skills/conventions/cross-cut-frequencies.md: cached counts of features across 25 ref games.
- skills/conventions/reference-game-patterns.md: cached 14 design moves + 13 anti-patterns + open questions for pick_mechanic.
- skills/design-constraints/core-knowledge-priors.md: 4 allowed prior categories.
- skills/design-constraints/forbidden-elements.md: hard rejects (digits, letters, clipart, conventions, language).
- skills/design-constraints/composition-and-tutorial.md: 3-level structure with +1/+2 mechanics per level.
- skills/design-constraints/checklist.md: 21-item §3.4 checklist for spec/critique gating.
- skills/design-constraints/difficulty-rules.md: 2-stage difficulty model, per-level a/b/c/d justification.
- skills/mechanic-novelty/taxonomy-of-25-games.md: full mechanic taxonomy of reference set.
- skills/mechanic-novelty/similarity-check.md: positive novelty test procedure.
- skills/mechanic-novelty/negative-similarity-check.md: 3 principles + 8 dimensions for visual overlap rejection.
- skills/mechanic-novelty/prior-games-index-format.md: index schema.
- prior-games/index.md: 27 prior generated games + 25 ref => 52 mechanic families to be novel against.
- skills/mechanism-details/*.md (25 files): cached condensed mechanism summaries (next).
- 25 deep-analyses + level screenshots: pragmatically sampled (next).
- 5 source files in full: cn04, vc33, tu93, sp80, sb26 (next).

## Deliverables Produced
- None (cached `reference-game-patterns.md` replaces per-run study notes per state file).

## Notes
- Read all 25 mechanism-detail summaries (mechanism-details/*.md, ~1684 lines total).
- Source files in full: cn04 (620 lines, click+arrow+rotate selection idiom; sprite/level/HUD/step structure; ACTION6 click→display_to_grid→get_sprite_at→select; ACTION1-4 nudge; ACTION5 rotate; _get_hidden_state; _get_valid_actions gates after click).
- Source files in full: sp80 (738 lines, fluid-flow CA; phase machine "change"|"spill"; level.add_sprite/remove_sprite mid-step; tilt rotation via permutation tables; try_move_sprite for collision-aware movement; multi-frame animation by early-return pattern).
- Source files (substantial): sb26 (head+animation phase pattern with multiple `>=0/-1` sentinel ints in step()); each phase produces a visible frame and steps the counter.
- Sampled level_1.png screenshots: cn04 (clean coloured shapes with internal structure on cyan field, "8" connector nubs visible), sp80 (top-of-screen spawn + bottom cup + pipe in middle on orange field with letter-box), tu93 (maze tile with clear walkable mottled path, two distinct agent colours).
- Engine API confirmed: NovaBaseGame, Level, Camera(background, letter_box, interfaces=[]), RenderableUserDisplay (render_interface(frame)→ndarray), Sprite (clone, set_position, set_layer, move, rotate, render, color_remap, set_visible, pixels, x, y, width, height, tags, rotation), level (get_sprites, get_sprites_by_tag, get_sprites_by_name, get_sprite_at(x,y,ignore_collidable=True), add_sprite, remove_sprite, get_data, grid_size), self.action.id, self.action.data["x"]/["y"], self.camera.display_to_grid(int(x), int(y))→Optional[Tuple], self.complete_action(), self.next_level(), self.lose(), self.win(), self.try_move_sprite(sprite, dx, dy)→collisions, self._action_count, self._current_level_index.
- Prior-games corpus: 27 games. Mechanic families taken (must avoid): tether-pawn-cycle, radial-cycle-lock, tide-tilt-buoyant, bead-lift-swap, lantern-cone-illuminate, seed-grow-surround-dissolve, pair-blend-recipe, multiset-signature-classify, rolling-cube-face-paint, anchor-pivot-place, domino-cascade-topple, phase-step-tile, anchor-pull-magnet, beam-mirror-reflect, glide-deflect-thaw, pursuer-merge-walk, live-switch-routing, gear-mesh-cascade, shadow-cast-collect, grain-accumulate-topple, cohort-step-route, lever-balance-torque, chamber-stamp-partition, polarity-attract-discharge, wavefront-converge-timing, settle-pile-tilt.
- Reference 25 also taken: shape-mirror-cover, procedural-graph-walk(undo), orbit-fire-paint, nub-pair-glyph, colour-cycle-walk, stamp-3x3-paint, walk-vs-scroll, sokoban-explode-chase, row-col-shift-grid, cycler-attribute-match, mirror-orb-merge, centroid-puppet-leg, frame-paint-canvas, rod-stretch-retract, tile-place-commit, scene-find-target, paired-snake-trail, pour-shelf-route, recipe-fruit-collect, program-pawn-trace, tape-rewrite-rule, maze-pickup-train, row-slide-pull-tab, lock-drag-crate.
