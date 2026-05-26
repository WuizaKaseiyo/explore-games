# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02): game ID `rt9k`, family `torus-wrap-tone-cycle`, distinguishing-rule paragraphs
- skills/code/spec-template.md: 9-section structure
- skills/code/universal-scaffold.md: file-structure expectations
- skills/code/novaengine-api.md: Sprite/Level/Camera signatures
- skills/code/id-generation.md: confirms `rt9k` validity (re-checked)
- skills/design-constraints/composition-and-tutorial.md: 3-level structure, +1-or-+2 rule, no-hidden-mechanics
- skills/design-constraints/difficulty-rules.md: per-level (a) random-resistance, (b) human-tractable, (c) planning depth, (d) step budget
- skills/design-constraints/checklist.md: items 11, 12, 18, 19, 20, 21, 22 — answered in spec content
- skills/design-constraints/forbidden-elements.md: confirms no symbols/letters/clipart/cultural conventions
- skills/global/action-enum.md: ACTION7 strict-undo (confirmed omitted), ACTION5 freedom slot (confirmed unused — pure-arrow game)
- skills/global/color-legend.md: palette assignments (1, 3, 5, 6, 11, 14)

## Deliverables Produced
- mechanic-spec.md: full 9-section spec covering
  - § 1 working title (non-rendered)
  - § 2 mechanic family + §3.4 prior pair (geometry/topology + objectness)
  - § 3 sprite roster (avatar, wall_solid, filter_magenta/yellow/green, goal_plain, goal_yellow)
  - § 4 three levels with mechanics enumeration, per-mechanic counterfactual necessity, per-level witness, per-level (a)/(b)/(c)/(d) difficulty justification — L1 N=1, L2 N+2=3, L3 M+1=4 (filter colour additions are NOT new mechanics, same M3 rule)
  - § 5 action mapping `[1, 2, 3, 4]`, no clicks, no ACTION5, no ACTION7
  - § 6 HUD (StepCounterHud at pixel rows 60..63) and per-game state (`_tone`, `_steps_remaining`)
  - § 7 win predicate (goal-cell + tone-match)
  - § 8 lose predicate (steps-remaining == 0)
  - § 9 novelty note: closest taxonomy + prior-games near-misses with concrete distinguishing rules

## Notes
- Grid layout chosen as 16-wide × 15-tall logical (stride 4 ⇒ 64×60 pixel playfield), with 4-pixel HUD strip at the bottom of the 64×64 frame. This satisfies the universal scaffold's camera-viewport rule and mirrors `wa30`'s pattern (HUD overlays bottom row).
- L1 has 1 mechanic (M1 wrap), L2 adds 2 (M2 tone-cycle, M3 filter), L3 adds 1 (M4 goal-tone). Net: 1 → 3 → 4. Both deltas are within the +1-or-+2 rule. The L3 delta does NOT count "yellow filter" as a new mechanic — yellow vs green are the same M3 rule applied to different tone values, so the count is genuinely +1 (M4 alone).
- Counterfactual necessity per mechanic at each level was verified manually by tracing alternate paths: every winning path at L2 must pass `filter_green`; every winning path at L3 must pass both `filter_green` AND `filter_yellow` AND end with tone=yellow at goal. The reasoning is articulated in §4 per the strict per-mechanic table requirement of `checklist.md` item 12.
- Witness lengths: L1 = 9 actions; L2 = 16 actions; L3 = 19 actions. Step budgets: 30 / 50 / 70 — strictly non-decreasing across levels per `difficulty-rules.md` § 2.d.
- Visual signature deliberately diverges from the closest prior `pk4m` (red/blue duotone): `rt9k` uses {magenta=6, yellow=11, green=14} as the tone trio over {off-white=1, grey=3, black=5} infrastructure — six-colour palette with no overlap with pk4m's dominant pair. The avatar is a 4×4 sprite with a black-cored ring (internal pattern) rather than a 1×1 pawn — addressing checklist item 20 and the kf42→vh68 cautionary tale.
- Per checklist item 22 (ACTION7 strict-undo): undo would arguably be useful here (a wrong wrap is hard to undo without further wraps), but adding undo would change the game's planning identity by removing the "compose wraps to recover lost tone" challenge. ACTION7 is therefore omitted entirely — the action set [1,2,3,4] does not list 7.
- Witness for L3 was carefully designed so the goal-tone gate (M4) is *demonstrably* triggered: the witness reaches the goal cell at step 4 with tone=green, the gate refuses, the player wraps further, and only at step 19 does the tone match.
