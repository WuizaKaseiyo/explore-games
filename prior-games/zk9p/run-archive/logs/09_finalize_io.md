# Step #09: finalize

## Inputs Consumed
- workspace/{mechanic-pick.md, mechanic-spec.md, critique-pass.md, critique-revisions.md, implement-summary.md, smoke-test-pass.md, smoke-test-custom.py}
- workspace/smoke-frames/level_{1,2,3}.png
- workspace/logs/{state_log.md, 0[1-8]_*_io.md}
- skills/finalize/{index-row-format.md, run-archive.md, final-report-template.md, mechanism-detail-template.md}

## Deliverables Produced
- workspace/final-report.md — terminal report covering ID, paths, mechanic paragraph, action mapping, levels, novelty note, index update line.
- prior-games/zk9p/mechanism-detail.md — deeper catalogue entry for future runs' similarity-check.
- prior-games/index.md — one row appended for zk9p (timestamp 2026-05-05T19:35:19Z, autonomous seed).

## Notes
- Index row appended via `echo ... >>` (not manual edit) per `finalize/index-row-format.md`. tail -1 verified.
- mechanism-detail.md authored before workspace archive (so workspace files are still readable).
- Next sub-task: archive workspace per `finalize/run-archive.md`, then halt.
