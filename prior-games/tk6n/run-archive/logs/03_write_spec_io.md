# Step #03: write_spec

## Inputs Consumed
- mechanic-pick.md (from #02 pick_mechanic)
- skills/code/spec-template.md (read here)
- skills/code/universal-scaffold.md (read here for available_actions
  and naming conventions)
- skills/code/id-generation.md (read in pick_mechanic)
- skills/design-constraints/composition-and-tutorial.md (read in study)
- skills/design-constraints/difficulty-rules.md (read in study)
- skills/design-constraints/checklist.md (read in study; spec authored
  to pass items 1-22)

## Deliverables Produced
- mechanic-spec.md: full 9-section spec for game `tk6n`. Contains
  sprite roster, 3 levels with witness-required mechanics + 1-line
  necessity counterfactual per mechanic per level + witness
  solutions + difficulty justifications, action mapping (subset
  `[1, 2, 3, 4, 5]`), HUD/state, win/lose predicates, and novelty
  re-grounding against 6 closest priors.

## Notes
- L1 has 1 mechanic (M1: throw + outbound + homing-return + catch +
  target-light-on-overlap). L2 adds M2 (wall-height gating). L3 adds
  M3 (deterministic patrol guard with boomerang-freeze). +1 per level
  promotion satisfies `composition-and-tutorial.md`.
- The witness solutions are illustrative; the precise shortest
  sequence is to be validated in `smoke_test`. The spec deliberately
  marks the L1 witness as "estimated 17 actions" with step budget
  25 to leave generous margin per `difficulty-rules.md` § d.
- Per ACTION-7-strict-undo rule (`action-enum.md` § Slot 7), ACTION7
  is OMITTED from `available_actions`; the game has no undo.
- `wall_short` is introduced ONLY at L2; in L1 only `wall_tall` is
  present so the player learns the boomerang dynamic without
  wall-type confusion.
- `guard` and `guard_frozen` are introduced ONLY at L3 to keep L2
  focused on M2.
