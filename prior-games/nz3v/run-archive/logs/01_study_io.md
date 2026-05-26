# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, 3-level cap, ID rules, output paths
- skills/global/* (from state Skills): paths, action-enum (slot 5 freedom, slot 7 strict-undo), color-legend
- skills/conventions/from-tech-report.md: §3.4 priors + 12-question gate, RHAE scoring (3-level weights L1=17%, L2=33%, L3=50%)
- skills/conventions/cross-cut-frequencies.md: 25/25 step-counter, 25/25 tag-querying, ACTION5 9/25, ACTION7 6/25
- skills/conventions/reference-game-patterns.md: cached design moves (step-counter HUD, tag query, ACTION5 identity verb, visual coupling, multi-phase step), anti-patterns (single-mechanic scaling, big-blocks-on-empty-field, repeated palette `{4,8,9}`), discoverability via animation, no hidden state
- skills/design-constraints/* (5 files): priors, forbidden elements, exact-3-level structure with +1-or-+2 mechanic rule, full 16-checklist, difficulty 4-bullet rule per level
- skills/mechanic-novelty/* (4 files): taxonomy of 25 references, similarity-check (positive), negative-similarity-check (3 principles + 8 dimensions + cautionary kf42/vh68 tale), prior-games index format
- skills/mechanism-details/*.md (all 25): per-game mechanic summaries — read in full
- prior-games/index.md: 55 prior generated games with mechanic_family tags
- 5 reference source files in full (game_sources_3_lvls/<id>/<hash>/<id>.py):
  - cn04 (620 L) — click+arrow+ACTION5 jigsaw rotate/translate
  - sk48 (643 L) — arrow+click+undo paired-trail-match
  - cd82 (677 L) — arrow+click+ACTION5 orbit-fire-paint sweep (8-slot ring + animation phases)
  - tr87 (696 L) — arrow-only symbol-cycle rule rewriting
  - m0r0 (712 L) — arrow+click mirror-quad-control with axis-flipped quadrants

## Deliverables Produced
- (none — transition to pick_mechanic carries no deliverables)

## Notes
- Cached patterns + cross-cut frequencies file replace per-run study-notes write, per state instructions.
- Did not view all 75 reference screenshots in this state; deferring visual comparison to pick_mechanic's negative-similarity gate where a candidate is concrete.
- Reference patterns flag: ACTION5 is where novelty lives; "post-discovery planning depth" is the load-bearing critique gate; visual signature divergence is mandatory (kf42 → vh68 cautionary tale).
- Prior corpus (55 games) is dense — covers tether/cycle/tilt/fold/rotate/cascade/grapple/route/blast/grow/sokoban variants. Need a mechanic that diverges on "what's on the board" and "core dynamic" axes, not just verb cardinality.
