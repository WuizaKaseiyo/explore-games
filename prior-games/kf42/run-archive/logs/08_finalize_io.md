# Step #08: finalize (terminal)

## Inputs Consumed
- workspace/mechanic-pick.md (from #02): ID `kf42`, family `tether-pawn-cycle`, seed `(autonomous)`.
- workspace/mechanic-spec.md (from #05 rev-2): full spec text.
- workspace/critique-pass.md (from #06): 16/16 PASS verdict.
- workspace/implement-summary.md (from #07): paths + line count + mechanic summary.
- prior-games/index.md: header-only; will append one row.
- prior-games/kf42/{kf42.py, metadata.json}: final artefacts (untouched).
- skills/finalize/{index-row-format.md, final-report-template.md, mechanism-detail-template.md, run-archive.md}: procedural references for this state.

## Deliverables Produced
- (Side effect) one row appended to prior-games/index.md at 2026-04-28T16:19:10Z.
- workspace/final-report.md: per the final-report-template (game ID, paths, mechanic paragraph, action mapping, level summary, novelty note, index-update confirmation).
- prior-games/kf42/mechanism-detail.md: per the mechanism-detail-template (summary, action mapping table, 3-row per-level progression, win/lose conditions, internal state, notable code patterns).
- prior-games/kf42/run-archive/: workspace deliverables + per-state IO logs moved here (separate Bash step below).

## Notes
- Terminal state. After this entry, no further entries to state_log.md per the run-harness skill (Step 4: "Stop. Do not append further `workspace/logs/state_log.md` entries.").
- Order followed exactly: index row → final-report → mechanism-detail → archive → recreate empty logs/.
