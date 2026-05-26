# Step #09: finalize (terminal)

## Inputs Consumed
- workspace/mechanic-pick.md, workspace/mechanic-spec.md, workspace/smoke-test-pass.md (data sources for the index row, final report, and mechanism-detail)
- skills/finalize/{index-row-format, final-report-template, mechanism-detail-template, run-archive}
- prior-games/index.md (current end-of-file before append)

## Deliverables Produced
- prior-games/index.md: appended one row for `nh4w` with mechanic-family `arc-loft-shot`, autonomous seed.
- workspace/final-report.md: terminal report with mechanic, action mapping, level summary, novelty note, index-update confirmation.
- prior-games/nh4w/mechanism-detail.md: catalogue entry mirroring the format of skills/mechanism-details/<id>.md.
- prior-games/nh4w/run-archive/: full workspace copy (markdown deliverables, smoke-test-custom.py, logs/, smoke-frames/).
- runs/2026-05-10T12-58-16/meta.json: status updated to "completed", terminal_state="finalize", game_id="nh4w".

## Notes
- Index row appended via `echo >> index.md`, verified with `tail -1`.
- Run-archive populated under prior-games/nh4w/run-archive/ with 7 markdown deliverables, 1 python custom-checks file, 9 IO logs, 3 smoke-frame PNGs.
- The per-run workspace remains in place under runs/2026-05-10T12-58-16/ as the canonical run record.
