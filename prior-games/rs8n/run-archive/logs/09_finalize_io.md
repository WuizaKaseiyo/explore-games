# Step #09: finalize

## Inputs Consumed
- mechanic-pick.md, mechanic-spec.md, critique-pass.md, implement-summary.md, smoke-test-pass.md (workspace deliverables of prior states)
- prior-games/index.md (current end before append; 45 rows)
- skills/finalize/{final-report-template.md, index-row-format.md, mechanism-detail-template.md, run-archive.md}

## Deliverables Produced
- prior-games/index.md: one row appended at the bottom: `| rs8n | line-reverse-sweep | Line-Reverse Sweeper — ... | 2026-05-08T19:12:48Z | (autonomous) |` (now 46 rows total).
- workspace/final-report.md: per the template — game ID, paths, mechanic paragraph (~140 words), action mapping, level summary, novelty note, index update confirmation.
- prior-games/rs8n/mechanism-detail.md: per the template — summary, action-mapping table, per-level mechanic-progression table with witnesses inline, win/lose conditions, internal state list, notable code patterns (sweep-phase machine, reverse-mapping by index, BlockingMode.BOUNDING_BOX trick, `ignore_collidable=True` for INTANGIBLE detection, perimeter sprite, avatar facing via white eye stripe).
- prior-games/rs8n/run-archive/: copy of every workspace .md + .py + smoke-frames PNGs + per-state IO logs + state_log.md.
- runs/2026-05-08T19-19-38/meta.json: status updated to `"completed"`, `finished_at` and `terminal_state` set.

## Notes
- Final layout under `prior-games/rs8n/`: `rs8n.py` (679 lines), `metadata.json`, `mechanism-detail.md`, `run-archive/{*.md, *.py, logs/*.md, smoke-frames/*.png}`.
- The terminal state per task-overview.md is `finalize`. Run is **complete**.
