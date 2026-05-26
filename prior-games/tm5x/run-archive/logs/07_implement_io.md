# Step #07: implement

## Inputs Consumed
- workspace/mechanic-spec.md (revised; from #05 write_spec)
- workspace/critique-pass.md (verdict from #06 critique_spec)
- skills/code/universal-scaffold.md (file structure + style rules)
- skills/code/novaengine-api.md (Sprite / Level / Camera / NovaBaseGame /
  RenderableUserDisplay / InteractionMode signatures)
- skills/code/id-generation.md (ID is `tm5x`, already verified)
- skills/global/{action-enum,color-legend,paths}.md
- Reference source styling: cn04, m0r0, sk48 (read in study state)

## Deliverables Produced
- prior-games/tm5x/tm5x.py (516 lines): full implementation
- prior-games/tm5x/metadata.json: schema-compliant metadata
- workspace/implement-summary.md: one-paragraph summary, file paths,
  smoke-verification checks

## Notes
- AST parse PASS; instantiation PASS (Tm5x() constructs, 3 levels,
  pawn-cell imprint reads +2 at L1 start, all expected state).
- The smoke-test gate from the implement state ("if instantiation
  raises, FIX") is satisfied.
- The runtime exec test of step() via `g.action = ...` failed because
  `action` is a read-only property on NovaBaseGame; the engine drives
  step() through its own scheduler, not by direct action-attribute
  assignment. This is the normal novaengine pattern; the smoke_test
  state will exercise step via the engine's intended entry point.
- __pycache__ directories cleaned.
- Transitioning to smoke_test.
