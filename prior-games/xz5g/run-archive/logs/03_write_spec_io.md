# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02): mechanic family, ID xz5g, novelty rules.
- skills/code/spec-template.md: 9-section spec contract.
- skills/code/universal-scaffold.md: file structure, style rules.
- skills/code/novaengine-api.md: API signatures (Sprite, Level, Camera, NovaBaseGame).
- skills/design-constraints/{checklist,composition-and-tutorial,difficulty-rules,core-knowledge-priors,forbidden-elements}.md
- skills/global/{action-enum,color-legend,paths}.md
- skills/conventions/reference-game-patterns.md (for HUD bar, tag-based dispatch, no-hidden-state cue rules)
- skills/mechanic-novelty/{similarity-check,negative-similarity-check}.md (re-run on full spec)
- prior-games/vt6q/vt6q.py (recent generated game; template for code structure)
- prior-games/{vy3k,hp9c,pv5q}/mechanism-detail.md (closest priors; distinguishing rules)
- skills/mechanism-details/cn04.md (closest reference)

## Deliverables Produced
- mechanic-spec.md: full 9-section spec.
  - §1 Title, §2 Mechanic family, §3 Sprite roster (avatar 6×6,
    avatar_target 6×6 ring, companion 6×6, companion_target 6×6
    ring, anchor_pin 4×4, pivot_marker 6×6 halo, direction_indicator
    4×4 widget, step_bar HUD).
  - §4 Levels with witnesses:
    - L1 (M1+M2): avatar (12, 32) → target (32, 12) via 1 CW around
      (32, 32). Witness 2 actions; budget 25.
    - L2 (M1+M2+M3 companion-deliver): avatar (8, 32) → target
      (56, 32); companion (32, 8) → target (32, 56). 2 CWs around
      (32, 32). Witness 3 actions; budget 30.
    - L3 (M1+M2+M3+M4 anchor-pin+M5 direction-toggle): avatar
      (32, 12) → target (32, 52); companion (8, 32) → target
      (56, 32); anchor_pin at (52, 32) blocks naive CW path,
      direction_indicator at (4, 4). Witness 4 actions (toggle to
      CCW, set pivot (32, 32), 2× ACTION5); budget 50.
  - §5 Action mapping: available_actions=[5, 6]. ACTION5 commit-rotate;
    ACTION6 click dispatches by target (widget toggle / no-op / set pivot).
  - §6 HUD + state. StepCounterHud + persistent _pivot, _direction, _steps_left, _pivot_marker, _dir_indicator.
  - §7 Win predicate (every target tag has matching rotatable at same coord).
  - §8 Lose: _steps_left exhaustion.
  - §9 Novelty note with vy3k / hp9c / cn04 / pv5q / qj4r-rj5w-wj7d
    distinguishing rules + negative-similarity check on full spec.

## Notes
- L1 is tutorial: random-stumble probability tolerated (~1/655 within
  budget). Per from-tech-report § 7, tutorial is allowed to be random-
  reachable.
- L2/L3 random-resistance lower (1/220 and ≪1/10000 respectively).
- L3 mechanic-count is L2+2 (anchor-pin + direction-toggle); per
  composition-and-tutorial allowed (1 OR 2 new mechanics per level).
- Win predicate uses size-matched 6×6 sprites for avatar/target so
  win = exact top-left coincidence; cleaner than 8×8 inset rule.
- Negative-similarity-check on full spec returns NOVEL: zero overlap
  on principal dimensions 6/7/8 vs vy3k.
- Discoverability cues spec'd:
  - pivot_marker halo persistent on _pivot cell.
  - direction_indicator widget pip-corner shows current direction.
  - anchor_pin highlights briefly on rejection.
  - rejected rotatable sprites flash pink for 1 frame.
- ACTION7 omitted (no undo verb needed); checklist 22 satisfied.
