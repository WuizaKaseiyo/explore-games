# Step #05: implement

## Inputs Consumed
- workspace/mechanic-spec.md (from #03, with §4-L3 updates after this state)
- skills/code/universal-scaffold.md
- skills/code/novaengine-api.md
- skills/global/* (palette, paths, action enum)

## Deliverables Produced
- prior-games/xv2b/xv2b.py (575 lines)
- prior-games/xv2b/metadata.json
- workspace/implement-summary.md

## Notes
- During smoke verification, found the originally-spec'd L3 (V_AB slit-0, target (0,5,10)) was unwinnable because back-flow B→A through V_AB once B>A traps water in oscillation. Redesigned: V_AB slit-15 + targets (0,5,3) + pump strict-necessity preserved (V_BC slit-8 still gates gravity strictly, so pump remains the only B→C path once B=8). Spec mechanic-spec.md §4 L3 + critique-pass.md §12 L3 row updated to match.
- All three witnesses verified by direct simulation: L1 wins at tick 16 (action 18); L2 wins at tick 8 (action 9); L3 wins at action 27.
- Instantiation + on_set_level + camera.render() all succeed without raising.
