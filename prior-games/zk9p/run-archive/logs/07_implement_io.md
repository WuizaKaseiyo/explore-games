# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (#03/#05 deliverable)
- workspace/critique-pass.md (#06 sign-off)
- skills/code/{universal-scaffold.md, novaengine-api.md, id-generation.md, smoke-test-checks.md}
- skills/global/{action-enum.md, color-legend.md, paths.md}
- 5 reference source files re-skimmed mentally (cn04, m0r0, sb26, tu93, wa30 — for class structure, sprite-bank style, and step() dispatch convention)

## Deliverables Produced
- prior-games/zk9p/zk9p.py (434 lines)
- prior-games/zk9p/metadata.json
- workspace/implement-summary.md

## Notes
- Followed universal-scaffold.md style: meaningful sprite/method/constant names; class body order __init__ → on_set_level → helpers → step → _get_hidden_state.
- Camera viewport resized in on_set_level to match level grid_size (14/16/18) — checked at runtime smoke.
- Phase pursuer interaction toggled via InteractionMode.TANGIBLE/INTANGIBLE based on `self._tick % 2`; tick is incremented at the start of every pursuer-advancing action (ACTION1-4, plus ACTION5 in L3).
- Two-pass conflict resolution for pursuer movement (compute all destinations, then apply) per the universal-scaffold "simultaneous-conflict resolution gotcha".
- Floor sprite carries the visual richness (palette-3 speckle on palette-4 ground); entity sprites are single-cell palette-coloured 1×1 sprites.
- ACTION5 in L1/L2 is gated to a 1-unit step-counter drain with no pursuer advance (no-op verb); in L3 it's the spec's tick-skip (2-unit drain, 1 pursuer tick, no avatar move).
- Witness for L1 verified to terminate at 4 ACTION1 presses (one shorter than spec hand-trace; difficulty justification unaffected).
- Transition: smoke_test.
