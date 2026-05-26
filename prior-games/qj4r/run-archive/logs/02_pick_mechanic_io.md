# Step #02: pick_mechanic

## Inputs Consumed
- task-overview.md (from #01): autonomous mode (no seed)
- skills/mechanic-novelty/taxonomy-of-25-games.md: 25 reference families
- skills/mechanic-novelty/{similarity-check,negative-similarity-check,prior-games-index-format}.md
- skills/mechanism-details/{ar25,m0r0,cn04}.md (closest near-misses)
- skills/code/id-generation.md
- skills/code/spec-template.md, universal-scaffold.md
- skills/design-constraints/* (re-confirmation)
- prior-games/index.md: 37 entries + fb7t in directory only

## Deliverables Produced
- workspace/mechanic-pick.md: ID `qj4r`, mechanic family `fold-mirror-pair`, one-paragraph description, distinguishing rules vs every flagged near-miss (ar25, m0r0, cn04, bx84, wt39, tg6w, pz4t, qm4t), and explicit negative-similarity-check pass.

## Notes
- Closest taxonomy near-miss: ar25 (mirror-line + ghost). The fold mechanic differs by being a *one-shot* reflection that *contracts the playfield* per action, with no permanent mirror line or continuous ghost.
- Closest prior near-miss: bx84 / wt39 / tg6w — all distinct on core dynamic.
- Palette commitment chosen to avoid the kf42→vh68 cautionary tale's `{4, 8, 9}`-dominant signature.
- No-undo design (per cached-pattern guidance "generated games should not assume undo is available"); fold actions are non-reversible mid-level — encourages planning.
