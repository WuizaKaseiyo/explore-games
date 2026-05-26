# Step #09: finalize

## Inputs Consumed
- mechanic-spec.md (carried)
- mechanic-pick.md (carried)
- final-report-template.md (newly read)
- index-row-format.md (newly read)
- mechanism-detail-template.md (newly read)
- run-archive.md (newly read)
- prior-games/index.md (carried)

## Deliverables Produced
- prior-games/index.md (one new row appended for `hk7v`)
- prior-games/hk7v/mechanism-detail.md (new catalogue entry)
- workspace/final-report.md (terminal deliverable)
- prior-games/hk7v/run-archive/ (workspace deliverables + logs +
  smoke-frames copied for co-location with the artefact)

## Notes
- The terminal state's `step()` writes deliverables but does not
  modify `<game_id>.py` or `metadata.json`.
- Archive includes both `smoke-test-custom.py` and the underscore-
  named `smoke_test_custom.py` (importable copy used at runtime).
- Final state. No further state transitions.
