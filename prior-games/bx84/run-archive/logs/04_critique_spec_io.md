# Step #04: critique_spec

## Inputs Consumed
- workspace/mechanic-spec.md (the spec being critiqued)
- workspace/mechanic-pick.md (cross-reference for novelty rules)
- skills/design-constraints/checklist.md (items 1-18)
- skills/design-constraints/{composition-and-tutorial,core-knowledge-priors,difficulty-rules,forbidden-elements}.md
- skills/mechanic-novelty/{similarity-check,negative-similarity-check,taxonomy-of-25-games,prior-games-index-format}.md
- prior-games/index.md
- The 25 deep-analyses from #01 (recalled for distinguishing-rule re-validation against deeper view; specifically reconfirmed against ar25, cd82, tn36, re86)

## Deliverables Produced
- workspace/critique-pass.md — itemised PASS verdict for items 1-18, the positive similarity check, the negative similarity check (re-walked on fleshed-out spec), and all 5 common failure modes from `critique_spec.md`.

## Notes
- This is the FIRST visit to `critique_spec` (revision count = 0). Spec passes on first attempt.
- The most-critical gate (item 18 / L3 commute test) was specifically designed-for in the spec: the prism-toggle mechanic introduces genuine click-order dependence via sticky-but-only-on-click target lighting. The swap (place_mirror, toggle_prism) → (toggle_prism, place_mirror) breaks the witness because the south branch only exists in state ES, and the player must place a mirror (and re-trace) WHILE the prism is still in ES to capture target_yellow_south's lit-state.
- Tag-name conventions follow `universal-scaffold.md` § "Style rules" — semantic names (`mirror`, `filter`, `prism`, `target_blue`, etc.) instead of obfuscated tokens.
