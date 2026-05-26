# Step #07: finalize

## Inputs Consumed
- mechanic-spec.md (full): for the per-game catalogue mechanism-detail
- workspace/final-report.md (drafting): pulled from the spec + smoke-test outputs
- skills/finalize/index-row-format.md, final-report-template.md, mechanism-detail-template.md, run-archive.md (full)
- prior-games/index.md (re-read at finalize time): noted concurrent insertion of `pf3w` between run start and finalize; verified family-level distinct from tg6w (wavefront-tick-on-click vs simultaneous-slide-on-arrow).

## Deliverables Produced
- prior-games/index.md: appended ONE row (tg6w | settle-pile-tilt | ... | 2026-05-07T15:33:50Z | (autonomous)).
- prior-games/tg6w/mechanism-detail.md: full per-game catalogue entry per `mechanism-detail-template.md` — Summary, Action mapping, Per-level mechanic progression with witness sequences, Win condition, Lose condition, Internal state, Notable code patterns.
- workspace/final-report.md: per `final-report-template.md` — generated game header, mechanic paragraph, action mapping, levels, novelty note, index update confirmation.
- prior-games/tg6w/run-archive/: populated with all workspace `.md` and `.py` deliverables, the `logs/` directory containing state_log.md + 7 IO logs, and `smoke-frames/` containing the 3 PNGs.

## Notes
- `prior-games/tg6w/` final layout: `tg6w.py`, `metadata.json`, `mechanism-detail.md`, `run-archive/{*.md, *.py, logs/*.md, smoke-frames/*.png}`.
- The concurrent insertion of `pf3w` during the run was a non-issue; pf3w's mechanic family (wavefront-converge-timing) does not overlap tg6w's settle-pile-tilt at the family level (different verb, different action subset, different core dynamic).
- All checklist items 1-21, all 9 universal smoke-test checks, all 4 custom checks, and the novelty re-check passed without revision loops. Final game state on the L3 witness sequence: `GameState.WIN`.
