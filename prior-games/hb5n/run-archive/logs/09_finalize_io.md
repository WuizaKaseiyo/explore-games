# Step #09: finalize (terminal)

## Inputs Consumed
- mechanic-spec.md, mechanic-pick.md, critique-pass.md, implement-summary.md, smoke-test-pass.md (from prior states)
- skills/finalize/index-row-format.md, final-report-template.md, mechanism-detail-template.md, run-archive.md (templates)

## Deliverables Produced
- One row appended to prior-games/index.md for hb5n.
- workspace/final-report.md: terminal report covering game ID, source paths, mechanic paragraph, action mapping, level summary, novelty note, index update confirmation.
- prior-games/hb5n/mechanism-detail.md: deep catalogue entry mirroring the 25 reference-game format; structure follows the template (Summary, Action mapping, Per-level mechanic progression with witnesses, Win condition, Lose condition, Internal state, Notable code patterns).
- prior-games/hb5n/run-archive/: full copy of workspace deliverables (`*.md`, `*.py`) + logs/ (per-state IO logs + state_log.md) + smoke-frames/ (level_{1,2,3}.png).
- meta.json updated: status="completed", finished_at, terminal_state="finalize", game_id="hb5n".

## Notes
- Terminal state. No outbound transitions.
- The generated game lives at prior-games/hb5n/{hb5n.py, metadata.json, mechanism-detail.md, run-archive/}.
- Per-run workspace remains at runs/2026-05-11T01-16-22/workspace/ as the canonical run record.
