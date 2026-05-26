# Step #04: critique_spec

## Inputs Consumed
- `workspace/mechanic-spec.md` (from #03 write_spec).
- `workspace/mechanic-pick.md` (from #02 pick_mechanic) — re-read
  to confirm the mechanic-family is unchanged from pick-time.
- `skills/design-constraints/checklist.md` (16 items).
- `skills/mechanic-novelty/{similarity-check,negative-similarity-check,taxonomy-of-25-games}.md`.
- `prior-games/index.md`, `prior-games/kf42/{mechanism-detail.md,
  run-archive/smoke-frames/level_1.png, level_2.png}` for the
  re-run negative-similarity check.
- Spot-checked deeper evidence at
  `deep-analysis-3lvls/{ar25,cn04,cd82,lp85}/<id>-deep-analysis.md`
  to confirm distinguishing rules vs the closest taxonomy entries
  hold against the deep-view (per the state's instruction to consult
  deep-analysis when distinguishing-rule judgement matters).

## Deliverables Produced
- `workspace/critique-pass.md` — 16 checklist items each marked
  `✅ PASS` with a one-line justification, plus the two novelty
  verdicts (similarity-check NOVEL, negative-similarity-check NOVEL
  with explicit 8-dimension table). Final verdict: PASS.

## Notes
- Spent extra scrutiny on dimension 3 of the negative-similarity-check
  ("what is the level asking for") because both kf42 and qz73 reduce
  to "coloured movable on coloured target". Concluded this is a
  goal-shape similarity at most marginal (the verbs that achieve the
  goal are entirely different) and does not by itself trigger
  rejection. Kf42's actual prior failure mode (per the cautionary
  tale in `negative-similarity-check.md`) was sharing 6+ dimensions
  with vh68; qz73 shares ~1.5 with kf42.
- Spent extra scrutiny on item 7 ("forbidden elements") because the
  8-slot ring layout could read as a clock face. Concluded acceptable
  because (a) no numerals, (b) no hour/minute hand structure, (c)
  per-level tip counts are 3, 3, and 5 — never the 12 a clock
  needs, (d) tips and sockets are heterogeneous (different colours).
- Did NOT find any spec issue requiring a transition back to
  write_spec. Consequence: this is the only critique_spec visit; no
  loop guard triggered.
