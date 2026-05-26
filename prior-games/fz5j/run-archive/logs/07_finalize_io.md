# Step #07: finalize

## Inputs Consumed
- `workspace/mechanic-pick.md`, `workspace/mechanic-spec.md`, `workspace/critique-pass.md`, `workspace/implement-summary.md`, `workspace/smoke-test-pass.md` — all per prior states.
- `prior-games/index.md` — header + 11 prior rows.
- `skills/finalize/{index-row-format,final-report-template,mechanism-detail-template,run-archive}.md`.

## Deliverables Produced
- One row appended to `prior-games/index.md` for `fz5j`.
- `workspace/final-report.md` (now archived under `run-archive/`).
- `prior-games/fz5j/mechanism-detail.md`.
- Workspace fully archived under `prior-games/fz5j/run-archive/` (deliverables, logs, smoke-frames, smoke-test-custom.py, _smoke_runner.py).
- Workspace cleaned to empty (only `logs/` directory remains for the next run).
- `__pycache__/` directories cleaned both in workspace and in prior-games/fz5j/.

## Notes
- Run completed without entering `fix_implementation` (smoke test passed on first visit) and without re-entering `critique_spec` (critique passed on first visit). FSM trajectory: study → pick_mechanic → write_spec → critique_spec → implement → smoke_test → finalize.
- Final state of `prior-games/fz5j/` matches the run-archive layout in `skills/finalize/run-archive.md`.
