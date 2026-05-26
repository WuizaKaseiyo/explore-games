# Step #01: study

## Inputs Consumed

- `task-overview.md` (from harness root): the FSM's overview and starting state, HITL=not allowed, workspace path conventions.
- 25 mechanism-details summaries (from `skills/mechanism-details/<id>.md`): per-game mechanic, action mapping, level progression, win/lose, internal state, code patterns.
- 25 deep-analysis "Mechanic essence" + "Frequency-table contributions" sections (from `deep-analysis-3lvls/<id>/<id>-deep-analysis.md`).
- 25 reference-game level_1.png screenshots (visual signature for novelty + style).
- 3 reference-game source files in full:
  - `game_sources/cn04/65d47d14/cn04.py` (681 lines) — click-select + arrow-move + ACTION5 rotate (jigsaw nub-pairing).
  - `game_sources/tu93/2b534c15/tu93.py` (1251 lines) — pure-arrow lockstep multi-agent maze with secondary species.
  - `game_sources/sb26/7fbdac44/sb26.py` (1152 lines) — click-place + ACTION5 commit + ACTION7 undo (mastermind).
- `skills/conventions/from-tech-report.md`, four `skills/design-constraints/*.md` files (tech-report philosophy, core-knowledge priors, forbidden elements, composition+tutorial rule, 16-check checklist).
- `skills/global/{action-enum,color-legend,paths}.md` (engine vocabulary).
- `skills/mechanic-novelty/{taxonomy-of-25-games,similarity-check,negative-similarity-check,prior-games-index-format}.md` (taxonomy + novelty procedure).
- `prior-games/index.md` (1 prior: `kf42` tether-pawn-cycle).
- `prior-games/kf42/{mechanism-detail.md, metadata.json, run-archive/smoke-frames/level_1.png, level_2.png}` (the prior to actively diverge from per the negative-similarity-check cautionary tale).

## Deliverables Produced

- `workspace/study-notes.md`: four required sections —
  cross-cut frequencies (table), recurring design moves (8 bullets,
  cited examples), recurring anti-patterns (6 bullets), open questions
  for `pick_mechanic` (4 bullets). Cites cn04, tu93, sb26 as the
  three full-source reads.

## Notes

- The prior corpus is non-empty: kf42 exists. The negative-similarity-check
  cautionary tale is directly relevant — it documents how the *previous*
  autonomous run produced vh68, which on its face had a correct
  distinguishing-rule paragraph against kf42 but visually shared all the
  surface dimensions. The next state must explicitly diverge on visual
  signature (palette, sprite grain, "what is on the board") and core
  dynamic, not just on a verb-cardinality argument.
- Cn04 surprised me by having a 681-line source despite covering 5 levels
  and a non-trivial rotation-aware pixel-snap algorithm. The compactness
  comes from: (a) all sprite definitions inlined as a single `sprites`
  dict with `clone()` per level, (b) win-predicate as a single function
  that re-renders and counts unmatched `8`s, (c) no animation phases.
- Tu93's "walkable underlay" pattern (a single sprite with pixel value
  2 = walkable, queried by tag) is a load-bearing implementation idiom
  for any maze-based mechanic.
- Sb26 has 8 phase-tick state ints in step() — extreme but readable.
  For a 3-level generated game, 1-2 phase ticks (e.g. for a single
  commit animation) is the right amount of phase-machine machinery.
