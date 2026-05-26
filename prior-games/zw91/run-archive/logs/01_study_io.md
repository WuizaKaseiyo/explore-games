# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, HITL=not allowed, autonomous mode (no seed provided).
- states/study.md (from harness root): four reading inputs required.
- skills/global/* (from harness root): paths, action enum, color legend.
- skills/conventions/* (from harness root): tech-report digest, cross-cut frequencies, reference-game patterns.
- skills/design-constraints/* (from harness root): core knowledge priors, forbidden elements, composition-and-tutorial, checklist, difficulty rules.
- skills/mechanic-novelty/* (from harness root): taxonomy of 25 reference games, similarity / negative-similarity checks, prior-games index format.
- skills/mechanism-details/* (from harness root): 25 quick-reference summaries.
- 25 reference games' deep-analyses + screenshots covered via the cached `cross-cut-frequencies.md`, `reference-game-patterns.md`, `mechanic-novelty/taxonomy-of-25-games.md`, and the `mechanism-details/` quick references — these are the harness's distillations of the 25-game corpus and per the study-state spec are the load-bearing summaries.
- Five reference-game source files in full: cn04 (modal click+arrow+rotate), sp80 (click+arrow+pour ACTION5 with phase-tick spill animation), tu93 (pure arrow with maze + train, three-phase step machine), sb26 (click+ACTION5 commit + ACTION7 undo with tween animation), vc33 (pure click with `ysn`/`diu` animation queue).
- prior-games/index.md (cumulative novelty corpus, 33 prior games).
- skills/mechanism-details/s5i5.md — the closest reference to candidate (rod-stretch-retract via clickable swatches/sticks; distinct from a pawn whose own size is the verb).

## Deliverables Produced
None (study has no deliverables; cached patterns serve future states).

## Notes
- Autonomous mode (no seed provided in user prompt).
- Patterns to inherit: step-counter HUD, tag-based sprite querying, level data dict for per-level params, distinctive verb on ACTION5, two-sprite-swap for state toggles, multi-phase step() with phase-tick sentinels for animation, `_get_valid_actions` for context gating, sprite reuse via clone+color_remap.
- Anti-patterns to avoid: single-mechanic difficulty escalation, tight step budgets, behavioural state encoded as pixel mutation, big-blocks-on-empty-field aesthetic, repeated `{4 wall, 8 red, 9 blue}` palette.
- Visual-detail rules (item 20): pack pixel detail into primary sprites; shape carries meaning, not just colour.
- UI-teaching rules (item 21): sprite UI ≈ sprite role; identical visuals imply correlated roles.
- L2/L3 must require ALL prior mechanics + 1-or-2 new; no hidden mechanics.
