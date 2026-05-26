# Step #07: finalize

## Inputs Consumed
- task-overview.md, states/finalize.md.
- skills/finalize/{index-row-format, final-report-template, mechanism-detail-template, run-archive}.md.
- mechanic-pick.md, mechanic-spec.md, critique-pass.md, implement-summary.md, smoke-test-pass.md (assembled into final-report and mechanism-detail).
- prior-games/index.md (the cumulative index, just appended to).

## Deliverables Produced
- `final-report.md` (workspace) — terminal deliverable per template.
- `prior-games/hl4n/mechanism-detail.md` — deep catalogue entry mirroring `skills/mechanism-details/<id>.md` format.
- `prior-games/index.md` — one row appended for hl4n.
- `prior-games/hl4n/run-archive/` — full workspace archive: 7 .md files (mechanic-pick, mechanic-spec, critique-pass, implement-summary, smoke-test-pass, final-report) + 2 .py files (smoke-test-custom, smoke-test-universal) + `logs/` (state_log + 6 IO logs) + `smoke-frames/` (3 PNGs).

## Notes
- Index row appended via `echo >> ...` to avoid manual-edit risk; verified with `tail -1`.
- Game files (`hl4n.py`, `metadata.json`) NOT modified during finalize — they are immutable from the implement state onward.
- Workspace archive uses `cp` (not move); the canonical run record at `runs/2026-05-09T00-56-34/workspace/` stays in place per skill guidance.
- Future runs' negative-similarity-check will look up the L1 frame at `prior-games/hl4n/run-archive/smoke-frames/level_1.png` — confirmed present.
- Workflow complete.
