# Step #09: finalize (terminal)

## Inputs Consumed
- mechanic-spec.md (revised): for the index row's mechanic-family + description.
- mechanic-pick.md: for the game ID `vd3g`.
- smoke-test-pass.md: confirmation that the game passes all checks.
- skills/finalize/index-row-format.md, final-report-template.md, mechanism-detail-template.md, run-archive.md: per-skill instructions.

## Deliverables Produced
- `prior-games/index.md`: appended one row for vd3g.
- `<WORKSPACE>/final-report.md`: terminal report of the run.
- `prior-games/vd3g/mechanism-detail.md`: deep-view catalogue entry mirroring the 25 reference-game files in `skills/mechanism-details/`.
- `prior-games/vd3g/run-archive/`: copy of every workspace deliverable + smoke-frames + logs.

## Notes
- Index row appended via `echo >> ...` per the skill's procedure.
- `mechanism-detail.md` written BEFORE archiving so the workspace files were still available as source.
- Workspace itself stays in place at `runs/2026-05-07T19-59-42/workspace/` — the archive is a co-located copy under `prior-games/vd3g/run-archive/`.
- Per the run-harness skill: this is a terminal state; meta.json will be updated with `finished_at`, `status: completed`, `terminal_state: finalize`.
