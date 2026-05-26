# Step #09: finalize (terminal)

## Inputs Consumed
- workspace/mechanic-spec.md, workspace/mechanic-pick.md, workspace/smoke-test-pass.md (from prior states).
- skills/finalize/index-row-format.md, final-report-template.md, mechanism-detail-template.md, run-archive.md (from harness).
- prior-games/index.md (the cumulative corpus, to be appended).

## Deliverables Produced
- prior-games/index.md: one row appended for kg7p. (A previous execution of this run had already appended a row; the duplicate I added during this run's finalize was removed so the index has exactly one kg7p row matching the existing on-disk artefacts.)
- workspace/final-report.md: 9-section final report. Already on disk from the prior execution and verified accurate against the spec; no rewrite needed.
- prior-games/kg7p/mechanism-detail.md: deep-view catalogue entry. Already on disk and verified accurate; no rewrite needed.
- prior-games/kg7p/run-archive/: workspace deliverables (mechanic-pick, mechanic-spec, critique-revisions, critique-pass, implement-summary, smoke-test-pass, final-report, smoke-test-custom.py, smoke-frames/) and per-state IO logs co-located with the game source.

## Notes
- The run-archive directory already existed from a prior execution of the same run_id. This finalize step copied the current run's workspace deliverables and IO logs into the archive (overwriting matching filenames where they were updated this pass).
- The archive contains some stale IO logs from the prior execution (06_implement_io.md, 07_smoke_test_io.md, 08_finalize_io.md) that don't match my current numbering; these are left in place rather than deleted per the harness "do not clean up" rule.
- Index row appended: `| kg7p | beam-tether-haul | Beam-Tether Haul — avatar projects a directional tether beam that couples haulable blocks; ACTION5 toggles beam; L3 adds direction-locked blocks. | 2026-05-11T01:47:59Z | (autonomous) |` (from the prior execution; my own duplicate row was sed-removed to keep the index clean).
- Terminal state reached. meta.json will be updated to status=completed, terminal_state=finalize.
