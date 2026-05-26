# Step #09: finalize

## Inputs Consumed
- `mechanic-pick.md`, `mechanic-spec.md`, `final-report.md` (drafted),
  `prior-games/index.md` (existing rows for novelty cross-reference).
- `skills/finalize/{index-row-format, final-report-template, mechanism-detail-template, run-archive}.md`.

## Deliverables Produced
- `final-report.md` (workspace deliverable per template).
- One row appended to `prior-games/index.md`:
  `| qm4t | convex-pen-trap | Convex Pen Trap — click cells to drop vertex-posts whose convex hull defines a pen; ACTION5 commits and captures every critter strictly inside, scored against per-colour tally chips (forbidden critters and patrollers strike). | 2026-05-08T00:00:57Z | (autonomous) |`
- `prior-games/qm4t/mechanism-detail.md` (deep catalogue entry,
  matching `skills/mechanism-details/<id>.md` schema).
- `prior-games/qm4t/run-archive/` populated with workspace `*.md` and
  `*.py` deliverables, `logs/*.md` (per-state IO logs + state_log),
  and `smoke-frames/*.png`.
- `runs/2026-05-07T23-02-58/meta.json` updated:
  `status="completed"`, `finished_at="2026-05-08T00:01:00Z"`,
  `terminal_state="finalize"`, plus `game_id` and `mechanic_family`.

## Notes
- This is the terminal state; no further state entries on `state_log.md`
  beyond this finalize step.
- The per-run workspace at `runs/2026-05-07T23-02-58/` is preserved
  in place as the canonical record per the run-harness skill.
