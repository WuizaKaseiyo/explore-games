# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, notes
- states/study.md (from harness root): study state spec
- skills/global/{action-enum, color-legend, paths}.md
- skills/conventions/{from-tech-report, cross-cut-frequencies, reference-game-patterns}.md
- skills/design-constraints/{checklist, composition-and-tutorial, core-knowledge-priors, forbidden-elements, difficulty-rules}.md
- skills/mechanic-novelty/{taxonomy-of-25-games, similarity-check, negative-similarity-check, prior-games-index-format}.md
- skills/mechanism-details/<25 ids>.md (all 25 condensed summaries read)
- 5 reference-game source files spanning families:
  - cn04 (click+arrow+ACTION5 — rotate-translate-jigsaw): full read
  - wa30 (arrow+ACTION5 — carry-pickup-drop with BFS): full read
  - m0r0 (arrow+click — mirrored-quad-control): large excerpt incl. step machine
  - sk48 (arrow+click+undo — paired-trail-match): large excerpt
  - sb26 (click+ACTION5+undo — mastermind-feedback): large excerpt
- prior-games/index.md (66 rows): full read
- Untracked prior-games/<id>/metadata.json (gh4r, hp9c, lz7q, qd6n, tc8s, tx4q, vk6m, vw3p, xv4n): scanned for novelty awareness

Screenshots not viewed individually — visual signature reasoning will be done in pick_mechanic against
specific candidate's near-miss priors (per negative-similarity-check.md procedure).

## Deliverables Produced
- None (per state spec; cached patterns file replaces per-run study-notes write)

## Notes
- Internalised: the "no instructions / discoverable mechanic" principle, multi-mechanic 3-level
  composition rule, 64×64 design-pixel resolution requirement (no chunky upscaled grids), ACTION5
  as the freedom slot, ACTION7 as strict undo, step-counter-as-only-resource pattern.
- Prior corpus is HUGE (66+ entries). Walk/click/select+arrow patterns are well-mined. Less-used
  prior corners: (a) audio/temporal patterns mapped to visual rhythms, (b) probabilistic weight
  composition, (c) topology mutation (cells get added/removed, not just toggled), (d) embedded
  agent-dialog (agentness with negotiable goals).
