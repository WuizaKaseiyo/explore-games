# Step #02: pick_mechanic

## Inputs Consumed
- `workspace/study-notes.md` (from #01 study): cross-cut frequency observations, anti-pattern list, open questions for this state.
- `task-overview.md`: confirmed autonomous mode (no seed string passed inline).
- `prior-games/index.md`: two priors — `kf42` tether-pawn-cycle, `qz73` radial-cycle-lock.
- `prior-games/kf42/mechanism-detail.md`, `prior-games/qz73/mechanism-detail.md`: deep view of priors for distinguishing-rule judgement.
- `prior-games/<id>/run-archive/smoke-frames/level_1.png` for both priors: visual signature comparison.
- `skills/mechanic-novelty/{taxonomy-of-25-games.md, similarity-check.md, negative-similarity-check.md, prior-games-index-format.md}`: the novelty test procedure.
- `skills/design-constraints/{core-knowledge-priors.md, forbidden-elements.md, composition-and-tutorial.md, checklist.md}`: §3.4 priors (allowed: objectness/geometry/physics/agentness), banned elements (no letters/digits-as-glyphs/clipart/cultural-conventions), one-new-mechanic-per-level rule.
- `skills/global/{action-enum.md, color-legend.md, paths.md}`: action subset patterns and palette.
- `skills/code/id-generation.md`: 4-character ID rules + reserved list.
- `deep-analysis-3lvls/<id>/level_1.png` for sp80, g50t, m0r0, dc22 (closest 25-set near-misses surfaced during the similarity check).

## Deliverables Produced
- `workspace/mechanic-pick.md`: 4-character ID `kx14`; mechanic-family tag `tide-tilt-buoyant`; one-paragraph description; positive similarity-check matrix vs taxonomy + priors with concrete distinguishing rules for the 5 surfaced near-misses (kf42, qz73, sp80, g50t, m0r0); negative similarity-check across the 8 dimensions for the 4 closest near-misses, all clearing the 3-dimension threshold; verdict NOVEL.

## Notes
- **ID `kx14` chosen.** Verified against the 25 reserved IDs and the 2 prior-game IDs; no collision. Letters `kx` carry no English-word association; digits `14` are arbitrary.
- **Action subset `[1, 2, 3, 4, 6]` (cardinal motion + click).** Common precedent (ka59, dc22, m0r0, wa30 use this). ACTION5 deliberately unused — the game's distinctive verb (tide control) lives on ACTION1/2 with intuitive UP=raise / DOWN=lower mapping rather than overloading the freedom slot. This is non-standard for the action-enum convention but not forbidden, and it preserves the directness of "press up → water rises".
- **Priors picked carefully to avoid the kf42→vh68 cautionary tale.** The two priors (kf42, qz73) both feature small coloured pawns/tips on dark/grey fields with click-then-act verbs. kx14's vertical-cross-section water/air signature, medium-sized internally-patterned ball sprites, and "manipulate-the-environment-not-the-actor" core dynamic differ on the named principles (palette, sprite grain, core dynamic) from both priors.
- **Mechanic count per level:** L1 = 2 (tide + tilt), L2 = 3 (+ platforms), L3 = 4 (+ anchor). One new mechanic per level promotion, satisfying composition-and-tutorial.md's contract. The witness solution will exercise every mechanic at every level (no hidden mechanics).
- **§3.4 priors:** primarily *physics* (water surface buoyancy + tilt nudge) + *objectness* (balls as persistent entities) + *basic geometry/topology* (platforms blocking vertical paths). Three of the four priors used; agentness deliberately absent (no autonomous antagonist agents).
- **§3.4 forbidden elements check:** no digits-as-glyphs, no letters, no real-world clipart (water is rendered as a flat blue fill with a horizontal surface line — abstract, not "ocean" or "river" iconography), no cultural conventions (the mapping "UP-arrow raises water" is a discoverable physical rule, not a learned association).
