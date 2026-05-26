# Step #07: finalize

## Inputs Consumed
- workspace/mechanic-pick.md, mechanic-spec.md, critique-pass.md, implement-summary.md, smoke-test-pass.md (all per-state deliverables)
- skills/finalize/index-row-format.md
- skills/finalize/final-report-template.md
- skills/finalize/mechanism-detail-template.md
- skills/finalize/run-archive.md
- prior-games/index.md (to append the rt9k row)

## Deliverables Produced
- prior-games/index.md: appended one row for rt9k.
- workspace/final-report.md: per the final-report template (game ID, paths, mechanic paragraph, action mapping, level summary, novelty note, index-update confirmation).
- prior-games/rt9k/mechanism-detail.md: per the mechanism-detail template — summary + action mapping + per-level table with witnesses + win/lose conditions + internal state + notable code patterns. This becomes the deep counterpart to skills/mechanism-details/<id>.md for future runs' similarity-check.
- prior-games/rt9k/run-archive/: archived workspace deliverables (.md, .py), per-state IO logs (under logs/), and rendered smoke frames (under smoke-frames/).
- runs/<run_id>/meta.json: status updated to "completed", finished_at and terminal_state populated.

## Notes
- Index row uses the run's autonomous-mode marker `(autonomous)` for the seed column and a 140-char-bounded description ("Torus Wrap with Tone-Cycle — arrows walk an avatar on a torus playfield; each wrap-cross cycles tone through 3 hues; tone-coded filter walls and L3 goal-tone gate.").
- Archive layout follows finalize/run-archive.md verbatim. The `_smoke_runner.py` ad-hoc harness used during smoke_test was also archived for completeness (helpful for future debug). The PNG smoke frames are under run-archive/smoke-frames/ for browsing.
- Per the `Things You Must Not Do` section of the run-harness skill, no earlier run's directory was touched; `<game_id>.py` and `metadata.json` were not modified during finalize.
