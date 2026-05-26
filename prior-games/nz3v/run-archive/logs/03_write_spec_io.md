# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02): family `rotor-sweep-walk`, ID `nz3v`, action subset [1,2,3,4], distinguishing rules
- code/spec-template.md (from state Skills): 9-section structure
- code/universal-scaffold.md (from state Skills): file structure + style rules + camera-viewport rule
- design-constraints/composition-and-tutorial.md (from study): exactly 3 levels, +1-or-+2 mechanic per level rule
- design-constraints/difficulty-rules.md (from study): per-level 4-bullet difficulty justification
- design-constraints/checklist.md (from study): 22-item checklist (especially items 11, 12, 18, 20, 22)

## Deliverables Produced
- mechanic-spec.md: Full 9-section spec.
  - §1 Title: Rotor-Sweep Walk.
  - §2 Mechanic family: priors used = geometry/topology + physics + objectness.
  - §3 Sprite roster: 6 sprite types (rotor 2×2, avatar/target/wall/stop_tile/counter_switch all 1×1) on 12×12 grid 5× scale.
  - §4 Level progression with explicit witness solutions per level (L1=18 actions, L2=15 actions, L3=15 actions); per-mechanic counterfactual necessity statements; per-level 4-bullet difficulty justification.
  - §5 Action mapping: pure cardinal walk [1,2,3,4]; ACTION7 absent (no undo).
  - §6 HUD/state: WedgeOverlay + RotorNotchOverlay + StepCounterHud; internal state includes _rotor_angle, _direction, _frozen_remaining, _actions_in_phase.
  - §7 Win: avatar at target → next_level().
  - §8 Lose: step budget exhausted OR stepped-into-dark-cell.
  - §9 Novelty note: closest taxonomy = g50t/lq5x; closest priors = fz5j/lq5x/vp6h/pf3w/xz5g/qz73; distinguishing rules per cousin.

## Notes
- Mechanic ladder: L1 has 1 mech (rotor-sweep), L2 adds stop-tile (+1=2), L3 adds counter-rotation switch (+1=3). Satisfies +1-or-+2 rule. All carry forward; all required by L3 witness.
- Per-mechanic counterfactual necessity: each level explicitly names walls/sprites/budget that block alternate paths.
- L1 step budget 28; L2 22; L3 22 — does NOT shrink.
- Rotation cadence K=6 actions per sector; K'=4 actions extension when stop-tile triggered.
- L3 witness routing initially had a wall-collision issue at gx=4 column; revised final layout uses walls (3,1)(3,2)(3,4), stop-tile (2,3), switch (4,5), avatar (1,1), target (1,10) — final witness 15 actions terminates at SW target via reversed (counter-clockwise) rotation NW→SW.
- Palette deliberately avoids the kf42→vh68 anti-pattern `{4,8,9}` cluster.
- Checklist item 20 awareness: 12×12 grid is "small logical grid" but each cell renders at 5× = 5×5 px; sprites have internal pixel detail (rotor 10×10 px, avatar/target/walls/tiles 5×5 px each with distinguishable pattern). Wedge tint paints background-only (palette 4 → 11), not sprite pixels — sprite detail preserved.
- Action subset [1,2,3,4] — the distinctive verb is the *environmental sweep*, not a player verb; deliberate divergence from most timing-walk priors that include ACTION5 or ACTION6.
- One concern to flag in critique: L3 witness path requires checking that walls (3,1)(3,2)(3,4) actually force the witness route (no shortcut via gx=2 column straight-down). The walls at (3,1)(3,2) prevent direct east-bound at gy=1,2 but gx=2 column is open. The witness goes (1,1)→(1,2)→(1,3)→(2,3)... which is OK because stop-tile is at (2,3) and must be triggered. A non-witness alternative like (1,1)→(2,1)→(2,2)→(2,3)... triggers stop-tile equivalently — so the witness might not be unique. critique_spec should evaluate.
