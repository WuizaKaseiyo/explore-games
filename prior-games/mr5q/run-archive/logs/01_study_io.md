# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM diagram, HITL=not allowed, paths convention
- prior-games/index.md (from harness root): cumulative novelty source-of-truth (24 prior games as of run start)
- skills/global/* (registered skills): action enum, color legend, paths
- skills/conventions/from-tech-report.md, cross-cut-frequencies.md, reference-game-patterns.md (registered skills): design philosophy + cached recurring patterns
- skills/design-constraints/* (registered skills): core-knowledge-priors, forbidden-elements, composition-and-tutorial, checklist, difficulty-rules
- skills/mechanic-novelty/* (registered skills): taxonomy-of-25-games, similarity-check, negative-similarity-check, prior-games-index-format
- skills/mechanism-details/*.md (registered skills): per-game quick-reference summaries for the 25 reference games
- 25 mechanism-details/<id>.md (skills/mechanism-details/): all 25 read in full as the per-game evidence layer (the deep-analysis files are the authoritative source but the mechanism-details are the harness-provided distilled summary)
- 5 reference-game source files in full: cn04 (rotate-translate-jigsaw, click+arrow+ACTION5, 620 lines), sk48 (paired-trail-match, click+arrow+ACTION6+ACTION7 undo, 643 lines), m0r0 (mirrored-quad-control, arrow+click+ACTION5, 712 lines), sp80 (liquid-flow-routing, arrow+click+ACTION5, 738 lines), sb26 (mastermind-feedback, click+ACTION5+undo, 827 lines)

## Deliverables Produced
- None (per state file: cached `reference-game-patterns.md` replaces per-run study-notes write).

## Notes
- Internalised: 64×64 grid, palette 0..15, 25/25 step-counter HUD, 25/25 tag-based sprite querying, ACTION5 = freedom-slot for distinctive verb, no on-screen text/digits/letters/clipart, exactly 3 levels in this harness with 1-or-2 new mechanics per promotion + every earlier mechanic carried forward AND required by witness.
- Recurring code patterns picked up: phase-tick state machines for animations, tag-based sprite querying via get_sprites_by_tag, level data dict driving per-level params, snapshot+rollback for undo, click-to-select then arrows-to-move composition.
- Anti-patterns to avoid: single-mechanic difficulty escalation, tight step budgets, hidden mechanics, stochastic step(), {4 wall, 8 red, 9 blue} palette signature already used by kf42/vh68, all-1×1-sprite rendering, decorative sprites that fail no-information-loss-at-32×32 test, no-hidden-state cue rule.
- Pillar coverage map (rough) from the 24 priors: lots of click-or-walk-and-trigger; agentness only in zk9p (pursuer-merge), rk7x (live-switch routing), wt39 (glide-deflect avatar isn't agentness — it's physics/momentum). Less-explored corners: agentness with multiple intent-bearing NPCs, geometry+topology of the playfield itself (tiling/coverage), physics with held-object dynamics.

