# Step #09: finalize

## Inputs Consumed
- workspace/mechanic-pick.md
- workspace/mechanic-spec.md
- workspace/critique-pass.md
- workspace/implement-summary.md
- workspace/smoke-test-pass.md
- skills/finalize/{index-row-format, final-report-template, mechanism-detail-template, run-archive}.md

## Deliverables Produced
- prior-games/index.md: one row appended (bw7k | actor-replay-shade | description | 2026-05-09T02:02:36Z | (autonomous))
- prior-games/bw7k/mechanism-detail.md: deep-view catalogue entry mirroring the format of skills/mechanism-details/<id>.md (Summary, Action mapping, Per-level mechanic progression with witnesses, Win condition, Lose condition, Internal state, Notable code patterns)
- workspace/final-report.md: per `final-report-template.md` (game ID, paths, mechanic paragraph ~150 words, action mapping, level summary, novelty note vs tn36 and jd4q, index-update confirmation)
- prior-games/bw7k/run-archive/: full workspace + logs copied
- meta.json updated: status=completed, finished_at=2026-05-09T02:03:59Z, terminal_state=finalize, game_id=bw7k

## Notes
- Order honoured: index row appended first, then mechanism-detail.md authored, then run-archive populated, then final-report.md written.
- The per-run workspace at `runs/2026-05-09T01-02-39/workspace/` is preserved; the archive copy under `prior-games/bw7k/run-archive/` is the convenience co-location for users browsing the prior-games corpus.
- meta.json updated per the run-harness skill (status: running → completed; finished_at + terminal_state + game_id added).
