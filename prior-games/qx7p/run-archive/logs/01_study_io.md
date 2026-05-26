# Step #01: study

## Inputs Consumed
- task-overview.md (from harness root): workflow framing, FSM, HITL=not allowed.
- states/study.md (from harness root): four reading inputs required before transition.
- skills/global/* (skill register): action-enum, color-legend, paths.
- skills/conventions/from-tech-report.md (skill register): distilled philosophy.
- skills/conventions/cross-cut-frequencies.md (skill register): pre-computed feature frequencies.
- skills/conventions/reference-game-patterns.md (skill register): cached patterns from past runs.
- skills/design-constraints/* (skill register): priors, forbidden, composition, checklist, difficulty rules.
- skills/mechanic-novelty/* (skill register): taxonomy + similarity checks + index format.
- skills/mechanism-details/<id>.md (skill register): per-game quick references.
- deep-analysis-3lvls/<id>/<id>-deep-analysis.md and level_{1,2,3}.png × 25 ids.
- 5 chosen reference source files in full.
- prior-games/index.md (corpus state of truth for novelty).

## Deliverables Produced
- None (per state spec — cached `reference-game-patterns.md` replaces per-run study notes).

## Notes
- Read mechanism-details summaries for all 25 reference games (faster than each deep-analysis; deep-analysis governs near-misses).
- Read 5 source files in full: cn04, sp80, m0r0, sk48, tr87. Spans:
  - cn04: click-select + arrows + ACTION5 rotate + connector-pixel snap.
  - sp80: click + arrows + ACTION5 commit + multi-phase animation step machine + tilt rotation level data + sprite "two-mode" tag-based collision.
  - m0r0: arrows + click toggle + mirrored quadrant axes + InteractionMode.INTANGIBLE merge + walls.
  - sk48: arrows + click switch + ACTION7 undo + trail-as-list + per-tile match indicators.
  - tr87: pure arrows (no click) + cycle-by-name-suffix + grammar-rules data per level + animation phase tick.
- prior-games/index.md is heavily saturated (29 priors). Many "obvious" mechanic families are claimed.

