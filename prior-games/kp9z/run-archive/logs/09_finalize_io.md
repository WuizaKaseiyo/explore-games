# Step #09: finalize

## Inputs Consumed
- workspace/mechanic-spec.md (mechanic, action mapping, level summary, novelty cross-references)
- workspace/mechanic-pick.md (game ID, family tag, novelty argument)
- workspace/smoke-test-pass.md (verification of the implementation)
- workspace/critique-pass.md (per-checklist verdict)
- workspace/implement-summary.md (file paths and line count)
- skills/finalize/* (templates: final-report, index-row-format, mechanism-detail, run-archive)

## Deliverables Produced
- workspace/final-report.md (the run's terminal report; uses the
  finalize/final-report-template format).
- prior-games/index.md: appended one row for kp9z (verified by tail -1).
- prior-games/kp9z/mechanism-detail.md: deep-view catalogue entry per
  finalize/mechanism-detail-template.
- prior-games/kp9z/run-archive/: workspace deliverables (.md + .py +
  smoke-frames/) + logs/ archived per finalize/run-archive.md.

## Notes
- Index-row timestamp generated via `date -u`: 2026-05-06T23:03:52Z.
- run-archive includes the smoke-frames directory so future runs can
  consult the rendered initial frames during their negative similarity
  check, per `mechanic-novelty/negative-similarity-check.md` (priors are
  expected to have frames at `prior-games/<id>/run-archive/smoke-frames/`).
- Cleaned __pycache__ left over from smoke-test imports.
