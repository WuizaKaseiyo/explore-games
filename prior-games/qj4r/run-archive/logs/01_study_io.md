# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): 3-level cap, prior-games corpus is novelty source of truth
- states/study.md: 4 reading inputs spec
- skills/global/{paths,action-enum,color-legend}.md: ACTION5 = freedom slot, palette 0..15, -1 = wildcard, click via display_to_grid
- skills/conventions/from-tech-report.md: 4 pillars, no instructions, composition not scaling, 3-level weight (1/2/3)/6
- skills/conventions/cross-cut-frequencies.md: step-counter HUD universal, tag-based queries universal, action-subset minimal
- skills/conventions/reference-game-patterns.md: 14 inheritance patterns, 13 anti-patterns, mandatory animation cases, no-hidden-state rule, UI-teaches rule
- skills/design-constraints/core-knowledge-priors.md: 4 priors (objectness, geometry/topology, physics, agentness); energy bar must-have
- skills/design-constraints/forbidden-elements.md: no letters, digits-as-glyphs, clipart, cultural conventions, language
- skills/design-constraints/composition-and-tutorial.md: L1 base, L2 +1-or-+2, L3 +1-or-+2, all earlier required
- skills/design-constraints/checklist.md: 21-item gate, per-mechanic counterfactual table, no-hidden-state, no-low-resolution, UI-teaches
- skills/design-constraints/difficulty-rules.md: post-discovery planning, generous step budget, never-shrinking
- skills/mechanic-novelty/taxonomy-of-25-games.md: 25 reference families
- skills/mechanic-novelty/similarity-check.md, negative-similarity-check.md: positive + negative novelty gates (kf42→vh68 cautionary tale)
- skills/mechanic-novelty/prior-games-index-format.md: index schema
- skills/mechanism-details/{cn04,sb26,m0r0,sp80,cd82,tu93,ka59,r11l}.md: distilled per-game summaries
- prior-games/index.md: 37 prior generated games (kf42 ... zw91 + fb7t in dir-only); novelty must dodge all
- 5 reference source files in full (cn04 + wa30 fully read; sk48 + sb26 deep skim of step()/win/valid_actions sections; cd82 patterns via mechanism-details). API anchored: sprites dict, levels list, NovaBaseGame subclass with on_set_level/step/_get_valid_actions/_get_hidden_state, RenderableUserDisplay subclass for HUD, complete_action() at end of every step

## Deliverables Produced
- None (study has no deliverables; cached patterns file replaces per-run study-notes)

## Notes
- Cached `reference-game-patterns.md` and `cross-cut-frequencies.md` substitute for derivation work past runs always converged to.
- Universal idioms confirmed: step-counter HUD, tag-based sprite querying, level data dict for budgets, ACTION5 distinctive verb, multi-phase step() with phase-tick sentinel for animations, color_remap for selection cues.
- Anti-patterns to dodge (per cautionary tales): coloured-pawn-blocks-on-walled-grid + click-to-select + arrows-to-move (kf42/vh68 family), low-resolution chunky upscale, single-mechanic difficulty escalation.
- Empty prior-games slot of fb7t (in dir but not in index.md) named "Phase-Transition Matter" — to be treated as a near-prior for novelty.
