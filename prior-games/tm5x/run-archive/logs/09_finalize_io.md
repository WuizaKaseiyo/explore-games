# Step #09: finalize (terminal)

## Inputs Consumed
- workspace/mechanic-pick.md, mechanic-spec.md, critique-pass.md,
  implement-summary.md, smoke-test-pass.md (all earlier-state
  deliverables — used as source material for final-report and
  mechanism-detail)
- prior-games/index.md (header verified, row appended)
- skills/finalize/{index-row-format,final-report-template,run-archive,
  mechanism-detail-template}.md

## Deliverables Produced
- prior-games/index.md: one row appended for tm5x
  (`thermal-aura-imprint` / `Aura-Imprint Polarity Stamp ...`).
- prior-games/tm5x/mechanism-detail.md: catalogue entry mirroring
  the format of skills/mechanism-details/<id>.md, including
  per-level witnesses, win/lose conditions, internal state,
  notable code patterns.
- workspace/final-report.md: per the final-report-template (game
  ID, paths, mechanic paragraph, action mapping, level summary,
  novelty note, index-row confirmation).
- prior-games/tm5x/run-archive/: full workspace archive
  (mechanic-pick, mechanic-spec, critique-pass, critique-revisions,
  implement-summary, smoke-test-pass, smoke-test-custom.py,
  smoke-runner.py, final-report, logs/{01..09}_*.md + state_log.md,
  smoke-frames/level_{1,2,3}.png).
- run/meta.json: status=completed; finished_at=2026-05-07T22:04:44Z;
  terminal_state=finalize; game_id=tm5x.

## Notes
- Run terminates here. Per run-harness skill: do not append further
  entries to state_log.md; do not modify the harness folder beyond
  this state's deliverables.
- The generated game is now part of the prior-games corpus and will
  be considered by future runs' similarity-check.
