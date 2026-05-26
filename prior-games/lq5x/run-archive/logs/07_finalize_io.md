# Step #07: finalize

## Inputs Consumed
- workspace/mechanic-pick.md, workspace/mechanic-spec.md, workspace/critique-pass.md, workspace/implement-summary.md, workspace/smoke-test-pass.md (all from prior states): used for the final report and the per-game mechanism-detail catalogue.
- prior-games/index.md (read-then-append): cumulative novelty floor.
- skills/finalize/{index-row-format,final-report-template,mechanism-detail-template,run-archive}.md.

## Deliverables Produced
- prior-games/index.md: one new row appended for `lq5x` (timestamp 2026-04-29T09:53:05Z, seed `(autonomous)`).
- prior-games/lq5x/mechanism-detail.md: the deep-view catalogue entry for this generated game; future runs' similarity-check will read it for any near-miss.
- workspace/final-report.md: the terminal deliverable per the template.
- (next step) prior-games/lq5x/run-archive/: workspace artefacts moved here.

## Notes
- mechanism-detail.md was authored BEFORE archiving (per the state spec's order requirement) so it could read workspace/mechanic-spec.md and final-report.md in place.
- The terminal action is the workspace archive, after which the workspace will be empty (except .gitkeep + recreated empty logs/) and ready for the next run.
