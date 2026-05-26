# Step #09: finalize

## Inputs Consumed
- workspace/mechanic-spec.md (revision 1)
- workspace/mechanic-pick.md
- workspace/critique-pass.md
- workspace/implement-summary.md
- workspace/smoke-test-pass.md
- skills/finalize/index-row-format.md, final-report-template.md, mechanism-detail-template.md, run-archive.md

## Deliverables Produced
- workspace/final-report.md — terminal deliverable; covers ID, paths, mechanic paragraph, action mapping, level summary, novelty note, index-update confirmation.
- prior-games/vp6h/mechanism-detail.md — deep catalogue entry mirroring `skills/mechanism-details/<id>.md` style; covers summary, action mapping, per-level mechanic progression with witness sequences inline, win/lose, internal state, notable code patterns.
- (Side effect) one row appended to `prior-games/index.md`: `| vp6h | shadow-cast-collect | ... | 2026-05-06T15:27:17Z | (autonomous) |`.
- prior-games/vp6h/run-archive/ populated with all workspace deliverables (.md + .py), per-state IO logs under `logs/`, and copied smoke-frames PNGs under `smoke-frames/`.
- runs/2026-05-06T14-16-36/meta.json updated: status=completed, terminal_state=finalize, game_id=vp6h.

## Notes
- prior-games corpus grew from 17 to 18 entries.
- Final game artifact: `prior-games/vp6h/vp6h.py` (462 lines), `metadata.json`.
- Workflow finished cleanly through 9 state visits (1 study → 1 pick_mechanic → 2 write_spec → 2 critique_spec → 1 implement → 1 smoke_test → 1 finalize).
