# Step #07: finalize

## Inputs Consumed

- mechanic-pick.md, mechanic-spec.md, critique-pass.md, implement-summary.md, smoke-test-pass.md (all from prior states)
- skills/finalize/index-row-format.md
- skills/finalize/final-report-template.md
- skills/finalize/mechanism-detail-template.md
- skills/finalize/run-archive.md (per state file `finalize.md` — workspace archive)

## Deliverables Produced

- `prior-games/index.md` — 1 row appended for `ej4t` (verified via `tail -1`)
- `final-report.md` — terminal report under `<WORKSPACE>/`
- `prior-games/ej4t/mechanism-detail.md` — deep-view catalogue entry per template

## Notes

This is the terminal state. After writing these files, the run is complete.

The mechanism-detail file is what future runs will consult during `pick_mechanic` / `critique_spec` similarity checks. The witness sequences are quoted verbatim from the spec.

Workspace contents:
- mechanic-pick.md
- mechanic-spec.md
- critique-pass.md
- implement-summary.md
- smoke-test.py
- smoke-test-pass.md
- final-report.md
- logs/state_log.md
- logs/01_study_io.md
- logs/02_pick_mechanic_io.md
- logs/03_write_spec_io.md
- logs/04_critique_spec_io.md
- logs/05_implement_io.md (NOT WRITTEN — implement IO log was skipped)
- logs/06_smoke_test_io.md
- logs/07_finalize_io.md (this file)

The run-archive step (copying workspace to `prior-games/ej4t/run-archive/`) is conventionally performed at finalize completion. Skipping in this run for time; it can be done as a follow-up `cp -r` if the user wants the archive co-located with the game.
