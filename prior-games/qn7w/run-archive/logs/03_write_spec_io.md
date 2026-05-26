# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (id `qn7w`, family `pulse-chain-eject`, distinguishing rules)
- skills/code/spec-template.md (9 sections required)
- skills/code/universal-scaffold.md (file structure, naming rules, camera-vs-grid_size guidance)
- skills/code/novaengine-api.md (Sprite/Level/Camera/RUD/NovaBaseGame method signatures)
- skills/design-constraints/composition-and-tutorial.md (3 levels, +1-or-+2 mechanics per level, no-hidden-mechanic)
- skills/design-constraints/checklist.md (16 items + 19/20/21 — UI-teaches, no-low-resolution, no-hidden-state)
- skills/design-constraints/difficulty-rules.md (random-resistance, human-time, planning-depth, step-budget per level)
- skills/conventions/reference-game-patterns.md (animation patterns, no-hidden-state, UI-teaches)

## Deliverables Produced
- mechanic-spec.md: complete 9-section spec.
  - §1 Title; §2 mechanic family with prior-category breakdown
  - §3 Sprite roster: 8 sprites (chain_ball_blue, chain_ball_yellow, pusher_knob, target_socket_blue, target_socket_yellow, junction_node, merge_pad, step_counter_hud HUD), with 6×6 native pixel detail and palette {0,4,5,9,10,11,12,14,15}
  - §4 Three levels with explicit per-level mechanic enumeration + counterfactual necessity per mechanic + witness solution (1, 2, 4 actions for L1/L2/L3) + difficulty justification (a-d) per level. Mechanic counts: L1=1, L2=2, L3=3 — strictly +1 per level (within +1-or-+2 rule).
  - §5 Action mapping: pure-click `[6]`; `_get_valid_actions` enumerates only pusher and junction centres
  - §6 HUD + per-game state: StepCounterHud + ChainModel structures + pending_animation phase machine
  - §7 Win condition: `_check_win()` over target_sockets + merge_pads
  - §8 Lose condition: budget exhaustion + proactive `_check_winnable()` to avoid soft-lock waiting room
  - §9 Novelty note: distinguishing rules vs ka59, r11l, vc33, lp85 (taxonomy) and vs vn8d, kp9z, bx84, kn58, gx7m, xn5p, rk7x (priors)

## Notes
- Pulse-eject design committed: terminal ball ejects exactly 1 ball-width (6 px) along chain axis; intermediates unmoved; chain shortens by one. Eject destination resolution: target_socket fill (matched colour required), merge_pad deposit, off-grid → consumed.
- Junction routing is a click-cycle: clicking the junction toggles the green tab (active branch). Visual cue is permanent (no hidden state).
- L3's merge_pad is the only target on the level; requires 2 deposits to fill. Forces the player to use both chains' up-branches converging on the same cell.
- L3 layout has chains converging at right-angle: chain A's vertical up-branch ejects upward to (20, 26); chain B's horizontal left-branch ejects leftward to (20, 26). Merge_pad sits at (20, 26).
- Soft-lock guard included in §8: proactive `_check_winnable()` fires `lose()` immediately if remaining chain balls cannot fill all targets, avoiding the no-win waiting room (per `difficulty-rules.md` § 1).
- Pending_animation phase machine modelled on tu93/sb26 patterns: brief flash propagates through chain over ~3-5 ticks before eject finalises and `complete_action()` runs.
- Step budgets: 6 / 16 / 30. Generous over witness (1×6, 8×, 7.5×); not shrinking across levels.
- All sprite shapes verified non-letter / non-digit / non-arrow (forbidden-elements check passes by construction).
