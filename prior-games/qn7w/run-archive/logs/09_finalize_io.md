# Step #09: finalize (terminal)

## Inputs Consumed
- mechanic-spec.md, mechanic-pick.md, smoke-test-pass.md, implement-summary.md (workspace artefacts)
- skills/finalize/{final-report-template, index-row-format, mechanism-detail-template, run-archive}.md
- prior-games/index.md (current end of file)

## Deliverables Produced
- One row appended to `prior-games/index.md`:
  ```
  | qn7w | pulse-chain-eject | Pulse-Chain Eject — click pushers to fire momentum pulses through stationary ball-chains; only the terminal ball ejects per pulse. | 2026-05-08T00:11:56Z | (autonomous) |
  ```
- `workspace/final-report.md`
- `prior-games/qn7w/mechanism-detail.md` (deep-view catalogue entry for future similarity-checks)
- `prior-games/qn7w/run-archive/` populated with all workspace markdown + the smoke-test-custom.py + the rendered smoke-frames + the per-state IO logs.

## Notes
- Index row landed at the end of the file (verified via tail -1).
- mechanism-detail.md follows the same format as the 25 reference-game files under `skills/mechanism-details/`; the per-level table includes the witness sequence for each level (cap-3 levels per harness rule).
- run-archive contains: critique-pass.md, critique-revisions.md, final-report.md, implement-summary.md, mechanic-pick.md, mechanic-spec.md, smoke-test-custom.py, smoke-test-pass.md, smoke-frames/ (3 PNGs), and logs/ with 9 IO logs + state_log.md.
- Updated meta.json: status=completed, terminal_state=finalize, game_id=qn7w, finished_at=2026-05-08T00:11:56Z.
- Workflow halted (terminal). The next harness run will get a fresh `runs/<new_run_id>/workspace/` directory.
