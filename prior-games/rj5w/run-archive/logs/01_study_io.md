# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, HITL=not allowed, paths convention
- skills/global/{paths,action-enum,color-legend}.md: action slots, palette, paths
- skills/conventions/from-tech-report.md: full NovaPlay design philosophy + 12-question gate
- skills/conventions/cross-cut-frequencies.md: 25/25 step-counter+tags+camera; ACTION5 modal in 9/25; ACTION7 undo in 6/25
- skills/conventions/reference-game-patterns.md: cached patterns (14 design moves, 13 anti-patterns, discoverability rules, open questions)
- skills/design-constraints/{core-knowledge-priors,forbidden-elements,composition-and-tutorial,checklist,difficulty-rules}.md
- skills/mechanic-novelty/{taxonomy-of-25-games,prior-games-index-format,similarity-check,negative-similarity-check}.md
- skills/mechanism-details/*.md: per-game summaries for all 25 reference games (Summary sections)
- 5 reference-game source files spanning families:
  - cn04 (621 lines, click+arrow+ACTION5 select-rotate, full)
  - wa30 (840 lines, arrow+ACTION5 modal lock-pickup, full)
  - tr87 (697 lines, pure-arrow tape cycler with morph animation, full)
  - tu93 (1113 lines, pure-arrow multi-agent train with 3-phase step, structural)
  - r11l (1707 lines, pure-click drag-tween, structural step+animation)
- Sampled screenshots: cn04, sp80, m0r0, lp85, wa30, sb26, tu93, cd82 (visual signatures noted)
- Sampled prior-game smoke-frames: qm4t, zw91, nb6t
- prior-games/index.md (36 priors registered) + prior-games/fb7t/ (Phase-Transition Matter; treated as 37th unregistered prior)

## Deliverables Produced
- None (per state spec; cached patterns replace per-run study-notes.md)

## Notes
- Engine fluency confirmed: NovaBaseGame, Camera(letter_box), Sprite(pixels/-1 transparent), Level(sprites=, grid_size=, data=), RenderableUserDisplay, GameAction.ACTION1..7, level.get_sprites_by_tag, get_sprite_at, complete_action, next_level, lose, win.
- Multi-frame animation pattern (skip complete_action while phase counter advances) seen in tr87, tu93, r11l, cn04 implicitly. Critical for long-distance / chain-reaction dynamics.
- ACTION5 carries identity verb when present (rotate, commit, pour, lock, cycle).
- Prior corpus is dense (~37 games); negative-similarity test is the active novelty gate.
