# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02 pick_mechanic): ID `tg6w`, family `settle-pile-tilt`, distinguishing rules
- skills/code/spec-template.md (full): 9-section template
- skills/design-constraints/composition-and-tutorial.md (re-read): 3-level structure, +1-or-+2-per-level rule
- skills/design-constraints/difficulty-rules.md (re-read): per-level random-resistance/human-time/planning-depth/step-budget bullets
- skills/design-constraints/checklist.md (re-read): 21-item gate
- skills/code/universal-scaffold.md (re-read): naming convention, sprite-bank conventions, two-sprite-swap idiom, simultaneous-conflict resolution gotcha
- skills/code/novaengine-api.md (re-read): Sprite, Level, Camera, ACTION enum signatures
- skills/global/action-enum.md (re-read): pure-arrow [1,2,3,4] subset pattern
- skills/global/color-legend.md (re-read): palette indices

## Deliverables Produced
- mechanic-spec.md: 9-section spec, 237 lines. Sections:
  - §1 Title (working: "Settle-Pile Tilt")
  - §2 Mechanic family with three core priors (objectness, physics, geometry)
  - §3 Sprite roster: 8 sprite kinds (`wall_solid`, `wall_rim_yellow`, `wall_rim_orange`, `block_yellow`, `block_orange`, `target_yellow`, `target_orange`, `sticky_pad`) with 3×3 pixel matrices, plus `StepCounterHud` widget; sub-cell detail and sprite-role commentaries (checklist items 20, 21)
  - §4 Three levels with explicit ASCII layouts, mechanics-required (M1/M2/M3 inheritance + 1 new per level), per-mechanic counterfactual necessity (each citing the concrete cell that blocks alternate paths), witness solutions traced action-by-action with state at each step, and four-bullet difficulty justifications per level
  - §5 Action mapping: `[1, 2, 3, 4]` with semantic per slot
  - §6 HUD + internal state with persistent visual cues for every mutated state
  - §7 Win condition (every block on same-coloured target)
  - §8 Lose condition (step exhaustion + soft-lock detection on sticky-pad mismatched capture)
  - §9 Novelty note: distinguishing rules vs g50t, tu93, sp80, m0r0 (taxonomy) and zd7m, wt39, kn58, kx14, kp9z (priors); negative-similarity table

## Notes
- Three mechanics (M1, M2, M3) on a +1/+1 progression: L1 = 1, L2 = 2, L3 = 3. All carry forward; counterfactual necessity argued per (mechanic, level) pair with concrete cell citations.
- Action subset pure-arrow `[1, 2, 3, 4]` per the m0r0/tr87 "directional input IS the unusual mechanic" pattern.
- Witness lengths: L1 = 1, L2 = 2, L3 = 4. Step budgets 12/25/30 (generous over witness, non-shrinking across levels).
- L3 has a deliberately destructive trivial heuristic: greedy-DOWN-first traps orange at the sticky-pad (yellow's target), making the level unwinnable. This is the named heuristic that fails the post-discovery planning-depth gate. The witness goes LEFT first.
- Soft-lock detection added to §8 (lose() fires on the turn the level becomes unwinnable, e.g. orange caught at yellow-target). Explicitly avoids the `difficulty-rules.md` § 1 forbidden "no-win waiting room".
- Visual signature: dark off-black backdrop + yellow/orange blocks (off-white centre pip) + grey solid walls / coloured-rim walls (grey core) + magenta X-pattern sticky-pad. Distinct from every prior's palette per the negative-similarity table.
