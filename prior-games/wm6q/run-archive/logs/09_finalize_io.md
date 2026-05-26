# Step #09: finalize (terminal)

## Inputs Consumed
- `mechanic-pick.md`, `mechanic-spec.md`, `critique-pass.md`,
  `implement-summary.md`, `smoke-test-pass.md` (all from prior states)
- `prior-games/wm6q/{wm6q.py, metadata.json}` (from #07 implement)
- `prior-games/index.md` (existing 70-row index, before append)
- `skills/finalize/{index-row-format, final-report-template,
  mechanism-detail-template, run-archive}.md`

## Deliverables Produced
- One row appended to `prior-games/index.md` (`wm6q | edge-color-rotate-match
  | ...`).
- `workspace/final-report.md` — per-template final report.
- `prior-games/wm6q/mechanism-detail.md` — deep-view catalogue entry.
- `prior-games/wm6q/run-archive/` — copy of every workspace `.md` and `.py`
  deliverable, plus per-state IO logs and rendered smoke frames.

## Notes
- Order followed: `mechanism-detail.md` written BEFORE the archive copy
  (per the run-archive skill's order requirement).
- `wm6q.py` line count = 392 (after the implement state's small
  numpy-array fix during smoke_test). Consistent with `final-report.md`.
- Run terminates here.
