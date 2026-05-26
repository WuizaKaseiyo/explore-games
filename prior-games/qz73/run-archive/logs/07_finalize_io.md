# Step #07: finalize

## Inputs Consumed
- `workspace/mechanic-pick.md` — game_id, mechanic-family tag.
- `workspace/mechanic-spec.md` — for the mechanic paragraph + level summaries.
- `workspace/critique-pass.md` — confirmation the spec passed all 16 checklist items.
- `workspace/implement-summary.md` — file paths + line count.
- `workspace/smoke-test-pass.md` — confirmation all checks passed.
- `prior-games/index.md` — current state before append.
- `skills/finalize/{index-row-format,final-report-template,mechanism-detail-template,run-archive}.md`.

## Deliverables Produced
- One row appended to `prior-games/index.md` for `qz73`.
- `workspace/final-report.md`.
- `prior-games/qz73/mechanism-detail.md`.
- (Workspace will be moved to `prior-games/qz73/run-archive/` after this log is closed.)

## Notes
- Index row appended via `echo >>` per the
  `index-row-format.md` procedure (NOT via Edit, which would risk a file rewrite).
- Mechanism-detail authored to mirror the structure of the 25
  reference-game mechanism-details under `skills/mechanism-details/`,
  so future runs' similarity-checks have a deep-view to consult.
- Run-archive procedure executes after this IO log is sealed: move
  every workspace `.md` (and the smoke-frames + smoke_test_custom.py)
  + every `workspace/logs/*.md` into `prior-games/qz73/run-archive/`,
  then recreate empty `workspace/logs/`.
