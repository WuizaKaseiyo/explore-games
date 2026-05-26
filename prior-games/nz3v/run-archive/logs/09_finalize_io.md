# Step #09: finalize (terminal)

## Inputs Consumed
- mechanic-pick.md, mechanic-spec.md, critique-pass.md, implement-summary.md, smoke-test-pass.md (workspace) — sources for index row + mechanism-detail.md + final-report.md.
- finalize/index-row-format.md, final-report-template.md, mechanism-detail-template.md, run-archive.md — output schemas.

## Deliverables Produced
- `prior-games/index.md`: appended one row for nz3v.
- `prior-games/nz3v/mechanism-detail.md`: catalogue entry mirroring the 25 reference-game format.
- `final-report.md` (workspace + archived): per template; references generated source, metadata, mechanic, levels, novelty.
- `prior-games/nz3v/run-archive/`: full workspace deliverables + per-state IO logs + smoke-frames/ copied in.
- `runs/2026-05-08T23-26-14/meta.json`: status=completed, finished_at set, terminal_state=finalize, game_id=nz3v.

## Notes
- Run completed end-to-end. All gates passed; no errors.
- Total state visits: study(1) + pick_mechanic(1) + write_spec(2) + critique_spec(2) + implement(1) + smoke_test(1) + finalize(1) = 9 transitions, well below all caps.
- Game `nz3v` (Rotor-Sweep Walk) is the 56th entry in the cumulative prior-games corpus.
