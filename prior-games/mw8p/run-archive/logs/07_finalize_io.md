# Step #07: finalize

## Inputs Consumed
- `workspace/mechanic-spec.md` (from #03): used for mechanism-detail.md
  per-level rows + the level witnesses copied into them.
- `workspace/final-report.md` (just written): mirrored summary text
  into the prior-game catalogue entry.
- `workspace/mechanic-pick.md` (from #02): family tag + ID for the
  index row.
- `skills/finalize/index-row-format.md`: exact append procedure.
- `skills/finalize/final-report-template.md`: 6-section template.
- `skills/finalize/mechanism-detail-template.md`: catalogue entry
  template.
- `skills/finalize/run-archive.md`: archive layout.

## Deliverables Produced
- `workspace/final-report.md`: terminal final report.
- `prior-games/index.md`: one new row appended (mw8p row at the bottom).
- `prior-games/mw8p/mechanism-detail.md`: catalogue entry (Summary,
  Action mapping, Per-level mechanic progression with witnesses,
  Win, Lose, Internal state, Notable code patterns).
- `prior-games/mw8p/run-archive/`: workspace .md + .py + logs +
  smoke-frames mirrored from `runs/<run_id>/workspace/`.
- `runs/<run_id>/meta.json`: status updated to `completed` with
  `finished_at` timestamp and `terminal_state = "finalize"`.

## Notes
- Index timestamp from `date -u +%Y-%m-%dT%H:%M:%SZ` at finalize
  time (Z-suffix UTC): `2026-05-11T02:17:20Z`. (Note: the clock on
  the harness host has drifted slightly relative to the run-id
  timestamp; this is normal — the run-id is a per-session ISO
  stamp, the index timestamp is a UTC "stamp at finalize" stamp.)
- The mechanism-detail.md file at
  `prior-games/mw8p/mechanism-detail.md` is the deep-view counterpart
  to the 25 reference-game files under `skills/mechanism-details/`,
  consulted by future runs' similarity-check.
- All workspace deliverables AND per-state IO logs AND smoke-frames
  copied into `prior-games/mw8p/run-archive/`. The original
  `runs/2026-05-11T02-16-16/workspace/` directory remains untouched
  per the harness-skill rule.
