# Step #09: finalize (terminal)

## Inputs Consumed
- mechanic-pick.md, mechanic-spec.md, critique-pass.md, implement-summary.md, smoke-test-pass.md (workspace deliverables to date)
- skills/finalize/{index-row-format,final-report-template,mechanism-detail-template,run-archive}.md
- prior-games/index.md (target of the index-row append)

## Deliverables Produced
- prior-games/index.md: appended one row for `rj5w | axis-fold-mirror | ... | 2026-05-08T01:06:59Z | (autonomous)`.
- workspace/final-report.md: per `final-report-template.md`. Cites paths, mechanic paragraph, action mapping, level summary, novelty note, index update.
- prior-games/rj5w/mechanism-detail.md: per `mechanism-detail-template.md`. Deep-view catalogue entry that future runs' similarity-check will read.
- prior-games/rj5w/run-archive/: copy of every workspace `.md` and `.py` deliverable plus the smoke-frames/ subdir; per-state IO logs and the state-log under run-archive/logs/.
- The per-run workspace at runs/2026-05-08T01-25-06/workspace/ is left in place as the canonical run record.

## Notes
- Index row appended via `echo … >> prior-games/index.md`; tail-1 verified the row landed.
- `__pycache__` directories removed from prior-games/rj5w/ after the smoke test.
- The terminal-state directory layout is:
  ```
  prior-games/rj5w/
    rj5w.py
    metadata.json
    mechanism-detail.md
    run-archive/
      mechanic-pick.md
      mechanic-spec.md
      critique-pass.md
      critique-revisions.md
      implement-summary.md
      smoke-test-pass.md
      smoke-test-custom.py
      final-report.md
      smoke-frames/{level_1,level_2,level_3}.png
      logs/
        state_log.md
        01_study_io.md ... 08_smoke_test_io.md
  ```
- Workflow finished. State machine reaches terminal state.
