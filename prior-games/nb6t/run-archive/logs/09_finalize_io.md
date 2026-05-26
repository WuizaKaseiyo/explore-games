# Step #09: finalize (terminal)

## Inputs Consumed
- mechanic-spec.md (rev. 2): for the index row + final report content.
- final-report-template.md, index-row-format.md, mechanism-detail-template.md, run-archive.md: finalization templates.
- workspace deliverables (mechanic-pick, mechanic-spec, critique-pass, critique-revisions, implement-summary, smoke-test-pass, smoke-test-custom.py, smoke-frames/*.png).

## Actions Taken
1. Appended one row to `prior-games/index.md`:
   ```
   | nb6t | hinge-chain-reach | Articulated Reach — three rod-segments at independent hinges; rotate / extend / cycle active; carry-and-drop at L3 to deliver an item to a drop-zone. | 2026-05-07T22:11:11Z | (autonomous) |
   ```
   Verified via `tail -2`.
2. Wrote `final-report.md` to workspace per `final-report-template.md`.
3. Wrote `prior-games/nb6t/mechanism-detail.md` per `mechanism-detail-template.md` — the deep-view catalogue entry for this generated game.
4. Archived workspace artefacts to `prior-games/nb6t/run-archive/`:
   - All `*.md` and `*.py` workspace deliverables (including `smoke-test-custom.py`).
   - `smoke-frames/` PNG directory (the visual-sanity check renders).
   - All per-state IO logs and `state_log.md` under `run-archive/logs/`.
5. Updated `runs/2026-05-07T21-15-41/meta.json` to status `completed`, terminal_state `finalize`, finished_at `2026-05-07T22:11:11Z`.

## Deliverables Produced
- `runs/2026-05-07T21-15-41/workspace/final-report.md`
- `prior-games/nb6t/mechanism-detail.md`
- `prior-games/nb6t/run-archive/` (populated with 8 .md files, 1 .py file, smoke-frames/, and 9 logs).
- One row appended to `prior-games/index.md`.

## Notes
- Terminal state. No further state transitions.
- The per-run workspace at `runs/2026-05-07T21-15-41/workspace/` remains in place as the canonical run record; the archive copy under `prior-games/nb6t/run-archive/` is the convenience co-location.
