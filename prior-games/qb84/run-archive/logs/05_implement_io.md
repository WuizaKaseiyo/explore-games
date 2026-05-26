# Step #05: implement

## Inputs Consumed
- workspace/mechanic-spec.md (from #03 write_spec): full 9-section spec.
- workspace/critique-pass.md (from #04 critique_spec): clean critique.
- skills/code/{universal-scaffold,novaengine-api,id-generation}.md.
- Reference style: re-using the cn04 source (read in #01 study) as
  the closest analogue — single click+arrow game with selection
  state, tag-based sprite querying, simple HUD bar.

## Deliverables Produced
- prior-games/qb84/qb84.py (519 lines).
- prior-games/qb84/metadata.json.
- workspace/implement-summary.md.

## Notes
- Found and fixed a peg-color reader bug at implement-time (read
  pixels[1,0] instead of pixels[1,1], because sticky peg's centre
  is the marker pixel, not the body colour).
- All 3 level witnesses verified end-to-end against the running
  engine: L1 advances after action 8, L2 after action 12 cumulative
  (L2's 12 actions), L3 reaches GameState.WIN after action 14
  (L3's 14 actions). Final L3 chain matches target exactly.
- Pair-peg propagation confirmed working: action 8 of L3 sets B5
  via direct swap and B6 via propagation in a single step.
- Sticky-peg lock confirmed: B3 in L3 locked after action 5.
- pycache cleaned.

