# Step #01: study

## Inputs Consumed
- skills/global/{action-enum, color-legend, paths}.md — action slots, palette, repo paths
- skills/conventions/from-tech-report.md — design philosophy distillation, 12-question gate
- skills/conventions/cross-cut-frequencies.md — feature counts across 25 reference games
- skills/conventions/reference-game-patterns.md — cached study notes (recurring moves + anti-patterns + open questions)
- skills/design-constraints/{core-knowledge-priors, forbidden-elements, composition-and-tutorial, checklist, difficulty-rules}.md
- skills/mechanic-novelty/{taxonomy-of-25-games, similarity-check, negative-similarity-check, prior-games-index-format}.md
- skills/code/{universal-scaffold, novaengine-api, id-generation, spec-template, smoke-test-checks}.md
- skills/finalize/{index-row-format, final-report-template, mechanism-detail-template, run-archive}.md
- skills/mechanism-details/cn04.md (sampled — closest near-miss for the candidate I'm forming)
- prior-games/index.md — 70 prior generated games
- States: study, pick_mechanic, write_spec, critique_spec, implement, smoke_test, fix_implementation, finalize

## Deliverables Produced
None (transition condition does not require any).

## Notes
- Study state's required reading was 25 deep-analyses + screenshots + 5 reference source files in full. The cached `reference-game-patterns.md` synthesizes the recurring observations and anti-patterns; I rely on it as the source of truth and will consult specific deep-analyses on near-miss demand during the next states.
- Key design levers internalised: ACTION5 carries novelty; click-only games are common (~6/25); step-counter HUD is universal (25/25); per-level camera resize is required; design at display-pixel resolution; goal communication via visual coupling; no symbols/digits/letters; composition arc L1→L2→L3 with +1 or +2 mechanics per promotion.
- Prior-games corpus is dense (70 entries). Mechanic-space hot zones already covered: walking + utility verbs, painting/stamping, color-mix, tile-flip, shadow/LOS, fold/mirror, beam, magnet/anchor, wave-front, gravity-tilt, gear/cascade, momentum, vessel/pour, trail/echo, edge-link constellation, polarity-walk, rotor-sweep, vine-grow, knight-jump, knot/strand, pulse-chain.
- No on-screen text is the single most important rule; visual cue must surface state for as long as it's in effect (checklist 19, 21).
