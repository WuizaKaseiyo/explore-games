# Step #01: study

## Inputs Consumed
- `task-overview.md` (from harness root): FSM overview, autonomous run (no seed), HITL not allowed.
- `skills/conventions/from-tech-report.md`: distilled philosophy — 12-question gate (exploration / modelling / goal-setting / planning), 64×64 grid, action-efficiency scoring, "no instructions" principle, 3-level cap with composition arc (L1 base / L2 +new / L3 +new), determinism required.
- `skills/conventions/cross-cut-frequencies.md`: 25/25 step-counter HUD; 25/25 tag-based queries; click in 19/25; ACTION5 distinctive in 9/25; ACTION7 undo in 6/25; lives in 1/25.
- `skills/conventions/reference-game-patterns.md`: 14 recurring design moves, discoverability-through-observable-change (multi-frame animation for long-distance / chain-reaction mechanics), 13 anti-patterns including L3 = L2-with-bigger-grid, palette `{4,8,9}` repetition, small-blocks-on-empty-field aesthetic.
- `skills/design-constraints/core-knowledge-priors.md`: four allowed priors (objectness, geometry/topology, physics, agentness).
- `skills/design-constraints/forbidden-elements.md`: no letters, digits-as-glyphs, real-world clipart, cultural conventions, language.
- `skills/design-constraints/composition-and-tutorial.md`: exactly 3 levels; L1 base, L2 = L1 + (1 or 2 new), L3 = L2 + (1 or 2 new), all witness-required, none drop out.
- `skills/design-constraints/checklist.md`: 22 items; items 11/12/18/20/21/22 are the load-bearing gates.
- `skills/design-constraints/difficulty-rules.md`: two-stage difficulty (exploration + planning); ~2 min/level, ~6 min total; budgets generous; L3 planning must defeat a named trivial heuristic.
- `skills/global/action-enum.md`: ACTION5 = freedom slot; ACTION7 STRICT undo only.
- `skills/global/color-legend.md`: palette 0..15 + `-1` transparent.
- `skills/global/paths.md`: harness path conventions.
- `skills/mechanic-novelty/taxonomy-of-25-games.md`: 25 mechanic-family rows (taxonomy bar).
- `skills/mechanic-novelty/similarity-check.md` + `negative-similarity-check.md`: positive (distinguishing-rule) + negative (3-of-8-dimensions shared with any prior) gates.
- `skills/mechanic-novelty/prior-games-index-format.md`: index schema.
- `skills/code/spec-template.md`: 9-section spec contract.
- `skills/code/universal-scaffold.md`: file layout, camera-must-match-grid_size rule, semantic naming required, common patterns (two-sprite swap, simultaneous-conflict resolution).
- `skills/code/novaengine-api.md`: Sprite / Level / Camera / NovaBaseGame / GameAction / InteractionMode / BlockingMode signatures.
- `skills/code/id-generation.md`: 4-char ID rules.
- `skills/code/smoke-test-checks.md`: 10 universal + 2-4 custom smoke checks; CHECK_WITNESS_WINS is the strongest.
- `skills/finalize/*.md`: final-report, mechanism-detail, run-archive, index-row schemas.
- `skills/mechanism-details/{cn04, sb26, sp80, tu93, ka59, wa30, m0r0}.md`: representative spread of mechanic-family interiors.
- `game_sources_3_lvls/cn04/65d47d14/cn04.py` (skim of class body, ~270 lines centered on `on_set_level` + `step()`): anchors API patterns — camera setup, sprite-level rendering, click-to-select with `display_to_grid`, ACTION5 rotation, win-check + lose-on-budget pattern.
- 5 rendered level_1 frames (cn04, sp80, tu93, ka59, prior `nz3v`): anchors visual taste — pixel-rich primary sprites, varied palettes, internal sprite structure (eyes, rings, hollows) rather than monochrome blocks.
- `prior-games/index.md` (81 rows, 80 priors): novelty bar including kf42, qz73, kx14, qb84, lq5x, gv47, hr8q, pj7k, pz4t, vn8d, fz5j, kn58, bx84, wt39, zk9p, rk7x, gx7m, vp6h, kp9z, zd7m, lv4k, xn5p, mr5q, pf3w, tg6w, vd3g, jd4q, ek73, tm5x, qx7p, kj82, nb6t, qm4t, qn7w, zw91, rj5w, wj7d, qj4r, jx5k, ds5q, qf8m, pv5q, vy3k, vt6q, rs8n, xz5g, kw8t, tj4n, mz6t, lt7m, dz4m, pn5d, xv2b, wq3m, wb6n, pk4m, kv8w, nf3z, hl4n, bw7k, bz3k, dj5h, fw8c, yh3p, qy7w, hk7v, rt9k, pq5w, cv5b, wm6q, nh4w, tk6n, nz3v.
- States read ahead: `pick_mechanic`, `write_spec`, `critique_spec`, `implement`, `smoke_test`, `fix_implementation`, `finalize` — full FSM is now in working memory.

## Deliverables Produced
- None (per state's `## Next States` deliverables: "None.").

## Notes
- Cached patterns file replaces the per-run study-notes write; the FSM is set to transition to `pick_mechanic` after this state.
- Visual taste: avoid the chunky-upscaled-low-res look (tu93-style 16×16) and the {4,8,9}-only palette family. Aim for richer internal pixel structure on every primary sprite.
- Lots of priors already explore: cardinal walking + click-select + ACTION5-modal, projectile/beam mechanics, fold/mirror/reflect, fluid/flow, stacking/balancing, chained chain-reactions, vine/branch growth, gear/cascade. Open territory still includes: time-dilation/turn-banking, music/rhythm (probably forbidden — cultural), recursion/self-similar zoom, refraction-by-medium, knotting/braiding (qy7w covers strand-twist), shadow-casting (vp6h), constellation-graph (jx5k).
- Forbidden combos to avoid: more pawn-on-grid + colour-target-tile games (oversaturated); more reflection/fold games (qj4r, wj7d, rj5w).
