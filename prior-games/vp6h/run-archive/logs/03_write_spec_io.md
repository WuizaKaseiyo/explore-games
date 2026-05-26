# Step #03: write_spec

## Inputs Consumed
- workspace/mechanic-pick.md (from #02)
- skills/code/spec-template.md (9-section structure)
- skills/code/universal-scaffold.md (file scaffold + style rules)
- skills/code/novaengine-api.md (engine API surface)
- skills/code/id-generation.md (ID format already validated in #02)
- skills/design-constraints/* (composition-and-tutorial, difficulty-rules, checklist, forbidden-elements, core-knowledge-priors)
- skills/global/* (action-enum, color-legend, paths)
- skills/mechanic-novelty/* (re-grounded for §9)

## Deliverables Produced
- workspace/mechanic-spec.md: 9-section spec covering title, mechanic family, sprite roster (8 sprites), 3-level progression with witness solutions and per-mechanic counterfactual necessity (M1 alone at L1; M1+M2 at L2; M1+M2+M3 at L3), action mapping (subset [1,2,3,4,6]), HUD (StepCounterHud), per-game state, win/lose predicates, novelty notes against lq5x/bx84/lf52/kn58/gv47/fz5j with negative-similarity-check verdict NOVEL.

## Notes
- Iterated L2 layout twice during drafting to ensure M2 (lantern-slide) is *necessary* (not just available). Final layout: crystal B at (col 6, row 11..12), no pillar at col 6, default lantern lights col 6 → lantern must be slid before B is pickable. Removed col-2 pillar to ensure A is in default-shaded position purely by being outside lantern range (so sliding lantern leftward does light col 2 → forces ordering: collect A before sliding).
- Adopted the **forgiving rule**: lit crystals are no-op on walk-on (no destruction). Friendlier discovery; player can experiment without irrecoverable loss. Discovery of M3 at L3 happens via "walk onto C with one lantern slid → no-op → infer must slide other lantern."
- L3 layout: ensured a single dual-position config (top@cols 0..4, bot@cols 10..14) makes A, B, C all simultaneously safe — because A's column has a top-pillar that protects it from top-light when top-lantern slides left, and B's column has a bot-pillar that protects from bot-light when bot-lantern slides right.
- Witness step counts: L1=7 actions / 40 budget; L2=26 actions / 70 budget; L3=24 actions / 120 budget. Budget headroom 5–6× the witness consistently.
