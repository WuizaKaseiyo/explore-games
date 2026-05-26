# Step #03: write_spec

## Inputs Consumed
- `workspace/mechanic-pick.md` (from #02): the 4-char ID `mw8p`,
  family `predator-prey-triangle`, mechanic description, novelty
  argument vs zk9p.
- `skills/code/spec-template.md`: 9-section spec contract.
- `skills/design-constraints/composition-and-tutorial.md`: L1/L2/L3
  structure with +1-or-+2 mechanic promotion.
- `skills/design-constraints/checklist.md`: 22-item gate, especially
  items 11 (mechanic inheritance), 12 (strict counterfactual
  necessity / no trivial fallback), 18 (difficulty floor/ceiling),
  20 (no chunky low-res), 21 (UI teaches), 22 (ACTION7 strict-undo
  or absent).
- `skills/design-constraints/core-knowledge-priors.md`: objectness +
  agentness only (no physics, no geometry/topology) — chosen to
  exploit the less-explored agentness corner of the prior cube.
- `skills/design-constraints/difficulty-rules.md`: L1 no-plan, L2
  moderate post-discovery plan, L3 trivial-heuristic-defeating plan.
- `skills/global/action-enum.md`: `[1, 2, 3, 4]` is the chosen
  subset; ACTION7 omitted per item 22.
- `skills/global/color-legend.md`: palette selection plan (10/12/14/
  13/15 for creatures+walls+exit; 2 background; 4 outline).
- `skills/code/universal-scaffold.md`: file layout + camera
  viewport rule (grid_size = (64, 64) = camera default, no
  per-level resize).
- `skills/code/novaengine-api.md`: Sprite / Level / Camera /
  NovaBaseGame signatures.
- `skills/conventions/reference-game-patterns.md`: step-counter HUD
  pattern; private `_steps_used` counter (NOT engine's
  `_action_count`, per fix_implementation lose-path pattern).
- `skills/mechanic-novelty/{similarity,negative-similarity}-check.md`:
  re-grounded against the full spec.

## Deliverables Produced
- `mechanic-spec.md`: full 9-section spec covering title, mechanic
  family, sprite roster (5 sprite kinds + step-counter HUD), L1/L2/L3
  layouts with witness traces, action mapping `[1, 2, 3, 4]`, HUD +
  internal state, win/lose conditions, and novelty re-grounding.

## Notes
- L1 layout: walls form 3-zone playfield (top corridor / middle
  chamber containing B / bottom corridor), connected only via col 7.
  The col-6 vertical barrier traps B in the middle chamber so B
  cannot reach A's col-7 traversal path — witness wins in 14 actions
  (7 RIGHT + 7 UP), step budget 25.
- L2 layout: open arena. C placed at (4, 3) BETWEEN A's pursuit-
  pull-on-B direction and B at (4, 5). On turn 1, B steps vertically
  to (4, 4); C also steps vertically to (4, 4) and removes B. The
  witness is 14 actions (7 RIGHT + 7 DOWN), step budget 30.
  CRITICAL DETAIL: the witness requires RIGHT-first (or any first
  action with |A.y-B.y| > |A.x-B.x|), since DOWN-first makes B's
  pursuit horizontal and C's vertical step misses. The witness
  selects the unique direction that triggers M2 at turn 1.
- L3 layout: row-6 wall barrier forces A to traverse row 7 to col 7
  before going up. C₁ sits on A's only first-move cell (forcing M3
  to fire at turn 1). C₂ sits at (3, 7) between A and B at (5, 7),
  so B's horizontal pursuit step lands C₂ onto B at (4, 7) on turn 1
  (M2 fires). Witness is 14 actions (7 RIGHT + 7 UP), step budget 35.
- Verified counterfactual necessity for every mechanic at every
  level (item 12): M1's pursuit fires every turn unconditionally;
  M2's removal of B is necessary to prevent B from catching A by
  turn 8 (L2) / turn 3 (L3); M3 is necessary because L3's only
  legal first move requires eating C₁.
- L3's "trivial heuristic that fails" per `difficulty-rules.md`
  § 2d: greedy-distance-toward-exit attempts UP from (3, 7) but
  hits the row-6 wall; witness instead routes via col 7. The
  alternate "don't eat C" heuristic also fails because C₂'s cell is
  the only forward-path cell at (3, 7).
- Visual taste: palette diverges from zk9p (which is yellow-
  dominant) and from kf42→vh68 ({4, 8, 9} family). Palette uses
  light-blue / orange-red / green-pink / maroon / purple / light-
  grey-background.
