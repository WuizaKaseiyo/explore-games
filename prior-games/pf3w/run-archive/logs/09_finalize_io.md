# Step #09: finalize

## Inputs Consumed
- mechanic-pick.md, mechanic-spec.md, critique-pass.md, implement-summary.md, smoke-test-pass.md (workspace deliverables from prior states).
- skills/finalize/index-row-format.md, final-report-template.md, mechanism-detail-template.md, run-archive.md.
- prior-games/index.md (existing — appended to).
- prior-games/pf3w/pf3w.py, metadata.json (immutable artifacts).

## Deliverables Produced
- prior-games/index.md: appended one row for `pf3w` (date-stamped 2026-05-07T15:25:50Z, seed `(autonomous)`).
- prior-games/pf3w/mechanism-detail.md: deep-view catalogue entry covering summary, action mapping, per-level mechanic progression with witness sequences, win/lose conditions, internal state, and notable code patterns.
- runs/2026-05-07T14-33-55/workspace/final-report.md: terminal report with paths, mechanic summary, action mapping, level summary, novelty notes, and index update confirmation.
- prior-games/pf3w/run-archive/: workspace deliverables (.md + .py) copied into co-located archive; logs/ subdirectory contains the state_log + 9 per-state IO logs; smoke-frames/ subdirectory contains the 3 rendered initial-frame PNGs.

## Notes
- Order of writes: mechanism-detail.md FIRST (uses workspace files as source), then run-archive copy. Per the run-archive skill, this preserves the convenience of having all workspace artifacts inside the prior-games directory.
- runs/2026-05-07T14-33-55/meta.json updated: status="completed", finished_at, terminal_state="finalize", game_id="pf3w".
- Workflow finished; the workspace is sealed and the next harness run will get a fresh runs/<new_run_id>/workspace/ directory.
